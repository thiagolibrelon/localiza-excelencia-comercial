# Lote 02 (novo lote, 5.348) — Exploração P4+P8+P11+P13+P14+P15

## Resumo
- Total de ligações no lote: 38
- Vendedores identificados neste lote: Bruna (Localiza Empresas — várias ligações, possivelmente mais de uma pessoa), Ramiro, Thais, Luma, Amanda, Matheus, Tatiana, Carla Cunha, Camila Andrade, Cristina, Brenda, Andresa, Flávia, Talita, Juliana, Isaías, Vitor, Lucas, João Paulo, Gabriel, Fabrício, Paulo Faustino, Tanita, Gabriela, Fabrisa(?) + 2 vendedores sem nome claro (homem de BH na lig. do Cliente 27170310; executivo RAC na lig. do Cliente 07997963)

## P4 — Health Score (por cliente, só os que têm sinal claro)
| Cliente | Volume | Adimplência | Fidelidade | Engajamento | Complex.Operacional | Potencial Upsell | Score Total (0-12) | Risco Churn |
|---|---|---|---|---|---|---|---|---|
| 12224630 | 2 | 1 | 2 | 2 | 2 | 2 | 11 | Baixo |
| 19781049 | 2 | 1 | 2 | 2 | 1 | 2 | 10 | Baixo |
| 07997963 | 2 | 1 | 1 | 2 | 2 | 2 | 10 | Médio (RAC já com Movida) |
| 01574802 | 1 | 1 | 2 | 2 | 1 | 2 | 9 | Baixo (retorno previsto H2) |
| 25242238 | 2 | 0 | 2 | 1 | 1 | 2 | 8 | Médio (2 faturas atrasadas) |
| 16715835 | 1 | 1 | 1 | 2 | 2 | 1 | 8 | Baixo |
| 11390532 | 2 | 1 | 1 | 2 | 1 | 1 | 8 | Médio (insatisfação acumulada) |
| 27170310 | 1 | 0 | 2 | 2 | 1 | 1 | 7 | Baixo-médio (limite de crédito estourado) |
| 22808555 | 1 | 1 | 0 | 1 | 0 | 2 | 5 | Médio (hoje na Movida; win-back aberto) |
| 27304203 | 1 | 1 | 0 | 1 | 0 | 1 | 4 | Alto (cotando Movida 42% mais barata) |
| 27285095 | 0 | 1 | 0 | 0 | 1 | 0 | 2 | Alto (desistiu da PJ, foi ao balcão PF) |

## P8 — Objeções (tabela de frequência)
| Tipo | Ocorrências | Resposta mais usada | Eficácia predominante | Melhor exemplo observado |
|---|---|---|---|---|
| OB3 Demanda baixa | 7 (01577908, 21917231, 23944469, 23949612, 01574802, 17449341, 27319935) | R1 (validou e explorou causa: obras paradas, frota própria, sazonalidade) | Média (mantém cadastro vivo, sem conversão imediata) | Cliente 01574802: vendedor validou a pausa e extraiu pipeline concreto (2 obras no H2) |
| OB1 Preço/valor | 5 (19781049, 27304203, 11390532, 25242238, 27170310) | R2 (usou dado: reajuste em sistema, melhor NPC já aplicado) + R3 pontual | Média-alta | Cliente 19781049: Thais explicou reajuste de 15/06 com datas e valores, criou urgência legítima ("reserve para travar preço, cancelamento PJ sem taxa") — superada |
| OB6 Burocracia/aprovação | 4 (16715835, 23939662, 12224630, 27170310) | R1/R4 (explicou fluxo e ofereceu caminhos alternativos) | Alta | Cliente 16715835: Amanda consultou a Receita Federal em tempo real para validar sócio-administrador e destravou aprovação de 3 reservas |
| OB2 Prazo/adiamento | 4 (27333335, 26026315, 17086344, 21126648) | Agendou retorno com data/hora (sem exploração — próximo de R5) | Baixa-média | Cliente 21126648: Brenda formalizou proposta no WhatsApp e marcou retorno para terça (única com follow-up estruturado) |
| OB5 Problema não resolvido | 2 (27285095, 11390532) | R6 (argumentou sem acolher a frustração) | Baixa | Cliente 27285095: bloqueio de condutor sem motivo (LGPD) — vendedora insistiu no procedimento e cliente abandonou a reserva PJ — perdida |
| OB7 Indisponibilidade | 1 (11390532) | R1 (substituiu Strada por Montana, mesma categoria) | Média | Cliente 11390532: orientou ligar na central para tentar manter versão High Line |

