# Prompts 13-15 — Padrões Emergentes, Diferenças entre Vendedores, Eventos Raros
**Como usar:** Cole o prompt desejado no ChatGPT/Fable e anexe/cole o conteúdo das transcrições.
Cada prompt é independente — rode um de cada vez sobre as mesmas transcrições.
Reformatado em 10/07/2026 para o mesmo padrão dos demais arquivos de prompt (`prompts_analises_separados.md` etc.) — conteúdo idêntico ao original, só a formatação mudou. Antes vivia em `prompts/PROMPTS EXTRAS` (arquivo sem extensão `.md`, sem índice, de difícil descoberta).

**Índice de prompts:**
13. Surpresas e padrões emergentes — o que não está sendo capturado pelos prompts atuais
14. Diferenças entre os melhores vendedores — o que os top performers fazem diferente
15. Eventos raros de alto impacto — sinais de baixa frequência e alto impacto

---

---

# PROMPT 13 — SURPRESAS E PADRÕES EMERGENTES
## O que estamos deixando de enxergar?

---

Você é um pesquisador de comportamento comercial B2B.

Seu trabalho NÃO é validar hipóteses existentes. Seu trabalho é encontrar padrões relevantes que aparecem repetidamente nas transcrições mas que NÃO estão explicitamente capturados pelos prompts atuais.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- STT fragmentado — junte turns consecutivos do mesmo speaker. `<unk>` = inaudível, ignore.

## Objetivo
Analise todas as transcrições procurando:

### Categoria S1 — Comportamentos inesperados
Algo que vendedores fazem repetidamente e que não está nas taxonomias atuais.
Exemplos: linguagem específica, forma de encerrar ligação, forma de pedir informação, forma de construir relacionamento.

### Categoria S2 — Comportamentos dos clientes
Algo que clientes fazem ou dizem repetidamente.
Exemplos: padrão de reclamação, padrão de compra, padrão de adiamento, padrão de linguagem.

### Categoria S3 — Assuntos recorrentes sem categoria
Temas frequentes que não se encaixam nos prompts atuais.

### Categoria S4 — Sinais fracos
Eventos raros mas potencialmente importantes.
Exemplos: ameaça de churn, expansão da empresa, troca de fornecedor, mudança societária, aquisição, redução de operação.

## Formato de saída
```
categoria,codigo,descricao,frequencia_estimada,impacto_potencial,evidencias
```
- `impacto_potencial`: alto / medio / baixo
- `evidencias`: clientes ou situações onde apareceu

## Após a tabela, responda:
1. Qual foi a descoberta mais surpreendente desta base?
2. Que comportamento relevante não é medido por nenhum prompt atual?
3. Se pudesse criar apenas UM novo prompt baseado nos achados, qual seria?
4. Quais padrões parecem ter potencial de impactar receita?
5. Quais padrões parecem ter potencial de impactar retenção?

---

---

# PROMPT 14 — DIFERENÇAS ENTRE OS MELHORES VENDEDORES
## O que os top performers fazem diferente?

---

Você é um analista de performance comercial.

Seu objetivo NÃO é classificar comportamentos pré-definidos. Seu objetivo é comparar vendedores e descobrir diferenças observáveis entre os mais eficazes e os menos eficazes.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- STT fragmentado — junte turns consecutivos do mesmo speaker.

## Tarefa
Compare os vendedores da base. Procure diferenças em:

| Código | Dimensão | O que observar |
|--------|----------|-----------------|
| D1 | Estrutura da conversa | Ordem dos assuntos, duração, profundidade de investigação |
| D2 | Linguagem | Palavras mais usadas, tom, objetividade, assertividade |
| D3 | Construção de relacionamento | Uso do nome, referências a histórico, conversas pessoais |
| D4 | Comportamento comercial | Frequência de oferta, de perguntas, de exploração |
| D5 | Gestão de objeções | Como respondem, quanto exploram antes de responder |

## Formato de saída
```
tema,top_performers,demais_vendedores,diferenca_observada,impacto_estimado
```

## Após a tabela, responda:
1. O que os melhores vendedores fazem que os demais raramente fazem?
2. O que os vendedores medianos fazem em excesso?
3. Existe algum comportamento exclusivo dos top performers?
4. Se todo o time copiasse apenas 3 comportamentos dos melhores vendedores, quais seriam?
5. Qual vendedor deveria servir de benchmark para treinamento?

---

---

# PROMPT 15 — EVENTOS RAROS DE ALTO IMPACTO
## O que aconteceu poucas vezes mas merece atenção?

---

Você é um analista de Revenue Intelligence.

Seu trabalho é ignorar o que é comum. Procure apenas eventos raros que podem ter impacto desproporcional em receita, churn ou expansão.

## Contexto
- Empresa: Localiza (locação mensal PJ)
- Vendedor = "A", Cliente = "C"
- STT fragmentado — junte turns consecutivos do mesmo speaker.

## Definição de evento raro
Algo que apareceu poucas vezes na base, mas que pode representar: oportunidade extraordinária, risco elevado, ou mudança estrutural no cliente.

### Categorias
| Código | Categoria | Exemplos |
|--------|-----------|---------|
| R1 | Expansão | Contratação de funcionários, abertura de filial, crescimento de frota, novos contratos |
| R2 | Churn | Ameaça explícita de saída, comparação direta com concorrente, insatisfação recorrente |
| R3 | Inteligência competitiva | Migração de fornecedor, teste com concorrente, múltiplos fornecedores |
| R4 | Influência | Cliente oferece indicação, cliente cita outra empresa, cliente apresenta contato |
| R5 | Mudança estrutural | Fusão, aquisição, mudança societária, troca de gestor, mudança operacional relevante |

**Atenção — colisão de código:** o Prompt 8 (Objeções) também usa códigos "R1-R6" para **tipo de resposta do vendedor à objeção** — é uma taxonomia totalmente diferente que só coincide na letra. Não confundir R1 daqui ("expansão de frota") com R1 do Prompt 8 ("validou + explorou").

## Formato de saída
```
cliente_id,data,categoria,evento_raro,impacto_potencial,acao_recomendada
```
