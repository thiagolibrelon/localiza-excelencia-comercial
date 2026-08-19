# Lote 005 — Exploração P3 (Problemas recorrentes) + P7 (Cross-sell/Upsell)

## Resumo do lote
- Total de ligações no lote: **38**
- Ligações da BASE_ANTIGA_1275: 38 (100% — não há ligações do NOVO_LOTE nesse arquivo)
- Ligações "vazias" para classificação (número errado, correio de voz cortado, transferência que não completa): **3** — Cliente 05614928 (ligou para empresa errada), Cliente 06356330 (1ª das 3 ligações, 17s, corte em correio de voz) e Cliente 06437531 (transferência que corta antes de falar com o contato).
- As demais 35 ligações têm conteúdo analisável, embora várias sejam contatos de manutenção de carteira curtos e sem problema/produto relevante (ex.: 05560781, 05662716, 05767917, 05911139, 06328901).
- Dois pares/trios de ligações repetem o mesmo cliente no mesmo dia ou em dias seguidos, tratando do mesmo assunto em continuação: **05692557** (2x), **05878806** (2x, mesma disputa de sinistro), **06194463** (2x, mesma reserva sendo montada), **06252636** (2x, mesma disputa de reserva/logística), **06356330** (3x, mesmo contrato AD).

---

## PARTE P3 — Problemas recorrentes

### Parte 1 — Por ligação (apenas ligações com problema identificado; 15 de 38)

