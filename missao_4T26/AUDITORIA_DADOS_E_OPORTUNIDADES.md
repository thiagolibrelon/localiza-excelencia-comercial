# Auditoria de dados e mapa de oportunidades — Missão 4T26

> **Draft v0.2 — 01/10/2026 (refeito).** Complementa `PLANO_MISSAO_4T26.md`.
> **Fontes: somente o CSV da consulta do Power BI (19.078 linhas × 88 colunas) e o código M que o gera.** Nada do repositório entra
> nos números: sem junho, julho, diárias, reservas, exemplos ou documentos anteriores. **Única exceção: a legenda dos códigos P1–P15 e CH1–CH7, que vem do repositório.** Sem prompts novos.
> As oportunidades têm plano próprio em `PLANO_OPORTUNIDADES.md`. Números reproduzíveis com `scripts/auditoria_dados_missao.py`; dicionário das 88 colunas em `anexos/dicionario_dados_setembro.csv`;
> catálogo completo em `anexos/catalogo_oportunidades.csv`.

---

## 0. Em dois minutos

1. **Só temos setembro** (31/08–30/09) e a duração de ligação só existe até 22/09. Não há tendência entre meses e não há resultado
   real depois da ligação; tudo o que segue é leitura de um mês.
2. **As 88 colunas foram auditadas uma a uma:** 46 podem ser usadas, 34 com ressalva e 8 não devem ser usadas. Dos 9 blocos de dado, 4 têm selo verde e 5 amarelo (seção 2).
3. **Carga operacional (tudo o que não é negociação): 43,2% do tempo de ligação pelo GPT e 47,6% pelo Gemini.** O nível bate; a tendência não: o GPT sobe de 37% para 55% ao longo do mês e o Gemini cai de 50% para 43%. O classificador GPT mudou de versão no meio de setembro (seção 5).
4. **O código M tem três falhas que alteram números:** 657 ligações concluídas sem análise viram DETRATORA; 934 ligações de 31/08 recebem a chave do mês 08; e um ramo da regra nunca é executado (seção 3).
5. **Não existe uma "duração ótima" única.** Ligações de negociação com 5 min ou mais são 47% das ligações, 76% dos fechamentos e 77% do tempo: a eficiência por hora fica plana (≈ 1,0–1,2) a partir de 5 min e é menor entre 2 e 5 min (seção 8.2).
6. **Challenger SIM/NÃO não serve como meta.** Com duração controlada, o fechamento é igual com e sem Challenger. A escada *dado concreto → conexão → reação* (14,0% → 20,1% → 22,1%) e o elo fraco do SPIN (Implicação, nota 1 em 50,7%) apontam o que treinar (seção 8.1).
7. **Contato e cadência:** 2.985 clientes ficaram com uma única tentativa falha (≈ 900 conversas/mês com uma 2ª tentativa); só **27,1%** dos retornos devidos tiveram nova tentativa no prazo; a sexta-feira rende 29% menos tentativas por vendedor.
8. **1% dos clientes concentra 20,1% do tempo de ligação** (≈ 120 clientes).
9. **Mapeei 89 oportunidades em 8 eixos** (seção 7): 65 com dado pronto, 16 parciais e 8 que dependem de dado que não temos.
10. **As lacunas que mais pesam:** resultado real, base de treinamento, meses anteriores e duração a partir de 23/09 (seção 10).

---

## 1. Escopo e convenções

| Item | Regra adotada |
|---|---|
| Janela | 31/08–30/09 (22 dias com ligação). Duração e análises de tempo: 01–22/09 (15 dias úteis; 07/09 é feriado) |
| Horário | O CSV traz `data_visita_ev` em UTC; subtraí 3 h para BRT |
| Booleanos | `VERDADEIRO`/`FALSO` (a coluna `venda` usa `True`/`False`) |
| Cliente | `codigo_cliente` normalizado para 8 dígitos |
| Carga operacional | Ligação com problema **ou** de tipo suporte, cobrança, pós-venda ou dúvida de contrato |
| Negociação | Nova venda, upsell, renovação, retenção e misto, sem problema |
| Fechamento | "Fechou" (GPT) **ou** "venda" (Gemini); as duas fontes concordam pouco (seção 4) |

**Legenda dos códigos** (do repositório: `scripts/classificar_ligacoes_diario.py` e `prompts/prompts_nivel1_por_ligacao.md`; o CSV traz só o código):

| Problema (`p3_*`) | Significado | Problema (`p3_*`) | Significado |
|---|---|---|---|
| P1 | Acesso/sistema (portal fora do ar, senha, biometria) | P9 | Sinistro (acidente, avaria, franquia de dano) |
| P2 | Faturamento/cobrança (boleto, fatura, valor incorreto) | P10 | Reserva/sistema (reserva com erro no sistema) |
| P3 | Multa/infração | P11 | Outro (com descrição) |
| P4 | Manutenção/substituto | P12 | Manipulação de pesquisa/NPS |
| P5 | Condutor/cadastro (erro ou bloqueio) | P13 | Crédito/cadastro PJ (limite, cadastro pendente) |
| P6 | Km excedente | P14 | Preço/competitividade |
| P7 | Disponibilidade (sem carro na data ou loja) | P15 | Tag de pedágio (falha) |
| P8 | Franquia/agência | | |

| Challenger (`p5_codigos_challenger`) | Significado |
|---|---|
| CH1 | Custo oculto revelado |
| CH2 | ROI calculado |
| CH3 | Urgência por regra real |
| CH4 | Concorrente ou alternativa superada com dado |
| CH5 | Dor revelada → produto conectado |
| CH6 | Antecipação de problema |
| CH7 | Descoberta de necessidade não declarada |

---

## 2. Mapa dos dados: 9 blocos, 88 colunas

**Como as fontes se encadeiam no código M:** tabela de visitas internas (CRM) → junção com `meta` (`call_object` → `segment_id`) → `analise_llm`, `spinselling_llm` e `categorizacao_llm`
(Aletheia/Gemini) → `F_Carteiras_Equipe` (matrícula → divisional, distrital, carteira) → filtro DVINT → `Tempo_de_ligação` (duração) → regra POSITIVA/INFORMATIVA/DETRATORA →
`Ligações Classificadas` (GPT) → filtro `status ≠ Not Started`.

| Bloco | Colunas | Usar | Ressalva | Não usar | Base aplicável | Selo | Observação |
|---|---:|---:|---:|---:|---|---|---|
| A. Identificadores e chaves | 8 | 5 | 1 | 2 | 19.078 linhas | **Amarelo** | Código de cliente perde o zero (19,3%) e é nulo em 7,8%; 2 colunas duplicadas |
| B. CRM e telefonia | 10 | 3 | 6 | 1 | 19.078 linhas; duração só em Completed | **Verde** | Horário em UTC; duração até 22/09; `Chave` falha em 31/08 |
| C. Regra do Power Query | 1 | 0 | 1 | 0 | 19.078 linhas | **Amarelo** | 657 Completed sem análise viram DETRATORA |
| D. Aletheia (Gemini): análise | 26 | 12 | 11 | 3 | 5.839 (30,6%) | **Verde** | Estável dia a dia; vários campos saturados ou com valor-sentinela |
| E. Aletheia (Gemini): SPIN | 10 | 8 | 2 | 0 | 5.840 (30,6%) | **Verde** | Notas estáveis; narrativas com nomes de pessoas |
| F. Aletheia (Gemini): categorização | 5 | 4 | 1 | 0 | 5.839 (30,6%) | **Verde** | `Sem Classificação` = ligação sem análise (69%) |
| G. GPT: venda | 9 | 5 | 2 | 2 | 6.232 (32,7%) | **Amarelo** | Versão do classificador muda no mês |
| H. GPT: problemas | 8 | 3 | 5 | 0 | 6.232 (32,7%) | **Amarelo** | Idem; 83% de "nenhum" |
| I. GPT: Challenger | 11 | 6 | 5 | 0 | 6.232 (32,7%) | **Amarelo** | Qualidade 83% "alta"; textos esparsos |
| **Total** | **88** | **46** | **34** | **8** | | | |

**Colunas que não devem ser usadas (8):** `codigo_cliente_analise` e `matricula_ev` (duplicam outras), `tipo_interacao` (redundante com `tipo_ligacao`), `nota_demanda_atendimento` (constante 0),
`volume_frota_propria` e `volume_aluguel_concorrencia` (95% e 99% de valor-sentinela), `p1_desfecho_original` e `p2_tipo_original` (3 e 1 valores na base inteira).
"Saturado" nem sempre é defeito: eventos raros, como `venda` (2,5% verdadeiro), são naturalmente concentrados em um valor. O defeito é a saturação de campos que deveriam discriminar
(`oportunidades_boleano` 92%, `demanda_de_atendimento_boleano` 81%, `necessidade_nova_visita_boleano` 79%).

### 2.1 Colunas por bloco

**Uso:** *Usar* = confiável para análise · *Ressalva* = usar com o cuidado indicado · *Não usar* = duplicada, constante ou sem informação. **Preenchida** = % da base do bloco (tabela acima) com valor. Fonte: `anexos/dicionario_dados_setembro.csv`, que traz também mínimo, média, máximo e valor mais comum.

#### A. Identificadores e chaves — 8 colunas: 5 usar · 1 ressalva · 2 não usar

