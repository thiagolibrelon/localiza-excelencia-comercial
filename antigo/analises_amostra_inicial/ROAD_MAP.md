# AUDITORIA ESTRATÉGICA & PLANO DE MATURIDADE
## Squad de Excelência Comercial — Localiza Frota PJ
*Versão 1.0 | Junho 2026 | Confidencial*

---

## EXECUTIVE SUMMARY

O framework de 12 prompts construído representa um ativo competitivo raro: inteligência comportamental extraída de conversa real, não de survey ou CRM. A base de 87 ligações com 14 clientes já revelou insights acionáveis que nenhum relatório de pipeline entregaria — nenhum vendedor pediu indicação uma única vez, ZARP e Meoo nunca foram mencionados, e a Andreza opera num patamar Challenger que o restante do time sequer visualiza.

**O problema não é falta de dado. É falta de sistema para transformar dado em comportamento recorrente.**

Os 12 prompts hoje funcionam como instrumentos isolados rodados episodicamente. O salto de maturidade exige três mudanças simultâneas: (1) cadência — análise contínua, não pontual; (2) hierarquia de impacto — saber quais prompts geram receita vs. quais são operacionais; (3) institucionalização — o insight sai do arquivo Markdown e entra no 1:1 da segunda-feira.

**Potencial financeiro conservador desta base:** Se os 8 vendedores analisados elevassem a taxa de tentativa comercial em ligações de suporte de ~20% para 60%, e apenas 15% dessas tentativas convertessem em upsell médio de R$200/mês por cliente, o ganho incremental anual ultrapassa **R$180k** só nesta carteira.

---

## PARTE 1 — AUDITORIA DOS 12 PROMPTS

### 1.1 Pontos Fortes do Conjunto

| Força | Evidência |
|-------|-----------|
| **Taxonomia robusta** | Cada prompt tem códigos padronizados (B1-B10, CH1-CH7, OP1-OP8) que permitem consolidação cruzada sem retrabalho |
| **Saída em CSV** | Todos os prompts retornam CSV, o que habilita dashboard imediato sem parsing manual |
| **Desfecho extraído da transcrição** | Resolve o problema de atribuição sem depender de dados de CRM |
| **Cobertura 360°** | Os 12 prompts cobrem toda a jornada: entrada → comportamento → resultado → promessa → competição |
| **Dupla visão** | Todos têm análise por ligação E consolidação por vendedor/cliente |
| **Perguntas qualitativas embutidas** | Cada prompt termina com 4-5 perguntas que forçam síntese estratégica, não só tabela |

### 1.2 Fragilidades e Gaps Críticos

| Gap | Impacto | Severidade |
|-----|---------|------------|
| **Sem sequenciamento definido** | Os 12 prompts são independentes — nenhuma instrução diz para rodar P4 (health) antes de P6 (oportunidades), o que gera análises sem contexto | Alta |
| **Sem score de prioridade por ligação** | Toda ligação recebe o mesmo peso analítico. Uma ligação de 3 min de voicemail consome o mesmo espaço que uma de 22 min com proposta de 50 carros | Alta |
| **Ausência de feedback loop** | Nenhum prompt pergunta: "o que mudou no comportamento do vendedor desde a última análise?" — sem linha de base não há evolução mensurável | Alta |
| **Ausência de análise de sazonalidade** | Os dados já revelaram que março e setembro são meses de readequação (alta urgência) e janeiro/julho são bons para fechar 12 meses — nenhum prompt estrutura isso | Média |
| **P10 (Promessas) sem rastreamento automático** | O prompt depende de ligações subsequentes para verificar cumprimento — sem ID de promessa e data-alvo não há rastreabilidade real | Média |
| **P12 (Talk ratio) é estimativa qualitativa** | Sem timestamps de turn, o ratio é inferido por contagem de turns e extensão — impreciso para decisão de coaching | Baixa |
| **Sem prompt de síntese mensal** | 12 análises separadas sem um prompt que integre os outputs e responda: "qual o estado da carteira este mês vs. o anterior?" | Alta |
| **Ausência de análise de prospecção fria** | Todo o framework assume base instalada. Não existe prompt para ligações de prospecção de novos clientes | Média |