| cliente_id | data | problemas_identificados | quem_relatou | foi_resolvido_na_ligacao | escalou_para | observacao |
|---|---|---|---|---|---|---|
| 05275842 | 2026-06-03 | P4 | cliente | PARCIAL | nao_escalou | Condutor recebeu contato da agência sobre KM próxima de 40 mil e entendeu como pedido de devolução; era pedido de substituição. Vendedora explicou a regra, mas pediu para o cliente confirmar a mensagem exata recebida pelo condutor. |
| 05275842 | 2026-06-03 | P1 | cliente | NAO | nao_escalou | Funcionalidade nova de "adicionar condutor" no WebCorp (lançada no dia anterior) ficou com tela em branco ao vivo durante a ligação. Vendedora reconheceu instabilidade de recurso recém-implantado. |
| 05541327 | 2026-06-01 | P5 | cliente | SIM | nao_escalou | Cliente pediu remoção do acesso de um funcionário desligado no portal; vendedora executou na hora ("retirei o cadastro dele"). |
| 05551695 | 2026-06-03 | P1 | cliente | PARCIAL | nao_escalou | Tela do WebCorp travou no navegador do cliente após concluir a reserva; cliente não conseguia baixar a confirmação. Vendedora contornou enviando o localizador da reserva por fora (não pode enviar a tela interna). |
| 05692557 | 2026-06-01 | P1 | cliente | NAO | 0800 | Reserva feita pelo próprio cliente saiu registrada no nome de outra pessoa (bug sistêmico não identificado pela vendedora). Orientado a acionar 0800/e-mail para a Localiza apurar. |
| 05692557 | 2026-06-01 | P11 | cliente | PARCIAL | 0800 | Cliente relata dificuldade crônica em obter suporte da unidade "Localiza Meu/assinatura" (contrato de carro por assinatura separado do RAC comercial): "fica enviando eu de um para outro". Vendedora reconhece a falha ("tem muitos clientes que param aqui") mas não tem acesso ao sistema da outra unidade; repassa contato de 0800 dedicado. |
| 05732193 | 2026-06-03 | P1 | cliente | SIM | nao_escalou | Confusão entre dois portais distintos (portal de negociação de boletos vs. WebCorp) e sobre login/e-mail compartilhado entre dois usuários da mesma empresa. Vendedora esclareceu completamente na ligação. |
| 05878806 | 2026-06-01 | P9 | cliente | NAO | supervisora | Disputa de cobrança de sinistro: cliente pagou franquia de ~R$4 mil pelo carro alugado e recebeu boleto adicional de R$1.120 referente a terceiro, que não reconhece. Cliente ameaça encerrar contratos e "ir para as redes sociais". Vendedora abre apuração interna e promete retorno no dia seguinte. |
| 05878806 | 2026-06-02 | P9 | cliente | PARCIAL | supervisora | Ligação de acompanhamento da mesma disputa (dia seguinte). Vendedora (outra executiva, Cristina) confirma que a resposta recebida pelo cliente não veio da área correta de apuração, reabre o caso com prioridade e pede números de contrato adicionais para instruir a investigação. Ainda sem solução final. |
| 05974287 | 2026-06-01 | P5 | vendedor_detectou | PARCIAL | nao_escalou | Contato antigo da empresa foi desligado; novo contato (Thalisson) não tem login porque falta validação de sócio via link de cadastro. Vendedora identifica a pendência e envia fatura manualmente "por liberalidade" enquanto o cadastro não é regularizado. |
| 05988682 | 2026-06-02 | P1 | cliente | PARCIAL | IT | Cliente pede unificação de login entre três empresas do mesmo grupo; processo não é automático — vendedora orienta o passo a passo de redefinição de senha e diz que vai pedir a unificação dos códigos internamente. |
| 06004842 | 2026-06-03 | P7 | cliente | PARCIAL | nao_escalou | Cliente sem conseguir reserva para Bonito/MS no feriado, tanto pelo WebCorp quanto pela central 0800 — categoria esgotada no destino turístico. Vendedora explica ciclo de devolução/lavagem e orienta reconsultar por volta de 13h30, sem garantia. |
| 06252636 | 2026-06-02 | P10 | cliente | PARCIAL | IT/agência | Ao editar data e local de 3 reservas de picape (mudança de cidade e data), as reservas caem em "consulta"/"confirmação" em vez de manterem a prioridade da reserva original. Vendedor precisa cancelar e recriar as 3 reservas e contatar a gerente da agência diretamente para tentar garantir os veículos. |
| 06252636 | 2026-06-03 | P10 | cliente | NAO | 0800 (sugerido, sem confiança de resolução) | Ligação de escalonamento do mesmo caso: decisor da empresa terceirizada (Lucas) discute com o vendedor, exige que o sistema priorize reservas antigas, não aceita a explicação técnica e encerra a ligação insatisfeito, dizendo que vai "buscar algum recurso" em outro canal. O próprio vendedor reconhece que a central "faz a mesma coisa" e provavelmente não resolverá. |
| 06368346 | 2026-06-01 | P1 | cliente | PARCIAL | nao_escalou | Cliente recebeu e-mail automático de reset de senha sem entender o motivo. Vendedor esclarece que pode ser disparo automático do sistema e orienta a ignorar, sem explicar a causa raiz do disparo. |
| 06446906 | 2026-06-01 | P11 | cliente | PARCIAL | supervisora | Cliente pede tarifa melhor para o aluguel diário (não quer migrar para mensal por demanda irregular); não existe categoria de desconto para diária no fluxo do vendedor, que precisa subir solicitação para a coordenação. |
| 06473372 | 2026-06-05 | P10 | cliente | PARCIAL | nao_escalou | E-mails internos conflitantes do cliente (um pedindo para desconsiderar, outro para manter a reserva) deixam o status da reserva futura ambíguo. Vendedora confirma que a reserva segue aberta e orienta cancelamento pela plataforma caso não seja mais necessária. |

### Parte 2 — Consolidado do lote (tabela de frequência)

