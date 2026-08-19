# Lote 003 — Exploração P3+P7

## Resumo do lote
- Total de ligações no lote: 38
- Ligações da BASE_ANTIGA_1275: 38 (o lote inteiro é da base antiga; nenhuma do NOVO_LOTE_5348)
- Sentimento: todas marcadas como POSITIVE no cabeçalho (o rótulo é do STT, não reflete o conteúdo — ver Cliente 03096291 e 03964949, que têm forte atrito).
- Nota: ~11 ligações são "vazias" para classificação (contato ausente/em reunião, correio de voz, morte em espera de URA, transferência de ramal). São elas: 02631583 (Lucas ausente), 02672458 (Janaína no almoço), 03096291/37s (Arnaldo ausente), 03289309 (Daniela ausente, tratado por WhatsApp), 03302117 (transferência p/ SP), 03638154 (cliente ocupado), 04049506 (Vanderlei em viagem), 04078679 (morreu em espera de URA), 04199141 (Nilson saiu — turnover, transferência), 04301889/81s (transferência errada de ramal). Os números abaixo refletem as ~27 ligações com conteúdo.
- Duas ligações "quase vazias" mas com sinal útil: 02742076 e 02856182 (contato ausente, mas o vendedor sondou frota própria / prorrogação).
- Vendedores identificados: Bruna (3), Amanda (5), Everton (2), Ana Paula, Cristina (2), Gabriela (2), Stephanie (2), Carla, Matheus (2), Keyla, Andresa, Ângelo (2), Victor, Lucas (2 — Delta), Thalita, Keila, Aline, Cristiane, Pedro (2), Rodrigo.

## P3 — Problemas recorrentes (tabela de frequência)
| Código | Categoria | Ocorrências | Resolvido na ligação (SIM/NAO/PARCIAL — contagem) | Escalou (contagem por destino) |
|---|---|---|---|---|
| P1 | Acesso/sistema (portal, senha, biometria, e-mail vinculado a outra empresa) | 5 | SIM 1 / PARCIAL 4 / NAO 0 | 1 (suporte interno de cadastro/acessos) |
| P2 | Faturamento/cobrança (valor de diária, indenização, inadimplência, CNPJ de agência) | 7 | SIM 1 / PARCIAL 2 / NAO 4 | 4 (assistência ao cliente 2; financeiro/0800 2) |
| P3 | Multa/infração | 2 | SIM 1 / PARCIAL 1 | nao_escalou |
| P4 | Manutenção/substituto | 0 | — | — |
| P5 | Condutor/cadastro (troca de titular, remover gestor demitido, criar acesso) | 3 | PARCIAL 3 | 2 (suporte interno — vendedor apoiando executiva de férias) |
| P6 | Km excedente | 0 (mencionado como dúvida em 03289309 e 04301889, sem cobrança em disputa) | — | — |
| P7 | Disponibilidade | 1 | PARCIAL 1 | 1 (supervisora da agência) |
| P8 | Franquia/agência (fatura em CNPJ de outra corporação/agência) | 1 | PARCIAL 1 | 1 (assistência ao cliente) |
| P9 | Sinistro (avaria de pneu/para-choque, fatura de indenização) | 1 | NAO 1 | 1 (assistência ao cliente / emergencial) |
| P10 | Reserva/sistema (delay de integração, grupo errado, reserva não confirmada pela agência) | 3 | PARCIAL 3 | 2 (agência/central) |
| P11 | Outro (tarifa diária flutuante altíssima em feriado; e-mail de pesquisa não entregue; veículo bloqueado por inadimplência na estrada) | 4 | PARCIAL 1 / NAO 3 | 2 (financeiro/0800) |
| P12 | Manipulação de pesquisa/NPS (vendedor pede/induz resposta da pesquisa) | 2 | NAO 2 (por definição) | nao_escalou |

Leitura direcional: **P2 (faturamento) é o problema dominante do lote — 7 ocorrências, e 4 delas NÃO resolvidas na ligação**, o pior índice de resolução do lote. Junto com P1 (acesso, 5) e P10 (reserva/sistema, 3), atrito de portal + cobrança concentra a maioria das dores. O padrão de resolução é "assumir a dor fora da ligação" (WhatsApp pessoal, chamado interno, retorno prometido) — daí a alta contagem de PARCIAL.