### 1.3 Mapa de Impacto vs. Automação

```
                      ALTO IMPACTO
                           │
           P1 (Conversão)  │  P4 (Health Score)
           P6 (Op. Perdidas)│  P5 (Challenger)
                           │
AUTOMAÇÃO  ────────────────┼──────────────── VALIDAÇÃO
 PLENA                     │                 HUMANA
                           │
           P2 (Tipo Lig.)  │  P10 (Promessas)
           P12 (Talk ratio)│  P8 (Objeções)
                           │
                      BAIXO IMPACTO
```

| Prompt | Impacto Receita | Automação LLM | Validação Humana | Frequência Ideal |
|--------|----------------|---------------|------------------|-----------------|
| P1 — Conversão | **Crítico** | Total | Nenhuma | **Diária** |
| P2 — Tipo de ligação | Operacional | Total | Nenhuma | Diária |
| P3 — Problemas recorrentes | Retenção | Total | Produto/Ops | Semanal |
| P4 — Health Score | **Crítico** | Total | Gerente valida | **Semanal** |
| P5 — Challenger | **Alto** | Total | Coach valida | Semanal |
| P6 — Op. Perdidas | **Crítico** | Total | 1:1 coaching | **Diária** |
| P7 — Cross-sell | **Alto** | Total | Gerente valida | Semanal |
| P8 — Objeções | Alto | Total | Coach valida | Semanal |
| P9 — Abertura/Fechamento | Alto | Total | Coach valida | Quinzenal |
| P10 — Promessas | **Crítico** | Parcial | Vendedor confirma | **Semanal** |
| P11 — Intel. competitiva | Estratégico | Total | Gerente valida | Mensal |
| P12 — Talk ratio | Coaching | Parcial | Coach usa em 1:1 | Quinzenal |

### 1.4 Melhorias Específicas em 4 Prompts

---

#### MELHORIA P1 — CONVERSÃO
**Gap atual:** Não distingue o *peso* de cada comportamento B1-B10 — B3 (histórico do cliente) e B6 (urgência real) têm peso muito maior que B9 (rapport), mas todos valem igual.

**Versão revisada — adicionar ao final:**

```
## PESO DOS COMPORTAMENTOS (adicionar coluna ao CSV)
Após classificar B1-B10, calcule o score_comercial da ligação:

| Comportamento | Peso |
|--------------|------|
| B1 (diagnóstico) | 2 |
| B3 (histórico) | 2 |
| B6 (urgência real) | 3 |
| B10 (sonda concorrência) | 3 |
| B4 (proteção cliente) | 2 |
| B5 (upsell encaixado) | 2 |
| B2, B7, B8, B9 | 1 cada |

score_comercial = soma dos pesos onde o comportamento = SIM
Adicionar coluna: score_comercial (0–18)

## NOVA QUESTÃO FINAL:
6. Qual é o score_comercial médio das ligações que fecharam vs. que não fecharam?
   Existe um score_comercial mínimo abaixo do qual nenhuma ligação fechou?
```

---

#### MELHORIA P4 — HEALTH SCORE
**Gap atual:** Score é estático — calculado em snapshot. Não detecta tendência (melhorando vs. piorando).

**Versão revisada — substituir formato de saída por:**

```
## FORMATO DE SAÍDA REVISADO
cliente_id,executivo,periodo_analisado,total_ligacoes,
volume,adimplencia,fidelidade,engajamento,complexidade_operacional,
potencial_upsell,score_total,score_anterior,tendencia,
dias_sem_contato_proativo,risco_churn,alerta_imediato,proxima_acao

Onde:
- score_anterior: informe manualmente o score do mês anterior (ou "N/A" na primeira análise)
- tendencia: subindo / estavel / caindo (comparação com score_anterior)
- dias_sem_contato_proativo: quantos dias desde a última ligação onde o VENDEDOR ligou
- alerta_imediato: SIM/NAO — score ≤ 6 ou tendencia = caindo + risco_churn = alto

## NOVA QUESTÃO FINAL:
6. Para cada cliente com alerta_imediato = SIM, descreva em 2 frases qual ação o vendedor
   deve tomar nos próximos 3 dias úteis para reverter o sinal negativo.
```

