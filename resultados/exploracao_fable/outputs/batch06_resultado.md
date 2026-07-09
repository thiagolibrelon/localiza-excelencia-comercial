# Lote 06 — Exploração P3+P7

## Resumo do lote
- Total de ligações no lote: 38
- Ligações da BASE_ANTIGA_1275: 6
- Ligações do NOVO_LOTE_5348: 32

Nota: ~10 ligações são contatos de rotina/prospecção sem problema nem oferta relevante (recados com secretárias, correio de voz, check-ins rápidos) e 1 é o vendedor preso na URA sem falar com ninguém.

## P3 — Problemas recorrentes (tabela de frequência)
| Código | Categoria | Ocorrências | Resolvido na ligação (SIM/NAO/PARCIAL — contagem) | Escalou (contagem por destino) |
|---|---|---|---|---|
| P1 | Acesso/sistema (portal, senha, biometria) | 4 | SIM 1 / PARCIAL 3 | 0800: 1; suporte telemetria (Mob7): 1; outro executivo: 1; nao_escalou: 1 |
| P2 | Faturamento/cobrança | 5 | SIM 2 / PARCIAL 3 | 0800: 1; suporte interno: 1; outro executivo: 1; nao_escalou: 2 |
| P3 | Multa/infração | 2 | SIM 1 / PARCIAL 1 | nao_escalou: 2 |
| P4 | Manutenção/substituto | 1 | SIM 1 | nao_escalou: 1 (orientado a agendar via WhatsApp assistência) |
| P5 | Condutor/cadastro | 2 | SIM 1 / NAO 1 | nao_escalou: 2 |
| P6 | Km excedente | 0 | — | — |
| P7 | Disponibilidade | 1 | NAO 1 (reserva cancelada) | nao_escalou: 1 |
| P8 | Franquia/agência | 0 | — | — |
| P9 | Sinistro | 0 | — | — |
| P10 | Reserva/sistema | 2 | SIM 1 / NAO 1 | nao_escalou: 2 |
| P11 | Outro (renegociação de tarifa pós-reajuste) | 1 | NAO 1 | nao_escalou: 1 |

Obs.: ligações com múltiplos problemas foram contadas em cada categoria (ex.: boleto vencido + multa + senha do portal na mesma chamada).

## P3 — Exemplos
- **Cliente 26670679** (P2+P1): boletos nunca chegam por e-mail, empresa caiu no Serasa com ~R$900 de juros. Vendedor explica que "a Localiza não envia os boletos por e-mail... o gestor tem acesso à plataforma [WebCorp] para emissão" — mas só o sócio (viajando) tem login. Escalado para 0800; resolução parcial.
- **Cliente 23428588** (P11): cliente pede trocar de categoria/franquia mantendo tarifa antiga após reajuste. Vendedora: "Eu tentei de tudo... não está tendo exceção, nem com volume de carro — mandei proposta para oito carros e não deram nenhum desconto." Não resolvido, cliente ficou de "pensar".
- **Cliente 12363390** (P5): cadastro feito em dezembro nunca teve follow-up — "eu não tive resposta da parte de vocês e a gente acabou locando com outra empresa, que respondeu a gente mais rápido." Venda perdida por falha no onboarding.

## P7 — Cross-sell/Upsell (tabela de frequência)
| Código | Produto | Vezes mencionado | Vezes ofertado ativamente | Janelas perdidas identificadas |
|---|---|---|---|---|
| PR1 | Aluguel mensal leve (core) | ~13 | 7 | 1 |
| PR2 | Aluguel pesado | 2 | 2 | 0 |
| PR3 | Telemetria | 1 (cliente já usa, pediu suporte) | 0 | 0 |
| PR4 | Proteção total | 2 | 2 | 0 |
| PR5 | Upgrade categoria | 3 | 1 | 0 |
| PR6 | Km adicional/franquia | 3 (config. de cotação) | 0 | 0 |
| PR7 | Contrato anual / mensal fixo 3-12m | 6 | 5 | 0 |
| PR8 | Elétrico | 0 | 0 | 0 |
| PR9 | ZARP | 0 | 0 | 0 |
| PR10 | Meoo (assinatura) | 6 | 2 | 1 |
| PR11 | Seminovos | 0 | 0 | 1 |
| PR12 | Gestão de frotas | 3 | 1 | 2 |

## P7 — Exemplos
- **Oferta bem feita — Cliente 15580210 (vendedora Cristina):** numa única ligação sobre troca de condutor, ofertou o plano mensal fixo 12 meses guiando a cliente na simulação no WebCorp, puxou a Proteção Total Avarias ("te isenta 100% de franquia... cobre vidros e pneus") e ainda gerou cotação do Localiza Meoo com carro zero km. Três ofertas ativas encaixadas na demanda.
- **Oferta bem feita — Cliente 05628910 (vendedora Ana Paula):** sondou frota própria e perguntou "vocês utilizam caminhões pesados?" → cliente confirmou e aceitou receber executivo do time de pesados. Cross-sell PR2 gerado a partir de pergunta de descoberta. (Mesmo padrão no Cliente 06721151: caminhão na oficina → oferta de aluguel de caminhão, recusada mas bem tentada.)
- **Janela perdida — Cliente 05218056:** cliente revela que faz todas as locações diárias via agência de viagens; vendedor encerra com "vocês estão muito bem assegurados com as agências de viagens" em vez de disputar o volume (PR1).
- **Janela perdida — Cliente 25198551:** cliente conta que a empresa comprou uma Compass para cortar custo de locação no Norte — janela clara para Seminovos/contrato longo; vendedor fez pitch "aluguel vs compra" apenas depois da compra concretizada e prometeu genericamente "preço melhor".

## Observações livres
A causa nº 1 de não-resolução no lote é falta de autonomia tarifária/sistêmica do vendedor ("o sistema puxa a tarifa vigente", "nem a agência libera") — o vendedor vira porta-voz do "não" sem alternativa de retenção. O processo de boleto (não enviado por e-mail, só via portal com login único do gestor) gerou atrito em 3 ligações, incluindo negativação no Serasa. Curiosidade operacional: uma "ligação" é o próprio vendedor preso na URA do Meoo reclamando ("essa URA da Localiza é peste" — Cliente 15481836), sintoma de que nem o time interno navega bem os canais.
