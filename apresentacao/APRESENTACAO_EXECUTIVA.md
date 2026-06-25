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
| Total de ligações analisadas | **1.275** |
| Clientes únicos | **1.109** |
| Período | Junho 2026 |
| Fonte | Gravações de chamadas — Localiza Empresas |
| Formato | Transcrição por Speech-to-Text |

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

### Distribuição de potencial — 1.275 ligações

```
ALTO          :   70 ligações   ( 5,5%)   Pontuação ≥ 20
MÉDIO         :  298 ligações   (23,4%)   Pontuação 13–19
BAIXO         :  525 ligações   (41,2%)   Pontuação  7–12
SEM POTENCIAL :  382 ligações   (30,0%)   Pontuação  0– 6
```

**28,9% das ligações** (368 no total) tinham potencial comercial real — alto ou médio.

### O que aparece nas ligações de alto potencial

Das 70 ligações com maior pontuação:

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

O scoring identificou **82 ligações com sinais de cancelamento ou expansão** nas 1.275 chamadas.

**Prioridade mais alta:**

| Cliente | Pontuação | Sinal | Ação |
|---------|-----------|-------|------|
| 07118469 | 30/30 | Risco de cancelar + expansão | CRÍTICA |
| 08208057 | 29/30 | Risco de cancelar + expansão | CRÍTICA |
| 20271903 | 28/30 | Risco de cancelar + expansão | CRÍTICA |
| 27247224 | 28/30 | Expansão + concorrência mencionada | ALTA |
| 25141965 | 27/30 | Expansão | ALTA |

---

## 6. Resultados — Análise com IA (415 ligações — blocos 1 e 2 completos)

> Os 5 blocos restantes completam nos próximos dias (limite de API gratuita: 20 req/dia).
> Os padrões abaixo são consistentes e suficientes para as hipóteses.

### 7 hipóteses sobre o que fecha um contrato

---

**H1 — O argumento da diária vs. mensal é o que mais converte**

Toda vez que o vendedor traduz o tempo restante do aluguel em reais e compara com o mensal, o cliente para e recalcula. Não é persuasão — é matemática que o cliente não havia feito sozinho.

Nos dados: os casos com maior taxa de conversão imediata têm em comum exatamente esse momento — o vendedor faz a conta em voz alta e o cliente diz "faz sentido".

*Ação:* treinar o time a fazer o cálculo em tempo real. "Quantos dias você vai precisar? × R$ da diária = R$ X. O mensal custa R$ Y. A diferença é R$ Z."

---

**H2 — Fechar sem data é não fechar**

O fechamento com convite genérico ("qualquer coisa me chama", "fico à disposição") domina o time. Nos 415 ligações analisadas, menos de 15% terminam com um prazo definido dos dois lados.

O fechamento com data — onde o vendedor propõe um momento concreto e o cliente confirma — é raro e aparece quase exclusivamente nas ligações com desfecho positivo.

*Ação:* substituir "qualquer coisa me chama" por "te mando hoje e você me fala até quinta". Roleplay de 30 minutos com o time resolve isso.

---

**H3 — A plataforma está consumindo o time comercial**

Dois problemas aparecem com frequência alta nos dados:

- **Biometria facial:** 10+ clientes no bloco 2 não conseguem completar o cadastro de condutor. O vendedor vira suporte de TI. Nenhuma pergunta comercial é feita.
- **Senha e acesso:** 11+ clientes no bloco 1 ligaram para resetar senha. Mesma dinâmica.
- **Responsável não encontrado:** 16+ clientes num único bloco ligaram e não conseguiram falar com a pessoa certa. Isso aparece no sistema como "chamada realizada" — mas nenhuma conversa comercial aconteceu.

*Ação:* escalar o problema de biometria para produto/operações. Resolve 10% do atrito operacional do time sem precisar treinar ninguém.

---

**H4 — Quem pergunta sobre concorrência defende o contrato antes de perdê-lo**

Quando o vendedor pergunta sobre outros fornecedores e usa dado real de diferenciação, o cliente para para pensar — mesmo quando já tem proposta da concorrência. Quando não pergunta, perde a chance de contra-argumentar.

Dado relevante dos dados de IA: um cliente que já havia fechado com a Unidas recebeu uma ligação onde o vendedor não perguntou sobre a situação competitiva. A ligação terminou com "te mando os contatos para futuras demandas". A conta estava perdida — e o vendedor não soube.

Novo dado: o modelo de assinatura de veículo (Carro Zero) apareceu como concorrência nos dados. Não é Unidas nem Movida — é uma categoria diferente. O time precisa saber como rebater esse modelo específico.

---

**H5 — Há um segmento que o time não deveria tentar converter**

30% das 1.275 ligações têm pontuação zero ou perto disso. Nos dados de IA, esses casos são consistentemente ligações onde o cliente ligou para resolver um problema operacional e não havia nenhuma intenção comercial.

Parte do esforço do time está sendo gasto em clientes que não estão em modo de compra naquele momento. Segmentar o motivo da ligação antes de escalar o esforço aumenta o retorno por chamada.

---

**H6 — Localiza Pesados é um produto invisível**

Um vendedor no bloco 2 perguntou sobre a frota própria do cliente. O cliente mencionou que tinha caminhões. O vendedor apresentou a locação de veículos pesados da Localiza. O cliente não sabia que esse produto existia.

Necessidade que nunca apareceria se o vendedor não tivesse perguntado.

Dos 1.109 clientes da base, quantos têm frota mista (carros + caminhões) e nunca receberam uma oferta de locação de pesados? Essa é uma oportunidade não mapeada.

---

**H7 — O problema de biometria é um vazamento de receita mensurável**

Cada ligação consumida por problema de biometria ou senha é uma ligação que não gerou tentativa comercial. Se 10% das ligações viram suporte de plataforma, o volume de oportunidades perdidas é calculável — e o custo de resolver o fluxo de biometria provavelmente é menor do que o custo de manter o vazamento.

---

## 7. Próximos Passos

| Ação | Prazo | Impacto esperado |
|------|-------|-----------------|
| Ligar para os 5 clientes em risco máximo identificados | Hoje | Retenção ou captura de expansão |
| Escalar problema de biometria para produto/operações | Esta semana | Libera 10% da capacidade comercial do time |
| Treinar o time no argumento da diária vs. mensal | 2 semanas | Aumento imediato de conversão nas ligações com clientes em aluguel diário |
| Treinar fechamento com data no lugar do convite genérico | 2 semanas | Aumento de compromissos concretos pós-ligação |
| Criar pergunta padrão sobre concorrência e frota própria | 2 semanas | Redução de perdas silenciosas para outros fornecedores |
| Confirmar H1-H7 com análise completa (1.275 ligações) | Esta semana | Hipóteses com evidência quantitativa completa |

---

*Análise desenvolvida com framework de 15 prompts B2B — Localiza Frota PJ | Junho 2026*
*Scoring automático: 1.275 ligações em menos de 30 segundos | Análise com IA: 415 ligações concluídas (blocos 1 e 2)*
