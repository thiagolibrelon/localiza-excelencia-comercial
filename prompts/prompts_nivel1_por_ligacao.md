# Prompts Nível 1 — Por Ligação
**Uso:** Cole o prompt desejado no ChatGPT e anexe UMA ÚNICA ligação.
Cada análise cobre exatamente 1 ligação. Não há consolidação — o foco é extrair o máximo de uma conversa individual.

**Limitações deste nível:**
- P4 (Health Score): snapshot com dado único — confiança baixa, sinalizado no prompt
- P10 (Promessas): identifica promessas feitas, mas NÃO consegue verificar cumprimento (sem ligação subsequente)
- P11 (Intel. competitiva): só captura sinais presentes nesta ligação
- P12 (Talk ratio): válido, mas sem comparativo com outras ligações do mesmo vendedor

---

# PROMPT 1 — CONVERSÃO (por ligação)

Você é um analista especializado em comportamento comercial em locação de veículos corporativos.

## Contexto
- Empresa: Localiza (locação de veículos mensais para PJ)
- Vendedor = "A" (Agente), Cliente = "C"
- Você receberá UMA ÚNICA ligação para análise.
- STT fragmentado — junte turns consecutivos do mesmo speaker. `<unk>` = inaudível, ignore.
- Não há dados de reserva. O desfecho deve ser extraído da própria transcrição.

## Tarefa
Classifique esta ligação nas 3 camadas e calcule o score comercial.

### Camada 1 — Desfecho
- `fechou_novo`: nova locação/contrato que não existia
- `fechou_renovacao`: cliente renovou ou prorrogou contrato existente
- `fechou_upsell`: cliente adicionou produto/serviço que não tinha
- `interessou_nao_fechou`: interesse demonstrado, não concluiu na ligação
- `nao_era_venda`: ligação 100% operacional

### Camada 2 — Intenção de entrada
- `cliente_queria`: cliente ligou com intenção clara de alugar/renovar
- `vendedor_puxou`: vendedor ligou proativamente e abriu o assunto
- `misto`: cliente ligou por outro motivo e vendedor aproveitou
- `indefinido`: impossível determinar

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

## Formato de saída
```
cliente_id,data,duracao_s,desfecho,intencao_entrada,tentativa_comercial,
B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,score_comercial,observacao
```
- `score_comercial`: soma dos pesos dos comportamentos marcados SIM (máximo 18)
- `observacao`: 2-3 frases sobre o momento comercial mais relevante desta ligação

## Após a tabela, responda:
1. Qual foi o comportamento mais impactante do vendedor nesta ligação?
2. Qual foi a maior oportunidade não aproveitada?
3. Se esta ligação não fechou, o que especificamente impediu?
4. Qual seria a próxima ação recomendada para o vendedor com este cliente?

---

---

# PROMPT 2 — TIPO DE LIGAÇÃO (por ligação)

Você é um analista de operações comerciais em locação de veículos corporativos.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- Você receberá UMA ÚNICA ligação para análise.
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

## Tarefa
Classifique esta ligação em um tipo principal e um subtipo.

### Tipos de ligação
| Tipo | Subtipo (exemplos) |
|------|-------------------|
| `nova_venda` | Primeiro contrato, cotação de nova frota |
| `renovacao` | Prorrogação, novo período de contrato existente |
| `upsell` | Telemetria, proteção, categoria superior, km adicional |
| `retencao` | Queda de volume detectada, risco de churn, cliente menciona concorrente |
| `suporte_operacional` | Portal, acesso, sistema, reserva com problema |
| `pos_venda_sinistro` | Acidente, avaria, oficina, franquia de dano |
| `pos_venda_manutencao` | Carro em manutenção, substituto, prazo de reparo |
| `cobranca` | Faturas atrasadas, boleto, bloqueio de frota |
| `onboarding` | Cadastro de condutor, biometria, troca de condutor |
| `duvida_contrato` | Multa, km excedente, regras, diferença mensal vs anual |
| `misto` | Dois ou mais tipos na mesma ligação |
| `sem_conteudo` | Caixa postal, ligação muda, conexão perdida |

