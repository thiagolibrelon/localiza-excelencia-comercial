# Lote 04 (novo lote, 5.348) — Exploração P4+P8+P11+P13+P14+P15

## Resumo
- Total de ligações no lote: 38
- Vendedores identificados neste lote: Rodrigo (gestor), Ana Luísa, Cristiane, Luiz, Tatiana, Rosiane, Talita, Matheus, Fábio, Pedro, Daniel Luiz, Isadora, Cristina, Tamire, Ângelo, Lucas, Bruna, Ana Paula, Stephanie, Fabrício, Brenda. (1 ligação sem contato humano — vendedor caiu na URA, Cliente 15481836; nomes com STT ruidoso em 2-3 ligações não foram forçados.)

## P4 — Health Score (por cliente, só os que têm sinal claro — não force todos)
| Cliente | Volume | Adimplência | Fidelidade | Engajamento | Complex.Operacional | Potencial Upsell | Score Total (0-12) | Risco Churn |
|---|---|---|---|---|---|---|---|---|
| 26513991 | 2 | 1 | 2 (Platinum, 3 anos só Localiza) | 2 | 1 | 2 (proposta 12m, crédito 12k) | 10 | Baixo |
| 25198551 | 2 (mensal desde abril) | 1 | 1 | 2 | 1 (confusão de fatura recorrente) | 2 (Toro locação longa até fim do ano) | 9 | Baixo-médio |
| 19842308 | 2 (contrato ativo + setembro) | 1 | 1 | 2 | 1 | 2 (pediu ampliação de crédito) | 9 | Baixo |
| 13365284 | 1 (1º contrato, teste 30d) | 1 | 1 | 2 | 1 | 2 (12-24 meses se teste funcionar) | 8 | Baixo |
| 09038408 | 1 (esporádico, diretor) | 1 | 1 | 2 | 1 | 2 (interesse em Pesados/caminhões) | 8 | Baixo |
| 14267275 | 1 | 1 | 1 | 2 | 1 | 1 (migrou diária→mensal) | 7 | Baixo |
| 18317702 | 1 (mensal 2º mês) | 1 | 1 | 2 | 1 | 1 | 7 | Baixo |
| 17263728 | 1 | 0 (2 faturas vencidas 29/05) | 1 | 1 | 1 | 1 | 5 | Médio |
| 07173449 | 1 | 0 (3 multas + indenização vencidas, ~R$900) | 1 | 1 | 1 | 0 | 4 | Médio-alto |
| 07883480 | 0 (inativo, migrou) | 1 | 0 | 1 (aceitou receber tabela) | 1 | 1 | 4 | Alto (já perdido, recuperável) |
| 12363390 | 0 (nunca locou) | 1 | 0 (locou com concorrente) | 1 | 1 | 0 | 3 | Alto |
| 25386563 | 0 | 1 | 0 | 0 (pediu exclusão do cadastro) | 1 | 0 | 2 | Churn consumado (detrator ativo) |
| 24330744 | 0 | 1 | 0 | 0 | 0 | 0 | 1 | Churn consumado (empresa fechou) |

## P8 — Objeções (tabela de frequência)
| Tipo | Ocorrências | Resposta mais usada | Eficácia predominante | Melhor exemplo observado |
|---|---|---|---|---|
| OB1 Preço/valor | 5 (07883480, 27117767, 26551679, 26513991, 25198551) | R1/R2 (validou e usou dado do cliente) | Média | Cliente 26513991: objeção a câmbio automático mais caro; Rodrigo usou flexibilidade de km mês a mês (R2) e a objeção foi superada — proposta dupla enviada |
| OB3 Demanda baixa | 6 (26602474, 06721151, 08127990, 16507374, 25830517, 12363390) | R1 (validou + explorou frota/previsão) | Baixa-média | Cliente 26602474: Matheus explorou e extraiu previsão concreta ("julho/agosto, diárias") — adiada com data |
| OB5 Problema não resolvido | 3 (20148743, 12363390, 25386563) | R1/R4 quando resolvível; R5 quando emocional | Alta quando operacional / nula quando relacional | Cliente 20148743: não conseguia login e alugava como PF; Matheus resolveu na hora com reset guiado por vídeo — superada |
| OB2 Prazo/adiamento | 2 (27171387 "não estamos prontos p/ assinatura", 25830517) | R1 | Média | Cliente 27171387: vendedora validou e converteu em pedido de cotação mensal (HB20/Onix, 3 mil km) — adiada com próximo passo |
| OB6 Burocracia/aprovação | 1 (07173449 — boleto precisa de 3 dias de vencimento) | R4 (posicionou-se como aliada, foi buscar solução interna) | Média | Cliente 07173449: vendedora assumiu o caso e prometeu retorno em 24h via WhatsApp — adiada |