| Coluna | O que é | Preenchida | Valores distintos | Uso | Observação |
|---|---|---:|---:|---|---|
| `id_transcricao` | ID da ligação no CRM (chave da junção com Tempo_de_ligação) | 100% | 19.078 | Usar | — |
| `segment_id` | ID do segmento de transcrição (chave das tabelas Aletheia) | 100% | 19.078 | Usar | — |
| `cd_segmento` | Mesmo ID, vindo da tabela Ligações Classificadas | 32,7% | 6.232 | Usar | — |
| `codigo_cliente` | Código do cliente (perde zero à esquerda) | 92,2% | 12.206 | Ressalva | normalizar para 8 dígitos; 7,8% nulos |
| `codigo_cliente_analise` | Código do cliente dentro da tabela de análise | 30,6% | 5.101 | **Não usar** | duplica codigo_cliente |
| `matricula_ev_createdby` | Matrícula do vendedor que registrou | 100% | 67 | Usar | — |
| `matricula_ev` | Matrícula do vendedor na análise | 30,6% | 63 | **Não usar** | duplica matricula_ev_createdby |
| `nome_createdby` | Nome do vendedor | 100% | 67 | Usar | — |

**Notas.** (1) `cd_segmento` é o mesmo valor de `segment_id` em todas as 6.232 linhas em que aparece (só as classificadas pelo GPT); ficou em *Usar* porque é a chave da junção com `Ligações Classificadas` e sua ausência indica ligação sem classificação GPT. Pelo critério dos outros dois duplicados (que repetem uma coluna mais completa) poderia ser *Usar com ressalva*. (2) `nome_createdby` é *Usar* quanto à qualidade do dado (1:1 com a matrícula, 67 nomes); no BI o nome fica **fora** do modelo publicado (ver `bi/README_BI_v1.md`, seção 6).

#### B. CRM e telefonia — 10 colunas: 3 usar · 6 ressalva · 1 não usar

| Coluna | O que é | Preenchida | Valores distintos | Uso | Observação |
|---|---|---:|---:|---|---|
| `data_visita_ev` | Data e hora da ligação (serial Excel, UTC) | 100% | 18.774 | Ressalva | UTC: subtrair 3h |
| `status` | Status no CRM (Completed, Sem Sucesso, Open) | 100% | 3 | Ressalva | 613 conversas GPT estão fora de Completed |
| `tipo_ligacao` | Inbound ou Outbound | 100% | 2 | Ressalva | saturado (≥ 90% no mesmo valor) |
| `tipo_interacao` | Remota: procurei o cliente / cliente nos procurou | 100% | 2 | **Não usar** | saturado (≥ 90% no mesmo valor); redundante com tipo_ligacao |
| `DIVISIONAL` | Divisional (filtro DVINT) | 100% | 1 | Ressalva | constante |
| `DISTRITAL` | Distrital (DTIN1–5) | 100% | 5 | Usar | — |
| `CARTEIRA` | Carteira do vendedor | 100% | 67 | Usar | — |
| `Data` | Dia da ligação derivado no Power Query | 100% | 22 | Usar | — |
| `Chave` | Carteira + número do mês (chave para metas) | 100% | 126 | Ressalva | linhas de 31/08 recebem mês 08 |
| `CallDurationInSeconds` | Duração da ligação em segundos (tabela Tempo_de_ligação) | 69,9% | 859 | Ressalva | só Completed e só até 22/09 |

#### C. Regra do Power Query — 1 coluna: 0 usar · 1 ressalva · 0 não usar

| Coluna | O que é | Preenchida | Valores distintos | Uso | Observação |
|---|---|---:|---:|---|---|
| `Classificação tipo de ligação` | POSITIVA / INFORMATIVA / DETRATORA / IGNORAR (regra do Power Query) | 100% | 4 | Ressalva | DETRATORA inclui 657 Completed sem análise |

#### D. Aletheia (Gemini) — análise da ligação — 26 colunas: 12 usar · 11 ressalva · 3 não usar

| Coluna | O que é | Preenchida | Valores distintos | Uso | Observação |
|---|---|---:|---:|---|---|
| `resumo_analise` | Resumo narrativo da ligação | 100% | 5.837 | Ressalva | contém nomes de pessoas |
| `objetivo` | Objetivo da ligação (texto) | 100% | 4.536 | Usar | — |
| `objetivo_atingido` | Objetivo foi atingido? | 100% | 2 | Usar | — |
| `oportunidades` | Oportunidades identificadas (texto) | 100% | 5.195 | Usar | — |
| `oportunidades_boleano` | Há oportunidade? | 100% | 2 | Ressalva | saturado (≥ 90% no mesmo valor); VERDADEIRO em 92% |
| `nota_oportunidades` | Nota da oportunidade (0–10) | 100% | 9 | Usar | — |
| `demanda_venda_eminente` | Demanda de venda iminente (texto) | 100% | 2.648 | Usar | — |
| `demanda_venda_eminente_boleano` | Há demanda de venda iminente? | 100% | 2 | Usar | — |
| `nota_demanda_venda` | Nota da demanda de venda (0–10) | 100% | 11 | Usar | — |
| `venda` | Venda realizada na ligação? | 100% | 2 | Ressalva | saturado (≥ 90% no mesmo valor); concorda só em parte com p1_desfecho (kappa 0,46) |
| `demanda_de_atendimento` | Demanda de atendimento (texto) | 100% | 4.567 | Usar | — |
| `demanda_de_atendimento_boleano` | Há demanda de atendimento? | 100% | 2 | Ressalva | VERDADEIRO em 81% |
| `nota_demanda_atendimento` | Nota da demanda de atendimento | 100% | 1 | **Não usar** | constante; constante (0 em 100%) |
| `necessidade_nova_visita` | Necessidade de nova visita (texto) | 100% | 4.540 | Usar | — |
| `necessidade_nova_visita_boleano` | Precisa de nova visita? | 100% | 2 | Ressalva | VERDADEIRO em 79% |
| `urgencia_nova_visita` | Urgência da nova visita (1–10) | 100% | 10 | Usar | — |
| `motivo_nova_visita` | Motivo da nova visita (texto) | 100% | 4.089 | Ressalva | valor-sentinela frequente |
| `data_sugerida_nova_visita` | Data sugerida para a nova visita (dd/mm/aaaa) | 100% | 131 | Ressalva | valor-sentinela frequente |
| `falou_tomador_decisao` | Falou com o tomador de decisão? | 100% | 2 | Usar | — |
| `falou_secretaria_eletronica` | Caiu em secretária eletrônica? | 100% | 2 | Ressalva | saturado (≥ 90% no mesmo valor) |
| `frota_propria` | Frota própria (texto) | 100% | 524 | Ressalva | valor-sentinela frequente |
| `frota_propria_boleano` | Cliente tem frota própria? | 100% | 2 | Usar | — |
| `volume_frota_propria` | Volume da frota própria | 100% | 108 | **Não usar** | valor-sentinela frequente; 95% é 'sem dados necessários' |
| `aluguel_concorrencia` | Aluguel com concorrente (texto) | 100% | 418 | Ressalva | valor-sentinela frequente |
| `aluguel_concorrencia_boleano` | Aluga de concorrente? | 100% | 2 | Ressalva | saturado (≥ 90% no mesmo valor) |
| `volume_aluguel_concorrencia` | Volume alugado do concorrente | 100% | 41 | **Não usar** | valor-sentinela frequente; 99% é 'sem dados necessários' |

#### E. Aletheia (Gemini) — SPIN Selling — 10 colunas: 8 usar · 2 ressalva · 0 não usar

| Coluna | O que é | Preenchida | Valores distintos | Uso | Observação |
|---|---|---:|---:|---|---|
| `resumo_spin` | Resumo da ligação sob a ótica SPIN | 100% | 5.839 | Ressalva | contém nomes de pessoas |
| `spin_situacao` | Evidência SPIN — Situação (texto) | 100% | 5.737 | Usar | — |
| `nota_spin_situacao` | Nota SPIN Situação (1–5) | 100% | 4 | Usar | — |
| `spin_problema` | Evidência SPIN — Problema (texto) | 100% | 4.700 | Usar | — |
| `nota_spin_problema` | Nota SPIN Problema (1–5) | 100% | 5 | Usar | — |
| `spin_implicacao` | Evidência SPIN — Implicação (texto) | 100% | 3.568 | Ressalva | valor-sentinela frequente |
| `nota_spin_implicacao` | Nota SPIN Implicação (1–5) | 100% | 5 | Usar | — |
| `spin_necessidade_solucao` | Evidência SPIN — Necessidade de solução (texto) | 100% | 4.890 | Usar | — |
| `nota_spin_necessidade_solucao` | Nota SPIN Necessidade (1–5) | 100% | 5 | Usar | — |
| `nota_final_spin` | Nota final SPIN (1–5) | 100% | 5 | Usar | — |

#### F. Aletheia (Gemini) — categorização — 5 colunas: 4 usar · 1 ressalva · 0 não usar

