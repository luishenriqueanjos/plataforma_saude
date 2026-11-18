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


class TestMetasPersistenciaERegras(unittest.TestCase):
    """Testes unitarios e de persistencia SQLite das metas diarias (HU-03)."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_original = main.DB_PATH
        main.DB_PATH = os.path.join(self.temp_dir.name, "test_metas.db")
        main.init_db(reset=True)

    def tearDown(self):
        main.DB_PATH = self.db_original
        self.temp_dir.cleanup()

    def test_metas_iniciais_seed_ca03_1(self):
        """CA-03.1: Banco inicializado possui metas padrao de agua (2000 ml) e sono (8 h) zeradas."""
        # Preparar / Agir
        metas = main.obter_metas()

        # Conferir
        self.assertEqual(set(metas.keys()), {"agua", "sono"})
        self.assertEqual(metas["agua"]["valor_diario"], 2000.0)
        self.assertEqual(metas["agua"]["progresso_atual"], 0.0)
        self.assertEqual(metas["agua"]["percentual"], 0)
        self.assertEqual(metas["sono"]["valor_diario"], 8.0)
        self.assertEqual(metas["sono"]["progresso_atual"], 0.0)
        self.assertEqual(metas["sono"]["percentual"], 0)

    def test_cadastrar_e_atualizar_metas_respeita_contrato_ca03_1(self):
        """CA-03.1: Cadastrar ou redefinir metas grava na tabela META, reinicia progresso e segue contrato."""
        # Preparar
        esperado = carregar_exemplo("metas-criadas.json")
        main.registrar_progresso_meta({"tipo": "agua", "quantidade": 500})

        # Agir
        status, resposta = main.salvar_metas({"agua_ml": 2500, "sono_horas": 7.5})

        # Conferir
        self.assertEqual(status, 201)
        self.assertEqual(set(resposta.keys()), set(esperado.keys()))
        self.assertEqual(
            set(resposta["metas"]["agua"].keys()),
            set(esperado["metas"]["agua"].keys()),
        )
        self.assertEqual(resposta["metas"]["agua"]["valor_diario"], 2500.0)
        self.assertEqual(resposta["metas"]["agua"]["progresso_atual"], 0.0)
        self.assertEqual(resposta["metas"]["agua"]["percentual"], 0)
        self.assertEqual(resposta["metas"]["sono"]["valor_diario"], 7.5)
        self.assertEqual(resposta["metas"]["sono"]["progresso_atual"], 0.0)

        conn = main.get_connection()
        total_linhas = conn.execute(
            "SELECT COUNT(*) AS total FROM META WHERE usuario_id = 1"
        ).fetchone()["total"]
        conn.close()
        self.assertEqual(total_linhas, 2)

    def test_recusa_metas_invalidas_ca03_3(self):
        """CA-03.3: Recusa valores ausentes, nao numericos, zero ou negativos sem alterar metas salvas."""
        # Preparar
        esperado = carregar_exemplo("erro-meta-invalida.json")
        casos_invalidos = [
            {"agua_ml": 0, "sono_horas": 8},
            {"agua_ml": -250, "sono_horas": 8},
            {"agua_ml": 2000, "sono_horas": 0},
            {"agua_ml": 2000, "sono_horas": -1},
            {"agua_ml": "", "sono_horas": 8},
            {"agua_ml": None, "sono_horas": 8},
            {"agua_ml": "abc", "sono_horas": 8},
        ]

        # Agir / Conferir
        for payload in casos_invalidos:
            status, resposta = main.salvar_metas(payload)
            self.assertEqual(status, 400)
            self.assertEqual(set(resposta.keys()), set(esperado.keys()))
            self.assertEqual(resposta["erro"], "Meta inválida.")

        metas_atuais = main.obter_metas()
        self.assertEqual(metas_atuais["agua"]["valor_diario"], 2000.0)
        self.assertEqual(metas_atuais["sono"]["valor_diario"], 8.0)

    def test_atualizar_progresso_agua_sono_e_teto_percentual_ca03_2(self):
        """CA-03.2: Acumula progresso de agua e sono e limita percentual visual em 100%."""
        # Preparar
        main.salvar_metas({"agua_ml": 2000, "sono_horas": 8})

        # Agir
        status_agua, resp_agua = main.registrar_progresso_meta(
            {"tipo": "agua", "quantidade": 250}
        )
        status_sono, resp_sono = main.registrar_progresso_meta(
            {"tipo": "SONO", "quantidade": 2}
        )
        status_teto, resp_teto = main.registrar_progresso_meta(
            {"tipo": "agua", "quantidade": 2000}
        )

        # Conferir
        self.assertEqual(status_agua, 200)
        self.assertEqual(resp_agua["metas"]["agua"]["progresso_atual"], 250.0)
        self.assertEqual(resp_agua["metas"]["agua"]["percentual"], 12)

        self.assertEqual(status_sono, 200)
        self.assertEqual(resp_sono["metas"]["sono"]["progresso_atual"], 2.0)
        self.assertEqual(resp_sono["metas"]["sono"]["percentual"], 25)

        self.assertEqual(status_teto, 200)
        self.assertEqual(resp_teto["metas"]["agua"]["progresso_atual"], 2250.0)
        self.assertEqual(resp_teto["metas"]["agua"]["percentual"], 100)

    def test_recusa_progresso_invalido_ou_meta_inexistente_ca03_3(self):
        """CA-03.3: Valida tipo, quantidade positiva e erro 404 quando nao ha meta cadastrada."""
        # Preparar / Agir / Conferir - tipo invalido
        status_tipo, resp_tipo = main.registrar_progresso_meta(
            {"tipo": "cafe", "quantidade": 100}
        )
        self.assertEqual(status_tipo, 400)
        self.assertEqual(resp_tipo["erro"], "Tipo inválido.")

        # Preparar / Agir / Conferir - quantidades invalidas
        for quantidade in (0, -100, "", None, "dez"):
            status_qtd, resp_qtd = main.registrar_progresso_meta(
                {"tipo": "agua", "quantidade": quantidade}
            )
            self.assertEqual(status_qtd, 400)
            self.assertEqual(resp_qtd["erro"], "Valor inválido.")

        # Preparar / Agir / Conferir - meta ausente no banco (404)
        conn = main.get_connection()
        conn.execute("DELETE FROM META WHERE usuario_id = 1")
        conn.commit()
        conn.close()

        status_404, resp_404 = main.registrar_progresso_meta(
            {"tipo": "agua", "quantidade": 250}
        )
        self.assertEqual(status_404, 404)
        self.assertEqual(resp_404["erro"], "Meta não encontrada.")


class TestMetasIntegracaoHTTP(unittest.TestCase):
    """Testes de integracao HTTP reais para GET/POST /api/metas e /api/metas/progresso."""

    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.db_original = main.DB_PATH
        main.DB_PATH = os.path.join(self.temp_dir.name, "test_metas_http.db")
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

    def _requisitar(self, path, method="GET", payload=None):
        data = None
        headers = {}
        if payload is not None:
            data = json.dumps(payload).encode("utf-8")
            headers["Content-Type"] = "application/json"

        req = urllib.request.Request(
            f"http://127.0.0.1:{self.port}{path}",
            data=data,
            headers=headers,
            method=method,
        )
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status, json.loads(resp.read().decode("utf-8"))
        except urllib.error.HTTPError as err:
            try:
                return err.code, json.loads(err.read().decode("utf-8"))
            finally:
                err.close()

    def test_fluxo_http_metas_diarias_e_progresso(self):
        """Valida GET /api/metas, POST /api/metas (201/400) e POST /api/metas/progresso (200/400)."""
        # Preparar
        exemplo_sucesso = carregar_exemplo("metas-criadas.json")
        exemplo_erro = carregar_exemplo("erro-meta-invalida.json")

        # Agir / Conferir - GET inicial
        status_get, metas_iniciais = self._requisitar("/api/metas")
        self.assertEqual(status_get, 200)
        self.assertEqual(metas_iniciais["agua"]["valor_diario"], 2000.0)
        self.assertEqual(metas_iniciais["sono"]["valor_diario"], 8.0)

        # Agir / Conferir - POST /api/metas valido (201)
        status_post, criado = self._requisitar(
            "/api/metas",
            method="POST",
            payload={"agua_ml": 2000, "sono_horas": 8},
        )
        self.assertEqual(status_post, 201)
        self.assertEqual(criado, exemplo_sucesso)

        # Agir / Conferir - POST /api/metas/progresso valido (200)
        status_prog, prog = self._requisitar(
            "/api/metas/progresso",
            method="POST",
            payload={"tipo": "agua", "quantidade": 250},
        )
        self.assertEqual(status_prog, 200)
        self.assertEqual(prog["metas"]["agua"]["progresso_atual"], 250.0)

        # Agir / Conferir - GET apos progresso confirma persistencia
        status_apos, metas_apos = self._requisitar("/api/metas")
        self.assertEqual(status_apos, 200)
        self.assertEqual(metas_apos["agua"]["progresso_atual"], 250.0)

        # Agir / Conferir - POST /api/metas invalido (400)
        status_err, erro = self._requisitar(
            "/api/metas",
            method="POST",
            payload={"agua_ml": 0, "sono_horas": 8},
        )
        self.assertEqual(status_err, 400)
        self.assertEqual(erro, exemplo_erro)

        # Agir / Conferir - POST /api/metas/progresso invalido (400)
        status_prog_err, prog_err = self._requisitar(
            "/api/metas/progresso",
            method="POST",
            payload={"tipo": "agua", "quantidade": -50},
        )
        self.assertEqual(status_prog_err, 400)
        self.assertEqual(prog_err["erro"], "Valor inválido.")
