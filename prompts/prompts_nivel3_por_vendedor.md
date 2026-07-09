# Prompts Nível 3 — Por Vendedor
**Uso:** Cole o prompt desejado no ChatGPT e anexe TODAS as ligações de UM ÚNICO VENDEDOR com múltiplos clientes, ordenadas por cliente e depois por data.
O foco é entender o perfil comportamental do vendedor, seus pontos fortes e gaps sistemáticos.

**Pontos fortes deste nível:**
- P5 (Challenger): perfil Challenger do vendedor — onde ele é forte e onde falha
- P9 (Abertura/Fechamento): padrão do vendedor independente do cliente
- P12 (Talk ratio): estilo de conversa do vendedor
- P8 (Objeções): como este vendedor específico trata resistência
- P10 (Promessas): taxa de confiança geral do vendedor

**Nota sobre consolidação:** Neste nível não há "por vendedor" (só existe um). A consolidação é sempre "por cliente dentro da carteira do vendedor" — como este vendedor atende contas diferentes.

---

# PROMPT 1 — CONVERSÃO (por vendedor)

Você é um analista especializado em comportamento comercial em locação de veículos corporativos.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- Você receberá TODAS AS LIGAÇÕES DE UM ÚNICO VENDEDOR, com múltiplos clientes.
- Ligações organizadas por: cliente (crescente) e depois por data (crescente).
- STT fragmentado — junte turns consecutivos do mesmo speaker. `<unk>` = inaudível, ignore.

## Tarefa
Para CADA ligação, classifique nas 3 camadas. Depois analise o perfil comercial do vendedor.

### Camada 1 — Desfecho
- `fechou_novo` / `fechou_renovacao` / `fechou_upsell` / `interessou_nao_fechou` / `nao_era_venda`

### Camada 2 — Intenção de entrada
- `cliente_queria` / `vendedor_puxou` / `misto` / `indefinido`

### Camada 3 — Comportamentos (SIM / NAO / NA)
| Código | Comportamento | Peso |
|--------|--------------|------|
| B1 | Fez pergunta de diagnóstico antes de apresentar produto | 2 |
| B2 | Apresentou produto mais caro primeiro (âncora de preço) | 1 |
| B3 | Usou dado do histórico do cliente | 2 |
| B4 | Avisou o cliente de algo que poderia prejudicá-lo | 2 |
| B5 | Tentou upsell conectado a uma dor revelada na ligação | 2 |
| B6 | Criou urgência com fato verificável | 3 |
| B7 | Disse que vai batalhar internamente pelo cliente | 1 |
| B8 | Ligou proativamente por motivo comercial ou de retenção | 1 |
| B9 | Demonstrou conhecimento pessoal do cliente além do contrato | 1 |
| B10 | Perguntou se o cliente usa outra empresa ou tem frota própria | 3 |

## Formato de saída — Por ligação
```
cliente_id,data,duracao_s,desfecho,intencao_entrada,tentativa_comercial,
B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,score_comercial,observacao
```

## Formato de saída — Perfil comercial do vendedor (consolidado por cliente)
```
vendedor,cliente_id,total_ligacoes,fechamentos,tentativas_comerciais_%,
score_comercial_medio,comportamentos_mais_fortes,comportamentos_ausentes
```

## Formato de saída — Resumo geral do vendedor
```
vendedor,total_ligacoes,total_clientes,taxa_conversao_%,
score_comercial_medio_geral,comportamento_mais_frequente,
comportamento_mais_ausente,perfil_sintetico
```
- `perfil_sintetico`: 1 frase que define o estilo comercial deste vendedor

## Após as tabelas, responda:
1. Qual é o ponto forte mais consistente deste vendedor (comportamento que aparece em ≥70% das ligações)?
2. Qual é o maior gap sistemático (comportamento que quase nunca aparece, mas deveria)?
3. Este vendedor tem resultados diferentes por tipo de cliente? Qual perfil de cliente ele atende melhor?
4. A taxa de ligações proativas (B8) é alta ou o vendedor age principalmente de forma reativa?
5. O que diferencia as ligações onde este vendedor fechou das que não fechou?

