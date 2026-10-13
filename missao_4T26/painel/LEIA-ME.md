# Painel de carga operacional · MVP em HTML (SharePoint + .bat)

Versão 1.0 · 13/10/2026 · responsável: Thiago Librelon (Excelência Comercial, venda interna DVINT)

O painel tem as mesmas 8 páginas do modelo aprovado para o BI (`missao_4T26/bi/mockups/`). Ele roda no navegador e
calcula tudo de acordo com os filtros de período, distrital e carteira. Não é preciso Power BI, servidor nem instalar
nada no computador de quem lê. Antes de investir no BI, o MVP serve para medir se a Gerência Operacional abre o painel
todos os dias.

```
 computador do Thiago                         pasta no SharePoint (sincronizada pelo OneDrive)
 ─────────────────────                        ─────────────────────────────────────────────────
 CSVs exportados da consulta                  Gestao/
        │                                       ├─ painel.html          ← as 8 páginas
        ▼                                       ├─ dados.js             ← números do dia (agregados)
 Atualizar painel.bat ──► atualizar_painel.py ──►├─ Abrir painel.bat     ← quem lê dá dois cliques aqui
                                                └─ logs/<usuario>.csv   ← um registro por abertura
```

## As peças

| Arquivo | Onde fica | Para quê |
|---|---|---|
| `painel.html` | pasta `Gestao` no SharePoint | O painel. Lê o `dados.js` da mesma pasta. |
| `dados.js` | pasta `Gestao` (gerado todo dia) | Só números agregados por dia e carteira, cerca de 0,5 MB por mês de dados. Não tem nome de vendedor, texto de ligação nem código de cliente. |
| `Abrir painel.bat` | pasta `Gestao` | Grava uma linha em `logs\<usuario>.csv` e abre o painel no navegador padrão. |
| `logs/` | pasta `Gestao` | Um arquivo por pessoa, para evitar conflito de sincronização. O painel mostra só contagens. |
| `atualizar_painel.py` e `Atualizar painel.bat` | **só no computador do Thiago** | Leem o CSV, gravam o `dados.js` e copiam para a pasta `Gestao` a versão mais nova do `painel.html` e do `Abrir painel.bat`. |

**Por que não um localhost?** Um servidor local esbarraria em porta bloqueada, antivírus e firewall, e precisaria ficar
ligado. Além disso, o CSV bruto ficaria acessível. Aqui o navegador abre um arquivo local (`file://`) e carrega
`dados.js` com uma tag `<script>`, que funciona sem servidor no Chrome e no Edge. Os dados brutos ficam com o Thiago e
só o agregado vai para a pasta compartilhada.

## Montagem (uma vez)

### 1. Pasta e permissões no SharePoint
1. Num site ou biblioteca da equipe, crie a pasta `Painel Carga Operacional` e, dentro dela, a pasta `Gestao`.
2. Permissões. No SharePoint, abra a pasta → **⋯ → Gerenciar acesso**:
   - `Gestao`: **Pode exibir** para a Gerência Operacional e **Pode editar** para o Thiago.
   - `Gestao/logs` (crie a pasta vazia): **Pode editar** para as mesmas pessoas da gerência. Sem isso o `.bat` abre o
     painel, mas não consegue registrar o acesso.
3. A permissão da pasta é o controle de acesso do painel: quem vê a pasta vê todas as carteiras (por código).

### 2. Computador do Thiago (quem atualiza)
1. Instale o Python 3.9 ou mais novo (python.org, marcando **Add python.exe to PATH**). Depois, no Prompt de Comando:
   `pip install pandas`.
