# Inteligência Comercial em Ligações B2B
## Localiza Frota PJ — Análise de 6.623 Ligações
### Junho–Julho 2026 (1.275 base piloto + 5.348 novo lote)

---

## 0. Nota de auditoria (09/07/2026)

Este documento foi revisado e atualizado com os dados da base combinada (6.623 ligações). Principais mudanças desde a versão anterior (baseada só nas 1.275 ligações de junho):

- **A taxa de fechamento caiu de 7,0% para 5,1%** na base combinada. O novo lote fecha proporcionalmente 33% menos que a base piloto (4,66% vs 6,98%). **A causa ainda não foi investigada** — pode ser sazonalidade, mix de carteira diferente, mudança de política comercial, ou o novo lote simplesmente não ter passado pela mesma curadoria do piloto. Tratar como pergunta em aberto, não como conclusão.
- **B3 e B4 inverteram de sinal**: eram negativos na análise original (n=58 fechamentos), agora são levemente positivos com amostra 5x maior (n=337 fechamentos). Qualquer material antigo que cite B3/B4 como negativos está desatualizado.
- **H10 (combinação de comportamentos) ficou mais forte e mais confiável**: 6,25x (era "4x", calculado sobre uma célula de n=28 — agora a mesma leitura vem de n=225 vs n=4.885).
- **Dois achados novos**: (1) 15% da base é prospecção fria do próprio vendedor sem nenhuma tração (não estava mapeado antes); (2) o score comercial automático discrimina mal quem fecha (score médio de quem fecha é *menor* que o de quem só se interessa) — problema do modelo, não ruído.
- **Cobertura desigual entre os prompts**: P1/P2 (desfecho + B1-B10) e P5/P6 (Challenger + oportunidades perdidas) estão ~99% completos nas duas bases. **P9/P10 (abertura/fechamento/promessas) só está completo na base piloto** — no novo lote, só 11 de 74 batches (~15%) foram processados até agora. Todo dado que depende de P9/P10 (FC1-FC5, AB1-AB5, promessas) neste documento **ainda é só da base piloto de 1.275** e está marcado como tal abaixo.
- Estimativa de **R$ em oportunidades perdidas não foi recalculada** na base combinada — continua sendo só a estimativa da IA sobre a base piloto (não auditada). A rodada atual de material para diretoria decidiu não usar valor agregado até isso ser validado.
- Tabela de portfólio (frota pesada/elétrico/telemetria/gestão de frota) foi adicionada com contagem de menções na base inteira. **Ressalva interna:** a categoria "frota pesada" hoje inclui picape/caminhonete junto com caminhão — picape é frota utilitária (negócio RAC), não pesados. Mantido assim por ora (fase exploratória); corrigir antes de qualquer decisão que dependa do número exato dessa linha.

---

## 1. O Ponto de Partida

> **"O que o vendedor faz para fechar um contrato?"**

Essa é a pergunta central do projeto. A hipótese de trabalho é simples: **os melhores vendedores fazem coisas diferentes dos medianos — e isso pode ser ensinado**.

O problema até hoje: sem análise sistemática, a resposta dependia de percepção gerencial, não de dados. Um gestor acompanha 2-3 ligações por semana. Aqui analisamos 6.623 de uma vez.

---

## 2. A Base de Dados

| Métrica | Valor |
|--------|-------|
| Total de ligações analisadas (base combinada) | **6.623** |
| — Base piloto | 1.275 ligações · 1.109 clientes · junho/2026 |
| — Novo lote | 5.348 ligações · 4.434 clientes · junho–julho/2026 |
| Fonte | Gravações de chamadas — Localiza Empresas |
| Formato | Transcrição por Speech-to-Text |

**Cobertura por grupo de prompt (09/07/2026):**

| Grupo | O que cobre | Base piloto | Novo lote | Status |
|---|---|---|---|---|
| P1/P2 | Desfecho + comportamentos B1-B10 + tipo de ligação | 100% | ~99% | ✅ praticamente completo nas duas bases |
| P5/P6 | Challenger (qualidade) + oportunidades perdidas | 100% | ~97% | ✅ praticamente completo nas duas bases |
| P9/P10 | Abertura/fechamento (AB1-AB5, FC1-FC5) + promessas | 100% | ~15% (11/74 batches) | ⚠️ só piloto até aqui |