## P3 — Exemplos
- **Cliente 03096291** (P2 + P11): contestação de fatura de 3 diárias a ~R$491/diária num carro popular. Cliente (Ricardo/Arnaldo) alega que o condutor pediu 2 diárias e que o valor é "um absurdo" para um carro de balcão. A vendedora manteve a linha correta ("a diária é flutuante igual passagem aérea, você aceitou o valor ao fechar a reserva; não houve erro da Localiza para eu contestar") mas prometeu tentar contestação assim mesmo. **Não resolvido; cliente ameaçou "cortar a Localiza daqui".** Maior atrito relacional do lote apesar do rótulo POSITIVE.
- **Cliente 03964949** (P9 + P2): fatura de indenização de R$1.313,76 por avaria (pneu rasgado em buraco + para-choque) num veículo com **proteção básica**, que não cobre roda/pneu. Cliente alega que nunca foi avisado e que o condutor não acionou a assistência na hora. Vendedora explicou o fluxo (sinistro → acionar emergencial primeiro) e que a contratação da proteção básica foi feita pelo gestor anterior (Evandro). **Não resolvido na ligação; orientou contestar via assistência ao cliente, com boleto vencendo no mesmo dia** — prometeu tentar prorrogar o boleto.
- **Cliente 04305366** (P2 + P11): veículo bloqueado por inadimplência parado na BR-116 na Bahia; cliente pediu desbloqueio emergencial. Vendedor (Pedro) escalou ao financeiro e retornou: **faturas vencidas desde 15/04, sem alçada para desbloquear** — orientou pagar e acionar 0800 para reboque. NAO resolvido, escala correta mas desfecho ruim para o cliente.
- **Cliente 03096291** (P3 — positivo): em outra ligação do mesmo cliente, a vendedora **conseguiu o cancelamento de uma multa** indevida (histórico mostrou contrato flexível, não fixo). SIM, resolvido — melhor desfecho de P3 do lote.
- **Cliente 03561228** (P12): a vendedora Amanda ligou explicitamente para pedir que o cliente respondesse a pesquisa de satisfação ("você recebeu um e-mail... a sua opinião é muito importante... consegue dar essa forcinha?"). O e-mail sequer havia chegado (P11). Também em **03736724**, Andresa encerra com "vou te mandar a pesquisa pra você me avaliar". Integridade do indicador comprometida.

## P7 — Cross-sell/Upsell (tabela de frequência)
| Código | Produto | Vezes mencionado | Vezes ofertado ativamente | Janelas perdidas identificadas |
|---|---|---|---|---|
| PR1 | Aluguel mensal leve (core) | ~11 | 6 | 0 |
| PR2 | Aluguel pesado | 0 | 0 | 0 |
| PR3 | Telemetria | 0 | 0 | 1 (multa/indicação de condutor recorrente → 03736724) |
| PR4 | Proteção total / cobertura de avarias | 4 | 1 | 1 (sinistro com proteção básica → 03964949) |
| PR5 | Upgrade de categoria | 1 | 0 | 0 |
| PR6 | Km adicional | 3 | 1 | 0 |
| PR7 | Contrato anual / mensal fixo (3/6/9/12 meses) | 6 | 4 | 1 (cliente com campanhas 4x/ano → 04090518) |
| PR8 | Veículos elétricos | 0 | 0 | 0 |
| PR9 | ZARP | 0 | 0 | 0 |
| PR10 | Meoo / assinatura (Localiza Meu) | 1 | 0 | 0 |
| PR11 | Venda de Seminovos | 0 | 0 | 0 |
| PR12 | Gestão de frotas | 0 | 0 | 3 (frota própria revelada → 02742076, 03423413, 03794445) |