| Código | Categoria | Total ocorrências | Clientes afetados | Resolvido na ligação (SIM/PARCIAL/NAO) | Escalou (%) |
|---|---|---|---|---|---|
| P1 | Acesso/sistema | 6 | 6 (05275842, 05551695, 05692557, 05732193, 05988682, 06368346) | SIM 1 / PARCIAL 3 / NAO 2 | 33% (1 para 0800, 1 para IT) |
| P2 | Faturamento/cobrança | 0 | 0 | — | — |
| P3 | Multa/infração | 0 | 0 | — | — |
| P4 | Manutenção/substituto | 1 | 1 (05275842) | PARCIAL 1 | 0% |
| P5 | Condutor/cadastro | 2 | 2 (05541327, 05974287) | SIM 1 / PARCIAL 1 | 0% |
| P6 | Km excedente | 0 | 0 | — | — |
| P7 | Disponibilidade | 1 | 1 (06004842) | PARCIAL 1 | 0% |
| P8 | Franquia/agência | 0 | 0 | — | — |
| P9 | Sinistro | 2 | 1 (05878806) | NAO 1 / PARCIAL 1 | 100% (supervisora/apuração) |
| P10 | Reserva/sistema | 3 | 2 (06252636, 06473372) | PARCIAL 2 / NAO 1 | 67% (IT/agência + 0800) |
| P11 | Outro (integração RAC×assinatura; negociação de tarifa diária) | 2 | 2 (05692557, 06446906) | PARCIAL 2 | 100% (0800 + supervisora) |
| P12 | Manipulação de pesquisa/NPS | 0 | 0 | — | — |

Total de ocorrências no lote: **17**, distribuídas em 15 ligações (05275842 e 05692557 concentram 2 problemas cada na mesma ligação).

### P3 — Respostas

**(1) Quais problemas são sistêmicos?**
P1 (acesso/sistema) e P10 (reserva/sistema) somam 9 das 17 ocorrências (~53%) e têm a mesma raiz: falhas de portal ou de comportamento do sistema de reservas que o vendedor não controla — recurso novo de "adicionar condutor" travando no lançamento (05275842), tela do WebCorp congelando após concluir reserva (05551695), reserva saindo com nome trocado (05692557), unificação de login manual entre CNPJs (05988682), e o padrão mais grave: reservas que perdem prioridade ao serem editadas e caem em "consulta" (06252636, repetido em duas ligações com escalada de tensão). Isso não é um problema pontual de um cliente — é comportamento reproduzido em contas diferentes.

**(2) Quais o vendedor resolve sem escalar, e como?**
P5 (condutor/cadastro) é resolvido inteiramente dentro da ligação: remoção de acesso de funcionário desligado feita na hora (05541327) e contorno manual (envio de fatura por fora) enquanto o cadastro formal não é validado (05974287). P4 e boa parte do P1 "leve" (email automático, confusão de portal) também são resolvidos por explicação direta do vendedor, sem necessidade de abrir chamado.

**(3) Quais escala desnecessariamente?**
O caso mais claro é 06252636 (2ª ligação): o próprio vendedor admite que "a central faz a mesma coisa que eu" antes de sugerir que o cliente ligue para o 0800 — ou seja, encaminha para um canal que ele mesmo não acredita que vai resolver, apenas para não deixar o cliente sem alternativa. Isso gera falsa expectativa em vez de reconhecer a limitação e buscar uma saída interna (ex.: acionamento direto de um supervisor).

**(4) Qual tem maior impacto negativo na relação?**
Empate entre P9 (sinistro/franquia do cliente 05878806, com ameaça explícita de encerrar contratos e "ir para as redes sociais", sem solução em nenhuma das duas ligações) e P10 no caso 06252636, onde um cliente de alto volume (10+ picapes/mês para uma operação terceirizada da Gerdau) encerra a segunda ligação visivelmente irritado, dizendo que vai "buscar algum recurso" fora da Localiza — mesmo com o sentimento da ligação marcado como POSITIVE, o teor do diálogo é de atrito real e risco de churn.