Nota: o pior desfecho do lote foi Cliente 25386563 (OB5 extrema): vendedor Pedro capitulou sem explorar (R5) — apenas "entendi, ok" diante de churn declarado.

## P11 — Inteligência competitiva (tabela de frequência)
| Tipo | Ocorrências | Concorrentes citados | Vendedor explorou (SIM/NAO — contagem) |
|---|---|---|---|
| IC4 Frota própria revelada | 9 (25198551, 27364562, 06721151, 17254737, 08127990, 25830517, 16507374, 25386563, 09038408-terceirizada) | — | SIM 5 / NAO 4 |
| IC3 Histórico de migração | 2 (07883480 → locadora local por preço; 12363390 → outra locadora por falta de resposta no cadastro) | "locadora local" (sem nome) | SIM 2 / NAO 0 |
| IC6 Vendedor sondou concorrência | 4 (07883480, 26513991, 06721151, 25830517) | — | SIM 4 (por definição) |
| IC2 Confirmação de exclusividade | 1 (26513991 — "de 3 anos pra cá só Localiza, virei Platinum") | Rentcars (comparador, uso passado) | SIM 1 |
| IC5 Comparação implícita de preço | 2 (27117767 PF vs PJ/agência; 07883480) | — | SIM 2 |
| IC7 Risco competitivo detectado | 3 (07883480 ativo com concorrente; 12363390; 25386563) | — | SIM 2 / NAO 1 |

## P13 — Padrões emergentes (o que NENHUM prompt captura)
1. **S3 | Fricção de login/acesso WebCorp fazendo receita PJ vazar para balcão PF** | ~5/38 ligações | Impacto ALTO | Cliente 20148743 (alugou como PF "no cartão do Jardim" por não conseguir senha), Cliente 26513991 (locava mensal no CPF de funcionário desde fevereiro porque o cadastro travou), Cliente 27305098 (reservou PF tendo cadastro PJ ativo), Cliente 00406257 (823s só recadastrando login após saída de funcionária), Cliente 13365284 (reset de senha guiado ao vivo). O cliente quer comprar PJ e o sistema o empurra para PF.
2. **S4 | Churn silencioso via compra de veículo próprio (CAPEX substituindo aluguel)** | 3-4/38 | Impacto ALTO | Cliente 25198551 (comprou Compass para eliminar locação no norte), Cliente 08127990 ("agora ele está com o dele"), Cliente 25386563 ("comprei um veículo para substituir"), Cliente 27364562 (usa carro próprio). Nenhuma ligação teve contra-argumento estruturado de TCO, exceto Rodrigo (25198551) com o pitch "rendimento paga o aluguel".
3. **S1 | Vendedores inativando cadastros proativamente para limpar carteira** | 2/38 | Impacto MÉDIO | Cliente 17254737 e Cliente 26551679 — Fábio e Lucas inativam cadastro sem demanda e deixam contato. Comportamento saudável de higiene de base, mas invisível às métricas de atividade.
4. **S3 | Cliente não entende a mecânica do contrato mensal (fechamento de ciclo, proporcionalidade, quebra)** | 3-4/38 | Impacto MÉDIO-ALTO | Cliente 25198551 (fatura veio "mais que o dobro" da diária ao devolver antes; quase virou detrator), Cliente 14267275 (precisou de call para entender que +1 dia = R$2.400 a menos), Cliente 27117767 (pricing diário flutuante). Educação de billing é feita call a call, não em escala.
5. **S1 | Vendedor perdido na URA da própria Localiza** | 1/38 | Impacto BAIXO (sintoma) | Cliente 15481836 — ligação inteira sem humano; vendedor desabafa "essa URA da Localiza é peste". Desperdício de esforço de carteira.
6. **S4 | Turnover de gestor no lado do cliente exigindo re-onboarding** | 3/38 | Impacto MÉDIO | Cliente 00406257 (Karina saiu, Thaís assumiu sem acesso), Cliente 09308133 (Silmara não está mais na empresa), Cliente 19361952 (condutor desligado ainda no contrato — risco de compliance).

