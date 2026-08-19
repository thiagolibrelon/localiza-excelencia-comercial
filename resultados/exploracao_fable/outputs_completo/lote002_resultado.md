# Lote 002 — Exploração P3+P7

## Resumo do lote
- Total de ligações no lote: 37
- Ligações da BASE_ANTIGA_1275: 37
- Ligações do NOVO_LOTE_5348: 0 (lote 100% composto pela base antiga)
- Nota: 8 ligações são "vazias" para classificação — contato ausente/em reunião, apenas transferência interna sem retorno ao tema, reagendamento de ligação futura ou espera em locução (Clientes 01354366, 01513088, 01650434, 01700124, 01804741, 02153429 e as duas primeiras tentativas com o Cliente 02504940). Os números abaixo refletem as ~29 ligações restantes com conteúdo analisável. Outra característica deste lote: predominância de ligações de manutenção de carteira/cortesia (apresentação de executivo, checagem de demanda, pesquisa de satisfação) e de suporte técnico (acesso, reserva), com poucas ligações de venda ativa.

## P3 — Problemas recorrentes (tabela de frequência)
| Código | Categoria | Ocorrências | Resolvido na ligação (SIM/NAO/PARCIAL — contagem) | Escalou (contagem por destino) |
|---|---|---|---|---|
| P1 | Acesso/sistema (login CNPJ, biometria, navegador travando) | 4 | SIM 0 / PARCIAL 1 / NAO 3 | 2 (TI/assistência técnica); 1 (0800/central); 1 nao_escalou |
| P2 | Faturamento/cobrança (fatura para agência errada, KM duplicado por substituição, fatura vencida, reserva fechando com dias errados) | 5 | SIM 2 / PARCIAL 2 / NAO 1 | 1 (setor de negociação/financeiro); 4 nao_escalou |
| P3 | Multa/infração | 0 | — | — |
| P4 | Manutenção/substituto (pneu furado, sem categoria para upgrade) | 2 | PARCIAL 2 | 2 (0800 assistência) |
| P5 | Condutor/cadastro (procuração/documentação de diretor trava aumento de limite) | 1 | NAO 1 | 1 (supervisão/diretoria interna) |
| P6 | Km excedente | 0 | — | — |
| P7 | Disponibilidade (categoria esgotada, grupo raro na frota) | 2 | PARCIAL 2 | 2 nao_escalou (contornado pelo próprio vendedor) |
| P8 | Franquia/agência | 0 | — | — |
| P9 | Sinistro (avaria contestada, dúvida sobre proteção contratada) | 2 | PARCIAL 2 | 2 (assistência clientes / 0800) |
| P10 | Reserva/sistema (prorrogação, reserva "sob consulta", tela travando) | 5 | SIM 2 / PARCIAL 3 | 1 (supervisora + agência); 4 nao_escalou |
| P11 | Outro (turnover de contato/gestor — cliente e vendedor) | 2 | N/A (natureza informativa, não é "problema resolvível") | 2 nao_escalou |
| P12 | Manipulação de pesquisa/NPS | 1 | NAO 1 (por definição) | nao_escalou |

Leitura direcional: P1 + P10 (acesso e falhas de portal/reserva) somam 9 das ~24 ocorrências de problema — praticamente 40% do lote, igual ao padrão já visto em lotes anteriores. Diferente do lote 02 (batch02) analisado antes, aqui quase todas as ocorrências de P2/P9 exigem acompanhamento fora da ligação (PARCIAL), e P1 tem a pior taxa de resolução do lote (3 de 4 casos ficam sem solução na própria ligação).

## P3 — Exemplos
- **Cliente 01596959** (P1): o login antigo (43588), usado para acessar reservas, faturas e comissões da CNPJ "Rafael Viagens", foi desativado; o novo login só mostra dados da empresa "VINC". O vendedor (Ângelo) reconhece não ter acesso ao CNPJ da Rafael e apenas repassa um canal genérico de contato, sem abrir chamado formal. A cliente se frustra ("vou perder o dia todo por causa disso... estou me irritando com isso") e encerra pedindo para não ser mais contatada por ele. Não resolvido na ligação — o pior desfecho de relacionamento do lote.
- **Cliente 01492545** (P5): cadastro de uma empresa ligada ao Banco do Brasil trava porque a área de compliance do cliente exige CPF/RG/CNH do diretor além da procuração já registrada em cartório. A vendedora tenta contornar comparando o procurador com o de outro CNPJ do mesmo grupo ("flat") para ver se já está validado em algum lugar, mas não resolve na ligação — apenas sinaliza internamente ("vou levantar aqui internamente").
- **Cliente 01946427** (P10): ao tentar mudar o horário de retirada de uma reserva confirmada (10h → 15h, para dar tempo de uma nova colaboradora ser integrada), a reserva cai em "sob consulta" e corre risco de não ser reconfirmada. A vendedora identifica o problema, promete acionar a agência de Caruaru e até "falar com a supervisora" para garantir o carro, e reforça acompanhamento via WhatsApp. Resolução parcial, pendente de confirmação externa à ligação.
- **Cliente 01739823** (P12): ao final de uma ligação de manutenção de contrato, a vendedora explica em detalhe a escala da pesquisa de satisfação ("de zero a oito é insatisfação, de nove a dez é satisfação") e insiste repetidamente para o cliente avaliá-la bem, mesmo com o cliente tentando encerrar por ter outra ligação entrando. Não é uma nota "ditada" literalmente, mas a condução da escala é feita de forma a induzir nota alta — classificado como quem_relatou=vendedor_detectou e foi_resolvido_na_ligacao=NAO por definição de categoria.

