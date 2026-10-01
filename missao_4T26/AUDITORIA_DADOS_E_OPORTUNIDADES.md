# Auditoria de dados e mapa de oportunidades — Missão 4T26

> **Draft v0.1 — 01/10/2026.** Complementa `PLANO_MISSAO_4T26.md`.
> Escopo: **todos** os dados do repositório + o CSV de setembro da consulta do Power BI. Sem prompts novos.
> Números reproduzíveis com `scripts/auditoria_dados_missao.py` e `scripts/baseline_carga_operacional.py`;
> o catálogo completo (com pergunta, dados, esforço e impacto) está em `anexos/catalogo_oportunidades.csv`.

---

## 0. Em dois minutos

1. **Temos 12 ativos de dados.** 5 recebem selo verde, 5 amarelo e 2 vermelho (seção 1). O mais valioso é o CSV de setembro:
   19.078 tentativas, 67 carteiras, 88 colunas juntando CRM, duração, Gemini (Aletheia) e GPT (classificador).
2. **O número da carga operacional resiste a duas réguas independentes, a tendência não.** Pela definição completa (tudo o que
   não é negociação) o GPT dá **43,2%** do tempo de ligação e o Gemini dá **47,6%**. Mas o GPT sobe de 37% para 55% ao longo
   de setembro enquanto o Gemini cai de 50% para 43%. O GPT mudou de comportamento no meio do mês (seção 3).
3. **O tempo do vendedor ao telefone:** negociação **35,1%** · carga operacional **43,2%** · relacionamento sem demanda **20,6%** ·
   sem conteúdo 1,1%.
4. **Tempo ótimo de ligação comercial:** os fechamentos por hora de conversa sobem até **5–20 min** (1,21–1,25) e caem acima de
   20 min (0,90). **27% das ligações de negociação (≥ 5 min) geram 68% dos fechamentos.**
5. **Challenger e SPIN:** a escada *dado concreto → conexão com a situação → reação do cliente* tem 14,0% → 20,1% → 22,1%; o
   Challenger completo aparece em 9,1% das ligações. No SPIN, **Implicação é o elo fraco** (50,7% das ligações com nota 1).
6. **Contato e cadência:** 57% das tentativas terminam como Sem Sucesso; **2.985 clientes** ficaram com uma única tentativa falha
   (≈ 900 conversas/mês se houvesse 2ª tentativa); só **15,5%** das ligações que pedem retorno têm novo contato em 14 dias.
7. **Mapeei 83 oportunidades em 9 eixos** (seção 5): 50 já têm dado pronto, 24 dependem de ajuste e
   9 dependem de dado que não temos.
8. **As duas maiores lacunas** são o **resultado real** depois da ligação (as diárias param em junho/26) e a **base de
   treinamento** (notas, presença, trilha), necessária para a trilha de conhecimento.

---

## 1. Inventário e selo de confiança

| # | Ativo | Período · tamanho | Motor | Selo | Observação |
|---|---|---|---|---|---|
| A1 | CSV de setembro — CRM/telefonia (status, tipo, hora, duração, carteira, vendedor) | 31/08–30/09 · 19.078 linhas | Sistema | **Verde** | Duração só até 22/09; horário em UTC |
| A2 | CSV de setembro — Gemini/Aletheia (análise, SPIN, categorização) | 5.839 analisadas | Gemini | **Verde** | Estável dia a dia (SPIN médio 2,52–2,89); campos saturados (F-09) |
| A3 | CSV de setembro — GPT C12 (P1, P2, P3, P5) | 01–25/09 · 4.745 GPT + 1.487 automáticas | GPT | **Amarelo** | Nível confiável, **tendência não** (F-01) |
| A4 | Consolidado de junho | 01–29/06 · 6.623 ligações | Gemini | **Amarelo** | Outro motor; sem vendedor/carteira |
| A5 | Consolidado de julho + P1–P11 | 01–31/07 · 10.240 ligações (64% classificadas) | Gemini | **Amarelo** | 8,6% sem cliente; sem sentimento |
| A6 | Diárias AM/AD por código | 07/25–06/26 · 37.347 códigos | Sistema | **Verde** | Perfil de valor ok; **resultado defasado 3 meses** |
| A7 | Cruzamentos (ligações × diárias, reservas, ritmo) | jun · 1.275 ligações | Misto | **Vermelho** | Reservas cobrem 11–19% dos clientes; útil como método |
| A8 | Scoring de potencial | jun e jul | Heurístico | **Vermelho** | Documentado como mal calibrado (`PERSONAS_ALETHEIA.md`) |
| A9 | Banco de exemplos, candidatos e Guia Challenger | 238 anotados + 250 candidatos | Painel de agentes | **Verde** | Validado por maioria; nomes mascarados |
| A10 | Exploração qualitativa (Fable) | 243 arquivos | LLM | **Amarelo** | Amostral (456 de 6.623 em P3/P7) |
| A11 | Documentos analíticos (`analises/`, `apresentacao/`) | jun–ago | Humano + LLM | **Amarelo** | `DICIONARIO_TECNICO.md` desatualizado |
| A12 | Código e prompts (classificador, taxonomia) | `scripts/`, `prompts/` | — | **Verde** | Fonte de verdade: `prompts_nivel1_por_ligacao.md` + `analisar_gemini_julho.py` |

**Pontos fortes:** chaves únicas (0 duplicados em `id_transcricao` e `segment_id`); duração presente em 100% das Completed até
22/09; Gemini estável e completo até 30/09; trechos de Challenger e problemas ancorados em texto literal; pipeline com
retomada e controle de custo diário.

**O que não existe no repositório:** agosto; vendedor/carteira nos consolidados de junho e julho; resultado real depois da
ligação; base de treinamento; custo-hora; log de telefonia; áudio.

---

## 2. Auditoria de qualidade — achados

