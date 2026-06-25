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

Além do score, o sistema gera **análises qualitativas** que não entram diretamente na pontuação, mas enriquecem o CSV para análises cruzadas: tipo de abertura, tipo de fechamento, objeções tratadas, promessas sem prazo, fluxo comercial, produtos mencionados. Essas análises estão detalhadas nas seções 7 a 11 deste documento.

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
**Palavras buscadas:** nova filial, nova unidade, mais carros, mais veículos, expandindo, crescendo, novos funcionários, novo contrato, nova obra, aumentar frota.

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

### 5.5 Objeção de Preço detectada (+1 se houve rebuttal)
**Palavras buscadas nos turnos do CLIENTE:** está caro, muito caro, mais barato, desconto, outro lugar mais barato, fora do orçamento.

**Racional:** Objeção não respondida é venda perdida. Mas não basta responder — precisa responder com DADO. Quando o cliente objeta e o vendedor responde com argumento real (ver Seção 8), a ligação recebe +1 ponto extra nesta dimensão. Quando o vendedor capitula em silêncio, não pontua.

---

## 6. Dimensão 3 — Comportamento do Vendedor (0-10 pts)
*Fonte dos prompts: P1 (B1-B10), P5 (Challenger), P9 (Abertura/Fechamento), P10 (Promessas)*

**Pergunta que responde:** *"O vendedor aplicou os comportamentos que o framework identifica como correlacionados com fechamento?"*

Os pesos desta dimensão são derivados **diretamente dos pesos do P1**, que foram definidos com base em comportamentos que diferenciam fechamentos dos não-fechamentos.

### 6.1 Pergunta Diagnóstica antes do Produto — B1 (+2 pontos)
**Palavras buscadas no discurso do vendedor:** como está, qual é a, quanto roda, tem demanda, como funciona, quais são, quantos carros, como está a frota, me conta, me fala um pouco.

**Racional:** B1 tem peso=2 no framework P1. Vendedor que entende a necessidade antes de propor tem proposta mais aderente, menos objeção de "não é o que eu preciso". O P14 mostrou que Rodrigo e Carla fazem diagnóstico profundo; Ramiro e Everton perguntam apenas "tem demanda?" — diferença crítica.

### 6.2 Densidade de Perguntas — proxy quantitativo de B1 (+1 ponto bônus)
**Como medido:** conta o número de "?" nos turnos do vendedor dividido pelo número de turnos. Se a taxa for ≥ 1,5 perguntas por turno, recebe +1 ponto adicional.

**Racional:** B1 detecta se o vendedor perguntou alguma coisa. A densidade vai além: mede se ele fez isso sistematicamente ao longo de toda a ligação. Dos dados, as ligações ALTO têm média de **36,9 perguntas** vs. **6,2 perguntas** nas ligações SEM POTENCIAL — uma diferença de 6x.

### 6.3 Sondagem de Concorrente ou Frota Própria — B10 (+3 pontos)
**Palavras buscadas no discurso do vendedor:** outra locadora, frota própria, tem frota, outra empresa de locação, usa alguma outra, aluga em outro lugar, tem veículo próprio.

**Racional:** B10 tem **peso=3 no P1 — o maior do framework**, empatado com B6. A análise das 35 ligações mostrou que apenas Carla faz essa pergunta sistematicamente. É o comportamento mais discriminante entre top performers e medianos. Quem não pergunta, não sabe que o cliente está dividido entre concorrentes.

**Penalidade:** Se o cliente citou concorrente mas o vendedor não explorou → −1 ponto (oportunidade P11 desperdiçada).

### 6.4 Urgência com Fato Verificável — B6 (+3 pontos)
**Palavras buscadas no discurso do vendedor:** hoje, amanhã, prazo, vence, último dia, essa semana, antes que, contrato encerra, renovar agora, fechar ainda hoje.

**Racional:** B6 tem **peso=3 no P1 — o maior do framework**, empatado com B10. Urgência real (baseada em fato, não pressão) cria âncora temporal para o cliente decidir. Sem urgência, "qualquer coisa me chama" é a saída padrão.

### 6.5 Upsell Conectado à Dor — B5 (+2 pontos)
**Palavras buscadas no discurso do vendedor:** proteção, telemetria, upgrade, quilometragem maior, categoria superior, contrato anual, elétrico, cobertura total.
(Ativado apenas se há contexto comercial ≥ 2 sinais — evita falso positivo em menção casual)

