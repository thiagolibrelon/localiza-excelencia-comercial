# Prompts de Análise — Ligações Localiza
**Como usar:** Cole o prompt desejado no ChatGPT e anexe/cole o conteúdo do arquivo `para_gpt.txt`.
Cada prompt é independente — rode um de cada vez sobre as mesmas transcrições.

**Índice de prompts:**
1. Conversão — o que gera fechamento
2. Tipo de ligação — classificação por natureza da chamada
3. Problemas recorrentes — mapeamento de gargalos sistêmicos
4. Health score — qualidade e risco de cada conta
5. Comportamentos Challenger — quando o vendedor ensina algo ao cliente
6. Oportunidades perdidas — onde o vendedor poderia ter agido
7. Cross-sell e Upsell — portfólio completo vs. o que foi ofertado
8. Objeções — como o cliente resistiu e o vendedor respondeu
9. Abertura e fechamento — como a ligação começa e termina
10. Promessas — o que foi prometido e o que foi entregue
11. Inteligência competitiva — o que os clientes revelaram sobre concorrentes
12. Talk/listen ratio — quem fala mais e o que isso impacta

---

---

# PROMPT 1 — CONVERSÃO
## O que o vendedor fala que gera fechamento?

---

Você é um analista especializado em comportamento comercial em locação de veículos corporativos.

## Contexto
- Empresa: Localiza (locação de veículos mensais para PJ)
- Vendedor = "A" (Agente), Cliente = "C"
- Transcrições de STT fragmentado — junte turns consecutivos do mesmo speaker para entender o sentido. `<unk>` = palavra inaudível, ignore.
- Não há dados de reserva disponíveis. O desfecho deve ser extraído da própria transcrição.

## Tarefa
Para CADA ligação, classifique nas 3 camadas e retorne uma tabela CSV.

### Camada 1 — Desfecho
- `fechou_novo`: nova locação/contrato que não existia
- `fechou_renovacao`: cliente renovou ou prorrogou contrato existente
- `fechou_upsell`: cliente adicionou produto/serviço que não tinha
- `interessou_nao_fechou`: interesse demonstrado, não concluiu na ligação
- `nao_era_venda`: ligação 100% operacional

### Camada 2 — Intenção de entrada
- `cliente_queria`: cliente ligou com intenção clara de alugar/renovar
- `vendedor_puxou`: vendedor ligou proativamente e abriu o assunto
- `misto`: cliente ligou por outro motivo e vendedor aproveitou para oferecer
- `indefinido`: impossível determinar

### Camada 3 — Comportamentos do vendedor (SIM / NAO / NA)
| Código | Comportamento |
|--------|--------------|
| B1 | Fez pergunta de diagnóstico antes de apresentar produto |
| B2 | Apresentou produto mais caro primeiro (âncora de preço) |
| B3 | Usou dado do histórico do cliente |
| B4 | Avisou o cliente de algo que poderia prejudicá-lo |
| B5 | Tentou upsell conectado a uma dor revelada na ligação |
| B6 | Criou urgência com fato verificável (readequação, bloqueio, disponibilidade) |
| B7 | Disse que vai batalhar internamente pelo cliente |
| B8 | Ligou proativamente (não recebeu) por motivo comercial ou de retenção |
| B9 | Demonstrou conhecimento pessoal do cliente além do contrato |
| B10 | Perguntou se o cliente usa outra empresa ou tem frota própria |

## Formato de saída
Retorne CSV com estas colunas exatas:
```
cliente_id,data,duracao_s,desfecho,intencao_entrada,tentativa_comercial,B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,observacao
```
- `tentativa_comercial`: SIM ou NAO
- `observacao`: 1-2 frases sobre o momento comercial mais relevante

## Após a tabela, responda:
**O que os vendedores que mais converteram fizeram de diferente?**
Organize em: (1) comportamentos mais frequentes nos fechamentos, (2) comportamentos ausentes quando não fechou, (3) sequência observada nas ligações que converteram, (4) perfil do cliente que mais responde.

---

---

# PROMPT 2 — TIPO DE LIGAÇÃO
## Qual é a natureza de cada ligação?

---

Você é um analista de operações comerciais em locação de veículos corporativos.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

## Tarefa
Classifique CADA ligação em um tipo principal e um subtipo. Retorne CSV.