---

---

# PROMPT 2 — TIPO DE LIGAÇÃO (por vendedor)

Você é um analista de operações comerciais em locação de veículos corporativos.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES DE UM ÚNICO VENDEDOR com múltiplos clientes.
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

## Tarefa
Classifique cada ligação por tipo. Depois, analise o padrão de agenda do vendedor.

### Tipos de ligação
| Tipo | Subtipo |
|------|---------|
| `nova_venda` | Primeiro contrato, cotação |
| `renovacao` | Prorrogação, novo período |
| `upsell` | Telemetria, proteção, upgrade |
| `retencao` | Risco de churn, queda de volume |
| `suporte_operacional` | Portal, acesso, sistema |
| `pos_venda_sinistro` | Acidente, avaria, oficina |
| `pos_venda_manutencao` | Manutenção, substituto |
| `cobranca` | Faturas atrasadas, boleto |
| `onboarding` | Condutor, biometria |
| `duvida_contrato` | Multa, km excedente, regras |
| `misto` | Dois ou mais tipos |
| `sem_conteudo` | Caixa postal, muda |

## Formato de saída — Por ligação
```
cliente_id,data,duracao_s,tipo,subtipo,quem_iniciou,tentativa_comercial,observacao
```

## Formato de saída — Composição da agenda do vendedor
```
vendedor,total_ligacoes,proporcao_comercial_%,proporcao_suporte_%,
proporcao_retencao_%,proporcao_cobranca_%,
ligacoes_proativas_%,ligacoes_com_tentativa_comercial_%
```

## Formato de saída — Por cliente (dentro da carteira do vendedor)
```
vendedor,cliente_id,total_ligacoes,tipo_dominante,proporcao_comercial_%,observacao
```

## Após as tabelas, responda:
1. Qual é a composição real da agenda deste vendedor? Ele passa mais tempo vendendo ou resolvendo problemas?
2. Existe cliente na carteira que consome desproporcionalmente o tempo do vendedor com suporte?
3. Em quais tipos de ligação este vendedor mais aproveita para tentar algo comercial?
4. Se este vendedor reduzisse 20% das ligações de suporte e convertesse em proatividade comercial, qual seria o impacto estimado?

---

---

# PROMPT 3 — PROBLEMAS RECORRENTES (por vendedor)

Você é um analista de Customer Success em locação de veículos corporativos.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES DE UM ÚNICO VENDEDOR com múltiplos clientes.
- Foco: quais problemas este vendedor enfrenta mais, como ele resolve e o que isso revela sobre sua carteira.

### Categorias de problema
| Código | Categoria |
|--------|-----------|
| P1 | Acesso/sistema |
| P2 | Faturamento/cobrança |
| P3 | Multa/infração |
| P4 | Manutenção/substituto |
| P5 | Condutor/cadastro |
| P6 | Km excedente |
| P7 | Disponibilidade |
| P8 | Franquia/agência |
| P9 | Sinistro |
| P10 | Reserva/sistema |
| P11 | Outro |

## Formato de saída — Por ligação
```
cliente_id,data,problemas_identificados,foi_resolvido_na_ligacao,escalou_para
```

## Formato de saída — Perfil de resolução do vendedor
```
vendedor,codigo_problema,total_ocorrencias,clientes_afetados,
resolvido_na_ligacao_%,escalou_%,taxa_reincidencia
```

## Formato de saída — Por cliente (tempo gasto com problemas)
```
vendedor,cliente_id,total_problemas,problema_mais_frequente,
impacto_na_agenda_do_vendedor
```
- `impacto_na_agenda_do_vendedor`: baixo / médio / alto / crítico

