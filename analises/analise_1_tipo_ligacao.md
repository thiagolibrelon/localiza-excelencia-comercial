# Análise 1 — Tipo de Ligação
**Base:** 14 clientes, ~87 ligações analisadas

---

## Distribuição por tipo

| Tipo | Qtd estimada | % |
|------|-------------|---|
| Suporte operacional (portal, sistema, acesso) | ~22 | 25% |
| Renovação / prorrogação de contrato | ~18 | 21% |
| Pós-venda (sinistro, avaria, multa, manutenção) | ~16 | 18% |
| Cobrança (faturas atrasadas, prorrogação de boleto) | ~10 | 11% |
| Nova venda / cotação | ~8 | 9% |
| Misto (suporte + tentativa comercial) | ~7 | 8% |
| Onboarding (condutor, cadastro, biometria) | ~4 | 5% |
| Caixa postal / sem conteúdo | ~2 | 2% |

---

## Classificação por cliente

### cliente_22154206 — Carla / Luciano
| # | Data | Tipo | Desfecho |
|---|------|------|----------|
| 1-5 | jan-fev | Renovação | Fechou |
| 6-10 | fev-mar | Suporte operacional (portal, condutores) | Não era venda |
| 11-15 | mar-abr | Misto (renovação + onboarding) | Fechou |
| 16-20 | abr-mai | Pós-venda (multas, manutenção) | Não era venda |
| 21-31 | mai | Renovação + upsell | Fechou |
> Conta com ciclo completo: suporte → fidelização → upsell.

---

### cliente_9322936 — Weverton / Andreia (Benefícios)
| # | Data | Tipo | Desfecho |
|---|------|------|----------|
| 1 | dez | Nova venda (cotação contrato 12m) | Fechou (interessou) |
| 2 | jan | Misto (carro elétrico — ROI + upsell) | Interessou, não fechou |
| 3 | jan | Nova venda (contrato mensal manual) | Cotação enviada |
| 4 | jan | Suporte (carro zero km — disponibilidade) | Não era venda |
| 5 | jan | Nova venda (contrato anual gerente SP) | Cotação enviada |
| 6 | mar | Pós-venda (carro em manutenção, cliente VIP) | Não era venda |
| 7-11 | mar | Suporte + pós-venda | Não era venda |

---

### cliente_6572518 — Lucas / Rangel (Posto)
| # | Data | Tipo | Desfecho |
|---|------|------|----------|
| 1-4 | fev-mar | Pós-venda (boleto terceiro, avaria combustível) | Não era venda |
| 5-6 | mar | Cobrança + suporte pós-venda (reembolso) | Não era venda |
| 7 | mar | Misto (NPS + cliente pede contrato anual) | Interessou, cotação enviada |
| 8 | abr | Nova demanda (cabine dupla) — sem disponibilidade | Não fechou |
| 9 | mar | Cobrança (boleto prorrogado) | Não era venda |
| 10-11 | mai | Suporte operacional | Não era venda |

---

### cliente_25257738 — Gabriela / Larissa (Entregas)
| # | Data | Tipo | Desfecho |
|---|------|------|----------|
| 1 | jan | Misto (troca de plano + condutores) | Fechou (troca de grupo) |
| 2 | fev | Onboarding (condutor novo, portal senha) | Não era venda |
| 3 | fev | Suporte (acesso portal financeiro) | Não era venda |
| 4 | fev | Nova demanda (Furgão urgente) — sem disponibilidade | Não fechou |
| 5 | mar | Misto (reserva + dúvida multa) | Fechou (reserva) |
| 6 | mar | Suporte + nova reserva | Fechou (reserva) |
| 7 | fev | Suporte (portal financeiro) | Não era venda |
| 8 | abr | Pós-venda (manutenção, AC com defeito) | Não era venda |
| 9 | jan | Misto longo (condutor demitido + troca de plano + portal) | Fechou parcial |

---

### cliente_22153452 — Pedro / Gerson (Logística)
| # | Data | Tipo | Desfecho |
|---|------|------|----------|
| 1 | jan | Suporte operacional (portal acesso) | Não era venda |
| 2 | mai | Suporte longo (senha + multa condutor errado) | Não era venda |
| 3 | jan | Misto (negociação km excedente + advocacy) | Não era venda (resolveu fatura) |
| 4 | jan | Misto (suporte senha + competitor probe + upsell caminhão) | Interessou (upsell pesado) |
| 5 | jan | Suporte operacional (portal fora do ar) | Não era venda |
| 6 | jan | Suporte + advocacy (fatura R$18k pendente de negociação) | Não era venda |

---

### cliente_21578554 — Camila / Wagner (Energia Solar)
| # | Data | Tipo | Desfecho |
|---|------|------|----------|
| 1 | jan | Nova venda (cotação 50 carros) | Interessou, em aprovação |
| 2 | jan | Nova venda (escopo + documentação) | Em andamento |
| 3 | jan | Pós-venda (manutenção sem substituto) | Não era venda |
| 4 | fev | Suporte (portal empresa errada) | Não era venda |
| 5 | abr | Suporte (reserva sob consulta) | Não era venda |
| 6 | mai | Suporte (taxa de devolução em outra cidade) | Não era venda |

---

### cliente_8127924 — Andreza / Alexandre (Fortal)
| # | Data | Tipo | Desfecho |
|---|------|------|----------|
| 1 | mar | Misto (fatura + competitor probe + relatório) | Não era venda direta |
| 2 | abr | Upsell (telemetria) | Interessou, não fechou |
| 3 | mai | Misto (multa + renovação + aviso contra devolução antecipada) | Fechou (renovação) |

---

### cliente_17086353 — Andreza / Jeferson + Pedro (Caratinga)
| # | Data | Tipo | Desfecho |
|---|------|------|----------|
| 1 | mai | Misto (alteração km franqueada + competitor probe) | Fechou (alteração) |
| 2 | mar | Cobrança (12 faturas) | Não era venda |
| 3 | mar | Cobrança (confirmação) | Não era venda |
| 4 | abr | Retenção (verificar demanda + NPS) | Não era venda (manutenção) |

---

### Clientes de 1 ligação
| Cliente | Tipo | Desfecho |
|---------|------|----------|
| 1345044 | Caixa postal | Sem conteúdo |
| 16194344 | Cobrança | Não era venda |
| 16894398 | Nova reserva (sem disponibilidade) | Não fechou |
| 19361952 | Dúvida pós-venda (sinistro terceiro) | Não era venda |
| 20627315 | Dúvida pós-venda (franquia acidente) | Não era venda |
| 8583331 | Suporte técnico (biometria) | Não era venda |

---

## Insights por tipo de ligação

**Suporte operacional (25% das ligações)**
Maior categoria isolada. O vendedor é frequentemente o primeiro ponto de contato para problemas que não são de sua alçada (portal, sistema, manutenção). Isso consome tempo comercial mas cria oportunidades de upsell quando bem aproveitado.

**Misto (8% — maior potencial ignorado)**
Ligações que começam como suporte e têm tentativa comercial inserida pelo vendedor. Essa categoria tem a maior densidade de comportamentos Challenger e a maior taxa de conversão per capita.

**Cobrança (11%)**
Nenhuma conversão comercial direta. Mas gera churn quando mal gerenciada. A abordagem de Andreza — ligar antes do bloqueio automático e com tom empático — é melhor prática.

**Nova venda pura (9%)**
Rara nesta base. Quando ocorre, vem do cliente (inbound) ou de prospecção ativa de novo produto (ex: Pedro descobre que cliente tem caminhões próprios).