Scoring automático (Python, sem IA) já rodou nas duas bases — ver seção 5.

---

## 3. O Framework de Análise — 15 Perguntas

O framework foi desenhado para responder à pergunta central em **5 camadas**:

```
CAMADA 1 — O QUE ACONTECEU NA LIGAÇÃO?           → O desfecho e os comportamentos do vendedor
CAMADA 2 — QUAL O ESTADO DO CLIENTE?             → Os problemas e o valor potencial de cada conta
CAMADA 3 — O VENDEDOR USOU AS TÉCNICAS?          → 6 dimensões de comportamento comercial
CAMADA 4 — O QUE O MERCADO ESTÁ DIZENDO?         → Concorrência e proporção de fala
CAMADA 5 — O QUE NINGUÉM AINDA VIU?              → Padrões emergentes, diferenças entre vendedores, eventos raros
```

---

### CAMADA 1 — O que aconteceu na ligação?

**Pergunta 1 — Desfecho e comportamentos do vendedor**
Classifica o resultado de cada ligação (fechou / cliente interessado mas não fechou / não era venda) e avalia 10 comportamentos do vendedor com pesos definidos por correlação com fechamento. Gera uma pontuação comercial de 0 a 18.

*Por quê:* sem saber o desfecho, não há como identificar o que diferencia ligações que fecham das que não fecham.

**Pergunta 2 — Tipo de ligação**
Classifica a natureza da chamada: nova venda, renovação, expansão de contrato, retenção, suporte operacional, etc.

*Por quê:* misturar ligações de suporte com ligações de prospecção no mesmo pool distorce qualquer análise. É preciso separar o contexto antes de julgar o comportamento.

---

### CAMADA 2 — Qual o estado do cliente?

**Pergunta 3 — Problemas recorrentes**
Identifica se o cliente relatou algum problema (acesso à plataforma, faturamento, multa, manutenção, sinistro, etc.) e se foi resolvido na ligação.

*Por quê:* clientes com problemas não resolvidos têm risco de cancelamento. Saber quais problemas aparecem com mais frequência orienta operações e produto.

**Pergunta 4 — Valor potencial do cliente**
Pontua o cliente em 6 dimensões: volume de frota, adimplência, tempo de relacionamento, engajamento comercial, complexidade da conta e potencial de expansão.

*Por quê:* permite priorizar o esforço comercial — focar nos clientes com maior potencial e agir antes dos que estão em risco.

---

### CAMADA 3 — O vendedor usou as técnicas?

**Pergunta 5 — Comportamentos de venda consultiva (Challenger)**
Detecta se o vendedor:
- Revelou um custo oculto que o cliente não havia calculado
- Demonstrou retorno financeiro do produto
- Criou urgência com um fato real (prazo, preço, disponibilidade)
- Usou dado do concorrente para se diferenciar
- Antecipou um problema antes que o cliente o percebesse
- Descobriu uma necessidade que o cliente não havia declarado

*Por quê:* a venda consultiva é o framework com maior correlação com fechamento em contratos B2B complexos. Queremos saber quem do time já faz isso naturalmente.

**Pergunta 6 — Oportunidades perdidas**
Identifica e estima em R$ as oportunidades que existiam na ligação mas não foram aproveitadas: cliente em suporte sem pergunta comercial, dor relatada sem produto conectado, ligação encerrada sem próximo passo, indicação não solicitada.

*Por quê:* mostra o custo real de cada ligação mal aproveitada. Não é só "poderia ter vendido mais" — é "deixamos R$ X na mesa nesta chamada".

**Pergunta 7 — Expansão de portfólio**
Mapeia quais produtos foram mencionados vs. ofertados e estima receita incremental potencial por ligação. A Localiza tem 12 produtos no portfólio B2B; a maioria dos vendedores oferta apenas 2-3.

*Por quê:* saber onde estão as janelas de expansão não aproveitadas orienta o treinamento e o script comercial.

