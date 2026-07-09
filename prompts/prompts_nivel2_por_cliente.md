# Prompts Nível 2 — Por Cliente
**Uso:** Cole o prompt desejado no ChatGPT e anexe TODAS as ligações de UM ÚNICO CLIENTE, ordenadas cronologicamente.
O foco é entender a evolução do relacionamento com este cliente ao longo do tempo.

**Pontos fortes deste nível:**
- P4 (Health Score): uso mais completo — rastreia evolução cronológica
- P10 (Promessas): uso mais completo — verifica cumprimento entre ligações
- P3 (Problemas): identifica se o mesmo problema se repete (first call resolution)
- P9 (Abertura/Fechamento): vê se o padrão do vendedor muda conforme o relacionamento amadurece

**Nota sobre consolidação:** Neste nível não há "por vendedor" — o vendedor é um dado de contexto. A consolidação é sempre cronológica (como o relacionamento com o cliente evoluiu mês a mês).

---

# PROMPT 1 — CONVERSÃO (por cliente)

Você é um analista especializado em comportamento comercial em locação de veículos corporativos.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- Você receberá TODAS AS LIGAÇÕES de um único cliente, ordenadas por data (mais antiga primeiro).
- STT fragmentado — junte turns consecutivos do mesmo speaker. `<unk>` = inaudível, ignore.

## Tarefa
Para CADA ligação, classifique nas 3 camadas e calcule o score comercial.
Depois, analise a evolução do relacionamento ao longo do tempo.

### Camada 1 — Desfecho
- `fechou_novo` / `fechou_renovacao` / `fechou_upsell` / `interessou_nao_fechou` / `nao_era_venda`

### Camada 2 — Intenção de entrada
- `cliente_queria` / `vendedor_puxou` / `misto` / `indefinido`

### Camada 3 — Comportamentos do vendedor (SIM / NAO / NA)
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

## Formato de saída — Evolução cronológica do cliente
```
cliente_id,periodo,total_ligacoes,fechamentos,score_comercial_medio,
comportamento_mais_frequente,tendencia_relacionamento
```
- `periodo`: mês/ano (ex: Jan/2026)
- `tendencia_relacionamento`: crescendo / estavel / deteriorando

## Após as tabelas, responda:
1. Como a relação com este cliente evoluiu ao longo do tempo (primeiras vs. últimas ligações)?
2. Houve algum ponto de inflexão — um momento em que a relação claramente melhorou ou piorou?
3. O vendedor adaptou sua abordagem conforme conhecia melhor o cliente, ou repetiu sempre o mesmo padrão?
4. Quais comportamentos (B1-B10) aparecem consistentemente e quais nunca apareceram?
5. Qual é o estado atual do relacionamento e o que define o próximo capítulo desta conta?

---

---

# PROMPT 2 — TIPO DE LIGAÇÃO (por cliente)

Você é um analista de operações comerciais em locação de veículos corporativos.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES de um único cliente, ordenadas por data.
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

## Tarefa
Classifique cada ligação por tipo. Depois, analise o padrão de interação deste cliente.

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

## Formato de saída — Perfil de interação do cliente
```
cliente_id,total_ligacoes,tipo_mais_frequente,proporcao_comercial_%,
proporcao_suporte_%,ligacoes_iniciadas_pelo_vendedor_%,
ligacoes_iniciadas_pelo_cliente_%,observacao_padrao
```

## Após as tabelas, responda:
1. Este cliente liga mais por problemas ou por necessidades comerciais? O que isso revela?
2. O vendedor liga proativamente ou só responde quando o cliente chama?
3. Existe sazonalidade no padrão de ligações (meses com mais contato, meses de silêncio)?
4. A proporção entre ligações de suporte e comerciais mudou ao longo do tempo?

---

---

# PROMPT 3 — PROBLEMAS RECORRENTES (por cliente)