## P7 — Cross-sell/Upsell (tabela de frequência)
| Código | Produto | Vezes mencionado | Vezes ofertado ativamente | Janelas perdidas identificadas |
|---|---|---|---|---|
| PR1 | Aluguel mensal leve (core) | ~25 | 3 | 0 |
| PR2 | Aluguel pesado | 0 | 0 | 0 |
| PR3 | Telemetria | 1 (mencionada como recurso já existente para localizar veículo, não como upsell) | 0 | 0 |
| PR4 | Proteção total / cobertura de avarias | 4 | 3 | 1 |
| PR5 | Upgrade de categoria | 1 | 0 | 1 |
| PR6 | Km adicional | 2 | 0 | 0 |
| PR7 | Contrato anual | 2 | 2 | 1 |
| PR8 | Elétrico | 0 | 0 | 0 |
| PR9 | ZARP | 0 | 0 | 0 |
| PR10 | Meoo/assinatura | 1 | 0 | 1 |
| PR11 | Venda de Seminovos | 0 | 0 | 0 |
| PR12 | Gestão de frotas | 0 | 0 | 1 |

## P7 — Exemplos
- **Oferta ativa bem feita — Cliente 01739823 (Andresa)**: durante uma visita de manutenção de contrato, a vendedora oferece proativamente a proteção total de avarias e o seguro a terceiros ampliado, explicando o benefício de forma concreta ("se tiver alguma coisa com o carro da Localiza... a gente não vai cobrar nada de vocês") e promete enviar os detalhes por e-mail.
- **Oferta ativa bem feita — Cliente 01433093**: cotação de novo contrato mensal já nasce com proteção total de avarias incluída por padrão e fecha com contrato de 12 meses (PR7), reforçando como vantagem extra a inclusão de condutores adicionais sem custo.
- **Janela perdida — Cliente 02000111 (Romulo/grupo Universo)**: o cliente revela que o grupo tem 4 empresas (mesmo endereço, mesmos sócios) que vão precisar de cadastro na Localiza. A vendedora conduz apenas o processo de pré-cadastro e biometria de cada CNPJ, sem propor uma gestão de frotas centralizada (PR12) para o grupo.
- **Janela perdida — Cliente 02588908 (João Carlos)**: o cliente descreve um padrão sazonal muito claro de demanda ("período mais crítico é outubro para abril... aí a gente usa muita locação"), usando carro próprio no restante do ano. A vendedora apenas registra que vai "dar uma ligadinha de vez em quando" e não propõe contratação antecipada para a próxima alta temporada.
- **Janela perdida — Cliente 01492545 (Petrônio)**: o cliente menciona espontaneamente que pretende "pegar outro carro pra assinatura" enquanto aguarda a entrega de um veículo zero km, e chega a perguntar a probabilidade de precisar alugar por 1-2 meses nesse intervalo. A vendedora só discute aumento de limite de crédito e não conecta a fala com o portfólio de assinatura da própria Localiza (Meoo/PR10) — risco real de perder essa demanda para um concorrente.