### Tipos de ligação
| Tipo | Subtipo (exemplos) |
|------|-------------------|
| `nova_venda` | Primeiro contrato, cotação de nova frota |
| `renovacao` | Prorrogação, novo período de contrato existente |
| `upsell` | Telemetria, proteção, categoria superior, km adicional |
| `retencao` | Queda de volume detectada, risco de churn, cliente menciona concorrente |
| `suporte_operacional` | Portal de faturamento, acesso, sistema, reserva com problema |
| `pos_venda_sinistro` | Acidente, avaria, oficina, franquia de dano |
| `pos_venda_manutencao` | Carro em manutenção, substituto, prazo de reparo |
| `cobranca` | Faturas atrasadas, prorrogação de boleto, bloqueio de frota |
| `onboarding` | Cadastro de condutor, biometria, troca de condutor principal |
| `duvida_contrato` | Multa, km excedente, regras de contrato, diferença mensal vs anual |
| `misto` | Dois ou mais tipos na mesma ligação |
| `sem_conteudo` | Caixa postal, ligação muda, conexão perdida |

### Regras
- Se a ligação mistura suporte + tentativa comercial: tipo = `misto`, subtipo = ambos separados por `+`
- Se o vendedor ao final tentou algo comercial mesmo em ligação de suporte: marque `tentativa_comercial = SIM`

## Formato de saída
```
cliente_id,data,duracao_s,tipo,subtipo,quem_iniciou,tentativa_comercial,observacao
```
- `quem_iniciou`: vendedor / cliente / indefinido
- `observacao`: 1 frase descrevendo o assunto central

## Após a tabela, responda:
1. Qual tipo de ligação é mais frequente nesta base?
2. Em quais tipos o vendedor mais aproveita para tentar algo comercial?
3. Quais tipos têm maior taxa de fechamento?
4. Existe diferença de perfil entre clientes que ligam mais vs. clientes que recebem mais ligações do vendedor?

---

---

# PROMPT 3 — PROBLEMAS RECORRENTES
## Quais problemas aparecem com mais frequência e o que revelam?

---

Você é um analista de Customer Success em locação de veículos corporativos.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

## Tarefa
Identifique CADA problema mencionado ou vivenciado em cada ligação. Um problema pode aparecer em múltiplas ligações do mesmo cliente ou de clientes diferentes. Só marque um código se o problema for tema central ou relevante da ligação — não marque por menção tangencial de 1 palavra-chave sem um problema real por trás dela.

### Categorias de problema
| Código | Categoria | Exemplos |
|--------|-----------|---------|
| P1 | Acesso/sistema | Portal fora do ar, senha, biometria, dois portais distintos |
| P2 | Faturamento/cobrança | Boleto errado, fatura para terceiro, valor incorreto |
| P3 | Multa/infração | Multa no condutor errado, prazo de indicação, contestação |
| P4 | Manutenção/substituto | Carro em oficina, demora, sem substituto disponível |
| P5 | Condutor/cadastro | Troca de condutor, demitido com acesso, habilitação |
| P6 | Km excedente | Cobrança incorreta, plano errado, negociação de desconto |
| P7 | Disponibilidade | Carro reservado indisponível, categoria esgotada |
| P8 | Franquia/agência | Processo diferente em franqueada, fatura não baixada |
| P9 | Sinistro | Acidente, franquia de dano, mudança de oficina |
| P10 | Reserva/sistema | Reserva não aparece no sistema, status incorreto, erro ao criar/editar uma reserva, bug reproduzível do fluxo de reserva. **Não** marcar P10 quando for só dúvida de como navegar/usar o portal sem nenhum erro real (isso é "nenhum", não P10), nem quando o assunto real da ligação for outro (fatura, cadastro, troca de contato comercial) e "reserva" só aparecer de passagem. |
| P11 | Outro | Descrever |
| P12 | Manipulação de pesquisa/NPS | Vendedor pede/dita a nota da pesquisa de satisfação (ex: "as notas boas são 9 e 10", "só ajuda dar nota 9 ou mais") — problema não do cliente, mas de integridade do indicador |

**Nota sobre P12:** diferente das demais categorias, aqui quem "relata" o problema é o próprio comportamento do vendedor, não o cliente — marque `quem_relatou = vendedor_detectou` e `foi_resolvido_na_ligacao = NAO` (não é resolvível na ligação, é um padrão a corrigir em treinamento/gestão). Adicionado em 09/07/2026 após dois casos de coaching explícito de nota encontrados em explorações independentes (ver `analises/AUDITORIA_manipulacao_nps.md`).