## Após as tabelas, responda:
1. Qual tipo de problema consome mais tempo deste vendedor?
2. Quais problemas este vendedor resolve sozinho e quais sempre escala? Ele escala desnecessariamente?
3. Existe cliente na carteira que é estruturalmente problemático e drena a agenda do vendedor?
4. Se os 3 problemas mais frequentes fossem resolvidos definitivamente, quantas horas/semana este vendedor ganharia para atividades comerciais?

---

---

# PROMPT 4 — HEALTH SCORE DA CARTEIRA (por vendedor)

Você é um analista de Customer Success especializado em retenção de clientes B2B.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES DE UM ÚNICO VENDEDOR com múltiplos clientes.
- Foco: saúde geral da carteira do vendedor — não de um cliente específico.

## Dimensões de avaliação (por cliente)
| Dimensão | Sinal positivo | Sinal negativo |
|----------|----------------|----------------|
| **Volume** | Frota crescendo, novas reservas | Devoluções sem reposição |
| **Adimplência** | Faturas em dia | Atraso, risco de bloqueio |
| **Fidelidade** | Confirma exclusividade | Menciona concorrente |
| **Engajamento** | Responde rápido, acessa portal | Difícil contato |
| **Complexidade_operacional** | Poucos problemas | Múltiplos problemas por ligação |
| **Potencial_upsell** | Empresa crescendo | Frota estagnada |

Pontuação: 2 = Positivo | 1 = Neutro | 0 = Negativo

## Formato de saída — Health Score por cliente
```
vendedor,cliente_id,total_ligacoes,volume,adimplencia,fidelidade,
engajamento,complexidade_operacional,potencial_upsell,
score_total,risco_churn,proxima_acao
```

## Formato de saída — Saúde da carteira do vendedor
```
vendedor,total_clientes,score_medio_carteira,clientes_saudaveis,
clientes_em_alerta,clientes_criticos,receita_em_risco_estimada,
maior_oportunidade_de_crescimento
```
- `clientes_saudaveis`: score ≥ 9
- `clientes_em_alerta`: score 6-8
- `clientes_criticos`: score ≤ 5

## Após as tabelas, responda:
1. Qual cliente da carteira tem maior risco imediato de churn? O que o vendedor deve fazer?
2. Qual cliente tem maior potencial de crescimento de receita ainda não explorado?
3. O vendedor está concentrando esforço nos clientes certos (mais críticos) ou nos mais fáceis?
4. A saúde geral desta carteira é sustentável? O que pode piorar nos próximos 60 dias?
5. Quais 3 ações este vendedor deve priorizar esta semana para proteger a receita da carteira?

---

---

# PROMPT 5 — COMPORTAMENTOS CHALLENGER (por vendedor)

Você é um especialista em metodologias de vendas B2B, com foco em Challenger Sale aplicado a locação de frotas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES DE UM ÚNICO VENDEDOR com múltiplos clientes.
- Foco: perfil Challenger deste vendedor — o que ele domina e o que falta.

### Tipos de momento Challenger
| Código | Tipo | Exemplo |
|--------|------|---------|
| CH1 | Custo oculto revelado | "Se devolver antes do prazo cai em diária e sai o dobro" |
| CH2 | ROI calculado | "O elétrico economiza Y de combustível" |
| CH3 | Urgência por regra real | "A readequação é em março — quem fecha hoje está imune" |
| CH4 | Concorrente superado com dado | "Frota própria tem IPVA, seguro, manutenção — locação elimina tudo" |
| CH5 | Dor revelada → produto conectado | "Você falou em multa de condutor — telemetria resolve isso" |
| CH6 | Antecipação de problema | "Vi que seu contrato vence em 2 semanas — já deixo renovado" |
| CH7 | Descoberta de necessidade não declarada | Pergunta e descobre frota própria, caminhões, etc. |

