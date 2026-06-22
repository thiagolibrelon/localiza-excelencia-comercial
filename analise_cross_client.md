# Análise Cross-Client — 14 clientes, 87 ligações
**Projeto:** Localiza — O que o vendedor fala que gera conversão?

---

## Mapa de Clientes

| Cliente | Ligs | Executivo | Desfecho | Intenção de entrada |
|---------|------|-----------|----------|---------------------|
| 22154206 | 31 | Carla | **Fechou** (renovações + upsell contínuo) | Ativo — renovações de rotina |
| 9322936 | 11 | Weverton | **Fechou** (nova venda contrato 12m + manutenção de conta) | Misto (cliente buscou + vendedor prospecta upsell) |
| 6572518 | 11 | Lucas | **Não era venda** (pós-venda: boleto, sinistro, avaria) | Cliente com problemas operacionais |
| 25257738 | 9 | Gabriela | **Fechou** (troca de plano + renovações) | Cliente ativo querendo otimizar frota |
| 22153452 | 6 | Pedro | **Não era venda direta** (suporte: acesso, km excedente, multas) | Cliente com erros sistêmicos acumulados |
| 21578554 | 6 | Camila | **Interessou mas não fechou** (proposta 50 carros aguardando aprovação) | Vendedor prospecta + cliente inicia |
| 8127924 | 3 | Andreza | **Manutenção** + upsell tentado de telemetria | Vendedor prospecta queda de volume |
| 17086353 | 4 | Andreza | **Manutenção** (retenção + cobrança) | Vendedor prospecta retenção |
| 16894398 | 1 | Carla | **Interessou** (reserva sem disponibilidade) | Cliente iniciou reserva |
| 20627315 | 1 | Vilma | **Não era venda** (dúvida de franquia pós-acidente) | Cliente com problema |
| 19361952 | 1 | Ana Paula | **Não era venda** (dúvida de sinistro de terceiro) | Cliente com problema |
| 16194344 | 1 | n/id | **Não era venda** (cobrança faturas atrasadas) | Cobrança |
| 8583331 | 1 | Gabriela | **Não era venda** (suporte: biometria no portal) | Problema técnico |
| 1345044 | 1 | n/id | **Não era venda** (caixa postal) | Sem conteúdo |

---

## Os 9 Comportamentos que aparecem nos fechamentos

### 1. Ligação proativa antes do cliente reclamar
**Aparece em:** 22154206 (Carla), 8127924 (Andreza), 17086353 (Andreza), 25257738 (Gabriela)

Vendedor detecta queda de volume, contrato vencendo ou reserva parada e liga sem que o cliente peça. Nas contas que diminuíram volume, a pergunta direta "você está usando outra empresa?" aparece em 100% dos casos onde houve retenção bem-sucedida.

---

### 2. Pergunta de necessidade antes de apresentar produto
**Aparece em:** 9322936 (Weverton), 25257738 (Gabriela), 21578554 (Camila)

Exemplos reais gravados:
- *"Vocês precisam de espaço? Com o que trabalham?"* → cliente do delivery → ofereceram Furgão em vez de HB20
- *"Qual cidade vai ser a retirada?"* → Camila ajusta proposta de 50 carros por cidade

---

### 3. Âncora de preço (mostrar o mais caro primeiro)
**Aparece em:** 25257738 (Gabriela), 9322936 (Weverton)

Gabriela apresentou Furgão a R$4.700, depois mostrou grupo GC a R$3.550 — o segundo parece "barato" em comparação. Weverton usou lógica inversa: HB20 elétrico a R$3.600 vs TAO a R$4.200 → o mais barato justificado por ROI.

---

### 4. Uso explícito do histórico do cliente
**Aparece em:** 22154206 (Carla), 8127924 (Andreza), 17086353 (Andreza), 22153452 (Pedro), 25257738 (Gabriela)

Exemplos reais:
- *"O contrato de vocês foi em outubro, já completou a fidelidade — não tem multa para trocar"* → desbloqueou mudança de plano
- *"Desde dezembro vi que vocês devolveram muito carro sem repor"* → abriu conversa sobre churn
- *"Só vocês entre 800 empresas têm esse desconto especial"* → argumento de retenção

---

### 5. Proteção do cliente contra erro de custo
**Aparece em:** 25257738 (Gabriela), 8127924 (Andreza)

*"Se você devolver na sexta em vez de segunda, vai cair em diária e sai o dobro do mensal — não vale a pena."*

Esse comportamento cria confiança porque o vendedor atua contra o próprio interesse imediato da locadora.

---

### 6. Upsell encaixado naturalmente
**Aparece em:** 8127924 (Andreza), 9322936 (Weverton), 22154206 (Carla)