## Respostas — Parte P3
1. **Quais problemas são sistêmicos?** P1 (acesso/sistema) e P10 (reserva/sistema) — aparecem em contextos completamente diferentes (login multi-CNPJ, navegador/anexo de CNH, alteração de horário de reserva, prorrogação) e nenhum deles é resolvido de fato dentro da ligação em mais da metade dos casos. P2 também mostra um padrão sistêmico ligado a falta de acesso ao portal (cliente não recebe fatura por e-mail porque nunca teve login).
2. **Quais o vendedor resolve sem escalar, e como?** A maior parte de P10 (01401903, 01678344, 02415536) é resolvida só com explicação da regra de negócio (tolerância de 3h para devolução, prorrogação automática, como configurar reserva mensal corretamente) — o vendedor "traduz" o sistema para o cliente. Em P2, a explicação técnica do demonstrativo de fatura (Cliente 01722606) resolve a dúvida de cobrança duplicada sem precisar escalar.
3. **Quais escala desnecessariamente, ou deveria escalar e não escala?** O caso mais grave é o oposto do esperado: o Cliente 01596959 (P1) deveria ter sido escalado formalmente (chamado interno, transferência efetiva) e não foi — o vendedor apenas indicou "ligue para a central", o que gerou frustração alta e pedido do cliente para não ser mais contatado. Não há evidência de escalonamento desnecessário no lote.
4. **Qual tem maior impacto negativo na relação?** P1, com destaque para o Cliente 01596959: a cliente relata que vai "perder o dia todo", se diz "irritada" e encerra retirando a confiança no vendedor como ponto de contato. É o único desfecho claramente deteriorado do lote.
5. **O que produto/operações deveria priorizar?** (a) segregação correta de acessos multi-CNPJ/login (raiz do P1 em pelo menos 2 casos); (b) estabilidade do portal/navegador para anexar documentos de condutor (Cliente 02105371); (c) reduzir a incidência de reservas caindo "sob consulta" após qualquer alteração de horário/data (P10); (d) padronizar a lista de documentos exigida no cadastro de empresas vinculadas a instituições financeiras (Cliente 01492545), hoje resolvida "no jeitinho" comparando procurações entre CNPJs.

## Respostas — Parte P7
1. **Qual produto tem maior gap janela×oferta?** PR12 (gestão de frotas) e PR10 (Meoo/assinatura) — cada um teve uma janela clara identificada e zero ofertas ativas no lote.
2. **Quais clientes têm maior potencial de expansão imediata?** Cliente 02000111 (Romulo/grupo Universo, 4 CNPJs a cadastrar), Cliente 01946427 (Luísa/Integratio, já cotando um 4x4 por 27 meses e mantendo contratos fixos de 12 meses) e Cliente 02588908 (João Carlos, demanda sazonal previsível out-abr).
3. **Algum produto nunca mencionado?** PR2 (pesados), PR8 (elétrico), PR9 (ZARP) e PR11 (venda de seminovos) — zero menções em todo o lote.
4. **Qual perfil de cliente mais compra cross-sell quando ofertado?** Clientes em processo de nova cotação/reserva (onde a proteção total de avarias entra "por padrão" no fluxo, como nos Clientes 01433093 e 01909798) e clientes com relacionamento de longa data e bom histórico de pagamento (Cliente 01946427), que já aceitam facilmente reforçar contratos de 12 meses.
5. **Mapa de produto por situação:**
   - "Cliente diz que usa carro próprio e só aluga em picos sazonais" → ofereça **PR7** (contrato antecipado para a alta temporada), porque garante preço e disponibilidade antes do pico, evitando que o cliente procure a concorrência de última hora.
   - "Cliente tem múltiplas empresas/CNPJs do mesmo grupo" → ofereça **PR12** (gestão de frotas centralizada), porque consolida controle, faturamento e pode viabilizar desconto por volume.
   - "Cliente menciona interesse em carro por assinatura" → ofereça **PR10** (Meoo), porque é o produto de assinatura da própria Localiza e evita que a demanda vá para um concorrente.
   - "Cliente não sabe se contratou proteção total de avarias" → confirme e ofereça **PR4** imediatamente, porque reduz o risco de sinistro sem cobertura e o desgaste que isso causa na relação.
   - "Cliente faz reservas avulsas de 15+ dias repetidamente" → ofereça **PR1** no formato mensal, porque fica mais barato que a soma das diárias — padrão que o próprio vendedor já identificou espontaneamente em uma das ligações (Cliente 02045570).

## Observações livres
O lote é dominado por dois perfis de ligação: (1) manutenção de carteira/cortesia — apresentação de executivo de conta, checagem de demanda, confirmação de acesso — sem problema real a resolver; e (2) suporte operacional a acesso e reserva, que consome a maior parte do tempo dos executivos e raramente conclui dentro da própria ligação (P1 e P10 juntos respondem por boa parte das ~24 ocorrências de problema). Cross-sell fora do core é quase inexistente: em 37 ligações, PR4 é o único produto de upsell com tração real (ofertado ativamente 3 vezes), enquanto PR7, PR10 e PR12 aparecem quase exclusivamente como sinais não explorados. Um achado que merece atenção de compliance é a ligação do Cliente 01739823, em que a vendedora conduz a explicação da pesquisa de satisfação de um jeito que empurra para nota alta — um padrão de risco para a integridade do indicador de NPS, ainda que mais sutil do que uma "ditagem" literal de nota.
