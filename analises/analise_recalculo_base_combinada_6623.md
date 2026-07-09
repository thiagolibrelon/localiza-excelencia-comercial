# Recálculo das hipóteses na base combinada (6.623 ligações)

**Fonte:** `resultados/consolidado/CONSOLIDADO_LIGACOES.csv`
**Cobertura usada:** P1/P2 (99,6% — 6.594 ligações), P5/P6 (96,5-96,7% — ~6.400 ligações)
**Por que isso importa:** é a primeira vez que P1/P2/P5/P6 (desfecho, comportamentos B1-B10, Challenger, oportunidades perdidas) estão praticamente completos nas duas bases juntas. Tudo abaixo foi validado numa amostra 5x maior que a análise original de 1.275 ligações.

---

## 1. Achado mais importante: a taxa de fechamento caiu

| Base | Fechamentos | Total | Taxa |
|---|---|---|---|
| Base antiga (jun/2026) | 89 | 1.275 | **6,98%** |
| Novo lote (jun/jul) | 248 | 5.319 | **4,66%** |
| **Combinada** | 337 | 6.594 | **5,11%** |

O novo lote fecha **33% menos**, proporcionalmente, que a base antiga. Isso muda o "número que ninguém espera" que está em toda a apresentação (7,0%) — o número real na base ampliada é **5,1%**.

**Não sabemos ainda a causa** (sazonalidade, mix diferente de carteiras, mudança de política comercial, ou só o efeito de o novo lote não ter sido "curado" como o piloto). Isso é uma pergunta em aberto, não uma conclusão — vale investigar antes de levar pra a diretoria.

---

## 2. B1-B10: confirmações, e duas reversões importantes

| Comportamento | % fechou | % interessou | Diferencial | Direção vs. análise anterior (n=831) |
|---|---|---|---|---|
| B5 — upsell conectado à dor | 16,6% | 9,6% | **+7,1pp** | confirma (era +7,4pp) |
| B3 — usou histórico do cliente | 11,9% | 9,0% | **+2,9pp** | **inverteu** (era −4,6pp) |
| B4 — avisou risco ao cliente | 5,6% | 4,3% | **+1,4pp** | **inverteu** (era −2,5pp) |
| B6 — urgência com fato verificável | 4,5% | 3,3% | +1,1pp | enfraqueceu (era +2,5 a +5,1pp) |
| B9 — conhecimento pessoal | 0,6% | 1,1% | −0,5pp | consistente (perto de zero) |
| B2 — âncora de preço alto | 3,0% | 5,0% | −2,0pp | confirma (era −2,5pp) |
| B7 — prometeu batalhar internamente | 1,2% | 3,5% | −2,3pp | confirma (era −3,3pp) |
| B1 — diagnóstico antes do produto | 37,4% | 42,1% | −4,8pp | confirma (era −6,7pp) |
| B8 — ligou proativamente | 4,2% | 10,7% | **−6,5pp** | confirma (era −15,9 a −17,7pp, mas mais forte no dado pequeno) |
| B10 — perguntou sobre concorrente/frota | 5,3% | 15,9% | **−10,5pp** | confirma (era −13,1 a −17,1pp) |

**Leitura:** B5 continua, de longe, o comportamento isolado com maior correlação positiva. B10 e B8 continuam fortemente negativos (prospecção fria e sondagem de concorrente sem timing certo não fecham). **B3 e B4 inverteram de sinal** — a leitura correta agora é que eles são levemente positivos, não negativos. A conclusão anterior vinha de uma amostra de 58 fechamentos; com 337, o ruído se resolveu. Vale corrigir qualquer material que ainda cite B3/B4 como negativos.

**Score comercial médio:** fechou = 1,96 · interessou = 2,22 — **o score automático continua discriminando mal quem fecha** (replica o achado anterior, agora em escala 5x maior). Isso não é ruído — é um problema real do modelo de scoring, que merece atenção separada.

---

## 3. Challenger sozinho não move o número — qualidade sim

- "Teve Challenger" (SIM/NAO): fechou = 51,1% · interessou = 50,8% → **diferença de +0,3pp — estatisticamente irrelevante**.
- Mas a **qualidade** do Challenger discrimina forte:

| Qualidade do Challenger | N | Taxa de fechamento |
|---|---|---|
| Alta | 1.453 | **10,8%** |
| Média | 373 | 2,1% |
| Baixa | 9 | 0,0% (amostra mínima) |

Ter um Challenger "SIM" genérico não diz nada — o que importa é se ele foi bem executado. Challenger de qualidade média até fica **abaixo** da taxa base (5,1%), sinal de que uma tentativa capenga pode ser pior que não tentar.

---

## 4. A combinação continua sendo o achado mais forte — e mais forte do que se pensava

| Combinação | N | Taxa de fechamento |
|---|---|---|
| **B5 + Challenger de alta qualidade** | 225 | **20,0%** |
| B5 sozinho (sem Challenger bom) | 68 | 13,2% |
| Challenger de alta qualidade sozinho (sem B5) | 1.228 | 9,1% |
| Nenhum dos dois | 4.885 | 3,2% |

**20,0% vs. 3,2% = 6,25x** — mais forte que os "4x" que estavam na apresentação (que vinham de uma célula com N=28). Aqui a célula "combo" tem N=225 e a célula "nada" tem N=4.885 — é um resultado muito mais confiável.

Confirmado nas duas bases separadamente (não é artefato de uma só):
- Base antiga: combo = 25,8% (n=66) vs. nada = 4,4% (n=922)
- Novo lote: combo = 17,6% (n=159) vs. nada = 2,9% (n=3.963)

---

## 5. Oportunidades perdidas (P6) — o que domina, em escala

| Código | Tipo | % das ligações com P6 |
|---|---|---|
| OP1 | Suporte encerrado sem pergunta comercial | **39,9%** |
| OP6 | Upsell óbvio não tentado | **17,2%** |
| OP2 | Dor revelada, produto não conectado | 10,6% |
| OP3 | Fechamento sem urgência | 8,2% |
| OP4 | Referral não solicitado | 6,6% |
| OP7 | Churn não detectado | 2,7% |
| OP5 | Dado estratégico não explorado | 1,0% |
| OP8 | Escalada desnecessária | 0,8% |

A maior perda de receita não é "objeção mal respondida" — é **nem tentar**. OP1 (quase 40%) e OP6 (17%) juntos são quase 60% de toda oportunidade perdida identificada.

---

## 6. O que "não era venda" realmente é

Cruzando o desfecho (P1) com o tipo de ligação (P2), dentro do grupo "não era venda" (57,4% da base):

| Tipo real da ligação | % dentro de "não era venda" |
|---|---|
| Suporte operacional | 32,9% |
| **Nova venda (prospecção que não gerou tração)** | **26,5%** |
| Retenção | 8,6% |
| Pós-venda manutenção | 7,0% |

**Achado novo:** mais de 1/4 das ligações "não era venda" **eram tentativas de prospecção nova que simplesmente não geraram nenhuma tração** — não é só suporte consumindo tempo comercial. São **1.002 ligações** (15,1% de toda a base) de prospecção fria, das quais **90% foram iniciadas pelo próprio vendedor** (901/1.002). Isso reforça o achado de B8 (ligar proativamente correlaciona negativo) com um número concreto: 1 em cada 7 ligações da base é uma ligação fria do vendedor que não deu em nada.

---

## Resumo executivo (para quem só vai ler isso)

1. **A taxa de fechamento real é 5,1%, não 7,0%** — o novo lote fecha um terço menos que a base antiga. Investigar por quê antes de apresentar.
2. **B5 (upsell na dor) continua o comportamento isolado mais forte** (+7,1pp). B3 e B4 inverteram de negativos pra levemente positivos — corrigir qualquer material antigo.
3. **Challenger "ter ou não ter" não importa — qualidade sim** (10,8% vs 2,1% de fechamento conforme a execução).
4. **A combinação B5 + Challenger de qualidade multiplica por 6,25x** (20,0% vs 3,2%), não 4x — e agora com amostra grande o suficiente pra confiar sem ressalva.
5. **A maior oportunidade perdida é não tentar** (OP1+OP6 = quase 60% de tudo que se perde).
6. **15% da base é prospecção fria do próprio vendedor sem nenhuma tração** — não é só "suporte" que rouba tempo comercial.