| Coluna | O que é | Preenchida | Valores distintos | Uso | Observação |
|---|---|---:|---:|---|---|
| `categoria_principal` | Categoria da ligação (Suporte, Comercial, Consultivo, Tentativa de contato comercial) | 100% | 5 | Ressalva | valor-sentinela frequente; 'Sem Classificação' = ligação sem análise |
| `score_consultivo` | Score consultivo (0–1) | 100% | 7 | Usar | — |
| `score_tentativa_de_contato_comercial` | Score de tentativa de contato comercial (0–1) | 100% | 10 | Usar | — |
| `score_suporte` | Score de suporte (0–1) | 100% | 12 | Usar | — |
| `score_comercial` | Score comercial (0–1) | 100% | 12 | Usar | — |

#### G. Classificador GPT — venda — 9 colunas: 5 usar · 2 ressalva · 2 não usar

| Coluna | O que é | Preenchida | Valores distintos | Uso | Observação |
|---|---|---:|---:|---|---|
| `fonte_classificacao` | Origem da classificação (gpt, auto_curta) | 100% | 2 | Usar | — |
| `era_venda` | Era uma ligação de venda? | 95,7% | 2 | Usar | — |
| `p1_desfecho` | Desfecho comercial (fechou, interessou, não era venda…) | 100% | 5 | Ressalva | versão do classificador muda no mês |
| `p2_tipo` | Tipo da ligação (nova venda, suporte, cobrança…) | 100% | 14 | Ressalva | versão do classificador muda no mês |
| `p1_tentativa_comercial` | Houve tentativa comercial? | 100% | 2 | Usar | — |
| `evidencia_venda` | Evidência da venda (texto curto) | 100% | 4.272 | Usar | — |
| `p1_trecho_venda` | Trecho literal da venda | 41,9% | 2.028 | Usar | — |
| `p1_desfecho_original` | Desfecho original (antes de ajuste de regra) | 0,1% | 3 | **Não usar** | esparso (< 10% da base aplicável); 3 valores em toda a base |
| `p2_tipo_original` | Tipo original (antes de ajuste de regra) | 0,0% | 1 | **Não usar** | constante; esparso (< 10% da base aplicável); 1 valor em toda a base |

#### H. Classificador GPT — problemas — 8 colunas: 3 usar · 5 ressalva · 0 não usar

| Coluna | O que é | Preenchida | Valores distintos | Uso | Observação |
|---|---|---:|---:|---|---|
| `tem_problema` | A ligação tem problema? | 95,7% | 2 | Ressalva | taxa 13,6% → 27,4% em 15/09 |
| `p3_problemas_identificados` | Códigos dos problemas (P1…P15) | 100% | 73 | Ressalva | valor-sentinela frequente |
| `p3_problema_principal` | Problema principal | 95,7% | 16 | Ressalva | valor-sentinela frequente; taxa muda em 15/09 |
| `p3_foi_resolvido_na_ligacao` | Problema resolvido na ligação (SIM, PARCIAL, NAO) | 100% | 4 | Ressalva | valor-sentinela frequente |
| `p3_evidencias` | Evidência do problema (texto) | 100% | 960 | Usar | — |
| `p3_trechos` | Trecho literal do problema | 80,0% | 770 | Usar | — |
| `p3_trechos_status` | Status da busca do trecho | 81,1% | 93 | Usar | — |
| `p3_outro_descricao` | Descrição quando o problema é "Outro" | 5,8% | 56 | Ressalva | esparso (< 10% da base aplicável) |

#### I. Classificador GPT — Challenger — 11 colunas: 6 usar · 5 ressalva · 0 não usar

| Coluna | O que é | Preenchida | Valores distintos | Uso | Observação |
|---|---|---:|---:|---|---|
| `p5_teve_challenger` | Teve Challenger? | 100% | 2 | Ressalva | saturado (≥ 90% no mesmo valor) |
| `p5_codigos_challenger` | Códigos Challenger (CH1–CH7) | 100% | 41 | Ressalva | valor-sentinela frequente |
| `p5_qualidade` | Qualidade do Challenger (alta, media, baixa) | 100% | 4 | Ressalva | saturado (≥ 90% no mesmo valor); valor-sentinela frequente; 83% 'alta' (sem variância) |
| `p5_trouxe_dado` | Trouxe dado concreto? | 95,7% | 2 | Usar | — |
| `p5_conectou_situacao` | Conectou à situação do cliente? | 95,7% | 2 | Usar | — |
| `p5_cliente_reagiu` | Cliente reagiu? | 95,7% | 2 | Usar | — |
| `p5_frase_vendedor` | Frase do vendedor | 96,3% | 500 | Usar | — |
| `p5_reacao_cliente` | Reação do cliente | 57,9% | 241 | Usar | — |
| `p5_challenger_sem_dado` | Challenger sem dado concreto? | 95,7% | 2 | Ressalva | saturado (≥ 90% no mesmo valor) |
| `p5_trecho_challenger` | Trecho literal do Challenger | 68,6% | 295 | Usar | — |
| `p5_trecho_status` | Status da busca do trecho | 69,3% | 3 | Ressalva | saturado (≥ 90% no mesmo valor) |


---

## 3. Auditoria do código M

| ID | Sev. | Achado | Evidência | Impacto | Correção |
|---|---|---|---|---|---|
| M-01 | **Alto** | Ligação concluída **sem análise** vira DETRATORA | 657 Completed sem `analise_llm` → `objetivo_atingido` nulo → R = 0 → DETRATORA; são 26% das 2.511 DETRATORA | Infla o rótulo negativo | Criar a classe "SEM ANÁLISE" |
| M-02 | **Alto** | A chave `Carteira + mês` falha em 31/08 e não tem ano | 934 ligações (4,9%) de 31/08 recebem mês 08; as metas de setembro (mês 09) não casam | Meta e realizado desencontrados | Usar ano + mês da data de referência da meta |
| M-03 | Médio | Ramo morto na regra | `ndv ≥ 8 e A = 0 e sem decisor` nunca ocorre: `ndv ≥ 8` já torna `A = 1`; a cláusula `nova visita e ndv ≥ 8` é redundante. DETRATORA = "objetivo não atingido" | A regra parece mais sofisticada do que é | Simplificar ou reescrever com a intenção original |
| M-04 | Médio | `A` depende de campos saturados | `A` = 1 em 48,4%; "oportunidade ≥ 7" sozinha dá 44,3% e `oportunidades_boleano` é VERDADEIRO em 92% | POSITIVA pouco seletiva | Reavaliar limiares com a distribuição real |
| M-05 | Médio | Corte de data fixo na consulta SQL | `DATA_INCLUSAO_REGISTRO >= '2026-09-01'`: inclui ligações de 31/08 e não cresce sozinho | A consulta não é um produto diário | Janela móvel e histórico preservado |
| M-06 | Médio | `Data` é derivada de UTC | `Date.From(data_visita_ev)` sem ajuste de fuso | Análises por hora erradas | Subtrair 3 h antes de derivar a data |
| M-07 | Médio | Junções à esquerda sem alarme de cobertura | `Tempo_de_ligação` cobre 0% a partir de 23/09; `Ligações Classificadas` cobre 33% | A falta de dado passa despercebida | Medidas de cobertura no BI |
| M-08 | Médio | `Ligações Classificadas` entra sem versão | `p1_desfecho_original` e `p2_tipo_original` têm 3 e 1 linhas | Não dá para rastrear qual regra gerou cada linha | Coluna de versão obrigatória |
| M-09 | Baixo | `IGNORAR` mistura duas razões | 12.582 não concluídas + 318 secretária eletrônica | Perde-se a taxa de secretária | Separar as classes |
| M-10 | Baixo | Filtros sem efeito hoje | `DIVISIONAL = "DVINT"` (1 valor) e `status <> "Not Started"` (valor inexistente) | Escondem mudanças futuras de dado | Manter, mas com alerta quando filtrarem algo |

---

## 4. Auditoria da qualidade dos dados

