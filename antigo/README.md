# antigo/ — conteúdo desatualizado/substituído

Criada em 22/07/2026 na limpeza geral do projeto. Cada item abaixo tem uma razão específica pra estar aqui — não é "lixo", é histórico com evidência de que foi substituído.

| Item | Por que está aqui |
|---|---|
| `analises_amostra_inicial/` | Análises da amostra inicial (14-87 clientes) — substituídas pelas análises na base completa (6.623/6.813 ligações). Nenhum script referencia esta pasta. |
| `prompts_amostra_inicial/` | Prompt usado só na exploração via GPT da amostra inicial, superado pelos prompts atuais em `prompts/`. |
| `resultados_gemini_truncado/` | Primeiro run Gemini (24-25/06) — todos os batches vieram truncados por um bug de thinking tokens (já corrigido). Inutilizável, confirmado por nenhuma referência em nenhum script (`resultados/gemini_v2/` é o run correto da mesma base e SEGUE ativo, não mexi nele). |
| `dashboard_v1.html` | Primeira versão do dashboard executivo. `apresentacao/dashboardv2.html` é a versão atual e ativa. Zero scripts referenciam a v1. |
| `analise_rmr_h10_brutos/` | Exports brutos (`arq1`, `arq2`, `arq3`, `arq5`) usados uma vez pra construir `Analise RMR-H10/arvore_decisao_H10.md` e `dados_arvore_H10.csv` — já consumidos, nenhum script os lê mais (o índice de transcrições atual usa `resultados/exploracao_fable/inputs_completo/`, não estes arquivos). Mantidos fora do git (mesma lógica de PII de `dados/`). |

## O que NÃO foi movido (verificado como ainda ativo)

- `resultados/gemini_v2/` — ainda lido por `consolidar_ligacoes.py`, `cruzar_reservas*.py`, `cruzamento_hipoteses.py`, `gerar_status_prompts.py`.
- `dados/LIG`, `dados/cliente_*.json`, `dados/recebidos/*` — schema de origem referenciado em múltiplos scripts ativos.
- `resultados/gemini_novo_lote/` — pipeline ativo (100% completo, mas ainda é a fonte do CSV consolidado).

## O que ficou ambíguo (não mexi, avaliar depois)

- `Color_Code.md` (raiz) — design tokens de um tema Figma Make, sem relação aparente com a análise de ligações. Pode ser de outro projeto/uso externo (ex: construção de UI do Aletheia como produto). Não movido por falta de certeza.
- `Prompt_plano` (raiz, sem extensão) — prompt-mestre pra construir o Aletheia como produto SaaS (arquitetura, UX, IA). Pode estar em uso ativo fora deste repositório (Figma Make/Claude). Não movido pela mesma razão.