## Formato de saída — Parte 1 (por ligação)
```
cliente_id,data,problemas_identificados,quem_relatou,foi_resolvido_na_ligacao,escalou_para,observacao
```
- `problemas_identificados`: lista de códigos separados por `+` (ex: P1+P3)
- `quem_relatou`: cliente / vendedor_detectou
- `foi_resolvido_na_ligacao`: SIM / NAO / PARCIAL
- `escalou_para`: 0800 / supervisora / IT / nao_escalou

## Formato de saída — Parte 2 (consolidado)
Após a tabela por ligação, retorne uma tabela de frequência:
```
codigo,categoria,total_ocorrencias,clientes_afetados,resolvido_na_ligacao_%,escala_%
```

## Após as tabelas, responda:
1. Quais problemas são sistêmicos (aparecem em múltiplos clientes sem relação)?
2. Quais problemas o vendedor resolve sem escalar — e como faz isso?
3. Quais problemas o vendedor escala desnecessariamente (poderia resolver)?
4. Qual problema tem o maior impacto negativo na relação com o cliente?
5. O que o time de produto/operações deveria priorizar para reduzir o volume de chamados?

---

---

# PROMPT 4 — HEALTH SCORE DO CLIENTE
## Qual é a qualidade e o risco de cada conta?

---

Você é um analista de Customer Success especializado em retenção de clientes B2B.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.
- Não há dados de CRM ou reservas disponíveis. Avalie apenas pelos sinais das transcrições.

## Tarefa
Para CADA cliente (não para cada ligação), avalie as 6 dimensões de health score com base em TODOS os sinais encontrados nas transcrições daquele cliente.

### Dimensões de avaliação
| Dimensão | Sinal positivo | Sinal negativo |
|----------|----------------|----------------|
| **Volume** | Frota estável ou crescendo, cliente faz novas reservas | Devoluções sem reposição, cliente menciona redução |
| **Adimplência** | Faturas em dia, sem menção de atraso | Faturas atrasadas, risco de bloqueio |
| **Fidelidade** | Confirma exclusividade, não menciona concorrente | Menciona outra locadora, compara preços |
| **Engajamento** | Responde rápido, acessa portal, solicita NPS | Difícil de contatar, demora para resolver |
| **Complexidade_operacional** | Poucos problemas recorrentes | Múltiplos problemas sistêmicos por ligação |
| **Potencial_upsell** | Frota pequena + empresa crescendo, produto adicional revelado | Frota estagnada, sem abertura para novas ofertas |

### Pontuação por dimensão
- 2 = Positivo (sinais claros de saúde)
- 1 = Neutro (sem sinais claros)
- 0 = Negativo (sinais de risco)

## Formato de saída — Por cliente
```
cliente_id,executivo,total_ligacoes,volume,adimplencia,fidelidade,engajamento,complexidade_operacional,potencial_upsell,score_total,risco_churn,proxima_acao_recomendada
```
- `score_total`: soma das 6 dimensões (0-12)
- `risco_churn`: baixo / médio / alto
- `proxima_acao_recomendada`: 1 frase

## Após a tabela, responda:
1. Qual cliente tem maior risco imediato de churn e por quê?
2. Qual cliente tem maior potencial de crescimento de receita não explorado?
3. Existe correlação entre complexidade operacional alta e risco de churn?
4. Os clientes com mais ligações são os mais saudáveis ou os mais problemáticos?
5. Que sinal nas transcrições é o melhor preditor de churn iminente?

---

---

# PROMPT 5 — COMPORTAMENTOS CHALLENGER
## Quando o vendedor ensina algo ao cliente que muda uma decisão?

---

Você é um especialista em metodologias de vendas B2B, com foco em Challenger Sale aplicado a locação de frotas corporativas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

## O que é um comportamento Challenger
O vendedor **ensina** algo que o cliente não sabia, **adapta** para a realidade do cliente e **toma controle** da conversa — sem que o cliente tenha pedido. Especificamente:
- Revela uma consequência financeira que o cliente não calculou
- Explica uma regra do contrato/produto que muda uma decisão
- Conecta um produto a uma dor que o cliente acabou de revelar
- Antecipa um problema antes que o cliente perceba

