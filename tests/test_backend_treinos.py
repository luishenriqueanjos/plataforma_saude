import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer

# Adiciona o diretorio raiz do projeto ao sys.path para importar main.py
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import main  # noqa: E402


class TestBancoDadosETreinos(unittest.TestCase):
    """Testes automatizados de persistencia SQLite, regras de negocio e API HTTP (HU-01, HU-02, RNF-01)."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_original = main.DB_PATH
        main.DB_PATH = os.path.join(self.temp_dir.name, "test_treinos.db")
        main.init_db(reset=True)

    def tearDown(self):
        main.DB_PATH = self.db_original
        self.temp_dir.cleanup()

    def test_esquema_banco_e_privacidade_rnf01(self):
        """Verifica criacao das tabelas do modelo de dados e conformidade com RNF-01 (sem dados civis sensiveis)."""
        conn = main.get_connection()
        cur = conn.cursor()

        tabelas = {
            row["name"]
            for row in cur.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            ).fetchall()
        }
        for esperada in ("USUARIO", "TREINO", "EXERCICIO", "SERIE", "META"):
            self.assertIn(esperada, tabelas)

        colunas_usuario = [
            row["name"]
            for row in cur.execute("PRAGMA table_info(USUARIO)").fetchall()
        ]
        self.assertEqual(colunas_usuario, ["id"])
        for campo_sensivel in ("cpf", "rg", "nome", "email", "telefone", "endereco"):
            self.assertNotIn(campo_sensivel, [c.lower() for c in colunas_usuario])

        usuario_padrao = cur.execute("SELECT id FROM USUARIO WHERE id = 1").fetchone()
        self.assertIsNotNone(usuario_padrao)
        conn.close()

    def test_seed_inicial_e_listagem_ca01_3_ca02_3(self):
        """Verifica se o treino inicial de demonstracao e persistido e retornado com volume de 600 kg."""
        treinos = main.obter_treinos()
        self.assertEqual(len(treinos), 1)
        primeiro = treinos[0]
        self.assertEqual(primeiro["data"], "2026-10-15")
        self.assertEqual(primeiro["exercicio"], "Supino reto")
        self.assertEqual(primeiro["total_series"], 3)
        self.assertEqual(primeiro["volume_total"], 600.0)

    def test_calculo_volume_rn01_ca02_1(self):
        """Valida a regra RN-01: soma do produto (repeticoes * carga) de todas as series."""
        series = [
            {"repeticoes": 12, "carga": 25.0},
            {"repeticoes": 10, "carga": 30.0},
            {"repeticoes": 8, "carga": 35.5},
        ]
        # 12*25 (300) + 10*30 (300) + 8*35.5 (284) = 884.0
        self.assertAlmostEqual(main.calcular_volume(series), 884.0)

    def test_salvar_novo_treino_caminho_principal_ca01_1_ca01_3(self):
        """Valida o salvamento de um novo treino valido e sua persistencia na listagem."""
        payload = {
            "data": "2026-11-11",
            "exercicio": "Agachamento",
            "series": [
                {"repeticoes": 10, "carga": 40},
                {"repeticoes": 10, "carga": 45},
                {"repeticoes": 8, "carga": 50},
            ],
        }
        status, resposta = main.salvar_novo_treino(payload)
        self.assertEqual(status, 201)
        self.assertEqual(resposta["exercicio"], "Agachamento")
        self.assertEqual(resposta["total_series"], 3)
        self.assertEqual(resposta["volume_total"], 1250.0)

        historico = main.obter_treinos()
        self.assertEqual(len(historico), 2)
        self.assertEqual(historico[0]["exercicio"], "Agachamento")
        self.assertEqual(historico[0]["volume_total"], 1250.0)

    def test_recusa_dados_incompletos_ca01_2(self):
        """Valida recusa (HTTP 400) quando data, exercicio ou carga estao ausentes."""
        casos_incompletos = [
            {"data": "", "exercicio": "Supino reto", "series": [{"repeticoes": 10, "carga": 20}]},
            {"data": "2026-11-11", "exercicio": "", "series": [{"repeticoes": 10, "carga": 20}]},
            {"data": "2026-11-11", "exercicio": "Supino reto", "series": []},
            {
                "data": "2026-11-11",
                "exercicio": "Supino reto",
                "series": [
                    {"repeticoes": 10, "carga": 20},
                    {"repeticoes": 10, "carga": ""},
                ],
            },
        ]
        for dados in casos_incompletos:
            status, resposta = main.salvar_novo_treino(dados)
            self.assertEqual(status, 400)
            self.assertIn("erro", resposta)

        # Garante que nenhum treino incompleto foi gravado alem do seed inicial
        self.assertEqual(len(main.obter_treinos()), 1)

    def test_recusa_valores_menores_ou_iguais_a_zero_ca02_2_rn02(self):
        """Valida recusa (HTTP 400) quando repeticoes ou carga sao menores ou iguais a zero."""
        casos_invalidos = [
            {
                "data": "2026-11-11",
                "exercicio": "Remada",
                "series": [{"repeticoes": 0, "carga": 20}],
            },
            {
                "data": "2026-11-11",
                "exercicio": "Remada",
                "series": [{"repeticoes": 10, "carga": 0}],
            },
            {
                "data": "2026-11-11",
                "exercicio": "Remada",
                "series": [{"repeticoes": 10, "carga": -15}],
            },
        ]
        for dados in casos_invalidos:
            status, resposta = main.salvar_novo_treino(dados)
            self.assertEqual(status, 400)
            self.assertEqual(resposta["erro"], "Dados inválidos.")

        self.assertEqual(len(main.obter_treinos()), 1)


class TestIntegracaoAPIHTTP(unittest.TestCase):
    """Testes de integracao das rotas HTTP do servidor PlataformaHandler."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_original = main.DB_PATH
        main.DB_PATH = os.path.join(self.temp_dir.name, "test_api_treinos.db")
        main.init_db(reset=True)

        self.server = HTTPServer(("127.0.0.1", 0), main.PlataformaHandler)
        self.port = self.server.server_port
        self.base_url = f"http://127.0.0.1:{self.port}"
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join(timeout=2)
        main.DB_PATH = self.db_original
        self.temp_dir.cleanup()

    def test_get_pagina_inicial_html(self):
        with urllib.request.urlopen(f"{self.base_url}/") as resp:
            self.assertEqual(resp.status, 200)
            conteudo = resp.read().decode("utf-8")
            self.assertIn("Plataforma de Saúde", conteudo)

    def test_get_e_post_api_treinos(self):
        # 1. Consulta inicial
        with urllib.request.urlopen(f"{self.base_url}/api/treinos") as resp:
            self.assertEqual(resp.status, 200)
            lista = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(len(lista), 1)

        # 2. Criacao de novo treino via POST /api/treinos
        novo = {
            "data": "2026-11-11",
            "exercicio": "Desenvolvimento",
            "series": [
                {"repeticoes": 10, "carga": 16},
                {"repeticoes": 10, "carga": 16},
                {"repeticoes": 10, "carga": 16},
            ],
        }
        req = urllib.request.Request(
            f"{self.base_url}/api/treinos",
            data=json.dumps(novo).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            self.assertEqual(resp.status, 201)
            criado = json.loads(resp.read().decode("utf-8"))
            self.assertEqual(criado["volume_total"], 480.0)

        # 3. Recusa via POST /api/treinos com carga vazia
        invalido = {
            "data": "2026-11-11",
            "exercicio": "Desenvolvimento",
            "series": [{"repeticoes": 10, "carga": ""}],
        }
        req_invalido = urllib.request.Request(
            f"{self.base_url}/api/treinos",
            data=json.dumps(invalido).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with self.assertRaises(urllib.error.HTTPError) as ctx:
            urllib.request.urlopen(req_invalido)
        self.assertEqual(ctx.exception.code, 400)
        ctx.exception.close()


if __name__ == "__main__":
    unittest.main()
