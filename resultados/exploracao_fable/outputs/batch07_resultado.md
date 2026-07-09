# Lote 07 — Exploração P3+P7

## Resumo do lote
- Total de ligações no lote: 38
- Ligações da BASE_ANTIGA_1275: 13
- Ligações do NOVO_LOTE_5348: 25

Nota: ~10 ligações são muito curtas (39–60s, contato ausente/ocupado) ou de prospecção/manutenção sem problema nem oferta — não geram ocorrência nas tabelas.

## P3 — Problemas recorrentes (tabela de frequência)
| Código | Categoria | Ocorrências | Resolvido na ligação (SIM/NAO/PARCIAL — contagem) | Escalou (contagem por destino) |
|---|---|---|---|---|
| P1 | Acesso/sistema (portal, senha, biometria) | 4 | SIM: 3 / PARCIAL: 1 | nao_escalou: 4 |
| P2 | Faturamento/cobrança | 4 | SIM: 3 / PARCIAL: 1 | 0800: 1 (negociar juros) / nao_escalou: 3 |
| P3 | Multa/infração | 1 | SIM: 1 | nao_escalou: 1 (0800 citado só p/ fotos) |
| P4 | Manutenção/substituto | 1 | PARCIAL: 1 | 0800 (emergencial): 1 |
| P5 | Condutor/cadastro | 2 | PARCIAL: 2 | nao_escalou: 2 |
| P6 | Km excedente | 0 | — | — |
| P7 | Disponibilidade | 0 | — | — |
| P8 | Franquia/agência | 1 | SIM: 1 | nao_escalou: 1 |
| P9 | Sinistro | 1 | SIM: 1 | nao_escalou: 1 |
| P10 | Reserva/sistema | 1 | PARCIAL: 1 | IT: 1 |
| P11 | Outro (insatisfação geral, crédito reprovado, dúvida de prorrogação) | 3 | SIM: 1 / NAO: 1 / PARCIAL: 1 | nao_escalou: 2 / análise de crédito interna: 1 |

Total de problemas identificados: 18. Taxa de resolução na ligação: SIM 10 / PARCIAL 7 / NAO 1.

## P3 — Exemplos
- **P1 — Cliente 20148743**: cliente deixou de alugar por não conseguir acessar login/senha do app ("precisei alugar um carro, tive que passar no cartão do Jardim... era tão fácil pela plataforma"). Vendedor enviou login + vídeo de reset por WhatsApp. Problema de acesso estava suprimindo receita silenciosamente.
- **P10 — Cliente 16161947**: cliente logou no portal mas o sistema bloqueou a reserva com erro ("não deixa eu passar da data, não deixa eu ver carro"); tentou 3x, ligou no 0800 e desistiu após 20 min. Vendedor escalou para TI. **Cliente acabou alugando em outro lugar** — falha de sistema virou venda perdida.
- **P4+P2 — Cliente 12936013**: carro não ligou e cliente achou que era bloqueio por fatura atrasada; vendedora verificou que não havia bloqueio (pagamento já compensado) e direcionou ao 0800 emergencial para substituição do veículo.
- **P11 — Cliente 25386563**: detrator explícito — pediu cancelamento do cadastro ("a Localiza me decepcionou em todos os pontos... o aplicativo não reflete o que vocês vendem de imagem"). Vendedor apenas acatou, sem tentativa de recuperação estruturada.

## P7 — Cross-sell/Upsell (tabela de frequência)
| Código | Produto | Vezes mencionado | Vezes ofertado ativamente | Janelas perdidas identificadas |
|---|---|---|---|---|
| PR1 | Aluguel mensal leve (core) | 15 | 7 | 0 |
| PR2 | Aluguel pesado | 2 | 2 | 0 |
| PR3 | Telemetria | 1 | 0 | 0 |
| PR4 | Proteção total | 1 | 1 | 0 |
| PR5 | Upgrade categoria | 1 | 0 | 0 |
| PR6 | Km adicional/franquia | 3 | 0 | 0 |
| PR7 | Contrato anual | 2 | 1 | 0 |
| PR8 | Elétrico | 0 | 0 | 0 |
| PR9 | ZARP | 0 | 0 | 0 |
| PR10 | Meoo (assinatura) | 1 | 1 | 1 |
| PR11 | Seminovos | 0 | 0 | 0 |
| PR12 | Gestão de frotas | 2 | 0 | 2 |

## P7 — Exemplos
- **Oferta ativa exemplar (PR1+PR7) — Cliente 26513991, vendedor Rodrigo**: detectou cliente locando mensal no CPF de um funcionário há ~5 meses, argumentou dedução fiscal e preço PJ, destravou o login parado desde fevereiro, explicou flexibilidade de franquia de km e fechou envio de propostas de 3 a 12 meses. Conversão de PF para PJ + porta para contrato anual na mesma ligação.
- **Oferta ativa exemplar (PR1+PR4) — Cliente 13365284, vendedor Ângelo**: onboarding completo com reserva mensal concluída ao vivo; ofertou proteção ampliada (aceita) e proteção total com argumento de previsibilidade (recusada sem atrito). Já plantou o contrato de 12 meses ("me chama no WhatsApp que a gente faz outra negociação").
- **Oferta ativa (PR2) — Cliente 09038408**: cliente citou distribuição com vans/VUC terceirizados; vendedora ofertou Localiza Pesados e enviou portfólio de caminhões — janela bem aproveitada.
- **Janela perdida (PR12) — Cliente 16507374**: cliente declarou frota própria de veículos e 3 caminhões; vendedor ofertou pesados (bom), mas não abordou gestão/terceirização de frota, que era a dor maior implícita.
- **Janela semi-perdida (PR12) — Cliente 25830517**: cliente tem 2 Saveiros próprias; vendedora começou a sondar custo de manutenção vs. locação mensal, mas a ligação morreu em "ligo em outro horário" sem agendamento firme.

## Observações livres
Escalação quase inexistente neste lote: os gestores resolvem ou encaminham via WhatsApp/0800 orientado, e o WhatsApp do gestor funciona como canal universal de fechamento (login, propostas, faturas, termos). O padrão comercial mais forte do lote é a conversão PF→PJ e diária→mensal (4 ligações com esse pitch), enquanto produtos periféricos (telemetria, elétrico, ZARP, seminovos) têm zero tração. Dois alertas competitivos/churn: cliente 21511693 cotando simultaneamente com a Movida e o detrator 25386563 cancelando cadastro sem esforço de retenção.
