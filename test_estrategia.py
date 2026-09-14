import pytest

from estrategia_f1 import calcular_estrategia_pit_stop as estrategia


# --- Caixa preta: validacao de entradas (valores limite) ---
@pytest.mark.parametrize("voltas", [29, 81, 0, -1])
def test_voltas_fora_do_limite_lanca_erro(voltas):
    with pytest.raises(ValueError):
        estrategia(voltas, 30, 0, 50)


@pytest.mark.parametrize("temp", [9, 61])
def test_temperatura_fora_do_limite_lanca_erro(temp):
    with pytest.raises(ValueError):
        estrategia(50, temp, 0, 50)


@pytest.mark.parametrize("voltas", [30, 80])
@pytest.mark.parametrize("temp", [10, 60])
def test_limites_validos_nao_lancam_erro(voltas, temp):
    assert estrategia(voltas, temp, 0, 50)["pneu"] in {"Wet", "Soft", "Hard", "Medium"}


# --- Caixa preta: escolha do composto ---
@pytest.mark.parametrize("temp", [10, 24, 25, 60])
def test_chuva_maior_igual_50_sempre_wet(temp):
    assert estrategia(50, temp, 50, 10)["pneu"] == "Wet"


def test_soft_com_frio_e_desgaste_alto():
    assert estrategia(50, 24, 49, 70)["pneu"] == "Soft"


@pytest.mark.parametrize("temp,desgaste", [(24, 69), (25, 70)])
def test_nao_usa_soft_se_faltar_uma_das_condicoes(temp, desgaste):
    assert estrategia(50, temp, 0, desgaste)["pneu"] != "Soft"


def test_hard_por_temperatura_alta():
    assert estrategia(50, 25, 0, 10)["pneu"] == "Hard"


def test_hard_por_muitas_voltas_restantes():
    assert estrategia(31, 24, 0, 10)["pneu"] == "Hard"


def test_medium_quando_nenhuma_regra_se_aplica():
    assert estrategia(30, 24, 0, 10)["pneu"] == "Medium"


# --- Caixa preta: alerta de parada obrigatoria ---
def test_desgaste_80_gera_parada_na_proxima_volta():
    r = estrategia(50, 30, 0, 80)
    assert r["parada_obrigatoria"] is True
    assert r["volta_pit"] == 1


def test_desgaste_abaixo_de_80_nao_gera_alerta():
    r = estrategia(50, 30, 0, 79)
    assert r["parada_obrigatoria"] is False
    assert r["volta_pit"] == 25
