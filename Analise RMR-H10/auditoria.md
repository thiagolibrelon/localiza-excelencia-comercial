# Auditoria — dados e árvore de decisão H10

Data: 13/07/2026. Escopo: integridade do CSV consolidado, robustez estatística da árvore, e avaliação de enriquecimento sob a ótica de um diretor que quer resultados melhores em venda interna (upsell/cross-sell na base existente).

---

## 1. Integridade estrutural — OK

- `dados_arvore_H10.csv` tem exatamente 6.623 linhas, mesmo total do `CONSOLIDADO_LIGACOES.csv`. Nenhum `segment_id` duplicado. Nenhuma linha com a mesma chave (base+cliente+data+duração) repetida.
- A partição em 8 ramos soma exatamente 6.623 — mutuamente exclusiva e exaustiva, sem overlap nem buraco.
- Reprodutível: `scripts/gerar_arvore_h10.py` recalcula tudo do zero a partir do CSV bruto.

## 2. Robustez estatística — 2 achados que corrigem o que já foi apresentado

Testei significância (teste de proporção, z-score + p-valor) nas comparações centrais:

| Comparação | Taxas | p-valor | Conclusão |
|---|---|---|---|
| Ramo 6 (upsell+Challenger alto) vs Ramo 5 (nada) | 19,7% vs 3,1% | **1,0×10⁻³²** | Sólido — praticamente impossível ser acaso |
| Ramo 6 vs Ramo 1 (só Challenger alto) | 19,7% vs 9,1% | **1,6×10⁻⁶** | Sólido — upsell soma valor real além do Challenger |
| Ramo 6 vs Ramo 7 (upsell sem Challenger bom) | 19,7% vs 15,1% | 0,37 | **NÃO significativo** — n=73 é pequeno demais pra afirmar que a qualidade do Challenger ainda importa quando já tem upsell |
| FC1 (fecha c/ data) vs FC3 dentro do Ramo 6 | 21,5% vs 15,9% | 0,34 | **NÃO significativo** — a mesma ressalva vale aqui |

**Correção necessária:** o `arvore_decisao_H10.md` original afirma "fechar com data ainda soma mais uma vez dentro da melhor célula" como se fosse achado confirmado. Não é — com n=130 vs n=69, a diferença de 5,6pp pode ser ruído. Vou reclassificar esse item de "achado" pra "sinal a validar com mais dados" no arquivo da árvore.

**O que continua sólido, sem ressalva:** a combinação upsell+Challenger de qualidade (ramo 6) bate qualquer outro ramo com folga estatística enorme. Isso é o núcleo de H10 e está intacto.

Intervalos de confiança (Wilson, 95%) de cada ramo, pra referência:

| Ramo | n | Taxa | IC 95% |
|---|---:|---:|---|
| 1 — Challenger alto, sem upsell | 1.289 | 9,1% | 7,6%–10,8% |
| 2 — Challenger médio | 487 | 5,1% | 3,5%–7,5% |
| 3 — Challenger baixo | 1.163 | 1,5% | 1,0%–2,4% |
| 4 — sem Challenger, com OP6 | 303 | 8,3% | 5,7%–11,9% |
| 5 — sem Challenger, sem OP6 | 3.051 | 3,1% | 2,6%–3,8% |
| 6 — upsell + Challenger alto | 228 | 19,7% | 15,1%–25,4% |
| 7 — upsell, Challenger fraco | 73 | 15,1% | 8,6%–25,0% |

## 3. Bugs de qualidade de dado encontrados (não invalidam a árvore, mas precisam de nota)

### 3a. `p5_teve_challenger` está corrompido em ~81 linhas
Esse campo deveria ser binário (SIM/NAO), mas tem valores como `CH1`, `CH5`, `CH6`, `CH7` — o código do Challenger vazou pra dentro do campo binário em algum ponto da extração/consolidação. Não afeta a árvore (que usa só `p5_qualidade`), mas quem usar `p5_teve_challenger` direto vai contar errado.

