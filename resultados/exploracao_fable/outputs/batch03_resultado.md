# Lote 03 — Exploração P3+P7

## Resumo do lote
- Total de ligações no lote: 38
- Ligações da BASE_ANTIGA_1275: 3
- Ligações do NOVO_LOTE_5348: 35

Perfil do lote: forte predominância de ligações proativas de carteira/prospecção (apresentação de executivo, "está precisando de locação?", cadastro novo/inativo). ~14 ligações são contato de rotina curto sem problema nem oferta além do core; ~5 nem alcançaram o decisor (recado/retorno agendado).

## P3 — Problemas recorrentes (tabela de frequência)
| Código | Categoria | Ocorrências | Resolvido na ligação (SIM/NAO/PARCIAL) | Escalou (contagem por destino) |
|---|---|---|---|---|
| P1 | Acesso/sistema (portal, senha, gestor) | 2 | NAO 1 / PARCIAL 1 | backoffice-e-mail 1 / nao_escalou 1 |
| P2 | Faturamento/cobrança | 2 | NAO 2 | nao_escalou 2 |
| P3 | Multa/infração | 0 | — | — |
| P4 | Manutenção/substituto (troca de veículo) | 2 | SIM 1 / PARCIAL 1 | backoffice-substituição 1 / nao_escalou 1 |
| P5 | Condutor/cadastro | 4 | SIM 2 / PARCIAL 1 / NAO 1 | backoffice (negado) 1 / 0800 (orientado) 1 / nao_escalou 2 |
| P6 | Km excedente | 1 | PARCIAL 1 (orientação painel de gestão) | nao_escalou 1 |
| P7 | Disponibilidade | 3 | SIM 1 / PARCIAL 1 / NAO 1 | supervisora-agência 1 / nao_escalou 2 |
| P8 | Franquia/agência | 0 | — | — |
| P9 | Sinistro (furto/acidente) | 2 | PARCIAL 2 | 0800 1 / nao_escalou 1 |
| P10 | Reserva/sistema | 1 | PARCIAL 1 (workaround por telefone) | central de reservas 1 |
| P11 | Outro (crédito 2x, reajuste de tarifa 1x, telefonia 2x) | 5 | SIM 2 / PARCIAL 1 / NAO 2 | condutor-crédito/financeiro 2 / 0800 1 / nao_escalou 2 |

Notas:
- "Escalou" aqui quase nunca é 0800/supervisora clássicos: o padrão dominante é encaminhar para um "condutor" interno (crédito, substituição, reservas, responsável) via e-mail/WhatsApp, com promessa de retorno.
- Limite de crédito apareceu 2x como bloqueador de reserva (P11) — em um caso o vendedor contornou abrindo contrato com 1.000 km para depois migrar para 5.000 km.

## P3 — Exemplos
- **Cliente 23722410 (P2, churn consumado):** cobrança de ~R$700 por um friso que soltou sozinho na estrada; contestação negada. "Nós achamos isso uma injustiça e procuramos outro fornecedor... desculpa não vai resolver a questão". Cliente migrou para a Unidas e o gerente teve o valor descontado do salário.
- **Cliente 27285095 (P5, não resolvido):** condutor com CPF bloqueado sem justificativa possível (LGPD). Cliente: "você tem que dar um motivo pelo menos... não existe isso" — desistiu do PJ e disse que vai alugar "na pessoa física mesmo, direto na localiza da minha cidade".
- **Cliente 27104103 (P10, workaround):** "quando chega na parte de cadastrar o condutor, ele fica só carregando" — falhou em Chrome, Mozilla e Edge; vendedora transferiu para a central de reservas para concluir por telefone e ficou na linha.

## P7 — Cross-sell/Upsell (tabela de frequência)
| Código | Produto | Vezes mencionado | Vezes ofertado ativamente | Janelas perdidas identificadas |
|---|---|---|---|---|
| PR1 | Aluguel mensal leve (core) | ~16 | 6 | 0 |
| PR2 | Aluguel pesado | 1 | 1 (sondagem ativa: "vocês têm caminhão?") | 0 |
| PR3 | Telemetria | 1 | 1 (aceita na hora) | 0 |
| PR4 | Proteção total / ampliada | 3 | 1 | 0 |
| PR5 | Upgrade categoria | 2 | 0 (ambas iniciadas pelo cliente) | 0 |
| PR6 | Km adicional | 2 | 1 (proposta 4-5 mil km a enviar) | 0 |
| PR7 | Contrato anual (12m) | 2 | 1 (cotação 3/6/9/12 meses) | 0 |
| PR8 | Elétrico | 0 | 0 | 0 |
| PR9 | ZARP | 0 | 0 | 0 |
| PR10 | Meoo | 0 | 0 | 1 |
| PR11 | Seminovos | 1 | 0 | 0 |
| PR12 | Gestão de frotas | 2 | 0 | 3 |

## P7 — Exemplos
- **Oferta ativa bem feita — vendedora Luma, Cliente 23006894:** durante reserva guiada no portal, ofertou proteção total avarias ("menino novo" como condutor) e telemetria por R$51/mês explicando o benefício de rastreio em tempo real — cliente respondeu "Ah, eu quero" na hora, e a vendedora ainda se ofereceu para atribuí-la como gestora de telemetria. Único caso de cross-sell não-core convertido no lote.
- **Sondagem ativa correta — Cliente 01574802:** vendedor perguntou espontaneamente "vocês têm caminhão aí na engenharia?" (probe PR2) — cliente não tinha, mas é o único caso de prospecção ativa fora do core.
- **Janela perdida — Cliente 07997963 (PR10):** igreja com 750 funcionários pedindo condição para colaboradores alugarem direto como PF ("o funcionário sempre pede... para nós é interessante") — vendedor redirecionou para RAC faturado e não ofertou Meoo/assinatura. Cliente ainda avisou que "a Movida está imbatível" no preço.
- **Janelas perdidas — PR12:** clientes 01574802, 27319935 e 21917231 citaram frota própria (5 carros, veículos próprios, carros de obra) e nenhum vendedor sondou gestão/terceirização de frota.

## Observações livres
O lote é dominado por ligações de relacionamento/prospecção curtas em que o vendedor se apresenta, pergunta demanda e encerra — o repertório de oferta se resume ao mensal core (3/6/9/12 meses); produtos como telemetria, proteção e pesado só aparecem quando a conversa já está dentro de uma reserva. O WhatsApp é o canal universal de follow-up ("vou te mandar um oi"), e a escalação padrão é para "condutores" internos (crédito, substituição, reservas), não para 0800/supervisora. Concorrência citada 2x (Movida "imbatível" em preço; Unidas pós-churn por cobrança de avaria de R$700), ambas ligadas a preço/cobrança, não a serviço. Uma transcrição (Cliente 26026315) tem áudio de duas conversas sobrepostas — classificada com cautela em P11 (dificuldade com 0800 para abrir chamado).