**Racional:** B5 tem peso=2 no P1. O P7 (Cross-sell/Upsell) e P6 (Oportunidades Perdidas) mostram que upsell desconectado da dor do cliente raramente converte. Thais é a melhor nisso: identifica que cliente está próximo do limite de diárias e propõe mensal antes que ele devolva o carro.

### 6.6 Usou Histórico do Cliente — B3 (+1 ponto)
**Palavras buscadas:** vi aqui, no cadastro, no seu histórico, na nossa base, você já, faz tempo que, última vez que, no sistema aqui, já é cliente.

**Racional:** B3 tem peso=1 no P1. Personalização com dados reais do cliente aumenta credibilidade. Carla faz isso sistematicamente — menciona condições comerciais anteriores antes de qualquer proposta.

### 6.7 Alerta ao Cliente — B4 (+1 ponto)
**Palavras buscadas:** fique atento, cuidado com, antes que, se não renovar, risco de, pode gerar multa, vai perder, importante que.

**Racional:** B4 tem peso=2 no P1. Vendedor que alerta o cliente age como consultor, não como tirador de pedido. Cria credibilidade e senso de urgência legítima.

### 6.8 Challenger — Revelou Custo Oculto — CH1 (+1 ponto)
**Palavras buscadas:** mas o que acontece, na hora do sinistro, sem a cobertura, taxa de operação, custo real, no final fica mais caro, o que eles não falam, frota própria tem custo de.

**Racional:** CH1 é o comportamento Challenger mais frequente nos dados (14 ocorrências na amostra). Quando o cliente menciona que o concorrente é mais barato, revelar o custo que ele não havia calculado (sinistro sem cobertura, taxa de operação mais alta, IPVA e manutenção em frota própria) muda a percepção de "mais caro" para "mais seguro". É diferenciação com dado, não com argumento emocional.

### 6.9 Challenger — Antecipação de Problema — CH6 (+1 ponto)
**Palavras buscadas:** vai estourar, vai ultrapassar, logo você vai precisar, com esse crescimento, no ritmo que, antes que vire um problema, alta temporada, disponibilidade vai cair.

**Racional:** CH6 é alertar o cliente sobre um problema que ele ainda não percebeu. "Com esse crescimento de motoristas, seu km vai estourar em setembro" demonstra expertise e cria urgência verdadeira — não inventada para forçar fechamento, mas baseada em projeção real do contexto do cliente.

### 6.10 Tipo de Abertura — P9 AB1-AB5 (+1 ponto / penalidade)
O tipo de abertura é classificado olhando os **primeiros 3 turnos do vendedor** (ver Seção 7 para detalhes completos).

| Tipo | Pontos | Racional |
|------|--------|---------|
| AB1 Contextualizada | +1 | Chegou com dados do cliente — receptor mais aberto |
| AB2 Relacional | 0 | Cria conexão, mas sem informação específica |
| AB3 Genérica | 0 | "Em que posso ajudar?" — cliente sabe que vendedor não sabe nada |
| AB4 Reativa | 0 | Neutro — apenas responde ao que o cliente trouxe |
| AB5 De proteção | penalidade | "Manter cadastro ativo" — sem objetivo comercial |

### 6.11 Tipo de Fechamento — P9 FC1-FC5 (+1 a +3 pts / penalidade)
O tipo de fechamento é classificado olhando os **últimos 5 turnos de cada speaker** (ver Seção 8 para detalhes completos).

| Tipo | Pontos | Racional |
|------|--------|---------|
| FC1 Compromisso duplo | +3 | Ambos assumiram — o único que garante continuidade |
| FC5 Diretivo | +2 | Vendedor disse ao cliente o que fazer |
| FC2 Só do vendedor | +1 | Há próximo passo, mas só um lado assumiu |
| FC4 Aberto | 0 | Nada definido |
| FC3 Vago | penalidade | "Qualquer coisa me chama" — vai para o arquivo morto |

### 6.12 Promessas sem Prazo — P10 (penalidade)
(Ver Seção 9 para detalhes)

Cada promessa detectada SEM palavra de prazo próxima conta como risco. 2+ promessas sem prazo = penalidade registrada no campo `penalidades` do CSV.