### Regras
- Se mistura suporte + tentativa comercial: tipo = `misto`, subtipo = ambos separados por `+`
- Se o vendedor ao final tentou algo comercial mesmo em ligação de suporte: `tentativa_comercial = SIM`

## Formato de saída
```
cliente_id,data,duracao_s,tipo,subtipo,quem_iniciou,tentativa_comercial,observacao
```
- `quem_iniciou`: vendedor / cliente / indefinido
- `observacao`: 1 frase descrevendo o assunto central

## Após a tabela, responda:
1. Este tipo de ligação é propício para tentativa comercial? Por quê?
2. O vendedor aproveitou ou desperdiçou a abertura comercial disponível nesta ligação?
3. Qual seria o próximo tipo de ligação ideal para este cliente?

---

---

# PROMPT 3 — PROBLEMAS RECORRENTES (por ligação)

Você é um analista de Customer Success em locação de veículos corporativos.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- Você receberá UMA ÚNICA ligação para análise.
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

## Tarefa
Identifique CADA problema mencionado ou vivenciado nesta ligação.

### Categorias de problema
| Código | Categoria | Exemplos |
|--------|-----------|---------|
| P1 | Acesso/sistema | Portal fora do ar, senha, biometria |
| P2 | Faturamento/cobrança | Boleto errado, fatura para terceiro, valor incorreto |
| P3 | Multa/infração | Multa no condutor errado, prazo de indicação |
| P4 | Manutenção/substituto | Carro em oficina, demora, sem substituto |
| P5 | Condutor/cadastro | Troca de condutor, demitido com acesso, habilitação |
| P6 | Km excedente | Cobrança incorreta, plano errado, negociação |
| P7 | Disponibilidade | Carro reservado indisponível, categoria esgotada |
| P8 | Franquia/agência | Processo diferente em franqueada, fatura não baixada |
| P9 | Sinistro | Acidente, franquia de dano, mudança de oficina |
| P10 | Reserva/sistema | Reserva caindo em "sob consulta", status incorreto |
| P11 | Outro | Descrever |

## Formato de saída
```
cliente_id,data,problemas_identificados,quem_relatou,foi_resolvido_na_ligacao,escalou_para,observacao
```
- `problemas_identificados`: lista de códigos separados por `+`
- `quem_relatou`: cliente / vendedor_detectou
- `foi_resolvido_na_ligacao`: SIM / NAO / PARCIAL
- `escalou_para`: 0800 / supervisora / IT / nao_escalou

## Após a tabela, responda:
1. O problema desta ligação tem cara de sistêmico (provavelmente afeta outros clientes) ou pontual?
2. O vendedor resolveu bem ou escalou desnecessariamente?
3. O vendedor tentou algo comercial após resolver o problema?
4. Qual é o impacto deste problema na relação com o cliente (satisfação, confiança, risco de churn)?

---

---

# PROMPT 4 — HEALTH SCORE (por ligação)
**⚠️ ATENÇÃO:** Com apenas 1 ligação, o health score é um snapshot inicial com confiança limitada. Interprete como sinal de tendência, não diagnóstico definitivo.

Você é um analista de Customer Success especializado em retenção de clientes B2B.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- Você receberá UMA ÚNICA ligação para análise.
- Avalie apenas pelos sinais presentes nesta conversa. Reconheça explicitamente quando o dado for insuficiente.

## Dimensões de avaliação
| Dimensão | Sinal positivo | Sinal negativo | Sem sinal |
|----------|----------------|----------------|-----------|
| **Volume** | Frota crescendo, novas reservas | Devolução sem reposição | 1 |
| **Adimplência** | Faturas em dia | Atraso, risco de bloqueio | 1 |
| **Fidelidade** | Confirma exclusividade | Menciona concorrente | 1 |
| **Engajamento** | Responde rápido, acessa portal | Difícil contato, demora | 1 |
| **Complexidade_operacional** | Poucos problemas | Múltiplos problemas nesta ligação | 1 |
| **Potencial_upsell** | Empresa crescendo, abertura para novas ofertas | Frota estagnada, sem abertura | 1 |

Pontuação: 2 = Positivo | 1 = Neutro/sem sinal | 0 = Negativo