Você é um analista de Customer Success em locação de veículos corporativos.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES de um único cliente, ordenadas por data.
- Foco: identificar se os mesmos problemas se repetem (falha de First Call Resolution).

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
cliente_id,data,problemas_identificados,foi_resolvido_na_ligacao,escalou_para,observacao
```

## Formato de saída — Histórico de problemas do cliente
```
codigo,categoria,total_ocorrencias,datas_ocorrencias,
resolvido_primeira_vez_%,reincidencia,impacto_acumulado
```
- `reincidencia`: SIM (mesmo problema apareceu em ligações diferentes) / NAO
- `impacto_acumulado`: baixo / médio / alto / crítico

## Após as tabelas, responda:
1. Existe problema que se repete neste cliente sem ser definitivamente resolvido? Quantas vezes?
2. Esse padrão de reincidência cria risco de churn? Em qual dimensão?
3. O vendedor resolveu problemas na ligação ou sempre escalou?
4. Qual problema único, se resolvido definitivamente, mais melhoraria a experiência deste cliente?

---

---

# PROMPT 4 — HEALTH SCORE (por cliente)

Você é um analista de Customer Success especializado em retenção de clientes B2B.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES de um único cliente, ordenadas por data.
- Avalie a evolução do health score ao longo do tempo, não apenas o estado atual.

## Dimensões de avaliação
| Dimensão | Sinal positivo | Sinal negativo |
|----------|----------------|----------------|
| **Volume** | Frota crescendo, novas reservas | Devoluções sem reposição |
| **Adimplência** | Faturas em dia | Atraso, risco de bloqueio |
| **Fidelidade** | Confirma exclusividade | Menciona concorrente |
| **Engajamento** | Responde rápido, acessa portal | Difícil contato, demora |
| **Complexidade_operacional** | Poucos problemas | Múltiplos problemas por ligação |
| **Potencial_upsell** | Empresa crescendo, abertura | Frota estagnada |

Pontuação: 2 = Positivo | 1 = Neutro | 0 = Negativo

## Formato de saída — Health Score por período
```
cliente_id,executivo,periodo,ligacoes_no_periodo,
volume,adimplencia,fidelidade,engajamento,complexidade_operacional,
potencial_upsell,score_total,variacao_vs_periodo_anterior
```
- `variacao_vs_periodo_anterior`: +N / -N / estável

## Formato de saída — Estado atual e trajetória
```
cliente_id,score_atual,tendencia,risco_churn,
sinal_mais_preocupante,sinal_mais_positivo,
dias_sem_contato_proativo,alerta_imediato,proxima_acao_recomendada
```
- `tendencia`: subindo / estavel / caindo
- `alerta_imediato`: SIM se score ≤ 6 ou tendência caindo + risco alto

## Após as tabelas, responda:
1. Em que momento o health score atingiu o pico e o vale? O que aconteceu?
2. Qual dimensão é mais volátil neste cliente (oscila mais)?
3. Qual dimensão é estruturalmente fraca (nunca passou de 1)?
4. Se o score está caindo: quando começou e o que o vendedor poderia ter feito diferente?
5. Qual é a ação mais urgente nos próximos 3 dias úteis?

---

---

# PROMPT 5 — COMPORTAMENTOS CHALLENGER (por cliente)

Você é um especialista em metodologias de vendas B2B, com foco em Challenger Sale aplicado a locação de frotas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES de um único cliente, ordenadas por data.
- Foco: como o nível de sofisticação da abordagem do vendedor evoluiu com este cliente.

### Tipos de momento Challenger
| Código | Tipo |
|--------|------|
| CH1 | Custo oculto revelado |
| CH2 | ROI calculado |
| CH3 | Urgência por regra real |
| CH4 | Concorrente/alternativa superada com dado |
| CH5 | Dor revelada → produto conectado |
| CH6 | Antecipação de problema |
| CH7 | Descoberta de necessidade não declarada |

## Formato de saída — Por ligação
```
cliente_id,data,teve_challenger,codigos_challenger,
frase_exata_ou_resumo,resultado_imediato
```

## Formato de saída — Evolução Challenger com este cliente
```
cliente_id,periodo,ligacoes_com_challenger,taxa_challenger_%,
tipos_usados,qualidade_media,evolucao_vs_periodo_anterior
```

## Após as tabelas, responda:
1. O vendedor aumentou ou diminuiu o uso de Challenger conforme o relacionamento avançou?
2. Quais tipos de Challenger (CH1-CH7) funcionaram melhor com este cliente específico?
3. O cliente responde bem a ensinamentos do vendedor ou resiste? Qual é o padrão de reação?
4. Há momentos nas ligações em que o vendedor claramente DEVERIA ter usado Challenger e não usou?
5. Qual seria o argumento Challenger mais adequado para a próxima ligação com este cliente?

---

---

# PROMPT 6 — OPORTUNIDADES PERDIDAS (por cliente)

Você é um coach de vendas B2B especializado em locação de frotas corporativas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES de um único cliente, ordenadas por data.
- Foco: padrão de oportunidades perdidas ao longo do relacionamento com este cliente.

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

### Tabela de valor potencial por produto
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
cliente_id,data,oportunidades_perdidas,descricao,
o_que_deveria_ter_dito,valor_potencial_mensal_R$
```