---

## 7. Classificação de Abertura (P9 — AB1 a AB5)

Esta análise **não entra diretamente no score principal** mas gera o campo `tipo_abertura` no CSV e aparece no relatório de distribuição.

**Como é detectado:** olhamos apenas os primeiros 3 turnos do vendedor. A abertura define o tom da ligação inteira — depois do terceiro turno, o padrão já está estabelecido.

| Código | Nome | O que detectamos | Impacto |
|--------|------|-----------------|---------|
| AB1 | Contextualizada | "Vi aqui no sistema", "no seu contrato", "você já alugou com a gente" | Melhor: vendedor chegou preparado |
| AB2 | Relacional | "Como você está?", "tudo bem?", "faz tempo" | Boa: cria conexão pessoal |
| AB3 | Genérica | "Em que posso ajudar?", "central de atendimento" | Fraca: cliente sabe que vendedor não sabe nada |
| AB4 | Reativa | Nenhum dos anteriores — vendedor apenas responde | Neutra |
| AB5 | De proteção | "Manter o cadastro ativo", "verificar os dados" | Pior: sem objetivo comercial declarado |

**Resultado na base (1.275 ligações):**
- 87,5% das ligações são AB4 (reativas) — vendedor apenas responde ao que o cliente trouxe
- AB1 aparece em apenas 3,7% — raridade que explica por que a personalização é diferencial

---

## 8. Classificação de Fechamento (P9 — FC1 a FC5)

Esta análise gera o campo `tipo_fechamento` no CSV e entra no score (seção 6.11).

**Como é detectado:** olhamos os últimos 5 turnos de cada speaker separadamente. O fechamento é o que fica na memória do cliente — uma ligação ótima com fechamento vago vai para o arquivo morto.

| Código | Nome | O que detectamos | Eficácia |
|--------|------|-----------------|---------|
| FC1 | Compromisso duplo | Vendedor E cliente assumiram próximo passo com data | Máxima — raridade na base |
| FC2 | Só do vendedor | Vendedor assumiu ("vou te mandar"), cliente não comprometeu | Boa — continuidade depende do vendedor |
| FC3 | Vago | "Qualquer coisa me chama", "à disposição", "pode nos procurar" | Péssima — sem âncora temporal |
| FC4 | Aberto | Nenhum dos outros padrões detectados | Neutra — inclassificável |
| FC5 | Diretivo | "Preciso que você envie até as 16h", "você precisa confirmar até" | Forte — diz ao cliente o que fazer |

**Resultado na base (1.275 ligações):**
- FC4 (aberto/inclassificável): **73,3%** — a maioria das ligações não tem padrão detectável
- FC3 (vago): **18%** — o segundo maior grupo, e o mais prejudicial
- FC1 (compromisso duplo): apenas **14 ligações (1,1%)** — o mais eficaz e o mais raro

**Sinais de FC1 no vendedor:** "te ligo na", "você me confirma até", "combinado então", "deixa agendado para"
**Sinais de FC1 no cliente:** "amanhã eu te ligo", "vou confirmar até", "pode ligar amanhã", "combinado"
**Sinais de FC3:** "qualquer coisa me chama", "surgindo demanda", "à disposição", "se precisar é só ligar"

**Detecção de objeção e rebuttal (campo `objecao_preco` e `rebuttal_detectado`):**
Quando o CLIENTE faz objeção de preço, verificamos se nos 3 próximos turnos do vendedor há argumento real.
- **Rebuttal com dado:** "se você calcular", "incluído no preço", "quando conta tudo", "a diferença é"
- **Capitulação:** ausência desses argumentos nos turnos seguintes
- **Resultado na base:** 77 objeções detectadas | 13 com rebuttal (16,9%) | 64 sem resposta (83,1%)

---

## 9. Promessas e Prazos (P10)

Gera o campo `promessas_sem_prazo` no CSV — número de promessas sem prazo detectadas.

**Como é detectado:** para cada turno do vendedor que contém uma promessa, verificamos se existe uma palavra de prazo em um raio de 80 caracteres ao redor da promessa.

**Palavras de promessa:** vou te mandar, vou enviar, te ligo, vou verificar, vou resolver, vou contestar, providencio, vou retornar.

