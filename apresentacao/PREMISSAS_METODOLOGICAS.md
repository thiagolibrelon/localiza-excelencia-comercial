# Premissas Metodológicas
## Framework de Análise de Ligações B2B — Localiza Frota PJ | Junho 2026

> Este documento registra as decisões e premissas que sustentam o framework.
> Serve para defender a metodologia, identificar limitações e orientar atualizações futuras.

---

## 1. PREMISSAS SOBRE OS DADOS

### 1.1 Qualidade da transcrição (STT)
- As ligações foram transcritas por Speech-to-Text (STT) — não é transcrição humana revisada
- A qualidade varia: nomes próprios, jargão técnico e sobreposição de vozes geram erros
- O framework foi desenhado para ser robusto a erros de STT: usa padrões de palavras múltiplas, não palavras isoladas
- **Premissa aceita:** erros de STT afetam casos individuais, mas não distorcem os padrões agregados de 1.275 ligações

### 1.2 Segmentação de fala
- Quando dois turnos consecutivos são do mesmo locutor, o sistema os trata como fala contínua
- Silêncios curtos entre turnos do mesmo locutor são tratados como pausa, não como troca de interlocutor
- **Impacto:** o talk ratio (proporção de fala) pode ter margem de erro de até 5-10% por ligação; a direção do padrão é confiável

### 1.3 Identificação dos locutores
- A distinção entre "vendedor" e "cliente" depende de como a transcrição foi gerada
- Em ligações onde o cliente ligou para a Localiza, o locutor 1 costuma ser o cliente
- Em ligações onde o vendedor ligou para o cliente, o locutor 1 costuma ser o vendedor
- **Premissa aceita:** o framework usa contexto conversacional (não apenas posição) para identificar o papel de cada locutor

### 1.4 Período analisado
- Todas as ligações são de junho de 2026 — um recorte de tempo único
- Padrões sazonais (renovação de frota no final de semestre, etc.) podem distorcer se junho for atípico
- **Limitação conhecida:** sem série histórica, não é possível distinguir padrão permanente de padrão sazonal

---

## 2. PREMISSAS SOBRE O SCORING AUTOMÁTICO (Python, sem IA)

### 2.1 Lógica do scoring
O scoring de 0 a 30 pontos foi construído sobre 3 premissas:

**Premissa A — Contexto importa antes de comportamento**
Uma ligação longa iniciada pelo vendedor tem mais potencial do que uma ligação curta iniciada pelo cliente para reclamar. Por isso, a Dimensão 1 (contexto) precede a avaliação de comportamento.

**Premissa B — Sinais do cliente valem tanto quanto comportamento do vendedor**
Um cliente que menciona expansão de frota ou risco de cancelamento representa oportunidade/urgência independente de como o vendedor se comportou. Por isso, Dimensão 2 (sinais do cliente) tem peso igual à Dimensão 3 (vendedor).

**Premissa C — A pergunta sobre concorrência é o comportamento mais valioso**
B10 (sondagem de concorrência) tem peso 3 — o dobro da maioria dos outros comportamentos — porque:
- Aparece raramente (19% das melhores ligações)
- Tem correlação com desfecho positivo nos dados analisados (H4)
- A vendedora identificada como top performer (Carla) é a única que faz isso sistematicamente
- Perder um cliente para concorrência sem saber é o pior cenário: é invisível nos dados de venda

### 2.2 Detecção por palavras-chave
O scoring automático usa dicionários de palavras-chave, não IA. Isso significa:

**O que o scoring captura bem:**
- Palavras e expressões explícitas: "cancelar", "unidas", "nova filial", "prazo", "diária"
- Menções diretas a produtos, concorrentes, problemas conhecidos
- Padrões de fechamento com frases típicas

**O que o scoring NÃO captura:**
- Intenção implícita: um cliente que diz "vou pensar" está diferente de um que diz "não preciso" — o scoring pode tratar os dois igual
- Tom e emoção: um "sim" entusiasmado e um "sim" relutante têm o mesmo peso
- Contexto longo: o scoring analisa palavras presentes, não sequência narrativa
- Ironia ou negação complexa: "não preciso cancelar" pode ser lido como "cancelar" dependendo da janela de contexto

**Consequência para interpretação:**
O scoring é confiável para ranking relativo (quem tem mais potencial do que quem) e para detecção de sinais claros. Não é confiável para julgamento de casos limítrofes individuais.

### 2.3 Limiares de classificação
Os limiares (ALTO ≥ 20, MÉDIO 13–19, BAIXO 7–12, SEM POTENCIAL 0–6) foram definidos por:
- Distribuição dos scores observados: os limiares foram ajustados para que ALTO represente ~5-10% do volume (ligações verdadeiramente diferenciadas)
- Validação manual de amostras: foram verificadas manualmente ~20 ligações em cada faixa para confirmar que a classificação faz sentido intuitivo
- **Não foram calibrados contra resultados de venda reais** (CRM): essa validação está pendente

---

## 3. PREMISSAS SOBRE A ANÁLISE COM IA (Gemini 2.5 Flash)

### 3.1 Modelo utilizado
- Modelo: Gemini 2.5 Flash (Google)
- Tier: gratuito (free tier)
- Limite: 250.000 tokens de entrada por minuto / 20 requisições por dia
- **Implicação:** a análise completa de 1.275 ligações requer múltiplos dias (20 req/dia → ~3 dias para 7 blocos × 7 análises)

