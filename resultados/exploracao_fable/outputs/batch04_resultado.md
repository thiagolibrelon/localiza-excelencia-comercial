# Lote 04 — Exploração P3+P7

## Resumo do lote
- Total de ligações no lote: 38
- Ligações da BASE_ANTIGA_1275: 8
- Ligações do NOVO_LOTE_5348: 30

## P3 — Problemas recorrentes (tabela de frequência)
| Código | Categoria | Ocorrências | Resolvido na ligação (SIM/NAO/PARCIAL — contagem) | Escalou (contagem por destino) |
|---|---|---|---|---|
| P1 | Acesso/sistema (portal, senha, biometria) | 8 | SIM 4 / PARCIAL 4 / NAO 0 | nao_escalou 8 |
| P2 | Faturamento/cobrança | 4 | SIM 1 / PARCIAL 2 / NAO 1 | financeiro (transferência) 1; e-mail assistência clientes 1; nao_escalou 2 |
| P3 | Multa/infração | 0 | — | — (1 caso citado como "multa" era na verdade km cedido → contado em P6) |
| P4 | Manutenção/substituto | 1 | SIM 1 | nao_escalou 1 |
| P5 | Condutor/cadastro | 7 | SIM 4 / PARCIAL 3 / NAO 0 | 0800 1; nao_escalou 6 |
| P6 | Km excedente | 4 | SIM 1 / PARCIAL 2 / NAO 1 | e-mail assistência clientes 1; nao_escalou 3 |
| P7 | Disponibilidade | 4 | SIM 1 / PARCIAL 2 / NAO 1 | nao_escalou 4 |
| P8 | Franquia/agência | 1 | PARCIAL 1 | nao_escalou 1 |
| P9 | Sinistro | 1 | (relato histórico — franquia de avaria cobrada meses depois, já paga) | nao_escalou 1 |
| P10 | Reserva/sistema | 4 | SIM 3 / NAO 1 | central 0800 1; nao_escalou 3 |
| P11 | Outro (tag pedágio, telemetria pendente, confusão de plataformas, troca de executivo) | 4 | SIM 3 / PARCIAL 1 | e-mail interno/IT 1; nao_escalou 3 |

**Leitura direcional:** P1 (acesso/senha/biometria) é disparado o problema mais frequente — 8 de 38 ligações (~21%) têm o vendedor atuando como helpdesk de WebCorp, quase sempre resolvendo em linha sem escalar. P5 (cadastro/condutor) vem em segundo. Cobranças contestadas (P2+P6) são as únicas que saem NAO-resolvidas ou escaladas.

## P3 — Exemplos
- **Cliente 20371206** (P2+P6, NAO resolvido, escalou): fatura veio R$ 4.800 vs. ~R$ 3.300 habituais por 3.192 km cedidos; cliente contesta — "Impossível, porque a gente ficou em casa com esse carro parado na garagem". Vendedora não consegue abrir o chamado; cliente precisa redigir e-mail à assistência.
- **Cliente 10891848** (P2+P6+P8, PARCIAL): agência não soube informar a data-limite de devolução ("não tinha como acessar o contrato"), cliente devolveu 2 dias depois e foi cobrado em diárias extras + km excedente. Vendedora explica que agência só vê o contrato no encerramento; cobrança mantida.
- **Cliente 11615931** (P1, SIM): "faz cinco anos que... a gente não consegue receber a nova senha por conta do e-mail que está desatualizado" — dois CNPJs parados por problema de acesso; resolvido em linha com redefinição + validação Trust.

## P7 — Cross-sell/Upsell (tabela de frequência)
| Código | Produto | Vezes mencionado | Vezes ofertado ativamente | Janelas perdidas identificadas |
|---|---|---|---|---|
| PR1 | Aluguel mensal leve (core) | 16 | 7 | 0 |
| PR2 | Aluguel pesado | 0 | 0 | 1 (cliente 23944469 opera caminhão próprio) |
| PR3 | Telemetria | 2 | 0 | 1 (cliente 27307774, frota de 11 utilitários sem gestão) |
| PR4 | Proteção total / ampliada | 8 | 5 (2 aceitas, 3 recusadas) | 0 |
| PR5 | Upgrade categoria | 2 (ambas como downgrade p/ retenção) | 0 | 0 |
| PR6 | Km adicional | 3 (gestão de franquia, não venda) | 0 | 0 |
| PR7 | Contrato anual | 2 | 0 | 0 |
| PR8 | Elétrico | 0 | 0 | 0 |
| PR9 | ZARP | 0 | 0 | 0 |
| PR10 | Meoo | 0 | 0 | 0 |
| PR11 | Seminovos | 1 | 0 | 2 (clientes 21126648 e 27233552) |
| PR12 | Gestão de frotas | 3 | 1 | 2 (clientes 27307774 e 19279800) |

## P7 — Exemplos
- **Oferta ativa bem feita — Brenda, Cliente 21126648:** cliente elogia atendimento; vendedora sonda demanda, cliente pergunta por picape, ela cota Montana mensal na hora ("3.289,74 já com proteção padrão... disponibilidade para retirar na próxima semana"), formaliza por WhatsApp e agenda follow-up para terça. Ciclo completo de oferta. Porém, na mesma ligação, o cliente perguntou "você tem a venda também?" — Seminovos foi citado de passagem e não houve oferta/encaminhamento (janela PR11 perdida).
- **Oferta ativa bem feita — Graziele, Cliente 07155344:** ao ouvir que o cliente tem frota própria, ofertou gestão de frotas ("substituir essa frota por carros locados anualmente... para quem sabe reduzir custos"). Cliente recusou, mas a janela foi trabalhada — único caso de PR12 ofertado no lote.
- **Janela perdida clara — Cliente 27307774:** vendedora coletou no script que o cliente tem 11 utilitários de frota 100% própria e nenhum alugado — e encerrou sem nenhuma menção a gestão de frotas ou telemetria; ficou só na reserva avulsa.

## Observações livres
Mais da metade do tempo de fala do lote é suporte operacional (acesso WebCorp, biometria, reserva guiada passo a passo em ligações de 10-30 min) — o vendedor funciona como helpdesk, o que gera relacionamento mas quase nenhuma janela de venda é aproveitada durante esses atendimentos longos. Dois casos de vazamento direto de receita PJ→PF: clientes 04506203 (sem disponibilidade no PJ, fechou como pessoa física na hora) e 26621049 (não consegue operar pelo CNPJ e "já vai na pessoa física de novo"). Concorrência apareceu 2x com sensibilidade a preço explícita (Movida a R$ 2.890 vs. cotação de ~R$ 5 mil no cliente 27304203; Unidas no 08113560) — o lote sugere que recotação/downsell rápido é a resposta padrão, sem defesa estruturada de valor.
