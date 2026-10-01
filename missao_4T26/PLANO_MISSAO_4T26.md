# Missão 4T26 — Reduzir o tempo da venda interna com problemas

> **Draft v0.1 — 01/10/2026.** Plano para validar com o Gerente de Excelência Comercial.
> Números de setembro vêm de `Consulta Power Bi - Cópia.csv` (19.078 ligações, 31/08–30/09) e são reproduzíveis com
> `scripts/baseline_carga_operacional.py`. Nada aqui usa prompt novo: a régua é a do classificador atual (modo foco / C12).

---

## 1. A missão em uma frase (com o pedido do chefe explícito)

**Reduzir a carga operacional sobre a força de vendas interna** — o tempo que o vendedor gasta em ligações com
problema — consolidando os resultados do Aletheia em visões **diária, semanal e mensal**, para gestão ativa dos
indicadores e insights que **redirecionem o time para atividades comercialmente mais produtivas**.

**Sucesso em dezembro, em uma frase:** *"A carga operacional caiu de X% para Y%, devolvemos Z horas/mês ao time,
sabemos qual alavanca moveu o ponteiro e o BI continua rodando sem depender de mim."*

---

## 2. Canvas de contratação (pronto para colar)

| Campo | Texto |
|---|---|
| **MISSÃO** | Reduzir a carga operacional sobre a força de vendas interna, consolidando o Aletheia em visões diária, semanal e mensal para gestão ativa e insights que devolvam tempo do time a atividades mais produtivas. |
| **POR QUE AGORA?** | Em set/26, ~30% do tempo de ligação do time foi consumido por ligações com problema; elas duram 1,9× mais e só ~10% são resolvidas na própria chamada. O Aletheia já classifica as ligações, falta virar rotina de gestão antes das metas de 2027. |
| **ENTREGA ATÉ DEZEMBRO** | (1) BI único em produção, atualizado todo dia útil até 08h (D-1), em uso pela gestão; (2) baseline congelado e régua estável; (3) plano de ações priorizadas com dono, com ao menos 1 piloto medido; (4) leitura final out→dez da carga operacional. |
| **INDICADOR** | **Norte:** % do tempo de ligação em ligações com problema (baseline congelado em 09/10 → meta dez). **Apoio:** pendências geradas por dia, horas excedentes/mês, reincidência. **Controle:** cobertura D-1 ≥ 95% e adoção semanal. |
| **LÍDER + TIME** | **Líder:** Thiago Librelon (Especialista de Excelência Comercial). **Apoios:** Gerente de Excelência Comercial (patrocínio e decisão), Gerente de Vendas (dono das ações com o time), Gerente de Produto (problemas sistêmicos), Especialista de Treinamentos (playbooks), Dados/TI e CX (pipeline e gateway). *Nomes a preencher.* |
| **MARCOS** | **09/10** baseline congelado · **30/10** BI v1 em produção · **13/11** plano de ações aprovado · **16/11** pilotos no ar · **17/12** leitura final e decisão para 2027. |
| **DEPENDÊNCIAS** | Tabela `Tempo_de_ligação` atualizada (hoje para em 22/09) · tabelas `analise_llm`, `spin` e `categorizacao` do Aletheia (BigQuery) · `F_Carteiras_Equipe` · acesso ao llm-gate e máquina na rede Localiza · gateway/workspace do Power BI · Vendas e Produto para executar ações. |
| **O QUE NÃO FAREMOS** | Novos prompts ou nova taxonomia · ranking punitivo de vendedores · política de cold call ou meta de ligações (é do Gerente de Vendas) · correção de sistemas (entregamos evidência ao Produto) · tempo real (o corte é D-1) · medir o trabalho fora da ligação (só estimar por amostra). |

---

## 3. Onde estamos — o que os dados de setembro dizem

Base: ligações classificadas pelo GPT **com duração**, 01–22/09 (3.546 ligações; ~63 vendedores; 15 dias úteis).

