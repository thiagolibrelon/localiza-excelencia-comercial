# Lógica de Scoring de Potencial Comercial
## Sistema de Avaliação Automática de Ligações — Localiza Frota PJ

---

## 1. O Problema que Estamos Resolvendo

> **"De 1.275 ligações, quantas tinham potencial comercial real — e esse potencial foi aproveitado?"**

Sem critérios claros, qualquer resposta é subjetiva.
O scoring transforma essa pergunta em um número rastreável, comparável e repetível.

---

## 2. O Que É "Potencial Comercial"?

Definição operacional adotada:

> Uma ligação tem **potencial comercial** quando existe pelo menos um dos três elementos:
> 1. **Contexto favorável** — a ligação durou tempo suficiente e teve natureza comercial
> 2. **Sinal do cliente** — o cliente revelou oportunidade de negócio (expansão, churn, concorrente)
> 3. **Comportamento do vendedor** — o vendedor aplicou ações que correlacionam com fechamento

Potencial **não é** sinônimo de fechamento. Uma ligação pode ter potencial alto e o vendedor desperdiçar (oportunidade perdida). Pode também ter potencial baixo e ainda gerar negócio por acaso. O scoring captura o potencial da situação, não o resultado isolado.

---

## 3. Arquitetura do Score

O score total varia de **0 a 30 pontos**, dividido em 3 dimensões independentes:

```
POTENCIAL COMERCIAL (0-30) =
    Dimensão 1: Contexto       (0-10)  ← P2 + P12
  + Dimensão 2: Sinais Cliente (0-10)  ← P11 + P15 + P4
  + Dimensão 3: Vendedor       (0-10)  ← P1 + P5 + P9 + P10
```

**Por que 3 dimensões separadas?**
Porque elas medem coisas distintas. Uma ligação pode ter sinal forte do cliente (expansão detectada) mas vendedor fraco. Ou vendedor excelente em ligação curta de suporte. Separar as dimensões permite entender **onde está o gap**, não apenas se há potencial.

---

## 4. Dimensão 1 — Contexto (0-10 pts)
*Fonte dos prompts: P2 (Tipo de Ligação) e P12 (Talk Ratio)*

**Pergunta que responde:** *"Esse contexto permite uma ação comercial?"*

### 4.1 Duração (0-4 pontos)
| Duração | Pontos | Racional |
|---------|--------|---------|
| > 10 min | 4 | Conversa profunda; múltiplos temas abordados |
| > 5 min | 3 | Conversa substantiva com troca real de informação |
| > 2 min | 2 | Conteúdo suficiente para análise qualificada |
| > 30s | 1 | Curta, mas com algum conteúdo |
| < 30s | 0 | Superficial demais para extrair qualquer sinal |

**Por quê?** O P12 (Talk Ratio) mostrou que ligações mais longas têm mais turns, mais perguntas e mais abertura para diálogo. Não há como fazer diagnóstico comercial em 20 segundos.

### 4.2 Quem Iniciou (0-2 pontos)
| Quem ligou primeiro | Pontos | Racional |
|---------------------|--------|---------|
| Vendedor (A) | 2 | Indica ligação proativa — comportamento B8 do framework |
| Cliente (C) | 1 | Cliente pode estar sinalizando algo; contexto aproveitável |

**Por quê?** O comportamento B8 ("ligar proativamente por motivo comercial") recebe peso=1 no framework P1. Vendedor que liga é vendedor que está buscando negócio, não apenas respondendo.

### 4.3 Natureza da Ligação (0 a +4 / −2 pontos)
| Sinal | Pontos | Racional |
|-------|--------|---------|
| 3+ sinais comerciais no discurso do vendedor | +4 | Ligação tem componente de venda ativo |
| 1-2 sinais comerciais | +2 | Componente comercial parcial |
| 0 comerciais + 3+ sinais operacionais | −2 | Ligação puramente de suporte sem janela de venda |

**Sinais comerciais buscados:** proposta, valor, cotação, desconto, renovar, migrar, contrato, reserva, fechar, mensal, locação.

**Sinais operacionais buscados:** biometria, senha, boleto, avaria, oficina, sinistro, multa, condutor, portal fora.

**Por quê?** O P2 classifica ligações em tipos. Ligações de suporte puro têm contexto diferente de ligações de renovação ou nova venda. O framework não descarta ligações operacionais — elas ainda podem ter janela de upsell — mas parte de um patamar menor.

---

## 5. Dimensão 2 — Sinais do Cliente (0-10 pts)
*Fonte dos prompts: P11 (Intel Competitiva), P15 (Eventos Raros), P4 (Health Score)*

**Pergunta que responde:** *"O cliente revelou alguma oportunidade nessa ligação?"*

### 5.1 Sinal de Expansão (+4 pontos)
**Palavras buscadas:** nova filial, nova unidade, mais carros, mais veículos, expandindo, crescendo, novos funcionários, novo contrato, mineradora, nova obra, aumentar frota.