---

#### MELHORIA P6 — OPORTUNIDADES PERDIDAS
**Gap atual:** Identifica o que faltou, mas não quantifica o custo. "Impacto alto/médio/baixo" é subjetivo demais para apresentar ao Diretor.

**Versão revisada — substituir `impacto_estimado` por:**

```
## NOVA COLUNA: valor_potencial_mensal_R$
Para cada oportunidade perdida, estime em R$ o impacto mensal:
- OP4 (referral não solicitado): R$ 500 por referral convertido (LTV 12 meses)
- OP5 (dado estratégico não explorado): R$ 1.500 por conta nova média

## Tabela de valor por produto (para OP2 e OP6):
| Produto | Receita mensal estimada por unidade |
|---------|-------------------------------------|
| PR3 (Telemetria) | R$ 50/veículo |
| PR4 (Proteção) | R$ 80/veículo |
| PR7 (Contrato anual) | R$ 200 (retenção de churn) |
| PR8 (Elétrico) | R$ 3.600/veículo |
| PR9 (ZARP/Meoo) | R$ 300/contrato |

## NOVA QUESTÃO FINAL:
6. Qual é o valor total de receita mensal que ficou na mesa neste período,
   somando as oportunidades perdidas? Apresente como:
   "R$ X/mês de receita recorrente não capturada."
```

---

#### MELHORIA P10 — PROMESSAS
**Gap atual:** Sem ID de promessa, é impossível rastrear cumprimento entre sessões de análise diferentes.

**Versão revisada — adicionar ao início:**

```
## PRÉ-PROCESSAMENTO OBRIGATÓRIO
Antes de analisar promessas, ordene as ligações de cada cliente por data (crescente).
Numere cada promessa com ID único: [cliente_id]-PM-[sequencial]
Ex: 22154206-PM-001

## FORMATO DE SAÍDA REVISADO
promise_id,cliente_id,vendedor,data_promessa,ligacao_origem,
tipo_promessa,frase_exata_ou_resumo,prazo_prometido,
data_verificacao,ligacao_verificacao,foi_cumprida,
evidencia,impacto_no_cliente,status_atual

Onde:
- promise_id: ID único rastreável [cliente_id]-PM-[nnn]
- prazo_prometido: data ou "sem prazo definido"
- status_atual: cumprida / pendente / vencida / nao_verificavel

## ALERTA AUTOMÁTICO:
Liste ao final todas as promessas com status_atual = "vencida" ou "pendente"
ordenadas por antiguidade. Estas são as ações mais urgentes do vendedor.
```

---

## PARTE 2 — ARQUITETURA DE ANÁLISE (OPERATING MODEL)

### 2.1 Cadência Operacional

```
SEGUNDA │ TERÇA  │ QUARTA │ QUINTA │ SEXTA  │
────────┼────────┼────────┼────────┼────────┤
P1+P6   │ P4+P10 │ P5+P8  │ P7+P11 │ SÍNTESE│
Diário  │ Semanal│ Semanal│ Semanal│ Semanal│
Analista│ Analista│ Coord.│ Coord. │ Gerente│
```

**Ciclo Mensal:**
- Semana 1: Análise completa dos 12 prompts (todas as ligações do mês)
- Semana 2-3: Acompanhamento semanal (P1, P4, P6, P10)
- Semana 4: Revisão de tendência + apresentação ao Diretor

### 2.2 Fluxo Ideal de Uso

```
[STT/Transcrição]
       ↓
[gerar_para_gpt.py]
       ↓
[TRIAGEM — P2: Tipo de Ligação]
       │
       ├── nao_era_venda → arquivo operacional (alimenta P3 semanal)
       │
       └── comercial/misto → CAMADA PRIMÁRIA
              ↓
       [P1: Conversão + P6: Op. Perdidas]  ← DIÁRIO
              ↓
       [P4: Health Score + P10: Promessas] ← SEMANAL
              ↓
       [P5: Challenger + P8: Objeções]     ← COACHING
              ↓
       [P7: Cross-sell + P11: Competitivo] ← ESTRATÉGICO
              ↓
       [Dashboard Unificado → Reunião Segunda]
```

### 2.3 Integração dos Outputs em Dashboard Unificado

