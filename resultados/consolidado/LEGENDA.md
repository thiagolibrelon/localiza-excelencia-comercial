# CONSOLIDADO_LIGACOES.csv — legenda e como atualizar

Arquivo único, 1 linha por ligação (`segment_id` é a chave), 1 bloco de colunas por prompt.
6.623 linhas = todas as ligações das 2 bases (1.275 antiga + 5.348 novo lote). Coluna em
branco = aquele prompt ainda não rodou para aquela ligação especificamente.

## Como foi gerado

```
python scripts/consolidar_ligacoes.py         # etapa 1: Gemini P1/P2/P5/P6/P9/P10
python scripts/consolidar_ligacoes_etapa2.py   # etapa 2: exploração Fable P3/P4/P7/P8/P11/P13/P14/P15
```

Rodar de novo (nessa ordem) sempre que: (a) mais batches de P9_P10 do novo lote terminarem
no Gemini, (b) uma nova rodada de exploração Fable for feita. O script relê tudo do zero —
não é incremental, mas é idempotente (resultado final sempre reflete o que existe em
`resultados/gemini_v2/`, `resultados/gemini_novo_lote/` e `resultados/exploracao_fable/`
naquele momento).

## Colunas

| Coluna | Origem | Cobertura atual | Observação |
|---|---|---|---|
| `segment_id` | dados brutos | 100% | chave única da ligação |
| `base_origem`, `cliente_id`, `data`, `duracao_s`, `sentimento` | dados brutos | 100% | — |
| `p1_*` (desfecho, B1-B10, score) | Gemini P1_P2 | 99,6% | conversão/comportamento por ligação |
| `p2_*` (tipo, subtipo, quem_iniciou) | Gemini P1_P2 | 99,6% | natureza da chamada |
| `p5_*` (challenger) | Gemini P5_P6 | 96,7% | — |
| `p6_*` (oportunidades perdidas) | Gemini P5_P6 | 96,5% | — |
| `p9_*` (abertura/fechamento) | Gemini P9_P10 | 33,8% | novo lote só tem 11/74 batches rodados até agora |
| `p10_num_promessas`, `p10_tipos`, `p10_risco_max` | Gemini P9_P10 | 23,9% | **agregado por cliente+batch, não por ligação específica** — P10 é tabela filha (0..N promessas por ligação), sem campo que aponte pra uma chamada exata. Valor replicado em todas as ligações daquele cliente naquele batch. |
| `p3_amostrado`, `p3_nota` | Exploração Fable (P3 — problemas recorrentes) | 6,9% amostrado / 1,5% com nota | passe exploratório agregado (456 ligações, 12 lotes), não é CSV por ligação — `nota` só é preenchida se a ligação foi citada nominalmente como exemplo no markdown. Ver `resultados/exploracao_fable/outputs/batchNN_resultado.md` pro relatório completo do lote. |
| `p7_amostrado`, `p7_nota` | Exploração Fable (P7 — cross-sell) | mesma amostra do P3 | mesma ressalva do P3 |
| `p4_p8_p11_p13_p14_p15_amostrado`, `..._nota` | Exploração Fable (health score, objeções, inteligência competitiva, padrões emergentes, diferenças entre vendedores, eventos raros) | 2,3% amostrado / 0,9% com nota | passe exploratório em 152 ligações (só novo lote, 4 de 10 lotes planejados — 6 lotes ainda não rodaram). Ver `resultados/exploracao_fable/outputs_novo_lote_363/loteNN_resultado.md` |

## Limitações conhecidas

- **P9_P10 do novo lote está 15% completo** (11/74 batches) — a maior parte das 5.348 ligações novas ainda não tem abertura/fechamento nem promessas mapeadas.
- **P3/P4/P7/P8/P11/P13/P14/P15 nunca rodaram na base inteira** — só amostras exploratórias (456 e 152 ligações respectivamente). As colunas de nota são esparsas por design: cobrem só os exemplos citados nominalmente nos relatórios, não uma classificação sistemática por ligação.
- **P10 é aproximado**: como não há campo que ligue uma promessa a uma ligação específica, o resumo (`p10_*`) é por cliente+batch e aparece repetido em todas as ligações daquele cliente no mesmo batch.
- ~200-250 ligações por grupo Gemini ficam sem match por mismatch de contagem entre as tabelas do mesmo lote (o modelo às vezes pula ou adiciona uma linha) — ficam em branco em vez de arriscar um casamento errado.

## Próximos passos sugeridos

1. Terminar P9_P10 do novo lote (63 batches restantes) e rodar `consolidar_ligacoes.py` de novo.
2. Se decidir rodar P4/P8/P11/P13/P14/P15 nos 6 lotes restantes (05-10 de `inputs_novo_lote_363/`), rodar `consolidar_ligacoes_etapa2.py` de novo depois.
3. Se algum dia rodar P3/P7/P4/P8/etc. na base inteira (não só amostra), o script já está pronto pra isso — só apontar pros arquivos novos.
