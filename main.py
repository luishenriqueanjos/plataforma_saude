import json
import os
import sqlite3
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "treinos.db")
HTML_PATH = os.path.join(BASE_DIR, "prototipo", "index.html")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(reset=False):
    if reset and os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = get_connection()
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE IF NOT EXISTS USUARIO (
            id INTEGER PRIMARY KEY AUTOINCREMENT
        );

        CREATE TABLE IF NOT EXISTS TREINO (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES USUARIO(id)
        );

        CREATE TABLE IF NOT EXISTS EXERCICIO (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            treino_id INTEGER NOT NULL,
            nome TEXT NOT NULL,
            FOREIGN KEY (treino_id) REFERENCES TREINO(id)
        );

        CREATE TABLE IF NOT EXISTS SERIE (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            exercicio_id INTEGER NOT NULL,
            repeticoes INTEGER NOT NULL,
            carga REAL NOT NULL,
            FOREIGN KEY (exercicio_id) REFERENCES EXERCICIO(id)
        );

        CREATE TABLE IF NOT EXISTS META (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id INTEGER NOT NULL,
            tipo TEXT NOT NULL,
            valor_diario REAL NOT NULL,
            FOREIGN KEY (usuario_id) REFERENCES USUARIO(id)
        );
        """
    )

    user = cur.execute("SELECT id FROM USUARIO WHERE id = 1").fetchone()
    if not user:
        cur.execute("INSERT INTO USUARIO (id) VALUES (1)")

    count = cur.execute("SELECT COUNT(*) as total FROM TREINO").fetchone()["total"]
    if count == 0:
        cur.execute("INSERT INTO TREINO (usuario_id, data) VALUES (1, '2026-10-15')")
        treino_id = cur.lastrowid
        cur.execute(
            "INSERT INTO EXERCICIO (treino_id, nome) VALUES (?, ?)",
            (treino_id, "Supino reto"),
        )
        exercicio_id = cur.lastrowid
        for _ in range(3):
            cur.execute(
                "INSERT INTO SERIE (exercicio_id, repeticoes, carga) VALUES (?, 10, 20.0)",
                (exercicio_id,),
            )

    conn.commit()
    conn.close()


def calcular_volume(series):
    """RN-01: Volume total = soma de (repeticoes * carga) de cada serie."""
    return sum(s["repeticoes"] * s["carga"] for s in series)


def obter_treinos():
    conn = get_connection()
    cur = conn.cursor()
    treinos_rows = cur.execute(
        "SELECT id, data FROM TREINO WHERE usuario_id = 1 ORDER BY id DESC"
    ).fetchall()

    resultado = []
    for t in treinos_rows:
        ex = cur.execute(
            "SELECT id, nome FROM EXERCICIO WHERE treino_id = ? LIMIT 1", (t["id"],)
        ).fetchone()
        if not ex:
            continue

        series_rows = cur.execute(
            "SELECT repeticoes, carga FROM SERIE WHERE exercicio_id = ? ORDER BY id ASC",
            (ex["id"],),
        ).fetchall()
        series = [
            {"repeticoes": s["repeticoes"], "carga": s["carga"]} for s in series_rows
        ]
        resultado.append(
            {
                "id": t["id"],
                "data": t["data"],
                "exercicio": ex["nome"],
                "total_series": len(series),
                "volume_total": calcular_volume(series),
                "series": series,
            }
        )

    conn.close()
    return resultado


def salvar_novo_treino(dados):
    data_treino = (dados.get("data") or "").strip()
    nome_exercicio = (dados.get("exercicio") or "").strip()
    series_input = dados.get("series") or []

    if not data_treino or not nome_exercicio or not series_input:
        return 400, {
            "erro": "Dados incompletos.",
            "detalhe": "Informe a data, o exercício e as séries antes de salvar o treino.",
        }

    series_validadas = []
    for s in series_input:
        try:
            rep = int(s.get("repeticoes"))
            carga = float(s.get("carga"))
        except (TypeError, ValueError):
            return 400, {
                "erro": "Dados incompletos.",
                "detalhe": "Informe a carga de todas as séries antes de salvar o treino.",
            }

        if rep <= 0 or carga <= 0:
            return 400, {
                "erro": "Dados inválidos.",
                "detalhe": "As repetições e a carga de todas as séries devem ser maiores que zero.",
            }

        series_validadas.append({"repeticoes": rep, "carga": carga})

    volume_total = calcular_volume(series_validadas)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO TREINO (usuario_id, data) VALUES (1, ?)", (data_treino,))
    treino_id = cur.lastrowid

    cur.execute(
        "INSERT INTO EXERCICIO (treino_id, nome) VALUES (?, ?)",
        (treino_id, nome_exercicio),
    )
    exercicio_id = cur.lastrowid

    for s in series_validadas:
        cur.execute(
            "INSERT INTO SERIE (exercicio_id, repeticoes, carga) VALUES (?, ?, ?)",
            (exercicio_id, s["repeticoes"], s["carga"]),
        )

    conn.commit()
    conn.close()

    return 201, {
        "id": treino_id,
        "data": data_treino,
        "exercicio": nome_exercicio,
        "total_series": len(series_validadas),
        "volume_total": volume_total,
        "series": series_validadas,
        "mensagem": "Treino registrado com sucesso.",
    }


class PlataformaHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            with open(HTML_PATH, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        elif self.path == "/api/treinos":
            self._send_json(200, obter_treinos())
        else:
            self._send_json(404, {"erro": "Rota não encontrada."})

    def do_POST(self):
        if self.path == "/api/treinos":
            length = int(self.headers.get("Content-Length", 0))
            raw = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
            try:
                dados = json.loads(raw)
            except json.JSONDecodeError:
                dados = {}
            status, resposta = salvar_novo_treino(dados)
            self._send_json(status, resposta)
        else:
            self._send_json(404, {"erro": "Rota não encontrada."})


if __name__ == "__main__":
    if "--reset" in sys.argv:
        init_db(reset=True)
        print("Banco de dados restaurado para o estado inicial da demonstracao.")
    else:
        init_db(reset=False)
        porta = 5000
        print(f"Servidor iniciado em http://localhost:{porta}")
        servidor = HTTPServer(("127.0.0.1", porta), PlataformaHandler)
        servidor.serve_forever()