| ID | Sev. | Achado | Evidência | Impacto | Ação |
|---|---|---|---|---|---|
| F-01 | **Crítico** | O classificador GPT muda de comportamento dentro de setembro | Taxa de problema 0% (01/09) → 13,6% (02–14) → 27,5% (15–25); 18/09 fora do padrão (Challenger 26,7%, era venda 56%) | Impede medir redução | Reprocessar setembro com uma versão e gravar a versão em cada linha (E2) |
| F-02 | **Crítico** | Duração ausente de 23/09 em diante | 100% das Completed até 22/09; 0% depois | KPI de tempo cego em 6 dias úteis | Chamado em `Tempo_de_ligação` |
| F-03 | **Crítico** | Motores diferentes em cada mês | Challenger 29,1% (jun) → 18,9% (jul) → 9,1% (set); fechou 5,1% → 5,3% → 3,2%; agosto ausente | Tendência entre meses não é comparável | Comparar só dentro do mesmo motor |
| F-04 | **Crítico** | Resultado real não é verificável | "Fechou" é o que foi dito na ligação; reservas (jun) cobrem 11–19% dos clientes por desfecho; diárias param em 06/2026 | Sem prova de conversão ou ROI | Atualizar diárias e reservas (O-72) |
| F-05 | Alto | Conversas reais registradas como Sem Sucesso/Open | 613 conversas GPT (13%), 143 com problema, sem duração nem Gemini | Subestima a carga | Tratar como "conversa sem duração" e revisar o registro |
| F-06 | Alto | Cobertura incompleta | 2.016 Completed sem GPT (28–30/09: 1.035; 31/08: 279; 24/09: 202); 657 Completed sem Gemini (10%) | Dias recentes sem classificação | Rodar o classificador em D-1 |
| F-07 | Alto | A qualidade do Challenger perdeu variância | 358 de 430 (83%) 'alta', 9 'baixa' | Sem escala para treinar e medir | Usar as sub-flags (dado, conexão, reação) como escala |
| F-08 | Alto | IDs de cliente quebrados | 19,3% com menos de 8 dígitos; 7,8% nulos; julho: 121 '00000000' e 758 'SEMINFO' | Junção com diárias só em 53% das linhas | Normalizar com 8 dígitos no Power Query |
| F-09 | Alto | Campos saturados ou mortos | `nota_demanda_atendimento` = 0 em 100%; oportunidades VERDADEIRO 92%; demanda de atendimento 81%; nova visita 79% | Não discriminam | Retirar de filtros e KPIs |
| F-10 | Alto | Diárias defasadas | Último mês 2026-06; 53% de match | Perfil de valor desatualizado | Atualizar jul–set |
| F-11 | Médio | Horário em UTC | Picos 12–14h e 17–20h UTC = 9–11h e 14–17h BRT | Análise por hora errada sem ajuste | Subtrair 3h no Power Query |
| F-12 | Médio | Rótulos sujos | `p5_teve_challenger` com 'CH1', 'CHALLENGER', 'NA0'; `p9_desfecho` com caixa mista; 'supporte_operacional'; `p1_desfecho` com valores de `p2_tipo` | Contagens divididas | Dicionário de normalização |
| F-13 | Médio | Régua POSITIVA/INFORMATIVA/DETRATORA | DETRATORA = 38,7% das Completed (basta `objetivo_atingido` = FALSO); critério A verdadeiro em 52,4% | Rótulo amplo e negativo | Revisar regra e nome |
| F-14 | Médio | Estimativas em R$ (P6) | R$ 2,68 mi em 3.729 de 5.076 ligações | Valor do modelo, não verificado | Usar para ordenar, não como meta |
| F-15 | Médio | Sentimento sem poder | Jun: 98% POSITIVE; jul: 100% nulo | Sem uso | Descartar |
| F-16 | Médio | Pouca série por cliente | Set∩jul = 1.080 de 8.132; set∩jun = 800 de 5.372 | Análise por cliente só dentro do mês | — |
| F-17 | Médio | Carteira e vendedor são 1:1 | 67 carteiras = 67 matrículas | "Por carteira" equivale a "por vendedor" | Política de uso não punitivo; comparar por pares |
| F-18 | Médio | Trechos com nomes de clientes | O classificador mascara só o vendedor | LGPD | Perfis de acesso e máscara |
| F-19 | Baixo | Duração extrema | Máx. 3.631 s; 2,5% < 30 s | Distorce médias | Mediana e P90 |
| F-20 | Baixo | Status Open sem análise | 1.647 (8,6%), 0% analisadas | Desconhecido | Investigar o significado |
| F-21 | Baixo | Documentação desatualizada | `DICIONARIO_TECNICO.md`; `Claude.md` só trata de diárias; a `PERSONAS_ALETHEIA.md` cita `CONTEUDO_4SLIDES` (o arquivo é `5SLIDES`) | Confusão | Novo `CLAUDE.md` |

---

## 3. Duas réguas, uma verdade

A carga operacional medida pelos dois motores, por semana (01–22/09, Completed com duração):

| Semana | GPT: horas | GPT: carga operacional (problema + suporte + cobrança + pós-venda + dúvida de contrato) | Gemini: horas | Gemini: categoria Suporte |
|---|---:|---:|---:|---:|
| 31/08–06/09 | 69,2 | 37,1% | 73,2 | 50,2% |
| 07–13/09 | 68,8 | 35,0% | 68,9 | 49,1% |
| 14–20/09 | 89,1 | 49,1% | 89,9 | 46,3% |
| 21–22/09 | 38,8 | 55,0% | 39,7 | 43,1% |
| **Período** | **265,9** | **43,2%** | **271,7** | **47,6%** |

**Leitura:** o **nível** está entre 43% e 48% pelos dois lados, então é seguro dizer que perto de metade do tempo ao telefone
não é negociação. A **tendência** não é segura: os motores apontam para lados opostos. Até o baseline congelado (E2), o BI deve
mostrar as duas réguas lado a lado e a tendência com selo amarelo. O Gemini é a régua de referência porque ficou estável o
mês inteiro (SPIN médio diário entre 2,52 e 2,89, desvio de 0,10) e cobre até 30/09.

---

## 4. As quatro personas avaliam os dados

### 4.1 Quem são

| Persona | Pergunta-guia | Decide | Critério de nota |
|---|---|---|---|
| **P1 · Auditoria de Dados** | "Posso mostrar esse número à diretoria sem constrangimento?" | O que entra no BI e com que selo | Completude, consistência entre fontes, estabilidade no tempo, rastreabilidade, privacidade |
| **P2 · Gerência Operacional** (assina as horas devolvidas) | "Onde está o tempo e que alavanca o devolve sem piorar o atendimento?" | Onde atacar a carga e como medir o ganho | Tempo, pendências, reincidência, origem do problema |
| **P3 · Gerência Comercial / Coach** | "O que os melhores fazem, quando insistir ou encerrar, a quem retornar?" | Cadência, priorização e coaching | Conversão, tempo ótimo, contato, follow-up, mercado |
| **P4 · Aprendizagem (Treinamento)** | "Que habilidade falta, que exemplo real ensina e como sei que mudou?" | Conteúdo, trilha e avaliação | Competências, banco de exemplos, evidência literal |

P2 e P3 correspondem às personas Gerente de Operações (a ser formalizada) e Gerente de Vendas do `PERSONAS_ALETHEIA.md`; P4 é o
Especialista de Treinamentos; P1 é o Especialista de Excelência Comercial em modo auditor.

### 4.2 Nota de utilidade por ativo (0 a 5) e confiabilidade (P1)

