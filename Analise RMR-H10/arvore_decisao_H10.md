# Árvore de decisão — H10 (upsell + Challenger + fechamento)

Gerado a partir de `resultados/consolidado/CONSOLIDADO_LIGACOES.csv` (6.623 ligações, base antiga + novo lote), cruzando P1+P2 (desfecho, B1-B10), P5+P6 (Challenger CH1-CH7 + Oportunidades Perdidas OP1-OP8) e P9+P10 (abertura/fechamento). Cobertura: B5 em 99,6% das ligações, qualidade do Challenger em 96,7%, abertura/fechamento em 96,8% (P9/P10 foi recalculado nesta rodada — antes o CSV consolidado só tinha 44,9% do novo lote, corrigido rodando de novo `consolidar_ligacoes.py` + `consolidar_ligacoes_etapa2.py`).

Script que gera este arquivo e o CSV/exemplos: `scripts/gerar_arvore_h10.py`.

**Regra de "fechou":** `p1_desfecho` em `fechou_novo`, `fechou_upsell` ou `fechou_renovacao`.

---

## A árvore

```
TODAS AS LIGAÇÕES — n=6.623 — 5,1% fecham (337)
│
├─ Upsell tentado (B5) = NÃO — n=6.395
│   ├─ Challenger ALTA qualidade   — n=1.289 → 9,1% fecha
│   ├─ Challenger MÉDIA            — n=487   → 5,1% fecha
│   ├─ Challenger BAIXA            — n=1.163 → 1,5% fecha
│   ├─ Sem Challenger, com OP6 (upsell óbvio não tentado) — n=303  → 8,3% fecha
│   └─ Sem Challenger, sem OP6 (não havia abertura visível) — n=3.051 → 3,1% fecha
│
└─ Upsell tentado (B5) = SIM — n=301
    ├─ Challenger ALTA qualidade — n=228 → 19,7% fecha  ★ MELHOR CÉLULA (H10)
    │   ├─ Fechou com FC1 (compromisso c/ data)       — n=130 → 21,5%  ⚠ diferença NÃO significativa (p=0,34)
    │   ├─ Fechou com FC3 ("qualquer coisa me chama")  — n=69  → 15,9%  ⚠ vs FC1
    │   ├─ Abriu com AB1 (relacional)                  — n=141 → 19,1%
    │   └─ Abriu com AB4 (reativa)                     — n=20  → 40,0% ⚠ N baixo
    └─ Challenger baixa/média/nenhuma — n=73 → 15,1% ⚠ vs ramo 6, diferença NÃO significativa (p=0,37)

(29 ligações sem dado de B5 — P1 não resolveu essas, ver ramo "0_sem_dado_B5" no CSV/exemplos)
```

## Tabela — ramos principais

| Ramo | n | Fechou | Taxa | Leitura |
|---|---:|---:|---:|---|
| 0 — sem dado de B5 | 29 | 0 | 0,0% | lacuna de processamento, não é achado |
| 1 — sem upsell, Challenger alto | 1.289 | 117 | 9,1% | Challenger sozinho já ajuda bastante |
| 2 — sem upsell, Challenger médio | 487 | 25 | 5,1% | perto da média geral |
| 3 — sem upsell, Challenger baixo | 1.163 | 18 | 1,5% | Challenger malfeito é pior que não tentar |
| 4 — sem upsell, sem Challenger, com OP6 | 303 | 25 | 8,3% | havia abertura óbvia e não foi usada — ainda assim fecha mais que a média, cliente já estava propenso |
| 5 — sem upsell, sem Challenger, sem OP6 | 3.051 | 96 | 3,1% | o "padrão do time" hoje — maior grupo da base |
| 6 — **upsell + Challenger alto** | 228 | 45 | **19,7%** | **a combinação vencedora — 6,4x o ramo 5** |
| 7 — upsell sem Challenger bom | 73 | 11 | 15,1% | amostra pequena, tratar com cautela |

## Tabela — dentro do ramo vencedor (6)

| Sub-ramo | n | Fechou | Taxa | Significância |
|---|---:|---:|---:|---|
| Fechou com FC1 (data marcada) | 130 | 28 | 21,5% | vs FC3: p=0,34 — **não significativo** |
| Fechou com FC3 ("qualquer coisa me chama") | 69 | 11 | 15,9% | — |
| Abriu com AB1 (relacional) | 141 | 27 | 19,1% | não testado (N já baixo no AB4) |
| Abriu com AB4 (reativa) | 20 | 8 | 40,0% | ⚠ N muito baixo, não usar como número, só como sinal |

## Leitura

1. **Challenger bem executado sozinho já vale a pena** (ramo 1: 9,1%, quase 2x a média geral de 5,1%).
2. **Challenger malfeito é pior que não tentar nada** (ramo 3: 1,5%, abaixo até do "padrão do time" sem tentativa nenhuma, ramo 5: 3,1%). Não é "tentar que conta" — é executar bem.
3. **A combinação upsell + Challenger alto multiplica o resultado, e isso é estatisticamente sólido** (ramo 6: 19,7% vs ramo 5: 3,1%, p=1,0×10⁻³²; vs ramo 1: 9,1%, p=1,6×10⁻⁶). Esse é o núcleo confiável de H10.
4. **Ressalva de auditoria (13/07/2026):** os recortes mais finos dentro do ramo 6 — FC1 vs FC3 (p=0,34) e "Challenger alto" vs "Challenger fraco" quando já há upsell (ramo 6 vs 7, p=0,37) — **não passam no teste de significância** com o N atual. São sinais direcionalmente consistentes com a lógica de negócio, não achados provados. Não apresentar "fechar com data soma mais" como fato confirmado — apresentar como hipótese a validar com mais dados (ideal: recalcular depois que P9/P10 tiver mais volume, ou agrupar mais meses).
5. **Ressalva sobre upsell real:** os 301 casos de B5=SIM ainda não foram confirmados como upsell de produto real (Telemetria, Proteção Total etc.) — essa é a validação que o Prompt P7 traria (em standby, ver decisão de 13/07/2026).
6. **Achado de enriquecimento (auditoria):** o ramo vencedor dura em média 661s (~11 min) contra 168s (~2,8 min) do ramo "não fez nada" — o playbook custa ~4x mais tempo por ligação, não é neutro em capacidade.
7. **Achado de enriquecimento — relevante pra venda interna:** o ramo vencedor já ocorre desproporcionalmente mais em ligações de upsell/renovação/retenção (23% do ramo, vs 9-19% no resto da árvore) do que em venda nova. H10 já pende naturalmente pro cenário que a diretoria está priorizando agora.

Ver `auditoria.md` nesta pasta para a auditoria completa (integridade dos dados, bugs de taxonomia encontrados, e recomendação de prioridade de enriquecimento).

## Arquivos desta pasta

- `dados_arvore_H10.csv` — as 6.623 ligações com a coluna `ramo` (e `sub_ramo_fechamento`/`sub_ramo_abertura` para o ramo 6), pra filtrar/conferir em Excel.
- `exemplos_por_ramo.md` — pelo menos 5 ligações reais de cada ramo, com resumo do Challenger e/ou da oportunidade perdida quando disponível, e a transcrição completa.
- `auditoria.md` — auditoria de integridade dos dados + avaliação de enriquecimento (visão de diretor, venda interna).