| Achado | Número | Por que importa |
|---|---|---|
| Carga por problema | **80 h de 266 h = 30,0%** do tempo de ligação (18,8% das ligações) | É o ponteiro da missão. |
| Problema alonga a ligação | **432 s vs 232 s (1,9×)**; mediana 313 s vs 143 s | ≈ 37 h excedentes em 15 d.u. (≈ 50–60 h/mês). |
| Quase nada se resolve na ligação | Resolvido **10,3%** · parcial 45,8% · não 43,8% | ~90% vira pendência: trabalho que o vendedor carrega depois, fora do telefone. |
| Concentração em 3 códigos | **P1 acesso/sistema 36,8%** · P2 faturamento 17,2% · P13 crédito/cadastro PJ 13,5% = **67,5%** do tempo com problema | Define onde agir primeiro. |
| Quem origina | Outbound = ~90% das ligações e 78% das ligações com problema; a taxa é maior no inbound (36% vs 17%) | A maior parte do volume nasce de ligação ativa do vendedor: sugere triagem *antes* de ligar (hipótese, não causa provada). |
| Reincidência | **18,8%** das ligações com problema são de clientes com 2+ no período | Lista acionável para atendimento dedicado. |
| Visão ampla de carga | **43,2%** do tempo se somarmos suporte operacional, cobrança, pós-venda e dúvida de contrato | Alternativa de definição (ver decisão 1). |

### Três alertas que mudam o plano

1. **A régua não está estável.** A taxa de ligações com problema foi de **13,6% (02–14/09) para 27,4% (15–22/09)** e a
   carga de tempo de **20% para 47%**. O salto coincide com o período de ajustes do prompt (commits de 24–25/09), então
   a hipótese é mudança de versão do classificador, não mudança do negócio. **Sem baseline congelado não existe
   "redução" mensurável.** É o entregável nº 1.
2. **Faltam dados recentes.** A duração (`Tempo_de_ligação`) é 0% de 23/09 em diante, e a classificação GPT é 0% de
   28 a 30/09 e parcial em 24/09 (94 de 294). Hoje o classificador roda manual (abre janelas), então o D-1 precisa de
   agendamento.
3. **Tempo em ligação não é carga total.** A duração medida dá ~17 min de conversa por vendedor/dia, dos quais ~5 min
   com problema. O ganho visível no telefone é pequeno em horas absolutas. O argumento forte é o trabalho **fora** da
   ligação (os ~90% não resolvidos) e a oportunidade comercial. Por isso o plano mede **pendências geradas** além do
   tempo, e propõe uma amostra curta de diário de tempo para calibrar.

---

## 4. KPIs (definição única para diário, semanal e mensal)

| # | KPI | Fórmula | Baseline provisório | Meta dez |
|---|---|---|---|---|
| **K1** | **Carga por problema** (norte) | Σ duração das ligações com `tem_problema = SIM` ÷ Σ duração das ligações classificadas | 30,0% (instável: 20% → 47%) | A calibrar em 09/10. Proposta: **−5 p.p. geral e −10 p.p. no piloto vs controle** |
| K2 | Pendências geradas/dia | Ligações com problema e `p3_foi_resolvido_na_ligacao` ≠ SIM | 698 em 15 d.u. (≈ 47/dia) | −20% no piloto |
| K3 | Horas excedentes/mês | n_problema × (TMA_problema − TMA_sem_problema) | ≈ 50–60 h/mês | −30% no piloto |
| K4 | Resolução na ligação | % de ligações com problema resolvidas (SIM) | 10,3% | ≥ 20% nos códigos priorizados |
| K5 | Reincidência | % de ligações com problema de clientes com 2+ no mês | 18,8% | Lista ativa tratada; reincidência −25% |
| K6 | Taxa de ligações com problema | ligações com problema ÷ ligações classificadas | 18,8% (instável) | Só acompanhar |
| C1 | Cobertura de classificação D-1 | Completed classificadas ÷ Completed | 89,5% (01–22/09); 0% em 28–30/09 | **≥ 95%** |
| C2 | Cobertura de duração D-1 | classificadas com duração ÷ classificadas | 87% até 22/09, 0% depois | **≥ 95%** |
| C3 | Latência | BI atualizado até 08h do dia útil seguinte | manual | **≥ 95% dos dias úteis** |
| C4 | Estabilidade da régua | Concordância em auditoria de 100 ligações · K6 sem salto sem mudança de versão | não medido | **≥ 90%** em `tem_problema` |
| C5 | Adoção | Leituras semanais realizadas (segunda 08h) + decisões registradas | 0 | ≥ 8 leituras · ≥ 3 decisões |

