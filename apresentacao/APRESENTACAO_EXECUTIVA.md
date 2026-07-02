# Inteligência Comercial em Ligações B2B
## Localiza Frota PJ — Análise de 1.275 Ligações
### Junho 2026

---

## 1. O Ponto de Partida

> **"De 1.275 ligações gravadas, o que o vendedor faz para fechar um contrato?"**

Essa é a pergunta central do projeto. A hipótese de trabalho é simples: **os melhores vendedores fazem coisas diferentes dos medianos — e isso pode ser ensinado**.

O problema até hoje: sem análise sistemática, a resposta dependia de percepção gerencial, não de dados. Um gestor acompanha 2-3 ligações por semana. Aqui analisamos 1.275 de uma vez.

---

## 2. A Base de Dados

| Métrica | Valor |
|--------|-------|
| Total de ligações analisadas (base original, análise completa) | **1.275** |
| Clientes únicos (base original) | **1.109** |
| Período | Junho 2026 |
| Fonte | Gravações de chamadas — Localiza Empresas |
| Formato | Transcrição por Speech-to-Text |

> **Atualização 01/07/2026:** recebido um novo lote de **5.348 ligações** (4.434 clientes), ampliando a base combinada para **6.623 ligações**. Scoring automático já rodado nas duas bases (seção 5). Análise com IA do novo lote está em andamento — ver nota na seção 6.

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

**Pergunta 9 — Como o vendedor abriu e fechou a ligação**
Classifica a abertura (contextualizada / relacional / genérica / reativa) e o fechamento:
- **Fechamento forte:** "vou te mandar a proposta hoje e você me dá um retorno até quinta" — prazo definido dos dois lados
- **Fechamento médio:** só o vendedor assume uma ação, sem compromisso do cliente
- **Fechamento fraco:** "qualquer coisa me chama" — sem próximo passo, sem prazo

*Por quê:* o fechamento é o comportamento com maior impacto isolado no resultado. A diferença entre "qualquer coisa me chama" e "te ligo terça às 10" define se há continuidade ou não.

**Pergunta 10 — Promessas feitas pelo vendedor**
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

## 5. Resultados — Análise Automática Sem IA (1.275 Ligações)

> Esta análise foi construída inteiramente em Python, **sem uso de inteligência artificial generativa**, rodando as 1.275 ligações em menos de 30 segundos.

### Como funciona o scoring automático

Cada ligação recebe uma **pontuação de 0 a 30** dividida em 3 dimensões:

```
PONTUAÇÃO TOTAL (0-30) =
  Dimensão 1: CONTEXTO DA LIGAÇÃO  (0-10)  → duração, quem iniciou a conversa
+ Dimensão 2: SINAIS DO CLIENTE    (0-10)  → expansão de frota, risco de cancelamento, concorrência, dores
+ Dimensão 3: COMPORTAMENTO DO VENDEDOR (0-10)  → diagnóstico, urgência, upsell, sondagem, fechamento
```

Os sinais são detectados por **dicionários de palavras-chave** derivados dos 15 prompts. Exemplos:

| Comportamento | Como detectamos |
|--------------|-----------------|
| Vendedor criou urgência | "hoje", "prazo", "vence", "último dia" no discurso do vendedor |
| Vendedor perguntou sobre concorrência | "outra locadora", "frota própria", "movida", "unidas" no discurso do vendedor |
| Cliente em expansão | "nova filial", "mais carros", "expandindo" no discurso do cliente |
| Cliente em risco de cancelar | "cancelar", "vou excluir", "encerrar contrato" no discurso do cliente |
| Vendedor definiu próximo passo | "combinado", "te ligo na", "retorno amanhã", "deixa agendado" no discurso do vendedor |

### Distribuição de potencial — 1.275 ligações (base original)

```
ALTO          :   84 ligações   ( 6,6%)   Pontuação ≥ 20
MÉDIO         :  298 ligações   (23,4%)   Pontuação 13–19
BAIXO         :  508 ligações   (39,8%)   Pontuação  7–12
SEM POTENCIAL :  385 ligações   (30,2%)   Pontuação  0– 6
```

**30,0% das ligações** (382 no total) tinham potencial comercial real — alto ou médio.

### Validação com o novo lote — 6.623 ligações combinadas (01/07/2026)

O scoring foi rodado também nas 5.348 ligações novas. A distribuição bateu com a base original — sinal de que o modelo generaliza, não é sobreajustado:

```
ALTO          :   368 ligações   ( 5,6%)   Pontuação ≥ 20
MÉDIO         : 1.502 ligações   (22,7%)   Pontuação 13–19
BAIXO         : 2.480 ligações   (37,4%)   Pontuação  7–12
SEM POTENCIAL : 2.273 ligações   (34,3%)   Pontuação  0– 6
```

