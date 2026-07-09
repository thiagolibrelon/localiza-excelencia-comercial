# Lote 09 — Exploração P3+P7

## Resumo do lote
- Total de ligações no lote: 38
- Ligações da BASE_ANTIGA_1275: 8
- Ligações do NOVO_LOTE_5348: 30

Nota: ~14 ligações são puramente relacionais (apresentação de executivo, check-in de carteira, tentativa de contato sem sucesso) e não trazem problema nem oferta relevante.

## P3 — Problemas recorrentes (tabela de frequência)
| Código | Categoria | Ocorrências | Resolvido na ligação (SIM/NAO/PARCIAL — contagem) | Escalou (contagem por destino) |
|---|---|---|---|---|
| P1 | Acesso/sistema (portal, senha, biometria) | 4 | SIM: 4 | nao_escalou: 4 |
| P2 | Faturamento/cobrança | 5 | SIM: 2, PARCIAL: 2, NAO: 1 | canal assistência/e-mail (Asclis): 1; nao_escalou: 4 |
| P3 | Multa/infração | 0 | — | — |
| P4 | Manutenção/substituto | 1 | SIM: 1 (renovação de frota solicitada) | nao_escalou: 1 |
| P5 | Condutor/cadastro | 1 | SIM: 1 | nao_escalou: 1 |
| P6 | Km excedente | 1 | PARCIAL: 1 (recorrente há meses) | canal assistência/e-mail: 1 |
| P7 | Disponibilidade | 2 | PARCIAL: 2 (dependem de retorno da agência) | nao_escalou: 2 (vendedor aciona gerente da agência) |
| P8 | Franquia/agência | 1 | PARCIAL: 1 | nao_escalou: 1 |
| P9 | Sinistro | 1 | PARCIAL: 1 (dúvida esclarecida, cobrança mantida) | 0800: 1 |
| P10 | Reserva/sistema | 5 | SIM: 4, PARCIAL: 1 | nao_escalou: 5 |
| P11 | Outro (limite de crédito) | 3 | SIM: 1, PARCIAL: 2 | supervisora: 1; nao_escalou: 2 |

## P3 — Exemplos
- **Cliente 16742927 (P2)** — Desconto de lavagem especial prometido pela assistência em 02/06 não aplicado na fatura que vence dia 13/06; cliente já havia pedido urgência 2x sem retorno. Executiva verifica o portal na hora ("não foi abatido dentro da fatura, não") e promete forçar prioridade e prorrogação sem juros.
- **Cliente 12175635 (P9)** — Caminhão de terceiro bateu no carro locado, BO indica culpa do terceiro, mas: "mesmo não sendo... nós que pagamos a franquia?" — resposta: "é cobrada a franquia da empresa... a Localiza não vai atrás do terceiro". Orientado a tentar o 0800 de sinistro.
- **Cliente 17812674 (P6)** — "Todos os meses está excedendo... a gente resolve um mês, no outro mês eu tenho problema de novo. Ainda nem consegui resolver do mês 6 e no mês 7 já está com km excedente novamente." Executiva demonstra pelo odômetro que o excedente é real (7 mil km rodados vs 4 mil contratados em 2 meses).
- **Cliente 12936013 (P11)** — Crédito de 100 mil reprovado; executivo pede 80 mil com justificativa incluindo a supervisora e ensina workaround (reserva diária convertida em mensal "porque aí não lê o crédito").

## P7 — Cross-sell/Upsell (tabela de frequência)
| Código | Produto | Vezes mencionado | Vezes ofertado ativamente | Janelas perdidas identificadas |
|---|---|---|---|---|
| PR1 | Aluguel mensal leve (core) | 12 | 5 | 1 |
| PR2 | Aluguel pesado | 1 | 0 | 0 (demanda já em tratativa com outro time) |
| PR3 | Telemetria | 1 | 1 (aceita na hora) | 0 |
| PR4 | Proteção total | 3 | 1 | 0 |
| PR5 | Upgrade categoria | 0 | 0 | 0 |
| PR6 | Km adicional | 1 | 0 | 1 |
| PR7 | Contrato anual / mensal fixo | 4 | 1 | 1 |
| PR8 | Elétrico | 0 | 0 | 0 |
| PR9 | ZARP | 0 | 0 | 0 |
| PR10 | Meoo / assinatura | 2 | 0 | 0 |
| PR11 | Seminovos | 1 | 0 | 1 (fraca — frota própria sem sondagem) |
| PR12 | Gestão de frotas | 5 | 1 | 1 |

## P7 — Exemplos
- **Oferta ativa bem feita — Cliente 26663713 (PR3, vendedora Adriane)** — Cliente pede rastreio dos 4 utilitários novos ("os carros ficam em tempo integral com os funcionários... queria ter um controle maior"); vendedora oferta telemetria na hora com preço claro (R$1,49/dia ≈ R$44,70/mês) e fecha: "então a gente vai contratar esse serviço... coloca nos quatro".
- **Oferta ativa bem feita — Cliente 27297868 (PR1+PR4, vendedor Everton)** — Prospecção de conta nova: mapeia demanda (12 meses, ~800 km/mês), dimensiona pacote de 1.000 km e explica proteção padrão vs. proteção total de avarias com exemplos concretos antes de mandar proposta dupla por WhatsApp.
- **Janela perdida — Cliente 17812674 (PR6)** — Cliente estoura o pacote de 2.000 km/mês todos os meses (3.000 km/mês de excedente comprovado); ninguém oferta upgrade de pacote de km, que resolveria a dor recorrente e capturaria receita previsível.
- **Janela perdida — Cliente 06366924 (PR12/PR11)** — Cliente confirma "tem [frota própria], mas a gente aluga bastante de vocês ainda"; vendedora só anota o contato do responsável e encerra, sem plantar gestão de frotas/terceirização.
- **Janela perdida — Cliente 27173230 (PR7)** — Cliente queria "aquela que era já três meses direto", barrada por limite de crédito; vendedora confirma a reserva avulsa e não tenta ampliar crédito nem recuperar o contrato de 3 meses.

## Observações livres
Limite de crédito é o atrito transversal do lote: aparece em 4 ligações, trava reservas, derruba um contrato de 3 meses e leva um executivo a ensinar workaround (diária→mensal "não lê o crédito") que contorna a política interna. O canal de contestação por e-mail (Asclis/assistência) tem SLA estourado em 3 casos, forçando o executivo de conta a virar despachante de chamados — bom para relacionamento, ruim para custo de atendimento. Chama atenção o volume de pedidos ativos de avaliação/pesquisa de satisfação ao fim das ligações (7+), inclusive em ligações sem resolução concluída.