| ID | Sev. | Achado | Evidência | Impacto | Ação |
|---|---|---|---|---|---|
| F-01 | **Crítico** | O classificador GPT muda de versão dentro de setembro | Taxa de problema 0% (01/09) → 13,6% (02–14) → 27,4% (15–22); 18/09 fora do padrão (Challenger 26,7%, era venda 56,4%) | Impede medir redução | Reprocessar setembro com uma versão e gravá-la em cada linha |
| F-02 | **Crítico** | Duração ausente de 23/09 em diante | Completed com duração: 100% até 22/09; 0% depois | KPI de tempo cego em 6 dias úteis | Chamado em `Tempo_de_ligação` |
| F-03 | **Crítico** | Não há resultado real; "fechou" vem de duas fontes que discordam | Ambos 53 · só Gemini 62 · só GPT 58 (kappa 0,46) | Fechamento ambíguo | "Venda confirmada" (ambos) e "provável" (qualquer um) |
| F-04 | Alto | 613 conversas reais fora de Completed | 613 conversas GPT (13%) como Sem Sucesso/Open; 143 com problema; sem duração | Subestima a carga | Tratar como conversa sem duração |
| F-05 | Alto | Cobertura incompleta | 2.016 Completed sem GPT (28–30/09: 1.035; 31/08: 279; 24/09: 202); 657 sem Gemini | Dias recentes sem classificação | Rodar o classificador em D-1 |
| F-06 | Alto | A qualidade do Challenger perdeu variância | 358 de 430 (83%) "alta"; 9 "baixa" | Sem escala para treinar e medir | Usar as sub-flags como escala |
| F-07 | Alto | IDs de cliente quebrados | 19,3% com menos de 8 dígitos; 7,8% nulos | Junções por cliente falham | Normalizar no Power Query |
| F-08 | Alto | Campos saturados ou mortos | `nota_demanda_atendimento` = 0 em 100%; oportunidades 92%; demanda de atendimento 81%; nova visita 79% | Não discriminam | Retirar de filtros e KPIs |
| F-09 | Alto | Valores-sentinela no lugar de nulo | "sem dados necessários": frota 86%, volume de frota 95%, concorrência 87%, volume de concorrência 99%, `spin_implicacao` 33%, motivo 21%, data sugerida 22% | Contagens e médias enganosas | Converter para nulo antes de medir |
| F-10 | Alto | Dado pessoal em texto livre | 2.690 de 5.839 resumos (46%) citam o 1º nome do vendedor; nomes de clientes nos textos; trechos só parcialmente mascarados | LGPD | Perfis de acesso e máscara |
| F-11 | Médio | Horário em UTC | Picos 12–14h e 17–20h UTC = 9–11h e 14–17h BRT | Análise por hora errada | −3 h no Power Query |
| F-12 | Médio | Rótulos e formatos | "supporte_operacional" (1 linha); `venda` usa True/False e as demais VERDADEIRO/FALSO | Contagens divididas | Dicionário de normalização |
| F-13 | Médio | Status Open sem significado conhecido | 1.647 (8,6%), todos sem análise Gemini; 292 classificados pelo GPT | Desconhecido | Investigar |
| F-14 | Médio | Carteira e vendedor são 1:1 | 67 carteiras = 67 matrículas; 75 clientes em mais de uma carteira | "Por carteira" equivale a "por vendedor" | Uso não punitivo; comparar por pares |
| F-15 | Baixo | Duração extrema | Máx. 3.631 s; 2,5% < 30 s | Distorce médias | Mediana e P90 |

---

## 5. Duas réguas, uma verdade

Carga operacional medida pelos dois motores, por semana (01–22/09, Completed com duração):

| Semana | GPT: horas | GPT: carga operacional | Gemini: horas | Gemini: categoria Suporte |
|---|---:|---:|---:|---:|
| 31/08–06/09 | 69,2 | 37,1% | 73,2 | 50,2% |
| 07–13/09 | 68,8 | 35,0% | 68,9 | 49,1% |
| 14–20/09 | 89,1 | 49,1% | 89,9 | 46,3% |
| 21–22/09 | 38,8 | 55,0% | 39,7 | 43,1% |
| **Período** | **265,9** | **43,2%** | **271,7** | **47,6%** |

**Leitura:** o **nível** está entre 43% e 48% pelos dois lados, então é seguro dizer que perto de metade do tempo ao telefone não é negociação. A **tendência** não é segura: os motores
apontam para lados opostos. O Gemini é a régua de referência porque ficou estável o mês inteiro (nota SPIN média diária entre 2,52 e 2,89, desvio de 0,10) e cobre até 30/09.
Até o baseline congelado, o BI mostra as duas réguas lado a lado e a tendência com selo amarelo.

Alocação pelo Gemini (mesmo período): Suporte 47,6% · Comercial 30,3% · Tentativa de contato comercial 11,5% · Consultivo 10,6%. Duração mediana: Suporte 260 s, Comercial 255 s, Consultivo 124 s, Tentativa de contato 83 s.

---

## 6. As quatro personas avaliam os dados

### 6.1 Quem são

| Persona | Pergunta-guia | Decide | Critério de nota |
|---|---|---|---|
| **P1 · Auditoria de Dados** | "Posso mostrar esse número à diretoria sem constrangimento?" | O que entra no BI e com que selo | Completude, consistência entre fontes, estabilidade, rastreabilidade, privacidade |
| **P2 · Gerência Operacional** (assina as horas devolvidas) | "Onde está o tempo e que alavanca o devolve sem piorar o atendimento?" | Onde atacar a carga e como medir o ganho | Tempo, pendências, reincidência, origem do problema |
| **P3 · Gerência Comercial / Coach** | "O que os melhores fazem, quando insistir ou encerrar, a quem retornar?" | Cadência, priorização e coaching | Conversão, tempo, contato, follow-up, mercado |
| **P4 · Aprendizagem (Treinamento)** | "Que habilidade falta, que exemplo real ensina e como sei que mudou?" | Conteúdo, trilha e avaliação | Competências, exemplos reais, evidência literal |

### 6.2 Nota por bloco (0 a 5)

| Bloco | Confiab. (P1) | Util. P2 | Util. P3 | Util. P4 | Selo |
|---|---:|---:|---:|---:|---|
| A. Identificadores e chaves | 3 | 3 | 4 | 1 | Amarelo |
| B. CRM e telefonia | 4 | 5 | 5 | 2 | Verde |
| C. Regra do Power Query | 2 | 3 | 4 | 1 | Amarelo |
| D. Gemini: análise | 4 | 3 | 5 | 4 | Verde |
| E. Gemini: SPIN | 4 | 1 | 3 | 5 | Verde |
| F. Gemini: categorização | 4 | 4 | 3 | 2 | Verde |
| G. GPT: venda | 2 | 4 | 5 | 3 | Amarelo |
| H. GPT: problemas | 2 | 5 | 3 | 4 | Amarelo |
| I. GPT: Challenger | 2 | 1 | 3 | 5 | Amarelo |

*Notas são avaliação qualitativa minha, para discussão; não saem de fórmula.*

### 6.3 Cinco perguntas por persona: o dado responde?

**P1 · Auditoria de Dados**

| Pergunta | Resposta | Onde |
|---|---|---|
| Os números são estáveis no tempo? | **Não** | F-01 |
| As fontes concordam? | **Parcial**: nível sim, tendência e "fechou" não | Seção 5; F-03 |
| Dá para ligar a ligação a cliente e vendedor com segurança? | **Parcial** | F-07, F-14 |
| Há dado pessoal exposto? | **Sim, exposto** | F-10 |
| A regra do BI está correta? | **Não** | M-01 a M-04 |

**P2 · Gerência Operacional**

| Pergunta | Resposta | Onde |
|---|---|---|
| Quanto do tempo é carga operacional? | **Sim** (43–48%) | Seção 5 |
| Qual problema atacar primeiro? | **Sim** (P1, P2, P13 = 67,5%) | O-03 |
| Quanto trabalho existe fora do telefone? | **Não** | O-12 |
| Quanto vale em R$? | **Não** | O-13 |
| Onde a carga se concentra? | **Sim**: carteira, distrital e 1% dos clientes | O-10, O-84 |

**P3 · Gerência Comercial / Coach**

| Pergunta | Resposta | Onde |
|---|---|---|
| Quando insistir e quando encerrar? | **Parcial**: descritivo, poucos fechamentos | O-17 |
| Quem recontatar? | **Sim** | O-28 |
| Que retorno está vencido? | **Sim** | O-55 |
| O que os melhores fazem? | **Parcial**: dá para achar carteiras desviantes, não a prática | O-52 |
| Qual o resultado real da ligação? | **Não** | O-65 |

**P4 · Aprendizagem**

| Pergunta | Resposta | Onde |
|---|---|---|
| Que habilidade falta? | **Sim** (SPIN Implicação; Challenger com dado) | O-40, O-39 |
| Há exemplo real para ensinar? | **Sim** (2.028 + 770 + 295 trechos) | O-42 |
| A escala de qualidade distingue níveis? | **Não** (83% "alta") | O-44 |
| A nota de treinamento muda o comportamento? | **Não** (sem dado) | O-48 |
| Dá para acompanhar a evolução? | **Parcial** (4 semanas, versão instável) | O-47 |

---

## 7. Catálogo de oportunidades

89 oportunidades. **Prontidão:** *Pronto* = o dado existe no CSV; *Parcial* = precisa de ajuste; *Lacuna* = depende de dado que não temos. **Onda:** 1 = out–nov; 2 = nov–dez; 3 = depende de lacuna ou fica para 2027.
**Persona:** DAD = auditoria, OPE = operacional, COM = comercial, APR = aprendizagem. Campos completos (pergunta, dados, esforço, entrega, pacote) em `anexos/catalogo_oportunidades.csv`; o agrupamento em 12 pacotes e o calendário estão em `PLANO_OPORTUNIDADES.md`.

### E1 · Carga operacional e capacidade