## Tarefa
Para CADA ligação, identifique se houve momentos Challenger e classifique.

### Tipos de momento Challenger (neste contexto)
| Código | Tipo | Exemplo |
|--------|------|---------|
| CH1 | Custo oculto revelado | "Se devolver antes do prazo cai em diária e sai o dobro" |
| CH2 | ROI calculado | "O elétrico custa X a mais, mas economiza Y de combustível" |
| CH3 | Urgência por regra real | "A readequação é em março — quem fecha hoje está imune" |
| CH4 | Concorrente/alternativa superada com dado | "Frota própria tem IPVA, seguro, manutenção — locação elimina tudo isso" |
| CH5 | Dor revelada → produto conectado | "Você falou em multa de condutor errado — telemetria resolve exatamente isso" |
| CH6 | Antecipação de problema | "Vi que seu contrato vence em 2 semanas — já deixo renovado para não cair em diária" |
| CH7 | Descoberta de necessidade não declarada | Vendedor pergunta e descobre que cliente tem frota própria, caminhões, etc. |

## Formato de saída — Por ligação
```
cliente_id,data,duracao_s,teve_challenger,codigos_challenger,frase_exata_ou_resumo,resultado_imediato,observacao
```
- `teve_challenger`: SIM / NAO
- `codigos_challenger`: lista de códigos (ex: CH1+CH5)
- `frase_exata_ou_resumo`: transcrição literal ou paráfrase próxima
- `resultado_imediato`: cliente aceitou / cliente refletiu / sem reação visível

## Formato de saída — Por vendedor (consolidado)
```
vendedor,total_ligacoes,ligacoes_com_challenger,taxa_challenger_%,tipos_mais_usados,qualidade_media
```
- `qualidade_media`: alta (cliente aceitou) / média (reflexão) / baixa (sem reação)

## Após as tabelas, responda:
1. Qual vendedor tem o perfil Challenger mais forte?
2. Qual tipo de momento Challenger (CH1-CH7) gera mais aceitação imediata?
3. Existem ligações em que o vendedor DEVERIA ter usado Challenger e não usou? Dê exemplos.
4. O comportamento Challenger acontece mais em ligações proativas (vendedor liga) ou reativas (cliente liga)?
5. Monte um roteiro de 5 passos com os melhores comportamentos Challenger desta base para servir de guia de treinamento.

---

---

# PROMPT 6 — OPORTUNIDADES PERDIDAS
## Onde o vendedor poderia ter agido e não agiu?

---

Você é um coach de vendas B2B especializado em locação de frotas corporativas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

## Definição de oportunidade perdida
Momento em que o vendedor poderia ter:
- Feito uma pergunta que não fez
- Oferecido um produto conectado a uma dor revelada
- Criado urgência que não criou
- Pedido uma indicação
- Explorado um dado revelado pelo cliente (frota própria, outra empresa, plano de expansão)
- Transformado uma ligação de suporte em abertura comercial

## Tarefa
Para CADA ligação, identifique oportunidades perdidas e classifique.

### Tipos de oportunidade perdida
| Código | Tipo | Descrição |
|--------|------|-----------|
| OP1 | Suporte encerrado sem pergunta comercial | Resolveu o problema e desligou sem perguntar nada |
| OP2 | Dor revelada, produto não conectado | Cliente mencionou problema que se encaixa em produto existente |
| OP3 | Fechamento sem urgência | Proposta enviada sem prazo, escassez ou argumento de valor |
| OP4 | Referral não solicitado | Cliente satisfeito, vendedor não pediu indicação |
| OP5 | Dado estratégico não explorado | Cliente revelou frota própria, expansão de empresa, outra locadora |
| OP6 | Upsell óbvio não tentado | Contexto claro para produto adicional, vendedor não ofereceu |
| OP7 | Churn não detectado | Sinais de queda de volume ou insatisfação ignorados |
| OP8 | Escalada desnecessária | Vendedor transferiu para 0800 problema que poderia resolver |

## Formato de saída — Por ligação
```
cliente_id,data,duracao_s,oportunidades_perdidas,descricao_do_que_faltou,o_que_deveria_ter_dito,impacto_estimado
```
- `oportunidades_perdidas`: lista de códigos (ex: OP1+OP4)
- `descricao_do_que_faltou`: 1-2 frases descrevendo o momento específico
- `o_que_deveria_ter_dito`: sugestão de frase/abordagem alternativa
- `impacto_estimado`: alto / médio / baixo