2. Copie `atualizar_painel.py`, `Atualizar painel.bat`, `painel.html` e `Abrir painel.bat` desta pasta do repositório
   para uma pasta local, por exemplo `Documentos\painel_dvint\`. Essa pasta **não** é a pasta compartilhada.
3. Sincronize a pasta `Gestao` (passo 3) e dê dois cliques em `Atualizar painel.bat`. Na primeira vez:
   - abre uma janela para escolher o CSV. Se você **cancelar**, ela pede uma **pasta** de CSVs;
   - depois, outra janela para escolher a pasta `Gestao` sincronizada.

   O script grava o `dados.js`, copia `painel.html` e `Abrir painel.bat` para a pasta e guarda as escolhas para os
   próximos dias.

### 3. Computador de cada leitor (Gerência Operacional)
1. Abra a pasta `Painel Carga Operacional` no navegador → **Sincronizar** (ou **Adicionar atalho a Meus arquivos**).
2. No Explorador de Arquivos, clique com o botão direito na pasta `Gestao` → **Sempre manter neste dispositivo**. Sem isso
   o `dados.js` pode ficar só na nuvem e o painel não o encontra.
3. Botão direito em `Abrir painel.bat` → **Enviar para → Área de trabalho (criar atalho)**. Renomeie o atalho para
   "Painel DVINT".
4. Navegador: Chrome ou Edge atualizados. O painel se ajusta a telas menores; em tela cheia (F11) fica melhor.

## Rotina diária (Thiago, cerca de 2 minutos)

1. **Exporte o CSV da consulta** no mesmo formato do arquivo de setembro: as 88 colunas da consulta do Power BI/Excel,
   separador `;`. Guarde **todos** os CSVs na mesma pasta (por exemplo `Documentos\painel_dvint\csv\`), com o de setembro
   como base e um arquivo por dia (`2026-10-13.csv` e assim por diante). O script lê a pasta inteira e junta as linhas.
   Se a mesma ligação (`id_transcricao`) aparecer em dois arquivos, vale a do arquivo mais novo.
   - Por que manter o histórico: reincidência (K5), clientes sem 2ª tentativa, retornos no prazo e o número da
     tentativa dependem dos dias anteriores. Com só o CSV de ontem, esses números ficam errados.
   - Um único CSV acumulado também serve. Nesse caso, escolha o arquivo em vez da pasta.
2. Dois cliques em **Atualizar painel.bat** e confirme a pasta. Confira o resumo que aparece na tela:
   - as datas: dados até, duração até e classificação GPT até;
   - o K1 do arquivo;
   - os avisos **ATENÇÃO**, que aparecem quando a duração ou a classificação do último dia não chegaram.
3. O OneDrive envia o `dados.js` em segundos. Quem abrir o painel (ou apertar F5) vê o dia novo. A data e a hora da
   atualização aparecem no rodapé e na página 8.

Por linha de comando (para agendar no Agendador de Tarefas, por exemplo):
`python atualizar_painel.py --entrada "C:\...\csv" --saida "C:\...\Painel Carga Operacional\Gestao"`

## Como usar o painel

- **Páginas** (botões à esquerda, ou teclas 1 a 8):

  | Página | Pergunta | O que mostra |
  |---|---|---|
  | 1 · Dia | O que mudou ontem? | Cartões K1, Gemini, K7, pendências e horas; 4 alertas; carteiras do dia |
  | 2 · Semana | A tendência piora ou melhora? | Semana fechada, matriz das 8 últimas semanas e roteiro da reunião de segunda |
  | 3 · Período | Estamos no caminho da meta? | Medidor, composição do tempo e simulador de P1 |
  | 4 · Problemas | Onde o tempo se perde? | Pareto, resolução por código, origem e carteiras |
  | 5 · Carteiras | Quais carteiras concentram a carga? | Ranking com mediana, distritais, concentração de clientes e mínimo de ligações |
  | 6 · Tempo e ritmo | Que duração e que cadência rendem mais? | Fechamento por duração, funil, horário, 2ª tentativa e retornos |
  | 7 · Competências | Onde treinar? | Challenger, SPIN, carteira contra a mediana e as 6 carteiras com mais oportunidade |
  | 8 · Qualidade do dado | Posso confiar nos números de hoje? | Cobertura, verificações da carga, valores-sentinela e uso do painel |

- **Período**:
  - O padrão é **Mês do último dado**. Também há Tudo, Últimos 30 dias, Últimos 7 dias e Personalizado.
  - Mexer nas datas muda o período para Personalizado.
  - Se o período não tiver ligações com duração, as páginas 1 a 3 oferecem um botão para ir ao último mês com duração.
- **Distrital e carteira**:
  - Clicar numa carteira em qualquer tabela ou no ranking da página 5 aplica o filtro. Um segundo clique tira o filtro.
  - Os rankings de carteira continuam mostrando todas as carteiras e destacam a escolhida.
- **Limpar filtros** volta ao padrão.
- Cada computador lembra a última página e os filtros.
- **Cores:** paleta oficial do LDS (Localiza Design System), a mesma de `Color_Code.md` na raiz do repositório, e fonte
  Inter embutida no arquivo, para abrir igual em qualquer computador, mesmo sem internet.

  | Cor | Significado |
  |---|---|
  | Verde `#018444` e verde-limão `#78DE1F` | Negociação, o que melhorou, resolvido |
  | Vermelho `#D92020` | Carga operacional, problema, o que piorou |
  | Cinza | Referências: baseline, Gemini, mediana |
  | Verde-noite `#003418` | Menu lateral |

## Validação antes de divulgar

Na página 3, escolha **Personalizado de 01/09/2026 a 22/09/2026** e confira:

| Onde | Valor esperado |
|---|---|
| Página 3: K1 do período · horas classificadas · horas operacionais · K3 | 43,2% · 265,9 h · 114,8 h · 36,9 h |
| Página 3: composição do tempo | negociação 35,1% · relacionamento 20,6% · operacional sem problema 13,1% · com problema 30,0% |
| Página 4: K6 · K2 · K4 · K5 | 19,1% · 698 · 10,3% · 18,8% |
| Página 4: Pareto | P1 + P2 + P13 = 67,5% do tempo em problema (o rótulo arredonda para 68%) |
| Página 5 (mínimo 40) | 48 carteiras elegíveis · mediana 39,4% |
| Página 8: C1 · C2 | 89,5% · 100,0% |
| Página 3 com a carteira S1I05A | K1 46,8% · K7 34,7% |

Esta versão foi conferida automaticamente contra `missao_4T26/bi/reconciliacao.csv`: **135 de 135 valores batem**. A
planilha tem 151 itens; os outros 16 não aparecem no painel. São a classe legada (M06–M08), contagens de clientes e o
"Meu painel" do vendedor (página 9, segunda fase).

## Registro de acesso

- **O que é gravado:** a cada abertura pelo `Abrir painel.bat`, uma linha com data, hora, usuário do Windows e nome do
  computador, em `logs\<usuario>.csv`. Abrir o `painel.html` direto não gera registro.
- **O que o painel mostra:** na página 8, só contagens: pessoas e acessos nos últimos 7 dias e pessoas desde o início.
  As contagens entram no painel na atualização seguinte.
- **Transparência:** avise as pessoas. Sugestão de texto: *"O atalho do painel registra data, hora e usuário de cada
  abertura, só para medirmos o uso do MVP antes de decidir pelo Power BI."*
- **Critério sugerido para decidir o BI:** depois de 4 semanas, ver quantos gerentes abrem o painel 3 ou mais vezes
  por semana e quantas decisões da reunião de segunda saíram dele.

## Problemas comuns

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| "Não encontrei os dados do painel" | `dados.js` só na nuvem ou ainda sincronizando | Botão direito na pasta `Gestao` → **Sempre manter neste dispositivo**; espere o ícone verde. |
| Números de dias atrás | OneDrive pausado ou sem sincronizar | Veja a data no rodapé. Retome a sincronização no ícone da nuvem, perto do relógio. |
| O `.bat` mostra "Não encontrei o painel.html" | O `.bat` foi copiado para fora da pasta | Use um **atalho** para o `.bat` em vez de uma cópia, ou edite a linha `set "PASTA=..."` no início do arquivo. |
| O acesso não aparece na página 8 | O leitor não tem permissão de edição em `logs`, ou a atualização ainda não rodou | Ajuste a permissão de `Gestao/logs`. A contagem entra na próxima atualização. |
| A empresa bloqueia `.bat` no SharePoint | Política de TI | Deixe o `Abrir painel.bat` na área de trabalho de cada leitor, com a linha `set "PASTA=..."` apontando para a pasta sincronizada. |
| Página 1 vazia ("Sem ligações com duração") | O período escolhido não tem duração | Clique no botão que leva ao último mês com duração. A página 8 mostra até quando há duração. |
| Erro "O CSV não tem as colunas esperadas" ao atualizar | O CSV não veio da consulta completa | Exporte da mesma consulta do arquivo de setembro (88 colunas). |
| "python não é reconhecido" | Python fora do PATH | Reinstale marcando **Add python.exe to PATH**, ou use `py -3`; o `.bat` já tenta os dois. |

## Limites do MVP (de propósito)

- **Sem segurança por linha:** quem acessa a pasta vê todas as carteiras, identificadas por código. Os vendedores ficam
  para a segunda fase. Uma opção é uma pasta por vendedor com o próprio `dados.js`, filtrado pela carteira dele.
- **Baseline provisório:**
  - K1 43,2%, meta 38,2%, piloto 33,2%.
  - Setembro mistura versões do GPT, e a duração só existe até 22/09.
  - Os valores ficam em `CONFIG_PAINEL`, no início do `atualizar_painel.py`. Quando o baseline for congelado, mude-os
    ali e rode a atualização.
- **Fora do painel:**
  - o trecho para coaching, porque o texto livre pode ter nome e telefone de contato do cliente (LGPD);
  - a página 9 "Meu painel", que fica para a fase dos vendedores.
- **Regras de negócio:** as mesmas do plano da missão e de `missao_4T26/bi/`. A carga operacional (K1) conta problema,
  suporte, cobrança, pós-venda e dúvida de contrato, sobre a base classificada pelo GPT com duração; o fuso é −3 h.