| ID | Oportunidade | Evidência hoje | Prontidão | Impacto | Persona | Onda |
|---|---|---|---|---|---|---:|
| O-01 | Carga operacional completa | 43,2% do tempo (114,8 h em 15 d.u.): 30,0% com problema + 13,1% suporte, cobrança, pós-venda e dúvida de contrato. Régua Gemini (categoria Suporte): 47,6% | Pronto | Alto | OPE | 1 |
| O-02 | Mapa de alocação do tempo | GPT: negociação 35,1% · carga operacional 43,2% · relacionamento sem demanda 20,6% · sem conteúdo 1,1%. Gemini: Suporte 47,6% · Comercial 30,3% · Tentativa de contato 11,5% · Consultivo 10,6% | Pronto | Alto | OPE | 1 |
| O-03 | Pareto do tempo por problema | P1 36,8% · P2 17,2% · P13 13,5% = 67,5% do tempo com problema | Pronto | Alto | OPE | 1 |
| O-04 | Horas excedentes por problema | TMA 432 s vs 232 s (1,9×); ≈ 37 h excedentes em 15 d.u. (≈ 50–60 h/mês) | Pronto | Médio | OPE | 1 |
| O-05 | Pendências geradas | 698 de 778 ligações com problema (89,7%) não foram resolvidas na ligação; ≈ 47/dia | Pronto | Alto | OPE | 1 |
| O-06 | Reincidência de problema | 18,8% das ligações com problema são de clientes com 2+ no período | Pronto | Alto | OPE | 1 |
| O-07 | Origem do problema (inbound x outbound) | Taxa de problema 36% no inbound vs 17% no outbound; 80% das ligações com problema nascem de ligação ativa | Pronto | Médio | OPE | 1 |
| O-08 | Suporte dura tanto quanto venda | Mediana de duração: Suporte 260 s · Comercial 255 s · Consultivo 124 s · Tentativa de contato 83 s | Pronto | Médio | OPE | 1 |
| O-09 | Composição do atendimento sem problema | Sem problema: suporte 23,0 h · dúvida de contrato 8,0 h · cobrança 2,1 h · pós-venda 1,8 h (34,9 h) | Pronto | Médio | OPE | 1 |
| O-10 | Concentração do tempo em poucos clientes | 1% dos clientes (≈ 120) concentra 20,1% do tempo de ligação; 10% concentra 70,7% | Pronto | Alto | OPE | 1 |
| O-11 | Candidatos a autoatendimento ou automação | P1: 208 ligações, 29,4 h · P2: 132 ligações, 13,8 h. A causa raiz não está nos dados, só o sintoma | Parcial | Alto | OPE | 2 |
| O-12 | Carga fora da ligação | ≈ 17 min de conversa por vendedor/dia, 7 min em carga operacional; o resto é invisível aos dados | Lacuna | Alto | OPE | 2 |
| O-13 | Horas devolvidas em R$ | Não há premissa de custo nos dados | Lacuna | Alto | OPE | 2 |
| O-14 | Quando o suporte chega | Suporte (Gemini): 40% das ligações às 8h vs 25% às 16h; segunda 28,7% → sexta 35,5% | Pronto | Médio | OPE | 2 |
| O-15 | Alerta de incidente sistêmico | P1 oscila de 2,4% a 11% das ligações por dia (contaminado pela mudança de versão do GPT) | Parcial | Médio | OPE | 2 |
| O-16 | Conversas reais fora de Completed | 613 conversas classificadas pelo GPT (13%) estão como Sem Sucesso/Open; 143 com problema; sem duração | Pronto | Médio | DAD | 1 |

### E2 · Tempo e ritmo da ligação

| ID | Oportunidade | Evidência hoje | Prontidão | Impacto | Persona | Onda |
|---|---|---|---|---|---|---:|
| O-17 | O fechamento exige tempo | ≥ 5 min = 47% das ligações de negociação, 76% dos fechamentos e 77% do tempo. Taxa: 4,9% (2–5 min) → 12,2% → 19,0% → 32,0% (> 12 min) | Pronto | Alto | COM | 1 |
| O-18 | Zona de baixa eficiência de 2 a 5 minutos | Nova venda: 333 ligações (42%) com 4,2% de fechamento e 0,76 fechamentos/h vs 1,04–1,29 nas outras faixas (14 fechamentos; intervalo largo) | Parcial | Médio | COM | 2 |
| O-19 | Avanço comercial satura em 5–8 minutos | POSITIVA: 19% (1–2 min) → 43% (2–5) → 56% (5–8) → 58% (8–12) → 64% (> 12) | Pronto | Médio | COM | 1 |
| O-20 | Duração das ligações fechadas por tipo | Mediana: nova venda 624 s (≈ 10 min) · renovação 378 s (≈ 6 min); upsell tem só 3 casos | Pronto | Médio | COM | 1 |
| O-21 | TMA alvo por tipo | Mediana: nova venda 277 s · renovação 293 s · suporte 267 s · cobrança 239 s · dúvida de contrato 306 s · relacionamento sem demanda 107 s | Pronto | Médio | COM | 1 |
| O-22 | Ligações muito curtas e secretária eletrônica | 12% das Completed duram < 60 s; secretária eletrônica em 5,4% das analisadas; 'sem conteúdo' = 1,1% do tempo | Pronto | Baixo | OPE | 2 |
| O-23 | Habilidade exige tempo | Challenger: mediana 400 s vs 248 s; SPIN médio 2,5 (< 2 min) → 3,7 (8–12 min). Com duração controlada (5–12 min), o fechamento com Challenger é igual ao sem (9,3% vs 8,7%) | Pronto | Alto | APR | 1 |
| O-24 | Benchmark de TMA por carteira | TMA médio de 129 s a 575 s entre carteiras (≥ 40 ligações classificadas) | Pronto | Médio | COM | 1 |
| O-25 | Fechamentos de menos de 2 minutos | 10 fechamentos em ligações < 2 min; metade são renovações. Separar renovação rápida de sondagem | Parcial | Baixo | COM | 3 |
| O-26 | Talk ratio, silêncio e interrupções | Não há dado de fala por turno | Lacuna | Médio | APR | 3 |

### E3 · Contactabilidade e cadência

| ID | Oportunidade | Evidência hoje | Prontidão | Impacto | Persona | Onda |
|---|---|---|---|---|---|---:|
| O-27 | Funil de contato | 19.078 tentativas → 34,0% Completed; 57,3% Sem Sucesso; 8,6% Open | Pronto | Alto | COM | 1 |
| O-28 | Recontato de clientes não atendidos | 4.766 clientes outbound com 1 tentativa falha; 2.985 até 23/09 sem 2ª tentativa; a 2ª tentativa atende 30,5% → ≈ 900 conversas/mês | Pronto | Alto | COM | 1 |
| O-29 | Melhor horário de ligação | 36,5% (11h) e 36,6% (12h) vs 30,2% (13h); 18h 40,4% (n = 267). Diferença ≤ 6 p.p. | Pronto | Baixo | COM | 2 |
| O-30 | Dia da semana | 33% a 35% em todos os dias úteis (achado negativo) | Pronto | Baixo | COM | 3 |
| O-31 | Inbound como porta do suporte | Inbound = 4,8% das ligações, 69,2% atendidas, 36% com problema | Pronto | Médio | OPE | 2 |
| O-32 | Esforço de discagem | 14,6 tentativas e 5,0 atendidas por vendedor/dia (66% sem conversa) | Pronto | Alto | OPE | 1 |
| O-33 | Atendimento por carteira | 15,7% a 60,8% entre carteiras (≥ 40 ligações classificadas) | Pronto | Médio | COM | 2 |
| O-34 | Cadência ideal de tentativas | 1ª 36,5% · 2ª 30,5% · 3ª 33,5% · 4ª 32,8% (sem queda forte até a 4ª) | Pronto | Médio | COM | 2 |
| O-35 | Capacidade por dia da semana | Tentativas por vendedor: segunda 16,7 · terça 14,0 · quarta 14,7 · quinta 15,6 · sexta 11,9 (−29% vs segunda); atendidas 5,5 vs 3,9 | Pronto | Médio | OPE | 2 |
| O-36 | Clientes com muitas tentativas e nenhuma conversa | 39 clientes com 5+ tentativas sem nenhuma atendida | Pronto | Baixo | COM | 2 |
| O-37 | Motivo da falha de contato | Só existe o status Sem Sucesso | Lacuna | Médio | OPE | 3 |

### E4 · Competências: Challenger, SPIN e trilha

| ID | Oportunidade | Evidência hoje | Prontidão | Impacto | Persona | Onda |
|---|---|---|---|---|---|---:|
| O-38 | Mapa de competências por carteira | Entre carteiras (≥ 40 lig.): SPIN médio 2,9 (2,1 a 3,4); Challenger 9,4% (0,8% a 21,7%) | Pronto | Alto | APR | 1 |
| O-39 | Escada do Challenger | Trouxe dado 14,0% · conectou à situação 20,1% · cliente reagiu 22,1% · Challenger completo 9,1% | Pronto | Alto | APR | 1 |
| O-40 | SPIN: elo fraco | Implicação: nota 1 em 50,7% das ligações (média 2,0) · Problema 27,2% · Necessidade 21,0% · Situação 4,0% | Pronto | Alto | APR | 1 |
| O-41 | SPIN × desfecho | Nota 4: 91,5% 'interessou' e 5,6% fecha; nota 2: 80,5% e 10,8%. O SPIN mede consultoria, não fechamento imediato | Pronto | Médio | APR | 1 |
| O-42 | Banco de conteúdo real | 295 trechos de Challenger · 770 de problemas · 2.028 de venda · 500 frases do vendedor · ≈ 5.840 narrativas SPIN em 4 dimensões | Pronto | Alto | APR | 1 |
| O-43 | Contraexemplos | 86 casos de Challenger sem dado concreto; 2.962 ligações (50,7%) com Implicação nota 1 | Pronto | Médio | APR | 2 |
| O-44 | Qualidade do Challenger sem variância | 358 de 430 (83%) 'alta', 63 'media', 9 'baixa'. Usar as sub-flags (dado, conexão, reação) como escala | Parcial | Alto | APR | 2 |
| O-45 | Uso dos 7 códigos Challenger | CH6 216 · CH3 136 · CH4 108 · CH1 84 · CH5 34 · CH7 34 · CH2 29 | Pronto | Médio | APR | 1 |
| O-46 | Efeito do Challenger no resultado | Negociação: 10,4% vs 8,3%; igual com duração controlada. Challenger SIM/NÃO não serve como KPI | Pronto | Alto | APR | 1 |
| O-47 | Curva de aprendizado | Exige régua estável; hoje há 4 semanas e a versão do GPT muda | Parcial | Alto | APR | 2 |
| O-48 | Dados de treinamento | Não há base de treinamento | Lacuna | Alto | APR | 2 |
| O-49 | Gamificação sem gaming | Challenger SIM/NÃO não discrimina (ver ch_resultado); pontuar dado + conexão + reação | Pronto | Médio | APR | 2 |
| O-50 | Micro-lições por problema | P1/P2/P13 = 67,5% do tempo com problema; só 10,3% resolvidos na ligação; 770 trechos | Parcial | Alto | APR | 2 |
| O-51 | Trilha de conhecimento do vendedor (MVP) | Ver seção 8.1 | Parcial | Alto | APR | 2 |