### 3b. `p5_teve_challenger` e `p5_qualidade` se contradizem em ~1.299 linhas (19,6% da base)
1.299 ligações têm `teve_challenger=NAO` mas `qualidade` diferente de "nenhum" (1.161 com qualidade=baixa, 133 média, 5 até "alta"). Ou seja, quase toda a categoria "Challenger baixa" (1.161 de 1.170 = 99,2%) está marcada como "não teve Challenger" no campo binário. Isso sugere que os dois campos foram avaliados com critérios diferentes (um mais rígido, um mais permissivo) — não são intercambiáveis. A árvore usa só `qualidade`, então fica consistente internamente, mas é um sinal de que o Prompt P5 merece uma revisão de critério antes da próxima rodada.

### 3c. `p9_desfecho` é essencialmente inutilizável sem normalização
Encontrei 15+ valores distintos pra um campo que deveria ser uma categoria fechada: `POSITIVO`, `NEGATIVO`, `Resolvido`/`RESOLVIDO` (case diferente), `Sucesso`, `Insucesso`, `SEM_DEMANDA`/`Sem demanda`, `NEGOCIO_FECHADO`, `AGENDAMENTO`/`Agendamento`, `NEGOCIACAO`, `ENCERRADO`, `Aberto`... Diferentes batches usaram vocabulários diferentes. Não usei esse campo na árvore (usei `p1_desfecho`, que é limpo), mas fica registrado — se algum dia quiserem usar `p9_desfecho`, precisa de um dicionário de normalização antes.

### 3d. `p6_valor_potencial_reais` não é numérico limpo
Mistura `"nenhum"`, `"0"`, valores puros (`"200"`), e formatos com sufixo (`"50/v"`, `"protecao=80/v"`, `"3600/v"`). Confirma o que já estava sinalizado em auditorias anteriores ("revalidar origem") — não dá pra somar R$ direto sem parsear esses formatos primeiro.

### 3e. `sentimento` e `p9_usou_nome` têm variância quase nula
`sentimento` é POSITIVE em 97,9% dos casos (6.485/6.623) — não discrimina nada, não vale a pena usar como variável. Mesmo padrão em menor grau pra `p9_usou_nome` (88,5% SIM).

---

## 4. Enriquecimento — o que a árvore ganhou ao cruzar com dados que já estavam disponíveis (sem prompt novo)

### Duração da ligação — achado operacional importante
| Ramo | Duração média |
|---|---:|
| 6 — upsell + Challenger alto (o vencedor) | **661s (~11 min)** |
| 1 — só Challenger alto | 494s |
| 2 — Challenger médio | 304s |
| 7 — upsell sem Challenger bom | 370s |
| 4 — sem Challenger, com OP6 | 213s |
| 5 — não fez nada | **168s (~2,8 min)** |
| 3 — Challenger malfeito | 144s |

**Leitura pro diretor:** o combo vencedor não é grátis — leva **4x mais tempo de ligação** que o "padrão do time" hoje. Se a meta é rodar esse playbook em escala, isso tem implicação de capacidade: ou aumenta o tempo médio de ligação do time, ou o playbook precisa ser reservado pras contas de maior potencial (ver seção 5, recomendação P4).

### Tipo de ligação — o achado mais relevante pra "venda interna"
Cruzei o ramo com `p2_tipo`, separando ligações de **base existente** (upsell/renovação/retenção) vs **venda nova**:

| Ramo | % da ligação é upsell/renovação/retenção (base existente) |
|---|---:|
| 6 — vencedor | **23%** |
| 7 — upsell sem Challenger bom | 27% |
| 2 — Challenger médio | 19% |
| 1 — Challenger alto | 15% |
| 3 — Challenger baixo | 14% |
| 4 — com OP6 | 16% |
| 5 — nada | 9% |

