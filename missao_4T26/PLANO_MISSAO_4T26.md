# Missão 4T26 — Reduzir o tempo da venda interna com problemas

> **Draft v0.2 — 01/10/2026.** Plano para validar com o Gerente de Excelência Comercial.
> **O que mudou desde a v0.1:** carga operacional passa a ser **completa** (tudo o que não é negociação); metas mantidas; piloto e
> assinatura das horas com a Gerência Operacional; BI nominal organizado por carteira; "onde publicar" saiu do caminho crítico;
> a exploração dos dados ganhou um eixo próprio (ver `AUDITORIA_DADOS_E_OPORTUNIDADES.md`, 83 oportunidades) e uma trilha de
> conhecimento como projeto de destaque.
> Números de setembro vêm do CSV da consulta do Power BI (19.078 ligações, 31/08–30/09) e são reproduzíveis com
> `scripts/baseline_carga_operacional.py` e `scripts/auditoria_dados_missao.py`. Nada aqui usa prompt novo.

---

## 1. A missão em uma frase (com o pedido do chefe explícito)

**Reduzir a carga operacional sobre a força de vendas interna** — o tempo gasto com problemas, suporte, cobrança, pós-venda e dúvidas
de contrato, que hoje domina a capacidade do time — consolidando os resultados do Aletheia em visões **diária, semanal e mensal**
para gestão ativa dos indicadores e insights que **redirecionem o time para atividades comercialmente mais produtivas**.

**Definição de carga operacional (decisão de 01/10):** todo tempo de ligação que **não é negociação**. Suporte, cobrança e pós-venda são
papéis legítimos do vendedor, mas não são negociação, e é a soma deles que compete com a venda.

**Sucesso em dezembro, em uma frase:** *"A carga operacional caiu de X% para Y%, devolvemos Z horas/mês ao time, sabemos qual alavanca
moveu o ponteiro e o BI continua rodando sem depender de mim."*

---

## 2. Canvas de contratação (pronto para colar)

| Campo | Texto |
|---|---|
| **MISSÃO** | Reduzir a carga operacional sobre a força de vendas interna, consolidando o Aletheia em visões diária, semanal e mensal para gestão ativa e insights que devolvam tempo do time a atividades mais produtivas. |
| **POR QUE AGORA?** | Em set/26, ~43% do tempo de ligação do time não foi negociação (problemas, suporte, cobrança, pós-venda): só ~35% foi. Ligações com problema duram 1,9× mais e só ~10% se resolvem na própria chamada. O Aletheia já classifica as ligações; falta virar rotina de gestão antes das metas de 2027. |
| **ENTREGA ATÉ DEZEMBRO** | (1) BI único em produção, atualizado todo dia útil até 08h (D-1), em uso pela gestão; (2) baseline congelado e régua estável; (3) plano de ações priorizadas com dono e ao menos 1 piloto medido contra controle; (4) mapa de 83 oportunidades de insight com 5 dossiês entregues; (5) MVP da trilha de conhecimento do vendedor; (6) leitura final out→dez. |
| **INDICADOR** | **Norte:** % do tempo de ligação em carga operacional (baseline congelado em 09/10 → meta dez). **Apoio:** tempo de negociação, pendências geradas por dia, horas excedentes, reincidência. **Controle:** cobertura D-1 ≥ 95% e adoção semanal. |
| **LÍDER + TIME** | **Líder:** Thiago Librelon (Especialista de Excelência Comercial). **Piloto:** Thiago + Gerência Operacional, que também assina as horas devolvidas. **Apoios:** Gerente de Excelência Comercial (patrocínio e decisão), Gerente de Vendas, Gerente de Produto (problemas sistêmicos), Especialista de Treinamentos (trilha), Dados/TI e CX (pipeline). *Nomes a preencher.* |
| **MARCOS** | **09/10** baseline congelado e carteiras-piloto definidas · **30/10** BI v1 em produção · **13/11** plano de ações aprovado e gate da trilha · **16/11** pilotos no ar · **17/12** leitura final e decisão para 2027. |
| **DEPENDÊNCIAS** | Duração de ligação a partir de 23/09 (hoje a série para em 22/09) · tabelas `analise_llm`, `spin` e `categorizacao` do Aletheia (BigQuery) · `F_Carteiras_Equipe` · acesso ao llm-gate e máquina na rede Localiza · gateway/workspace do Power BI · Vendas, Produto e Operações para executar ações · 9 pedidos de dado (auditoria, seção 8). |
| **O QUE NÃO FAREMOS** | Novos prompts ou nova taxonomia · ranking punitivo de vendedores · política de cold call ou meta de ligações (é do Gerente de Vendas) · correção de sistemas (entregamos evidência ao Produto) · tempo real (o corte é D-1) · horas devolvidas em R$ sem premissa de custo-hora · afirmar tendência antes do baseline congelado. |