| Camada | Prompts Fonte | Métrica no Dashboard | Responsável |
|--------|--------------|---------------------|-------------|
| **Receita** | P1, P7 | Taxa de conversão semanal / Receita incremental identificada | Gerente |
| **Risco** | P4, P10, P11 | Clientes em alerta / Promessas vencidas / Contas com concorrente ativo | Gerente |
| **Comportamento** | P5, P8, P9 | Score Challenger por vendedor / Taxa de objeção superada / Qualidade de fechamento | Coordenador |
| **Eficiência** | P2, P3, P12 | % ligações com tentativa comercial / Problemas resolvidos na ligação / Talk ratio | Analista |

### 2.4 KPIs Primários do Squad de Excelência

| # | KPI | Fórmula | Meta (90 dias) | Fonte |
|---|-----|---------|----------------|-------|
| 1 | **Taxa de Tentativa Comercial** | Ligações com tentativa_comercial=SIM / total ligações não-comerciais | +30pp (de ~20% para ~50%) | P1, P2 |
| 2 | **Score Challenger Médio** | Média de ligacoes_com_challenger / total por vendedor | ≥40% do time acima de 2 CH/semana | P5 |
| 3 | **Taxa de Promessa Cumprida** | Promessas cumpridas / (cumpridas + não cumpridas) | ≥85% | P10 |
| 4 | **Oportunidades Perdidas de Alto Impacto** | Ligações com OP2+OP5+OP6 e impacto=alto / total | Redução de 40% | P6 |
| 5 | **Health Score Médio da Carteira** | Média de score_total por cliente | Manter ≥8/12, nenhum <5 | P4 |

---

## PARTE 3 — MATRIZ DE RESPONSABILIDADES

| Nível | Responsabilidades Principais | Outputs Esperados | Tempo Semanal |
|-------|------------------------------|-------------------|---------------|
| **Analista** | Rodar P1, P2, P6 diariamente. Consolidar CSV dos 12 prompts semanalmente. Manter dashboard atualizado. Alertar sobre promessas vencidas (P10) e clientes em alerta (P4). | Dashboard atualizado toda segunda 8h. Lista de oportunidades perdidas da semana. Ranking de tentativa comercial por vendedor. | **8–10h/semana** |
| **Coordenador** | Analisar outputs de P5 e P8 para identificar gaps de coaching. Conduzir 1:1 semanal com vendedores usando evidências de transcrição. Validar health score (P4) com contexto de CRM. Escalar alertas competitivos (P11) ao Gerente. | Relatório semanal de comportamento por vendedor. Plano de coaching com frases reais das transcrições. Ações de retenção para contas em alerta. | **6–8h/semana** |
| **Gerente** | Revisar dashboard toda segunda. Decidir sobre contas com churn_risk=alto (P4). Aprovar estratégia de cross-sell (P7) para top 5 contas. Monitorar KPIs do squad. Apresentar insights ao Diretor quinzenalmente. | Relatório executivo quinzenal (1 página). Decisões de ação em contas críticas documentadas. Meta de KPIs revisada mensalmente. | **3–4h/semana** |
| **Diretor** | Consumir dashboard executivo toda segunda (15 min). Aprovar iniciativas de produto com base em P3 (problemas sistêmicos). Usar P11 (intel. competitiva) para estratégia de mercado. Validar roadmap trimestral do squad. | Decisões sobre investimento em tech stack. Alinhamento com time de produto sobre problemas sistêmicos. Aprovação de programa de coaching. | **1–2h/semana** |

---

## PARTE 4 — ROADMAP 90 DIAS

### Semana 1–2: Quick Wins

| Ação | Responsável | Impacto |
|------|-------------|---------|
| Rodar P6 em todas as 87 ligações e calcular `valor_potencial_mensal_R$` total | Analista | Quantifica o que está sendo perdido — número para apresentar ao Diretor |
| Criar alerta semanal automático de promessas PM3+PM4+PM5 não verificadas | Analista | Elimina o maior risco de churn por negligência |
| Compartilhar com cada vendedor as 3 melhores frases Challenger (P5) de Andreza e Pedro | Coordenador | Aprendizado peer-to-peer com evidência real |
| Mapear os 3 clientes com health score mais baixo (P4) e criar plano de ação individual | Gerente | Retenção imediata antes que vire churn |