**(5) O que produto/operações deveria priorizar?**
(a) Corrigir o comportamento do motor de reservas para que editar data/local de uma reserva já confirmada não a jogue de volta para "em consulta" — é a queixa mais tecnicamente fundamentada do lote (06252636). (b) Testar melhor recursos novos do WebCorp antes do rollout (o caso "adicionar condutor" travando no primeiro dia, 05275842). (c) Dar SLA e comunicação proativa para apuração de sinistro/franquia — o cliente 05878806 ficou dois dias sem resposta e ameaçou churn. (d) Resolver a integração de atendimento entre RAC comercial e a unidade de assinatura ("Localiza Meu"), hoje um silo que o próprio vendedor reconhece como fonte de atrito recorrente (05692557).

---

## PARTE P7 — Cross-sell e Upsell

### Por ligação (todas as 38; "—" quando não há produto/janela relevante)

| cliente_id | data | duracao_s | produtos_mencionados | produtos_ofertados | janelas_identificadas | janelas_perdidas | o_que_deveria_ter_dito | impacto_estimado |
|---|---|---|---|---|---|---|---|---|
| 05275842 | 2026-06-03 | 1748 | PR8 (elétrico), PR7 (mensal fixo 3/6/9/12) | PR7 (explicado ativamente como economia); híbrido oferecido como substituto do elétrico indisponível | PR3 (cliente calcula km manualmente para saber quando o condutor se aproxima de 40 mil) | PR3 | "Vocês fazem esse controle manual de km — a telemetria automatiza isso e evita a confusão que o Edson teve com a agência." | Alto (frota crescendo para 12 carros) |
| 05432425 | 2026-06-01 | 140 | PR1 | PR1 (migração diário→mensal, recusada com justificativa de km) | PR6 (cliente roda 8-10 mil km/mês, valor acima do padrão) | PR6 | "Já que o volume de km é o que inviabiliza o mensal, veja um plano de km mais alto — pode compensar mesmo com tarifa um pouco maior." | Médio |
| 05511229 | 2026-06-03 | 632 | PR1 (cotação categoria/km) | — | — | — | — | Baixo |
| 05519027 | 2026-06-01 | 159 | — | — | — | — | — | — |
| 05541327 (1) | 2026-06-01 | 76 | PR1 | PR1 (migração AD→mensal, recusada) | — | — | — | Baixo |
| 05541327 (2) | 2026-06-01 | 92 | — | — | — | — | — | — |
| 05551695 | 2026-06-03 | 347 | PR4 (mencionado, confirmado que não foi contratado) | — | PR4 | PR4 | "Notei que vocês não pegaram a proteção total avarias nessa reserva — quer que eu explique a cobertura, já que o condutor é iniciante?" | Médio |
| 05560781 | 2026-06-02 | 80 | — | — | — | — | — | — |
| 05614928 | 2026-06-05 | 36 | — | — | — | — | — | Vazia (número errado) |
| 05624661 | 2026-06-03 | 89 | PR12 (cliente pergunta sobre contrato de 36 meses) | — | PR12 (cliente autoexcluiu ao esclarecer que só precisa de retiradas esporádicas de 2-3 dias) | — | — | Baixo |
| 05662716 | 2026-06-03 | 56 | — | — | — | — | — | — |
| 05692557 (1) | 2026-06-01 | 443 | PR9/PR10 ("Localiza Meu"/assinatura, produto já contratado pelo cliente) | — | — | — | — | Médio (cliente multi-produto, mas frustrado) |
| 05692557 (2) | 2026-06-02 | 161 | PR5 (upgrade executado), PR6 (km 2000→3000) | PR5 e PR6 (ambos a pedido do próprio cliente, confirmados pelo vendedor) | — | — | — | Médio |
| 05732193 | 2026-06-03 | 482 | — | — | — | — | — | — |
| 05742991 | 2026-06-01 | 80 | PR1 | PR1 (migração AD→mensal, recusada — cliente usa só dias avulsos) | — | — | — | Baixo |
| 05754021 | 2026-06-02 | 202 | PR1 (regras de faturamento AD explicadas) | — | — | — | — | Baixo |
| 05767917 | 2026-06-02 | 33 | — | — | — | — | — | — |
| 05809062 | 2026-06-01 | 182 | PR1 | PR1 (migração AD→mensal, 256→159/diária; cliente muito receptivo, aguardando aprovação do coordenador) | — | — | — | Alto (fechamento iminente) |
| 05878806 (1) | 2026-06-01 | 702 | PR4 | PR4 (ofertado ativamente em meio à disputa de sinistro; cliente reage com confusão/ceticismo) | — | — | — | Médio (timing de oferta questionável) |
| 05878806 (2) | 2026-06-02 | 2136 | PR4 | PR4 (reiterado; cliente demonstra interesse em deixar a cobertura ampliada "flegada" por padrão, pendente de aprovação da diretoria) | — | — | — | Médio |
| 05879742 | 2026-06-01 | 102 | PR1 | PR1 (migração diário→mensal, cliente indeciso — depende de demanda de assistência técnica) | — | — | — | Médio |
| 05911139 | 2026-06-01 | 91 | — | — | — | — | — | — |
| 05974287 | 2026-06-01 | 318 | — | — | — | — | — | — |
| 05988682 | 2026-06-02 | 231 | — | — | — | — | — | — |
| 06004842 | 2026-06-03 | 253 | — | — | — | — | — | — |
| 06082647 | 2026-06-03 | 196 | — | — | — | — | — | — |
| 06194463 (1) | 2026-06-01 | 180 | — | — | — | — | — | — |
| 06194463 (2) | 2026-06-02 | 502 | PR4, adicionais (condutor adicional, limpeza garantida) | PR4 ofertado e **aceito na hora** durante o passo a passo da reserva assistida | — | — | — | Alto (upsell concretizado) |
| 06252636 (1) | 2026-06-02 | 1393 | PR7 (mensal fixo 3 meses), PR4 (proteção mantida), limpeza (adicional aceito) | PR7 explicado ativamente; limpeza aceita | — | — | — | Alto (10+ veículos em jogo) |
| 06252636 (2) | 2026-06-03 | 501 | — | — | — | — | — | Negativo (atrito, sem venda) |
| 06328901 | 2026-06-05 | 81 | — | — | — | — | — | — |
| 06356330 (1) | 2026-06-01 | 17 | — | — | — | — | — | Vazia |
| 06356330 (2) | 2026-06-01 | 218 | PR1 | PR1 (migração AD→mensal por custo, 2.800→2.600, decisão pendente) | — | — | — | Médio |
| 06356330 (3) | 2026-06-01 | 164 | PR1 (acompanhamento) | — | — | — | — | Baixo |
| 06368346 | 2026-06-01 | 78 | — | — | — | — | — | — |
| 06437531 | 2026-06-01 | 88 | — | — | — | — | — | Vazia |
| 06446906 | 2026-06-01 | 172 | PR1 | PR1 (migração AD→mensal, 131→124, recusada por demanda irregular) | — | — | — | Baixo |
| 06473372 | 2026-06-05 | 121 | — | — | — | — | — | — |

