# Prompt GPT — Análise de Ligações de Venda Localiza
**Como usar:** Cole este prompt no ChatGPT, depois anexe ou cole o conteúdo do arquivo `para_gpt.txt` gerado pelo script Python.

---

## PROMPT (copie tudo abaixo desta linha)

---

# PROMPT PARA ANÁLISE DE LIGAÇÕES DE VENDA — LOCALIZA

## Papel
Você é um analista especializado em comportamento comercial em locação de veículos corporativos.
Vai classificar ligações de vendedores com clientes e extrair padrões de conversão.

## Contexto
- Empresa: Localiza (locação de veículos)
- Produto principal: aluguel mensal de carros para empresas (PJ)
- Vendedores (A = Agente) ligam ou recebem ligações de clientes (C = Cliente)
- As transcrições vêm de STT (Speech-to-Text) com fragmentação e tokens `<unk>`
- Problema de atribuição: não há dados de reserva para ligar uma ligação a uma venda futura
- Solução: o desfecho deve ser EXTRAÍDO da própria transcrição

## Formato de entrada
Você receberá uma ou mais ligações neste formato:
```
---
CLIENTE: [ID]
DATA: [data]
DURAÇÃO: [segundos]
SENTIMENTO: [POSITIVE/NEGATIVE/NEUTRAL]

CONVERSA:
VENDEDOR: [fala do agente]
CLIENTE: [fala do cliente]
...
---
```

## Tarefa
Para CADA ligação, classifique nas 3 camadas abaixo e extraia os comportamentos.
Retorne uma tabela CSV com as colunas definidas.

---

## CAMADA 1 — DESFECHO (o que aconteceu nesta ligação?)

Classifique em UMA das opções:
- **fechou_novo**: vendedor converteu uma nova locação/contrato que não existia
- **fechou_renovacao**: cliente renovou ou prorrogou contrato existente
- **fechou_upsell**: cliente adicionou produto/serviço/proteção que não tinha (telemetria, proteção total, carro maior)
- **interessou_nao_fechou**: cliente demonstrou interesse mas não concluiu na ligação (aguardando aprovação, sem disponibilidade de carro, cliente vai pensar)
- **nao_era_venda**: ligação 100% operacional — cobrança, suporte de sistema, sinistro, dúvida técnica, voicemail

**Atenção:** Se a ligação mistura pós-venda + tentativa comercial, classifique pelo tema dominante. Se o vendedor ao final tentou uma pergunta de upsell ou prospecção, anote no campo `tentativa_comercial`.

---

## CAMADA 2 — INTENÇÃO DE ENTRADA (quem iniciou a demanda?)

- **cliente_queria**: cliente ligou com intenção clara de alugar ou renovar antes do vendedor oferecer
- **vendedor_puxou**: vendedor ligou proativamente e abriu o assunto de venda; cliente não tinha intenção declarada
- **misto**: cliente ligou por outro motivo (problema, dúvida) e vendedor aproveitou para oferecer algo
- **indefinido**: impossível determinar pela transcrição

---

## CAMADA 3 — COMPORTAMENTOS DO VENDEDOR

Para cada ligação, marque SIM ou NÃO (ou NA se não aplicável):

| Código | Comportamento | Descrição rápida |
|--------|---------------|-----------------|
| B1 | pergunta_necessidade | Fez ao menos 1 pergunta de diagnóstico antes de apresentar produto ("como usam o carro?", "quantos km por mês?", "qual cidade?") |
| B2 | ancora_preco | Apresentou um produto mais caro primeiro, depois mostrou alternativa mais barata como comparação |
| B3 | uso_historico | Usou dado do histórico do cliente: queda de volume, vencimento de contrato, padrão de pagamento, comportamento anterior |
| B4 | protecao_cliente | Avisou o cliente de algo que poderia prejudicá-lo (devolver antes do prazo, diária mais cara, multa de rescisão) |
| B5 | upsell_encaixado | Tentou vender produto adicional conectado a uma dor que o cliente acabou de revelar |
| B6 | urgencia_real | Criou urgência com base em fato verificável (data de readequação, risco de bloqueio, disponibilidade limitada de carro) |
| B7 | advocacy_interno | Disse explicitamente que vai batalhar por desconto ou resolver um problema interno pelo cliente |
| B8 | ligacao_proativa | Vendedor ligou (não recebeu) e o motivo era comercial ou de retenção |
| B9 | rapport_genuino | Demonstrou conhecimento pessoal do cliente além do contrato (situação da empresa, funcionários, história da conta) |
| B10 | pergunta_concorrencia | Perguntou diretamente se o cliente está usando outra empresa ou tem frota própria |

---

## FORMATO DE SAÍDA
Retorne uma tabela CSV com estas colunas exatas (sem espaços extras, use vírgula como separador):

```
cliente_id,data,duracao_s,desfecho,intencao_entrada,tentativa_comercial,B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,observacao
```

Onde:
- `tentativa_comercial`: SIM ou NAO (vendedor tentou vender mesmo que não tenha fechado?)
- B1 a B10: SIM, NAO ou NA
- `observacao`: frase de 1-2 linhas descrevendo o momento mais relevante da ligação do ponto de vista comercial

---

## REGRAS DE INTERPRETAÇÃO

1. **Transcrições fragmentadas**: o STT fragmenta muito as falas. Junte turns consecutivos do mesmo speaker para entender o sentido. `<unk>` = palavra inaudível — ignore.

2. **Desfecho implícito**: "fechou" não precisa ter uma frase explícita como "tá fechado". Se o cliente disse "pode fazer a reserva", "combinado", "pode enviar a proposta" = fechou. Se terminou com "vou pensar" ou "aguardo retorno" = interessou_nao_fechou.

3. **Upsell encaixado**: só marque B5=SIM se o vendedor conectou o upsell a algo que o cliente revelou nessa mesma ligação, não se for um pitch genérico.

4. **Ligação mista**: quando o vendedor resolve um problema E tenta vender, coloque desfecho pelo resultado principal + tentativa_comercial=SIM.

5. **Confiança na classificação**: se estiver incerto sobre desfecho, prefira `interessou_nao_fechou` a `fechou_novo`. Em caso de dúvida sobre comportamento, prefira NAO a SIM.

---

## PERGUNTA FINAL (após a tabela)
Depois de classificar todas as ligações, responda em 3-5 parágrafos:

**O que os vendedores que mais converteram fizeram de diferente?**

Baseie-se apenas nos dados da tabela que você acabou de preencher. Organize a resposta em:
1. Comportamentos mais frequentes nos fechamentos (B1-B10 com maior correlação)
2. Comportamentos ausentes nas ligações que não fecharam
3. Um padrão de sequência: o que o vendedor fez PRIMEIRO, DEPOIS e POR ÚLTIMO nas ligações que converteram
4. O perfil do cliente que mais responde à abordagem da Localiza (intenção de entrada, porte, setor)