## P7 — Exemplos
- **Melhor venda consultiva — Cliente 04198180 (vendedor Lucas / conta Delta Service)**: fechou negociação de contrato de 12 meses para 2 veículos (grupo CE, 2.000 km), e agregou uma dica genuína de economia — abrir o contrato em Belo Horizonte (tarifa mais barata) e deslocar para Ouro Branco, reduzindo a mensalidade recorrente. Verificou crédito (R$50 mil), simulou na WebCorp, capturou expansão futura (cliente sinalizou picape e "estrada" para a semana seguinte). PR7 + PR1 bem executados. Referência do lote.
- **Oferta ativa proativa — Cliente 02600832 (Bruna)**: sem que o cliente pedisse, ofereceu migrar do mensal flexível para o mensal fixo (planos 3/6/9/12 meses) e condicionou desconto ao volume ("quanto maior a frota, melhor eu mexo no custo"), aproveitando que o cliente sinalizou possível retorno com +1 ou 2 carros vindos de outra locadora. PR7.
- **"Consultoria gratuita" — Cliente 04090518 (Victor)**: ligou só para avisar que o contrato AD já estava no mesmo valor do mensal e que o cliente poderia ficar +10 dias pelo mesmo preço ("é prestar uma consultoria gratuita"). Cliente recusou (já tinha resolvido em outro lugar), mas revelou que aluga "em campanhas 4x no ano" — **janela para PR7 (contrato recorrente/anual) que não foi trabalhada**.
- **Upsell de proteção bem feito — Cliente 04224398 (Keila)**: numa cotação de estrada, ofertou ativamente a proteção total avaria e comparou com honestidade mensal comum vs. assinatura (Localiza Meu), admitindo que às vezes o mensal sai mais barato que a assinatura. PR4 + PR1.
- **Janela perdida clássica — Cliente 03964949 (sinistro)**: cliente acabou de tomar uma indenização de R$1.313 porque estava na proteção básica. A vendedora explicou tecnicamente a diferença de coberturas, mas **não converteu a dor numa oferta de upgrade para proteção total (PR4) nas próximas locações** — foco ficou 100% na contestação.
- **Janelas perdidas de gestão de frota — Clientes 02742076, 03423413, 03794445**: os três revelaram operar com **frota própria** ("estamos com os próprios também"; "a gente usa realmente pela frota"). Nenhum vendedor ofereceu PR12 (gestão de frotas) nem PR2 — o dado competitivo mais valioso do lote foi colhido e descartado.

## Perguntas finais — P3
1. **Quais problemas são sistêmicos?** P2 (faturamento) e P1/P10 (acesso e reserva). Recorrem em vários clientes, com raízes estruturais: tarifa diária flutuante mal comunicada (03096291), proteção contratada por gestor anterior que o cliente atual desconhece (03964949), e-mail/login preso a empresa anterior (02611182), biometria de condutor demitido travando a conta (02675454), delay de integração no portal (02909699). São falhas de produto/comunicação, não de atendimento pontual.
2. **Quais o vendedor resolve sem escalar, e como?** Explicações de fatura com base contratual (03561228 — as 4 diárias dos meses de 30 dias; 03346536 — desconsiderar e-mail automático de fim de contrato), cancelamento de multa via histórico (03096291), e a maioria dos ajustes de cadastro/acesso via WhatsApp pessoal e reset de senha. O método dominante é "assumir a operação manualmente" fora da ligação.
3. **Quais escala desnecessariamente?** Poucos casos de escalonamento desnecessário — os escalonamentos foram, em geral, corretos (avaria → assistência ao cliente; inadimplência → financeiro; cadastro fora da carteira → executiva responsável/suporte). O gargalo real é o oposto: muita coisa que **deveria** ser self-service acaba manualizada pelo executivo.
4. **Qual tem maior impacto negativo na relação?** P2/P9 nos casos 03096291 (diária de R$491 → ameaça de churn) e 03964949 (indenização-surpresa de R$1.313 com boleto vencendo no dia). Ambos combinam valor inesperado + sensação de não ter sido avisado + desfecho não resolvido. 04305366 (carro bloqueado na estrada por inadimplência) é operacionalmente o mais grave, mas a dívida é do cliente.
5. **O que produto/operações deveria priorizar?** (a) Comunicação proativa da tarifa flutuante e do valor da diária no ato da reserva diária, para matar contestações como a 03096291; (b) alerta/aviso antes de gerar fatura de indenização de avaria, com o detalhamento da cobertura contratada; (c) desvincular login/e-mail de empresa anterior no onboarding (02611182); (d) fluxo automatizado de troca de titular quando o condutor com biometria sai da empresa (02675454); (e) governança do NPS — coibir o pedido de nota (P12), que aparece 2x e inflar o indicador.

