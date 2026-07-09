# Lote 02 — Exploração P3+P7

## Resumo do lote
- Total de ligações no lote: 38
- Ligações da BASE_ANTIGA_1275: 6
- Ligações do NOVO_LOTE_5348: 32
- Nota: ~8 ligações são "vazias" para classificação (correio de voz, contato ausente/em reunião, espera em URA, follow-up de cortesia) — os números abaixo refletem as ~30 com conteúdo.

## P3 — Problemas recorrentes (tabela de frequência)
| Código | Categoria | Ocorrências | Resolvido na ligação (SIM/NAO/PARCIAL — contagem) | Escalou (contagem por destino) |
|---|---|---|---|---|
| P1 | Acesso/sistema (portal, senha, biometria) | 6 | SIM 2 / PARCIAL 4 / NAO 0 | 1 (time interno de acessos) |
| P2 | Faturamento/cobrança | 4 | SIM 1 / PARCIAL 2 / NAO 1 | 1 (diretoria/coordenação) |
| P3 | Multa/infração | 1 | SIM 1 | nao_escalou |
| P4 | Manutenção/substituto | 1 | NAO 1 (orientado a acionar 0800) | 1 (0800) |
| P5 | Condutor/cadastro | 4 | SIM 2 / PARCIAL 1 / NAO 1 | 1 (0800/assistência ao cliente) |
| P6 | Km excedente | 0 | — | — |
| P7 | Disponibilidade | 0 | — | — |
| P8 | Franquia/agência | 0 | — | — |
| P9 | Sinistro | 0 | — | — |
| P10 | Reserva/sistema (erro em reserva, prorrogação, tag, instabilidade) | 5 | SIM 1 / PARCIAL 4 / NAO 0 | 3 (chamado interno/IT; apoio interno; central de reservas + time da plataforma) |
| P11 | Outro (tarifa dinâmica alta em feriado; e-mail de pesquisa não entregue) | 2 | PARCIAL 1 / NAO 1 | nao_escalou |

Leitura direcional: P1 + P10 (acesso e falhas de portal/reserva) somam 11 das ~23 ocorrências de problema — quase metade do lote. Muitos "PARCIAL" são o vendedor assumindo a correção fora da ligação (chamado, WhatsApp, retorno prometido).

## P3 — Exemplos
- **Cliente 25203214** (P10): cliente prorrogou 1 dia pelo portal e o sistema gravou devolução em **2031**, convertendo a locação em mensal. Vendedor explicou a regra dos 30 dias, garantiu recobrança como diária pelo "espelho" da reserva e abriu chamado interno por erro sistêmico. Resolução parcial, mas com forte tranquilização ("estou te dando minha palavra").
- **Cliente 26339122** (P5): CPF do condutor bloqueado impediu a reserva. Vendedor não conseguiu resolver internamente: "para ele poder retirar o veículo, ele vai ter que ligar lá na assistência ao cliente... a Localiza bloqueia e o CPF não pode ser nem condutor". Escalou para 0800.
- **Cliente 22027180** (P2): cliente abriu contrato "mensal fixo" em vez de "flexível" e levou multa; pediu estorno. Vendedor: "normalmente não tem o que fazer... mas amanhã cedinho eu vou conversar com a minha diretoria". Não resolvido na ligação, escalado à diretoria.

## P7 — Cross-sell/Upsell (tabela de frequência)
| Código | Produto | Vezes mencionado | Vezes ofertado ativamente | Janelas perdidas identificadas |
|---|---|---|---|---|
| PR1 | Aluguel mensal leve (core) | ~19 | 7 | 0 |
| PR2 | Aluguel pesado | 0 | 0 | 0 |
| PR3 | Telemetria | 0 | 0 | 0 |
| PR4 | Proteção total | 3 | 1 | 0 |
| PR5 | Upgrade categoria | 1 | 0 | 0 |
| PR6 | Km adicional | 2 | 0 | 0 |
| PR7 | Contrato anual | 1 ("mensal até 12 meses") | 0 | 0 |
| PR8 | Elétrico | 0 | 0 | 0 |
| PR9 | ZARP | 0 | 0 | 0 |
| PR10 | Meoo/assinatura | 5 | 0 | 3 |
| PR11 | Seminovos | 0 | 0 | 0 |
| PR12 | Gestão de frotas | 1 | 0 | 1 |

## P7 — Exemplos
- **Oferta ativa bem feita — Cliente 07448263 (vendedora Aline)**: cliente GF sem histórico RAC recebeu oferta estruturada de cashback de R$ 1.000 na fatura GF + upgrade Platinum para incentivar a primeira locação diária/mensal. Conduziu objeções ("se o aluguel for menos de mil?"), enviou login e reset de senha na hora. Melhor oferta do lote.
- **Oferta ativa de proteção — Cliente 27299074**: durante reserva mensal assistida no WebCorp, o vendedor sugeriu ativamente a cobertura ampliada: "te sugiro colocar ampliado, porque ela cobre até 100 mil [terceiros]... aumenta 60 reais". Upsell de proteção (PR4) no fluxo natural da reserva.
- **Janela perdida — Cliente 26382175**: cliente declarou "semana que vem eu vou cadastrar minha outra empresa... até vou pegar um carro por assinatura na outra empresa". Vendedora respondeu apenas "aí você avisa a gente" — nenhuma oferta/encaminhamento de assinatura (PR10) foi feito.
- **Janela perdida — Cliente 27337310**: cliente disse estar avaliando "trocar meu carro por um carro novo [ou] alugar um carro" — abertura clara para assinatura/contrato de longo prazo (PR10/PR7); vendedor só citou a locação mensal RAC genérica.

## Observações livres
Boa parte do lote é contato proativo de carteira (apresentação de gestor, sondagem de demanda, reativação de cadastro parado), e nesses contatos dois clientes revelaram perda para concorrência (Volkswagen e Movida) sem que o vendedor sondasse o que fechou ou contra-ofertasse. O padrão dominante de atendimento é "assumir a dor" via WhatsApp pessoal do gestor ("me manda um oi", "eu faço a prorrogação para você") — resolve bem no curto prazo, mas concentra o relacionamento na pessoa e mascara falhas recorrentes de portal (P1/P10). Cross-sell fora do core é quase inexistente: assinatura/Meoo aparece 5x na boca do cliente e 0x como oferta do vendedor.
