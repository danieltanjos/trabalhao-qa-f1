# Trabalho Prático — Testes em Telemetria de F1 (pytest + coverage)

Dupla: Daniel Tavares dos Anjos e João Victor Bagatim

Repositório: https://github.com/danieltanjos/trabalhao-qa-f1.git

## Como rodar

```
pip install pytest pytest-cov
pytest --cov=estrategia_f1 --cov-branch --cov-report=term-missing
pytest --cov=estrategia_f1 --cov-branch --cov-report=html
```

Resultado: **22 passed — 100% statement e 100% branch coverage.**

## Arquivos

| Arquivo | Conteúdo |
|---|---|
| `estrategia_f1.py` | código corrigido |
| `test_estrategia.py` | suíte pytest |

## Etapa 1 — Casos de teste de caixa preta

| # | Caso | Entrada (voltas, temp, chuva, desgaste) | Esperado |
|---|---|---|---|
| 1 | Voltas fora do limite | 29 / 81 / 0 / -1 | `ValueError` |
| 2 | Temperatura fora do limite | 9 e 61 | `ValueError` |
| 3 | Limites válidos (30, 80 × 10, 60) | — | sem exceção |
| 4 | Chuva ≥ 50% independe da temperatura | 50, {10,24,25,60}, 50, 10 | `Wet` |
| 5 | Frio + desgaste alto | 50, 24, 49, 70 | `Soft` |
| 6 | Só uma das condições de Soft | (24,69) e (25,70) | ≠ `Soft` |
| 7 | Temperatura ≥ 25 | 50, 25, 0, 10 | `Hard` |
| 8 | Mais de 30 voltas restantes | 31, 24, 0, 10 | `Hard` |
| 9 | Nenhuma regra se aplica | 30, 24, 0, 10 | `Medium` |
| 10 | Desgaste ≥ 80 | 50, 30, 0, 80 | alerta + `volta_pit = 1` |
| 11 | Desgaste 79 | 50, 30, 0, 79 | sem alerta |

## Etapa 3 — Bugs identificados no código base

| # | Local | Código com bug | Correção | Teste que pega |
|---|---|---|---|---|
| 1 | Validação de voltas | `not 30 < voltas_totais <= 80` | `not 30 <= voltas_totais <= 80` | `test_limites_validos_nao_lancam_erro[30-*]`, `test_medium_quando_nenhuma_regra_se_aplica` |
| 2 | Escolha de Wet | `porcentagem_chuva > 50` | `>= 50` | `test_chuva_maior_igual_50_sempre_wet` |
| 3 | Escolha de Soft | `temp < 25 or desgaste >= 70` | `and` no lugar de `or` | `test_nao_usa_soft_se_faltar_uma_das_condicoes`, `test_hard_por_muitas_voltas_restantes` |

Executando a suíte contra o código base original: 10 testes falharam e 12 passaram; após as correções, os 22 passam.

Bugs 1 e 2 são erros de limite (`<` vs `<=`); o bug 3 troca o operador lógico da regra de pneu macio.
