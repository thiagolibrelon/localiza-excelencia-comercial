# Lote 004 — Exploração P3+P7

## Resumo do lote
- Total de ligações no lote: 38
- Ligações da BASE_ANTIGA_1275: 38 (100% — este lote não contém ligações do NOVO_LOTE_5348)
- Sentimento: 38/38 marcadas como POSITIVE (nenhuma NEGATIVE/NEUTRO neste lote)
- Ligações "vazias" para classificação (correio de voz/PABX sem transferência, contato ausente/em reunião, reagendamento sem conteúdo de negócio): 11 — Clientes 04422452, 04428124, 04531149 (ligação de 84s), 04754516, 04836169, 04882635 (ligação de 54s), 04968336, 04996114 (ligação ruim, sem conteúdo aproveitável), 05104534, 05113579 (ligação de 25s), 05260852.
- As análises abaixo refletem as ~27 ligações com conteúdo substantivo (17 clientes únicos, vários com 2-3 ligações no período 01–05/06).

## P3 — Problemas recorrentes (tabela de frequência)
| Código | Categoria | Ocorrências | Resolvido na ligação (SIM/NAO/PARCIAL — contagem) | Escalou (contagem por destino) |
|---|---|---|---|---|
| P1 | Acesso/sistema (troca de gestor sem acesso, biometria trust, dois portais PF x PJ, reset de senha travando) | 6 | SIM 1 / PARCIAL 4 / NAO 1 | 0 (tudo resolvido pelo próprio vendedor ou deixado para acompanhamento via WhatsApp) |
| P2 | Faturamento/cobrança (crédito não libera após pagamento, cobrança não identificada, dúvida de ciclo de fatura, negociação de prazo) | 6 | SIM 2 / PARCIAL 2 / NAO 2 | 2 (financeiro interno / suporte da Localiza) |
| P3 | Multa/infração | 1 | SIM 1 | nao_escalou |
| P4 | Manutenção/substituto | 0 | — | — |
| P5 | Condutor/cadastro (reserva em nome errado, troca de condutor/gestor) | 5 | PARCIAL 5 | 0 (ajustes feitos na hora pelo próprio vendedor) |
| P6 | Km excedente | 0 | — | — |
| P7 | Disponibilidade (modelo específico não garantido, grupo V esgotado) | 2 | PARCIAL 2 | 0 |
| P8 | Franquia/agência | 0 | — | — |
| P9 | Sinistro | 0 | — | — |
| P10 | Reserva/sistema (erro "não permitido abertura de reserva para esse cliente") | 1 | NAO 1 | 0 (vendedor ficou de verificar internamente e retornar) |
| P11 | Outro (cadastro de condomínio bloqueado por exigir inscrição estadual, campo incompatível com o tipo de entidade) | 1 | NAO 1 | 0 |
| P12 | Manipulação de pesquisa/NPS | 0 | — | — |

Leitura direcional: neste lote não houve nenhuma escalada formal a 0800 ou supervisão — todos os casos foram resolvidos na hora ou empurrados para acompanhamento pessoal do próprio vendedor (WhatsApp/e-mail), o mesmo padrão de "concierge manual" observado em lotes anteriores. P1+P2 concentram 12 das 22 ocorrências (~55%) — acesso/portal e crédito/cobrança seguem sendo a dupla dominante de fricção.

## P3 — Exemplos
- **Cliente 04393256** (P1+P5, duas ligações — 233s e 456s): novo gestor de frota (Alessandro) assumiu a carteira após saída dos antigos responsáveis (Luiz, Guilherme, André, Evelyn) e não tem acesso ao WebCorp. O vendedor explica que a liberação exige e-mail/biometria trust de um dos sócios (Isabela ou Tiago), não aceita procuração isolada: "mesmo que você tenha uma procuração, ainda assim a gente precisa que um dos sócios da empresa emita uma autorização". Na segunda ligação o processo segue em curso, dependente da validação do sócio no mesmo dia.
- **Cliente 04857542** (P1, duas ligações — 399s e 291s): cliente tenta migrar um contrato via seguro para mensal PJ e entra sem perceber no portal de pessoa física em vez do PJ ("Você está no portal da pessoa física, não tá?"). O vendedor conduz a correção passo a passo por WhatsApp/celular ao longo de duas ligações até concluir a reserva mensal flexível com sucesso — exemplo direto da categoria "dois portais distintos" do taxonomia P1.
- **Cliente 05096701** (P1+P10+P11, 647s): ligação mais longa do lote, com três problemas emaranhados — reset de senha via QR code que trava, cadastro de atualização bloqueado porque o formulário exige "inscrição estadual" e o cliente é um condomínio (não possui esse dado), e um erro de sistema "não é permitido abertura de reserva para esse cliente" causado por confusão entre dois CNPJs do mesmo grupo (um de "investimento", outro de "condomínio"). Nenhum dos três foi resolvido na ligação; a transcrição termina em meio à investigação do vendedor.
- **Cliente 04305366** (P2, duas ligações — 83s e 160s): cliente inadimplente relata que equipe de remoção já estava no local para retirar o veículo; pede para o vendedor "segurar" a remoção até o pagamento cair à tarde. Na ligação seguinte, mesmo após o cliente comprovar o pagamento de todas as faturas ("ele já registrou todas as faturas como paga"), o limite de crédito continua bloqueado no sistema — vendedor não resolve e orienta o cliente a acionar o suporte diretamente.
- **Cliente 04933986** (P3, único caso de multa do lote): cliente pergunta como indicar o condutor real infrator. Vendedor explica o processo com precisão (baixar relatório de condutores no portal de faturamento, preencher, assinar conforme CNH, anexar CNH, enviar por e-mail) e resolve integralmente na ligação, sem necessidade de escalar.