## Formato de saída — Acumulado deste cliente
```
cliente_id,total_oportunidades_perdidas,valor_acumulado_perdido_R$_mes,
tipo_mais_frequente,oportunidade_critica_ainda_aberta
```
- `oportunidade_critica_ainda_aberta`: oportunidade que ainda pode ser capturada na próxima ligação

## Após as tabelas, responda:
1. Qual é o valor total de receita mensal que ficou na mesa ao longo de todo o histórico deste cliente?
2. Existe oportunidade perdida que se repete em todas as ligações com este cliente?
3. Qual é a única ação que, se feita na próxima ligação, recuperaria a maior oportunidade ainda aberta?

---

---

# PROMPT 7 — CROSS-SELL E UPSELL (por cliente)

Você é um especialista em expansão de receita em contas B2B de locação de frotas corporativas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES de um único cliente, ordenadas por data.
- Foco: evolução do portfólio ativo deste cliente e oportunidades de expansão.

## Portfólio de produtos disponíveis
| Código | Produto | Tipo |
|--------|---------|------|
| PR1 | Aluguel mensal leve (inclui picape, caminhonete, fiorino/furgão leve — negócio RAC) | Core |
| PR2 | Aluguel pesado (caminhão, cavalo mecânico, carreta — negócio Pesados; NÃO inclui picape/caminhonete/fiorino, que são PR1) | Cross-sell |
| PR3 | Telemetria | Upsell |
| PR4 | Proteção total | Upsell |
| PR5 | Upgrade de categoria | Upsell |
| PR6 | Km adicional / plano maior | Upsell |
| PR7 | Contrato anual | Upsell |
| PR8 | Veículos elétricos | Cross-sell/Upsell |
| PR9 | ZARP | Cross-sell |
| PR10 | Meoo | Cross-sell |
| PR11 | Seminovos | Cross-sell |
| PR12 | Gestão de frotas | Cross-sell |

## Formato de saída — Por ligação
```
cliente_id,data,produtos_mencionados,produtos_ofertados,
janelas_identificadas,janelas_perdidas,receita_incremental_potencial_R$
```

## Formato de saída — Mapa do portfólio deste cliente
```
cliente_id,produtos_ativos_confirmados,produtos_ja_ofertados_e_recusados,
produtos_nunca_ofertados_com_janela,produto_prioritario_para_proxima_ligacao,
receita_incremental_total_potencial_R$_mes
```

## Após as tabelas, responda:
1. Qual produto tem a maior janela ainda não aproveitada neste cliente?
2. Houve produto que foi ofertado e recusado? Por qual objeção? Essa objeção ainda é válida?
3. Como o portfólio deste cliente evoluiu desde a primeira ligação? Cresceu ou estancou?
4. Escreva o pitch de cross-sell ideal para a próxima ligação com este cliente, baseado no que foi revelado ao longo do histórico.

---

