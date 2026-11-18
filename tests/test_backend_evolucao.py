import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request
from http.server import HTTPServer
from pathlib import Path

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

import main  # noqa: E402

EXEMPLOS_DIR = Path(ROOT_DIR) / "contrato" / "exemplos"


def carregar_exemplo(nome):
    return json.loads((EXEMPLOS_DIR / nome).read_text(encoding="utf-8"))


class TestMultiExercicioEvolucaoESono(unittest.TestCase):
    """Testes para treino multi-exercicio, evolucao de cargas e registro direto de sono."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_original = main.DB_PATH
        main.DB_PATH = os.path.join(self.temp_dir.name, "test_evolucao.db")
        main.init_db(reset=True)

    def tearDown(self):
        main.DB_PATH = self.db_original
        self.temp_dir.cleanup()

    def test_salvar_e_listar_treino_com_multiplos_exercicios(self):
        """DT-03: Salva e recupera multiplos exercicios e series livres em uma unica sessao."""
        # Preparar
        payload = {
            "data": "2026-11-18",
            "exercicios": [
                {
                    "nome": "Agachamento",
                    "series": [
                        {"repeticoes": 10, "carga": 60},
                        {"repeticoes": 8, "carga": 70},
                    ],
                },
                {
                    "nome": "Leg press",
                    "series": [
                        {"repeticoes": 12, "carga": 120},
                    ],
                },
            ],
        }

        # Agir
        status, resposta = main.salvar_novo_treino(payload)
        historico = main.obter_treinos()

        # Conferir
        self.assertEqual(status, 201)
        self.assertEqual(resposta["total_exercicios"], 2)
        self.assertEqual(resposta["total_series"], 3)
        # (10*60 + 8*70) + (12*120) = 1160 + 1440 = 2600.0
        self.assertEqual(resposta["volume_total"], 2600.0)
        self.assertEqual(historico[0]["total_exercicios"], 2)
        self.assertEqual(
            [ex["nome"] for ex in historico[0]["exercicios"]],
            ["Agachamento", "Leg press"],
        )

    def test_recusa_treino_multiexercicio_com_campo_invalido(self):
        """RN-02: Se qualquer exercicio ou serie estiver invalido, recusa toda a sessao."""
        # Preparar
        payload = {
            "data": "2026-11-18",
            "exercicios": [
                {"nome": "Supino reto", "series": [{"repeticoes": 10, "carga": 20}]},
                {"nome": "Agachamento", "series": [{"repeticoes": 10, "carga": 0}]},
            ],
        }

        # Agir
        status, resposta = main.salvar_novo_treino(payload)

        # Conferir
        self.assertEqual(status, 400)
        self.assertEqual(resposta["erro"], "Dados inválidos.")
        self.assertEqual(len(main.obter_treinos()), 1)

    def test_evolucao_cargas_insuficiente_e_suficiente_ca04_1_ca04_2(self):
        """CA-04.1 e CA-04.2: Indica dados insuficientes com 1 sessao e serie cronologica com >= 2."""
        # Preparar / Agir (apenas 1 treino do seed inicial)
        evolucao_inicial = main.obter_evolucao_cargas("Supino reto")

        # Conferir CA-04.2
        self.assertFalse(evolucao_inicial["dados_suficientes"])
        self.assertEqual(evolucao_inicial["total_registros"], 1)
        self.assertIn("2 sessões", evolucao_inicial["mensagem"])

        # Preparar segunda sessao em data posterior e conferir CA-04.1
        main.salvar_novo_treino(
            {
                "data": "2026-10-22",
                "exercicios": [
                    {
                        "nome": "Supino reto",
                        "series": [
                            {"repeticoes": 10, "carga": 22},
                            {"repeticoes": 10, "carga": 23},
                            {"repeticoes": 8, "carga": 25},
                        ],
                    }
                ],
            }
        )

        # Agir
        evolucao = main.obter_evolucao_cargas("Supino reto")
        esperado = carregar_exemplo("evolucao-exercicio.json")

        # Conferir
        self.assertEqual(set(evolucao.keys()), set(esperado.keys()))
        self.assertTrue(evolucao["dados_suficientes"])
        self.assertEqual(evolucao["total_registros"], 2)
        self.assertEqual(evolucao["resumo"]["carga_inicial"], 20.0)
        self.assertEqual(evolucao["resumo"]["carga_atual"], 25.0)
        self.assertEqual(evolucao["resumo"]["variacao_kg"], 5.0)
        self.assertEqual(evolucao["resumo"]["variacao_percentual"], 25.0)
        self.assertEqual(
            [p["data"] for p in evolucao["pontos"]],
            ["2026-10-15", "2026-10-22"],
        )

    def test_registrar_sono_modo_definir_substitui_sem_somar(self):
        """Registro de sono em modo 'definir' grava horas dormidas diretamente."""
        # Preparar
        main.salvar_metas({"agua_ml": 2000, "sono_horas": 8})

        # Agir
        st1, r1 = main.registrar_progresso_meta(
            {"tipo": "sono", "quantidade": 7.5, "modo": "definir"}
        )
        st2, r2 = main.registrar_progresso_meta(
            {"tipo": "sono", "quantidade": 8, "modo": "definir"}
        )

        # Conferir
        self.assertEqual(st1, 200)
        self.assertEqual(r1["metas"]["sono"]["progresso_atual"], 7.5)
        self.assertEqual(r1["metas"]["sono"]["percentual"], 94)

        self.assertEqual(st2, 200)
        self.assertEqual(r2["metas"]["sono"]["progresso_atual"], 8.0)
        self.assertEqual(r2["metas"]["sono"]["percentual"], 100)


class TestEvolucaoIntegracaoHTTP(unittest.TestCase):
    """Testa GET /api/treinos/evolucao e UI sem tags internas via HTTP."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_original = main.DB_PATH
        main.DB_PATH = os.path.join(self.temp_dir.name, "test_evolucao_http.db")
        main.init_db(reset=True)

        self.server = HTTPServer(("127.0.0.1", 0), main.PlataformaHandler)
        self.port = self.server.server_address[1]
        self.thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        main.DB_PATH = self.db_original
        self.temp_dir.cleanup()

    def test_http_evolucao_e_html_limpo(self):
        # Preparar / Agir
        with urllib.request.urlopen(
            f"http://127.0.0.1:{self.port}/api/treinos/evolucao?exercicio=Supino%20reto",
            timeout=5,
        ) as resp:
            status_api = resp.status
            dados = json.loads(resp.read().decode("utf-8"))

        with urllib.request.urlopen(
            f"http://127.0.0.1:{self.port}/", timeout=5
        ) as resp_html:
            html = resp_html.read().decode("utf-8")

        # Conferir
        self.assertEqual(status_api, 200)
        self.assertEqual(dados["exercicio"], "Supino reto")
        self.assertFalse(dados["dados_suficientes"])
        self.assertNotIn("HU-0", html)
        self.assertIn("Registrar sono", html)
        self.assertIn("+ Adicionar exercício", html)