Leitura: **diário para operar, média móvel de 7 dias para decidir, mensal para a meta.** Com ~270 ligações
classificadas por dia (~50 com problema), a taxa diária oscila ±3 p.p. só por ruído (11% a 18% em 02–14/09).

---

## 5. Roadmap de entregáveis (01/10 → 31/12)

Feriados considerados: 12/10, 02/11, 20/11 e 25/12. Dias úteis: out 21 · nov 19 · dez 22.

### Fase 1 — Régua e baseline (01–16/10)

| Data | Entregável | Critério de aceite |
|---|---|---|
| 06/10 | **E1 Dicionário de KPIs v1** | Definições de K1–K6 e C1–C5 validadas pelo chefe (decisão 1 fechada). |
| 09/10 | **E2 Baseline congelado de setembro** | Setembro inteiro reprocessado com **uma** versão de prompt/modelo; versão registrada; meta numérica calibrada. Fallback: baseline 01–22/09. |
| 09/10 | **E3 Chamados de dependência abertos** | Duração ≥ 23/09, agendamento do classificador e local de publicação com dono e prazo. |
| 16/10 | **E4 Pipeline D-1** | Classificador agendado, saída diária em pasta/tabela, refresh sem intervenção por 3 dias seguidos. |

**Gate 16/10:** régua congelada + pipeline D-1 funcionando. Sem isso, não se publica o BI.

### Fase 2 — BI v1 (19–30/10)

| Data | Entregável | Critério de aceite |
|---|---|---|
| 20/10 | **E5 Protótipo do BI** (Diário + Qualidade do dado) | Revisado com o chefe usando dados de setembro. |
| 23/10 | **E6 Dossiê de insights #0 (setembro)** | Pareto de tempo por problema, reincidência e origem (inbound/outbound), com 1 página. Vitória rápida e argumento para Vendas e Produto. |
| 26/10 | **Primeira leitura semanal (beta)** | Segunda 08h com Gerente de Vendas; ata com decisões. |
| 30/10 | **E7 BI v1 em produção** | 6 páginas (seção 6) no ar; 5 dias úteis seguidos de refresh até 08h; acesso restrito por perfil. |

**Gate 30/10:** BI em produção e a gestão abrindo toda segunda.

### Fase 3 — Insights → ação (03/11–04/12)

| Data | Entregável | Critério de aceite |
|---|---|---|
| 06/11 | **E8 1º fechamento mensal (outubro)** | Relatório de 1 página no D+4 útil: K1–K6 vs baseline, top 3 variações, decisão pedida. |
| 06/11 | **E9 Dossiê de insights #1 (outubro)** | Alavancas com tamanho em horas e pendências (ver abaixo). |
| 13/11 | **E10 Plano de ações priorizadas** | ≥ 3 alavancas com dono, data e ganho estimado; aprovado pelo Gerente de Excelência Comercial. |
| 16/11 | **E11 Pilotos no ar** (2 alavancas) | Grupo piloto e grupo controle definidos (por distrital/carteira); medição no mesmo BI. |
| 04/12 | **E12 2º fechamento mensal (novembro)** | Mesmo formato; primeira leitura parcial dos pilotos. |