**Pergunta 8 — Objeções**
Classifica o tipo de objeção do cliente (preço, prazo, produto inadequado, concorrência) e avalia como o vendedor respondeu: validou e explorou, usou dado do cliente para rebater, capitulou sem argumento, argumentou sem ouvir o cliente.

*Por quê:* objeção não tratada é venda perdida. Saber quais objeções o time não sabe responder é o insumo direto para treino.

**Pergunta 9 — Como o vendedor abriu e fechou a ligação** *(cobertura: só base piloto — ver seção 2)*
Classifica a abertura (contextualizada / relacional / genérica / reativa) e o fechamento:
- **Fechamento forte:** "vou te mandar a proposta hoje e você me dá um retorno até quinta" — prazo definido dos dois lados
- **Fechamento médio:** só o vendedor assume uma ação, sem compromisso do cliente
- **Fechamento fraco:** "qualquer coisa me chama" — sem próximo passo, sem prazo

*Por quê:* o fechamento é o comportamento com maior impacto isolado no resultado. A diferença entre "qualquer coisa me chama" e "te ligo terça às 10" define se há continuidade ou não.

**Pergunta 10 — Promessas feitas pelo vendedor** *(cobertura: só base piloto — ver seção 2)*
Rastreia cada compromisso assumido pelo vendedor (vai enviar, vai ligar, vai resolver) com o prazo correspondente e o risco de não cumprimento.

*Por quê:* promessa não cumprida é perda de confiança. Identificar compromissos sem prazo antes que virem problema é gestão preventiva de relacionamento.

---

### CAMADA 4 — O que o mercado está dizendo?

**Pergunta 11 — Inteligência competitiva**
Detecta menções a concorrentes (Unidas, Movida, Móvel, modelos de assinatura), frota própria do cliente, histórico de migração e se o vendedor aproveitou o sinal quando ele apareceu.

*Por quê:* cada menção de concorrente é uma janela de diferenciação. Se o cliente cita outro fornecedor e o vendedor muda de assunto, a empresa perdeu uma oportunidade de posicionamento.

**Pergunta 12 — Proporção de fala**
Mede quanto o vendedor falou vs. quanto o cliente falou (número de turnos e tamanho médio das falas).

*Por quê:* vendedor que fala mais de 60% do tempo não está ouvindo. Quem ouve mais, personaliza mais. Quem personaliza mais, fecha mais.

---

### CAMADA 5 — O que ninguém ainda viu?

**Pergunta 13 — Padrões emergentes**
Captura comportamentos novos, temas recorrentes sem categoria, sinais fracos de mudança. O que aparece que o framework não esperava?

*Por quê:* os frameworks existentes capturam o que já sabemos procurar. Esta camada é a exploratória — os dados às vezes revelam o que a hipótese inicial não incluía.

**Pergunta 14 — Diferenças entre vendedores**
Compara 5 dimensões de performance entre vendedores: estrutura da ligação, linguagem usada, nível de relacionamento, comportamento comercial e tratamento de objeções.

*Por quê:* identifica quem são os benchmarks reais do time — não por feeling do gestor, mas por comportamento observável nos dados.

**Pergunta 15 — Eventos raros de alto impacto**
Detecta eventos que aparecem em menos de 5% das ligações mas têm impacto desproporcional: cliente anunciando expansão de frota, risco de cancelamento explicitado, mudança de concorrente declarada, mudança estrutural no negócio do cliente.

*Por quê:* um cliente que diz "vou expandir para mais 30 carros" ou "estou pensando em encerrar o contrato" precisa de ação imediata. Esses sinais se perdem no volume sem um sistema de detecção.

---

## 4. Onde Queremos Chegar

O projeto responde a **3 perguntas de negócio**:

### Pergunta 1 — Diagnóstico
*"Qual é o nível atual de performance comercial do time?"*
→ Pontuação por vendedor, distribuição de desfechos, taxa de tentativa comercial por ligação

### Pergunta 2 — Causa
*"O que diferencia as ligações que fecham das que não fecham?"*
→ Quais comportamentos do vendedor correlacionam com desfecho positivo

### Pergunta 3 — Ação
*"O que fazer nos próximos 30 dias para aumentar conversão?"*
→ Top comportamentos a treinar, clientes para ação imediata, oportunidades de produto não exploradas