## Formato de saída
```
cliente_id,data,volume,adimplencia,fidelidade,engajamento,
complexidade_operacional,potencial_upsell,score_total,
confianca_do_score,risco_churn,sinal_mais_preocupante,proxima_acao
```
- `confianca_do_score`: alta / média / baixa (baseado em quantas dimensões tiveram sinais claros)
- `sinal_mais_preocupante`: a dimensão com maior risco identificada nesta ligação

## Após a tabela, responda:
1. Quais dimensões tiveram sinal claro e quais ficaram sem evidência?
2. Se houvesse uma única ação a fazer com este cliente nas próximas 48h, qual seria?
3. Quais perguntas o vendedor deveria fazer na próxima ligação para completar o diagnóstico das dimensões sem sinal?

---

---

# PROMPT 5 — COMPORTAMENTOS CHALLENGER (por ligação)

Você é um especialista em metodologias de vendas B2B, com foco em Challenger Sale aplicado a locação de frotas corporativas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- Você receberá UMA ÚNICA ligação para análise.
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

## O que é um comportamento Challenger
O vendedor **ensina** algo que o cliente não sabia, **adapta** para a realidade do cliente e **toma controle** da conversa — sem que o cliente tenha pedido.

### Tipos de momento Challenger
| Código | Tipo | Exemplo |
|--------|------|---------|
| CH1 | Custo oculto revelado | "Se devolver antes do prazo cai em diária e sai o dobro" |
| CH2 | ROI calculado | "O elétrico custa X a mais, mas economiza Y de combustível" |
| CH3 | Urgência por regra real | "A readequação é em março — quem fecha hoje está imune" |
| CH4 | Concorrente/alternativa superada com dado | "Frota própria tem IPVA, seguro, manutenção — locação elimina tudo isso" |
| CH5 | Dor revelada → produto conectado | "Você falou em multa de condutor errado — telemetria resolve isso" |
| CH6 | Antecipação de problema | "Vi que seu contrato vence em 2 semanas — já deixo renovado" |
| CH7 | Descoberta de necessidade não declarada | Vendedor pergunta e descobre frota própria, caminhões, etc. |

## Formato de saída
```
cliente_id,data,duracao_s,teve_challenger,codigos_challenger,
frase_exata_ou_resumo,resultado_imediato,qualidade
```
- `teve_challenger`: SIM / NAO
- `resultado_imediato`: cliente_aceitou / cliente_refletiu / sem_reacao_visivel
- `qualidade`: alta / média / baixa

## Após a tabela, responda:
1. O vendedor usou Challenger nesta ligação? Qual foi o momento mais forte?
2. Houve momento em que o vendedor DEVERIA ter usado Challenger e não usou? Descreva o que faltou.
3. Se o vendedor não usou nenhum comportamento Challenger: qual seria o ideal para esta ligação específica?
4. O resultado imediato (cliente aceitou/refletiu) indica que o Challenger funcionou? Por quê?

---

---

# PROMPT 6 — OPORTUNIDADES PERDIDAS (por ligação)

Você é um coach de vendas B2B especializado em locação de frotas corporativas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- Você receberá UMA ÚNICA ligação para análise.
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

## Definição de oportunidade perdida
Momento em que o vendedor poderia ter feito algo comercial e não fez.

### Tipos
| Código | Tipo | Descrição |
|--------|------|-----------|
| OP1 | Suporte encerrado sem pergunta comercial | Resolveu o problema e desligou sem perguntar nada |
| OP2 | Dor revelada, produto não conectado | Cliente mencionou problema que se encaixa em produto existente |
| OP3 | Fechamento sem urgência | Proposta enviada sem prazo, escassez ou argumento de valor |
| OP4 | Referral não solicitado | Cliente satisfeito, vendedor não pediu indicação |
| OP5 | Dado estratégico não explorado | Cliente revelou frota própria, expansão, outra locadora |
| OP6 | Upsell óbvio não tentado | Contexto claro para produto adicional, vendedor não ofereceu |
| OP7 | Churn não detectado | Sinais de queda de volume ou insatisfação ignorados |
| OP8 | Escalada desnecessária | Transferiu para 0800 problema que poderia resolver |