**Palavras de prazo:** hoje, amanhã, agora, esta semana, até segunda, até terça, até as 17h, em 24 horas, até o final do dia.

| Exemplo | Classificação |
|---------|--------------|
| "Vou te mandar **ainda hoje**" | Promessa COM prazo — risco baixo |
| "Vou te mandar" (sem prazo na frase) | Promessa SEM prazo — risco alto |
| "Te ligo **amanhã de manhã**" | Promessa COM prazo — risco baixo |
| "Te ligo" (sem data) | Promessa SEM prazo — risco alto |

---

## 10. Análise de Talk/Listen Ratio (P12)

O sistema mede **dois tipos diferentes** de proporção de fala:

### 10.1 Turn Ratio (campo `turn_ratio_vendedor`)
**O que é:** proporção dos **turnos de fala** do vendedor sobre o total.
Um "turno" é cada vez que uma pessoa começa a falar — independentemente de quantas palavras disse.

**Exemplo:** Se a ligação tem 50 turnos e o vendedor falou em 30 deles: turn_ratio = 30/50 = **0,60 (60%)**.

**Limitação:** Uma ligação STT fragmentada pode ter muitos turnos curtos que não representam domínio real da conversa.

### 10.2 Word Ratio (campo `word_ratio_vendedor`) — mais preciso
**O que é:** proporção das **palavras** do vendedor sobre o total de palavras da ligação.

**Exemplo:** Se o vendedor falou 800 palavras e o cliente 400: word_ratio = 800/1200 = **0,67 (67%)**.

**Por que importa mais que o turn ratio:** Uma pessoa pode ter muitos turnos curtos ("sim", "entendi") enquanto a outra domina com longos monólogos. O word ratio captura quem realmente falou mais. Vendedor que fala mais de 70% das palavras está monologando — não está ouvindo.

**Referência:** Vendedor ideal fala entre 40% e 60% das palavras. Abaixo de 35% = cliente dominou. Acima de 70% = vendedor não está ouvindo.

**Resultado na base:** A média é 60% para todos os níveis — indica que o time tem tendência a monologar independentemente da qualidade da ligação.

### 10.3 Campos relacionados no CSV
| Campo | O que mede |
|-------|-----------|
| `turns_vendedor` | Número de vezes que o vendedor falou na ligação |
| `turns_cliente` | Número de vezes que o cliente falou |
| `words_vendedor` | Total de palavras ditas pelo vendedor |
| `words_cliente` | Total de palavras ditas pelo cliente |
| `turn_ratio_vendedor` | % dos turnos que foram do vendedor (ex: 0,62 = 62%) |
| `word_ratio_vendedor` | % das palavras que foram do vendedor (ex: 0,67 = 67%) |

---

## 11. Fluxo Comercial (campo `fluxo_comercial`)

**O que é:** identifica em qual terço da ligação o vendedor fez a primeira tentativa comercial.

**Por que importa:** O timing importa tanto quanto o comportamento. Tentar vender no início, antes de resolver o problema do cliente, irrita. No meio é ideal — resolveu primeiro, depois tentou. No fim é tarde demais — o cliente já estava encerrando.

A ligação é dividida em 3 partes iguais pelo número total de turnos:

| Valor no CSV | Significado |
|-------------|------------|
| `inicio` | Primeira tentativa comercial no primeiro terço |
| `meio` | Primeira tentativa no terço do meio — padrão ideal |
| `fim` | Tentativa só no terço final — cliente já estava encerrando |
| `nao_detectado` | Nenhuma tentativa comercial identificada (suporte puro) |

**Resultado na base:**
- 50,4% tentam no início
- 18,3% no meio (ideal)
- 5,7% no fim
- 25,6% não detectado — suporte puro

---

## 12. Produtos Mencionados (campo `produtos_mencionados`)

**O que é:** lista de produtos do portfólio Localiza que foram mencionados na ligação.

**Por que importa:** A Localiza tem 12+ produtos B2B. A maioria dos vendedores menciona apenas 2-3. Saber quais foram mencionados é o insumo para identificar gaps de cross-selling (Framework P7).