---

## 5. Resultados — Análise Automática Sem IA (6.623 Ligações)

> Esta análise foi construída inteiramente em Python, **sem uso de inteligência artificial generativa**, rodando as ligações em segundos. Roda de forma determinística e auditável nas duas bases.

### Como funciona o scoring automático

Cada ligação recebe uma **pontuação de 0 a 30** dividida em 3 dimensões:

```
PONTUAÇÃO TOTAL (0-30) =
  Dimensão 1: CONTEXTO DA LIGAÇÃO  (0-10)  → duração, quem iniciou a conversa
+ Dimensão 2: SINAIS DO CLIENTE    (0-10)  → expansão de frota, risco de cancelamento, concorrência, dores
+ Dimensão 3: COMPORTAMENTO DO VENDEDOR (0-10)  → diagnóstico, urgência, upsell, sondagem, fechamento
```

Os sinais são detectados por **dicionários de palavras-chave** derivados dos 15 prompts (`scripts/scoring_potencial.py`). Exemplos:

| Comportamento | Como detectamos |
|--------------|-----------------|
| Vendedor criou urgência | "hoje", "prazo", "vence", "último dia" no discurso do vendedor |
| Vendedor perguntou sobre concorrência | "outra locadora", "frota própria", "movida", "unidas" no discurso do vendedor |
| Cliente em expansão | "nova filial", "mais carros", "expandindo" no discurso do cliente |
| Cliente em risco de cancelar | "cancelar", "vou excluir", "encerrar contrato" no discurso do cliente |
| Vendedor definiu próximo passo | "combinado", "te ligo na", "retorno amanhã", "deixa agendado" no discurso do vendedor |

### Distribuição de potencial — 6.623 ligações combinadas

```
ALTO          :   368 ligações   ( 5,6%)   Pontuação ≥ 20
MÉDIO         : 1.502 ligações   (22,7%)   Pontuação 13–19
BAIXO         : 2.480 ligações   (37,4%)   Pontuação  7–12
SEM POTENCIAL : 2.273 ligações   (34,3%)   Pontuação  0– 6
```

A distribuição do novo lote (284/1.204/1.972/1.888 em 5.348) bate com a da base piloto (84/298/508/385 em 1.275) — sinal de que o modelo generaliza, não é sobreajustado.

**28,3% das ligações** (1.870 no total) têm potencial comercial real — alto ou médio.

### O que aparece nas ligações de alto potencial *(base piloto, n=84 — ainda não recalculado na base combinada)*

Das ligações com maior pontuação na base piloto:

| Comportamento do vendedor | Frequência | O que isso indica |
|--------------------------|-----------|-------------------|
| Criou urgência com fato real | **93%** | Vendedor que fecha cria pressão de tempo com dado concreto |
| Fez diagnóstico antes de oferecer | **80%** | Vendedor que fecha entende a necessidade antes de propor o produto |
| Tentou expandir o contrato | **71%** | Vendedor que fecha conecta o produto à conversa do cliente |
| Definiu próximo passo com data | **47%** | Menos da metade fecha com compromisso concreto |
| Identificou cliente em expansão | **31%** | Cliente em crescimento = oportunidade maior do que a ligação atual |
| Identificou risco de cancelamento | **17%** | Risco detectado = urgência de retenção |
| Perguntou sobre concorrência ou frota própria | **19%** | O comportamento de maior peso no modelo aparece pouco até nas melhores ligações |

*Nota de auditoria: ao tentar recalcular esta tabela para a base combinada, o mapeamento de campos do script atual não reproduziu com confiança os números originais (divergências de até ~35pp em duas linhas). Antes de estender esta tabela para as 368 ligações ALTO da base combinada, revisar o mapeamento exato entre cada linha e o campo correspondente em `scripts/scoring_potencial.py`.*

### O número mais importante

**Perguntar sobre concorrência ou frota própria tem o maior peso no modelo de scoring** e aparece em apenas **19% das melhores ligações do time** (base piloto).

Isso significa que mesmo os melhores vendedores raramente fazem essa pergunta. Nos dados de IA (bloco 1, 210 ligações), foi identificado que a vendedora Carla é a única que faz isso sistematicamente — e ela aparece como referência de performance em conversão.