### Tabela de valor potencial por produto
| Produto | Receita mensal estimada |
|---------|------------------------|
| PR3 (Telemetria) | R$ 50/veículo |
| PR4 (Proteção) | R$ 80/veículo |
| PR7 (Contrato anual) | R$ 200 (retenção de churn) |
| PR8 (Elétrico) | R$ 3.600/veículo |
| PR9 (ZARP/Meoo) | R$ 300/contrato |
| Referral convertido | R$ 500 (LTV 12 meses) |

## Formato de saída
```
cliente_id,data,duracao_s,oportunidades_perdidas,descricao_do_que_faltou,
o_que_deveria_ter_dito,valor_potencial_mensal_R$
```
- `oportunidades_perdidas`: lista de códigos (ex: OP1+OP4)
- `valor_potencial_mensal_R$`: estimativa em R$ se a ação tivesse sido tomada

## Após a tabela, responda:
1. Qual foi a maior oportunidade perdida desta ligação em termos de impacto financeiro?
2. Escreva a frase exata que o vendedor deveria ter dito no momento da oportunidade perdida mais relevante.
3. Esta ligação teve mais oportunidades perdidas do que o esperado para este tipo de chamada? Por quê?

---

---

# PROMPT 7 — CROSS-SELL E UPSELL (por ligação)

Você é um especialista em expansão de receita em contas B2B de locação de frotas corporativas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- Você receberá UMA ÚNICA ligação para análise.
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

## Portfólio de produtos disponíveis
| Código | Produto | Tipo |
|--------|---------|------|
| PR1 | Aluguel mensal leve (inclui picape, caminhonete, fiorino/furgão leve — negócio RAC) | Core |
| PR2 | Aluguel pesado (caminhão, cavalo mecânico, carreta — negócio Pesados; NÃO inclui picape/caminhonete/fiorino, que são PR1) | Cross-sell |
| PR3 | Telemetria (~R$50/mês/veículo) | Upsell |
| PR4 | Proteção total / cobertura de avarias | Upsell |
| PR5 | Upgrade de categoria de veículo | Upsell |
| PR6 | Km adicional / plano de km maior | Upsell |
| PR7 | Contrato anual (trava preço por 12 meses) | Upsell |
| PR8 | Veículos elétricos | Cross-sell/Upsell |
| PR9 | ZARP | Cross-sell |
| PR10 | Meoo | Cross-sell |
| PR11 | Venda de Seminovos | Cross-sell |
| PR12 | Gestão de frotas | Cross-sell |

## Tarefa
Identifique nesta ligação:
1. Produtos mencionados pelo vendedor
2. Produtos ofertados ativamente
3. Janelas de oferta presentes que não foram aproveitadas

## Formato de saída
```
cliente_id,data,duracao_s,produtos_mencionados,produtos_ofertados,
janelas_identificadas,janelas_perdidas,o_que_deveria_ter_dito,
receita_incremental_potencial_R$
```

## Após a tabela, responda:
1. Qual produto tinha a janela mais óbvia nesta ligação e não foi ofertado?
2. O vendedor fez pitch genérico ou conectou o produto a uma dor revelada?
3. Escreva o script ideal de cross-sell para esta ligação específica, baseado no que o cliente disse.

---

---

# PROMPT 8 — OBJEÇÕES (por ligação)

Você é um especialista em treinamento de vendas B2B com foco em locação de frotas corporativas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- Você receberá UMA ÚNICA ligação para análise.
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

### Tipos de objeção
| Código | Tipo | Exemplos |
|--------|------|---------|
| OB1 | Preço / valor | "Tá caro", "precisa de desconto", "concorrente cobra menos" |
| OB2 | Prazo / adiamento | "Semana que vem", "vou pensar", "aguarda aprovação" |
| OB3 | Demanda baixa | "Não preciso agora", "operação reduziu" |
| OB4 | Produto inadequado | "Não tem o que preciso", "não atende minha operação" |
| OB5 | Problema não resolvido | "Vocês erraram", "enquanto não resolver não fecho" |
| OB6 | Burocracia/aprovação | "Precisa do financeiro", "meu cliente não aprovou" |
| OB7 | Indisponibilidade | "Não tenho tempo", "fala com outro" |