## P11 — Inteligência competitiva (tabela de frequência)
| Tipo | Ocorrências | Concorrentes citados | Vendedor explorou (SIM/NAO — contagem) |
|---|---|---|---|
| IC1 Menção direta | 3 (07997963, 27304203, 22808555) | Movida (única citada, 3x) | SIM: 3 / NAO: 0 |
| IC5 Comparação implícita/explícita de preço | 2 (27304203: Movida R$2.890 vs Localiza R$4.933; 07997963: "a Movida está imbatível") | Movida | SIM: 2 (Bruna recotou grupo mais barato; executivo ofereceu cashback R$200) |
| IC4 Frota própria revelada | 4 (27319935, 01574802, 17449341, 21917231) | — | SIM: 3 / NAO: 1 |
| IC3 Histórico de migração | 1 (22808555 — migrou para carro por assinatura Movida) | Movida | SIM: 1 (Tatiana reativou com cotação 12 meses) |
| IC6 Vendedor sondou concorrência | 2 (01574802 "seguiu com outra locadora?"; 27304203 perguntou coberturas da Movida) | — | — |
| IC7 Risco competitivo detectado | 3 (07997963, 27304203, 27285095 — este último fuga para balcão PF) | Movida / canal PF | SIM: 2 / NAO: 1 |

## P13 — Padrões emergentes (o que NENHUM prompt captura)
1. **S1 | Engenharia de contrato para contornar trava de crédito**: vendedor abre contrato com franquia de 1.000 km (mais barata) só para caber no limite de crédito e promete migrar para 5.000 km no dia seguinte via "condutor de contrato". Frequência: 1 caso explícito, mas descrito como rotina ("a gente dá um jeito"). Impacto: ALTO (risco de crédito/compliance mascarado). Evidência: Cliente 27170310.
2. **S3 | LGPD como muro recorrente**: bloqueios de condutor sem explicação, exigência de SCR assinado, validação de sócio via link — a justificativa "lei de proteção de dados" aparece em 3 ligações e em 1 delas custou a reserva. Frequência: 3/38. Impacto: ALTO (perda direta + frustração). Evidência: Clientes 27285095, 23939662, 16715835.
3. **S3 | Janela de reajuste de preços de meados de junho**: reajuste em sistema (~15/06) aparece como atrito em pelo menos 3 ligações (proposta antiga não honrada, "o aluguel deu uma subida", divergência de valor na tela). Vendedores usam como gatilho de urgência ("reserve para travar; PJ não tem taxa de cancelamento/no-show"). Frequência: 3/38. Impacto: MÉDIO. Evidência: Clientes 19781049, 25242238, 12224630.
4. **S2 | Fuga do canal oficial para o WhatsApp pessoal do executivo**: clientes pedem o número direto em ~8 ligações; verbalizam que "o número da Localiza é inviável conversar". Todo vendedor distribui o fixo/WhatsApp da mesa como diferencial. Frequência: ~8/38. Impacto: MÉDIO (dependência de pessoa, não de canal). Evidência: Clientes 16715835, 27304203, 17449341, 27319935.
5. **S1 | Co-navegação ao vivo no WebCorp como modelo operacional**: vendedor não tem autonomia sistêmica para emitir a reserva ("por segurança só você emite") e fica 6–20 min em linha guiando clique a clique; as 3 ligações mais longas do lote (1.182s, 1.112s, 1.067s) são todas isso. Frequência: 4-5/38. Impacto: MÉDIO (custo de atendimento alto; mas converte na hora). Evidência: Clientes 27170310, 12224630, 19781049, 27104103.
6. **S4 | Organizações religiosas como micro-segmento**: duas igrejas com estrutura de frota corporativa no lote (uma com 750 funcionários e 50 carros na Fleet), além de rapport religioso intenso em outra ligação. Impacto: BAIXO-MÉDIO (segmento com demanda esporádica faturada, hoje parcialmente na Movida). Evidência: Clientes 07997963, 12580658, 27170310.