### Clientes para ação imediata

O scoring identificou **376 ligações com sinais de cancelamento ou expansão** na base combinada (6.623 ligações) — 85 na base piloto, 291 no novo lote.

**Prioridade mais alta (score máximo em uma única ligação, 29/30):**

| Cliente | Base | Sinal | Ação |
|---------|------|-------|------|
| 08208057 | piloto | Risco de cancelar + expansão | CRÍTICA |
| 10845574 | novo lote | Risco de cancelar + expansão | CRÍTICA |
| 06821416 | novo lote | Risco de cancelar + expansão | CRÍTICA |
| 27247224 | piloto | Expansão de frota | ALTA |
| 10508823 | novo lote | Expansão de frota | ALTA |

---

## 6. Resultados — Análise com IA

> P1/P2 (desfecho + B1-B10) e P5/P6 (Challenger + oportunidades perdidas) estão praticamente completos nas **duas bases combinadas (6.623 ligações)**. P9/P10 (abertura, fechamento, promessas) só está completo na **base piloto (1.275)** — o novo lote está ~15% processado nesse grupo. Cada bloco abaixo indica sua cobertura.

### Desfecho das ligações — base combinada (6.594 ligações com P1/P2, 99,6% de cobertura)

| Desfecho | Ligações | % |
|---|---|---|
| Não era venda (suporte) | 3.785 | 57,1% |
| Interessou, não fechou | 2.458 | 37,1% |
| Fechou — novo | 226 | 3,4% |
| Fechou — renovação | 76 | 1,1% |
| Fechou — upsell | 35 | 0,5% |
| Sem conteúdo / outros | 14 | 0,2% |

**Total de fechamentos: 337 (5,1%)** de 6.594 ligações com desfecho mapeado.

**Isso é uma queda relevante frente à base piloto isolada (89 fechamentos, 6,98%).** O novo lote fecha proporcionalmente 33% menos (248/5.319 = 4,66%). A causa ainda não foi investigada — ver nota de auditoria no topo do documento.

### Achado novo: 15% da base é prospecção fria do próprio vendedor, sem tração

Dentro do grupo "não era venda" (57,1% da base), 26,5% eram na verdade **tentativas de prospecção nova que não geraram nenhuma tração** — não é só suporte consumindo tempo comercial:

| Tipo real da ligação (dentro de "não era venda") | % |
|---|---|
| Suporte operacional | 32,9% |
| **Nova venda sem tração** | **26,5%** |
| Retenção | 8,6% |
| Pós-venda manutenção | 7,0% |

São **1.002 ligações (15,1% de toda a base)**, das quais **90% foram iniciadas pelo próprio vendedor** (901/1.002). Reforça o achado de B8 (ligar proativamente correlaciona negativo, ver tabela abaixo) com um número concreto: **1 em cada 7 ligações da base é uma ligação fria do vendedor que não deu em nada.**

### Comportamentos com maior correlação com fechamento (B1-B10) — base combinada (n=337 fechamentos)

| Comportamento | % fechou | % interessou | Diferencial | Direção vs. análise original (n=58 fechamentos) |
|---|---|---|---|---|
| B5 — Upsell conectado à dor | 16,6% | 9,6% | **+7,1pp** | confirma (era +7,4pp) |
| B3 — Usou histórico do cliente | 11,9% | 9,0% | **+2,9pp** | **inverteu** (era −4,6pp) |
| B4 — Avisou risco ao cliente | 5,6% | 4,3% | **+1,4pp** | **inverteu** (era −2,5pp) |
| B6 — Urgência com fato verificável | 4,5% | 3,3% | +1,1pp | enfraqueceu (era +2,5pp) |
| B9 — Conhecimento pessoal | 0,6% | 1,1% | −0,5pp | consistente |
| B2 — Âncora de preço alto | 3,0% | 5,0% | −2,0pp | confirma |
| B7 — Prometeu batalhar internamente | 1,2% | 3,5% | −2,3pp | confirma |
| B1 — Diagnóstico antes do produto | 37,4% | 42,1% | −4,8pp | confirma (era −6,7pp) |
| B8 — Ligou proativamente | 4,2% | 10,7% | **−6,5pp** | confirma (era −15,9pp) |
| B10 — Perguntou sobre concorrente/frota | 5,3% | 15,9% | **−10,5pp** | confirma (era −13,1pp) |