**Isso é uma boa notícia direta pro objetivo do diretor:** o combo vencedor já acontece desproporcionalmente mais em ligações de base existente do que o resto da árvore. H10 não é só um achado de "fechamento em geral" — é, por natureza, mais forte exatamente no cenário que interessa (vender mais pra quem já é cliente).

### O que não ajudou
`p10_risco_max` (risco das promessas) não varia por ramo — todos os ramos ficam entre 91% e 96% "baixo risco". Não é uma variável que discrimina o comportamento vencedor, não vale a pena aprofundar aqui.

---

## 5. O que falta pra ter uma resposta completa pro diretor — avaliado como prioridade de negócio

O diretor quer "resultados melhores na venda interna". A árvore hoje responde **o quê** funciona (upsell + Challenger bem executado, com força estatística sólida) e mostrou que **já pende naturalmente pra venda interna**. Falta responder **quem** já faz isso bem e **em quem** aplicar primeiro.

### 🔴 Gap crítico — não existe identificação de vendedor em nenhum lugar do pipeline
Chequei o CSV consolidado inteiro e o JSON bruto de origem (`dados/cliente_*.json`) — não existe campo de vendedor/executivo em nenhum dos dois. A única forma de saber "quem" é o cruzamento por **carteira** (via `Cod` do cliente batendo com a base de diárias), que já existe como script (`scripts/cruzar_ligacoes_diarias.py` + `carteiras_comportamento.py`) — mas **só foi rodado pra base antiga (1.275 clientes, 19% da base total)**. Os outros 81% (novo lote, 5.348 clientes) nunca foram cruzados.

**Sem isso, a única resposta possível pra "quem treinar" é "ninguém sabe".** Esse é o item de maior prioridade — não é nem um prompt novo, é re-rodar um script existente apontando pro novo lote. Baixo custo, alto retorno.

### 🟡 P7 (cross-sell/upsell, PR1-PR12) — já em standby, continua sendo o 2º mais relevante
Confirma se os 301 casos de B5=SIM são upsell de produto real (Telemetria, Proteção Total etc.) e traz `receita_incremental_potencial` por ligação. Isso transforma "19,7% de taxa de fechamento" em "R$ X/mês se replicarmos isso". Sem P7, a árvore prova o padrão comportamental mas não converte em R$ — que é exatamente o que a diretoria financeira vai perguntar.

### 🟡 P4 (health score / valor potencial do cliente) — só amostrado hoje (152/363)
Prioriza **em quem** aplicar o playbook primeiro. Dado que o combo vencedor custa 4x mais tempo por ligação (achado da seção 4), faz sentido mirar primeiro nas contas de maior valor/potencial, não em todo mundo. Sem P4 em escala, não dá pra responder "quais 20% das contas merecem esse investimento de tempo".

### 🟢 P14 (diferenças entre vendedores) — só amostrado (152/363), e depende do gap crítico acima
Mostraria benchmarks reais entre quem já executa bem vs mal. Só fica acionável (por vendedor, não por carteira agregada) depois que o cruzamento carteira×base-nova for refeito.

### Ordem de prioridade recomendada
1. **Re-rodar `cruzar_ligacoes_diarias.py`/`carteiras_comportamento.py` pro novo lote** (script já existe, sem custo de LLM) — desbloqueia "quem".
2. **P7** (em standby, ~US$210-290, 175 lotes) — desbloqueia "que produto" e "quanto R$".
3. **P4 em escala** — desbloqueia "em quem aplicar primeiro", dado o custo de tempo por ligação.
4. **P14 em escala** — benchmarks por vendedor, só depois do item 1.

---

## Arquivos desta pasta

- `arvore_decisao_H10.md` — a árvore (atualizada com as ressalvas estatísticas desta auditoria).
- `dados_arvore_H10.csv` — dados anotados por ramo.
- `exemplos_por_ramo.md` — exemplos reais com transcrição completa.
- `auditoria.md` — este arquivo.