---

# PROMPT 8 — OBJEÇÕES (por cliente)

Você é um especialista em treinamento de vendas B2B com foco em locação de frotas corporativas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES de um único cliente, ordenadas por data.
- Foco: padrão de objeções recorrentes deste cliente e como o vendedor as tratou ao longo do tempo.

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
cliente_id,data,tipo_objecao,frase_cliente,resposta_vendedor_codigo,
eficacia,desfecho_da_objecao
```

## Formato de saída — Perfil de objeções deste cliente
```
cliente_id,objecao_mais_frequente,taxa_superacao_historica_%,
melhor_resposta_que_funcionou,objecao_ainda_nao_superada
```

## Após as tabelas, responda:
1. Qual objeção este cliente levanta com mais frequência? É estrutural ou situacional?
2. O vendedor aprendeu a tratar a objeção principal ao longo das ligações, ou repete a mesma abordagem?
3. Qual foi a melhor resposta observada que de fato superou a objeção?
4. Existe objeção que apareceu e nunca foi adequadamente respondida?

---

---

# PROMPT 9 — ABERTURA E FECHAMENTO (por cliente)

Você é um especialista em comportamento comercial e coaching de vendas B2B.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES de um único cliente, ordenadas por data.
- Foco: como o padrão de abertura e fechamento do vendedor evoluiu com este cliente.

## Parte 1: Abertura
| Código | Tipo |
|--------|------|
| AB1 | Contextualizada |
| AB2 | Relacional |
| AB3 | Genérica |
| AB4 | Reativa |
| AB5 | De proteção |

## Parte 2: Fechamento
| Código | Tipo |
|--------|------|
| FC1 | Com compromisso duplo |
| FC2 | Com próximo passo do vendedor |
| FC3 | Com convite |
| FC4 | Aberto |
| FC5 | Diretivo |

## Formato de saída — Por ligação
```
cliente_id,data,tipo_abertura,usou_nome,sinalizou_conta,
primeira_pergunta_tipo,tipo_fechamento,proximo_passo_claro,prazo_definido,desfecho
```

## Formato de saída — Evolução com este cliente
```
cliente_id,abertura_mais_usada,fechamento_mais_usado,
ligacoes_com_proximo_passo_definido_%,ligacoes_com_prazo_definido_%,
evolucao_qualidade_abertura,evolucao_qualidade_fechamento
```
- `evolucao_qualidade`: melhorou / manteve / piorou

## Após as tabelas, responda:
1. O vendedor personalizou as aberturas conforme o relacionamento amadureceu?
2. Existe padrão: quando o fechamento foi FC1 (compromisso duplo), o desfecho foi melhor?
3. O cliente passou a ligar espontaneamente conforme o tempo avançou (sinal de engajamento)?
4. Monte o roteiro ideal de abertura e fechamento para a próxima ligação com este cliente, usando o que já se sabe sobre ele.

---

---

# PROMPT 10 — PROMESSAS (por cliente)

Você é um especialista em Customer Success e retenção de clientes B2B.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES de um único cliente, ORDENADAS CRONOLOGICAMENTE.
- Analise cada promessa feita e verifique se foi cumprida nas ligações subsequentes.

### Tipos de promessa e risco
| Código | Tipo | Risco |
|--------|------|-------|
| PM1 | Resolve na mesma ligação | Baixo |
| PM2 | Envia documento/proposta | Médio |
| PM3 | Liga de volta com resultado | Médio-alto |
| PM4 | Encaminha para terceiro | Alto |
| PM5 | Negocia internamente | Alto |
| PM6 | Promessa implícita de cobertura | Muito alto |

## Formato de saída — Por promessa (rastreável)
```
promise_id,cliente_id,data_promessa,tipo_promessa,frase_exata_ou_resumo,
prazo_prometido,data_verificacao,foi_cumprida,evidencia,impacto_no_cliente,status_atual
```
- `promise_id`: [cliente_id]-PM-[nnn]
- `foi_cumprida`: SIM / NAO / PARCIAL / NAO_VERIFICAVEL
- `status_atual`: cumprida / pendente / vencida / nao_verificavel

## Formato de saída — Confiabilidade do vendedor com este cliente
```
cliente_id,vendedor,total_promessas,cumpridas,parciais,
nao_cumpridas,nao_verificaveis,taxa_confianca_%,
promessas_vencidas_pendentes,risco_relacional
```
- `risco_relacional`: baixo / médio / alto / crítico

## Após as tabelas, responda:
1. Qual é a taxa de confiança do vendedor com este cliente?
2. Existe promessa não cumprida que afetou visivelmente o tom das ligações seguintes?
3. Quais promessas estão vencidas ou pendentes e precisam de ação imediata?
4. O cliente demonstrou frustração ou perda de confiança em algum momento por promessa não cumprida?

---

---

# PROMPT 11 — INTELIGÊNCIA COMPETITIVA (por cliente)

Você é um analista de inteligência competitiva especializado em mercado B2B de locação de frotas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES de um único cliente, ordenadas por data.
- Foco: mapear o cenário competitivo deste cliente e como ele evoluiu.

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
cliente_id,data,tipo_sinal,frase_cliente_ou_vendedor,
concorrente_mencionado,vendedor_explorou,oportunidade_perdida
```