## Formato de saída — Por vendedor (consolidado)
```
vendedor,total_ligacoes,ligacoes_com_op_perdida,taxa_op_perdida_%,tipos_mais_frequentes,observacao
```

## Após as tabelas, responda:
1. Qual vendedor perde mais oportunidades comerciais por ligação?
2. Qual tipo de oportunidade perdida (OP1-OP8) é mais frequente nesta base?
3. Existe algum padrão: o vendedor perde mais oportunidades em ligações de suporte, de cobrança ou de renovação?
4. Qual oportunidade perdida tem maior impacto financeiro potencial?
5. Crie uma lista de 5 "perguntas de fechamento" que os vendedores deveriam ter como hábito ao encerrar QUALQUER ligação, independente do tipo.

---

---

# PROMPT 7 — CROSS-SELL E UPSELL
## O portfólio completo foi explorado? O que ficou na mesa?

---

Você é um especialista em expansão de receita em contas B2B de locação de frotas corporativas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

## Portfólio de produtos disponíveis
| Código | Produto | Tipo |
|--------|---------|------|
| PR1 | Aluguel mensal leve (carros de passeio, picape, caminhonete, fiorino/furgão leve — negócio RAC) | Core |
| PR2 | Aluguel pesado (caminhão, cavalo mecânico, carreta — negócio Pesados; NÃO inclui picape/caminhonete/fiorino, que são PR1) | Cross-sell |
| PR3 | Telemetria (rastreamento em tempo real, ~R$50/mês/veículo) | Upsell |
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
Para CADA ligação, identifique:
1. Produtos mencionados pelo vendedor (com ou sem oferta)
2. Produtos ofertados ativamente pelo vendedor
3. Produtos que tinham janela de oferta e não foram mencionados

### Definição de "janela de oferta"
O cliente disse algo que diretamente se conecta a um produto. Exemplos:
- Menciona multa em condutor errado → janela para PR3 (telemetria) e PR12 (gestão de frotas)
- Menciona que tem veículos próprios → janela para PR2 (pesado) e PR11 (seminovos)
- Tem sinistro com franquia alta → janela para PR4 (proteção)
- Renova mensalmente há mais de 3 meses → janela para PR7 (contrato anual)
- Empresa com perfil sustentável ou redução de custo de combustível → janela para PR8 (elétrico)

## Formato de saída — Por ligação
```
cliente_id,data,duracao_s,produtos_mencionados,produtos_ofertados,janelas_identificadas,janelas_perdidas,o_que_deveria_ter_dito,impacto_estimado
```
- `produtos_mencionados`: códigos separados por `+` (ex: PR1+PR3)
- `produtos_ofertados`: códigos dos produtos que o vendedor ativamente ofereceu
- `janelas_identificadas`: código do produto + gatilho que abriu a janela
- `janelas_perdidas`: janelas que existiam e não foram aproveitadas
- `impacto_estimado`: alto / médio / baixo

## Formato de saída — Por cliente (consolidado)
```
cliente_id,executivo,produtos_ativos,produtos_com_potencial,produto_prioritario,receita_incremental_potencial,observacao
```
- `receita_incremental_potencial`: estimativa qualitativa (ex: "R$50/mês por veículo se fechar telemetria")

## Formato de saída — Por produto (consolidado)
```
produto,codigo,vezes_mencionado,vezes_ofertado,janelas_identificadas,janelas_perdidas,taxa_aproveitamento_%
```

## Após as tabelas, responda:
1. Qual produto tem o maior gap entre janelas disponíveis e ofertas realizadas?
2. Quais clientes têm maior potencial de expansão de receita imediata?
3. Existe algum produto que nunca foi mencionado em nenhuma ligação? O que isso revela?
4. Qual é o perfil de cliente que mais compra cross-sell quando ofertado?
5. Monte um "mapa de produto por situação": para cada tipo de problema ou evento que o cliente menciona, qual produto deveria ser ofertado. Formato: "Quando o cliente diz X → ofereça Y porque Z."

---

---

# PROMPT 8 — OBJEÇÕES
## Como o cliente resistiu e como o vendedor respondeu?

---

Você é um especialista em treinamento de vendas B2B com foco em locação de frotas corporativas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