| Ativo | Confiab. (P1) | Util. P2 | Util. P3 | Util. P4 | Selo |
|---|---:|---:|---:|---:|---|
| A1 CSV set — CRM/telefonia | 4 | 5 | 5 | 2 | Verde |
| A2 CSV set — Gemini | 4 | 3 | 4 | 5 | Verde |
| A3 CSV set — GPT C12 | 2 | 5 | 4 | 4 | Amarelo |
| A4 Consolidado jun | 3 | 2 | 4 | 3 | Amarelo |
| A5 Consolidado jul + P1–P11 | 3 | 3 | 5 | 4 | Amarelo |
| A6 Diárias | 4 | 3 | 5 | 1 | Verde |
| A7 Cruzamentos | 2 | 2 | 3 | 1 | Vermelho |
| A8 Scoring de potencial | 1 | 1 | 2 | 1 | Vermelho |
| A9 Banco de exemplos e Guia | 4 | 1 | 3 | 5 | Verde |
| A10 Exploração Fable | 3 | 3 | 4 | 4 | Amarelo |
| A11 Documentos analíticos | 3 | 2 | 4 | 3 | Amarelo |
| A12 Código e prompts | 4 | 1 | 2 | 3 | Verde |

*Notas são avaliação qualitativa minha, para discussão; não saem de fórmula.*

### 4.3 Veredito de cada persona

**P1 · Auditoria de Dados**
- *Usa já:* A1, A2, A6 (perfil), A12.
- *Recusa:* tendência de K1 baseada no GPT antes do E2; conclusões dos cruzamentos de reservas; scoring de potencial; sentimento.
- *Pede:* versão por linha, auditoria amostral de 100 ligações/mês, IDs normalizados, reconciliação de status, dados de resultado.
- *Veredito:* "O **nível** da carga (43–48%) pode ir ao diretor hoje. A **tendência** só depois do baseline congelado."

**P2 · Gerência Operacional**
- *Usa já:* carga completa, Pareto de problemas, pendências, reincidência, origem (inbound × outbound), tamanho do cliente.
- *Recusa:* converter horas em R$ sem premissa; tratar tempo de ligação como carga total (são ≈ 17 min de conversa por vendedor/dia).
- *Pede:* diário de tempo em amostra, custo-hora, tickets fora do telefone, mapa dos processos de P1/P2/P13, escala da equipe.
- *Veredito:* "Dá para agir em P1, P2 e P13 e em clientes reincidentes. O ganho em horas precisa de amostra fora do telefone para ser assinado."

**P3 · Gerência Comercial / Coach**
- *Usa já:* tempo ótimo, recontato, follow-up, decisor, B1–B10 e objeções (jun/jul), concorrência, carteiras desviantes.
- *Recusa:* comparar carteiras sem normalizar (DTIN4 tem outro perfil: carga 31% contra 43–47% nos demais); usar o scoring de potencial.
- *Pede:* resultado real pós-ligação, motivo da falha de contato, perfil da carteira (porte, segmento), metas.
- *Veredito:* "Os maiores ganhos comerciais prontos são **recontato** e **follow-up**: não dependem de nenhuma melhoria de dado."

**P4 · Aprendizagem**
- *Usa já:* SPIN, escada do Challenger, trechos reais, exemplos anotados, objeções, Guia Challenger.
- *Recusa:* meta binária de Challenger (SIM/NÃO); ranking individual como motivador.
- *Pede:* notas de treinamento, escala de qualidade com variância, curadoria humana do conteúdo, regra de LGPD para trechos.
- *Veredito:* "Há material para um MVP, mas só **depois** de recalibrar a escala de qualidade e obter a base de treinamento."

---

## 5. Catálogo de oportunidades

83 oportunidades. **Prontidão:** *Pronto* = dado existe; *Parcial* = precisa de ajuste ou dado complementar; *Lacuna* = depende de dado que
não temos. **Onda:** 1 = out–nov; 2 = nov–dez; 3 = depende de lacuna ou fica para 2027. **Persona:** DAD = auditoria, OPE =
operacional, COM = comercial, APR = aprendizagem. Campos completos (pergunta, dados, esforço, entrega) em
`anexos/catalogo_oportunidades.csv`.

### E1 · Carga operacional e capacidade

| ID | Oportunidade | Evidência hoje | Prontidão | Impacto | Persona | Onda |
|---|---|---|---|---|---|---:|
| O-01 | Carga operacional completa | 43,2% do tempo (114,8 h em 15 d.u.): 30,0% com problema + 13,1% suporte, cobrança, pós-venda e dúvida de contrato. Régua Gemini (categoria Suporte): 47,6% | Pronto | Alto | OPE | 1 |
| O-02 | Mapa de alocação do tempo | Negociação 35,1% · carga operacional 43,2% · relacionamento sem demanda 20,6% · sem conteúdo 1,1% | Pronto | Alto | OPE | 1 |
| O-03 | Pareto do tempo por problema | P1 acesso/sistema 36,8% · P2 faturamento 17,2% · P13 crédito/cadastro PJ 13,5% = 67,5% do tempo com problema | Pronto | Alto | OPE | 1 |
| O-04 | Horas excedentes por problema | TMA 432 s vs 232 s (1,9×); ≈ 37 h excedentes em 15 d.u. (≈ 50–60 h/mês) | Pronto | Médio | OPE | 1 |
| O-05 | Pendências geradas | 89,7% não resolvidos na ligação; 698 pendências em 15 d.u. (≈ 47/dia) | Pronto | Alto | OPE | 1 |
| O-06 | Reincidência de problema | 18,8% das ligações com problema são de clientes com 2+ ligações com problema no período | Pronto | Alto | OPE | 1 |
| O-07 | Origem do problema (inbound x outbound) | Taxa de problema 36% no inbound vs 17% no outbound; 78% do volume com problema nasce de ligação ativa | Pronto | Médio | OPE | 1 |
| O-08 | Problema × tamanho do cliente | Quartil de maior volume (≈ 61 diárias/mês): 32,4% de taxa de problema vs 16–19% nos demais; 60,7% do tempo dessas contas é carga operacional | Parcial | Alto | OPE | 2 |
| O-09 | Composição do atendimento sem problema | Sem problema: suporte 23,0 h · dúvida de contrato 8,0 h · cobrança 2,1 h · pós-venda 1,8 h (34,9 h) | Pronto | Médio | OPE | 1 |
| O-10 | Candidatos a autoatendimento/automação | P1: 208 ligações, 29,4 h · P2: 132 ligações, 13,8 h. A causa raiz não está nos dados (só o sintoma) | Parcial | Alto | OPE | 2 |
| O-11 | Carga fora da ligação | ≈ 17 min de conversa/vendedor/dia, 5 min com problema; o resto é invisível aos dados | Lacuna | Alto | OPE | 2 |
| O-12 | Horas devolvidas em R$ | Sem premissa de custo no repositório | Lacuna | Alto | OPE | 2 |
| O-13 | Sazonalidade da carga | Taxa de problema por dia entre 11% e 35% (hoje contaminada pelo drift do classificador) | Parcial | Médio | OPE | 2 |
| O-14 | Alerta de incidente sistêmico | P1 oscila de 2,4% a 11% das ligações por dia | Parcial | Médio | OPE | 2 |
| O-15 | Conversas reais marcadas como Sem Sucesso/Open | 613 conversas classificadas pelo GPT (13%) têm status Sem Sucesso/Open; 143 com problema; sem duração | Pronto | Médio | DAD | 1 |