---

## 3. Onde estamos — o que os dados de setembro dizem

Base: ligações classificadas pelo GPT **com duração**, 01–22/09 (3.546 ligações; 63 carteiras; 15 dias úteis; 265,9 h de conversa).

### 3.1 Para onde vai o tempo do vendedor ao telefone

| Grupo | Horas | % do tempo |
|---|---:|---:|
| **Carga operacional** (problema + suporte + cobrança + pós-venda + dúvida de contrato) | 114,8 | **43,2%** |
| — com problema | 79,9 | 30,0% |
| — suporte, dúvida de contrato, cobrança e pós-venda sem problema | 34,9 | 13,1% |
| **Negociação** (nova venda, upsell, renovação, retenção, misto, sem problema) | 93,3 | **35,1%** |
| Relacionamento sem demanda (inclui onboarding) | 54,8 | 20,6% |
| Sem conteúdo | 3,0 | 1,1% |

**Triangulação com o Gemini:** a categoria *Suporte* do Aletheia ocupa **47,6%** do tempo no mesmo período. Os dois motores concordam no
**nível** (43–48%) e discordam na **tendência** (seção 3.3).

### 3.2 Achados

| Achado | Número | Por que importa |
|---|---|---|
| Problema alonga a ligação | **432 s vs 232 s (1,9×)**; mediana 313 s vs 143 s | ≈ 37 h excedentes em 15 d.u. (≈ 50–60 h/mês) |
| Quase nada se resolve na ligação | Resolvido **10,3%** · parcial 45,8% · não 43,8% | ~90% vira pendência fora do telefone (698 em 15 d.u. ≈ 47/dia) |
| Concentração em 3 códigos | **P1 acesso/sistema 36,8%** · P2 faturamento 17,2% · P13 crédito/cadastro PJ 13,5% = **67,5%** do tempo com problema | Define onde agir primeiro |
| Quem origina | Outbound = ~90% das ligações e 78% das com problema; a taxa é maior no inbound (36% vs 17%) | Sugere triagem antes de ligar (hipótese) |
| Reincidência | **18,8%** das ligações com problema são de clientes com 2+ no período | Lista acionável |
| Contas grandes sofrem mais | Quartil de maior volume: 32,4% de taxa de problema vs 16–19%; 60,7% do tempo dessas contas é carga operacional | Atendimento dedicado (diárias só até jun/26) |
| Carteiras muito diferentes | Carga de 16% a 73% entre carteiras; distrital DTIN4 com 31% vs 43–47% nos demais | Metas por perfil, não únicas |

### 3.3 Quatro alertas que mudam o plano

1. **A régua do GPT não é estável.** A taxa de ligações com problema foi de **13,6% (02–14/09) para 27,4% (15–22/09)**; a carga operacional medida pelo GPT
   sobe de 37% para 55% ao longo do mês enquanto o Gemini cai de 50% para 43%. Provável mudança de versão do classificador (commits de 24–25/09).
   **Sem baseline congelado não existe "redução" mensurável.** É o entregável nº 1.
2. **Faltam dados recentes.** A duração é 100% das Completed até 22/09 e 0% depois; o GPT cobre 89,5% das Completed até 22/09 e nada em 28–30/09.
   O classificador roda manual, então o D-1 precisa de agendamento.
3. **613 conversas reais (13%) estão como Sem Sucesso/Open no CRM**, sem duração. A carga está subestimada em ~143 ligações com problema.
4. **Tempo em ligação não é carga total.** São ~17 min de conversa por vendedor/dia, dos quais ~5 min com problema e ~7 min em carga operacional.
   O argumento forte é o trabalho **fora** do telefone (os ~90% não resolvidos) e a oportunidade comercial. Por isso o plano mede **pendências geradas**
   e propõe uma amostra de diário de tempo.

---

## 4. KPIs (definição única para diário, semanal e mensal)