## P14 — Diferenças entre vendedores
- **Bruna (Empresas)**: maior volume do lote; alterna suporte, cobrança e venda na mesma ligação — em Cliente 25242238 transformou cobrança de faturas atrasadas em pré-agendamento de 5 carros para a safra; em Cliente 27304203 reagiu bem à comparação com a Movida recotando um grupo mais barato (4.933→3.751). Ponto fraco: em Cliente 27285095 argumentou procedimento sem acolher a frustração e perdeu o cliente para o balcão PF.
- **Thais**: melhor gestão de objeção de preço do lote — explicou o reajuste com datas, ensinou fixo vs flexível, criou urgência legítima e acompanhou a reserva até a confirmação na agência (Cliente 19781049).
- **Luma**: condução didática de 18 min no WebCorp; detectou divergência de R$61 no valor, refez o fluxo até bater com a proposta assinada e antecipou orientações de fatura/spam (Cliente 12224630).
- **Matheus**: sondagem de pipeline mais estruturada (quando, quantas obras, quantos carros, onde), antecipa ampliação de crédito e sonda concorrência e até caminhões (Cliente 01574802); tom informal "tu" com novos cadastros (Cliente 27346432).
- **Ramiro**: cadência alta de ligações curtas de reativação com tom caloroso ("sentindo falta de vocês"); em Cliente 25249062 a ligação resgatou uma reserva que o cliente tinha esquecido; faz follow-up pós-retirada (Cliente 22111979). Pouco aprofundamento de descoberta.
- **Amanda**: rigor de governança — consultou a Receita Federal em tempo real para validar sócio e ofereceu dois caminhos de destravamento (Cliente 16715835).
- **Vendedor sem nome (BH)**: rapport extremo (religião, queijo, clima) por 20 min e criatividade para destravar crédito — mas via workaround de franquia de km que embute risco (Cliente 27170310).
- **Gabriel**: honesto sobre limite de autonomia ("já te dei o melhor NPC"), porém encerrou com insatisfação latente do cliente sem plano de recuperação (Cliente 11390532).
- **Andresa**: transparência incomum ao explicar a divisão interna Fleet vs RAC / executivo externo vs remoto, prevenindo ruído de relacionamento (Cliente 17449341).

## P15 — Eventos raros de alto impacto
| Cliente | Categoria | Evento | Impacto potencial | Ação recomendada |
|---|---|---|---|---|
| 07997963 | R3/R2 | Igreja com 750 funcionários e 50 carros na Localiza Fleet usa a MOVIDA (faturado) para todas as locações esporádicas — "a Movida está imbatível" no preço; proposta antiga de benefício a funcionários "não vingou" | Alto | Proposta formal de tarifa esporádica competitiva + retomar programa de locação para funcionários; cashback R$200 já ofertado, medir adesão |
| 27304203 | R3 | Cotação lado a lado: Fiorino Movida R$2.890/mês vs Localiza R$4.933 (recotada Strada R$3.751); decisão pendente | Alto | Follow-up em 48h com condição de fechamento; risco de perder o primeiro contrato do cadastro |
| 22808555 | R3/R1 | Cliente que migrou para assinatura Movida pediu sedan mensal 12 meses à Localiza — janela de win-back aberta | Médio-alto | Enviar cotação prometida no mesmo dia e acompanhar login na WebCorp (cliente relatou nunca ter acessado) |
| 25242238 | R1 | Pré-agendamento de 5 carros para a safra de setembro — condicionado à regularização de 2 faturas atrasadas | Alto | Resolver inadimplência agora e travar reservas antes do reajuste/disponibilidade |
| 01574802 | R1 | Duas obras novas confirmadas (Guarulhos em julho, Pouso Alegre em agosto) após devolução total da frota alugada; volume ainda indefinido | Médio-alto | Retorno agendado início de julho + preparar ampliação de crédito com antecedência (vendedor já sinalizou) |
| 27285095 | R2 | Cliente novo abandonou reserva PJ após bloqueio de condutor sem explicação (LGPD) e declarou que faria PF no balcão | Médio | Revisar script de comunicação de bloqueio; oferta ativa de recuperação do cadastro |
| 10343137 | R5 | Gestora de contato (Daniela) desligada da empresa; contatos atualizados em linha | Baixo-médio | Atualização de cadastro feita; validar novo fluxo com os 2 gestores remanescentes |

## Observações livres
O lote é dominado por atendimento consultivo/suporte (co-navegação no WebCorp, destravamento de crédito e acessos) mais do que prospecção fria — o executivo funciona na prática como "suporte premium com meta". A Movida é o único concorrente citado e aparece sempre pelo preço (nunca por serviço), enquanto o principal "concorrente" operacional é a própria burocracia interna da Localiza (crédito inicial, LGPD, aprovação de gestores), que causou a única perda clara do lote. O reajuste de preços de junho é um tema transversal que os melhores vendedores converteram em gatilho de urgência e os demais apenas comunicaram.
