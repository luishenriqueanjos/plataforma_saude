import json
from pathlib import Path

import pytest

import main

EXEMPLOS_DIR = Path(__file__).resolve().parent.parent / "contrato" / "exemplos"


def carregar_exemplo(nome):
    return json.loads((EXEMPLOS_DIR / nome).read_text(encoding="utf-8"))


@pytest.fixture(autouse=True)
def banco_isolado(tmp_path, monkeypatch):
    """Cria um banco SQLite limpo e isolado para cada teste (Cap. 12)."""
    db_teste = tmp_path / "teste_treinos.db"
    monkeypatch.setattr(main, "DB_PATH", str(db_teste))
    main.init_db(reset=True)
    return db_teste


def test_salvar_novo_treino_valido_respeita_contrato_201():
    """TC-01.1 / CA-01.1 e CA-02.1: Salva treino valido e confere chaves do contrato."""
    # Preparar
    esperado = carregar_exemplo("treino-criado.json")
    payload = {
        "data": "2026-10-15",
        "exercicio": "Supino reto",
        "series": [
            {"repeticoes": 10, "carga": 20},
            {"repeticoes": 10, "carga": 20},
            {"repeticoes": 10, "carga": 20},
        ],
    }

    # Agir
    status, resposta = main.salvar_novo_treino(payload)

    # Conferir
    assert status == 201
    assert set(resposta.keys()) == set(esperado.keys())
    assert resposta["exercicio"] == "Supino reto"
    assert resposta["total_series"] == 3
    assert resposta["volume_total"] == 600.0


def test_recusa_treino_com_carga_ausente_retorna_400_contrato():
    """TC-01.2 / CA-01.2: Impede salvamento quando falta a carga em uma serie."""
    # Preparar
    esperado = carregar_exemplo("erro-validacao.json")
    payload = {
        "data": "2026-10-15",
        "exercicio": "Supino reto",
        "series": [
            {"repeticoes": 10, "carga": 20},
            {"repeticoes": 10, "carga": ""},
        ],
    }

    # Agir
    status, resposta = main.salvar_novo_treino(payload)

    # Conferir
    assert status == 400
    assert set(resposta.keys()) == set(esperado.keys())
    assert resposta["erro"] == "Dados incompletos."


@pytest.mark.parametrize(
    "repeticoes,carga",
    [
        (0, 20.0),
        (-5, 20.0),
        (10, 0.0),
        (10, -10.0),
    ],
)
def test_recusa_valores_limite_zero_ou_negativo(repeticoes, carga):
    """TC-02.1 / CA-02.2: Recusa valores menores ou iguais a zero nos limites da particao."""
    # Preparar
    payload = {
        "data": "2026-10-15",
        "exercicio": "Agachamento",
        "series": [{"repeticoes": repeticoes, "carga": carga}],
    }

    # Agir
    status, resposta = main.salvar_novo_treino(payload)

    # Conferir
    assert status == 400
    assert resposta["erro"] == "Dados inválidos."


def test_persistencia_treino_listado_no_historico():
    """TC-01.3 / CA-01.3 e CA-02.3: Treino salvo permanece disponivel na consulta ao historico."""
    # Preparar
    payload = {
        "data": "2026-11-05",
        "exercicio": "Remada",
        "series": [
            {"repeticoes": 10, "carga": 30},
            {"repeticoes": 10, "carga": 30},
        ],
    }
    main.salvar_novo_treino(payload)

    # Agir
    historico = main.obter_treinos()

    # Conferir
    assert len(historico) >= 1
    ultimo = historico[0]
    assert ultimo["data"] == "2026-11-05"
    assert ultimo["exercicio"] == "Remada"
    assert ultimo["volume_total"] == 600.0


def test_cadastrar_metas_diarias_agua_e_sono_inicia_zerado():
    """TC-03.1 / CA-03.1: Cadastra metas de 2000ml de agua e 8h de sono com progresso zerado."""
    # Preparar
    payload = {"agua_ml": 2000, "sono_horas": 8}

    # Agir
    status, resposta = main.salvar_metas(payload)

    # Conferir
    assert status == 201
    metas = resposta["metas"]
    assert metas["agua"]["valor_diario"] == 2000.0
    assert metas["agua"]["progresso_atual"] == 0.0
    assert metas["agua"]["percentual"] == 0
    assert metas["sono"]["valor_diario"] == 8.0
    assert metas["sono"]["progresso_atual"] == 0.0


def test_atualizar_progresso_meta_agua_calcula_percentual():
    """TC-03.2 / CA-03.2: Registrar 250ml em uma meta de 2000ml atualiza o progresso."""
    # Preparar
    main.salvar_metas({"agua_ml": 2000, "sono_horas": 8})

    # Agir
    status, resposta = main.registrar_progresso_meta(
        {"tipo": "agua", "quantidade": 250}
    )

    # Conferir
    assert status == 200
    agua = resposta["metas"]["agua"]
    assert agua["progresso_atual"] == 250.0
    assert agua["percentual"] == 12


@pytest.mark.parametrize(
    "agua_ml,sono_horas",
    [
        (0, 8),
        (-250, 8),
        (2000, 0),
        (2000, -2),
        ("", 8),
    ],
)
def test_recusa_meta_invalida_zero_ou_negativa(agua_ml, sono_horas):
    """TC-03.3 / CA-03.3: Impede cadastro de meta vazia, zero ou negativa."""
    # Preparar
    payload = {"agua_ml": agua_ml, "sono_horas": sono_horas}

    # Agir
    status, resposta = main.salvar_metas(payload)

    # Conferir
    assert status == 400
    assert resposta["erro"] == "Meta inválida."


def test_obter_metas_retorna_agua_e_sono_padrao():
    """CA-03.1: Consulta GET /api/metas retorna as metas iniciais cadastradas."""
    # Preparar / Agir
    metas = main.obter_metas()

    # Conferir
    assert "agua" in metas
    assert "sono" in metas
    assert metas["agua"]["valor_diario"] == 2000.0
    assert metas["sono"]["valor_diario"] == 8.0