### Por cliente (consolidado — apenas clientes com sinal relevante)

| cliente_id | executivo | produtos_ativos | produtos_com_potencial | produto_prioritario | receita_incremental_potencial | observacao |
|---|---|---|---|---|---|---|
| 05275842 | não identificado | PR1 (frota crescendo, indo a 12 veículos) | PR3, PR8/híbrido | PR3 Telemetria | Média-alta (frota em expansão ativa) | Cliente gestora de frota terceirizada; controla km manualmente — caso didático de janela perdida de telemetria. |
| 05692557 | Keila/Keira | PR1 + assinatura (Localiza Meu) | — | Retenção (resolver dor de integração) | Baixa até resolver atrito | Cliente multi-produto mas frustrado com falta de suporte cruzado entre RAC e assinatura. |
| 05809062 | Isaías | PR1 (2 contratos AD) | PR1 mensal | PR1 | Alta e imediata | Cliente muito receptivo à migração (economia de mais da metade da diária); só falta aprovação interna do coordenador do cliente. |
| 06194463 | Rodrigo | PR1 (reserva nova em montagem) | PR4 (já convertido) | — | Já capturada | Melhor upsell fechado do lote: proteção total avarias aceita durante reserva assistida passo a passo. |
| 06252636 | Matheus | PR1 (10+ picapes/mês, operação terceirizada) | PR4, limpeza, PR7 | Retenção + PR7 | Alta, mas em risco | Maior volume do lote; 2ª ligação termina em atrito por falha de reserva — risco de churn supera potencial de expansão se não houver correção sistêmica. |
| 05878806 | Cristina | PR1 | PR4 (interesse revelado, pendente de aprovação da diretoria do cliente para tornar padrão) | Retenção (resolver disputa de sinistro) | Média, condicionada à resolução do P9 | Cliente sinaliza interesse real em cobertura ampliada por padrão, mas a disputa de franquia em aberto compromete a confiança necessária para fechar. |
| 06356330 | não identificado | PR1 (múltiplos contratos AD) | PR1 mensal | PR1 | Média | Padrão recorrente de contratos AD que ultrapassam o ponto de equilíbrio do mensal; oportunidade de revisão de portfólio do cliente. |

