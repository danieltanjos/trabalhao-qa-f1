"""Estrategia de pit stop de F1 (versao corrigida)."""


def calcular_estrategia_pit_stop(voltas_totais, temp_asfalto, porcentagem_chuva, desgaste_pneu):
    if not 30 <= voltas_totais <= 80:
        raise ValueError("voltas_totais deve estar entre 30 e 80")
    if not 10 <= temp_asfalto <= 60:
        raise ValueError("temp_asfalto deve estar entre 10 e 60")

    if porcentagem_chuva >= 50:
        pneu = "Wet"
    elif temp_asfalto < 25 and desgaste_pneu >= 70:
        pneu = "Soft"
    elif temp_asfalto >= 25 or voltas_totais > 30:
        pneu = "Hard"
    else:
        pneu = "Medium"

    parada_obrigatoria = desgaste_pneu >= 80
    volta_pit = 1 if parada_obrigatoria else voltas_totais // 2

    return {"pneu": pneu, "volta_pit": volta_pit, "parada_obrigatoria": parada_obrigatoria}