## O que é uma objeção neste contexto
Qualquer momento em que o cliente resistiu, adiou, recusou ou colocou condição para avançar. Inclui objeções explícitas ("não quero") e implícitas ("vou pensar", "aguarda", "não sei").

### Tipos de objeção
| Código | Tipo | Exemplos |
|--------|------|---------|
| OB1 | Preço / valor | "Tá caro", "precisa de desconto", "concorrente cobra menos" |
| OB2 | Prazo / adiamento | "Semana que vem", "vou pensar", "aguarda aprovação" |
| OB3 | Demanda baixa | "Não preciso agora", "operação reduziu", "é sazonalidade" |
| OB4 | Produto inadequado | "Não tem o que preciso", "não atende minha operação" |
| OB5 | Problema não resolvido | "Vocês erraram", "esse erro foi de vocês", "enquanto não resolver não fecho" |
| OB6 | Burocracia/aprovação | "Precisa do financeiro", "meu cliente não aprovou ainda" |
| OB7 | Indisponibilidade | "Não tenho tempo", "fala com outro" |

### Tipos de resposta do vendedor
| Código | Resposta | Descrição |
|--------|----------|-----------|
| R1 | Validou + explorou | "Entendo. O que está por trás disso?" |
| R2 | Usou dado do cliente | "Mas o seu histórico mostra que..." |
| R3 | Criou urgência | "Se esperarmos, o preço pode mudar em março." |
| R4 | Posicionou como aliado | "Deixa eu resolver isso internamente para você." |
| R5 | Capitulou sem explorar | Aceitou sem perguntar o que estava por trás |
| R6 | Argumentou sem ouvir | Respondeu antes de entender a objeção completa |

## Formato de saída — Por objeção identificada
```
cliente_id,data,tipo_objecao,frase_cliente,resposta_vendedor_codigo,frase_vendedor,eficacia,desfecho_da_objecao,observacao
```
- `eficacia`: alta / média / baixa
- `desfecho_da_objecao`: superada / adiada / perdida

## Formato de saída — Consolidado por tipo
```
tipo_objecao,total_ocorrencias,resposta_mais_usada,taxa_superacao_%,melhor_resposta_observada
```

## Após as tabelas, responda:
1. Qual tipo de objeção é mais frequente nesta base?
2. Qual resposta do vendedor tem a maior taxa de superação?
3. Existe objeção que nenhum vendedor soube responder bem?
4. O que os melhores vendedores fazem diferente na primeira frase após uma objeção?
5. Monte um playbook de objeções: para cada tipo (OB1-OB7), a melhor resposta observada na base + uma variação sugerida.

---

---

# PROMPT 9 — ABERTURA E FECHAMENTO
## Como a ligação começa e termina define o que acontece no meio.

---

Você é um especialista em comportamento comercial e coaching de vendas B2B.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

## Tarefa — Parte 1: Abertura
Para CADA ligação, analise as primeiras 3-5 falas do vendedor.

### Classifique a abertura em:
| Código | Tipo | Descrição |
|--------|------|-----------|
| AB1 | Contextualizada | Vendedor diz por que está ligando antes de pedir atenção |
| AB2 | Relacional | Começa com vínculo pessoal, pergunta sobre o cliente |
| AB3 | Genérica | "Em que posso ajudar?" sem contexto |
| AB4 | Reativa | Só responde ao que o cliente traz |
| AB5 | De proteção | Abre antecipando um problema que o cliente ainda não viu |

### Também identifique:
- O vendedor usou o nome do cliente?
- O vendedor sinalizou que consultou a conta antes de ligar?
- A primeira pergunta foi de diagnóstico ou de confirmação?

## Tarefa — Parte 2: Fechamento
Para CADA ligação, analise as últimas 3-5 falas do vendedor.

### Classifique o fechamento em:
| Código | Tipo | Descrição |
|--------|------|-----------|
| FC1 | Com compromisso duplo | Define o que o vendedor vai fazer E o que o cliente vai fazer, com prazo |
| FC2 | Com próximo passo do vendedor | Só define ação do vendedor (sem prazo do cliente) |
| FC3 | Com convite | "Se precisar, me chama" — sem próximo passo definido |
| FC4 | Aberto | Encerra sem definir nada |
| FC5 | Diretivo | Dá instrução clara ao cliente ("não paga essa fatura ainda") |