### O que aparece nas ligações de alto potencial

Das ligações com maior pontuação na base original (n=84):

| Comportamento do vendedor | Frequência | O que isso indica |
|--------------------------|-----------|-------------------|
| Criou urgência com fato real | **93%** | Vendedor que fecha cria pressão de tempo com dado concreto |
| Fez diagnóstico antes de oferecer | **80%** | Vendedor que fecha entende a necessidade antes de propor o produto |
| Tentou expandir o contrato | **71%** | Vendedor que fecha conecta o produto à conversa do cliente |
| Definiu próximo passo com data | **47%** | Menos da metade fecha com compromisso concreto |
| Identificou cliente em expansão | **31%** | Cliente em crescimento = oportunidade maior do que a ligação atual |
| Identificou risco de cancelamento | **17%** | Risco detectado = urgência de retenção |
| Perguntou sobre concorrência ou frota própria | **19%** | O comportamento de maior peso no modelo aparece pouco até nas melhores ligações |

### O número mais importante

**Perguntar sobre concorrência ou frota própria tem o maior peso no modelo de scoring** e aparece em apenas **19% das melhores ligações do time**.

Isso significa que mesmo os melhores vendedores raramente fazem essa pergunta. Nos dados de IA (bloco 1, 210 ligações), foi identificado que a vendedora Carla é a única que faz isso sistematicamente — e ela aparece como referência de performance em conversão.

### Clientes para ação imediata

O scoring identificou **376 ligações com sinais de cancelamento ou expansão** na base combinada (6.623 ligações).

**Prioridade mais alta (score máximo em uma única ligação):**

| Cliente | Pontuação | Sinal | Ação |
|---------|-----------|-------|------|
| 08208057 | 29/30 | Risco de cancelar + expansão | CRÍTICA |
| 10845574 | 29/30 | Risco de cancelar + expansão | CRÍTICA |
| 06821416 | 29/30 | Risco de cancelar + expansão | CRÍTICA |
| 27247224 | 29/30 | Expansão de frota | ALTA |
| 10508823 | 29/30 | Expansão de frota | ALTA |

---

## 6. Resultados — Análise com IA (1.275 ligações — ANÁLISE COMPLETA)

> Os 3 grupos de prompt prioritários (P1_P2, P5_P6, P9_P10) foram concluídos em 23/23 batches em 30/06/2026.
> Síntese final gerada com dados quantitativos completos — não são mais achados parciais.

### O número mais importante: R$28.490/mês em oportunidades não tentadas

44,8% das ligações encerram sem data ("qualquer coisa me chama"). A IA estimou o valor potencial de cada oportunidade perdida com base no contexto da ligação (frota, produto, contrato):

| Composição | Valor/mês |
|---|---|
| OP6 — Upsell óbvio não tentado | R$23.410 |
| OP7 — Churn não detectado | R$3.600 |
| OP1 — Suporte sem pergunta comercial | R$800 |
| Outros | resto |
| **Total** | **R$28.490/mês** |

*(Estimativa da IA a partir do contexto de 1.149 oportunidades perdidas identificadas — não é receita confirmada/auditada.)*

### Desfecho das 1.275 ligações

| Desfecho | Ligações | % |
|---|---|---|
| Não era venda (suporte) | 728 | 56,7% |
| Interessou, não fechou | 460 | 35,8% |
| Fechou — novo | 63 | 4,9% |
| Fechou — renovação | 12 | 0,9% |
| Fechou — upsell | 14 | 1,1% |
| Sem conteúdo | 7 | 0,5% |

**Total de fechamentos: 89 (7,0%)** de 1.275 ligações.

### Comportamentos com maior correlação com fechamento (B1-B10)

| Comportamento | % fechou | % interessou, não fechou | Diferencial |
|---|---|---|---|
| B5 — Upsell conectado à dor | 21,3% | 13,9% | **+7,4pp** |
| B6 — Urgência com fato verificável | 9,0% | 6,5% | **+2,5pp** |
| B9 — Conhecimento pessoal | 1,1% | 0,9% | +0,4pp |
| B1 — Diagnóstico antes do produto | 37,1% | 49,6% | −6,7pp |
| B10 — Perguntou sobre concorrente/frota | 4,5% | 17,6% | −13,1pp |
| B8 — Ligou proativamente | 5,6% | 21,5% | −15,9pp |

### 10 hipóteses sobre o que fecha um contrato

---

**H1 — A conta da diária vs. mensal é o que mais converte** · `Em validação`