### E2 · Tempo e ritmo da ligação

| ID | Oportunidade | Evidência hoje | Prontidão | Impacto | Persona | Onda |
|---|---|---|---|---|---|---:|
| O-16 | Tempo ótimo por tipo de ligação | Fechamentos por hora de conversa: 0,9 (<1 min) · 1,0–1,1 (1–5 min) · 1,21–1,25 (5–20 min) · 0,90 (>20 min). Mediana das ligações fechadas: nova venda 9 min, renovação 6–7 min, upsell 4–5 min | Pronto | Alto | COM | 1 |
| O-17 | Janela de aprofundamento | 27% das ligações de negociação (≥ 5 min) geram 68% dos fechamentos e usam 66% do tempo | Pronto | Alto | COM | 1 |
| O-18 | Ligações de negociação com menos de 3 min | 55,6% das ligações de negociação duram < 3 min e fecham 2,9%. Falta separar renovação por link de sondagem | Parcial | Médio | COM | 2 |
| O-19 | TMA alvo por tipo de ligação | Mediana: nova venda 277 s · renovação 293 s · suporte 267 s · cobrança 239 s · dúvida de contrato 306 s · relacionamento sem demanda 107 s | Pronto | Médio | COM | 1 |
| O-20 | Duração × Challenger e SPIN | Challenger: mediana 400 s vs 248 s. SPIN médio de 2,6 (1–2 min) a 3,8 (>20 min). Com duração controlada (5–12 min), o fechamento com Challenger é igual ao sem (9,3% vs 8,7%) | Pronto | Alto | APR | 1 |
| O-21 | Ligações vazias e secretária eletrônica | 12% das Completed duram < 60 s; secretária eletrônica em 5,4% das analisadas; sem conteúdo = 1,1% do tempo | Pronto | Baixo | OPE | 2 |
| O-22 | Benchmark de TMA por carteira | TMA médio de 129 s a 575 s entre carteiras (≥ 40 ligações) | Pronto | Médio | COM | 1 |
| O-23 | Talk ratio, silêncio e interrupções | Hoje só há estimativa por contagem de turnos (jun) | Lacuna | Médio | APR | 3 |

### E3 · Contactabilidade e cadência

| ID | Oportunidade | Evidência hoje | Prontidão | Impacto | Persona | Onda |
|---|---|---|---|---|---|---:|
| O-24 | Funil de contato | 19.078 tentativas → 34,0% Completed; 57,3% Sem Sucesso; 8,6% Open | Pronto | Alto | COM | 1 |
| O-25 | Recontato de clientes não atendidos | 4.766 clientes outbound com 1 tentativa falha; 2.985 até 23/09 sem 2ª tentativa; a 2ª tentativa atende 30,5% → ≈ 900 conversas/mês | Pronto | Alto | COM | 1 |
| O-26 | Melhor horário de ligação | 36,5% (11h) e 36,6% (12h) vs 30,2% (13h); 18h 40,4% (n=267). Diferença ≤ 6 p.p. | Pronto | Baixo | COM | 2 |
| O-27 | Dia da semana | 33% a 35% em todos os dias úteis (achado negativo) | Pronto | Baixo | COM | 3 |
| O-28 | Inbound como porta do suporte | Inbound = 4,8% das ligações, 69,2% atendidas, 36% com problema | Pronto | Médio | OPE | 2 |
| O-29 | Esforço de discagem | 14,6 tentativas e 5,0 atendidas por vendedor/dia (66% sem conversa) | Pronto | Alto | OPE | 1 |
| O-30 | Taxa de atendimento por carteira | 12,5% a 58,5% entre carteiras | Pronto | Médio | COM | 2 |
| O-31 | Motivo da falha de contato | Só existe o status Sem Sucesso | Lacuna | Médio | OPE | 3 |
| O-32 | Cadência ideal de tentativas | 1ª 36,5% · 2ª 30,5% · 3ª 33,5% · 4ª 32,8% (sem queda forte até a 4ª) | Pronto | Médio | COM | 2 |

### E4 · Competências: Challenger, SPIN e trilha

| ID | Oportunidade | Evidência hoje | Prontidão | Impacto | Persona | Onda |
|---|---|---|---|---|---|---:|
| O-33 | Mapa de competências por carteira | Entre carteiras (≥ 40 lig.): SPIN médio 2,9 (2,1 a 3,4); Challenger 9,4% (0,8% a 21,7%) | Pronto | Alto | APR | 1 |
| O-34 | Escada do Challenger | Trouxe dado 14,0% · conectou à situação 20,1% · cliente reagiu 22,1% · Challenger completo 9,1% | Pronto | Alto | APR | 1 |
| O-35 | SPIN: elo fraco | Implicação: 50,7% das ligações com nota 1 (média 2,0) · Problema 27,2% · Necessidade 21,0% · Situação 4,0% | Pronto | Alto | APR | 1 |
| O-36 | Banco de conteúdo real | 270 trechos literais de Challenger (set) + ≈ 760 de problemas + 238 exemplos anotados (P1, P2, P3, P5, P9) + 250 candidatos + Guia Challenger | Pronto | Alto | APR | 1 |
| O-37 | Contraexemplos | 86 casos de Challenger sem dado concreto; exemplos 'não challenger' já anotados no few-shot | Pronto | Médio | APR | 2 |
| O-38 | Efeito da qualidade do Challenger no resultado | Jun/Jul (venda): qualidade alta fecha 14,1%/22,0% vs baixa 2,2%/3,0% e nenhum 6,8%/7,5%. Em set, 83% dos Challenger são 'alta' (sem variância) | Parcial | Alto | APR | 2 |
| O-39 | Curva de aprendizado | Exige régua estável e ≥ 8 semanas | Parcial | Alto | APR | 2 |
| O-40 | Dados de treinamento | Não há base de treinamento no repositório | Lacuna | Alto | APR | 2 |
| O-41 | Gamificação sem gaming | PERSONAS_ALETHEIA: Challenger SIM/NÃO binário não discrimina; pontuar a qualidade (dado + conexão + reação) | Pronto | Médio | APR | 2 |
| O-42 | Micro-lições por situação | P1/P2/P13 = 67,5% do tempo com problema; só 10,3% resolvidos na ligação. Liga a trilha à missão | Parcial | Alto | APR | 2 |
| O-43 | Trilha por segmento (CNAE) | Maior taxa de problema: obras de infraestrutura 28,9%, arquitetura/engenharia 28,1% | Parcial | Médio | APR | 3 |
| O-44 | Trilha de conhecimento do vendedor (MVP) | Ver seção 6.1 | Parcial | Alto | APR | 2 |