## Perguntas finais — P7
1. **Qual produto tem maior gap janela×oferta?** PR12 (Gestão de frotas): 3 janelas claras (frota própria revelada), 0 ofertas. Empatado em relevância com PR4 (proteção total): cliente com sinistro/dano recorrente é o alvo natural e não recebeu oferta. PR3 (telemetria) tem gap conceitual — nenhuma menção, apesar da dor de indicação de condutor/multa (03736724).
2. **Quais clientes têm maior potencial de expansão imediata?** 04198180 (Delta — já fechando 12 meses × 2 veículos e sinalizou picape + estrada); 02600832 (pode trazer +1-2 carros de uma locadora concorrente); 04082544 e 04224398 (cotações ativas de picape/estrada em andamento); 04022717 (viagem longa recorrente, já pediu para o Paraná ~5 mil km).
3. **Algum produto nunca mencionado?** PR2 (pesado), PR8 (elétrico), PR9 (ZARP), PR11 (Seminovos) — zero menções e zero ofertas no lote inteiro. PR3 (telemetria) só aparece como janela perdida, nunca falado.
4. **Qual perfil de cliente mais compra cross-sell quando ofertado?** O cliente com demanda contínua e previsível (Delta, 04198180) fecha PR7/PR1 quando o vendedor traz argumento de custo concreto. O cliente com frota própria + RAC esporádico (02742076, 03794445) NÃO compra core adicional — mas é exatamente o perfil de PR12/PR2, que ninguém tentou. Upsell de proteção (PR4) converte quando ofertado no fluxo da cotação (04224398), não depois do sinistro.
5. **Mapa de produto por situação:**
   - Quando o cliente diz *"temos frota própria / usamos os nossos carros"* → ofereça **PR12 (gestão de frotas)** e **PR2 (pesados)**, porque a frota própria é o principal concorrente do aluguel e a gestão terceirizada é a porta de entrada para converter parte dela.
   - Quando o cliente *renova mensal flexível ou fica 3+ meses* → ofereça **PR7 (mensal fixo 3/6/9/12)**, porque a tarifa menor no plano longo retém e barateia (feito bem em 02600832 e 04198180).
   - Quando o cliente *sofre avaria/sinistro na proteção básica* (03964949) → ofereça **PR4 (proteção total)** para as próximas locações, porque a dor recém-vivida é o melhor argumento de valor.
   - Quando o cliente *reclama de multa/indicação de condutor errado* (03736724) → ofereça **PR3 (telemetria)** e **PR12**, porque rastreio identifica o condutor real e reduz o retrabalho de indicação.
   - Quando o cliente *aluga "em campanhas, 4x por ano"* (04090518) → ofereça **PR7 (contrato anual)**, porque a recorrência previsível já justifica um contrato com tarifa fechada.
   - Quando o cliente *contesta a diária flutuante como cara demais* (03096291) → ofereça migração para **PR1/PR7 mensal com km controlado**, porque o mensal tem valor fixo e resolve a percepção de imprevisibilidade que gera o atrito.

## Observações livres
O lote inteiro é da BASE_ANTIGA_1275 e concentra atendimento de manutenção/suporte, não de venda — o tempo dos executivos vai majoritariamente para contestação de fatura, ensino de portal e atualização de cadastros órfãos (turnover de contato aparece em 02611182, 02675454, 03166514, 04199141, 04198180). O padrão de "concierge manual via WhatsApp pessoal" observado em lotes anteriores se repete: os vendedores assumem prorrogações, resets de senha e reservas que o self-service deveria fazer — resolve no curto prazo, cria dependência e mascara falhas de UX da WebCorp. Dois eventos de alto impacto merecem follow-up: o Cliente 03096291 (diária de feriado a R$491 → ameaça explícita de churn) e o Cliente 03964949 (indenização-surpresa por avaria em proteção básica). O rótulo de sentimento POSITIVE do STT não é confiável — as duas ligações mais tensas do lote estão marcadas como POSITIVE. Inteligência competitiva subaproveitada: pelo menos 3 clientes revelaram frota própria e 1 sinalizou saída de outra locadora, sem que ninguém sondasse preço/condição do concorrente ou ofertasse PR12/PR2.
