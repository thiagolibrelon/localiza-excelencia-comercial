# ligacoes_genai — análise das ligações no motor do NPS

Adapta o motor de tabulação GenAI do NPS-PJ (`Exemplos/GEN_AI_NPS_CXPJ 2.ipynb`)
para rodar os prompts de análise de ligação via `llm-gate` da Localiza / API OpenAI,
na máquina da Localiza (roda o time de CX).

## Duas versões

| Versão | Prompts | Uso |
|---|---|---|
| **básica** | P1, P2, P3, P5, P9 | Reproduz os números da RMR + os problemas. Run diário D-1. |
| **completa** | P1–P15 | Análise profunda (health score por cliente, padrões emergentes, diferenças entre vendedores). Também vai a diário no futuro, provando valor e avaliando custo. |

Um único notebook, `VERSAO = "basica" | "completa"` na primeira célula.

## Arquivos

| Arquivo | O que é | Como é gerado |
|---|---|---|
| `Classificacoes_ligacoes.xlsx` | Taxonomia — 1 aba por prompt (`grupo \| codigo \| rotulo \| descricao \| peso`) | `scripts/gerar_classificacoes_ligacoes.py` (reprodutível) |
| `Exemplos_ligacoes.xlsx` | Few-shot — 1 aba por prompt (`trecho_transcricao \| classificacao \| motivo` + diagnóstico) | painel de 7 agentes, decidido por maioria (`scripts/consolidar_painel_exemplos.py`) |
| `Exemplos_ligacoes_CANDIDATOS.xlsx` | Candidatos minerados das ~9.500 ligações já classificadas em JULHO/ | `scripts/minerar_exemplos_ligacoes.py` |
| `GEN_AI_LIGACOES.ipynb` | O motor adaptado (roda o CX) | `scripts/gerar_notebook_ligacoes.py` (reprodutível) |
| `_panel/` | Intermediários do painel de agentes (candidatos, votos, gabarito) | passo 2/painel |

## Notebook — como rodar (time de CX)

1. `pip install requests pandas openpyxl tqdm`
2. Variável de ambiente `API_KEY` = chave do llm-gate.
3. Abrir `GEN_AI_LIGACOES.ipynb`, ajustar a célula **CONFIG**:
   - `VERSAO = "basica"` (P1/P2/P3/P5/P9) ou `"completa"`
   - `PASTA_ENTRADA` = pasta com os CSVs de ligação (formato 10 colunas)
   - `PASTA_SAIDA`
   - `LIMITE_LIGACOES = 20` para o primeiro teste
4. Rodar as células em ordem. Saída: `P1.csv…P9.csv` + `CONSOLIDADO.csv` + `_resultados.jsonl` (incremental).

- Cada ligação da básica = **4 chamadas** (P1+P2, P3, P5, P9).
- `MODELO_POR_PROMPT = {"P5": "gpt-4o"}` sobe o modelo só de um grupo (se o Challenger vier fraco no mini).
- `completa` só roda os prompts que tiverem aba em `Classificacoes_ligacoes.xlsx` — hoje P1/P2/P3/P5/P9. Para os demais: criar a aba de taxonomia + minerar exemplos + ajustar `SCHEMA` no notebook.

## Fonte de verdade da taxonomia

**`scripts/analisar_gemini_julho.py` + `prompts/prompts_nivel1_por_ligacao.md`** (concordam entre si).

⚠️ **NÃO** usar `apresentacao/DICIONARIO_TECNICO.md` — está dessincronizado da pipeline
real (apesar da auditoria de 10/07/2026). Diferenças achadas em 27/08/2026:

| Item | DICIONARIO_TECNICO.md (errado) | Pipeline real (usado aqui) |
|---|---|---|
| B2 | "Storytelling" | Âncora de preço alto |
| B3 | "Proposta de valor" (peso 1) | Usou histórico do cliente (peso 2) |
| B4 | "Escuta ativa" | Avisou risco ao cliente (peso 2) |
| B7–B9 | Objeção tratada / Pergunta aberta / Confirmação | Batalhar internamente / Ligou proativo / Conhecimento pessoal |
| score máx | 15 | **18** |
| P3 problema P5 | "Sinistro" | Condutor/cadastro |
| P3 problema P9 | "TAG/pedágio" | Sinistro |
| P3 | vai até P11 | vai até **P12** (P12 = manipulação de NPS) |
| FC5 | "Inaplicável" | **Diretivo** |
| Abertura | AB1–AB4 | AB1–**AB5** (AB5 = de proteção) |
| desfecho | "fechou" | fechou_novo / fechou_renovacao / fechou_upsell |

## Validação do `_CANDIDATOS`

1. Abrir `Exemplos_ligacoes_CANDIDATOS.xlsx`.
2. Coluna `usar`: deixar em branco para manter, pôr `x` para descartar.
3. Conferir/corrigir `classificacao_gemini` (é a saída do Gemile, pode ter erro).
4. Escrever `motivo` — a frase que explica por que a classificação se aplica (vai
   no prompt como few-shot).
5. `revisar_nomes = conferir` → sobrou nome próprio no `trecho_transcricao`, trocar por `[NOME]`.
   O scrub automático é agressivo mas não é NER — pode vazar apelido minúsculo ou nome
   após ponto final.
6. Meta: ~5–10 exemplos validados por código.