### E5 · Melhores práticas e benchmarks internos

| ID | Oportunidade | Evidência hoje | Prontidão | Impacto | Persona | Onda |
|---|---|---|---|---|---|---:|
| O-45 | Desviantes positivos por carteira | Carteiras com carga operacional ≤ 25% (n ≥ 43): KPI08A, SPI03A, MOI01A, COI04A, KPI07A, NOR05A. Validar contra ruído e perfil de cliente antes de concluir | Parcial | Alto | COM | 2 |
| O-46 | Comportamentos que fecham (B1–B10) | Fechamento com B4 (avisou risco) 16%/34% vs ≈ 8% · B5 (upsell encaixado) 20%/28% vs 7–8% · B6 (urgência real) 16%/30% vs 8% · B3 (usou histórico) 14–15% vs 8% | Pronto | Alto | COM | 1 |
| O-47 | Abertura e fechamento (P9) | 9.684 ligações com abertura, fechamento e prazo classificados | Pronto | Médio | COM | 2 |
| O-48 | Playbook de objeções | Superada: burocracia (OB6) 70% · problema não resolvido (OB5) 56% · preço (OB1) 50% · produto (OB4) 46% · demanda baixa (OB3) 16%. Resposta de eficácia alta supera 99% (819 de 820) | Pronto | Alto | APR | 1 |
| O-49 | Acesso ao decisor | Decisor em 72% das ligações. Em negociação: fechamento 8,4% vs 2,6% e objetivo atingido 77% vs 57% | Pronto | Alto | COM | 1 |
| O-50 | Disciplina de follow-up | 79% das ligações pedem nova visita; só 15,5% têm novo contato em 14 dias | Pronto | Alto | COM | 1 |
| O-51 | Retorno por urgência | Retorno em 14 dias: urgência 10 → 28,9% · 9 → 22,4% · 5 → 16,6% · 3 → 3,7% | Pronto | Médio | COM | 1 |
| O-52 | Promessas do vendedor | 5.251 promessas; 37% sem prazo definido. Cumprimento não é verificável com os dados atuais | Parcial | Médio | COM | 3 |
| O-53 | Contato desatualizado e acesso ao responsável | Não falou com o decisor em 28% das ligações analisadas (1.661 de 5.839): lista de atualização de contatos | Pronto | Médio | COM | 2 |

### E6 · Clientes, carteira e valor

| ID | Oportunidade | Evidência hoje | Prontidão | Impacto | Persona | Onda |
|---|---|---|---|---|---|---:|
| O-54 | Tempo × valor do cliente | Quartil de maior volume consome 30,6% do tempo; mediana de 0,26 min de ligação por diária/mês | Parcial | Alto | COM | 2 |
| O-55 | Prospecção sem histórico | 57% das ligações de nova venda são de clientes sem registro de diárias | Parcial | Médio | COM | 2 |
| O-56 | Health score e risco de churn | Risco alto 15,1% · médio 27,9%; apenas 1.080 clientes aparecem em julho e setembro | Parcial | Alto | COM | 2 |
| O-57 | Oportunidade perdida em R$ | R$ 2,68 mi estimados em 3.729 ligações (OP6 R$ 1,12 mi · OP2 R$ 0,56 mi · OP5 R$ 0,51 mi). Estimativa do modelo, não verificada | Parcial | Médio | COM | 2 |
| O-58 | Cross-sell e janelas perdidas | Produtos mencionados × ofertados × janela perdida por ligação | Pronto | Médio | COM | 2 |
| O-59 | Perfil por CNAE | Obras de infraestrutura 28,9% · arquitetura/engenharia 28,1% · comércio e reparação de veículos 27,0% | Pronto | Médio | COM | 2 |
| O-60 | Mudança de carteira | 2% dos clientes têm carteira diferente entre o CSV e as diárias | Parcial | Baixo | DAD | 3 |

### E7 · Mercado, concorrência e produto

| ID | Oportunidade | Evidência hoje | Prontidão | Impacto | Persona | Onda |
|---|---|---|---|---|---|---:|
| O-61 | Concorrência na voz do cliente | Set (texto livre): Movida 109 menções, Unidas 48. Jul (P11): Movida 200, Unidas 89 | Pronto | Alto | COM | 1 |
| O-62 | Lista de oportunidades: frota própria | ≈ 700 clientes (12% dos analisados) com frota própria; volume declarado em apenas 82 | Parcial | Alto | COM | 2 |
| O-63 | Lista de reconquista: aluguel com concorrente | 376 clientes (6% dos analisados); volume declarado em 13 | Parcial | Alto | COM | 2 |
| O-64 | Problemas sistêmicos para o Produto | Problema principal em set: P1 acesso/sistema 305 · P2 faturamento 173 · P13 crédito/cadastro PJ 161 · P14 preço 38 | Pronto | Alto | OPE | 1 |
| O-65 | Motivos de nova visita e objetivos | Termos mais frequentes: 'dados necessários' 1.246, 'fidelização' 834, 'acompanhamento' ≈ 1.200, 'contrato' 498 | Parcial | Médio | COM | 3 |
| O-66 | Sentimento e satisfação do cliente | Jun: 98% POSITIVE; jul: 100% nulo | Lacuna | Médio | COM | 3 |

### E8 · Qualidade de dados e governança