Nos casos observados, o vendedor faz o cálculo em voz alta e o cliente para para recalcular. Padrão recorrente nos dados, mas ainda sem amostra controlada suficiente para confirmar.

*Ação:* treinar o time a fazer o cálculo em tempo real. "X dias × R$ diária = R$ Y. O mensal custa R$ Z."

---

**H2 — Fechar sem data é não fechar** · `Confirmada`

FC3 ("qualquer coisa me chama") aparece em 44,8% das ligações. FC1 (compromisso duplo, o fechamento mais forte) só em 31,9%. Prazo definido: apenas 9%.

OP3 (não criou urgência para o fechamento) é a segunda oportunidade perdida mais frequente.

*Ação:* substituir "qualquer coisa me chama" por "te mando hoje e você me fala até quinta".

---

**H3 — A plataforma está consumindo o time comercial** · `Confirmada`

Biometria facial (10+ clientes), senha/acesso (11+), responsável não encontrado (16+). OP1 (suporte sem pergunta comercial) é a oportunidade perdida mais frequente — presente em ~60% dos casos.

*Ação:* escalar biometria para produto/operações. Libera ~10% da capacidade comercial do time sem treinar ninguém.

---

**H4 — Perguntar sobre concorrência protege — mas o timing é tudo** · `Revisada`

B10 tem correlação **negativa** com fechamento imediato (−13,1pp) — o oposto da hipótese original. A pergunta precisa vir *antes* da decisão do cliente, não depois. Novo concorrente identificado nos dados: **Carro Zero** (modelo de assinatura de veículo), categoria diferente de Unidas/Movida.

---

**H5 — 57% das ligações são suporte puro** · `Confirmada (mais forte que o esperado)`

728 de 1.275 ligações (56,7%) = "não era venda". 30,2% da base com score zero. Segmentar o motivo da ligação antes de escalar esforço comercial aumenta o retorno por chamada.

---

**H6 — Localiza Pesados é um produto invisível** · `Nova`

Vendedor perguntou sobre frota, cliente mencionou caminhões, vendedor apresentou Localiza Pesados — cliente não sabia que o produto existia. Quantos dos 1.109 clientes têm frota mista e nunca receberam essa oferta? Oportunidade não mapeada.

---

**H7 — Biometria com falha é vazamento de receita mensurável** · `Nova`

Se 10% das ligações viram suporte de plataforma e o time faz 100 ligações/semana, são ~10 oportunidades de venda perdidas semanalmente, de forma silenciosa e recorrente.

---

**H8 — Referral nunca é pedido, mesmo quando o cliente tem contato pra dar** · `Nova`

OP4 aparece sistematicamente nos 23 batches: cliente troca de CNPJ (sem indicação), menciona diretores/sócios (sem referral interno), encerra satisfeito (sem pedido para empresa do grupo). A abertura existe; a pergunta nunca é feita.

---

**H9 — O WhatsApp virou o pseudo-fechamento — e ninguém percebeu** · `Nova — P9_P10`

PM2 (promessa via WhatsApp) = 56,2% (684/1.216) de todas as promessas registradas, quase 100% sem prazo concreto. O WhatsApp substituiu o comprometimento formal sem criar a responsabilidade que ele implica. O pipeline é gerenciado pela memória do vendedor, não por processo.

---

**H10 — Não é um comportamento isolado, é a combinação que multiplica o resultado** · `Nova — cruzamento`

Cruzando Abertura × Challenger × Upsell (B5) por ligação (join de P1_P2+P5_P6+P9_P10, n=1.168), a taxa de fechamento varia de **0% a 28,6%** dependendo da combinação — não do fator isolado:

- **Abertura contextualizada (AB1) sozinha, sem challenger nem upsell: 3,9% de fechamento** (n=483) — quase igual à taxa base (7,0%). A abertura certa por si só não move o número.
- **Abertura contextualizada + Challenger forte (CH1/CH5/CH6) + upsell conectado à dor (B5): 28,6%** (n=28) — quase 4x a taxa base, e a melhor combinação identificada na base.
- Isso explica uma aparente contradição encontrada no cruzamento isolado: AB4 (reativa) parecia fechar mais que AB1 (15,2% vs 6,3%) quando olhada sozinha. Na verdade, a maioria das ligações com AB1 não recebe o resto do tratamento comercial — quando recebe, dispara para o topo da tabela.

*Ação:* parar de treinar comportamentos isolados. Treinar o **pacote completo**: abertura contextualizada → sondagem/challenger (CH1, CH5 ou CH6) → upsell conectado à dor identificada.

#### Tabela cruzada completa — Abertura × Challenger × Upsell (n=1.168, todas as combinações)