## P7 — Cross-sell/Upsell (tabela de frequência)
| Código | Produto | Vezes mencionado | Vezes ofertado ativamente | Janelas perdidas identificadas |
|---|---|---|---|---|
| PR1 | Aluguel mensal leve (core) | ~22 | 6 | 1 |
| PR2 | Aluguel pesado | 0 | 0 | 0 |
| PR3 | Telemetria | 0 | 0 | 0 |
| PR4 | Proteção total / avarias | 3 | 2 | 0 |
| PR5 | Upgrade de categoria | 2 (discussão de grupo V/VP e B/C, sem upsell efetivo) | 0 | 0 |
| PR6 | Km adicional | 1 | 0 | 0 |
| PR7 | Contrato anual | 1 | 1 | 0 |
| PR8 | Veículos elétricos | 0 | 0 | 0 |
| PR9 | ZARP | 0 | 0 | 0 |
| PR10 | Meoo | 0 | 0 | 0 |
| PR11 | Venda de Seminovos | 0 | 0 | 0 |
| PR12 | Gestão de frotas | 2 | 0 | 1 |

## P7 — Exemplos
- **Oferta ativa bem-sucedida — Cliente 04919242**: durante contato de acompanhamento de carteira, cliente revela que usa apenas 2 carros próprios de passeio para deslocamento entre cidades. O vendedor identifica a janela na hora e oferece PR1 com proteção e manutenção incluídas a partir de R$ 2.100/mês, argumentando que "o custo acaba ficando bem maior do que manter com a própria terceirizada" — envio de proposta por e-mail combinado. Melhor conversão potencial do lote.
- **Oferta ativa aceita — Cliente 04506203**: no fluxo de reserva assistida por telefone, o vendedor sugere ativamente a proteção total de avarias ("é bom colocar esse proteção total... isso é proteção total de avarias") e o cliente aceita de imediato — upsell de PR4 incorporado ao fluxo natural da reserva.
- **Demanda explícita do cliente — Cliente 05018875** (PR7): cliente pede diretamente uma cotação para contrato de 1 ano ou mais (com desconto), veículo específico (Nivus, cor branca, automático). Vendedor monta a proposta com desconto adicional na hora — cross-sell praticamente auto-gerado pelo cliente, só falta o fechamento.
- **Janela perdida — Cliente 05204346**: cliente revela que a empresa vendeu toda a frota própria porque os carros ficavam parados gerando despesa de pedágio e seguro ("resolvemos virar a receita, mudar a despesa para receita"). O vendedor apenas registra que "está tudo parado" e encerra a ligação sem sondar se existe demanda esporádica futura (viagens pontuais) que poderia ser atendida por locação avulsa — oportunidade de reengajamento não explorada.
- **Janela perdida — Cliente 05218056** (PR1/PR12): cliente da unidade de Florianópolis informa que a empresa não tem carros de frota na região e resolve deslocamentos curtos via agência de viagens terceirizada, não diretamente com a Localiza. O vendedor apenas confirma que "vocês estão muito bem assegurados com as agências de viagens" e se despede, sem oferecer abertura de conta RAC direta para reduzir a intermediação.
- **Oferta ativa recusada — Cliente 05034873**: vendedora detalha com números a conversão de diário para mensal (de R$1.536 em 10 dias para R$3.437,48 em 30 dias com proteção total incluída), mas o cliente explica que o uso é sempre curto e esporádico (técnico em viagem), então a oferta não converte — perfil de demanda incompatível com o produto ofertado, não falha de condução.