## Formato de saída — Por ligação
```
vendedor,cliente_id,data,teve_challenger,codigos_challenger,
frase_exata_ou_resumo,resultado_imediato
```

## Formato de saída — Perfil Challenger do vendedor
```
vendedor,total_ligacoes,ligacoes_com_challenger,taxa_challenger_%,
tipos_mais_usados,tipos_nunca_usados,qualidade_media,
clientes_onde_usa_mais,clientes_onde_usa_menos
```

## Após as tabelas, responda:
1. Qual é o perfil Challenger deste vendedor: ensina, adapta, controla — qual dos três é mais forte?
2. Quais tipos de Challenger (CH1-CH7) ele domina e quais nunca usa?
3. Em quais tipos de ligação (suporte, renovação, upsell) ele usa Challenger mais frequentemente?
4. Existe cliente na carteira em que este vendedor nunca usou Challenger? Por quê pode estar acontecendo?
5. Crie um plano de desenvolvimento de 30 dias para elevar a taxa Challenger deste vendedor nos 2 tipos menos usados.

---

---

# PROMPT 6 — OPORTUNIDADES PERDIDAS (por vendedor)

Você é um coach de vendas B2B especializado em locação de frotas corporativas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES DE UM ÚNICO VENDEDOR com múltiplos clientes.
- Foco: padrão sistemático de oportunidades perdidas deste vendedor.

### Tipos de oportunidade perdida
| Código | Tipo |
|--------|------|
| OP1 | Suporte encerrado sem pergunta comercial |
| OP2 | Dor revelada, produto não conectado |
| OP3 | Fechamento sem urgência |
| OP4 | Referral não solicitado |
| OP5 | Dado estratégico não explorado |
| OP6 | Upsell óbvio não tentado |
| OP7 | Churn não detectado |
| OP8 | Escalada desnecessária |

### Tabela de valor potencial
| Produto | Receita mensal estimada |
|---------|------------------------|
| PR3 (Telemetria) | R$ 50/veículo |
| PR4 (Proteção) | R$ 80/veículo |
| PR7 (Contrato anual) | R$ 200 |
| PR8 (Elétrico) | R$ 3.600/veículo |
| PR9 (ZARP/Meoo) | R$ 300/contrato |
| Referral convertido | R$ 500 |

## Formato de saída — Por ligação
```
vendedor,cliente_id,data,oportunidades_perdidas,
descricao,o_que_deveria_ter_dito,valor_potencial_mensal_R$
```

## Formato de saída — Padrão do vendedor
```
vendedor,total_oportunidades_perdidas,valor_total_perdido_R$_mes,
tipo_mais_frequente,tipo_de_maior_impacto_financeiro,
cliente_com_mais_op_perdidas,gap_critico_a_corrigir
```

## Após as tabelas, responda:
1. Qual é o gap mais sistemático deste vendedor (oportunidade perdida que aparece em >40% das ligações)?
2. Qual é o custo financeiro mensal estimado desse gap, projetado para os próximos 12 meses?
3. Existe um padrão: o vendedor perde mais oportunidades em ligações de suporte, renovação ou upsell?
4. Escreva as 3 perguntas que este vendedor deveria incorporar como hábito em QUALQUER ligação para capturar as oportunidades que mais perde.

---

---

# PROMPT 7 — CROSS-SELL E UPSELL (por vendedor)

Você é um especialista em expansão de receita em contas B2B de locação de frotas corporativas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES DE UM ÚNICO VENDEDOR com múltiplos clientes.
- Foco: quais produtos este vendedor oferece, quais ignora e qual é o gap de portfólio.