### Mês 1: Fundamentação

**Objetivo:** Cadência operacional instalada e todos os vendedores conscientes dos próprios gaps.

| Iniciativa | Quem | Entrega |
|------------|------|---------|
| Dashboard unificado no Notion ou Airtable com outputs dos 12 prompts | Analista | Semana 3 |
| Sessão de calibração: vendedor ouve 3 ligações próprias com feedback estruturado (P9 + P5) | Coordenador | Semana 3–4 |
| Protocolo de encerramento padrão (P10 revisado): todo vendedor termina a ligação com promessa ID + prazo | Coordenador | Semana 4 |
| Mapa de produto por situação (P7 revisado): quando cliente diz X → ofereça Y porque Z | Gerente + Analista | Semana 4 |
| Rodada completa dos 12 prompts com KPIs baseline | Analista | Fim do mês 1 |

### Mês 2: Escalada

**Objetivo:** Comportamentos Challenger viram rotina, não exceção.

| Iniciativa | Quem | Entrega |
|------------|------|---------|
| Programa de coaching semanal baseado em P5 e P8: "Momento Challenger da semana" | Coordenador | Toda segunda-feira |
| Playbook de objeções (P8) distribuído e treinado em roleplay | Coordenador | Semana 5–6 |
| Integração Make/Zapier: transcrição nova → dispara análise P1+P6 automaticamente | Analista + IT | Semana 6–7 |
| Teste piloto do Prompt Mestre Integrado com 20 ligações novas | Analista | Semana 7–8 |
| Review de health score: comparar mês 1 vs. mês 2 (campo `tendencia`) | Gerente | Fim do mês 2 |

### Mês 3: Institucionalização

**Objetivo:** Framework vira sistema de gestão, não projeto pontual.

| Iniciativa | Quem | Entrega |
|------------|------|---------|
| SLA definido: toda ligação analisada em 24h via automação | Analista | Semana 9–10 |
| Programa de certificação interna: "Challenger Certificado Localiza" (P5 score ≥ 3 CH/semana por 4 semanas) | Gerente | Semana 10–11 |
| Apresentação ao Diretor: ROI do squad — receita recuperada + churn evitado + upsell gerado | Gerente | Semana 12 |
| Expansão do framework para outras carteiras/regionais | Diretor | Mês 4+ |

### Top 5 Iniciativas Priorizadas

1. **Quantificar oportunidades perdidas em R$** — transforma análise em argumento de negócio
2. **Protocolo de promessas com ID rastreável** — elimina maior causa de churn silencioso
3. **Compartilhamento semanal de frases Challenger reais** — aprendizado de peer sem custo
4. **Automação P1+P6 com Make/Zapier** — elimina fricção de rodar manualmente
5. **Dashboard na segunda 8h** — cria hábito gerencial de consumo do dado

---

## PARTE 5 — DASHBOARD EXECUTIVO (SEGUNDA-FEIRA, 8H)

**O Diretor deve ver exatamente isso, em menos de 15 minutos:**

```
╔══════════════════════════════════════════════════════════════╗
║          PAINEL EXCELÊNCIA COMERCIAL — SEMANA [N]           ║
║          Localiza Frota PJ | [Data]                         ║
╠══════════════════════════════════════════════════╦═══════════╣
║ RECEITA EM RISCO                                 ║  AÇÕES    ║
║ ┌──────────────────────────────────────────┐     ║ URGENTES  ║
║ │ Clientes com alerta (score ≤6): [N]      │     ║           ║
║ │ Maior risco: [cliente_id] — [razão]      │     ║ [N] prom. ║
║ │ Receita mensal em risco: R$[X]           │     ║ vencidas  ║
║ └──────────────────────────────────────────┘     ║           ║
║ OPORTUNIDADES                                    ║ [N] cli.  ║
║ ┌──────────────────────────────────────────┐     ║ c/ concor.║
║ │ Receita não capturada esta semana: R$[X] │     ║ ativo     ║
║ │ Top gap: [produto] em [N] ligações       │     ║           ║
║ │ Vendedor com mais op. perdidas: [nome]   │     ║ [nome]    ║
║ └──────────────────────────────────────────┘     ║ sem contato║
║ COMPORTAMENTO                                    ║ há [N] dias║
║ ┌──────────────────────────────────────────┐     ╠═══════════╣
║ │ Score Challenger: Melhor=[nome] / [score]│     ║  TREND    ║
║ │ Pior=[nome] / [score]                    │     ║ Health:   ║
║ │ Taxa tentativa comercial: [X]% (meta 50%)│     ║ ↑[N] ↓[N] ║
║ │ Taxa promessa cumprida: [X]% (meta 85%)  │     ║ estável   ║
║ └──────────────────────────────────────────┘     ║ [N]       ║
╚══════════════════════════════════════════════════╩═══════════╝
```