### E5 · Melhores práticas e disciplina comercial

| ID | Oportunidade | Evidência hoje | Prontidão | Impacto | Persona | Onda |
|---|---|---|---|---|---|---:|
| O-52 | Desviantes positivos por carteira | Carteiras com carga operacional ≤ 25% (n ≥ 43): KPI08A, SPI03A, MOI01A, COI04A, KPI07A, NOR05A. Validar contra ruído e perfil antes de concluir | Parcial | Alto | COM | 2 |
| O-53 | Acesso ao decisor | Decisor em 71,6% das ligações. Em negociação: fechamento 8,4% vs 2,6% e objetivo atingido 77% vs 57% | Pronto | Alto | COM | 1 |
| O-54 | Contato desatualizado | Não falou com o decisor em 28% das ligações analisadas: lista de atualização de contatos | Pronto | Médio | COM | 2 |
| O-55 | Retorno no prazo | 79% das ligações pedem nova visita; dos 1.634 retornos devidos até 30/09, só 27,1% tiveram nova tentativa até o prazo + 2 dias | Pronto | Alto | COM | 1 |
| O-56 | Urgência não muda o comportamento | Retorno no prazo: urgência 1–3 → 22,6% · 4–6 → 26,1% · 7–10 → 28,2% | Pronto | Médio | COM | 1 |
| O-57 | Prazo sugerido de retorno | Mediana de 16 dias (25%–75%: 7 a 30 dias); 22% sem data (valor-sentinela) | Pronto | Baixo | COM | 2 |
| O-58 | Duas fontes de 'venda' | Ambos 53 · só Gemini 62 · só GPT 58 (kappa 0,46). Criar 'venda confirmada' (ambos) e 'venda provável' (qualquer um) | Pronto | Alto | COM | 1 |

### E6 · Clientes e mercado

| ID | Oportunidade | Evidência hoje | Prontidão | Impacto | Persona | Onda |
|---|---|---|---|---|---|---:|
| O-59 | Lista de oportunidades: frota própria | 697 ligações com frota própria (12% das analisadas); volume declarado em 5% (95% é valor-sentinela) | Parcial | Alto | COM | 2 |
| O-60 | Lista de reconquista: aluguel com concorrente | 376 ligações (6% das analisadas); volume declarado em 1% | Parcial | Alto | COM | 2 |
| O-61 | Concorrência na voz do cliente | Menções: Movida 109 · Unidas 48 · Arval 1 | Pronto | Médio | COM | 1 |
| O-62 | Problemas sistêmicos para o Produto | Problema principal: P1 305 · P2 173 · P13 161 · P10 69 · P7 62 ligações | Pronto | Alto | OPE | 1 |
| O-63 | Motivos de nova visita e objetivos | Termos: fidelização 834 · acompanhamento 557 · contrato 498 (em 5.839 análises) | Parcial | Médio | COM | 3 |
| O-64 | Ligações sem código de cliente | 7,8% das ligações sem código (≈ 1.490); 75 clientes aparecem em mais de uma carteira | Pronto | Baixo | DAD | 3 |
| O-65 | Resultado real depois da ligação | Não existe dado de resultado real; 'fechou' vem da própria ligação | Lacuna | Alto | COM | 2 |

### E7 · Qualidade de dados, código M e governança

| ID | Oportunidade | Evidência hoje | Prontidão | Impacto | Persona | Onda |
|---|---|---|---|---|---|---:|
| O-66 | Congelar versão e baseline | Taxa de problema 0% (01/09) → 13,6% (02–14) → 27,4% (15–22); 18/09 fora do padrão | Pronto | Alto | DAD | 1 |
| O-67 | Auditoria amostral humana | Não há matriz de confusão | Lacuna | Alto | DAD | 1 |
| O-68 | Reconciliar Gemini × GPT | 92,5% dos 'suporte_operacional' do GPT são 'Suporte' no Gemini. Nível de carga: 43,2% (GPT) vs 47,6% (Gemini), com tendências opostas | Pronto | Alto | DAD | 1 |
| O-69 | Normalizar IDs de cliente | 19,3% com menos de 8 dígitos (zero perdido); 7,8% nulos | Pronto | Médio | DAD | 1 |
| O-70 | Campos saturados, constantes e redundantes | 8 colunas 'não usar' (ex.: nota_demanda_atendimento = 0 em 100%); oportunidades VERDADEIRO 92%; demanda de atendimento 81%; nova visita 79% | Pronto | Médio | DAD | 1 |
| O-71 | Valores-sentinela | 'sem dados necessários': frota 86% · volume frota 95% · concorrência 87% · volume concorrência 99% · spin_implicacao 33% · motivo 21% · data sugerida 22% | Pronto | Médio | DAD | 1 |
| O-72 | Regra POSITIVA/INFORMATIVA/DETRATORA | 657 Completed sem análise Gemini viram DETRATORA (26% das 2.511); o ramo 'ndv ≥ 8 sem decisor' nunca ocorre; DETRATORA = objetivo não atingido | Pronto | Alto | COM | 1 |
| O-73 | Chave carteira + mês | 934 ligações de 31/08 (4,9%) recebem mês 08; a chave não tem ano | Pronto | Médio | DAD | 1 |
| O-74 | Corte de data fixo | Corte fixo; inclui ligações de 31/08; sem janela móvel nem histórico | Pronto | Médio | DAD | 1 |
| O-75 | Timestamp e calendário | Em UTC: pico real 9–11h e 14–17h BRT, com almoço 12–13h | Pronto | Baixo | DAD | 1 |
| O-76 | LGPD e perfis de acesso | 2.690 de 5.839 resumos (46%) citam o 1º nome do vendedor; nomes de clientes nos textos; trechos só parcialmente mascarados | Pronto | Alto | DAD | 1 |
| O-77 | Duração ausente de 23/09 em diante | Completed com duração: 100% até 22/09; 0% depois | Pronto | Alto | DAD | 1 |
| O-78 | Cobertura de classificação | 2.016 Completed sem GPT (28–30/09: 1.035) e 657 sem Gemini | Pronto | Alto | DAD | 1 |
| O-79 | Status Open | 1.647 (8,6%), todas sem análise Gemini; 292 foram classificadas pelo GPT | Parcial | Médio | DAD | 3 |
| O-80 | Rótulos e formatos | 'supporte_operacional' (1 linha); 'venda' usa True/False e as demais VERDADEIRO/FALSO; versões originais quase vazias (1 e 3 linhas) | Pronto | Baixo | DAD | 3 |
| O-81 | Legenda oficial dos códigos no dicionário do BI | As legendas existem no repositório (classificador e prompts); o CSV traz só o código. Falta publicá-las no BI | Pronto | Médio | DAD | 1 |

### E8 · Gestão e BI

| ID | Oportunidade | Evidência hoje | Prontidão | Impacto | Persona | Onda |
|---|---|---|---|---|---|---:|
| O-82 | Alertas diários | Ruído diário de ±3 p.p. → limites por desvio, não por variação de 1 dia | Parcial | Médio | OPE | 2 |
| O-83 | Ritual semanal | Segunda 08h com Gerência Operacional e Comercial | Pronto | Alto | OPE | 1 |
| O-84 | Metas por perfil de carteira | Carga de 16% a 73% entre carteiras; distrital DTIN4 com 31% vs 43–47% nos demais | Parcial | Alto | OPE | 2 |
| O-85 | Simulador de capacidade | Se P1 cair 30% → ≈ 8,8 h por 15 d.u. (≈ 12 h/mês) | Pronto | Médio | OPE | 2 |
| O-86 | Painel de coaching por carteira | 295 trechos de Challenger + 770 de problemas com evidência literal | Pronto | Alto | COM | 1 |
| O-87 | Pilotos pareados por carteira | 6 pares de carteiras com carga parecida (54,7% vs 56,0%), sorteados entre piloto e controle | Pronto | Alto | OPE | 1 |
| O-88 | Fila de ligações prioritárias | Depende de corrigir a regra POSITIVA/DETRATORA e do resultado real | Parcial | Alto | COM | 3 |
| O-89 | Previsão de carga | Não há série estável | Lacuna | Médio | OPE | 3 |


---

## 8. Dois projetos de destaque

### 8.1 Trilha de conhecimento do vendedor ("Duolingo do vendedor")

