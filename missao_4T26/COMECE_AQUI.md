# Missão 4T26 — como abrir todo o material

> Branch com o material: **`claude/sleepy-brown-rob4v5`** (ainda não foi para a branch principal).
> O material **não contém o CSV bruto** de setembro: só agregados, códigos de carteira, metadados das colunas e trechos de ligação mascarados.

## 1. Como trazer para este PC

**Opção A: clonar.**

```bash
git clone https://github.com/thiagolibrelon/localiza-excelencia-comercial.git
cd localiza-excelencia-comercial
git checkout claude/sleepy-brown-rob4v5
```

Se o repositório for privado, o Git pede login do GitHub (ou use o GitHub Desktop / `gh auth login`). Se a pasta `missao_4T26` não aparecer, o `checkout` não foi feito: ela só existe nessa branch.
Para pegar atualizações depois: `git pull`.

**Opção B: sem Git.** No GitHub, abra a branch `claude/sleepy-brown-rob4v5` → botão verde *Code* → *Download ZIP*. Ou use o `missao_4T26_material.zip` enviado na conversa (mesmo conteúdo, só a missão e os 4 scripts).

## 2. Ordem de leitura

> **Novo (13/10): painel MVP em HTML no lugar do Power BI.** Comece por `painel/LEIA-ME.md`. Para ver o painel neste PC, rode
> `python missao_4T26/painel/atualizar_painel.py --entrada "C:\caminho\Consulta Power Bi - Cópia.csv" --saida missao_4T26/painel` (na raiz do repositório)
> e abra `missao_4T26/painel/painel.html` no Chrome ou Edge.

| # | Abrir | Com o quê | Para quê |
|---|---|---|---|
| 0 | `painel/LEIA-ME.md` | VS Code / GitHub | **Painel MVP (decisão de 13/10):** HTML com as 8 páginas, pasta no SharePoint, `.bat` com registro de acesso, rotina diária |
| 1 | `PLANO_MISSAO_4T26.md` | VS Code (Ctrl+Shift+V para visualizar) ou GitHub | O plano: canvas, baseline, KPIs, cronograma até dezembro, riscos |
| 2 | `AUDITORIA_DADOS_E_OPORTUNIDADES.md` | idem | Mapa das 88 colunas (**seção 2.1 lista cada coluna e seu uso**), 10 achados no código M, 4 personas, 89 oportunidades |
| 3 | `PLANO_OPORTUNIDADES.md` | idem | Os 12 pacotes de oportunidade, capacidade e calendário |
| 4 | `prototipos/bi_wireframe.html` | Navegador (duplo clique) | Wireframe interativo das 8 páginas do BI |
| 5 | `prototipos/trilha_prototipo.html` | Navegador | Protótipo da trilha do vendedor (12 lições) |
| 6 | `bi/README_BI_v1.md` | VS Code / GitHub | **Roteiro do BI v1:** o que é, cronograma 01–07/10, montagem passo a passo, riscos |
| 7 | `bi/mockups/BI_v1_mockups.pdf` (ou `bi_mockups.html`) | Leitor de PDF / navegador | As 9 páginas do BI como vão ficar. O `_anotado.pdf` mostra o ID e as medidas de cada visual |
| 8 | `bi/especificacao_visuais.md`, `bi/modelo.md` | VS Code / GitHub | Cada visual (campos, medidas, filtros) e o modelo de dados |
| 9 | `bi/powerquery/*.m`, `bi/dax/*.dax`, `bi/tema/*.json` | Bloco de notas / VS Code | O código para colar no Power BI Desktop (ver README, seção 5) |
| 10 | `bi/reconciliacao.csv` | Excel (separador `;`) | 151 valores esperados para conferir o BI depois de montado |
| 11 | `bi/post_lancamento.md` | VS Code / GitHub | Texto do comunicado de lançamento (rascunho) |
| 12 | `anexos/*.csv` | Excel (UTF-8; se os acentos saírem errados, *Dados → De texto/CSV* e escolha UTF-8) | Dicionário das 88 colunas, série diária, carteiras, tempo ótimo, catálogo de oportunidades |