## Formato de saída — Por ligação
```
cliente_id,data,duracao_s,tipo_abertura,usou_nome,sinalizou_conta,primeira_pergunta_tipo,tipo_fechamento,proximo_passo_claro,prazo_definido,desfecho,observacao
```
- `primeira_pergunta_tipo`: diagnóstico / confirmação / nenhuma
- `proximo_passo_claro`: SIM / NAO
- `prazo_definido`: SIM / NAO

## Formato de saída — Por vendedor (consolidado)
```
vendedor,abertura_mais_usada,fechamento_mais_usado,usa_nome_%,sinaliza_conta_%,define_proximo_passo_%,define_prazo_%
```

## Após as tabelas, responda:
1. Qual vendedor tem o padrão de abertura mais forte? Por quê?
2. Qual vendedor tem o fechamento mais fraco? O que isso custa em conversão?
3. Existe correlação entre tipo de abertura e tipo de desfecho?
4. Existe correlação entre fechamento com prazo definido e taxa de conversão?
5. Monte um roteiro de abertura e fechamento padrão para este time, baseado nas melhores práticas observadas nesta base.

---

---

# PROMPT 10 — PROMESSAS
## O que o vendedor prometeu e o que realmente entregou?

---

Você é um especialista em Customer Success e retenção de clientes B2B.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.
- Cada cliente tem múltiplas ligações — analise em sequência cronológica para verificar cumprimento.

## O que é uma promessa neste contexto
Qualquer momento em que o vendedor disse (explícita ou implicitamente) que vai fazer algo: resolver, enviar, ligar de volta, encaminhar, verificar, negociar.

### Tipos de promessa
| Código | Tipo | Risco de não-cumprimento |
|--------|------|--------------------------|
| PM1 | Resolve na mesma ligação | Baixo — está feito antes de desligar |
| PM2 | Envia documento/proposta | Médio — depende de prioridade |
| PM3 | Liga de volta com resultado | Médio-alto — fácil de esquecer |
| PM4 | Encaminha para terceiro | Alto — sem visibilidade do que o terceiro fez |
| PM5 | Negocia internamente | Alto — processo longo, cliente aguarda sem prazo |
| PM6 | Promessa implícita de cobertura | Muito alto — nunca formalizada |

## Formato de saída — Por promessa (rastreável entre ligações)
```
cliente_id,data_promessa,tipo_promessa,frase_exata_ou_resumo,data_verificacao,foi_cumprida,evidencia,impacto_no_cliente
```
- `foi_cumprida`: SIM / NAO / PARCIAL / NAO_VERIFICAVEL (sem ligação subsequente)
- `evidencia`: o que aparece na ligação seguinte que confirma ou contradiz
- `impacto_no_cliente`: satisfação / frustração / neutro / churn_risk

## Formato de saída — Por vendedor (consolidado)
```
vendedor,total_promessas,cumpridas,parciais,nao_cumpridas,nao_verificaveis,taxa_confianca_%,tipo_promessa_mais_arriscada
```

## Após as tabelas, responda:
1. Qual vendedor tem a maior taxa de confiança (promessas cumpridas)?
2. Qual tipo de promessa tem maior risco de não-cumprimento nesta base?
3. Existe cliente com histórico de promessas não cumpridas acumuladas? Qual é o risco de churn?
4. Qual é o sinal nas transcrições que indica que uma promessa anterior não foi cumprida?
5. Monte um protocolo de encerramento de ligação que garanta rastreabilidade das promessas: o que o vendedor deve dizer nos últimos 60 segundos de qualquer ligação.

---

---

# PROMPT 11 — INTELIGÊNCIA COMPETITIVA
## O que os clientes revelaram sobre concorrentes e o que foi feito com isso?

---

Você é um analista de inteligência competitiva especializado em mercado B2B de locação de frotas.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- STT fragmentado — junte turns do mesmo speaker. `<unk>` = inaudível, ignore.

## O que buscar
1. Menções diretas a concorrentes (Unidas, Movida, Localfrio, Ouro Verde, outros)
2. Menções a frota própria (cliente tem carro/caminhão próprio)
3. Comparações de preço ou serviço com referência implícita a outra empresa
4. Confirmações de exclusividade com Localiza
5. Histórico de migração (cliente que saiu de outra empresa)
6. Momentos em que o vendedor sondou ativamente sobre concorrentes

