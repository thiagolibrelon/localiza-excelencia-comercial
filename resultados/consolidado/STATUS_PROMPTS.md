# Status dos prompts — acompanhamento

_Gerado em 2026-08-14 21:07 por `scripts/gerar_status_prompts.py` — rode o script de novo para atualizar._

## Gemini — P1/P2, P5/P6, P9/P10

| Base | Fase | Batches OK | Total | % | Pendentes |
|---|---|---|---|---|---|
| Base antiga (1.275 ligações) | P1_P2 | 23 | 23 | 100.0% | - |
| Base antiga (1.275 ligações) | P5_P6 | 23 | 23 | 100.0% | - |
| Base antiga (1.275 ligações) | P9_P10 | 23 | 23 | 100.0% | - |
| Novo lote (5.348 ligações) | P1_P2 | 74 | 74 | 100.0% | - |
| Novo lote (5.348 ligações) | P5_P6 | 74 | 74 | 100.0% | - |
| Novo lote (5.348 ligações) | P9_P10 | 74 | 74 | 100.0% | - |

**Total geral Gemini (6 combinações base×fase): 291/291 batches (100.0%)**

## Fable — exploração qualitativa

| Prompt(s) | Lotes OK | Total lotes | % lotes | Ligações OK | Ligações totais | Pendentes (lote) |
|---|---|---|---|---|---|---|
| P3/P7 — amostra antiga (`inputs`/`outputs`, encerrada) | 12 | 36 | 33.3% | 456 | 456 | - (não retomar) |
| P3/P7 — cobertura completa (`inputs_completo`, 100% da base) | 0 | 175 | 0.0% | 0 | 6623 | 1-175 |
| P4/P8/P11/P13/P14/P15 (novo lote, `novo_lote_363`) | 4 | 10 | 40.0% | 152 | 363 | 5-10 |

**P3/P7 cobertura completa:** prompt pronto para colar no Fable em `prompts/prompt_p3_p7_lote_completo.md`. Para cada lote pendente, colar o prompt + `resultados/exploracao_fable/inputs_completo/loteNNN.txt` no Fable e salvar a resposta em `resultados/exploracao_fable/outputs_completo/loteNNN_resultado.md`.

**Amostra antiga (12 lotes/456 ligações) e a cobertura completa não se sobrepõem por número de lote, mas cobrem as mesmas ligações** (a completa é superset, ordem fixa em vez de amostra aleatória) — a antiga fica só como registro histórico, não precisa reprocessar.
