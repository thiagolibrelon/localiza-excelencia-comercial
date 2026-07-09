# Lote 13 — Exploração P3+P7

## Resumo do lote
- Total de ligações no lote: 38
- Ligações da BASE_ANTIGA_1275: 8
- Ligações do NOVO_LOTE_5348: 30

Nota: ~7 ligações foram apenas tentativas de contato (recado, feriado, cliente em reunião/ocupado) sem conteúdo classificável.

## P3 — Problemas recorrentes (tabela de frequência)
| Código | Categoria | Ocorrências | Resolvido na ligação (SIM/NAO/PARCIAL — contagem) | Escalou (contagem por destino) |
|---|---|---|---|---|
| P1 | Acesso/sistema (portal, senha, biometria) | 7 | SIM 2 / PARCIAL 2 / NAO 3 | IT 1, 0800/central 1, interno 1, nao_escalou 4 |
| P2 | Faturamento/cobrança | 4 | SIM 2 / PARCIAL 1 / NAO 1 | interno (equipe faturamento) 1, nao_escalou 3 |
| P3 | Multa/infração | 0 | — | — |
| P4 | Manutenção/substituto | 1 | PARCIAL 1 | 0800/agência 1 |
| P5 | Condutor/cadastro | 6 | SIM 4 / NAO 2 | análise de crédito 1, interno (desbloqueio) 1, nao_escalou 4 |
| P6 | Km excedente | 2 | PARCIAL 2 | assistência clientes (e-mail) 1, supervisor 1 |
| P7 | Disponibilidade | 1 | PARCIAL 1 | interno (agência) 1 |
| P8 | Franquia/agência | 1 | SIM 1 (resolvida via contato da franquia, antes da ligação) | nao_escalou |
| P9 | Sinistro | 0 | — | — |
| P10 | Reserva/sistema (erro ao concluir reserva) | 2 | SIM 2 | nao_escalou 2 |
| P11 | Outro (follow-up Meoo não recebido; questão jurídica de locação PF; consulta programa de pontos) | 3 | SIM 2 / PARCIAL 1 | interno (equipe Meoo) 1, nao_escalou 2 |

Destaque: P1 (acesso/biometria/WebCorp) é disparado o problema mais frequente do lote e o de pior taxa de resolução em linha (3 NAO em 7).

## P3 — Exemplos (trechos representativos)

- **P1 / biometria travada — Cliente 27136499**: cadastro de senha com QR Code que não carrega; vendedora confirma "Parece que tá com erro mesmo (...) eles já estão olhando" e pede para o cliente tentar de novo em 1 hora — não resolvido na ligação, escalado para verificação de sistema.
- **P6 / cobrança de km excedente — Cliente 04180452**: cliente não viu o e-mail de opção de apuração e foi cobrado mensalmente após aferição na manutenção; pergunta "tem como a gente mudar isso aí?" — vendedor muda a modalidade para fim de contrato, mas a contestação da fatura "foge da minha alçada", orientada via e-mail à assistência clientes.
- **P5 / crédito reprovado — Cliente 07040637**: substituição reprovada; análise pede SCR assinado e "documentação comprobatória sobre as restrições em nome da empresa e dos sócios" — locação prevista para o dia seguinte fica travada aguardando documentos.
- **P1 / biometria de pessoa errada — Cliente 23037890**: reconhecimento facial falhava porque a sócia validava um acesso liberado para a responsável do financeiro; esclarecido em linha (SIM).

## P7 — Cross-sell/Upsell (tabela de frequência)
| Código | Produto | Vezes mencionado | Vezes ofertado ativamente | Janelas perdidas identificadas |
|---|---|---|---|---|
| PR1 | Aluguel mensal leve (core) | 14 | 5 | 0 |
| PR2 | Aluguel pesado | 0 | 0 | 0 |
| PR3 | Telemetria | 1 | 0 | 0 |
| PR4 | Proteção total | 6 | 2 | 0 |
| PR5 | Upgrade categoria | 1 | 1 | 0 |
| PR6 | Km adicional / ajuste de franquia | 4 | 2 | 0 |
| PR7 | Contrato anual | 2 | 1 | 0 |
| PR8 | Elétrico | 0 | 0 | 0 |
| PR9 | ZARP | 0 | 0 | 0 |
| PR10 | Meoo (assinatura) | 3 | 2 | 0 |
| PR11 | Seminovos | 0 | 0 | 0 |
| PR12 | Gestão de frotas | 2 | 0 | 2 |

## P7 — Exemplos

- **Oferta ativa bem feita (PR1 + PR10) — Cliente 01668088, vendedora Andresa**: numa visita de manutenção, sondou aluguel mensal ("Você acha que a possibilidade de retirar ou vocês realmente são sempre curtas diárias?"), descobriu contrato de assinatura de 36 meses com concorrente ("na época eu cotei com a Localiza, mas estava muito fora") e plantou a recompra: "Quando vencer, me pede o orçamento que quem sabe dessa vez a gente vai conseguir atender vocês." Ainda orientou antecipação de reservas para preço melhor.
- **Oferta ativa (PR1 migração diária→mensal) — Cliente 12157361**: contrato de 11 diárias em aberto; vendedora propõe estender até 30 dias "porque a tarifa no mensal é muito melhor (...) você paga a mesma coisa ficando com o carro 11 diárias ou 30 dias", e estrutura o cálculo de km pelo WhatsApp. Mesmo movimento (com promoção) no Cliente 03423413, recusado.
- **Janela perdida (PR12) — Cliente 09906000**: cliente afirma "o pessoal está se deslocando com o veículo próprio da empresa" e que usa Uber nos deslocamentos aéreos; vendedor apenas reforça disponibilidade de reservas pontuais, sem sondar terceirização/gestão da frota própria. Similar no Cliente 03423413 ("a gente já tem carro aqui").
- **Oferta ativa (PR7) — Cliente 05018875**: cliente pede Nivus por 12–24 meses; vendedor cota na hora com desconto adicional e explica a régua de preço (3 anos migra para o segmento de frotas).

## Observações livres
Chama atenção o volume de "atendimento consultivo de portal": em pelo menos 5 ligações longas (algumas de 10–17 min) o executivo faz a reserva junto com o cliente passo a passo na WebCorp, contornando bugs do sistema (página em branco, erro de telefone fixo, QR de biometria que não carrega) — o portal gera fricção que consome tempo comercial, mas também cria momentos de confiança onde surgem upsells naturais (upgrade de categoria, proteção total, km). Há sinais claros de expansão em curso não capturados nas tabelas: Cliente 23428932 sinalizou contrato novo com até 30 veículos (pendente de exceção de km >5.000) e Cliente 04180452 prometeu "melhorar a quantidade de veículos" — nenhum dos dois recebeu menção a telemetria ou gestão de frotas, que seguem praticamente ausentes do discurso do time.