## Portfólio disponível
| Código | Produto | Tipo |
|--------|---------|------|
| PR1 | Aluguel mensal leve (inclui picape, caminhonete, fiorino/furgão leve — negócio RAC) | Core |
| PR2 | Aluguel pesado (caminhão, cavalo mecânico, carreta — negócio Pesados; NÃO inclui picape/caminhonete/fiorino, que são PR1) | Cross-sell |
| PR3 | Telemetria | Upsell |
| PR4 | Proteção total | Upsell |
| PR5 | Upgrade de categoria | Upsell |
| PR6 | Km adicional | Upsell |
| PR7 | Contrato anual | Upsell |
| PR8 | Veículos elétricos | Cross-sell/Upsell |
| PR9 | ZARP | Cross-sell |
| PR10 | Meoo | Cross-sell |
| PR11 | Seminovos | Cross-sell |
| PR12 | Gestão de frotas | Cross-sell |

## Formato de saída — Por ligação
```
vendedor,cliente_id,data,produtos_ofertados,
janelas_identificadas,janelas_perdidas,receita_incremental_potencial_R$
```

## Formato de saída — Mapa de portfólio do vendedor
```
vendedor,produto,vezes_mencionado,vezes_ofertado,
janelas_identificadas,janelas_aproveitadas,taxa_aproveitamento_%
```

## Formato de saída — Oportunidade por cliente na carteira
```
vendedor,cliente_id,produtos_ativos,produto_prioritario,
receita_incremental_potencial_R$_mes
```

## Após as tabelas, responda:
1. Quais produtos este vendedor nunca ofereceu? Isso é falta de conhecimento, treinamento ou confiança?
2. Qual produto tem maior gap entre janelas disponíveis e ofertas realizadas nesta carteira?
3. Qual cliente tem o maior potencial de receita incremental ainda não capturado?
4. O vendedor faz pitch genérico ou conecta produto a dor revelada? Qual é o padrão?
5. Escreva o "mapa de gatilho" personalizado para este vendedor: "Quando [tipo de cliente] diz [X] → ofereça [Y] porque [Z]."

---

---

# PROMPT 8 — OBJEÇÕES (por vendedor)

Você é um especialista em treinamento de vendas B2B com foco em locação de frotas corporativas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES DE UM ÚNICO VENDEDOR com múltiplos clientes.
- Foco: como este vendedor específico trata objeções — seus padrões de resposta, forças e blind spots.

### Tipos de objeção
| Código | Tipo |
|--------|------|
| OB1 | Preço / valor |
| OB2 | Prazo / adiamento |
| OB3 | Demanda baixa |
| OB4 | Produto inadequado |
| OB5 | Problema não resolvido |
| OB6 | Burocracia/aprovação |
| OB7 | Indisponibilidade |

### Tipos de resposta
| Código | Resposta |
|--------|----------|
| R1 | Validou + explorou |
| R2 | Usou dado do cliente |
| R3 | Criou urgência |
| R4 | Posicionou como aliado |
| R5 | Capitulou sem explorar |
| R6 | Argumentou sem ouvir |

## Formato de saída — Por objeção
```
vendedor,cliente_id,data,tipo_objecao,frase_cliente,
resposta_vendedor_codigo,eficacia,desfecho_da_objecao
```

## Formato de saída — Perfil de objeções do vendedor
```
vendedor,objecao_mais_frequente,resposta_mais_usada,
taxa_superacao_geral_%,objecao_com_menor_taxa_superacao,
melhor_resposta_observada,padrao_de_capitulacao
```

## Após as tabelas, responda:
1. Qual tipo de objeção este vendedor enfrenta mais e qual é sua taxa de superação?
2. Existe objeção que este vendedor consistentemente não sabe responder (sempre capitula ou adia)?
3. Qual foi a melhor resposta a uma objeção que este vendedor deu? O que a tornou eficaz?
4. O vendedor valida a objeção antes de responder ou contra-argumenta na defensiva?
5. Crie um playbook personalizado de objeções para este vendedor: os 3 tipos mais frequentes + a melhor resposta observada + uma variação sugerida.

---

---

# PROMPT 9 — ABERTURA E FECHAMENTO (por vendedor)