### Por produto (consolidado do lote)

| Produto | Código | Vezes mencionado | Vezes ofertado ativamente | Janelas identificadas | Janelas perdidas | Taxa de aproveitamento (%) |
|---|---|---|---|---|---|---|
| Aluguel mensal leve (core) | PR1 | ~20 | 7 (migrações AD→mensal propostas) | 0 | 0 | 1 aceite entusiasmado + 2 pendentes de decisão de 7 ofertas (~14-43%) |
| Aluguel pesado | PR2 | 0 | 0 | 0 | 0 | — (nunca mencionado) |
| Telemetria | PR3 | 0 | 0 | 1 | 1 | 0% |
| Proteção total/cobertura de avarias | PR4 | 5 | 3 | 1 | 1 | 33% (1 aceito de 3 ofertados) |
| Upgrade de categoria | PR5 | 1 | 1 (a pedido do cliente) | 0 | 0 | 100% (mas reativo, não proativo) |
| Km adicional | PR6 | 2 | 1 | 1 | 1 | 50% |
| Contrato anual (mensal fixo longo) | PR7 | 2 | 2 | 0 | 0 | 0% fechado na ligação (decisões pendentes) |
| Veículos elétricos | PR8 | 1 | 0 | 0 | 0 (indisponibilidade de estoque, não falha comercial) | — |
| ZARP | PR9 | 0 (nome não citado; possível referência ambígua em "Localiza Meu") | 0 | 0 | 0 | — |
| Meoo | PR10 | 1 (produto já contratado pelo cliente, ambiguidade de STT com "Localiza Meu") | 0 | 0 | 0 | — |
| Venda de Seminovos | PR11 | 0 | 0 | 0 | 0 | — (nunca mencionado) |
| Gestão de frotas (36 meses) | PR12 | 1 | 0 | 1 | 1 (fraca — cliente autoexcluiu ao esclarecer que precisa só de retiradas esporádicas) | 0% |

### P7 — Respostas

**(1) Qual produto tem maior gap janela×oferta?**
PR3 (Telemetria): zero ofertas no lote inteiro, apesar de um sinal de necessidade explícito e concreto (cliente 05275842 fazendo controle manual de quilometragem para prever quando cada condutor se aproxima do limite de 40 mil km — exatamente o problema que telemetria resolve). PR6 (km adicional) também tem gap relevante: mencionado em contexto de objeção de preço (05432425) sem que o vendedor oferecesse ajuste de plano como saída.

**(2) Quais clientes têm maior potencial de expansão imediata?**
05809062 (migração AD→mensal com economia de mais de 50% na diária, cliente visivelmente entusiasmado, só falta aprovação interna) é o caso de fechamento mais próximo do lote. 06252636 tem o maior volume absoluto (10+ picapes/mês), mas o potencial está represado pelo atrito da 2ª ligação — expansão ali depende primeiro de resolver o problema de reserva (P10). 05275842 tem potencial de médio prazo pela frota em expansão ativa (indo a 12 veículos).