**B5 continua, de longe, o comportamento isolado com maior correlação positiva.** B10 e B8 continuam fortemente negativos — prospecção fria e sondagem de concorrente sem timing certo não fecham. **B3 e B4 inverteram de sinal**: a análise original vinha de apenas 58 fechamentos; com 337, o ruído se resolveu. Qualquer material que ainda cite B3/B4 como negativos precisa ser corrigido.

### Achado novo: o score comercial automático discrimina mal quem fecha

Score comercial médio (P1, escala 0-18): **quem fechou = 1,96 · quem só se interessou = 2,22**. Ou seja, o score que o próprio framework calcula é *menor* para quem fecha do que para quem só demonstra interesse — o oposto do esperado. Replica o achado da base piloto, agora em amostra 5x maior. Não é ruído: é um problema real do modelo de scoring que merece revisão separada (distinto do scoring de *potencial* da seção 5, que é outro modelo).

### Challenger: não é "ter ou não ter" — é qualidade de execução

"Teve Challenger" (SIM/NÃO) sozinho quase não discrimina: fechou = 51,1% · interessou = 50,8% (diferença de +0,3pp, irrelevante). Mas a **qualidade** da execução discrimina forte:

| Qualidade do Challenger | N | Taxa de fechamento |
|---|---|---|
| Alta | 1.453 | **10,8%** |
| Média | 373 | 2,1% |
| Baixa | 9 | 0,0% (amostra mínima) |

Um Challenger "SIM" genérico não diz nada — o que importa é se foi bem executado. Challenger de qualidade média fica **abaixo** da taxa base (5,1%): uma tentativa capenga pode ser pior que não tentar.

### 10 hipóteses sobre o que fecha um contrato

---

**H1 — A conta da diária vs. mensal é o que mais converte** · `Em validação — base piloto`

Nos casos observados, o vendedor faz o cálculo em voz alta e o cliente para para recalcular. Padrão recorrente nos dados, mas ainda sem amostra controlada suficiente para confirmar, e depende de P9/P10 (só piloto até aqui).

*Ação:* treinar o time a fazer o cálculo em tempo real. "X dias × R$ diária = R$ Y. O mensal custa R$ Z."

---

**H2 — Fechar sem data é não fechar** · `Confirmada — base piloto (aguarda P9/P10 do novo lote)`

FC3 ("qualquer coisa me chama") aparece em 44,8% das ligações da base piloto. FC1 (compromisso duplo, o fechamento mais forte) só em 31,9% — prazo definido: apenas 9%. Ainda não recalculado no novo lote (P9/P10 ~15% processado).

OP3 (não criou urgência para o fechamento) é a segunda oportunidade perdida mais frequente — ver tabela de OPs abaixo, essa parte já é da base combinada.

*Ação:* substituir "qualquer coisa me chama" por "te mando hoje e você me fala até quinta".

---

**H3 — A plataforma está consumindo o time comercial** · `Confirmada — base combinada`

Biometria facial, senha/acesso e responsável não encontrado seguem entre os problemas mais citados. Com a base combinada, agora temos o número preciso: **OP1 (suporte sem pergunta comercial) é 39,9% de toda oportunidade perdida**, e **OP6 (upsell óbvio não tentado) é 17,2%** — juntos, quase 60% de tudo que se perde:

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

A maior perda de receita não é "objeção mal respondida" — é **nem tentar**.

*Ação:* escalar biometria/senha/acesso para produto/operações. Libera capacidade comercial do time sem treinar ninguém.

---

**H4 — Perguntar sobre concorrência protege — mas o timing é tudo** · `Confirmada — base combinada`

B10 tem correlação **negativa** com fechamento imediato (−10,5pp na base combinada, era −13,1pp no piloto) — o oposto da hipótese original. A pergunta precisa vir *antes* da decisão do cliente, não depois. Concorrente identificado na base piloto: **Carro Zero** (modelo de assinatura de veículo), categoria diferente de Unidas/Movida — ainda não reconfirmado no novo lote.

