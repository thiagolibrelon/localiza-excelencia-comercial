# Lote 11 — Exploração P3+P7

## Resumo do lote
- Total de ligações no lote: 38
- Ligações da BASE_ANTIGA_1275: 8
- Ligações do NOVO_LOTE_5348: 30

Nota: ~12 ligações são puramente prospecção/rotina curta (contato de cadastro, pessoa ausente, recado) sem problema nem oferta — ficam fora das tabelas.

## P3 — Problemas recorrentes (tabela de frequência)
| Código | Categoria | Ocorrências | Resolvido na ligação (SIM/NAO/PARCIAL — contagem) | Escalou (contagem por destino) |
|---|---|---|---|---|
| P1 | Acesso/sistema (portal, senha, biometria) | 5 | SIM 2 / NAO 2 / PARCIAL 1 | IT 1 / nao_escalou 4 |
| P2 | Faturamento/cobrança | 9 | SIM 2 / NAO 3 / PARCIAL 4 | 0800 1 / gerente-time interno 3 / nao_escalou 5 |
| P3 | Multa/infração | 1 | PARCIAL 1 | 0800 (renegociação) 1 |
| P4 | Manutenção/substituto | 1 | PARCIAL 1 (cotação enviada) | nao_escalou 1 |
| P5 | Condutor/cadastro | 4 | SIM 2 / PARCIAL 2 | 0800 1 / nao_escalou 3 |
| P6 | Km excedente | 1 | SIM 1 (dúvida esclarecida) | nao_escalou 1 |
| P7 | Disponibilidade | 2 | SIM 1 (upgrade de categoria) / NAO 1 | supervisora 1 / nao_escalou 1 |
| P8 | Franquia/agência | 0 | — | — |
| P9 | Sinistro | 1 | SIM 1 (contexto: cliente bateu em carro de terceiro, alugou p/ vítima) | nao_escalou 1 |
| P10 | Reserva/sistema | 1 | PARCIAL 1 (reserva pendente de crédito, liberação pedida) | nao_escalou 1 |
| P11 | Outro (limite de crédito insuficiente; preço vs concorrência) | 2 | PARCIAL 1 / NAO 1 | supervisora 1 / nao_escalou 1 |

Faturamento/cobrança (P2) domina o lote e é a categoria com pior taxa de resolução em linha — quase tudo vira e-mail de contestação, retorno de gerente ou 0800.

## P3 — Exemplos
- **Cliente 07062354** (P2, escalou por e-mail): cliente encontra placas desconhecidas na fatura — "tem outra placa também que a gente desconhece... onde passou foi no Paraná e a outra em Rio-SP, a gente desconhece". Vendedora formaliza e-mail de contestação com cliente em cópia.
- **Cliente 02970782** (P2, Meoo, não resolvido): "tá uma bagunça, Localiza... me vem as prévias falando que a gente pagou em abril as notas que foram pagas em fevereiro". Cliente montou planilha própria com comprovantes para reprovar prévias; vendedor apenas promete acionar o time do Meoo.
- **Cliente 20295775** (P2, não resolvido): "a gente renovou esse contrato para 5 mil km e ficou 4.500. Agora esse mês me veio a fatura de 6.600". Vendedor substituto não consegue explicar e agenda retorno da gerente titular.
- **Cliente 15561598** (P1, resolvido): senha do WebCorp recusada repetidas vezes + biometria via QR code — vendedor conduziu passo a passo por 45 min até concluir a primeira reserva mensal.

## P7 — Cross-sell/Upsell (tabela de frequência)
| Código | Produto | Vezes mencionado | Vezes ofertado ativamente | Janelas perdidas identificadas |
|---|---|---|---|---|
| PR1 | Aluguel mensal leve (core) | 18 | 9 | 1 |
| PR2 | Aluguel pesado | 1 | 0 | 1 |
| PR3 | Telemetria | 1 | 1 | 0 |
| PR4 | Proteção total | 4 | 2 | 0 |
| PR5 | Upgrade categoria | 1 | 0 | 0 |
| PR6 | Km adicional | 3 | 1 | 0 |
| PR7 | Contrato anual | 2 | 0 | 0 (demanda anual redirecionada p/ Meoo) |
| PR8 | Elétrico | 1 (híbrido BYD Song citado em cotação) | 0 | 0 |
| PR9 | ZARP | 0 | 0 | 0 |
| PR10 | Meoo | 4 | 1 | 0 |
| PR11 | Seminovos | 1 (cliente comprou seminovo no passado) | 0 | 1 |
| PR12 | Gestão de frotas | 0 | 0 | 2 |

## P7 — Exemplos
- **Oferta bem feita — Cliente 27314245 (vendedor Lucas)**: cliente queria só diária de picape; Lucas fechou o atendimento com pitch de migração para mensal ("tá dando mil reais em uma diária... às vezes o mensal tá 3 mil, 3.500... simula 30 dias, olha a quilometragem") e ainda apresentou telemetria como recurso de gestão. Cliente reagiu: "caraca, não tinha pensado nisso".
- **Oferta bem feita — Cliente 21700717**: cliente pediu locação anual de SUV; vendedor fez upsell de km (2 mil → 3 mil, "a diferença de 2 pra 3 não é alta"), cotou mensal e ofertou ativamente o Meoo (assinatura), agendando contato do time em 24h.
- **Janela perdida — Cliente 23733007**: cliente revelou "tem bastante carro aqui, uns sete... a gente tem o nosso próprio caminhão também" — vendedora perguntou sobre o caminhão mas encerrou só com "fico à disposição": nada de PR2, PR11 ou PR12.
- **Janela perdida — Cliente 20182277**: cliente admite locar "mais pela Movida, que eles têm um preço melhor" e que pega utilitários — vendedor defendeu marca genericamente e não cotou nada em linha, só prometeu WhatsApp.

## Observações livres
O lote é dominado por ligações proativas de carteira (contato de rotina / reativação de cadastro): elas geram boas descobertas (frota própria, concorrência, mudança de CNPJ), mas quase nenhuma conversão dessas descobertas em oferta concreta na própria ligação — o padrão é "te mando no WhatsApp". Segundo padrão forte: fricção de faturamento do Meoo contaminando o relacionamento RAC (3 ligações com clientes Meoo reclamando de fatura/nota a vendedores do RAC, que não têm alçada e só repassam). Terceiro: o primeiro acesso ao WebCorp (senha + biometria) é um gargalo recorrente que consome ligações inteiras (uma de 45 min), mas quando o vendedor conduz junto, converte em reserva na hora.