| # | KPI | Fórmula | Baseline provisório | Meta dez |
|---|---|---|---|---|
| **K1** | **Carga operacional** (norte) | Σ duração das ligações com problema ou tipo suporte/cobrança/pós-venda/dúvida de contrato ÷ Σ duração das ligações classificadas | **43,2%** (GPT) · 47,6% (Gemini) | A confirmar em 09/10. Mantida: **−5 p.p. geral e −10 p.p. no piloto vs controle** |
| K1a | — com problema | Σ duração com `tem_problema = SIM` ÷ Σ duração | 30,0% | Acompanhar |
| K1b | — atendimento operacional sem problema | Suporte, cobrança, pós-venda e dúvida de contrato sem problema ÷ Σ duração | 13,1% | Acompanhar |
| **K7** | **Tempo de negociação** | Σ duração em nova venda, upsell, renovação, retenção e misto sem problema ÷ Σ duração | 35,1% | A calibrar em 09/10 (hipótese: +3 a +5 p.p.) |
| K2 | Pendências geradas/dia | Ligações com problema e `p3_foi_resolvido_na_ligacao` ≠ SIM | 698 em 15 d.u. (≈ 47/dia) | −20% no piloto |
| K3 | Horas excedentes/mês | n_problema × (TMA_problema − TMA_sem_problema) | ≈ 50–60 h/mês | −30% no piloto |
| K4 | Resolução na ligação | % de ligações com problema resolvidas (SIM) | 10,3% | ≥ 20% nos códigos priorizados |
| K5 | Reincidência | % de ligações com problema de clientes com 2+ no período | 18,8% | −25% |
| K6 | Taxa de ligações com problema | com problema ÷ classificadas | 18,8% (instável) | Só acompanhar |
| C1 | Cobertura de classificação D-1 | Completed classificadas ÷ Completed | 89,5% (01–22/09); 0% em 28–30/09 | **≥ 95%** |
| C2 | Cobertura de duração D-1 | Completed com duração ÷ Completed | 100% até 22/09; 0% depois | **≥ 95%** |
| C3 | Latência | BI atualizado até 08h do dia útil seguinte | manual | **≥ 95% dos dias úteis** |
| C4 | Estabilidade da régua | Concordância em auditoria de 100 ligações · K1 GPT vs Gemini sem divergência de tendência | não medido | **≥ 90%** em `tem_problema` |
| C5 | Adoção | Leituras semanais realizadas (segunda 08h) + decisões registradas | 0 | ≥ 8 leituras · ≥ 3 decisões |

**KPIs de produtividade comercial (exploração, sem meta até o dossiê):** fechamentos por hora de conversa (≈ 1,0–1,25 hoje, ver 6.2 da auditoria) ·
retorno em 14 dias após "nova visita necessária" (**15,5%**) · clientes com 1 tentativa falha sem 2ª tentativa (**2.985**) · esforço de discagem sem conversa (**66%**).

Leitura: **diário para operar, média móvel de 7 dias para decidir, mensal para a meta.** Com ~270 ligações classificadas por dia (~50 com problema), a taxa
diária oscila ±3 p.p. só por ruído.

---

## 5. Roadmap de entregáveis (01/10 → 31/12)

Feriados considerados: 12/10, 02/11, 20/11 e 25/12. Dias úteis: out 21 · nov 19 · dez 22.

### Fase 0 — Auditoria (concluída em 01/10)

| Entregável | Resultado |
|---|---|
| **E0 Auditoria de dados e mapa de oportunidades** | 12 ativos avaliados por 4 personas, 21 achados, 83 oportunidades, 9 pedidos de dado (`AUDITORIA_DADOS_E_OPORTUNIDADES.md`) |

### Fase 1 — Régua e baseline (02–16/10)

| Data | Entregável | Critério de aceite |
|---|---|---|
| 06/10 | **E1 Dicionário de KPIs v1** | K1–K7 e C1–C5 validados pelo chefe, com a carga completa |
| 09/10 | **E2 Baseline congelado de setembro** | Setembro inteiro reprocessado com **uma** versão de prompt/modelo, versão gravada por linha; K1 pelas duas réguas (GPT e Gemini); metas calibradas. Fallback: baseline 01–22/09 |
| 09/10 | **E3 Pedidos de dado e chamados** | Os 9 pedidos da auditoria com dono e prazo; carteiras-piloto definidas (seção 6) |
| 16/10 | **E4 Pipeline D-1** | Classificador agendado, saída diária, refresh sem intervenção por 3 dias seguidos |

**Gate 16/10:** régua congelada + pipeline D-1 funcionando. Sem isso, não se publica o BI.

