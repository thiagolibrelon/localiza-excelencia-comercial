# Análise 2 — Problemas Recorrentes
**Base:** 14 clientes, ~87 ligações analisadas

---

## Mapa de problemas sistêmicos

> Problema sistêmico = aparece em 2+ clientes sem relação entre si.

---

### 1. Acesso ao portal de faturamento
**Frequência:** 5 clientes afetados (22153452, 25257738, 8583331, 21578554, 8127924)
**Manifestações:**
- Senha inválida / esquecida → processo de reset por email é lento (caso: 2,5h para chegar o email)
- Login mostrando empresa anterior (ex: cliente mudou de empresa mas acesso antigo persiste)
- Portal financeiro e portal de reservas são dois links distintos — cliente não sabe qual usar
- Biometria no cadastro de condutor falha após o processo de redefinição
- Dois portais separados (reservas e faturamento) com credenciais diferentes — causa confusão

**Impacto no negócio:** Vendedor ocupa 20-40 minutos de chamada em suporte técnico por ligação. Estimativa: ~15 ligações nesta base são suporte de acesso = ~4-6h de tempo comercial perdido.

**Causa raiz provável:** UX/onboarding inadequado. Dois portais com fluxos distintos, sem instrução clara na contratação.

---

### 2. Multa atribuída ao condutor errado
**Frequência:** 3 clientes (22153452, 22154206, 25257738)
**Manifestações:**
- Multa vem no nome de ex-funcionário demitido
- Cliente não sabe o prazo para indicar o condutor correto
- Processo de contestação de multa não é transparente ao cliente
- Vendedor precisa explicar o fluxo de dentro para fora a cada vez

**Impacto no negócio:** Desgaste emocional alto ("não é culpa minha"). Risco de churn quando o cliente sente injustiça. Impacto financeiro real quando multa alta.

---

### 3. Veículo em manutenção sem substituto imediato
**Frequência:** 4 clientes (21578554, 25257738, 20627315, 9322936)
**Manifestações:**
- Cliente leva carro para manutenção → manutenção dura mais de 4h → substituto prometido mas não disponível
- Vendedor precisa acionar agência via WhatsApp e aguardar resposta manual
- Não há visibilidade de status de manutenção pelo executivo de contas (só o 0800 tem acesso)
- Caso grave: Camila/Wagner — veículo ficou 4h sem substituto, cliente foi ao 0800 e depois para o supervisor

**Impacto no negócio:** Operação do cliente travada. Ruptura de confiança na Localiza, não no vendedor. Risco de churn pós-incidente.

---

### 4. Km excedente cobrado incorretamente
**Frequência:** 2 clientes documentados (22153452, 22154206)
**Manifestações:**
- Sistema abriu contrato com 1.000 km em vez de 3.000 km por erro de migração
- Gerou fatura de R$18.000 de km excedente (caso Pedro/Gerson)
- Cliente não percebeu durante o período — só soube quando a fatura chegou
- Negociação de desconto (50% = R$8.000 de economia) demorou e exigiu escalada para diretoria

**Impacto no negócio:** Alto risco financeiro. Cliente que recebe uma fatura 10x maior que o esperado tem churn imediato se o vendedor não agir como advogado interno. Neste caso, Pedro salvou a conta.

---

### 5. Reserva caindo em status "sob consulta" ao editar
**Frequência:** 2 clientes (21578554, 25257738)
**Manifestações:**
- Cliente edita uma reserva existente → sistema coloca em "sob consulta" em vez de confirmar
- Cliente não entende por que editou e ficou pendente
- Vendedor precisa acionar agência para confirmar manualmente

**Impacto no negócio:** Gera insegurança operacional. Cliente não sabe se vai ter carro.

---

### 6. Processo diferente em agência franqueada vs. corporativo
**Frequência:** 3 clientes (17086353, 22154206, 22153452)
**Manifestações:**
- Agência franqueada tem processo próprio para alteração de contrato (km, condutor, grupo de veículo)
- Vendedor corporativo precisa intermediar entre cliente, franquia e sistema interno
- Fatura da franquia às vezes não é baixada automaticamente após pagamento
- Cliente não sabe para quem ligar: agência franqueada ou executivo corporativo?

**Impacto no negócio:** Experiência fragmentada. O cliente sente que está "no meio" de duas estruturas que não se comunicam.

---

### 7. Boleto enviado para pessoa/empresa errada
**Frequência:** 2 clientes (6572518, 16194344)
**Manifestações:**
- Boleto vai para terceiro (J.Vê Caldeiraria) que usa carro em nome do cliente
- Terceiro não repassa → conta fica com faturas em aberto → risco de bloqueio de frota
- Vendedor não tem visibilidade do fluxo de pagamento do terceiro

**Impacto no negócio:** Inadimplência involuntária. Cliente paga, terceiro não passa adiante.

---

### 8. Demora excessiva no processo de cobrança de sinistro
**Frequência:** 3 clientes (20627315, 19361952, 25257738)
**Manifestações:**
- Cliente tem acidente → não sabe qual é o valor da franquia
- Processo de sinistro é controlado por equipe de assistência, não pelo executivo
- Executivo não tem acesso ao relatório de sinistro
- Cliente precisa ligar para o 0800 para qualquer informação de sinistro

**Impacto no negócio:** Vendedor perde a oportunidade de ser o ponto de confiança no momento mais crítico. Cliente sente abandono exatamente quando mais precisa de suporte.

---

## Resumo: Onde estão os gargalos

| Categoria | Problemas mapeados | Quem resolve |
|-----------|-------------------|--------------|
| **Tecnologia/UX** | Portal (2 links), biometria, reserva "sob consulta" | Produto/TI |
| **Processos internos** | Km excedente por migração, franqueada vs corporativo | Operações |
| **Comunicação pós-venda** | Sinistro sem acesso do executivo, manutenção sem visibilidade | CS / Assistência |
| **Gestão de terceiros** | Boleto enviado para condutor, não para empresa | Financeiro / Billing |
| **Gestão de condutores** | Multa em ex-funcionário, acesso de demitido no portal | Produto / Processos |

---

## Padrão de comportamento do vendedor diante de problemas

**Melhores práticas observadas:**
- Pedro (22153452): liga pro cliente antes de o cliente perceber o problema da fatura de R$18k
- Andreza (8127924): resolve a fatura da franqueada sem pedir para o cliente ligar para o 0800
- Camila (21578554): copia supervisora no email de manutenção para dar credibilidade à escalada
- Gabriela (25257738): orienta a não devolver o carro cedo para evitar custo desnecessário

**Práticas que precisam melhorar:**
- Transferir para o 0800 sem antes tentar resolver (Ana Paula, cliente 19361952)
- Não registrar o problema antes de encerrar a ligação (Poliana, cliente 9322936)
- Não aproveitar a ligação de suporte para perguntar algo comercial no final (Lucas, 6572518)