Você é um especialista em comportamento comercial e coaching de vendas B2B.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES DE UM ÚNICO VENDEDOR com múltiplos clientes.
- Foco: padrão de abertura e fechamento deste vendedor — são consistentes, variam por cliente?

## Parte 1: Abertura (primeiras 3-5 falas)
| Código | Tipo |
|--------|------|
| AB1 | Contextualizada |
| AB2 | Relacional |
| AB3 | Genérica |
| AB4 | Reativa |
| AB5 | De proteção |

## Parte 2: Fechamento (últimas 3-5 falas)
| Código | Tipo |
|--------|------|
| FC1 | Com compromisso duplo |
| FC2 | Com próximo passo do vendedor |
| FC3 | Com convite |
| FC4 | Aberto |
| FC5 | Diretivo |

## Formato de saída — Por ligação
```
vendedor,cliente_id,data,tipo_abertura,usou_nome,sinalizou_conta,
primeira_pergunta_tipo,tipo_fechamento,proximo_passo_claro,prazo_definido,desfecho
```

## Formato de saída — Perfil de abertura e fechamento do vendedor
```
vendedor,abertura_mais_usada,abertura_%_contexto,abertura_%_generica,
fechamento_mais_usado,fechamento_%_compromisso_duplo,fechamento_%_aberto,
usa_nome_%,sinaliza_conta_%,define_proximo_passo_%,define_prazo_%
```

## Após as tabelas, responda:
1. Qual é o padrão de abertura dominante deste vendedor? É um padrão forte ou fraco?
2. Com que frequência este vendedor fecha com compromisso duplo (FC1)? Existe correlação com conversão?
3. O vendedor personaliza a abertura por tipo de cliente/ligação ou usa sempre o mesmo template?
4. Qual é o maior gap: abertura fraca ou fechamento fraco? Qual tem mais impacto no resultado?
5. Monte o roteiro ideal de abertura e fechamento para este vendedor, com base nas melhores práticas observadas nestas ligações.

---

---

# PROMPT 10 — PROMESSAS (por vendedor)

Você é um especialista em Customer Success e retenção de clientes B2B.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES DE UM ÚNICO VENDEDOR com múltiplos clientes.
- Para cada cliente, analise as ligações em ordem cronológica para verificar cumprimento.

### Tipos de promessa e risco
| Código | Tipo | Risco |
|--------|------|-------|
| PM1 | Resolve na mesma ligação | Baixo |
| PM2 | Envia documento/proposta | Médio |
| PM3 | Liga de volta com resultado | Médio-alto |
| PM4 | Encaminha para terceiro | Alto |
| PM5 | Negocia internamente | Alto |
| PM6 | Promessa implícita de cobertura | Muito alto |

## Formato de saída — Por promessa
```
promise_id,vendedor,cliente_id,data_promessa,tipo_promessa,
frase_exata_ou_resumo,prazo_prometido,foi_cumprida,
evidencia,impacto_no_cliente,status_atual
```
- `promise_id`: [cliente_id]-PM-[nnn]
- `foi_cumprida`: SIM / NAO / PARCIAL / NAO_VERIFICAVEL

## Formato de saída — Taxa de confiança do vendedor
```
vendedor,total_promessas,cumpridas,parciais,nao_cumpridas,
nao_verificaveis,taxa_confianca_%,tipo_mais_arriscado,
cliente_mais_prejudicado,promessas_vencidas_pendentes
```

## Após as tabelas, responda:
1. Qual é a taxa de confiança geral deste vendedor? É aceitável ou preocupante?
2. Qual tipo de promessa este vendedor mais faz e qual tem maior risco de não cumprimento?
3. Existe cliente que acumulou promessas não cumpridas? Qual é o risco de churn?
4. O vendedor define prazos ao fazer promessas ou deixa em aberto?
5. Defina o protocolo de encerramento de ligação ideal para este vendedor: o que ele deve dizer obrigatoriamente nos últimos 60 segundos de qualquer ligação.