| Código no CSV | Produto |
|-------------|---------|
| `telemetria` | Rastreamento e gestão de frota |
| `protecao_total` | Cobertura total sem franquia |
| `eletrico` | Veículos elétricos ou híbridos |
| `pesados` | Utilitários, vans, caminhões |
| `mensal_fixo` | Contrato mensal com fidelidade |
| `mensal_flex` | Contrato mensal sem multa por devolução |
| `diario` | Locação por diária |
| `webcorp` | Portal de gestão online |
| `nenhum` | Nenhum produto específico mencionado |

---

## 13. Classificação Final

| Score Total | Nível | Interpretação |
|-------------|-------|---------------|
| 20 – 30 | **ALTO** | Ligação com contexto, sinais e comportamento alinhados. Máxima prioridade de análise e follow-up. |
| 13 – 19 | **MÉDIO** | Há potencial mas algo faltou: contexto curto, sinal não explorado ou vendedor abaixo do esperado. |
| 7 – 12 | **BAIXO** | Potencial existe mas fraco. Geralmente ligação de suporte com uma janela commercial menor. |
| 0 – 6 | **SEM POTENCIAL** | Ligação puramente operacional ou sem conteúdo suficiente para análise comercial. |

---

## 14. Glossário Completo dos Campos do CSV

Todo campo do arquivo `scoring_potencial.csv` explicado em linguagem de negócio.

### Identificação
| Campo | Tipo | O que é |
|-------|------|---------|
| `client_id` | texto | ID numérico do cliente (anonimizado) |
| `data` | data | Data da ligação (YYYY-MM-DD) |
| `duracao_s` | número | Duração da ligação em segundos |
| `sentimento` | texto | Sentimento detectado no STT (positivo/negativo/neutro) |

### Score Principal
| Campo | Tipo | O que é |
|-------|------|---------|
| `nivel` | texto | Classificação: ALTO / MEDIO / BAIXO / SEM_POTENCIAL |
| `score_total` | 0-30 | Soma das 3 dimensões |
| `score_contexto` | 0-10 | Dimensão 1: o contexto permitia ação comercial? |
| `score_cliente` | 0-10 | Dimensão 2: o cliente revelou oportunidade? |
| `score_vendedor` | 0-10 | Dimensão 3: o vendedor aplicou os comportamentos certos? |

### Talk/Listen Ratio (P12)
| Campo | Tipo | O que é |
|-------|------|---------|
| `turns_vendedor` | número | Quantas vezes o vendedor falou (número de alternâncias de fala) |
| `turns_cliente` | número | Quantas vezes o cliente falou |
| `words_vendedor` | número | Total de palavras ditas pelo vendedor |
| `words_cliente` | número | Total de palavras ditas pelo cliente |
| `turn_ratio_vendedor` | 0-1 | % dos turnos que foram do vendedor (0,60 = 60%) |
| `word_ratio_vendedor` | 0-1 | % das palavras que foram do vendedor — mais preciso que turn ratio |

### Comportamentos B1-B10 e Challenger
| Campo | Tipo | O que é |
|-------|------|---------|
| `tem_diagnostico` | 0/1 | Vendedor fez diagnóstico antes de propor? (B1) |
| `tem_urgencia` | 0/1 | Vendedor criou urgência com fato real? (B6) |
| `tem_sondagem_concorrente` | 0/1 | Vendedor perguntou sobre concorrentes ou frota própria? (B10) |
| `tem_upsell` | 0/1 | Vendedor tentou oferecer produto adicional conectado à dor? (B5) |
| `tem_historico` | 0/1 | Vendedor usou dados históricos do cliente? (B3) |
| `tem_alerta` | 0/1 | Vendedor alertou o cliente sobre algum risco? (B4) |
| `tem_ch1` | 0/1 | Vendedor revelou custo oculto para rebater objeção ou diferenciar? (CH1 Challenger) |
| `tem_ch6` | 0/1 | Vendedor antecipou um problema futuro do cliente? (CH6 Challenger) |

### Sinais do Cliente
| Campo | Tipo | O que é |
|-------|------|---------|
| `tem_churn` | 0/1 | Cliente sinalizou cancelamento ou saída? (P15-R2) |
| `tem_expansao` | 0/1 | Cliente sinalizou crescimento ou nova demanda? (P15-R1) |
| `concorrente_cliente` | 0/1 | Cliente mencionou concorrente ou frota própria? (P11) |
| `concorrente_explorado` | 0/1 | Quando o cliente mencionou concorrente, o vendedor aproveitou com argumento? |
| `objecao_preco` | 0/1 | Cliente fez objeção de preço durante a ligação? |
| `rebuttal_detectado` | 0/1 | Vendedor respondeu à objeção com dado real (não capitulou)? |