### Tipos de sinal competitivo
| Código | Tipo | Exemplos |
|--------|------|---------|
| IC1 | Menção direta a concorrente | "A Unidas me ofereceu X" |
| IC2 | Confirmação de exclusividade | "Só uso a Localiza" |
| IC3 | Histórico de migração | "Saí da Movida faz 6 meses" |
| IC4 | Frota própria revelada | "Tenho 3 caminhões próprios" |
| IC5 | Comparação implícita | "Isso que vocês cobram é caro" (sem citar empresa) |
| IC6 | Sonda do vendedor | Vendedor perguntou diretamente sobre uso de concorrentes |
| IC7 | Risco competitivo detectado | Cliente demonstrou abertura para avaliar alternativas |

## Formato de saída — Por sinal identificado
```
cliente_id,data,tipo_sinal,frase_cliente_ou_vendedor,concorrente_mencionado,vendedor_explorou,como_explorou,oportunidade_perdida,observacao
```
- `vendedor_explorou`: SIM / NAO
- `oportunidade_perdida`: descreva o que poderia ter sido perguntado ou dito

## Formato de saída — Mapa competitivo por cliente
```
cliente_id,status_competitivo,concorrentes_mencionados,exclusividade_confirmada,risco_churn_competitivo,acao_recomendada
```
- `status_competitivo`: exclusivo_localiza / divide_com_concorrente / tem_frota_propria / indefinido

## Após as tabelas, responda:
1. Quais concorrentes aparecem mais frequentemente nestas ligações?
2. Quais clientes têm risco competitivo real e imediato?
3. Quais clientes confirmaram exclusividade — e o que os fidelizou?
4. O que os clientes que saíram de concorrentes revelaram (implicitamente) como motivo da saída?
5. Monte um roteiro de sonda competitiva: 3 perguntas que o vendedor deveria fazer em toda ligação de renovação ou acompanhamento para mapear o cenário competitivo do cliente.

---

---

# PROMPT 12 — TALK/LISTEN RATIO E DURAÇÃO
## Quem fala mais? E duração de chamada tem relação com desfecho?

---

Você é um analista de comportamento comercial com foco em dados de interação em vendas B2B.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- STT diarizado — cada turn é marcado com o speaker. Use a contagem de turns e a extensão das falas para estimar o ratio.
- `<unk>` = inaudível, ignore.

## Tarefa — Parte 1: Talk/Listen Ratio
Para CADA ligação, estime:
- Número de turns do vendedor (A)
- Número de turns do cliente (C)
- Extensão média dos turns de cada um (curto <10 palavras / médio 10-30 / longo >30)
- Talk ratio estimado do vendedor (% do tempo de fala)

### Classifique o padrão de fala do vendedor:
| Código | Padrão | Talk ratio estimado |
|--------|--------|-------------------|
| TL1 | Vendedor domina | >60% |
| TL2 | Equilibrado | 40-60% |
| TL3 | Cliente domina | <40% |

### Também identifique:
- O vendedor faz perguntas abertas (que geram respostas longas do cliente)?
- O vendedor interrompe o cliente?
- Há silêncios funcionais (pausa do vendedor para o cliente pensar)?

## Tarefa — Parte 2: Duração vs. Desfecho
Para CADA ligação, registre:
- Duração em segundos (campo já disponível)
- Tipo de ligação
- Desfecho comercial

## Formato de saída — Por ligação
```
cliente_id,data,duracao_s,turns_vendedor,turns_cliente,talk_ratio_vendedor_%,padrao_fala,perguntas_abertas,interrompe_cliente,desfecho,tipo_ligacao,observacao
```

## Formato de saída — Por vendedor (consolidado)
```
vendedor,media_talk_ratio_%,padrao_dominante,media_duracao_s,ligacoes_com_pergunta_aberta_%,taxa_conversao_estimada_%
```

## Após as tabelas, responda:
1. Existe correlação entre talk ratio do vendedor e taxa de conversão?
2. Existe correlação entre duração da ligação e desfecho?
3. Qual vendedor faz mais perguntas abertas? Isso tem impacto no desfecho?
4. Há diferença de talk ratio entre ligações que converteram vs. que não converteram?
5. Qual é o perfil de ligação ideal (duração + ratio + número de perguntas) baseado nos desfechos mais positivos desta base?