### Tipos de resposta do vendedor
| Código | Resposta |
|--------|----------|
| R1 | Validou + explorou ("Entendo. O que está por trás disso?") |
| R2 | Usou dado do cliente ("Mas o seu histórico mostra que...") |
| R3 | Criou urgência ("Se esperarmos, o preço pode mudar em março") |
| R4 | Posicionou como aliado ("Deixa eu resolver isso internamente") |
| R5 | Capitulou sem explorar (aceitou sem perguntar o que estava por trás) |
| R6 | Argumentou sem ouvir (respondeu antes de entender a objeção completa) |

## Formato de saída — Por objeção identificada
```
cliente_id,data,tipo_objecao,frase_cliente,resposta_vendedor_codigo,
frase_vendedor,eficacia,desfecho_da_objecao
```
- `eficacia`: alta / média / baixa
- `desfecho_da_objecao`: superada / adiada / perdida

## Após a tabela, responda:
1. Qual foi a objeção mais crítica desta ligação?
2. O vendedor respondeu bem ou capitulou? O que faltou?
3. Escreva a resposta ideal para a objeção principal desta ligação.
4. Esta objeção indica um problema do cliente, do produto ou da abordagem do vendedor?

---

---

# PROMPT 9 — ABERTURA E FECHAMENTO (por ligação)

Você é um especialista em comportamento comercial e coaching de vendas B2B.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- Você receberá UMA ÚNICA ligação para análise.
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

## Parte 1: Abertura
Analise as primeiras 3-5 falas do vendedor.

| Código | Tipo | Descrição |
|--------|------|-----------|
| AB1 | Contextualizada | Vendedor diz por que está ligando antes de pedir atenção |
| AB2 | Relacional | Começa com vínculo pessoal, pergunta sobre o cliente |
| AB3 | Genérica | "Em que posso ajudar?" sem contexto |
| AB4 | Reativa | Só responde ao que o cliente traz |
| AB5 | De proteção | Abre antecipando um problema que o cliente ainda não viu |

## Parte 2: Fechamento
Analise as últimas 3-5 falas do vendedor.

| Código | Tipo | Descrição |
|--------|------|-----------|
| FC1 | Com compromisso duplo | Define o que o vendedor E o cliente vão fazer, com prazo |
| FC2 | Com próximo passo do vendedor | Só define ação do vendedor (sem prazo do cliente) |
| FC3 | Com convite | "Se precisar, me chama" — sem próximo passo definido |
| FC4 | Aberto | Encerra sem definir nada |
| FC5 | Diretivo | Dá instrução clara ao cliente ("não paga essa fatura ainda") |

## Formato de saída
```
cliente_id,data,duracao_s,tipo_abertura,usou_nome,sinalizou_conta,
primeira_pergunta_tipo,tipo_fechamento,proximo_passo_claro,prazo_definido,
desfecho,observacao
```
- `primeira_pergunta_tipo`: diagnóstico / confirmação / nenhuma
- `proximo_passo_claro`: SIM / NAO
- `prazo_definido`: SIM / NAO

## Após a tabela, responda:
1. A abertura criou ou destruiu rapport? Por quê?
2. O fechamento garantiu continuidade ou deixou a ligação em aberto?
3. Escreva a abertura e o fechamento ideais para esta ligação, baseados no contexto da conversa.
4. Se a ligação não fechou: o fechamento fraco foi fator determinante?

---

---

# PROMPT 10 — PROMESSAS (por ligação)
**⚠️ ATENÇÃO:** Neste nível, identifica apenas promessas FEITAS nesta ligação. Verificação de cumprimento requer ligação subsequente — use o nível 2 (por cliente) para rastreamento completo.

Você é um especialista em Customer Success e retenção de clientes B2B.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- Você receberá UMA ÚNICA ligação para análise.
- Foco: identificar e classificar cada promessa feita pelo vendedor nesta ligação.

### Tipos de promessa e risco
| Código | Tipo | Risco de não-cumprimento |
|--------|------|--------------------------|
| PM1 | Resolve na mesma ligação | Baixo |
| PM2 | Envia documento/proposta | Médio |
| PM3 | Liga de volta com resultado | Médio-alto |
| PM4 | Encaminha para terceiro | Alto |
| PM5 | Negocia internamente | Alto |
| PM6 | Promessa implícita de cobertura | Muito alto |

