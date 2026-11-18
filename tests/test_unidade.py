from main import calcular_volume


def test_calcula_volume_tres_series_iguais():
    """TC-01.1 / CA-02.1: 3 series de 10 repeticoes com 20kg resultam em 600kg de volume."""
    # Preparar
    series = [
        {"repeticoes": 10, "carga": 20.0},
        {"repeticoes": 10, "carga": 20.0},
        {"repeticoes": 10, "carga": 20.0},
    ]

    # Agir
    volume = calcular_volume(series)

    # Conferir
    assert volume == 600.0


def test_calcula_volume_series_com_cargas_progressivas():
    """RN-01: Soma o produto (repeticoes * carga) de series com pesos variados."""
    # Preparar
    series = [
        {"repeticoes": 12, "carga": 15.0},
        {"repeticoes": 10, "carga": 20.0},
        {"repeticoes": 8, "carga": 25.0},
    ]

    # Agir
    volume = calcular_volume(series)

    # Conferir
    assert volume == 580.0


def test_calcula_volume_valor_limite_minimo():
    """TC-02.2: Valor limite minimo valido (1 repeticao com 0.5kg)."""
    # Preparar
    series = [{"repeticoes": 1, "carga": 0.5}]

    # Agir
    volume = calcular_volume(series)

    # Conferir
    assert volume == 0.5


def test_calcula_volume_lista_vazia_retorna_zero():
    """Multiplicidade (Cap. 10): Zero series nao deve lancar excecao."""
    # Preparar
    series = []

    # Agir
    volume = calcular_volume(series)

    # Conferir
    assert volume == 0
