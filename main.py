import json
import math
import os
import sqlite3
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse

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
            progresso_atual REAL NOT NULL DEFAULT 0,
            FOREIGN KEY (usuario_id) REFERENCES USUARIO(id)
        );
        """
    )

    # Garante a coluna progresso_atual caso o banco tenha sido criado na versao anterior
    colunas = [row["name"] for row in cur.execute("PRAGMA table_info(META)").fetchall()]
    if "progresso_atual" not in colunas:
        cur.execute(
            "ALTER TABLE META ADD COLUMN progresso_atual REAL NOT NULL DEFAULT 0"
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

    count_metas = cur.execute("SELECT COUNT(*) as total FROM META").fetchone()["total"]
    if count_metas == 0:
        cur.execute(
            "INSERT INTO META (usuario_id, tipo, valor_diario, progresso_atual) VALUES (1, 'agua', 2000.0, 0.0)"
        )
        cur.execute(
            "INSERT INTO META (usuario_id, tipo, valor_diario, progresso_atual) VALUES (1, 'sono', 8.0, 0.0)"
        )

    conn.commit()
    conn.close()


def calcular_volume(series):
    """RN-01: Volume total = soma de (repeticoes * carga) de cada serie."""
    return sum(s["repeticoes"] * s["carga"] for s in series)


def _validar_series(series_input):
    if not isinstance(series_input, list) or not series_input:
        return None, (
            400,
            {
                "erro": "Dados incompletos.",
                "detalhe": "Informe a data, o exercício e as séries antes de salvar o treino.",
            },
        )

    series_validadas = []
    for s in series_input:
        if not isinstance(s, dict):
            return None, (
                400,
                {
                    "erro": "Dados incompletos.",
                    "detalhe": "Informe a carga de todas as séries antes de salvar o treino.",
                },
            )
        try:
            rep = int(s.get("repeticoes"))
            carga = float(s.get("carga"))
        except (TypeError, ValueError):
            return None, (
                400,
                {
                    "erro": "Dados incompletos.",
                    "detalhe": "Informe a carga de todas as séries antes de salvar o treino.",
                },
            )

        if not math.isfinite(carga) or rep <= 0 or carga <= 0:
            return None, (
                400,
                {
                    "erro": "Dados inválidos.",
                    "detalhe": "As repetições e a carga de todas as séries devem ser maiores que zero.",
                },
            )

        series_validadas.append({"repeticoes": rep, "carga": carga})

    return series_validadas, None


def obter_treinos():
    conn = get_connection()
    cur = conn.cursor()
    treinos_rows = cur.execute(
        "SELECT id, data FROM TREINO WHERE usuario_id = 1 ORDER BY id DESC"
    ).fetchall()

    resultado = []
    for t in treinos_rows:
        ex_rows = cur.execute(
            "SELECT id, nome FROM EXERCICIO WHERE treino_id = ? ORDER BY id ASC",
            (t["id"],),
        ).fetchall()
        if not ex_rows:
            continue

        exercicios = []
        todas_series = []
        for ex in ex_rows:
            series_rows = cur.execute(
                "SELECT repeticoes, carga FROM SERIE WHERE exercicio_id = ? ORDER BY id ASC",
                (ex["id"],),
            ).fetchall()
            series = [
                {"repeticoes": s["repeticoes"], "carga": s["carga"]}
                for s in series_rows
            ]
            todas_series.extend(series)
            exercicios.append(
                {
                    "nome": ex["nome"],
                    "total_series": len(series),
                    "volume_total": calcular_volume(series),
                    "series": series,
                }
            )

        resumo_nome = (
            exercicios[0]["nome"]
            if len(exercicios) == 1
            else " + ".join(e["nome"] for e in exercicios)
        )
        resultado.append(
            {
                "id": t["id"],
                "data": t["data"],
                "exercicio": resumo_nome,
                "exercicios": exercicios,
                "total_exercicios": len(exercicios),
                "total_series": len(todas_series),
                "volume_total": calcular_volume(todas_series),
                "series": todas_series,
            }
        )

    conn.close()
    return resultado


def salvar_novo_treino(dados):
    data_treino = (dados.get("data") or "").strip()
    modo_multi = isinstance(dados.get("exercicios"), list)

    if not data_treino:
        return 400, {
            "erro": "Dados incompletos.",
            "detalhe": "Informe a data, o exercício e as séries antes de salvar o treino.",
        }

    exercicios_validados = []
    if modo_multi:
        exercicios_input = dados.get("exercicios") or []
        if not exercicios_input:
            return 400, {
                "erro": "Dados incompletos.",
                "detalhe": "Adicione pelo menos um exercício com séries antes de salvar o treino.",
            }
        for ex in exercicios_input:
            if not isinstance(ex, dict):
                return 400, {
                    "erro": "Dados incompletos.",
                    "detalhe": "Informe o nome e as séries de cada exercício antes de salvar.",
                }
            nome_ex = (ex.get("nome") or ex.get("exercicio") or "").strip()
            if not nome_ex:
                return 400, {
                    "erro": "Dados incompletos.",
                    "detalhe": "Informe o nome de todos os exercícios antes de salvar o treino.",
                }
            series_validadas, erro = _validar_series(ex.get("series"))
            if erro:
                return erro
            exercicios_validados.append({"nome": nome_ex, "series": series_validadas})
    else:
        nome_exercicio = (dados.get("exercicio") or "").strip()
        series_input = dados.get("series") or []
        if not nome_exercicio or not series_input:
            return 400, {
                "erro": "Dados incompletos.",
                "detalhe": "Informe a data, o exercício e as séries antes de salvar o treino.",
            }
        series_validadas, erro = _validar_series(series_input)
        if erro:
            return erro
        exercicios_validados.append(
            {"nome": nome_exercicio, "series": series_validadas}
        )

    todas_series = [s for ex in exercicios_validados for s in ex["series"]]
    volume_total = calcular_volume(todas_series)

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO TREINO (usuario_id, data) VALUES (1, ?)", (data_treino,))
    treino_id = cur.lastrowid

    exercicios_salvos = []
    for ex in exercicios_validados:
        cur.execute(
            "INSERT INTO EXERCICIO (treino_id, nome) VALUES (?, ?)",
            (treino_id, ex["nome"]),
        )
        exercicio_id = cur.lastrowid
        for s in ex["series"]:
            cur.execute(
                "INSERT INTO SERIE (exercicio_id, repeticoes, carga) VALUES (?, ?, ?)",
                (exercicio_id, s["repeticoes"], s["carga"]),
            )
        exercicios_salvos.append(
            {
                "nome": ex["nome"],
                "total_series": len(ex["series"]),
                "volume_total": calcular_volume(ex["series"]),
                "series": ex["series"],
            }
        )

    conn.commit()
    conn.close()

    resumo_nome = (
        exercicios_salvos[0]["nome"]
        if len(exercicios_salvos) == 1
        else " + ".join(ex["nome"] for ex in exercicios_salvos)
    )
    resposta = {
        "id": treino_id,
        "data": data_treino,
        "exercicio": resumo_nome,
        "total_series": len(todas_series),
        "volume_total": volume_total,
        "series": todas_series,
        "mensagem": "Treino registrado com sucesso.",
    }
    if modo_multi:
        resposta["exercicios"] = exercicios_salvos
        resposta["total_exercicios"] = len(exercicios_salvos)
    return 201, resposta


def obter_evolucao_cargas(nome_exercicio=None):
    """Agrega serie historica de cargas por exercicio em ordem cronologica (CA-04.1 e CA-04.2)."""
    conn = get_connection()
    cur = conn.cursor()
    rows = cur.execute(
        """
        SELECT
            t.id AS treino_id,
            t.data AS data,
            e.id AS exercicio_id,
            e.nome AS exercicio,
            s.repeticoes AS repeticoes,
            s.carga AS carga
        FROM TREINO t
        JOIN EXERCICIO e ON e.treino_id = t.id
        JOIN SERIE s ON s.exercicio_id = e.id
        WHERE t.usuario_id = 1
        ORDER BY t.data ASC, t.id ASC, e.id ASC, s.id ASC
        """
    ).fetchall()
    conn.close()

    contagem_por_nome = {}
    nome_canonico = {}
    for r in rows:
        chave = r["exercicio"].strip().lower()
        if chave not in nome_canonico:
            nome_canonico[chave] = r["exercicio"].strip()
            contagem_por_nome[chave] = set()
        contagem_por_nome[chave].add(r["exercicio_id"])

    exercicios_disponiveis = sorted(nome_canonico.values(), key=lambda n: n.lower())

    exercicio_alvo = (nome_exercicio or "").strip()
    if exercicio_alvo:
        chave_alvo = exercicio_alvo.lower()
        exercicio_alvo = nome_canonico.get(chave_alvo, exercicio_alvo)
    elif exercicios_disponiveis:
        melhor_chave = max(
            contagem_por_nome,
            key=lambda k: (
                len(contagem_por_nome[k]),
                -ord(nome_canonico[k][0].lower()),
            ),
        )
        exercicio_alvo = nome_canonico[melhor_chave]

    grupos = {}
    ordem_grupos = []
    for r in rows:
        if (
            not exercicio_alvo
            or r["exercicio"].strip().lower() != exercicio_alvo.lower()
        ):
            continue
        chave_grupo = (r["data"], r["treino_id"], r["exercicio_id"])
        if chave_grupo not in grupos:
            grupos[chave_grupo] = {
                "treino_id": r["treino_id"],
                "data": r["data"],
                "exercicio": r["exercicio"],
                "series": [],
            }
            ordem_grupos.append(chave_grupo)
        grupos[chave_grupo]["series"].append(
            {"repeticoes": r["repeticoes"], "carga": float(r["carga"])}
        )

    pontos = []
    for chave_grupo in ordem_grupos:
        g = grupos[chave_grupo]
        cargas = [s["carga"] for s in g["series"]]
        pontos.append(
            {
                "treino_id": g["treino_id"],
                "data": g["data"],
                "exercicio": g["exercicio"],
                "carga_maxima": max(cargas),
                "carga_media": round(sum(cargas) / len(cargas), 2),
                "volume_total": round(calcular_volume(g["series"]), 2),
                "total_series": len(g["series"]),
            }
        )

    dados_suficientes = len(pontos) >= 2
    if pontos:
        carga_inicial = pontos[0]["carga_maxima"]
        carga_atual = pontos[-1]["carga_maxima"]
        maior_carga = max(p["carga_maxima"] for p in pontos)
        variacao_kg = round(carga_atual - carga_inicial, 2)
        variacao_percentual = (
            round((variacao_kg / carga_inicial) * 100, 1) if carga_inicial > 0 else 0.0
        )
        resumo = {
            "carga_inicial": carga_inicial,
            "carga_atual": carga_atual,
            "maior_carga": maior_carga,
            "variacao_kg": variacao_kg,
            "variacao_percentual": variacao_percentual,
        }
    else:
        resumo = {
            "carga_inicial": 0.0,
            "carga_atual": 0.0,
            "maior_carga": 0.0,
            "variacao_kg": 0.0,
            "variacao_percentual": 0.0,
        }

    return {
        "exercicio": exercicio_alvo,
        "exercicios_disponiveis": exercicios_disponiveis,
        "total_registros": len(pontos),
        "dados_suficientes": dados_suficientes,
        "mensagem": (
            ""
            if dados_suficientes
            else "Registre pelo menos 2 sessões deste exercício para visualizar o gráfico de evolução de cargas."
        ),
        "resumo": resumo,
        "pontos": pontos,
    }


def obter_metas():
    conn = get_connection()
    cur = conn.cursor()
    rows = cur.execute(
        "SELECT id, tipo, valor_diario, progresso_atual FROM META WHERE usuario_id = 1"
    ).fetchall()
    conn.close()

    metas = {}
    for r in rows:
        valor = float(r["valor_diario"])
        progresso = float(r["progresso_atual"])
        percentual = min(100, round((progresso / valor) * 100)) if valor > 0 else 0
        metas[r["tipo"]] = {
            "id": r["id"],
            "tipo": r["tipo"],
            "valor_diario": valor,
            "progresso_atual": progresso,
            "percentual": percentual,
        }
    return metas


def salvar_metas(dados):
    """CA-03.1 e CA-03.3: Cadastra ou atualiza metas diarias de agua (ml) e sono (horas)."""
    try:
        meta_agua = float(dados.get("agua_ml"))
        meta_sono = float(dados.get("sono_horas"))
    except (TypeError, ValueError):
        return 400, {
            "erro": "Meta inválida.",
            "detalhe": "Informe valores numéricos para a meta de água e horas de sono.",
        }

    if (
        not math.isfinite(meta_agua)
        or not math.isfinite(meta_sono)
        or meta_agua <= 0
        or meta_sono <= 0
    ):
        return 400, {
            "erro": "Meta inválida.",
            "detalhe": "As metas de consumo de água e horas de sono devem ser maiores que zero.",
        }

    conn = get_connection()
    cur = conn.cursor()

    for tipo, valor in (("agua", meta_agua), ("sono", meta_sono)):
        existente = cur.execute(
            "SELECT id FROM META WHERE usuario_id = 1 AND tipo = ?", (tipo,)
        ).fetchone()
        if existente:
            cur.execute(
                "UPDATE META SET valor_diario = ?, progresso_atual = 0 WHERE id = ?",
                (valor, existente["id"]),
            )
        else:
            cur.execute(
                "INSERT INTO META (usuario_id, tipo, valor_diario, progresso_atual) VALUES (1, ?, ?, 0)",
                (tipo, valor),
            )

    conn.commit()
    conn.close()

    return 201, {
        "mensagem": "Metas diárias registradas com sucesso.",
        "metas": obter_metas(),
    }


def registrar_progresso_meta(dados):
    """CA-03.2: Atualiza o progresso diario de agua ou sono em direcao a meta."""
    tipo = (dados.get("tipo") or "").strip().lower()
    if tipo not in ("agua", "sono"):
        return 400, {
            "erro": "Tipo inválido.",
            "detalhe": "O tipo de meta deve ser 'agua' ou 'sono'.",
        }

    modo = (dados.get("modo") or "somar").strip().lower()
    if modo not in ("somar", "definir"):
        return 400, {
            "erro": "Modo inválido.",
            "detalhe": "O modo de atualização deve ser 'somar' ou 'definir'.",
        }

    try:
        quantidade = float(dados.get("quantidade"))
    except (TypeError, ValueError):
        return 400, {
            "erro": "Valor inválido.",
            "detalhe": "Informe uma quantidade numérica para atualizar o progresso.",
        }

    if not math.isfinite(quantidade) or quantidade <= 0:
        return 400, {
            "erro": "Valor inválido.",
            "detalhe": "A quantidade informada deve ser maior que zero.",
        }

    conn = get_connection()
    cur = conn.cursor()
    meta = cur.execute(
        "SELECT id, progresso_atual FROM META WHERE usuario_id = 1 AND tipo = ?",
        (tipo,),
    ).fetchone()

    if not meta:
        conn.close()
        return 404, {
            "erro": "Meta não encontrada.",
            "detalhe": "Cadastre a meta diária antes de registrar o progresso.",
        }

    novo_progresso = (
        quantidade if modo == "definir" else float(meta["progresso_atual"]) + quantidade
    )
    cur.execute(
        "UPDATE META SET progresso_atual = ? WHERE id = ?",
        (novo_progresso, meta["id"]),
    )
    conn.commit()
    conn.close()

    return 200, {
        "mensagem": "Progresso atualizado com sucesso.",
        "metas": obter_metas(),
    }


class PlataformaHandler(BaseHTTPRequestHandler):
    def _send_json(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self):
        length = int(self.headers.get("Content-Length", 0))
        raw = self.rfile.read(length).decode("utf-8") if length > 0 else "{}"
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}

    def do_GET(self):
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        if parsed.path in ("/", "/index.html"):
            with open(HTML_PATH, "rb") as f:
                content = f.read()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(content)))
            self.end_headers()
            self.wfile.write(content)
        elif parsed.path == "/api/treinos":
            self._send_json(200, obter_treinos())
        elif parsed.path == "/api/treinos/evolucao":
            exercicio = params.get("exercicio", [None])[0]
            self._send_json(200, obter_evolucao_cargas(exercicio))
        elif parsed.path == "/api/metas":
            self._send_json(200, obter_metas())
        else:
            self._send_json(404, {"erro": "Rota não encontrada."})

    def do_POST(self):
        parsed = urlparse(self.path)
        dados = self._read_json()
        if parsed.path == "/api/treinos":
            status, resposta = salvar_novo_treino(dados)
            self._send_json(status, resposta)
        elif parsed.path == "/api/metas":
            status, resposta = salvar_metas(dados)
            self._send_json(status, resposta)
        elif parsed.path == "/api/metas/progresso":
            status, resposta = registrar_progresso_meta(dados)
            self._send_json(status, resposta)
        else:
            self._send_json(404, {"erro": "Rota não encontrada."})


if __name__ == "__main__":
    if "--reset" in sys.argv:
        init_db(reset=True)
        print("Banco de dados restaurado para o estado inicial da demonstracao.")
    else:
        init_db(reset=False)
        porta = int(os.environ.get("PORT", "5000"))
        print(f"Servidor iniciado em http://localhost:{porta}")
        servidor = HTTPServer(("127.0.0.1", porta), PlataformaHandler)
        servidor.serve_forever()