### 3.2 Estrutura dos blocos
- 1.275 ligações divididas em 7 blocos de ~182 ligações cada
- Cada bloco recebe 7 prompts diferentes (cobrindo as 15 perguntas do framework)
- Cada prompt analisa o bloco inteiro de uma vez — não é análise ligação por ligação em chamadas separadas
- **Consequência:** a IA analisa padrões do conjunto, não julgamentos individuais precisos para cada ligação

### 3.3 Temperatura e determinismo
- Os prompts foram escritos para respostas estruturadas (CSV, JSON) com pouco espaço para variação
- A temperatura da IA não foi configurada explicitamente — usa o default do modelo
- **Premissa aceita:** a estrutura dos prompts (pedindo CSV com campos específicos) é suficiente para garantir consistência suficiente entre blocos

### 3.4 Amostragem parcial
- Os resultados atuais cobrem 415 ligações (blocos 1 e 2 de 7)
- Os padrões identificados são consistentes entre os dois blocos analisados
- **Premissa de trabalho:** os padrões dos blocos 1 e 2 são representativos do todo — os blocos restantes refinarão os números, não mudarão a direção das hipóteses
- **Risco:** se os primeiros 2 blocos tiverem viés (ex: foram selecionados clientes específicos), os dados podem não ser representativos

### 3.5 O que a IA não decide
- **A IA não define o framework**: as 15 perguntas, os comportamentos B1-B10, os tipos de fechamento FC1-FC5, os pesos do scoring — tudo foi definido pelos analistas antes de rodar qualquer modelo
- **A IA não julga o vendedor**: classifica comportamentos observáveis na transcrição, não avalia intenção ou competência
- **A IA pode errar em casos individuais**: a confiabilidade está nos padrões agregados, não em cada linha do CSV de resultado

---

## 4. PREMISSAS SOBRE AS HIPÓTESES

### 4.1 Causalidade vs. correlação
As hipóteses H1-H7 identificam correlações, não causalidade provada. Exemplos:

- **H1:** vendedores que fazem o argumento da diária vs. mensal aparecem mais em ligações com desfecho positivo. Isso não prova que o argumento causa o fechamento — pode ser que vendedores melhores em geral usem esse argumento e também fechem mais por outros motivos.

- **H4:** a vendedora Carla pergunta sobre concorrência e é top performer. Isso não prova que perguntar sobre concorrência causa performance — pode ser que vendedores mais experientes façam ambas as coisas.

**Para converter correlação em causalidade**, seria necessário: experimento controlado (treinamento de parte do time em um comportamento específico com grupo de controle) ou análise longitudinal com CRM.

### 4.2 O que "fechar" significa nos dados
- **Nos dados de IA:** `fechou` = desfecho classificado pela IA com base na transcrição
- **Na realidade:** pode haver fechamentos que aparecem em ligações posteriores não analisadas, e pode haver ligações classificadas como `fechou` que não resultaram em contrato assinado
- **Premissa aceita:** a classificação da IA para `desfecho` é uma aproximação útil, não uma verdade absoluta

### 4.3 A ausência de dados de CRM
O framework foi construído sem acesso ao histórico de vendas (CRM, contratos assinados, receita por cliente). Isso significa:
- Não é possível validar se clientes com score ALTO no scoring automático realmente converteram mais
- Não é possível confirmar qual comportamento isolado tem maior correlação com receita gerada
- **A validação cruzada com CRM é o próximo passo metodológico mais importante**

---

## 5. O QUE ESTE FRAMEWORK NÃO FAZ

| O que poderia parecer que fazemos | O que realmente fazemos |
|----------------------------------|------------------------|
| Avaliamos a performance de cada vendedor individualmente | Identificamos padrões de comportamento no conjunto — avaliação individual requer mais dados por vendedor |
| Provamos o que causa fechamento | Identificamos correlações que geram hipóteses a testar |
| Garantimos que os clientes listados como risco vão cancelar | Identificamos sinais que aumentam a probabilidade de risco — não há certeza |
| Analisamos 1.275 ligações com IA até agora | Analisamos 415 com IA; as outras 860 têm apenas o scoring automático (sem IA) |
| O scoring automático substitui a análise com IA | São complementares: o scoring é rápido e cobre tudo; a IA é mais profunda mas mais lenta |

---

## 6. DECISÕES DE DESIGN QUE MERECEM REVISÃO FUTURA

| Decisão | Racional atual | Quando revisar |
|---------|----------------|----------------|
| B10 com peso 3 (dobro dos outros) | Dados iniciais + padrão Carla | Quando tivermos correlação com CRM |
| Limiar ALTO ≥ 20 | Distribuição empírica + amostras manuais | Quando tivermos taxa de conversão por faixa |
| 7 blocos de ~182 ligações | Limite de token do modelo gratuito | Se mudar para API paga (blocos maiores) |
| 15 prompts agrupados em 7 chamadas de IA | Eficiência dentro do limite de 20 req/dia | Quando aumentar cota de API |
| Análise em lote (bloco inteiro por chamada) | Custo e limite de API | Se precisar de análise individual por ligação |

---

*Documento de metodologia — Projeto de Inteligência Comercial | Localiza Frota PJ | Junho 2026*
*Última atualização: 24/06/2026 — versão 1.0 (415 ligações com IA analisadas)*