---

**H5 — Mais da metade das ligações são suporte puro** · `Confirmada — base combinada (mais forte que o esperado)`

3.785 de 6.594 ligações (57,1%) = "não era venda". Dentro desse grupo, 26,5% são prospecção fria sem tração (ver achado novo acima) — o problema é maior e mais específico do que "é tudo suporte". Segmentar o motivo da ligação antes de escalar esforço comercial aumenta o retorno por chamada.

---

**H6 — O portfólio de frota pesada/elétrico/telemetria é subexplorado** · `Confirmada — contagem de menções, base combinada`

Contagem de menções na base inteira de 6.623 ligações (busca por palavra-chave, não classificação por IA):

| Produto | Base piloto (1.275) | Novo lote (5.348) | Total |
|---|---|---|---|
| Frota pesada / caminhão / picape | 175 | 537 | 712 |
| Elétrico / HB20 / TAO | 119 | 383 | 502 |
| Telemetria | 79 | 341 | 420 |
| Gestão de frota | 80 | 288 | 368 |
| Seminovos | 16 | 45 | 61 |
| ZARP | 1 | 4 | 5 |
| Meoo | 0 | 0 | 0 |

Frota pesada, elétrico, telemetria e gestão de frota aparecem centenas de vezes — não é nicho, é conversa recorrente que o time já está tendo. ZARP é genuinamente raro. Meoo tem zero menções em 6.623 ligações — ou não é chamado assim nas conversas, ou não está sendo oferecido a ninguém.

*Ressalva:* a linha "frota pesada" mistura picape/caminhonete (frota utilitária, negócio RAC) com caminhão (negócio Pesados) — não corrigido ainda, ver nota de auditoria no topo.

*Ação:* testar script de sondagem de portfólio ampliado, não só pesados.

---

**H7 — Biometria com falha é vazamento de receita mensurável** · `Nova — base piloto`

Se ~10% das ligações viram suporte de plataforma e o time faz 100 ligações/semana, são ~10 oportunidades de venda perdidas semanalmente, de forma silenciosa e recorrente.

---

**H8 — Referral nunca é pedido, mesmo quando o cliente tem contato pra dar** · `Confirmada — base combinada`

OP4 (referral não solicitado) é 6,6% de toda oportunidade perdida na base combinada (ver tabela em H3). Cliente troca de CNPJ sem indicação, menciona diretores/sócios sem referral interno, encerra satisfeito sem pedido para empresa do grupo. A abertura existe; a pergunta nunca é feita.

---

**H9 — O WhatsApp virou o pseudo-fechamento — e ninguém percebeu** · `Nova — base piloto (aguarda P9/P10 do novo lote)`

PM2 (promessa via WhatsApp) = 56,2% (684/1.216) de todas as promessas registradas na base piloto, quase 100% sem prazo concreto. O WhatsApp substituiu o comprometimento formal sem criar a responsabilidade que ele implica. O pipeline é gerenciado pela memória do vendedor, não por processo. Ainda não recalculado no novo lote.

---

**H10 — Não é um comportamento isolado, é a combinação que multiplica o resultado** · `Confirmada e reforçada — base combinada`

Duas versões desse achado, com coberturas diferentes:

**Versão combinada (B5 + qualidade do Challenger — P1/P2 + P5/P6, 6.623 ligações):**

| Combinação | N | Taxa de fechamento |
|---|---|---|
| **B5 + Challenger de alta qualidade** | 225 | **20,0%** |
| B5 sozinho (sem Challenger bom) | 68 | 13,2% |
| Challenger de alta qualidade sozinho (sem B5) | 1.228 | 9,1% |
| Nenhum dos dois | 4.885 | 3,2% |

**20,0% vs. 3,2% = 6,25x** — mais forte e mais confiável que os "4x" da análise original (que vinham de uma célula com N=28; aqui "combo" tem N=225 e "nada" tem N=4.885). Confirmado nas duas bases separadamente: base antiga combo=25,8% (n=66) vs nada=4,4% (n=922); novo lote combo=17,6% (n=159) vs nada=2,9% (n=3.963).