## Formato de saída — Mapa competitivo consolidado deste cliente
```
cliente_id,status_competitivo_atual,concorrentes_mencionados_historico,
exclusividade_confirmada,risco_churn_competitivo,
evolucao_risco_vs_inicio,acao_recomendada
```
- `status_competitivo_atual`: exclusivo_localiza / divide_com_concorrente / tem_frota_propria / indefinido
- `evolucao_risco_vs_inicio`: aumentou / manteve / diminuiu

## Após as tabelas, responda:
1. O risco competitivo com este cliente cresceu ou diminuiu ao longo do histórico?
2. O vendedor sondou ativamente em algum momento ou só descobriu quando o cliente revelou?
3. Existe frota própria ou concorrente que representa oportunidade de expansão para a Localiza?
4. Quais 3 perguntas o vendedor deveria fazer na próxima renovação para atualizar o mapa competitivo?

---

---

# PROMPT 12 — TALK/LISTEN RATIO (por cliente)

Você é um analista de comportamento comercial com foco em dados de interação em vendas B2B.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Você receberá TODAS AS LIGAÇÕES de um único cliente, ordenadas por data.
- Foco: como o padrão de conversação evoluiu ao longo do relacionamento.

## Tarefa — Por ligação
Estime para cada ligação:
- Turns do vendedor (A) e do cliente (C)
- Extensão média dos turns: curto <10 / médio 10-30 / longo >30
- Talk ratio estimado do vendedor (%)

| Código | Padrão | Talk ratio |
|--------|--------|-----------|
| TL1 | Vendedor domina | >60% |
| TL2 | Equilibrado | 40-60% |
| TL3 | Cliente domina | <40% |

## Formato de saída — Por ligação
```
cliente_id,data,duracao_s,turns_vendedor,turns_cliente,
talk_ratio_vendedor_%,padrao_fala,perguntas_abertas,desfecho
```

## Formato de saída — Evolução do padrão com este cliente
```
cliente_id,media_talk_ratio_%,padrao_dominante,
media_duracao_s,evolucao_talk_ratio,
ligacoes_com_pergunta_aberta_%,correlacao_ratio_desfecho
```
- `evolucao_talk_ratio`: vendedor fala mais ou menos com o tempo?
- `correlacao_ratio_desfecho`: nas ligações que fecharam, o ratio era maior ou menor?

## Após as tabelas, responda:
1. O vendedor ouve mais ou menos conforme o relacionamento matura?
2. Existe correlação clara neste cliente entre talk ratio do vendedor e desfecho da ligação?
3. O cliente passou a falar mais ao longo do tempo (sinal de confiança e engajamento)?
4. Qual é o perfil de ligação ideal com este cliente (duração + ratio + perguntas)?