| Abertura | Challenger | Upsell (B5) | n | Fechou | Taxa | Confiabilidade |
|---|---|---|---|---|---|---|
| AB4 | sem CH bom | B5 sim | 1 | 1 | 100,0% | ❌ n=1, ruído puro |
| AB4 | CH bom | B5 sim | 8 | 3 | 37,5% | ⚠️ amostra pequena |
| **AB1** | **CH bom** | **B5 sim** | **28** | **8** | **28,6%** | ✅ **melhor combo confiável** |
| AB1 | sem CH | B5 sim | 12 | 2 | 16,7% | ⚠️ amostra pequena |
| AB2 | sem CH | B5 sim | 6 | 1 | 16,7% | ❌ amostra mínima |
| AB2 | CH bom | B5 nao | 53 | 8 | 15,1% | ✅ confiável |
| AB4 | CH bom | B5 nao | 47 | 7 | 14,9% | ✅ confiável |
| AB4 | sem CH | B5 nao | 76 | 9 | 11,8% | ✅ confiável |
| AB2 | CH bom | B5 sim | 17 | 2 | 11,8% | ⚠️ amostra pequena |
| AB1 | CH bom | B5 nao | 143 | 13 | 9,1% | ✅ confiável, amostra grande |
| AB2 | sem CH | B5 nao | 98 | 5 | 5,1% | ✅ confiável |
| **AB1** | **sem CH** | **B5 nao** | **483** | **19** | **3,9%** | ✅ **"padrão" do time hoje** |
| AB3 | sem CH | B5 nao | 180 | 3 | 1,7% | ✅ confiável, ruim de verdade |
| AB3 | CH bom | B5 sim | 2 | 0 | 0,0% | ❌ amostra mínima |
| AB3 | CH bom | B5 nao | 14 | 0 | 0,0% | ⚠️ amostra pequena |
| AB5 | qualquer | qualquer | 0 | 0 | n/a | sem casos na base — abertura de proteção é rara demais |

*Taxa base geral (todas as 1.168 ligações do cruzamento): 6,9%. Das 20 combinações possíveis, só 9 têm amostra grande o suficiente (n≥14) pra confiar sem ressalva — as demais são direcionais, não conclusivas.*

CH_bom = teve pelo menos um dos códigos Challenger com evidência real de conversão (CH1, CH5 ou CH6 — ver seção Challenger acima).

---

### Novo lote (5.348 ligações, recebido 01/07/2026) — status da análise IA

Scoring automático já rodado (validou a distribuição de potencial — ver seção 5). Análise via IA (desfecho, Challenger, oportunidades em R$) começou em 01/07/2026, rodando no free tier do Gemini (cota diária limitada). Prioridade: P1_P2 primeiro (desfecho + B1-B10), depois P5_P6, depois P9_P10. Previsão: P1_P2 completo por volta de 05-07/07; os demais grupos seguem depois, conforme a cota permitir. **Os números de desfecho/hipóteses acima ainda se referem só à base original de 1.275 — serão atualizados quando o novo lote terminar.**

## 7. Próximos Passos

| Ação | Prazo | Impacto esperado |
|------|-------|-----------------|
| Ligar para os 5 clientes críticos (08208057, 10845574, 06821416, 27247224, 10508823) | Hoje | Retenção ou captura de expansão imediata |
| Escalar problema de biometria para produto/operações | Esta semana | Libera ~10% da capacidade comercial do time |
| Treinar CH1 — revelar custo oculto | 2 semanas | +2,5pp em B6 (mecanismo de urgência com evidência) |
| Inserir pergunta comercial em ligações de suporte (OP1) | 2 semanas | ~60% das ligações sem sondagem — qualquer melhora tem impacto imediato |
| Treinar fechamento com data no lugar do convite genérico (OP3) | 2 semanas | FC3 de 44,8% para meta abaixo de 20% |
| Inserir pedido de referral (OP4) | 2 semanas | Leads qualificados sem custo, hoje sistematicamente esquecido |
| Treinar B5 — upsell conectado à dor | 2 semanas | +7,4pp — maior diferencial identificado nos dados |
| Script de sondagem de frota pesada | 2 semanas | Abertura de mercado nos 1.109 clientes originais |
| Concluir análise IA do novo lote (5.348 ligações) | Em andamento | Dobra o tamanho da amostra, valida hipóteses em escala maior |

---

*Análise desenvolvida com framework de 15 prompts B2B — Localiza Frota PJ | Junho-Julho 2026*
*Scoring automático: 6.623 ligações (1.275 originais + 5.348 novo lote) | Análise com IA: 1.275 ligações completas (23/23 batches) — novo lote em andamento*