**(3) Algum produto nunca mencionado?**
PR2 (aluguel pesado) e PR11 (venda de seminovos) não aparecem em nenhuma das 38 ligações. PR9 (ZARP) também não é citado nominalmente — a única menção a "assinatura" no lote (cliente 05692557) é ambígua na transcrição ("Localiza Meu"), sem clareza se é ZARP ou Meoo.

**(4) Qual perfil de cliente mais compra cross-sell quando ofertado?**
O padrão mais forte do lote é o cliente que está em reserva assistida ao vivo, com o vendedor navegando o WebCorp junto: no caso 06194463, a proteção total avarias foi aceita no mesmo fluxo da reserva, sem fricção, porque o vendedor mostrou o valor incremental (R$ 60-183) no momento exato da decisão. Já ofertas "frias" de migração AD→mensal, feitas em ligações de checagem de carteira, têm taxa de aceite bem mais baixa (a maioria recusada por incerteza de demanda futura).

**(5) Mapa de produto por situação**
- "Cliente calcula km manualmente para saber quando está perto do limite" → ofereça **PR3 Telemetria**, porque automatiza esse controle e evita a confusão de comunicação vivida pelo cliente 05275842 (agência avisando substituição, condutor entendendo como devolução).
- "Cliente reclama de franquia/cobrança alta de sinistro" → ofereça **PR4 Proteção Total Avarias**, como fez a vendedora no caso 05878806 — mas com timing melhor (não no meio da disputa ainda não resolvida, e sim depois de fechar a apuração, para não soar como venda em cima do problema).
- "Contrato AD ultrapassou o prazo e está custando mais que o mensal equivalente" → ofereça **PR1** (migração para mensal), como em 05809062 e 06356330 — mostrando o valor em R$ concreto converte melhor do que citar percentual.
- "Cliente menciona contrato de longo prazo/frota própria/personalização" → explore **PR12 Gestão de Frotas**; no lote, o cliente 05624661 chegou a perguntar sobre 36 meses e a conversa não aprofundou o motivo antes de aceitar o "não" inicial.
- "Cliente relata km excedente frequente como motivo de não migrar para mensal" → ofereça **PR6** (plano de km maior) antes de desistir da migração, como poderia ter sido feito em 05432425.
- "Reserva de picapes/veículos em volume para operação recorrente (terceirização, obra, frota móvel)" → tratar como conta-chave e oferecer **PR7** (mensal fixo de prazo mais longo) proativamente, como já é feito parcialmente no caso 06252636 — mas priorizando primeiro resolver a fricção de P10 para não perder o cliente antes de converter a oferta.

---

## Observações livres
O lote é dominado por dois tipos de ligação: (a) manutenção de carteira/apresentação de novo executivo, em geral curtas e sem sinal de problema ou produto, e (b) atendimentos operacionais de reserva/cadastro/sinistro, onde se concentra praticamente toda a atividade de P3 e P7. O padrão de cross-sell mais bem-sucedido do lote acontece quando o vendedor está literalmente dentro do fluxo de reserva com o cliente (06194463, 06252636) — ali a proteção complementar e adicionais (limpeza, condutor extra) são aceitos com naturalidade. Fora desse contexto, ofertas de migração AD→mensal são o cross-sell mais tentado (7 vezes) mas o menos convertido na própria ligação, quase sempre adiado para aprovação interna do cliente ou recusado por incerteza de demanda. O caso mais crítico do lote combina P3 e P7 ao mesmo tempo: 06252636, onde um cliente de alto volume esbarra numa falha sistêmica de reserva (P10) e a segunda ligação termina em atrito real, sem venda e com risco concreto de churn — prioridade clara para operações antes de qualquer esforço comercial adicional nessa conta.
