# Testes do painel (para quem mexe no código)

Precisam de Node.js com Playwright e de uma pasta de teste com o painel gerado
(`python atualizar_painel.py --entrada <csv> --saida <pasta>`).

| Teste | O que confere | Como rodar |
|---|---|---|
| `numeros.js` | Os indicadores calculados no navegador são iguais aos recalculados com pandas (`esperado.py`) em três recortes: setembro inteiro, carteira S1I05A em 01–22/09 e distrital DTIN4 | `python testes/esperado.py <csv> > esperado.json` e depois `node testes/numeros.js <pasta> esperado.json` |
| `telas.js` | Abre as 9 páginas, procura erro de console, texto cortado e cartão estourado, e salva uma imagem de cada página | `node testes/telas.js <pasta> <pasta-imagens> 1440 900` |
| `configuracoes.js` | Baseline pessoal (aplicar, voltar à oficial, clique num mês), parâmetros e o `painel_config.json` baixado | `node testes/configuracoes.js <pasta> <pasta-imagens>` |
| `interacoes.js` | Clique que filtra (distrital, código, carteira), cartões que navegam, granularidade, comparação, tabelas (busca, ordenação, "mostrar mais"), CSV/PNG, simulador e estado salvo | `node testes/interacoes.js <pasta> <pasta-imagens>` |

Na versão 2.0, com o CSV de setembro: 69 de 69 indicadores iguais, nenhum erro de console nas 10 páginas em 1366, 1440 e 1920 px.
Para usar outro Chromium, defina a variável `CHROMIUM` com o caminho do executável.