| ID | Oportunidade | Evidência hoje | Prontidão | Impacto | Persona | Onda |
|---|---|---|---|---|---|---:|
| O-67 | Congelar versão e baseline | Taxa de problema 13,6% (02–14/09) → 27,4% (15–22/09) | Pronto | Alto | DAD | 1 |
| O-68 | Auditoria amostral humana | Não há matriz de confusão | Lacuna | Alto | DAD | 1 |
| O-69 | Recalibrar escalas | Challenger 'alta' = 83% em set. Resolver por regra de pós-processamento (sem novo prompt) | Parcial | Alto | DAD | 2 |
| O-70 | Reconciliar Gemini × GPT | 92,5% dos 'suporte_operacional' do GPT são 'Suporte' no Gemini. Nível de carga: 43,2% (GPT) vs 47,6% (Gemini), com tendências opostas | Pronto | Alto | DAD | 1 |
| O-71 | Normalizar IDs de cliente | 19,3% com < 8 dígitos; 7,8% nulos; julho: 121 '00000000' + 758 'SEMINFO' | Pronto | Médio | DAD | 1 |
| O-72 | Fechar o ciclo com resultado real | Diárias param em 06/2026; reservas (jun) cobrem 11–19% dos clientes por desfecho | Lacuna | Alto | COM | 2 |
| O-73 | Campos saturados ou mortos | nota_demanda_atendimento = 0 em 100%; oportunidades VERDADEIRO em 92%; demanda de atendimento 81%; nova visita 79% | Pronto | Médio | DAD | 1 |
| O-74 | Régua POSITIVA/INFORMATIVA/DETRATORA | DETRATORA = 38,7% das Completed (basta objetivo_atingido = FALSO); critério A verdadeiro em 52,4% | Pronto | Médio | COM | 2 |
| O-75 | LGPD e perfis de acesso | Trechos de set não anonimizam clientes; BI será nominal por carteira | Pronto | Alto | DAD | 1 |
| O-76 | Timestamp e calendário | Em UTC: pico real de ligações 9–11h e 14–17h BRT, com almoço 12–13h | Pronto | Baixo | DAD | 1 |

### E9 · Gestão e BI

| ID | Oportunidade | Evidência hoje | Prontidão | Impacto | Persona | Onda |
|---|---|---|---|---|---|---:|
| O-77 | Alertas diários | Ruído diário de ±3 p.p. → limites por desvio, não por variação de 1 dia | Parcial | Médio | OPE | 2 |
| O-78 | Ritual semanal | Segunda 08h com Gerência Operacional e Comercial | Pronto | Alto | OPE | 1 |
| O-79 | Metas por perfil de carteira | Carga de 16% a 73% entre carteiras; distrital DTIN4 com 31% vs 43–47% nos demais | Parcial | Alto | OPE | 2 |
| O-80 | Simulador de capacidade | Se P1 cair 30% → ≈ 8,8 h por 15 d.u. (≈ 12 h/mês) | Pronto | Médio | OPE | 2 |
| O-81 | Painel de coaching por carteira | 270 trechos de Challenger + ≈ 760 de problemas com evidência literal | Pronto | Alto | COM | 1 |
| O-82 | Fila de ligações prioritárias | Critério existente no Power Query; o scoring de julho foi marcado como mal calibrado | Parcial | Alto | COM | 3 |
| O-83 | Previsão de carga | Sem série estável ainda | Lacuna | Médio | OPE | 3 |


---

## 6. Dois projetos de destaque

### 6.1 Trilha de conhecimento do vendedor ("Duolingo do vendedor")

**Ideia:** cada ligação real vira exercício, e a árvore de habilidades de cada vendedor se atualiza com o que ele faz ao telefone,
sem prova nem curso longo.

**Árvore de habilidades (6 trilhas, todas com dado hoje):**

| Trilha | Degraus | Dado que mede | Linha de base (set) |
|---|---|---|---|
| T1 Diagnóstico SPIN | Situação → Problema → **Implicação** → Necessidade | `nota_spin_*` | Implicação com nota 1 em 50,7% |
| T2 Challenger | Trazer dado → conectar à situação → provocar reação (CH1–CH7) | `p5_trouxe_dado`, `p5_conectou_situacao`, `p5_cliente_reagiu` | 14,0% → 20,1% → 22,1%; completo 9,1% |
| T3 Objeções | Preço, prazo, demanda baixa, produto, problema não resolvido, burocracia, indisponibilidade | JULHO/P8 | Superadas de 16% (demanda baixa) a 70% (burocracia) |
| T4 Decisor e próximo passo | Chegar ao decisor → fechar com data → voltar no prazo | `falou_tomador_decisao`, follow-up | Decisor 72%; retorno em 14 dias 15,5% |
| T5 **Resolver rápido** | Identificar, resolver ou encaminhar P1/P2/P13 em poucos minutos | `tem_problema`, duração, resolvido | 10,3% resolvidos; TMA 432 s |
| T6 Abertura e fechamento | Abertura com contexto → fechamento com prazo | JULHO/P9 | 9.684 ligações classificadas |

**Mecânica proposta:**
1. **Diagnóstico automático:** o perfil de cada carteira nos últimos 30 dias define o nível em cada trilha (os dados já existem).
2. **Lição diária de 3–5 min:** um trecho real mascarado, a pergunta "o que faltou?", a resposta modelo e o motivo (reaproveita o campo `motivo` do few-shot).
3. **Missão da semana:** uma meta de comportamento (ex.: trazer 1 dado concreto em 3 ligações) verificada nas ligações da semana.
4. **XP, sequência e níveis por habilidade;** comparação entre carteiras de perfil parecido, com foco na evolução própria e sem ranking punitivo.
5. **Anti-gaming:** pontuar a qualidade (dado + conexão + reação), nunca o SIM/NÃO; o coach audita 10% dos acertos.
6. **Laço de medição:** lição → comportamento nas ligações em 14 dias → TMA, desfecho e carga operacional.

**Conteúdo já disponível:** 270 trechos literais de Challenger, ≈ 760 trechos de problemas, 238 exemplos anotados, 250 candidatos e o Guia Challenger.
**Conteúdo que falta:** exemplos de qualidade alta além de CH6/CH3 (set: CH6 216, CH3 136, CH4 108, CH1 84, CH5 34, CH7 34, **CH2 29**), curadoria humana e a base de notas de treinamento.

**MVP em dezembro (cabe no plano):** duas trilhas (T2 degrau "dado concreto" e T5 "resolver rápido") para as carteiras-piloto, 10 lições, regra de XP e plano de
medição. Marcos: 13/11 especificação; 27/11 conteúdo curado; 07/12 piloto no ar; 17/12 leitura.

**Riscos:** gaming da métrica; sensação de vigilância; régua do classificador instável; o tempo da lição concorre com a própria
missão de reduzir carga (por isso 3–5 min); LGPD nos trechos.

### 6.2 Tempo ótimo da ligação comercial

Base: 8.262 ligações de negociação (nova venda, upsell, renovação, retenção, misto) de junho, julho e setembro.