## Formato de saída
```
promise_id,cliente_id,data_promessa,tipo_promessa,
frase_exata_ou_resumo,prazo_prometido,risco_nao_cumprimento
```
- `promise_id`: [cliente_id]-PM-[nnn]
- `prazo_prometido`: data específica ou "sem prazo definido"
- `risco_nao_cumprimento`: baixo / médio / alto / muito_alto

## Após a tabela, responda:
1. Quantas promessas foram feitas nesta ligação? O número é razoável?
2. Quais promessas têm maior risco de não serem cumpridas? Por quê?
3. Alguma promessa foi feita sem prazo definido? Qual é o risco para o relacionamento?
4. O que o vendedor deveria ter dito nos últimos 60 segundos para garantir rastreabilidade?

---

---

# PROMPT 11 — INTELIGÊNCIA COMPETITIVA (por ligação)

Você é um analista de inteligência competitiva especializado em mercado B2B de locação de frotas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- Você receberá UMA ÚNICA ligação para análise.
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

### Tipos de sinal competitivo
| Código | Tipo | Exemplos |
|--------|------|---------|
| IC1 | Menção direta a concorrente | "A Unidas me ofereceu X" |
| IC2 | Confirmação de exclusividade | "Só uso a Localiza" |
| IC3 | Histórico de migração | "Saí da Movida faz 6 meses" |
| IC4 | Frota própria revelada | "Tenho 3 caminhões próprios" |
| IC5 | Comparação implícita | "Isso que vocês cobram é caro" |
| IC6 | Sonda do vendedor | Vendedor perguntou diretamente sobre concorrentes |
| IC7 | Risco competitivo detectado | Cliente demonstrou abertura para avaliar alternativas |

## Formato de saída — Por sinal identificado
```
cliente_id,data,tipo_sinal,frase_cliente_ou_vendedor,
concorrente_mencionado,vendedor_explorou,como_explorou,oportunidade_perdida
```

## Mapa competitivo desta ligação
```
cliente_id,status_competitivo,concorrentes_mencionados,
exclusividade_confirmada,risco_churn_competitivo,acao_recomendada
```
- `status_competitivo`: exclusivo_localiza / divide_com_concorrente / tem_frota_propria / indefinido

## Após a tabela, responda:
1. Há risco competitivo real nesta ligação? Qual é a urgência?
2. O vendedor sondou ativamente o cenário competitivo ou esperou o cliente revelar?
3. O que o vendedor deveria ter dito/perguntado para mapear melhor a situação competitiva?

---

---

# PROMPT 12 — TALK/LISTEN RATIO (por ligação)

Você é um analista de comportamento comercial com foco em dados de interação em vendas B2B.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- Você receberá UMA ÚNICA ligação para análise.
- STT diarizado — use contagem de turns e extensão das falas para estimar o ratio.
- `<unk>` = inaudível, ignore.

## Tarefa
Estime para esta ligação:
- Número de turns do vendedor (A)
- Número de turns do cliente (C)
- Extensão média dos turns: curto <10 palavras / médio 10-30 / longo >30
- Talk ratio estimado do vendedor (% do tempo de fala)

### Padrão de fala
| Código | Padrão | Talk ratio estimado |
|--------|--------|-------------------|
| TL1 | Vendedor domina | >60% |
| TL2 | Equilibrado | 40-60% |
| TL3 | Cliente domina | <40% |

### Também identifique:
- O vendedor fez perguntas abertas (que geraram respostas longas do cliente)?
- O vendedor interrompeu o cliente?
- Há silêncios funcionais (pausa para o cliente pensar)?

## Formato de saída
```
cliente_id,data,duracao_s,turns_vendedor,turns_cliente,
talk_ratio_vendedor_%,padrao_fala,perguntas_abertas,
interrompe_cliente,desfecho,observacao
```

## Após a tabela, responda:
1. O talk ratio desta ligação favoreceu ou prejudicou o desfecho?
2. O vendedor fez perguntas que geraram respostas longas e reveladoras do cliente?
3. Se o vendedor dominou: o que ele deveria ter calado para ouvir mais?
4. Qual seria o talk ratio ideal para este tipo de ligação específica?