**Regra de leitura:** O Diretor só precisa tomar decisão se houver célula vermelha (alerta). Verde = time executa. Vermelho = Diretor decide.

---

## PARTE 6 — PROGRAMA DE TREINAMENTO/COACHING

### Trilha por Nível

**Analista (Mês 1):**
- Dominar os 12 prompts e interpretar CSV
- Certificação em taxonomia (B1-B10, CH1-CH7, OP1-OP8)
- Construir dashboard no Notion/Airtable

**Vendedor (Contínuo):**
- Semana 1: "O que é um momento Challenger?" — ouvir 3 frases reais de Andreza/Pedro
- Semana 2-4: Roleplay de objeções com playbook do P8
- Mês 2: Protocolo de abertura e fechamento (P9 + P10 integrados)
- Mês 3: Certificação Challenger (P5 score mínimo)

**Coordenador (Mês 1-2):**
- Técnica de 1:1 com transcrição: "vou te mostrar o que você disse aqui e o que poderia ter dito"
- Não usar transcrição para punir — usar para construir
- Identificar padrão de gap individual vs. gap de time

### Tech Stack Sugerido

| Ferramenta | Uso | Custo estimado |
|------------|-----|----------------|
| **Make (Integromat)** | Automatizar disparo de análise quando nova transcrição chega | R$ 150/mês |
| **Airtable** | Base de dados de ligações + outputs CSV + dashboard | R$ 200/mês |
| **Notion** | Playbooks, roteiros, protocolo de promessas | R$ 50/mês |
| **Power BI** | Dashboard executivo com dados históricos | Grátis (básico) |
| **OpenAI API (GPT-4o)** | Automação dos 12 prompts sem interface manual | R$ 0,10–0,50/análise |
| **AssemblyAI ou Whisper** | STT com diarização de qualidade superior | R$ 0,01/min |

**Stack mínimo viável (Mês 1):** Airtable + Make + GPT-4o API = R$ 400/mês
**Stack completo (Mês 3):** Adicionar Power BI + AssemblyAI = R$ 700/mês

---

## PARTE 7 — RISCOS E CUIDADOS

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| **Vendedor sente que está sendo vigiado** | Alta | Alto | Comunicar como ferramenta de desenvolvimento, não auditoria. Compartilhar destaques positivos antes dos gaps. |
| **Qualidade do STT cria viés** | Média | Alto | Calibrar prompts com ligações que tenham STT limpo primeiro. Analista revisita manualmente 10% dos outputs. |
| **Sobreposição de contexto no GPT** | Alta (87+ ligações) | Médio | Nunca rodar todos os 87 clientes de uma vez. Máximo 15-20 ligações por sessão. Usar o Prompt Mestre com filtro de prioridade. |
| **Insight sem dono = insight ignorado** | Alta | Alto | Toda análise termina com "ação para [nome] até [data]". Sem dono, não vai ao dashboard. |
| **Tech stack substituindo humano no coaching** | Baixa | Alto | LLM identifica o padrão. Humano dá o feedback. A transcrição é evidência, não sentença. |
| **Escalada sem critério claro** | Média | Médio | Health score define automaticamente quem escala: score ≤6 ou tendência caindo → Gerente decide em 24h. |

---

*Documento produzido com base em análise das 87 ligações reais da carteira Localiza — junho 2026.*
*Próxima revisão sugerida: setembro 2026 (após 90 dias de operação do roadmap).*