### Fase 2 — BI v1 e primeiros dossiês (19–30/10)

| Data | Entregável | Critério de aceite |
|---|---|---|
| 20/10 | **E5 Protótipo do BI** (Visão do dia + Qualidade do dado) | Revisado com o chefe usando dados de setembro |
| 23/10 | **D1 Dossiê: carga operacional e tempo ótimo** | Mapa de alocação do tempo, Pareto de problemas, fechamentos por hora de conversa |
| 26/10 | **Primeira leitura semanal (beta)** | Segunda 08h com Gerência Operacional e Comercial; ata com decisões |
| 30/10 | **D2 Dossiê: recontato e follow-up** | Listas de clientes sem 2ª tentativa e de retornos vencidos, com tamanho em conversas |
| 30/10 | **E6 BI v1 em produção** | 8 páginas (seção 7); 5 dias úteis seguidos de refresh até 08h; acesso por perfil |

**Gate 30/10:** BI em produção e a gestão abrindo toda segunda.

### Fase 3 — Insights → ação (03/11–04/12)

| Data | Entregável | Critério de aceite |
|---|---|---|
| 06/11 | **E7 1º fechamento mensal (outubro)** | 1 página no D+4 útil: KPIs vs baseline, top 3 variações, decisão pedida |
| 06/11 | **D3 Dossiê: Challenger e SPIN** | Escada do Challenger, elo fraco do SPIN, qualidade × resultado (jun/jul), recomendação de escala |
| 13/11 | **E8 Plano de ações priorizadas** | ≥ 3 alavancas com dono, data e ganho estimado; aprovado pelo Gerente de Excelência Comercial |
| 13/11 | **Gate da trilha** | Base de treinamento obtida e régua de qualidade recalibrada; sem isso a trilha vira só biblioteca |
| 16/11 | **E9 Pilotos no ar** (2 alavancas) | Carteiras-piloto e controle definidos; medição no mesmo BI |
| 19/11 | **D4 Dossiê: concorrência e frota própria** | Listas de oportunidades (≈ 700 clientes com frota própria, 376 com aluguel em concorrente) |
| 27/11 | **T1 Conteúdo da trilha curado** | Biblioteca com lições de T2 (dado concreto) e T5 (resolver rápido) |
| 04/12 | **E10 2º fechamento mensal (novembro)** | Mesmo formato; primeira leitura parcial dos pilotos |
| 04/12 | **D5 Dossiê: melhores práticas e carteiras desviantes** | Só após baseline congelado e ruído controlado |

**Alavancas candidatas (hipóteses a validar no plano de ações, não conclusões):**

| Alavanca | Base nos dados | Dono provável |
|---|---|---|
| L1 Acesso/sistema (P1) | 36,8% do tempo com problema; ligações de 8–9 min | Produto + Treinamento |
| L2 Encaminhar faturamento/cobrança (P2) | 17,2% do tempo; 136 de 184 ligações de cobrança têm problema | Vendas + Financeiro |
| L3 Pré-checagem de crédito/cadastro antes da proposta (P13) | 13,5% do tempo | Vendas + Crédito |
| L4 Atendimento dedicado a clientes reincidentes e contas grandes | 18,8% de reincidência; quartil de maior volume com 32,4% de taxa de problema | Operações / CS |
| L5 Triagem antes do outbound | 78% das ligações com problema nascem de ligação ativa | Vendas |
| L6 Trilha "Resolver rápido" (T5) | 10,3% resolvidos na ligação; TMA 432 s | Treinamento |

### Fase 4 — Prova e fechamento (07–18/12; 21–31/12 só buffer)

| Data | Entregável | Critério de aceite |
|---|---|---|
| 07/12 | **T2 Trilha MVP no ar** (2 trilhas, 10 lições, regra de XP) | Carteiras-piloto usando; plano de medição ativo |
| 11/12 | **E11 Leitura final dos pilotos** | Piloto vs controle com a mesma régua; K1 e K3 com intervalo de variação; o que funcionou e o que não |
| 17/12 | **E12 Apresentação final e decisão 2027** | "De X% para Y%, Z h/mês devolvidas"; recomendação de escalar, ajustar ou parar |
| 18/12 | **E13 Runbook e handover** | Quem opera, como reprocessar, checklist de falha, versão da régua; BI roda 5 dias sem intervenção |
| 21–31/12 | Buffer | Só operação; dezembro fecha em janeiro |

### Visão semanal