## 3. Rodar os scripts (opcional)

Python 3.9+ e `pip install pandas numpy`. Os scripts ficam em `scripts/` e recalculam os números a partir do **CSV da consulta** (que não está no repositório; passe o caminho dele).

```bash
python scripts/auditoria_dados_missao.py "C:\caminho\Consulta Power Bi - Cópia.csv"      # refaz o dicionário e os anexos
python scripts/baseline_carga_operacional.py "C:\caminho\Consulta Power Bi - Cópia.csv"  # baseline do K1
python scripts/reconciliar_bi_v1.py "C:\caminho\Consulta Power Bi - Cópia.csv"           # refaz bi/reconciliacao.csv
```

## 4. O que dá e o que não dá para validar neste PC

| Dá | Não dá |
|---|---|
| **Gerar e abrir o painel MVP** (`painel/`) com o CSV e conferir os números da seção "Validação" do LEIA-ME | Testar a sincronização do SharePoint e o registro de acesso: dependem da pasta da empresa |
| Ler tudo, abrir os HTML e PDF, conferir o mapa de colunas | Rodar o Power Query: ele lê o BigQuery pelo DSN `lclz-dados` (ODBC), que só existe no ambiente oficial |
| Rodar os scripts contra o CSV e comparar com `reconciliacao.csv` | Validar o DAX: precisa do modelo carregado no Power BI Desktop (só roda em Windows) |
| Conferir se o M e o DAX fazem sentido lendo os arquivos | Testar o RLS e a publicação: dependem do workspace da empresa |

**O M e o DAX não foram executados em nenhum Power BI** (foram escritos e verificados só por leitura e por scripts). A validação de verdade é a reconciliação do `bi/README_BI_v1.md`, seção 7, no ambiente oficial.

## 5. Antes de levar para o ambiente oficial

- Nada aqui é dado bruto, mas há **códigos de carteira** (identificam o vendedor para quem é do time) nos mockups, em `anexos/carteira_set_2026.csv` e em `bi/reconciliacao.csv`, e **trechos de ligação mascarados** em `prototipos/trilha_prototipo.html`.
- Decisões que ainda dependem de você (README do BI, seção 6): audiência do BI na quarta, RLS, texto livre fora do modelo.
- O BI v1 é **retrato de setembro com baseline provisório**; os avisos estão nos mockups e no comunicado.
- **Painel MVP:** o `dados.js` gerado tem números por carteira (código) e não deve ir para o repositório (o `.gitignore` da pasta já o exclui). Leve para a pasta do SharePoint só `painel.html` e `Abrir painel.bat`; o script e o `Atualizar painel.bat` ficam no seu computador.

## 6. Mapa de pastas

```
missao_4T26/
  COMECE_AQUI.md                        este arquivo
  PLANO_MISSAO_4T26.md                  plano da missão (v0.3.3)
  AUDITORIA_DADOS_E_OPORTUNIDADES.md    auditoria dos dados e catálogo de oportunidades
  PLANO_OPORTUNIDADES.md                plano separado das oportunidades
  anexos/                               CSVs de apoio (dicionário, série diária, carteiras, tempo ótimo, catálogo)
  prototipos/                           wireframe do BI e protótipo da trilha (HTML)
  painel/                               MVP em HTML (decisão de 13/10): LEIA-ME, painel.html, atualizar_painel.py, .bat de abrir e de atualizar
  bi/
    README_BI_v1.md                     roteiro do BI v1
    powerquery/  dax/  tema/            código do modelo
    mockups/                            9 páginas em PNG, PDF e HTML
    especificacao_visuais.md  modelo.md  reconciliacao.csv  post_lancamento.md
scripts/                                scripts que recalculam os números a partir do CSV
```