### Padrões de Abertura e Fechamento (P9)
| Campo | Tipo | O que é |
|-------|------|---------|
| `tipo_abertura` | texto | Como a ligação começou: AB1_contextual / AB2_relacional / AB3_generica / AB4_reativa / AB5_protecao |
| `tipo_fechamento` | texto | Como a ligação terminou: FC1_compromisso_duplo / FC2_so_vendedor / FC3_vago / FC4_aberto / FC5_diretivo |

### Perguntas (proxy de diagnóstico)
| Campo | Tipo | O que é |
|-------|------|---------|
| `n_perguntas_vendedor` | número | Quantidade total de "?" nos turnos do vendedor |
| `densidade_perguntas` | número | Perguntas por turno do vendedor (n_perguntas / turns_vendedor) |

### Promessas (P10)
| Campo | Tipo | O que é |
|-------|------|---------|
| `promessas_sem_prazo` | número | Número de promessas feitas pelo vendedor SEM data/prazo próximo |

### Fluxo e Contexto
| Campo | Tipo | O que é |
|-------|------|---------|
| `fluxo_comercial` | texto | Em qual terço da ligação o vendedor fez a primeira tentativa comercial: inicio / meio / fim / nao_detectado |
| `produtos_mencionados` | texto | Lista de produtos do portfólio mencionados, separados por \| |

### Diagnóstico Textual
| Campo | Tipo | O que é |
|-------|------|---------|
| `razoes` | texto | Lista dos fatores que contribuíram positivamente para o score |
| `penalidades` | texto | Lista dos fatores que geraram penalidade ou alerta |

---

## 15. O Que Este Scoring NÃO Faz

É importante ser honesto sobre as limitações:

1. **Não detecta tom de voz nem emoção** — o STT entrega texto; sarcasmo, entusiasmo e hesitação ficam de fora.
2. **Não é o resultado final** — uma ligação ALTO pode não ter fechado; uma SEM_POTENCIAL pode ter gerado negócio por canal paralelo (WhatsApp, e-mail).
3. **Falsos positivos possíveis** — a palavra "cancelar" pode aparecer em "vou cancelar a reunião" (não a locação). Os dicionários são boas aproximações, não perfeitos.
4. **Depende de STT limpo** — se a transcrição for fragmentada ou com muito `<unk>`, o score pode subestimar o real.
5. **Word ratio uniforme pode indicar STT fragmentado** — quando o ratio é igual em todos os níveis (como observamos a 60%), pode ser artefato de como o STT quebrou os turnos, não comportamento real.

**Como mitigar:** As ligações ALTO e os eventos de churn/expansão devem ser **revisados manualmente** — o scoring é a triagem, não a análise final.

---

## 16. O Que o Scoring Responde

Com os dados de 1.275 ligações classificadas, conseguimos responder:

| Pergunta | Como respondida |
|----------|-----------------|
| Qual % das ligações tem potencial comercial? | Distribuição ALTO + MÉDIO |
| Quais clientes precisam de ação imediata? | Lista de churn + expansão detectados (85 ligações) |
| Quais vendedores aproveitam mais as oportunidades? | Score médio por vendedor vs. score de contexto |
| Quais comportamentos aparecem mais nas ligações ALTO? | Frequência de B1, B6, B10 nos ALTO vs. SEM_POTENCIAL |
| Onde o time está deixando dinheiro na mesa? | Ligações MÉDIO com sinal de cliente mas vendedor abaixo da média |
| O time sabe rebater objeção de preço? | Taxa de rebuttal: 16,9% — capitula em 83% das objeções |
| Como o time fecha as ligações? | FC3 (vago) = 18%, FC4 (sem padrão) = 73%, FC1 (ideal) = 1,1% |
| Quais produtos o time oferta? | Distribuição de `produtos_mencionados` no CSV |

---

*Metodologia: 15-prompt B2B Call Intelligence Framework — Localiza Frota PJ | Junho 2026*
*Versão 2.0 — atualizado após implementação das 10 novas dimensões de análise (25/06/2026)*
