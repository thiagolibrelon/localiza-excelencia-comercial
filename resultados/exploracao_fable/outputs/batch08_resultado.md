# Lote 08 — Exploração P3+P7

## Resumo do lote
- Total de ligações no lote: 38
- Ligações da BASE_ANTIGA_1275: 11
- Ligações do NOVO_LOTE_5348: 27

Nota: ~13 ligações são contatos de rotina/prospecção curtos sem problema nem oferta (contato ausente, "sem demanda no momento", cliente dirigindo/no hospital).

## P3 — Problemas recorrentes (tabela de frequência)
| Código | Categoria | Ocorrências | Resolvido na ligação (SIM/NAO/PARCIAL — contagem) | Escalou (contagem por destino) |
|---|---|---|---|---|
| P1 | Acesso/sistema (portal, senha, biometria) | 3 | SIM 2, PARCIAL 1 | nao_escalou 2, e-mail/central empresas 1 |
| P2 | Faturamento/cobrança | 6 | SIM 3, PARCIAL 2, NAO 1 | nao_escalou 3, 0800 1, financeiro interno 1, time de cadastro 1 |
| P3 | Multa/infração | 0 | — | — |
| P4 | Manutenção/substituto | 1 | PARCIAL 1 | 0800 1 |
| P5 | Condutor/cadastro | 5 | SIM 3, PARCIAL 1, NAO 1 | nao_escalou 4, time de cadastro 1 |
| P6 | Km excedente | 1 | SIM 1 (dúvida esclarecida) | nao_escalou 1 |
| P7 | Disponibilidade | 1 | PARCIAL 1 (redirecionou p/ outra agência) | nao_escalou 1 |
| P8 | Franquia/agência | 1 | SIM 1 (horário de agência em feriado) | nao_escalou 1 |
| P9 | Sinistro | 2 | SIM 1, NAO 1 | nao_escalou 1, time de cadastro/cobrança 1 |
| P10 | Reserva/sistema | 3 | SIM 1, PARCIAL 2 | assistência ao cliente/central 1, correção interna de tarifa 1, central de reservas 1 |
| P11 | Outro (dúvida sobre proteções PJ x PF) | 1 | SIM 1 | nao_escalou 1 |

Destaques: P2 e P5 dominam; casos ligados a inadimplência travam outras operações (substituição de carro bloqueada por boleto vencido; recolha de veículo por pagamentos em aberto).

## P3 — Exemplos
- **Cliente 22950071 (P2+P4, PARCIAL, 0800):** boleto vencido impede substituição de carro com embreagem ruim — "a substituição infelizmente não tem conta por causa desse valor em aberto"; vendedor orientou agendar manutenção pelo 0800-979-2020 ou devolver o carro e ficar sem até pagar segunda-feira.
- **Cliente 22938518 (P9+P2, NAO):** conta suspensa após sinistro com cobrança de R$115 mil contestada — "eles cobraram 115 mil... eu pedi a telemetria do veículo no momento do acidente, eles só mandaram um relatório feito à mão"; cliente já com advogado, vendedor só encaminhou o contato do time de cadastro para tentar novo CNPJ.
- **Cliente 09385430 (P1, SIM):** vendedor conduziu passo a passo, em linha, a redefinição de senha expirada + biometria facial na WebCorp e concluiu a prorrogação do contrato até dezembro — suporte completo sem escalar.

## P7 — Cross-sell/Upsell (tabela de frequência)
| Código | Produto | Vezes mencionado | Vezes ofertado ativamente | Janelas perdidas identificadas |
|---|---|---|---|---|
| PR1 | Aluguel mensal leve (core) | ~12 | 5 | 0 |
| PR2 | Aluguel pesado | 0 | 0 | 0 |
| PR3 | Telemetria | 1 | 0 | 1 |
| PR4 | Proteção total | 4 | 1 | 0 |
| PR5 | Upgrade categoria | 1 (cortesia relatada pelo cliente) | 0 | 0 |
| PR6 | Km adicional/franquia | 3 | 0 | 0 |
| PR7 | Contrato anual/mensal fixo longo | 5 | 1 | 1 |
| PR8 | Elétrico | 0 | 0 | 0 |
| PR9 | ZARP | 0 | 0 | 0 |
| PR10 | Meoo / Localiza Meu | 5 | 1 | 1 |
| PR11 | Seminovos | 0 | 0 | 1 |
| PR12 | Gestão de frotas | 1 (junto com PR10) | 0 | 0 |

## P7 — Exemplos
- **Oferta ativa bem feita — Cliente 26924782 (vendedor Rodrigo):** cliente pediu carro extra por 15 dias; vendedor converteu em proposta de mensal — "quando você faz de 15 a 20 dias... costuma ficar mais vantajoso pegar mensal... a diária de 200 cai pra 80, 90" — e reforçou benefício PJ de condutores ilimitados. Enviou as duas cotações.
- **Oferta ativa bem feita — Cliente 20455632:** vendedor detectou reserva mensal de 30 dias p/ São Paulo sem proteção e cotou proativamente a proteção total (+R$380): "eu sou o consultor exatamente para a gente poder evitar surpresas futuras". Cliente recusou, mas a abordagem foi consultiva e não invasiva.
- **Janela perdida — Cliente 02825926:** cliente locando 2 carros com concorrente por preço e disse "eu estava vendo um carro de leilão para a gente ver se eu comprava" — abertura clara para PR11 (Seminovos) e para proposta estruturada PR7 (ele já loca anual com o concorrente); vendedor só prometeu "melhorar a condição comercial" da diária.
- **Janela parcial — Cliente 07215651:** cliente pediu explicitamente contrato de 6 meses/1 ano com condição diferenciada; vendedor apenas apontou a tabela self-service da WebCorp ("o mensal fixo é tabelado, não consigo") sem construir proposta ou envolver pricing.

## Observações livres
Metade do lote é ligação proativa de carteira ("plano de visitas") de baixíssima conversão — muitos contatos nem alcançam o decisor. O vendedor frequentemente atua como help desk de acesso/cadastro (senha, biometria, WebCorp, Trust), o que gera goodwill mas consome ligações longas (600-900s) sem nenhuma tentativa de venda. Padrão notável: inadimplência/sinistro funciona como trava sistêmica (bloqueia substituição, recolhe carro, suspende conta) e o executivo comercial tem pouca alçada — tudo escala para 0800/financeiro/times internos, com risco de churn declarado (cliente 22938518 e cliente 02825926 já migrando para concorrente por preço).