Não é pitch de vendas puro — o upsell entra como solução para um problema que o cliente já tem:
- Telemetria: *"Você falou que tem problema com condutores, né? Por R$50/mês você acompanha cada um em tempo real"*
- Elétrico: *"O TAO usa só energia, sem combustível — economiza X por km vs carro a gasolina"*
- Contrato anual: *"Se fechar 12 meses agora, trava o preço — porque em março tem readequação"*

---

### 7. Criação de urgência baseada em fato real (não pressão falsa)
**Aparece em:** 25257738 (Gabriela), 17086353 (Andreza)

Gabriela: *"Contratos têm readequação em março e setembro. Se fechar 12 meses hoje, está imune."*
Andreza: *"Quando entrar na cadeia de cobrança pode bloquear os carros."*

Ambos são fatos reais do sistema — não promessas vagas.

---

### 8. Advocacy interno (defesa do cliente dentro da empresa)
**Aparece em:** 22153452 (Pedro), 8127924 (Andreza), 21578554 (Camila)

Pedro conseguiu R$8.000 de desconto em km excedente negociando com a gerência. Disse ao cliente: *"Eu bato pela sua causa lá dentro."*
Andreza resolveu fatura não baixada da agência franqueada sem deixar o cliente ligar para o 0800.
Camila colocou a supervisora em cópia para acelerar substituição de veículo.

---

### 9. Rapport genuíno (não forçado)
**Aparece em:** 8127924 (Andreza), 22153452 (Pedro), 17086353 (Andreza)

Andreza (para Alexandre, Fortal): *"Você pode ficar à vontade de me falar o que não tá legal — a Localiza sem você não existe."*
Pedro para Gerson: *"Mano, eu me sinto muito mal não ter conseguido isentar tudo — mas consegui R$8k de desconto."*

Isso gera fidelização emocional além do contrato.

---

## O que distingue "fechou" de "interessou mas não fechou"

| Situação | Padrão observado |
|----------|-----------------|
| **Fechou** | Vendedor controlou o processo end-to-end: fez perguntas, identificou necessidade, âncora de preço, urgência real, removeu objeção operacional |
| **Interessou mas não fechou** (Wagner/Camila) | Venda dependia de aprovação de terceiro fora do controle do vendedor. Camila fez tudo certo. Obstáculo era externo |
| **Interessou mas não fechou** (Luiz Eduardo/Carla) | Carro não disponível na agência. Obstáculo operacional |
| **Não era venda** | Ligações 100% de suporte pós-venda. Nenhum esforço comercial feito |

**Insight crítico:** Em todas as contas que mantiveram volume ou cresceram, o vendedor detectou o sinal de saída *antes* do cliente verbalizar. Nas contas que reduziram (17086353), a retenção foi possível porque a abordagem foi direta: *"Você tá usando outra empresa?"* e o cliente respondeu com honestidade, mantendo a relação.

---

## Padrões por vendedor

| Vendedor | Ponto forte | Ponto de atenção |
|----------|-------------|-----------------|
| **Carla** | Gestão de múltiplos contratos, renovação automática | Poucas ligações de prospecção ativa de novo produto |
| **Weverton** | Explicações técnicas profundas, ROI numérico, paciência com cliente menos experiente | Conversa longa pode perder cliente com pouco tempo |
| **Andreza** | Relacionamento, detecção proativa de churn, advocacy, NPS | Cobrança às vezes é o único assunto (modo reativo) |
| **Gabriela** | Âncora de preço, proteção do cliente de erro de custo, gestão de condutores | Disponibilidade de veículo depende da operação |
| **Camila** | Qualificação de demanda grande (50 carros), documenta tudo, copia supervisora | Sem conversão da conta grande ainda documentada |
| **Pedro** | Negociação interna, advocacy explícito, explicações de sistema para o cliente | Muito tempo em suporte técnico (acesso, portal, sistema) |
| **Lucas** | Pós-venda sólido, NPS | Poucas ligações de crescimento de conta observadas |

---

## Sequência observada nas ligações que converteram

1. **Abertura com contexto** — vendedor cita o histórico da conta ("vi que vocês devolveram muito carro")
2. **Pergunta de diagnóstico** — antes de oferecer qualquer coisa ("como que tá a frota de vocês?")
3. **Verificação de concorrência** — direta ou indireta ("tá usando outra empresa?")
4. **Âncora de preço** — apresenta opção mais cara primeiro, depois a solução
5. **Urgência real** — data de readequação, risco de bloqueio, prazo de disponibilidade
6. **Fechamento assumido** — "já faço a reserva" ou "já peço a aprovação aqui" sem esperar o cliente dar sinal explícito