## P14 — Diferenças entre vendedores
- **Rodrigo (gestor)**: calls longas e consultivas com fechamento de próximo passo concreto; usa flexibilidade de quilometragem e dedução fiscal PJ como argumento (Cliente 26513991 — recuperou conta que locava via CPF há meses e abriu proposta de 12 meses). Ponto fraco: promete "faço um preço melhor" genérico sem ancorar número (Cliente 25198551).
- **Ângelo**: melhor execução estruturada do lote — onboarding + reserva guiada ao vivo no portal + upsell transparente de proteções (ampliada aceita, total recusada sem atrito) e fechou reserva de R$3.141 na própria ligação (Cliente 13365284, 22 min). Modelo de D1 e D4.
- **Lucas**: educador; não capitula em desconto mas explica o mecanismo de pricing e dá alternativa acionável (reservar com antecedência + cancelamento grátis PJ — Cliente 27117767); inativa cadastro sem valor com transparência (Cliente 26551679). D5 forte sem ceder margem.
- **Matheus**: sondagem sistemática de frota e cross-sell de caminhões (Cliente 06721151); resolve atrito de login na hora com vídeo/print (Cliente 20148743); disciplinado em pedir avaliação. Estilo direto, menos rapport.
- **Cristina**: minuciosa em dados cadastrais e acessos; cross-sell bem colocado de Localiza Pesados que gerou interesse genuíno (Cliente 09038408 — "foi bom você me orientar").
- **Tamire**: relacionamento caloroso ("minha querida") e proatividade em gerar economia para o cliente (migração diária→mensal, de R$7,0k para R$4,6k — Cliente 14267275) — constrói confiança que retém.
- **Pedro**: em call de rotina é ok (Cliente 20033995, 27305098 — orientou trocar reserva PF por PJ), mas diante de churn furioso capitulou totalmente sem explorar nem registrar recuperação (R5, Cliente 25386563) — contraste claro com o resto do lote.

## P15 — Eventos raros de alto impacto
| Cliente | Categoria | Evento | Impacto potencial | Ação recomendada |
|---|---|---|---|---|
| 25386563 | R2 (churn) | Churn consumado e verbalizado com raiva: "Localiza caiu no meu conceito... conceito zero"; pediu exclusão de cadastro, comprou carro próprio, ex-acionista da empresa; reclama de atendimento e app | Alto (detrator ativo com potencial de dano de marca) | Escalar para recuperação sênior/ouvidoria; enviar faturas solicitadas imediatamente; NÃO recontatar comercialmente |
| 24330744 | R5 (mudança estrutural) | Cliente informou que fechou a empresa e mudou de ramo | Baixo direto / higiene | Inativar cadastro; manter contato pessoal registrado |
| 26513991 | R1 (expansão) | "A rotina começou a crescer, começou a cair uma viagem em cima da outra" — eventos em expansão; fidelizado Platinum; migrando de CPF para PJ com crédito de R$12k | Alto (upsell 12 meses) | Enviar proposta sedã manual/automático 3-12m e acompanhar em 1 semana |
| 25198551 | R1 + IC4 | Comprou Compass para operação eólica no norte (substituiu locação), mas sinalizou demanda de utilitário maior (Toro) em locação longa até o fim do ano | Médio-alto | Cotação proativa de Toro/utilitário antes que avalie compra ou concorrente |
| 12363390 | R3 (competitiva) | Perdeu a primeira locação para concorrente porque o cadastro Localiza não teve resposta a tempo | Médio (falha de processo replicável) | Auditar SLA de aprovação de cadastro novo; follow-up via WhatsApp como cliente pediu |
| 07883480 | R3 (competitiva) | Migração confirmada para locadora local por preço; cliente ainda aluga mensal com concorrente e aceitou receber tabela de mensal fixo 3-12m | Médio-alto (recuperação viável) | Enviar tabela grupo CE e retomar em 15 dias com oferta de contrato 6-12m |
| 09038408 | R1 (expansão/cross-sell) | Distribuidora de farinha com transporte terceirizado (van/VUC) demonstrou interesse real em Localiza Pesados | Médio | Encaminhar portfólio de pesados e agendar apresentação com o diretor |
| 08197238 | R4/R1 | Lead quente: demanda de locação de 2 meses sinalizada internamente (Diego), gatekeeper conectou vendedor direto ao decisor | Médio | Ligação imediata (já encaminhada na call) e proposta no mesmo dia |

## Observações livres
STT deste lote tem eco duplicado severo em pelo menos 2 ligações (Cliente 09308133 repete cada frase nos dois speakers) e a palavra "avaria" aparece sistematicamente no lugar de nomes próprios (provável "Maria"), o que impediu identificar 2-3 vendedoras. O lote é dominado por contatos de rotina/reativação de cadastro (~60%), mas concentra dois achados estratégicos: a fricção de login WebCorp que empurra receita PJ para balcão PF, e o churn silencioso por compra de veículo próprio em clientes pequenos — ambos atravessam vários clientes e nenhum prompt padrão os captura isoladamente.