**Ideia:** cada ligação real vira exercício, e a árvore de habilidades de cada vendedor se atualiza com o que ele faz ao telefone. Tudo o que está abaixo usa colunas do CSV.

| Trilha | Degraus | Dado que mede | Linha de base (set) |
|---|---|---|---|
| T1 Diagnóstico SPIN | Situação → Problema → **Implicação** → Necessidade | `nota_spin_*` | Implicação com nota 1 em 50,7% |
| T2 Challenger | Trazer dado → conectar à situação → provocar reação (CH1–CH7) | `p5_trouxe_dado`, `p5_conectou_situacao`, `p5_cliente_reagiu` | 14,0% → 20,1% → 22,1%; completo 9,1% |
| T3 Decisor e contato | Chegar ao decisor, tratar secretária, atualizar contato | `falou_tomador_decisao`, `falou_secretaria_eletronica` | Decisor 71,6%; secretária 5,4% |
| T4 Próximo passo e retorno | Fechar com data e urgência realista, voltar no prazo | `necessidade_nova_visita`, `data_sugerida`, `urgencia_nova_visita` | Retorno no prazo 27,1% |
| T5 **Resolver rápido** | Identificar, resolver ou encaminhar P1/P2/P13 em poucos minutos | `tem_problema`, duração, `p3_foi_resolvido_na_ligacao` | 10,3% resolvidos; TMA 432 s |
| T6 Conduzir o tempo | Aprofundar quando há demanda, encerrar quando não há | duração × resultado | Zona de 2–5 min com 0,76 fechamentos/h |

**Mecânica proposta:**
1. **Diagnóstico automático:** o perfil de cada carteira nos últimos 30 dias define o nível em cada trilha.
2. **Lição diária de 3–5 min:** um trecho real, a pergunta "o que faltou?", a resposta modelo (escrita por humano) e o motivo.
3. **Missão da semana:** uma meta de comportamento (ex.: trazer 1 dado concreto em 3 ligações) verificada nas ligações da semana.
4. **XP, sequência e níveis por habilidade;** comparação entre carteiras de perfil parecido, com foco na evolução própria e sem ranking punitivo.
5. **Anti-gaming:** pontuar a qualidade (dado + conexão + reação), nunca o SIM/NÃO; o coach audita 10% dos acertos.
6. **Laço de medição:** lição → comportamento nas ligações em 14 dias → TMA, desfecho e carga operacional.

**Conteúdo disponível no CSV:** 295 trechos de Challenger, 770 de problemas, 2.028 de venda, 500 frases do vendedor e ≈ 5.840 narrativas SPIN em 4 dimensões.
**O que falta:** a resposta modelo de cada lição (curadoria humana), exemplos de qualidade alta além de CH6/CH3 (CH6 216, CH3 136, CH4 108, CH1 84, CH5 34, CH7 34, **CH2 29**), exemplos de objeção (não há coluna) e a base de notas de treinamento.

**MVP em dezembro:** duas trilhas (T2 degrau "dado concreto" e T5 "resolver rápido") para as carteiras-piloto, 10 lições, regra de XP e plano de medição. Marcos: 13/11 especificação; 27/11 conteúdo curado; 07/12 piloto no ar; 17/12 leitura.
**Riscos:** gaming da métrica; sensação de vigilância; régua do classificador instável; o tempo da lição concorre com a missão de reduzir carga (por isso 3–5 min); LGPD nos trechos.

### 8.2 Tempo da ligação comercial: o que um mês de dados sustenta

Base: 1.139 ligações de negociação (GPT) com duração, 01–22/09. **Fechamento = "fechou" (GPT) ou "venda" (Gemini):** 138 eventos. Os intervalos são de 95% (Wilson).

| Duração | Ligações | Fechamentos | Taxa (intervalo) | Fechamentos por hora de conversa | % POSITIVA (nestas ligações) |
|---|---:|---:|---|---:|---:|
| < 2 min | 135 | 10 | 7,4% (4,1–13,1) | 2,87 | 59% |
| 2–5 min | 472 | 23 | 4,9% (3,3–7,2) | 0,87 | 69% |
| 5–8 min | 237 | 29 | 12,2% (8,7–17,0) | 1,16 | 73% |
| 8–12 min | 142 | 27 | 19,0% (13,4–26,3) | 1,17 | 70% |
| > 12 min | 153 | 49 | 32,0% (25,2–39,8) | 1,00 | 71% |

**O que os dados sustentam:**
- Ligações de **5 min ou mais** são 47% das ligações de negociação, produzem 76% dos fechamentos e usam 77% do tempo: **proporcional**, ou seja, sem ganho de eficiência por alongar.
- A eficiência por hora é **plana (≈ 1,0–1,2) de 5 min em diante** e **menor entre 2 e 5 min** (0,87). Em nova venda, 333 ligações (42%) ficam nessa faixa com 4,2% de fechamento e 0,76 fechamentos/h (só 14 fechamentos: o intervalo é largo).
- Os fechamentos de < 2 min são raros e metade é renovação; a mediana das ligações fechadas é **624 s (≈ 10 min) em nova venda** e **378 s (≈ 6 min) em renovação**.
- O avanço comercial (POSITIVA, a régua do Power Query) **satura cedo**. Em todas as ligações analisadas: 19% (1–2 min) → 43% (2–5) → 56% (5–8) → 58% (8–12) → 64% (> 12). Dentro das ligações de negociação, fica estável em ≈ 70% a partir de 2 min.

**O que NÃO sustentam:** uma duração ótima única, nem que alongar a ligação *cause* o fechamento (quem vai fechar tende a conversar mais). Com um mês e 138 fechamentos, a leitura é descritiva.

**Como transformar em recomendação (experimento nas carteiras-piloto):** protocolo de aprofundamento — após 3 min com decisor e dor identificada, conduzir até 8–12 min; ligação sem demanda encerra em até 2 min com próximo contato registrado.
Medir fechamentos por hora e carga operacional contra o controle. **Metas por tipo (hipótese):** nova venda 8–12 min · renovação 5–7 min · relacionamento sem demanda ≤ 2 min · suporte, reduzir da mediana atual (267 s).

---

## 9. Priorização

**Compromisso x exploração.** O plano compromete poucas coisas (a missão e seus KPIs); o resto é exploração com data para acabar. A exploração só vira compromisso se passar por um gate (dado pronto, dono, esforço).

| Bloco | Itens | Regra |
|---|---|---|
| **Compromisso** (Canvas) | O-01, O-03, O-04, O-05, O-06, O-07, O-66, O-68, O-69, O-72, O-73, O-77, O-83, O-87 | Entram nos marcos do plano |
| **Exploração com data** | Tempo (O-17, O-19), recontato e retorno (O-28, O-55, O-56), Challenger e SPIN (O-39, O-40, O-46), concorrência (O-61) | Dossiê com data; vira compromisso se houver dono |
| **Projeto de destaque** | Trilha MVP (O-51) | Gate em 13/11: base de treinamento e escala de qualidade recalibrada |
| **Depende de lacuna** | Onda 3 | Entra no pedido de dados (seção 10) |

**Dependências:** O-66 antecede O-47, O-82 e O-84; O-69 antecede O-06 e O-10; O-72 antecede O-88; O-65 antecede qualquer "fila de prioridade".

As ondas dizem **quando o dado permite**, não **o que será feito**: só vira entrega o bloco Compromisso e o que passar no gate.

### Onda 1 — outubro a novembro (dado pronto, esforço baixo ou médio) (50 itens)