| Semana | 05/10 | 12/10 | 19/10 | 26/10 | 02/11 | 09/11 | 16/11 | 23/11 | 30/11 | 07/12 | 14/12 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Régua e baseline | E1 E2 E3 | E4 | | | | | | | | | |
| BI | | | E5 | E6 | | | | | | | |
| Dossiês | | | D1 | D2 | D3 | | D4 | | D5 | | |
| Ação e pilotos | | | | | E7 | E8 | E9 → | → | E10 → | E11 | E12 E13 |
| Trilha | | | | | | Gate | | T1 | | T2 | |

---

## 6. Piloto e controle (a validar com a Gerência Operacional)

**Quem conduz:** Thiago + Gerência Operacional. **Quem assina as horas devolvidas:** Gerência Operacional.

**Critério de seleção sugerido:** carteiras com maior carga operacional (K1) e pelo menos 50 ligações classificadas em 01–22/09, pareadas por
posição no ranking e sorteadas entre piloto e controle (para que os dois grupos partam do mesmo nível). Base: `anexos/carteira_set_2026.csv`.

| Par | Piloto | Controle |
|---:|---|---|
| 1 | PSI10A (K1 60,7%) | RSI02A (72,5%) |
| 2 | RJI01A (58,8%) | PSI07A (59,5%) |
| 3 | NSI03A (55,8%) | KPI05A (53,3%) |
| 4 | MLI03A (52,7%) | S2I06A (52,1%) |
| 5 | S1I03A (50,5%) | REI01A (51,2%) |
| 6 | RJI05A (49,7%) | PSI11A (47,5%) |

Médias de partida: piloto 54,7% e controle 56,0% de carga operacional; taxa de problema 26,8% e 23,1%. Antes de fechar: conferir o perfil dos
clientes de cada carteira, confirmar que não há férias ou trocas de carteira em novembro–dezembro e refazer o sorteio com o baseline congelado (E2).

---

## 7. BI diário — especificação mínima

Cada página responde a **uma decisão** (princípio do `Prompt_plano`: contexto → insight → evidência → recomendação → ação).
**Hierarquia:** Divisional (DVINT) → Distrital (DTIN1–5) → **Carteira** (67; o vendedor aparece como atributo nominal da carteira, que é 1:1 com a matrícula).

| Página | Decisão que habilita | Granularidade | Visuais-chave |
|---|---|---|---|
| 1. Visão do dia | O que mudou ontem e exige ação hoje? | Dia (D-1), com média móvel 7d | K1, K7, K2, alertas de desvio, cobertura do dado |
| 2. Semana | A tendência piora ou melhora? | Semana (seg–sex) vs semana anterior | K1–K7 com variação semanal; ata da leitura de segunda |
| 3. Mês | Estamos no caminho da meta? | Mês e acumulado vs baseline | K1 vs meta, horas excedentes, fechamento |
| 4. Problemas | Qual problema atacar primeiro? | Dia/semana/mês | Pareto de **tempo** por código, resolução, reincidência, inbound × outbound; drill até o trecho literal |
| 5. Carteira e distrital | Onde a carga se concentra? | Semana/mês | Distribuição por carteira vs mediana e por perfil; filtros `DISTRITAL` e `CARTEIRA` |
| 6. Tempo e ritmo | Quando insistir, quando encerrar? | Semana/mês | Faixas de duração × fechamentos por hora, TMA por tipo, funil de contato, recontato e follow-up vencido |
| 7. Competências | Que habilidade falta nesta carteira? | Mês | Radar SPIN e Challenger, escada dado → conexão → reação, trechos para coaching |
| 8. Qualidade do dado | Posso confiar no número de hoje? | Dia | Coberturas, atraso, **versão do prompt**, duas réguas lado a lado (GPT × Gemini) |

Regras: calendário único (dia, semana ISO com início na segunda, mês); medidas DAX iguais nas três granularidades; horário convertido de UTC para BRT;
código de cliente com 8 dígitos; eixo Positiva/Informativa/Detratora do Power Query como filtro cruzado; trechos com nome de cliente só para perfil restrito.
**Uso:** nominal por carteira, mas comparado com a mediana e com carteiras de perfil parecido; o BI é para remover obstáculos, não para punir.

**Ajustes na consulta atual (a validar):** parametrizar o corte `>= '2026-09-01'`; trazer a versão da régua para cada linha; subtrair 3h do horário; normalizar
`codigo_cliente`; retirar campos saturados (`nota_demanda_atendimento`, `oportunidades_boleano`); acompanhar as 657 Completed sem `analise_llm`.