**Racional:** O P15 classifica expansão como evento R1 — evento raro de alto impacto. Um cliente que menciona crescimento é cliente com demanda imediata de veículos. Este é o sinal de maior valor por isso recebe a pontuação mais alta da dimensão.

**Exemplo real encontrado nas análises:** Cliente 27226042 (Eduardo) mencionou contrato de mineradora em Paragominas/PA com potencial de 2 anos — Rodrigo identificou, mas sem proposta de longo prazo na hora.

### 5.2 Concorrente Mencionado pelo Cliente (+3 pontos)
**Palavras buscadas:** Unidas, Movida, Móvel, Hertz, Avis, outra locadora, frota própria, carro próprio, outro fornecedor.

**Racional:** O P11 (Intel Competitiva) classifica esse sinal como IC1 (menção direta a concorrente) ou IC5 (comparação implícita). Cliente que cita concorrente está em processo de avaliação ou divisão de frota. É o momento exato para diferenciar.

**Exemplo real:** Cliente 24961959 (Cláudio) divide frota entre Localiza, Unidas e Móvel. Carla soube porque perguntou. Os demais vendedores nunca saberiam.

### 5.3 Sinal de Churn (+3 pontos)
**Palavras buscadas:** cancelar, não vou mais, vai cortar, excluir a localiza, não tenho interesse, vou devolver tudo, encerrar contrato.

**Racional:** O P15 classifica churn como evento R2 — ação imediata necessária. Um cliente em risco de saída tem urgência máxima. O score alto aqui sinaliza que a ligação precisa de follow-up prioritário, não que tudo está bem.

**Exemplo real:** Cliente 03096291 usou a frase literal "vou excluir a localiza daqui" — ninguém escalou automaticamente porque não há sistema de alerta.

### 5.4 Dores do Cliente (+1 a +2 pontos)
**Palavras buscadas nos turnos do cliente:** avaria, multa, problema, erro, cobrar, fatura incorreta, quilometragem excedente, demora, não tem.

**Racional:** O P6 (Oportunidades Perdidas) categoriza como OP2 a situação onde o cliente revela uma dor mas o vendedor não conecta a um produto. Cada dor é uma janela. 2+ dores = ligação com múltiplas janelas.

---

## 6. Dimensão 3 — Comportamento do Vendedor (0-10 pts)
*Fonte dos prompts: P1 (B1-B10), P5 (Challenger), P9 (Abertura/Fechamento), P10 (Promessas)*

**Pergunta que responde:** *"O vendedor aplicou os comportamentos que o framework identifica como correlacionados com fechamento?"*

Os pesos desta dimensão são derivados **diretamente dos pesos do P1**, que foram definidos com base em comportamentos que diferenciam fechamentos dos não-fechamentos.

### 6.1 Pergunta Diagnóstica antes do Produto — B1 (+2 pontos)
**Palavras buscadas no discurso do vendedor:** como está, qual é a, quanto roda, tem demanda, como funciona, quais são, quantos carros, como está a frota, me conta, me fala um pouco.

**Racional:** B1 tem peso=2 no framework P1. Vendedor que entende a necessidade antes de propor tem proposta mais aderente, menos objeção de "não é o que eu preciso". O P14 mostrou que Rodrigo e Carla fazem diagnóstico profundo; Ramiro e Everton perguntam apenas "tem demanda?" — diferença crítica.

### 6.2 Sondagem de Concorrente ou Frota Própria — B10 (+3 pontos)
**Palavras buscadas no discurso do vendedor:** outra locadora, frota própria, tem frota, outra empresa de locação, usa alguma outra, aluga em outro lugar, tem veículo próprio.

**Racional:** B10 tem **peso=3 no P1 — o maior do framework**, empatado com B6. A análise das 35 ligações mostrou que apenas Carla faz essa pergunta sistematicamente. É o comportamento mais discriminante entre top performers e medianos. Quem não pergunta, não sabe que o cliente está dividido entre concorrentes.

**Penalidade:** Se o cliente citou concorrente mas o vendedor não explorou → −1 ponto (oportunidade P11 desperdiçada).

### 6.3 Urgência com Fato Verificável — B6 (+3 pontos)
**Palavras buscadas no discurso do vendedor:** hoje, amanhã, prazo, vence, último dia, essa semana, antes que, contrato encerra, renovar agora, fechar ainda hoje.

**Racional:** B6 tem **peso=3 no P1 — o maior do framework**, empatado com B10. Urgência real (baseada em fato, não pressão) cria âncora temporal para o cliente decidir. Sem urgência, "qualquer coisa me chama" é a saída padrão.

### 6.4 Upsell Conectado à Dor — B5 (+2 pontos)
**Palavras buscadas no discurso do vendedor:** proteção, telemetria, upgrade, quilometragem maior, categoria superior, contrato anual, elétrico, cobertura total.
(Ativado apenas se há contexto comercial ≥ 2 sinais — evita falso positivo em menção casual)

**Racional:** B5 tem peso=2 no P1. O P7 (Cross-sell/Upsell) e P6 (Oportunidades Perdidas) mostram que upsell desconectado da dor do cliente raramente converte. Thais é a melhor nisso: identifica que cliente está próximo do limite de diárias e propõe mensal antes que ele devolva o carro.