| ID | Oportunidade | Impacto | Esforço | Persona | Entrega |
|---|---|---|---|---|---|
| O-01 | Carga operacional completa | Alto | P | OPE | KPI norte |
| O-02 | Mapa de alocação do tempo | Alto | P | OPE | BI (Mês) |
| O-03 | Pareto do tempo por problema | Alto | P | OPE | BI + dossiê |
| O-05 | Pendências geradas | Alto | P | OPE | KPI |
| O-06 | Reincidência de problema | Alto | P | OPE | Lista ativa |
| O-10 | Concentração do tempo em poucos clientes | Alto | P | OPE | Lista de contas de alto consumo |
| O-17 | O fechamento exige tempo | Alto | P | COM | Dossiê |
| O-23 | Habilidade exige tempo | Alto | P | APR | Dossiê |
| O-27 | Funil de contato | Alto | P | COM | BI |
| O-28 | Recontato de clientes não atendidos | Alto | P | COM | Lista ativa |
| O-32 | Esforço de discagem | Alto | P | OPE | KPI |
| O-38 | Mapa de competências por carteira | Alto | M | APR | BI (radar) |
| O-39 | Escada do Challenger | Alto | P | APR | Trilha |
| O-40 | SPIN: elo fraco | Alto | P | APR | Trilha |
| O-42 | Banco de conteúdo real | Alto | M | APR | Biblioteca curada |
| O-46 | Efeito do Challenger no resultado | Alto | P | APR | Dossiê |
| O-53 | Acesso ao decisor | Alto | P | COM | Treino de abordagem |
| O-55 | Retorno no prazo | Alto | P | COM | Agenda de retorno |
| O-58 | Duas fontes de 'venda' | Alto | P | COM | Definição de KPI |
| O-62 | Problemas sistêmicos para o Produto | Alto | P | OPE | Dossiê ao Produto |
| O-66 | Congelar versão e baseline | Alto | M | DAD | E2 do plano |
| O-67 | Auditoria amostral humana | Alto | M | DAD | Indicador C4 |
| O-68 | Reconciliar Gemini × GPT | Alto | P | DAD | Régua cruzada |
| O-72 | Regra POSITIVA/INFORMATIVA/DETRATORA | Alto | P | COM | Corrigir regra e nome |
| O-76 | LGPD e perfis de acesso | Alto | P | DAD | RBAC e máscara |
| O-77 | Duração ausente de 23/09 em diante | Alto | P | DAD | Chamado em Tempo_de_ligação |
| O-78 | Cobertura de classificação | Alto | P | DAD | Rodar o D-1 |
| O-83 | Ritual semanal | Alto | P | OPE | Rotina |
| O-86 | Painel de coaching por carteira | Alto | M | COM | 1:1 com evidência |
| O-87 | Pilotos pareados por carteira | Alto | P | OPE | Piloto e controle |
| O-04 | Horas excedentes por problema | Médio | P | OPE | KPI |
| O-07 | Origem do problema (inbound x outbound) | Médio | P | OPE | Dossiê |
| O-08 | Suporte dura tanto quanto venda | Médio | P | OPE | Dossiê |
| O-09 | Composição do atendimento sem problema | Médio | P | OPE | BI |
| O-16 | Conversas reais fora de Completed | Médio | P | DAD | Correção de dados |
| O-19 | Avanço comercial satura em 5–8 minutos | Médio | P | COM | Dossiê |
| O-20 | Duração das ligações fechadas por tipo | Médio | P | COM | Metas por tipo |
| O-21 | TMA alvo por tipo | Médio | P | COM | Metas por tipo |
| O-24 | Benchmark de TMA por carteira | Médio | P | COM | BI |
| O-41 | SPIN × desfecho | Médio | P | APR | Dossiê |
| O-45 | Uso dos 7 códigos Challenger | Médio | P | APR | Trilha |
| O-56 | Urgência não muda o comportamento | Médio | P | COM | Fila priorizada |
| O-61 | Concorrência na voz do cliente | Médio | P | COM | Dossiê |
| O-69 | Normalizar IDs de cliente | Médio | P | DAD | Regra no Power Query |
| O-70 | Campos saturados, constantes e redundantes | Médio | P | DAD | Limpeza do BI |
| O-71 | Valores-sentinela | Médio | P | DAD | Tratar como nulo |
| O-73 | Chave carteira + mês | Médio | P | DAD | Corrigir no Power Query |
| O-74 | Corte de data fixo | Médio | P | DAD | Parametrizar |
| O-81 | Legenda oficial dos códigos no dicionário do BI | Médio | P | DAD | Dicionário no BI |
| O-75 | Timestamp e calendário | Baixo | P | DAD | Subtrair 3h |

### Onda 2 — novembro a dezembro (precisa de baseline, ajuste ou dado complementar) (29 itens)

| ID | Oportunidade | Impacto | Esforço | Persona | Entrega |
|---|---|---|---|---|---|
| O-11 | Candidatos a autoatendimento ou automação | Alto | M | OPE | Hipótese ao Produto |
| O-12 | Carga fora da ligação | Alto | M | OPE | Amostra de 8–10 vendedores, 1 semana |
| O-13 | Horas devolvidas em R$ | Alto | P | OPE | Premissa com RH/Finanças |
| O-44 | Qualidade do Challenger sem variância | Alto | M | APR | Regra de pós-processamento |
| O-47 | Curva de aprendizado | Alto | M | APR | BI |
| O-48 | Dados de treinamento | Alto | M | APR | Pedir base ao T&D/RH |
| O-50 | Micro-lições por problema | Alto | M | APR | Trilha 'Resolver rápido' |
| O-51 | Trilha de conhecimento do vendedor (MVP) | Alto | G | APR | MVP em dezembro |
| O-52 | Desviantes positivos por carteira | Alto | M | COM | Entrevistas + playbook |
| O-59 | Lista de oportunidades: frota própria | Alto | P | COM | Lista de oportunidades |
| O-60 | Lista de reconquista: aluguel com concorrente | Alto | P | COM | Lista de oportunidades |
| O-65 | Resultado real depois da ligação | Alto | M | COM | Pedir base de resultado |
| O-84 | Metas por perfil de carteira | Alto | M | OPE | Pares comparáveis |
| O-14 | Quando o suporte chega | Médio | P | OPE | BI + escala |
| O-15 | Alerta de incidente sistêmico | Médio | M | OPE | Alerta ao Produto |
| O-18 | Zona de baixa eficiência de 2 a 5 minutos | Médio | P | COM | Experimento |
| O-31 | Inbound como porta do suporte | Médio | P | OPE | Dossiê |
| O-33 | Atendimento por carteira | Médio | P | COM | Benchmark |
| O-34 | Cadência ideal de tentativas | Médio | P | COM | Dossiê |
| O-35 | Capacidade por dia da semana | Médio | P | OPE | Escala e agenda |
| O-43 | Contraexemplos | Médio | P | APR | Biblioteca 'erros comuns' |
| O-49 | Gamificação sem gaming | Médio | M | APR | Regras de XP |
| O-54 | Contato desatualizado | Médio | P | COM | Lista de contatos a corrigir |
| O-82 | Alertas diários | Médio | M | OPE | BI |
| O-85 | Simulador de capacidade | Médio | P | OPE | BI what-if |
| O-22 | Ligações muito curtas e secretária eletrônica | Baixo | P | OPE | Higiene do funil |
| O-29 | Melhor horário de ligação | Baixo | P | COM | Dossiê |
| O-36 | Clientes com muitas tentativas e nenhuma conversa | Baixo | P | COM | Lista de higiene |
| O-57 | Prazo sugerido de retorno | Baixo | P | COM | Dossiê |

### Onda 3 — depende de lacuna ou fica para 2027 (10 itens)

| ID | Oportunidade | Impacto | Esforço | Persona | Entrega |
|---|---|---|---|---|---|
| O-88 | Fila de ligações prioritárias | Alto | G | COM | Só após baseline |
| O-26 | Talk ratio, silêncio e interrupções | Médio | G | APR | — |
| O-37 | Motivo da falha de contato | Médio | M | OPE | — |
| O-63 | Motivos de nova visita e objetivos | Médio | M | COM | Taxonomia de motivos |
| O-79 | Status Open | Médio | P | DAD | Investigar |
| O-89 | Previsão de carga | Médio | G | OPE | — |
| O-25 | Fechamentos de menos de 2 minutos | Baixo | M | COM | Dossiê |
| O-30 | Dia da semana | Baixo | P | COM | Fecha hipótese |
| O-64 | Ligações sem código de cliente | Baixo | P | DAD | Higiene de cadastro |
| O-80 | Rótulos e formatos | Baixo | P | DAD | Dicionário de normalização |


---

## 10. Pedidos de dado (lacunas)

| # | Dado | Para quê | Quem pode dar |
|---|---|---|---|
| 1 | Duração das ligações a partir de 23/09 | Fechar a série de tempo (F-02) | Dados/TI |
| 2 | Resultado real depois da ligação (reservas, contratos, diárias) | Provar conversão e ROI (O-65) | Dados/Comercial |
| 3 | Base de treinamento (notas, presença, trilha cursada) | Trilha e curva de aprendizado (O-48) | T&D/RH |
| 4 | Meses anteriores no mesmo formato | Tendência e sazonalidade | Aletheia |
| 5 | Custo-hora do vendedor | Horas devolvidas em R$ (O-13) | Finanças/RH |
| 6 | Diário de tempo de 8–10 vendedores por 1 semana | Carga fora do telefone (O-12) | Gerência Operacional |
| 7 | Log de telefonia (motivo da falha, tentativas) | O-37 | Telefonia |
| 8 | Perfil da carteira (porte, segmento, clientes ativos), escala e senioridade | Metas por perfil (O-84) | Comercial |
| 9 | Significado do status Open | F-13 | CRM |

---

## 11. Reprodutibilidade

| Arquivo | O que faz |
|---|---|
| `scripts/auditoria_dados_missao.py` | Recalcula todos os números desta auditoria a partir do CSV e escreve os anexos |
| `scripts/baseline_carga_operacional.py` | Baseline do KPI de problema |
| `scripts/gerar_dados_prototipos.py` | Gera os agregados que alimentam os dois protótipos |
| `missao_4T26/prototipos/bi_wireframe.html` | Wireframe interativo das 8 páginas do BI, com dados reais agregados |
| `missao_4T26/prototipos/trilha_prototipo.html` | Protótipo da trilha do vendedor: diagnóstico por carteira e 12 lições com trechos mascarados |
| `missao_4T26/anexos/dicionario_dados_setembro.csv` | Perfil das 88 colunas (bloco, preenchimento, domínio, saturação, uso recomendado) |
| `missao_4T26/anexos/serie_diaria_set_2026.csv` | Assinatura diária do classificador (para o drift) |
| `missao_4T26/anexos/carteira_set_2026.csv` | Métricas por carteira (≥ 40 ligações classificadas; sem nome de vendedor) |
| `missao_4T26/anexos/tempo_otimo_set_2026.csv` | Tabela da seção 8.2 |
| `missao_4T26/anexos/catalogo_oportunidades.csv` | Catálogo completo |