## Respostas — P3 (Problemas recorrentes)
1. **Quais problemas são sistêmicos?** P1 (processo de troca/validação de gestor via biometria trust, e a existência de dois portais distintos PF/PJ que confundem o próprio usuário) e P2 (crédito que não atualiza mesmo após confirmação de pagamento, e o ciclo de fatura de 30 dias a partir da retirada, não do fechamento do mês) — ambos aparecem em clientes diferentes e não dependem de um erro pontual de um único atendimento.
2. **Quais o vendedor resolve sem escalar, e como?** P3 (explicando o processo de indicação do condutor infrator passo a passo), P2 quando é só uma dúvida de regra de negócio (ciclo de fatura, negociação de prazo sem juros) e P5 (refazendo a reserva na hora com os dados corretos). Em todos esses casos o vendedor resolve com explicação detalhada e ação imediata no próprio sistema/portal.
3. **Quais escala desnecessariamente?** Nenhuma escalada formal (0800/supervisão) ocorreu neste lote — o padrão foi resolver na hora ou assumir pessoalmente o acompanhamento via WhatsApp. Isso é um ponto de atenção inverso: casos como o do Cliente 05096701 (erro sistêmico de bloqueio de reserva por confusão de CNPJ) provavelmente deveriam ter sido escalados formalmente a um time técnico em vez de ficarem com "eu vou ver aqui... eu te ligo já" do próprio vendedor.
4. **Qual tem maior impacto negativo na relação?** P1 ligado a troca de gestor/acesso (Cliente 04393256) e a confusão de portais (Cliente 04857542) — são os casos que mais consomem tempo do executivo (399s+291s e 233s+456s) e geram desgaste tanto para o cliente quanto para o vendedor, além do risco de erro humano em processos manuais.
5. **O que produto/operações deveria priorizar?** (a) Unificar ou deixar mais claro visualmente a diferença entre portal PF e portal PJ mensal; (b) simplificar/automatizar a liberação de acesso para novos gestores de frota quando os antigos saem da empresa; (c) revisar o formulário de atualização cadastral para aceitar entidades sem inscrição estadual (condomínios, associações); (d) investigar por que o limite de crédito não atualiza em tempo real após confirmação de pagamento.

## Respostas — P7 (Cross-sell/Upsell)
1. **Qual produto tem maior gap janela×oferta?** PR7 (contrato anual) e PR12 (gestão de frotas) têm o maior gap proporcional: aparecem pouquíssimas vezes, mas quando aparecem são sinais fortes (cliente pedindo diretamente um contrato de 1 ano, ou já sendo assinante de gestão de frotas questionando cobertura de outra região) e não são explorados para cross-sell adicional. Em volume absoluto, PR1 também tem uma janela perdida relevante (Cliente 05204346, que vendeu a frota e não foi sondado sobre demanda esporádica futura).
2. **Quais clientes têm maior potencial de expansão imediata?** Cliente 05018875 (já pediu contrato anual, falta só fechar a proposta), Cliente 04919242 (usa carro próprio, proposta de mensal já em andamento por e-mail) e Cliente 05021060 (já é assinante de PR12/gestão de frotas, pode crescer para locação avulsa complementar).
3. **Algum produto nunca mencionado?** Sim — PR2 (aluguel pesado), PR3 (telemetria), PR8 (elétricos), PR9 (ZARP), PR10 (Meoo) e PR11 (seminovos) não aparecem em nenhuma das 38 ligações do lote.
4. **Qual perfil de cliente mais compra cross-sell quando ofertado?** Clientes que já estão no meio de uma reserva ativa e recebem a oferta no fluxo natural (ex: proteção total durante a montagem da reserva, Cliente 04506203) topam de imediato. Já clientes com uso esporádico/curto e imprevisível (técnicos em viagem, sinistros pontuais) recusam consistentemente a migração para mensal, mesmo com desconto demonstrado (Clientes 04882635, 05034873, 05189056).
5. **Mapa de produto por situação:**
   - "Cliente usa carro próprio para deslocamento ocasional entre cidades → ofereça PR1 mensal com manutenção e proteção incluídas, porque reduz o custo fixo frente à frota própria (Cliente 04919242)."
   - "Cliente já é assinante de PR12 (gestão de frotas) e menciona precisar de carro avulso para viagem/quebra → ofereça PR1 esporádico complementar no mesmo contato (Cliente 05021060)."
   - "Cliente pede prazo de locação longo (1 ano ou mais) → ofereça PR7 com desconto por fidelização, aproveitando o pedido já explícito (Cliente 05018875)."
   - "Cliente relata que resolve locações via agência de viagens terceirizada → ofereça onboarding direto de conta RAC para reduzir a intermediação (Cliente 05218056)."
   - "Cliente relata que vendeu/encerrou a frota própria → antes de encerrar o contato, sonde se ainda existe demanda esporádica residual (viagens, picos) que justifique locação avulsa (Cliente 05204346)."

## Observações livres
Este é o primeiro lote da série sem nenhuma ligação do NOVO_LOTE_5348 e com 100% de sentimento POSITIVE — o que também limita a amostra de atritos mais graves (nenhum sinistro, nenhuma franquia de agência, nenhum caso de manipulação de NPS). Mesmo assim, o padrão de "vendedor como concierge manual do self-service" se repete: em quase todos os casos de acesso/portal (Clientes 04393256, 04475681, 04857542, 05096701) o executivo assume pessoalmente a tarefa de destravar login, redefinir senha ou orientar passo a passo por WhatsApp, em vez de o processo ser resolvido de forma automática pelo próprio portal. O lote também confirma um padrão qualitativo já visto em rodadas anteriores: ofertas de cross-sell bem argumentadas (com números concretos, como em 04919242 e 05034873) nem sempre convertem porque dependem do perfil de demanda do cliente — a maior alavanca de receita parece estar menos em "vender melhor" e mais em identificar, no início da ligação, qual cliente tem padrão de uso compatível com mensal/anual antes de gastar tempo com a simulação completa.