| Duração | Ligações | Taxa de fechamento | Fechamentos por hora de conversa |
|---|---:|---:|---:|
| < 30 s | 184 | 0,5% | 0,89 |
| 30–60 s | 915 | 1,2% | 0,91 |
| 1–2 min | 2.142 | 2,8% | 1,10 |
| 2–3 min | 1.350 | 4,7% | 1,14 |
| 3–5 min | 1.414 | 6,4% | 1,00 |
| 5–8 min | 988 | 13,0% | 1,23 |
| 8–12 min | 601 | 20,5% | **1,25** |
| 12–20 min | 424 | 30,4% | 1,21 |
| > 20 min | 244 | 39,8% | 0,90 |

**O que os dados sustentam:**
- A **eficiência** (fechamentos por hora de conversa) é máxima entre **5 e 20 min** e cai acima de 20 min.
- **27%** das ligações de negociação duram 5 min ou mais e produzem **68%** dos fechamentos, usando 66% do tempo.
- **55,6%** das ligações de negociação duram menos de 3 min e fecham 2,9%.
- Mediana das ligações fechadas: nova venda **9 min**, renovação 6–7 min, upsell 4–5 min.
- Challenger e SPIN aparecem em ligações longas, mas, com duração controlada (5–12 min), o fechamento com Challenger não muda em setembro (9,3% vs 8,7%).

**O que os dados NÃO sustentam:** que alongar a ligação *causa* o fechamento. Quem vai fechar tende a conversar mais (causalidade reversa). A taxa de
fechamento por duração é descritiva; a eficiência por hora é a leitura mais útil.

**Como transformar em recomendação (experimento):** nas carteiras-piloto, protocolo de aprofundamento — após 3 min com decisor e dor identificada,
conduzir até 8–12 min; ligação sem demanda encerra em até 2 min com próximo contato registrado. Medir fechamentos por hora e carga operacional contra o controle.
**Metas por tipo (hipótese a validar):** nova venda 8–12 min · renovação 5–7 min · upsell 4–5 min · relacionamento sem demanda ≤ 2 min · suporte reduzir da mediana atual de 4,5 min.

---

## 7. Priorização

**Compromisso x exploração.** O plano compromete poucas coisas (a missão e seus KPIs); o resto é exploração com data para acabar.
A exploração só vira compromisso se passar por um gate (dado pronto, dono, esforço).

| Bloco | Itens | Regra |
|---|---|---|
| **Compromisso** (Canvas) | O-01 a O-07, O-67, O-70, O-71, O-73, O-75, O-78 | Entram nos marcos do plano |
| **Exploração timeboxed** | Tempo ótimo (O-16 a O-22), recontato e follow-up (O-25, O-50, O-51), Challenger e SPIN (O-33 a O-36), concorrência (O-61) | Dossiê com data; vira compromisso se houver dono |
| **Projeto de destaque** | Trilha MVP (O-44) | Gate em 13/11: base de treinamento e régua recalibrada |
| **Depende de lacuna** | Onda 3 | Entra no pedido de dados (seção 8) |

**Dependências entre oportunidades:** O-67 (baseline) antecede O-38, O-39, O-77, O-79; O-72 (resultado real) antecede O-54, O-56, O-82; O-71 (IDs) antecede O-06, O-08, O-54.

As ondas dizem **quando o dado permite**, não **o que será feito**: só vira entrega o bloco Compromisso e o que passar no gate.

### Onda 1 — outubro a novembro (dado pronto, esforço baixo ou médio) (37 itens)

| ID | Oportunidade | Impacto | Esforço | Persona | Entrega |
|---|---|---|---|---|---|
| O-01 | Carga operacional completa | Alto | P | OPE | KPI norte |
| O-02 | Mapa de alocação do tempo | Alto | P | OPE | BI (Mês) |
| O-03 | Pareto do tempo por problema | Alto | P | OPE | BI + dossiê |
| O-05 | Pendências geradas | Alto | P | OPE | KPI |
| O-06 | Reincidência de problema | Alto | P | OPE | Lista ativa |
| O-16 | Tempo ótimo por tipo de ligação | Alto | P | COM | Dossiê |
| O-17 | Janela de aprofundamento | Alto | P | COM | Dossiê |
| O-20 | Duração × Challenger e SPIN | Alto | P | APR | Dossiê |
| O-24 | Funil de contato | Alto | P | COM | BI |
| O-25 | Recontato de clientes não atendidos | Alto | P | COM | Lista ativa |
| O-29 | Esforço de discagem | Alto | P | OPE | KPI |
| O-33 | Mapa de competências por carteira | Alto | M | APR | BI (radar) |
| O-34 | Escada do Challenger | Alto | P | APR | Trilha |
| O-35 | SPIN: elo fraco | Alto | P | APR | Trilha |
| O-36 | Banco de conteúdo real | Alto | M | APR | Biblioteca curada |
| O-46 | Comportamentos que fecham (B1–B10) | Alto | M | COM | Playbook |
| O-48 | Playbook de objeções | Alto | M | APR | Playbook |
| O-49 | Acesso ao decisor | Alto | P | COM | Treino de abordagem |
| O-50 | Disciplina de follow-up | Alto | P | COM | Agenda de retorno |
| O-61 | Concorrência na voz do cliente | Alto | M | COM | Dossiê |
| O-64 | Problemas sistêmicos para o Produto | Alto | P | OPE | Dossiê ao Gerente de Produto |
| O-67 | Congelar versão e baseline | Alto | M | DAD | E2 do plano |
| O-68 | Auditoria amostral humana | Alto | M | DAD | Indicador C4 |
| O-70 | Reconciliar Gemini × GPT | Alto | P | DAD | Régua cruzada |
| O-75 | LGPD e perfis de acesso | Alto | P | DAD | RBAC e máscara |
| O-78 | Ritual semanal | Alto | P | OPE | Rotina |
| O-81 | Painel de coaching por carteira | Alto | M | COM | 1:1 com evidência |
| O-04 | Horas excedentes por problema | Médio | P | OPE | KPI |
| O-07 | Origem do problema (inbound x outbound) | Médio | P | OPE | Dossiê |
| O-09 | Composição do atendimento sem problema | Médio | P | OPE | BI |
| O-15 | Conversas reais marcadas como Sem Sucesso/Open | Médio | P | DAD | Correção de dados |
| O-19 | TMA alvo por tipo de ligação | Médio | P | COM | Metas por tipo |
| O-22 | Benchmark de TMA por carteira | Médio | P | COM | BI |
| O-51 | Retorno por urgência | Médio | P | COM | Fila priorizada |
| O-71 | Normalizar IDs de cliente | Médio | P | DAD | Regra no M |
| O-73 | Campos saturados ou mortos | Médio | P | DAD | Limpeza do BI |
| O-76 | Timestamp e calendário | Baixo | P | DAD | Regra no M |

### Onda 2 — novembro a dezembro (precisa de baseline, ajuste ou dado complementar) (36 itens)