**Versão com abertura (Abertura × Challenger × Upsell — P9/P10, só base piloto, n=1.168):**

| Abertura | Challenger | Upsell (B5) | n | Fechou | Taxa | Confiabilidade |
|---|---|---|---|---|---|---|
| **AB1** | **CH bom** | **B5 sim** | **28** | **8** | **28,6%** | ✅ melhor combo confiável (piloto) |
| AB2 | CH bom | B5 nao | 53 | 8 | 15,1% | ✅ confiável |
| AB4 | CH bom | B5 nao | 47 | 7 | 14,9% | ✅ confiável |
| AB1 | CH bom | B5 nao | 143 | 13 | 9,1% | ✅ confiável, amostra grande |
| **AB1** | **sem CH** | **B5 nao** | **483** | **19** | **3,9%** | ✅ "padrão" do time (piloto) |
| AB3 | sem CH | B5 nao | 180 | 3 | 1,7% | ✅ confiável, ruim de verdade |

*Taxa base geral do cruzamento (piloto, n=1.168): 6,9%. Linhas com n pequeno omitidas — ver análise original para a tabela completa de 16 combinações.*

**Leitura:** a combinação continua sendo o achado mais forte do projeto. A versão sem abertura (B5+Challenger) já vale para a base inteira e é a que deve orientar decisão agora; a versão com abertura é mais rica mas só vale para o piloto até o novo lote fechar P9/P10.

*Ação:* parar de treinar comportamentos isolados. Treinar upsell conectado à dor identificada **e** garantir que a comparação com concorrente/Challenger seja bem executada (dado real, específico) — tentativa malfeita fica abaixo da média da base.

---

## 7. Próximos Passos

| Ação | Prazo | Impacto esperado |
|------|-------|-----------------|
| Investigar a queda de 7,0% → 5,1% na taxa de fechamento (sazonalidade, mix de carteira, curadoria do lote) | 2 semanas | Entender se é um problema real ou artefato da amostra, antes de agir sobre ele |
| Ligar para os 5 clientes críticos (08208057, 10845574, 06821416, 27247224, 10508823) | Hoje | Retenção ou captura de expansão imediata |
| Escalar biometria/senha/acesso para produto/operações | Esta semana | Tira do vendedor a maior fonte de oportunidade perdida (OP1, 39,9%) |
| Treinar upsell conectado à dor (B5) **com boa comparação com concorrente (Challenger de qualidade)** — guia já pronto (`treinamento/GUIA_CHALLENGER_BEM_FEITO.md`) | 2 semanas | 6,25x mais fechamento na combinação bem executada vs. nenhum dos dois |
| Inserir pergunta comercial em ligações de suporte (OP1) | 2 semanas | 39,9% das ligações sem sondagem — qualquer melhora tem impacto imediato |
| Reduzir prospecção fria sem preparo (B8) | 2 semanas | 1 em cada 7 ligações da base é ligação fria do vendedor sem tração |
| Inserir pedido de referral (OP4) | 2 semanas | Leads qualificados sem custo, hoje sistematicamente esquecido (6,6%) |
| Testar script de sondagem de portfólio (frota pesada, elétrico, telemetria, gestão de frota) | 2 semanas | Menções centenas de vezes na base — não é nicho |
| Revisar o modelo de score comercial automático (P1) | A definir | Hoje discrimina mal: score médio de quem fecha é menor que o de quem só se interessa |
| Concluir P9/P10 do novo lote (hoje ~15%) | Em andamento | Só assim H1, H2, H9 e a versão completa de H10 (com abertura) podem ser validadas na base combinada |
| Recalcular estimativa de R$ em oportunidades perdidas na base combinada | Em andamento | Estimativa atual (R$28.490/mês) é só da base piloto e não auditada |

---

*Análise desenvolvida com framework de 15 prompts B2B — Localiza Frota PJ | Junho–Julho 2026*
*Scoring automático: 6.623 ligações (1.275 piloto + 5.348 novo lote), completo | Análise com IA: P1/P2 e P5/P6 ~99% combinados · P9/P10 só piloto (~15% no novo lote) | Documento auditado e atualizado em 09/07/2026*
