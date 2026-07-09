# Lote 10 — Exploração P3+P7

## Resumo do lote
- Total de ligações no lote: 38
- Ligações da BASE_ANTIGA_1275: 4 (Clientes 12936013, 17204990, 20295674, 01946427)
- Ligações do NOVO_LOTE_5348: 34

Obs.: ~16 ligações são puramente proativas (apresentação de executivo, manutenção de carteira, tentativa de contato) sem problema trazido pelo cliente; as contagens de P3 abaixo referem-se às ~20 ligações com problema/demanda operacional. Algumas ligações têm mais de um problema (dupla codificação).

## P3 — Problemas recorrentes (tabela de frequência)
| Código | Categoria | Ocorrências | Resolvido na ligação (SIM/NAO/PARCIAL — contagem) | Escalou (contagem por destino) |
|---|---|---|---|---|
| P1 | Acesso/sistema (portal, senha, biometria) | 6 | SIM 2 / PARCIAL 4 / NAO 0 | interno-cadastro/IT 1; não_escalou 5 |
| P2 | Faturamento/cobrança | 5 | SIM 4 / PARCIAL 1 / NAO 0 | setor renegociação 1; não_escalou 4 |
| P3 | Multa/infração | 1 | PARCIAL 1 | não_escalou 1 |
| P4 | Manutenção/substituto | 0 | — | — |
| P5 | Condutor/cadastro | 4 | SIM 2 / PARCIAL 2 | interno (análise/condutor) 1; não_escalou 3 |
| P6 | Km excedente | 2 | PARCIAL 2 | setor renegociação 1; não_escalou 1 |
| P7 | Disponibilidade | 3 | SIM 1 / PARCIAL 2 | supervisora 1; não_escalou (acionou agência direto) 2 |
| P8 | Franquia/agência | 0 | — | — |
| P9 | Sinistro | 1 | PARCIAL 1 | 0800 1 |
| P10 | Reserva/sistema | 2 | SIM 1 / PARCIAL 1 | 0800 (workaround de reserva) 1; não_escalou 1 |
| P11 | Outro (link de pesquisa expirado; migração diário→mensal c/ trava de proteção) | 2 | PARCIAL 1 / NAO 1 | não_escalou 2 |

Total de problemas codificados: 26.

## P3 — Exemplos
- **Cliente 19512613 (P9, escalou 0800):** carro de terceiro Localiza causou engavetamento; cliente com "três dias sem trabalhar... a gente fatura de 10 a 15 mil" por dia parado. Vendedor orientou fluxo 0800/aviso de sinistro e ofereceu desconto para locação temporária no CNPJ enquanto o sinistro corre.
- **Cliente 17973551 (P6+P2, escalou renegociação):** "houve quilometragem excedente, porém eles só conseguiram apurar o odômetro na hora da entrega do carro" — cobrança-surpresa na fatura final + outra fatura já vencida; encaminhado para parcelamento no setor de renegociação.
- **Cliente 12936013 (P3+P1, PARCIAL):** gestor precisava da notificação de multa para repassar ao condutor, não conseguia logar no portal de faturamento ("não estou registrando"); vendedor desistiu do passo a passo e ficou de emitir e mandar por WhatsApp.
- **Cliente 05702473 (P1, SIM):** usuário bloqueado porque outra pessoa tentou a biometria no login dele — vendedor explicou a regra de CPF vinculado e destravou com reset de senha.

## P7 — Cross-sell/Upsell (tabela de frequência)
| Código | Produto | Vezes mencionado | Vezes ofertado ativamente | Janelas perdidas identificadas |
|---|---|---|---|---|
| PR1 | Aluguel mensal leve (core) | 15 | 7 | 1 (cliente 24128328) |
| PR2 | Aluguel pesado | 0 | 0 | 0 |
| PR3 | Telemetria | 0 | 0 | 0 |
| PR4 | Proteção total | 4 | 1 | 0 |
| PR5 | Upgrade categoria | 1 | 0 | 0 |
| PR6 | Km adicional | 3 | 0 (todas iniciadas pelo cliente) | 0 |
| PR7 | Contrato anual / mensal fixo 3-12m | 6 | 4 | 0 |
| PR8 | Elétrico | 0 | 0 | 0 |
| PR9 | ZARP | 0 | 0 | 0 |
| PR10 | Meoo (assinatura) | 6 | 3 | 2 (clientes 15215742, 01946427) |
| PR11 | Seminovos | 1 | 0 | 0 |
| PR12 | Gestão de frotas / terceirização | 2 | 1 | 2 (clientes 15215742, 24128328) |

## P7 — Exemplos
- **Oferta ativa bem feita — Cliente 26630232 (vendedora Gabriela):** cliente revelou "cinco carros... três estão parados e quebrados"; vendedora imediatamente ofertou terceirização de frota com proposta RAC até 12 meses + indicação Meoo, argumentando custo de capital parado. Melhor conversão de janela do lote.
- **Oferta ativa bem feita — Cliente 02536234 (vendedora Luma):** upsell puro de proteção — "vi que vocês não têm esse seguro [ampliado para terceiros]... aumenta apenas 200 reais na mensalidade", com follow-up agendado para a decisão do proprietário.
- **Janela perdida — Cliente 24128328:** cliente disse espontaneamente que a empresa parceira "tem alguns carros no contrato dela, só que não seria Localiza" (concorrente) e que planeja "aumentar a quantidade de veículos"; vendedor respondeu "não vou estender aqui contigo não, era só isso que eu precisava saber" — nenhuma oferta de conquista.
- **Janela perdida — Cliente 15215742:** cliente informou "a gente tem uma frota de veículos particulares... para o pessoal viajar"; vendedora encerrou com pesquisa de satisfação sem sondar terceirização/assinatura.

## Observações livres
O lote é dominado por ligações proativas de carteira (apresentação de novo executivo, "manutenção de cadastro"), com roteiro forte de deixar WhatsApp e pedir nota na pesquisa — inclusive coaching explícito de nota ("as notas boas é 9 e 10") em uma delas. A resolução se apoia quase toda em orientar o cliente dentro da WebCorp (prorrogação, perfis de gestor, cotação), com baixíssimo escalonamento formal; o padrão de fricção recorrente é acesso/biometria/login (P1), que consome minutos longos de ligação. Nas ofertas, o combo "mensal fixo 3/6/9/12 + indicação Meoo para prazos maiores" aparece como playbook consistente entre vários vendedores, mas ninguém tocou em telemetria, elétrico ou pesados.