**Alavancas candidatas (hipóteses a validar no dossiê #1, não conclusões):**

| Alavanca | Base nos dados | Dono provável |
|---|---|---|
| L1 Acesso/sistema (P1) | 36,8% do tempo com problema; ligações de 8–9 min | Produto + Treinamento |
| L2 Encaminhar faturamento/cobrança (P2) | 17,2% do tempo; 136 de 184 ligações de cobrança têm problema | Vendas + Financeiro |
| L3 Pré-checagem de crédito/cadastro antes da proposta (P13) | 13,5% do tempo | Vendas + Crédito |
| L4 Atendimento dedicado a clientes reincidentes | 18,8% das ligações com problema | Vendas / CS |
| L5 Triagem antes do outbound | 78% das ligações com problema nascem de ligação ativa | Vendas |

### Fase 4 — Prova e fechamento (07–18/12; 21–31/12 só buffer)

| Data | Entregável | Critério de aceite |
|---|---|---|
| 11/12 | **E13 Leitura final dos pilotos** | Piloto vs controle com a mesma régua; K1 e K3 com intervalo de variação; o que funcionou e o que não. |
| 17/12 | **E14 Apresentação final e decisão 2027** | "De X% para Y%, Z h/mês devolvidas"; recomendação de escalar, ajustar ou parar. |
| 18/12 | **E15 Runbook e handover** | Quem opera, como reprocessar, checklist de falha, versão da régua; BI roda 5 dias sem intervenção. |
| 21–31/12 | Buffer | Só operação; dezembro fecha em janeiro. |

### Visão semanal

| Semana | 05/10 | 12/10 | 19/10 | 26/10 | 02/11 | 09/11 | 16/11 | 23/11 | 30/11 | 07/12 | 14/12 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Régua e baseline | E1 E2 E3 | E4 | | | | | | | | | |
| BI | | | E5 | E7 | | | | | | | |
| Insights | | | E6 | | E8 E9 | E10 | | | E12 | | |
| Pilotos | | | | | | | E11 → | → | → | E13 | E14 E15 |

---

## 6. BI diário — especificação mínima

Cada página responde a **uma decisão** (princípio do `Prompt_plano`: contexto → insight → evidência → recomendação → ação).

| Página | Decisão que habilita | Granularidade | Visuais-chave |
|---|---|---|---|
| 1. Visão do dia | O que mudou ontem e exige ação hoje? | Dia (D-1), com média móvel 7d | K1, K2, K6, alertas de desvio, cobertura do dado |
| 2. Semana | A tendência piora ou melhora? | Semana (seg–sex) vs semana anterior | K1–K5 com variação semanal; ata da leitura de segunda |
| 3. Mês | Estamos no caminho da meta? | Mês e acumulado vs baseline | K1 vs meta, horas excedentes, fechamento |
| 4. Problemas | Qual problema atacar primeiro? | Dia/semana/mês | Pareto de **tempo** por código, resolução, reincidência, inbound vs outbound; drill até o trecho literal (`p3_trechos`) |
| 5. Carteira e distrital | Onde a carga se concentra? | Semana/mês | Distribuição vs mediana (não ranking nominal); filtros `DISTRITAL` e `CARTEIRA` |
| 6. Qualidade do dado | Posso confiar no número de hoje? | Dia | Cobertura de classificação e duração, atraso, **versão do prompt**, ligações sem classificação |

Regras: calendário único (dia, semana ISO com início na segunda, mês); medidas DAX iguais nas três granularidades;
eixo de produtividade Positiva/Informativa/Detratora (a régua do M atual) como filtro cruzado; trechos com nome de
cliente só para perfil restrito.

**Ajustes na consulta atual (a validar):** parametrizar o corte `>= '2026-09-01'` do SQL; trazer a versão da régua
para cada linha; confirmar a relação 1:1 entre `id_transcricao` e `segment_id` (hoje não há duplicidade no CSV);
monitorar as 657 ligações Completed sem `analise_llm` (~10%).

---

## 7. Riscos

| Risco | Prob. | Impacto | Mitigação |
|---|---|---|---|
| Régua instável invalida a comparação | Alta | Alto | E2 congela; versão do prompt visível no BI; auditoria amostral (C4). |
| Duração indisponível ou atrasada | Alta | Alto | Chamado em 09/10; fallback de baseline 01–22/09; C2 no BI. |
| Tempo em ligação subestima a carga real | Alta | Médio | Medir pendências (K2); amostra de diário de tempo (8–10 vendedores, 1 semana) em nov. |
| Ações dependem de Vendas e Produto | Média | Alto | Sucesso em 3 camadas (seção 8); plano de ações com dono aprovado pelo gestor. |
| Pipeline manual falha no D-1 | Média | Médio | Agendamento, retomada automática (`_andamento.jsonl`), alerta de falha, runbook. |
| Ruído diário gera falsos alarmes | Média | Médio | Média móvel 7d; limites por desvio, não por variação de 1 dia. |
| Vendedor vê o BI como vigilância | Média | Alto | Visão agregada por padrão; usar para remover obstáculos, não para punir (conforme `ROAD_MAP` e `PERSONAS_ALETHEIA`). |
| LGPD (trechos com nomes de clientes) | Média | Alto | Perfil restrito para trechos; sem trechos no resumo executivo. |
| Custo do GPT diário | Baixa | Médio | Acompanhar `consumo_diario.csv`; teto mensal combinado com CX. |

---

## 8. O que é sucesso em dezembro

**Camada 1 — depende de você (mínimo para dizer "entreguei"):**

- [ ] BI em produção, refresh até 08h em ≥ 95% dos dias úteis de nov–dez.
- [ ] Cobertura D-1 de classificação e duração ≥ 95%.
- [ ] Régua congelada e documentada; auditoria de 100 ligações com ≥ 90% de concordância em `tem_problema`.
- [ ] Três granularidades em uso: ≥ 8 leituras semanais com ata; fechamentos de outubro e novembro publicados no D+4.
- [ ] Plano de ações aprovado: ≥ 3 alavancas com dono e data; ≥ 1 piloto com grupo de controle.

**Camada 2 — resultado que você influencia:**

- [ ] K1 reduzido vs baseline congelado (proposta: −5 p.p. geral e −10 p.p. no piloto vs controle).
- [ ] Horas devolvidas ao time estimadas e assinadas pelo Gerente de Vendas.

**Camada 3 — aprendizado (vale como indicador no canvas):**

- [ ] Sabemos qual alavanca move o ponteiro, quanto ela vale em horas e o que não funcionou — mesmo se a meta numérica não for atingida.

---

## 9. Decisões em aberto (fechar até 06/10)

1. **Definição de carga operacional.** A) só ligações com problema (K1, 30%) ou B) ampliada com suporte, cobrança,
   pós-venda e dúvida de contrato (43%)? *Recomendo A como norte e B como visão secundária.*
2. **Meta numérica.** Confirmar o −5 p.p. / −10 p.p. só depois do baseline congelado (E2).
3. **Onde publicar a classificação diária.** Pasta no SharePoint lida pelo Power Query (menos dependência) ou tabela no
   BigQuery (mais robusto, exige Dados). *Recomendo pasta em outubro e avaliar BigQuery em novembro.*
4. **Quem é o grupo piloto** (distritais ou carteiras) e quem assina as horas devolvidas.
5. **Nome do vendedor no BI.** Anônimo por padrão, nominal só para gestor direto?

---

## 10. Próximos 5 dias úteis

| Dia | Ação |
|---|---|
| 02/10 | Validar este plano e a decisão 1 com o chefe. |
| 02/10 | Abrir chamado `Tempo_de_ligação` (≥ 23/09) e levantar quem agenda o classificador. |
| 05/10 | Rodar o classificador em todo setembro com uma versão congelada (E2). |
| 06/10 | Fechar o dicionário de KPIs (E1). |
| 09/10 | Baseline oficial + meta calibrada + pauta da primeira leitura semanal. |