| ID | Oportunidade | Impacto | Esforço | Persona | Entrega |
|---|---|---|---|---|---|
| O-08 | Problema × tamanho do cliente | Alto | M | OPE | Dossiê |
| O-10 | Candidatos a autoatendimento/automação | Alto | M | OPE | Hipótese ao Produto |
| O-11 | Carga fora da ligação | Alto | M | OPE | Amostra de 8–10 vendedores, 1 semana |
| O-12 | Horas devolvidas em R$ | Alto | P | OPE | Premissa com RH/Finanças |
| O-38 | Efeito da qualidade do Challenger no resultado | Alto | M | APR | Recalibrar escala |
| O-39 | Curva de aprendizado | Alto | M | APR | BI |
| O-40 | Dados de treinamento | Alto | M | APR | Pedir base ao T&D/RH |
| O-42 | Micro-lições por situação | Alto | M | APR | Trilha 'Resolver rápido' |
| O-44 | Trilha de conhecimento do vendedor (MVP) | Alto | G | APR | MVP em dezembro |
| O-45 | Desviantes positivos por carteira | Alto | M | COM | Entrevistas + playbook |
| O-54 | Tempo × valor do cliente | Alto | M | COM | Matriz esforço × valor |
| O-56 | Health score e risco de churn | Alto | M | COM | Alerta |
| O-62 | Lista de oportunidades: frota própria | Alto | P | COM | Lista de oportunidades |
| O-63 | Lista de reconquista: aluguel com concorrente | Alto | P | COM | Lista de oportunidades |
| O-69 | Recalibrar escalas | Alto | M | DAD | Regra no M ou no script |
| O-72 | Fechar o ciclo com resultado real | Alto | M | COM | Pedir atualização |
| O-79 | Metas por perfil de carteira | Alto | M | OPE | Pares comparáveis |
| O-13 | Sazonalidade da carga | Médio | P | OPE | BI |
| O-14 | Alerta de incidente sistêmico | Médio | M | OPE | Alerta ao Produto |
| O-18 | Ligações de negociação com menos de 3 min | Médio | M | COM | Dossiê |
| O-28 | Inbound como porta do suporte | Médio | P | OPE | Dossiê |
| O-30 | Taxa de atendimento por carteira | Médio | P | COM | Benchmark |
| O-32 | Cadência ideal de tentativas | Médio | P | COM | Dossiê |
| O-37 | Contraexemplos | Médio | P | APR | Biblioteca 'erros comuns' |
| O-41 | Gamificação sem gaming | Médio | M | APR | Regras de XP |
| O-47 | Abertura e fechamento (P9) | Médio | M | COM | Dossiê |
| O-53 | Contato desatualizado e acesso ao responsável | Médio | P | COM | Lista de contatos a corrigir |
| O-55 | Prospecção sem histórico | Médio | P | COM | Dossiê |
| O-57 | Oportunidade perdida em R$ | Médio | P | COM | Ordenar coaching |
| O-58 | Cross-sell e janelas perdidas | Médio | M | COM | Dossiê |
| O-59 | Perfil por CNAE | Médio | P | COM | Dossiê |
| O-74 | Régua POSITIVA/INFORMATIVA/DETRATORA | Médio | P | COM | Revisar regra e nome |
| O-77 | Alertas diários | Médio | M | OPE | BI |
| O-80 | Simulador de capacidade | Médio | P | OPE | BI what-if |
| O-21 | Ligações vazias e secretária eletrônica | Baixo | P | OPE | Higiene do funil |
| O-26 | Melhor horário de ligação | Baixo | P | COM | Dossiê |

### Onda 3 — depende de lacuna ou fica para 2027 (10 itens)

| ID | Oportunidade | Impacto | Esforço | Persona | Entrega |
|---|---|---|---|---|---|
| O-82 | Fila de ligações prioritárias | Alto | G | COM | Só após baseline e O-72 |
| O-23 | Talk ratio, silêncio e interrupções | Médio | G | APR | — |
| O-31 | Motivo da falha de contato | Médio | M | OPE | — |
| O-43 | Trilha por segmento (CNAE) | Médio | M | APR | — |
| O-52 | Promessas do vendedor | Médio | M | COM | — |
| O-65 | Motivos de nova visita e objetivos | Médio | M | COM | Taxonomia de motivos |
| O-66 | Sentimento e satisfação do cliente | Médio | G | COM | — |
| O-83 | Previsão de carga | Médio | G | OPE | — |
| O-27 | Dia da semana | Baixo | P | COM | Fecha hipótese |
| O-60 | Mudança de carteira | Baixo | P | DAD | Reconciliar |


---

## 8. Pedidos de dados (para fechar as lacunas)

| # | Dado | Para quê | Quem pode dar |
|---|---|---|---|
| 1 | Duração das ligações a partir de 23/09 | Fechar a série de tempo (F-02) | Dados/TI |
| 2 | Atualização das diárias (jul–set) e das reservas | Resultado real pós-ligação (O-72) | Dados/Comercial |
| 3 | Base de treinamento (notas, presença, trilha) | Trilha e curva de aprendizado (O-40) | T&D/RH |
| 4 | Custo-hora do vendedor | Horas devolvidas em R$ (O-12) | Finanças/RH |
| 5 | Diário de tempo de 8–10 vendedores por 1 semana | Carga fora do telefone (O-11) | Gerência Operacional |
| 6 | Log de telefonia (motivo da falha, tentativas) | O-31 | Telefonia |
| 7 | Perfil da carteira (porte, segmento, clientes ativos), escala e senioridade | Metas por perfil (O-79) | Comercial |
| 8 | Agosto | Fechar a série jun–set | Aletheia |
| 9 | Significado do status Open | F-20 | CRM |

---

## 9. Reprodutibilidade

| Arquivo | O que faz |
|---|---|
| `scripts/auditoria_dados_missao.py` | Recalcula as seções 3, 6.2 e as tabelas de apoio; escreve os anexos |
| `scripts/baseline_carga_operacional.py` | Baseline do KPI de problema (usado no plano) |
| `missao_4T26/anexos/serie_diaria_set_2026.csv` | Assinatura diária do classificador (para o drift) |
| `missao_4T26/anexos/carteira_set_2026.csv` | Métricas por carteira (≥ 40 ligações classificadas; sem nome de vendedor) |
| `missao_4T26/anexos/faixa_duracao_negociacao.csv` | Tabela da seção 6.2 |
| `missao_4T26/anexos/catalogo_oportunidades.csv` | Catálogo completo (83 linhas) |

Janela de duração: 01–22/09. Horário convertido de UTC para BRT. Código de cliente normalizado para 8 dígitos.