---

## 8. Riscos

| Risco | Prob. | Impacto | Mitigação |
|---|---|---|---|
| Régua instável invalida a comparação | Alta | Alto | E2 congela; versão visível no BI; auditoria amostral (C4); duas réguas lado a lado |
| Duração indisponível ou atrasada | Alta | Alto | Pedido em 09/10; fallback de baseline 01–22/09; C2 no BI |
| Tempo em ligação subestima a carga real | Alta | Médio | Medir pendências (K2); diário de tempo em amostra em novembro |
| Escopo cresce com 83 oportunidades | Alta | Alto | Compromisso só com a missão; o resto é exploração com data e gate (auditoria, seção 7) |
| Ações dependem de Vendas, Produto e Operações | Média | Alto | Sucesso em 3 camadas (seção 9); plano de ações com dono aprovado pelo gestor |
| Pipeline manual falha no D-1 | Média | Médio | Agendamento, retomada automática (`_andamento.jsonl`), alerta de falha, runbook |
| Ruído diário gera falsos alarmes | Média | Médio | Média móvel 7d; limites por desvio |
| Carteira = vendedor: BI vira vigilância | Média | Alto | Comparar com mediana e perfil; ata sem ranking; uso para remover obstáculos (conforme `ROAD_MAP` e `PERSONAS_ALETHEIA`) |
| Trilha mal medida incentiva gaming | Média | Médio | Pontuar qualidade (dado + conexão + reação), nunca SIM/NÃO; auditoria de 10% dos acertos |
| LGPD (trechos com nomes de clientes) | Média | Alto | Perfil restrito para trechos; máscara; sem trechos no resumo executivo |
| Custo do GPT diário | Baixa | Médio | Acompanhar `consumo_diario.csv`; teto mensal combinado com CX |

---

## 9. O que é sucesso em dezembro

**Camada 1 — depende de você (mínimo para dizer "entreguei"):**

- [ ] BI em produção, refresh até 08h em ≥ 95% dos dias úteis de nov–dez.
- [ ] Cobertura D-1 de classificação e duração ≥ 95%.
- [ ] Régua congelada e documentada; auditoria de 100 ligações com ≥ 90% de concordância em `tem_problema`.
- [ ] Três granularidades em uso: ≥ 8 leituras semanais com ata; fechamentos de outubro e novembro publicados no D+4.
- [ ] Plano de ações aprovado: ≥ 3 alavancas com dono e data; ≥ 1 piloto com grupo de controle.
- [ ] 5 dossiês entregues e a trilha MVP no ar para as carteiras-piloto.

**Camada 2 — resultado que você influencia:**

- [ ] K1 reduzido vs baseline congelado (−5 p.p. geral e −10 p.p. no piloto vs controle).
- [ ] Horas devolvidas ao time estimadas e assinadas pela Gerência Operacional.

**Camada 3 — aprendizado (vale como indicador no canvas):**

- [ ] Sabemos qual alavanca move o ponteiro, quanto ela vale em horas e o que não funcionou — mesmo se a meta numérica não for atingida.

---

## 10. Decisões

**Tomadas em 01/10:** carga operacional completa · metas mantidas (−5 p.p. geral, −10 p.p. piloto) · exploração ampla dos dados em paralelo ·
piloto conduzido por Thiago + Gerência Operacional, que assina as horas · BI nominal organizado por carteira · "onde publicar a classificação" fora do caminho crítico.

**Em aberto (fechar até 09/10):**

1. Lista final de carteiras do piloto e do controle (seção 6) com a Gerência Operacional.
2. Meta de K7 (tempo de negociação) e confirmação de K1 após o baseline.
3. Dono e prazo de cada um dos 9 pedidos de dado.
4. Gate da trilha (13/11): quem fornece a base de treinamento.

---

## 11. Próximos 5 dias úteis

| Dia | Ação |
|---|---|
| 02/10 | Validar este plano e a auditoria com o chefe; confirmar a definição de carga completa |
| 02/10 | Abrir o chamado de duração (≥ 23/09) e levantar quem agenda o classificador |
| 05/10 | Rodar o classificador em todo setembro com uma versão congelada (E2) |
| 06/10 | Fechar o dicionário de KPIs (E1) |
| 09/10 | Baseline oficial + metas calibradas + carteiras-piloto + pauta da primeira leitura semanal |