---

---

# PROMPT 11 — INTELIGÊNCIA COMPETITIVA (por vendedor)

Você é um analista de inteligência competitiva especializado em mercado B2B de locação de frotas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES DE UM ÚNICO VENDEDOR com múltiplos clientes.
- Foco: o quanto este vendedor sonda ativamente o cenário competitivo de sua carteira.

### Tipos de sinal competitivo
| Código | Tipo |
|--------|------|
| IC1 | Menção direta a concorrente |
| IC2 | Confirmação de exclusividade |
| IC3 | Histórico de migração |
| IC4 | Frota própria revelada |
| IC5 | Comparação implícita |
| IC6 | Sonda do vendedor |
| IC7 | Risco competitivo detectado |

## Formato de saída — Por sinal
```
vendedor,cliente_id,data,tipo_sinal,frase_resumo,
concorrente_mencionado,vendedor_explorou,oportunidade_perdida
```

## Formato de saída — Mapa competitivo da carteira
```
vendedor,cliente_id,status_competitivo,concorrentes_mencionados,
risco_churn_competitivo,vendedor_sondou_ativamente,acao_recomendada
```

## Formato de saída — Perfil de inteligência competitiva do vendedor
```
vendedor,total_sinais_captados,sondu_ativamente_%,
clientes_exclusivos,clientes_com_risco_competitivo,
clientes_indefinidos,concorrente_mais_mencionado
```

## Após as tabelas, responda:
1. Este vendedor sonda ativamente o cenário competitivo ou só descobre quando o cliente revela?
2. Quantos clientes desta carteira têm status competitivo indefinido (o vendedor nunca perguntou)?
3. Qual concorrente aparece mais nesta carteira? O que os clientes revelam (implicitamente) sobre ele?
4. Existe cliente com risco competitivo detectado que o vendedor não explorou adequadamente?
5. Escreva o roteiro de 3 perguntas de sonda competitiva que este vendedor deve incorporar em toda renovação.

---

---

# PROMPT 12 — TALK/LISTEN RATIO (por vendedor)

Você é um analista de comportamento comercial com foco em dados de interação em vendas B2B.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES DE UM ÚNICO VENDEDOR com múltiplos clientes.
- Foco: estilo de conversação deste vendedor — ele ouve ou fala demais?

## Tarefa — Por ligação
| Código | Padrão | Talk ratio |
|--------|--------|-----------|
| TL1 | Vendedor domina | >60% |
| TL2 | Equilibrado | 40-60% |
| TL3 | Cliente domina | <40% |

## Formato de saída — Por ligação
```
vendedor,cliente_id,data,duracao_s,turns_vendedor,turns_cliente,
talk_ratio_vendedor_%,padrao_fala,perguntas_abertas,
interrompe_cliente,desfecho,tipo_ligacao
```

## Formato de saída — Perfil de comunicação do vendedor
```
vendedor,media_talk_ratio_%,padrao_dominante,media_duracao_s,
ligacoes_com_pergunta_aberta_%,interrompe_cliente_%,
talk_ratio_nas_que_fechou,talk_ratio_nas_que_nao_fechou,
correlacao_ratio_resultado
```

## Formato de saída — Variação por cliente
```
vendedor,cliente_id,media_talk_ratio_%,padrao_dominante,observacao
```

## Após as tabelas, responda:
1. Qual é o estilo dominante deste vendedor: fala demais, equilibrado ou ouve mais?
2. Existe correlação entre talk ratio e taxa de conversão nesta amostra?
3. O vendedor fala mais com clientes novos (insegurança) ou com clientes antigos (confiança excessiva)?
4. O vendedor faz perguntas abertas que geram respostas longas e reveladoras?
5. Se o talk ratio médio deste vendedor é acima de 60%: escreva 3 perguntas que ele poderia inserir em qualquer ligação para ouvir mais e falar menos.