### 6.5 Usou Histórico do Cliente — B3 (+1 ponto)
**Palavras buscadas:** vi aqui, no cadastro, no seu histórico, na nossa base, você já, faz tempo que, última vez que, no sistema aqui, já é cliente.

**Racional:** B3 tem peso=1 no P1. Personalização com dados reais do cliente aumenta credibilidade. Carla faz isso sistematicamente — menciona condições comerciais anteriores antes de qualquer proposta.

### 6.6 Alerta ao Cliente — B4 (+1 ponto)
**Palavras buscadas:** fique atento, cuidado com, antes que, se não renovar, risco de, pode gerar multa, vai perder, importante que.

**Racional:** B4 tem peso=2 no P1. Vendedor que alerta o cliente age como consultor, não como tirador de pedido. Cria credibilidade e senso de urgência legítima.

### 6.7 Fechamento com Próximo Passo — P9 FC1/FC2 (+2 pontos / −1 penalidade)
**Sinais de próximo passo concreto (+2):** combinado, fica assim então, te ligo na, retorno amanhã, deixa agendado, próximo passo, você me confirma até.

**Sinais de fechamento vago (−1):** qualquer coisa me chama, surgindo demanda, pode me procurar, à disposição, qualquer dúvida.

**Racional:** O P9 classifica fechamentos em FC1-FC5. FC1 (compromisso duplo com prazo) e FC2 (próximo passo só do vendedor) são os únicos que criam âncora para continuação. FC3 e FC4 deixam o cliente sem referência temporal. O P14 mostrou que Rodrigo e Carla sempre definem ação concreta; Ramiro e Everton terminam com "qualquer coisa me fala" sem data.

### 6.8 Promessa Feita — P10 (+1 ponto)
**Palavras buscadas:** vou te mandar, vou enviar, te ligo, vou verificar, vou resolver, vou contestar, vou fazer, providencio.

**Racional:** O P10 rastreia promessas como indicador de comprometimento. Promessa feita = vendedor assumiu responsabilidade = maior chance de follow-up. (Ponto positivo por comprometimento; risco de promessa sem prazo é monitorado separadamente.)

---

## 7. Classificação Final

| Score Total | Nível | Interpretação |
|-------------|-------|---------------|
| 20 – 30 | **ALTO** | Ligação com contexto, sinais e comportamento alinhados. Máxima prioridade de análise e follow-up. |
| 13 – 19 | **MÉDIO** | Há potencial mas algo faltou: contexto curto, sinal não explorado ou vendedor abaixo do esperado. |
| 7 – 12 | **BAIXO** | Potencial existe mas fraco. Geralmente ligação de suporte com uma janela commercial menor. |
| 0 – 6 | **SEM POTENCIAL** | Ligação puramente operacional ou sem conteúdo suficiente para análise comercial. |

---

## 8. O Que Este Scoring NÃO Faz

É importante ser honesto sobre as limitações:

1. **Não detecta tom de voz nem emoção** — o STT entrega texto; sarcasmo, entusiasmo e hesitação ficam de fora.
2. **Não é o resultado final** — uma ligação ALTO pode não ter fechado; uma SEM_POTENCIAL pode ter gerado negócio por canal paralelo (WhatsApp, e-mail).
3. **Falsos positivos possíveis** — a palavra "cancelar" pode aparecer em "vou cancelar a reunião" (não a locação). Os dicionários são boas aproximações, não perfeitos.
4. **Depende de STT limpo** — se a transcrição for fragmentada ou com muito `<unk>`, o score pode subestimar o real.

**Como mitigar:** As ligações ALTO e os eventos de churn/expansão devem ser **revisados manualmente** — o scoring é a triagem, não a análise final.

---

## 9. O Que o Scoring Responde

Com os dados de 1.275 ligações classificadas, conseguimos responder:

| Pergunta | Como respondida |
|----------|-----------------|
| Qual % das ligações tem potencial comercial? | Distribuição ALTO + MÉDIO |
| Quais clientes precisam de ação imediata? | Lista de churn + expansão detectados |
| Quais vendedores aproveitam mais as oportunidades? | Score médio por vendedor vs. score de contexto |
| Quais comportamentos aparecem mais nas ligações ALTO? | Frequência de B1, B6, B10 etc. nos ALTO vs. SEM_POTENCIAL |
| Onde o time está deixando dinheiro na mesa? | Ligações MÉDIO com sinal de cliente mas vendedor abaixo da média |

---

## 10. Próximo Passo Recomendado

1. **Rodar o scoring nas 1.275 ligações** (`python scoring_potencial.py`) → 30 segundos
2. **Revisar manualmente as top 20 ligações ALTO** — validar se o score faz sentido na leitura real
3. **Cruzar com os resultados do Gemini** (P1-P15 completos) para confirmar hipóteses
4. **Apresentar distribuição + top clientes para ação** como primeiro entregável de valor

---

*Metodologia: 15-prompt B2B Call Intelligence Framework — Localiza Frota PJ | Junho 2026*
