# Painel DVINT · venda interna (HTML + SharePoint + .bat)

Versão 2.1 · 13/10/2026 · responsável: Thiago Librelon (Excelência Comercial, venda interna DVINT)

O painel mostra para a Gerência Operacional como o time trabalha. São 9 seções de análise: visão geral, tempo,
vendas, problemas, Challenger e SPIN, clientes, contato e cadência, carteiras e qualidade do dado. Há também uma seção
de configurações, onde se escolhe a baseline.

- **Como funciona:** é um site que abre no navegador a partir de uma pasta do SharePoint. Os gráficos são interativos:
  - mostram o valor ao passar o mouse;
  - um clique filtra o painel;
  - têm tabela equivalente e baixam em CSV ou PNG.
- **Filtros:** valem para todas as páginas. São período, comparação (baseline ou período anterior), granularidade (dia,
  semana ou mês), distrital e carteira.
- **O que não precisa:** Power BI, servidor ou instalar nada no computador de quem lê.
- **Definições:** as mesmas do memo da RMR. Setembro/2026 é o baseline.

```
 computador do Thiago                         pasta no SharePoint (sincronizada pelo OneDrive)
 ─────────────────────                        ─────────────────────────────────────────────────
 CSVs exportados da consulta                  Gestao/
        │                                       ├─ painel.html, app.js  ← o site
        ▼                                       ├─ vendor/              ← biblioteca de gráficos (ECharts)
 Atualizar painel.bat ──► atualizar_painel.py ──►├─ dados.js             ← números do dia
                                                ├─ Abrir painel.bat     ← quem lê dá dois cliques aqui
                                                └─ logs/<usuario>.csv   ← um registro por abertura
```

## As peças

| Arquivo | Onde fica | Para quê |
|---|---|---|
| `painel.html` + `app.js` | pasta `Gestao` | O site. A fonte Inter vai embutida, então abre igual sem internet. |
| `vendor/` | pasta `Gestao` | Apache ECharts 5 (licença Apache 2.0, em `LICENSE-echarts.txt`) e o idioma pt-BR. Não depende de internet nem de CDN. |
| `dados.js` | pasta `Gestao` (gerado todo dia) | Números agregados por dia e carteira, mais uma tabela por **código de cliente PJ** (sem nome nem telefone). Cerca de 1,4 MB por mês de dados. Não tem nome de vendedor (a carteira identifica) nem texto de ligação. |
| `Abrir painel.bat` | pasta `Gestao` | Grava uma linha em `logs\<usuario>.csv` e abre o painel no navegador padrão. |
| `logs/` | pasta `Gestao` | Um arquivo por pessoa, para evitar conflito de sincronização. O painel mostra só contagens. |
| `atualizar_painel.py` e `Atualizar painel.bat` | **só no computador do Thiago** | Leem o CSV, gravam o `dados.js` e copiam para `Gestao` a versão mais nova de `painel.html`, `app.js`, `vendor/` e `Abrir painel.bat`. |
| `painel_config.json` (opcional) | ao lado do script | Baseline oficial e parâmetros. Baixe-o pronto na seção Configurações do painel. |
| `testes/` | repositório | Testes automáticos de números, telas e cliques (para quem mexe no código). |

**Por que não um localhost?**
- Um servidor local esbarra em porta bloqueada, antivírus e firewall, e precisa ficar ligado.
- O navegador abre arquivos locais (`file://`) e carrega `dados.js` e `app.js` com tags `<script>`, o que funciona sem
  servidor no Chrome e no Edge.
- O CSV bruto fica com o Thiago; só os números agregados vão para a pasta compartilhada.

## Montagem (uma vez)

### 1. Pasta e permissões no SharePoint
1. Num site ou biblioteca da equipe, crie a pasta `Painel DVINT` e, dentro dela, a pasta `Gestao`.
2. Permissões (no SharePoint, abra a pasta → **⋯ → Gerenciar acesso**):
   - `Gestao`: **Pode exibir** para a Gerência Operacional e **Pode editar** para o Thiago.
   - `Gestao/logs` (crie a pasta vazia): **Pode editar** para as mesmas pessoas da gerência. Sem isso o `.bat` abre o
     painel, mas não registra o acesso.
3. A permissão da pasta é o controle de acesso. Quem vê a pasta vê:
   - todas as carteiras, por código;
   - os códigos de cliente.

### 2. Computador do Thiago (quem atualiza)
1. Instale o Python 3.9 ou mais novo (python.org, marcando **Add python.exe to PATH**). Depois, no Prompt de Comando,
   rode `pip install pandas`.
2. Copie esta pasta do repositório inteira (`painel.html`, `app.js`, `vendor/`, `atualizar_painel.py`, os dois `.bat`)
   para uma pasta local, por exemplo `Documentos\painel_dvint\`. Essa pasta **não** é a pasta compartilhada.
3. Sincronize a pasta `Gestao` (passo 3) e dê dois cliques em `Atualizar painel.bat`. Na primeira vez:
   - abre uma janela para escolher o CSV. Se você **cancelar**, ela pede uma **pasta** de CSVs;
   - depois, outra janela para escolher a pasta `Gestao`.

   O script grava o `dados.js`, copia o site para a pasta e guarda as escolhas para os próximos dias.

### 3. Computador de cada leitor (Gerência Operacional)
1. Abra a pasta `Painel DVINT` no navegador → **Sincronizar** (ou **Adicionar atalho a Meus arquivos**).
2. No Explorador de Arquivos, clique com o botão direito na pasta `Gestao` → **Sempre manter neste dispositivo**.
3. Botão direito em `Abrir painel.bat` → **Enviar para → Área de trabalho (criar atalho)**. Renomeie o atalho para
   "Painel DVINT".
4. Navegador: Chrome ou Edge atualizados. O site se ajusta a telas de 1366 a 2560 px.

## Rotina diária (Thiago, cerca de 2 minutos)

1. **Exporte o CSV** da análise do dia anterior, no mesmo formato de colunas de sempre, e guarde **todos** os CSVs na
   mesma pasta (por exemplo `Documentos\painel_dvint\csv\`).
   - O script lê a pasta inteira. Se a mesma ligação (`id_transcricao`) estiver em dois arquivos, vale a do mais novo.
   - **Mantenha o histórico desde setembro.** Baseline, reincidência, clientes sem 2ª tentativa, retornos no prazo e o
     número da tentativa dependem dos dias anteriores.
2. Dois cliques em **Atualizar painel.bat**. Confira o resumo na tela:
   - as datas: dados até, duração até e classificação até;
   - os números do baseline: analisadas, conversas, oportunidades, fechamentos, problemas e resolvidos. Eles têm de ser
     **iguais aos do memo da RMR** (8.008 analisadas, 5.887 conversas, 2.252 oportunidades, 192 fechamentos,
     1.342 problemas e 126 resolvidos). Se não forem, a pasta de CSVs não tem setembro completo;
   - os avisos **ATENÇÃO**.
3. O OneDrive envia os arquivos em segundos. Quem abrir o painel (ou apertar F5) vê o dia novo. A data da atualização
   fica no topo e na página "Qualidade do dado".

Por linha de comando (para agendar no Agendador de Tarefas):
`python atualizar_painel.py --entrada "C:\...\csv" --saida "C:\...\Painel DVINT\Gestao"`

## Como usar o painel

| Seção | Pergunta | O que tem |
|---|---|---|
| 1 · Visão geral | Como o time trabalhou no período? | 8 cartões com minigráfico e variação; evolução de qualquer indicador; "o que mudou" (só o que passou da margem de erro); funil do contato ao fechamento; distritais |
| 2 · Tempo | Para onde vai o tempo do time? | Carga operacional nas duas réguas (GPT e Gemini); composição do tempo; horas por tipo de ligação e por código de problema; mapa de calor dia × hora; duração × fechamento; simulador |
| 3 · Vendas | Quanto convertemos e o que acompanha o fechamento? | Funil comercial; taxa de fechamento no tempo; **fechamento por fator** (12 fatores: qualidade do Challenger, SPIN, decisor, tipo, origem, duração, horário…), com intervalo de confiança; fechamentos por tipo; carteiras |
| 4 · Problemas | Onde estão as fricções e o que fica pendente? | Pareto por código (ligações, horas ou todos os citados); resolução de **todos** os códigos; problemas por 100 conversas por carteira; origem; detalhe do código clicado |
| 5 · Challenger e SPIN | Como o time conduz a conversa? | Escada da conversa; qualidade do Challenger no tempo; códigos CH1–CH7; distribuição das notas SPIN; Challenger e SPIN × fechamento; mapa de competências por carteira |
| 6 · Clientes | Quem são os clientes que demandam o time? | Concentração do tempo; tentativas por cliente; sinais (frota própria, concorrente, decisor); **lista de clientes** com filtros (pendência, 2+ problemas, sem 2ª tentativa, retorno vencido, fecharam) e CSV |
| 7 · Contato e cadência | Quando e como o time consegue falar com o cliente? | Mapa de calor do atendimento; volume por hora; atendimento por nº da tentativa; status; tentativas por vendedor-dia; 2ª tentativa e retornos |
| 8 · Carteiras | Como cada carteira está? | Dispersão volume × indicador; distritais; tabela de todas as carteiras com variação; **ficha da carteira** contra a mediana |
| 9 · Qualidade do dado | Posso confiar nos números de hoje? | Cobertura por dia; verificações da carga; valores-sentinela; uso do painel; **dicionário dos indicadores** |

**Como ler os cartões e os gráficos**
- **Variação:** cada cartão mostra a variação contra a comparação escolhida no topo.
  - Verde ▲▼ = melhorou; vermelho = piorou.
  - Cinza com **≈** = a diferença está dentro da margem de erro (teste de duas proporções, 95%): não é mudança.
  - Volumes (ligações, conversas…) são comparados pela média por dia.
- **Interagir:**
  - Passe o mouse em qualquer gráfico para ver valores, tamanho da amostra e intervalo de confiança.
  - Clique numa barra de distrital ou de carteira, num ponto ou numa linha de tabela para filtrar o painel.
  - Os filtros ativos aparecem como etiquetas abaixo do topo; o **×** tira o filtro.
- **Botões de cada gráfico:** **Tabela** mostra os números do gráfico, **CSV** baixa os números e **PNG** baixa a imagem.
- **Atalhos:** as teclas 1 a 9 trocam de seção; a tecla 0 abre as Configurações. Cada computador lembra a última seção e os filtros.

**Cores**
- **Paleta:** derivada do LDS (Localiza Design System, `Color_Code.md`) e conferida com o validador de daltonismo.

  | Cor | Significado |
  |---|---|
  | Verde `#018444` | Vendas, o que melhorou, resolvido |
  | Vermelho `#D92020` | Carga operacional, problema, o que piorou |
  | Azul `#3A7FC1` | Séries neutras (relacionamento, parcial, renovação) |
  | Cinza | Referências: baseline, mediana, sem conteúdo |

- **Ordem:** a escala de verdes vai do claro ao escuro, na ordem das notas.
- **Topo e menu:** verde-noite `#003418` com destaque em verde-limão `#78DE1F`.

## Definições (iguais às do memo)

| Indicador | Definição |
|---|---|
| Ligações analisadas | Têm fonte de classificação |
| Conversas | Analisadas com tipo diferente de "sem conteúdo" |
| Oportunidades de venda | Desfecho diferente de "não era venda" ("interações classificadas como venda" no memo) |
| Taxa de fechamento | Fechamentos (desfecho "fechou …") ÷ oportunidades. É o fechamento **identificado na conversa**, não o do CRM |
| Conversas com problema | Problemas ÷ conversas |
| Resolvidos na ligação | Problemas resolvidos totalmente ÷ problemas |
| Challenger de alta qualidade | Campo de qualidade do Challenger = alta |
| Carga operacional (tempo) | Tempo em problema, suporte, cobrança, pós-venda e dúvida de contrato ÷ tempo das ligações classificadas pelo GPT com duração |

A lista completa, com as colunas do CSV, está na seção 9 do painel.

## Configurações: baseline e parâmetros

A seção **10 · Configurações** do painel tem os ajustes. A etiqueta "comparando com baseline ⚙", abaixo do topo, também
leva até ela.

- **Baseline oficial:** a mesma para todos os leitores. Hoje é setembro/2026. Vem do arquivo `painel_config.json` que fica
  **ao lado do `atualizar_painel.py`, na sua pasta local**. Sem o arquivo, vale setembro/2026.
- **Baseline pessoal:** qualquer leitor pode testar outra baseline (um mês ou um período qualquer). Ela vale só no
  computador dele e na hora.
  - A etiqueta do topo fica azul com a palavra **pessoal**, para ninguém confundir com a oficial.
  - O botão **voltar à oficial** desfaz a escolha.
- **Ajuda para escolher:** a tabela **Meses disponíveis** mostra, para cada mês, dias com dado, volume, fechamento,
  problema, carga operacional e cobertura. Ela marca **mês incompleto** e **cobertura baixa**, para você evitar uma
  baseline ruim. Clique num mês para preencher o formulário.
- **Parâmetros:** mínimo de conversas por carteira (rankings e medianas), amostra mínima de uma taxa (aviso de "amostra
  pequena") e meta de cobertura. Os ajustes também são pessoais.

**Para trocar a baseline oficial** (exemplo: passar a usar janeiro/2026):
1. Na seção Configurações, escolha **janeiro/2026**, clique em **Usar esta baseline (só para mim)** e confira os números
   no painel.
2. Clique em **Baixar painel_config.json**.
3. Salve o arquivo **na sua pasta local**, ao lado do `atualizar_painel.py` (não na pasta compartilhada). Se já existir,
   substitua.
4. Rode o **Atualizar painel.bat**. Ele confirma "Configuração de painel_config.json: baseline janeiro/2026" e imprime os
   números da nova baseline. Todos os leitores passam a ver janeiro/2026 como baseline oficial.

**Requisitos e regras**
- O painel só compara com períodos que estão nos dados. Para usar janeiro/2026, os CSVs de janeiro precisam continuar na
  pasta de CSVs.
- O baseline é **calculado dos dados** do período escolhido, com os mesmos filtros da tela. Assim, cada carteira e cada
  distrital é comparada com o próprio desempenho naquele período.
- O arquivo pode ser editado à mão. Chaves aceitas: `baseline_inicio`, `baseline_fim` (aaaa-mm-dd), `baseline_rotulo`,
  `min_ligacoes`, `min_n_taxa` e `limite_cobertura`. Datas inválidas fazem o script ignorar o arquivo e avisar.

## Validação

- **Antes de divulgar:** os números do baseline impressos pelo `Atualizar painel.bat` têm de bater com o memo
  (rotina diária, passo 2).
- **Nesta versão:** os testes automáticos (`testes/`) conferiram 69 de 69 indicadores do navegador contra o
  recálculo em pandas, em três recortes. Não houve erro de console nas 9 seções em telas de 1366, 1440 e 1920 px.
  Os cliques que filtram, as tabelas, as exportações e o simulador foram testados.

## Registro de acesso

- **O que é gravado:** a cada abertura pelo `Abrir painel.bat`, uma linha com data, hora, usuário do Windows e
  computador, em `logs\<usuario>.csv`.
- **O que o painel mostra:** só contagens, na seção 9. A contagem do dia entra na atualização seguinte.
- **Transparência:** avise as pessoas. Sugestão: *"O atalho do painel registra data, hora e usuário de cada abertura, só
  para medirmos o uso antes de decidir pelo Power BI."*

## Problemas comuns

| Sintoma | Causa provável | O que fazer |
|---|---|---|
| "Não encontrei os dados do painel" ou "Não encontrei a biblioteca de gráficos" | `dados.js` ou `vendor/` só na nuvem, ou ainda sincronizando | Botão direito na pasta `Gestao` → **Sempre manter neste dispositivo**; espere o ícone verde. |
| "Os dados são de uma versão antiga do painel" | O `dados.js` foi gerado pelo script 1.0 | Copie o `atualizar_painel.py` 2.0 para a sua pasta local e rode a atualização. |
| Números de dias atrás | OneDrive pausado | Veja a data no topo; retome a sincronização no ícone da nuvem. |
| O baseline não bate com o memo | A pasta de CSVs não tem setembro completo | Coloque o CSV completo de setembro na pasta e rode de novo. |
| O `.bat` mostra "Não encontrei o painel.html" | O `.bat` foi copiado para fora da pasta | Use um **atalho** em vez de uma cópia, ou edite a linha `set "PASTA=..."` no início do arquivo. |
| O acesso não aparece na seção 9 | Sem permissão de edição em `logs`, ou a atualização ainda não rodou | Ajuste a permissão de `Gestao/logs`. |
| A empresa bloqueia `.bat` no SharePoint | Política de TI | Deixe o `Abrir painel.bat` na área de trabalho de cada leitor, com `set "PASTA=..."` apontando para a pasta sincronizada. |
| "python não é reconhecido" | Python fora do PATH | Reinstale marcando **Add python.exe to PATH**; o `.bat` também tenta `py -3`. |

## Limites desta versão (de propósito)

- **Segurança por linha:** não há. Quem acessa a pasta vê todas as carteiras e clientes. A fase dos vendedores exige uma
  pasta por carteira.
- **Fora do painel:** trechos de ligação e frases para coaching, porque o texto livre pode ter nome e telefone de
  contato (LGPD).
- **Associação, não causa:** os gráficos de "fator × fechamento" mostram associação. Use-os para escolher hipóteses e
  teste no piloto contra o grupo de controle.
- **Troca de versão do classificador:** muda o nível de vários indicadores ao mesmo tempo. Quando muitos indicadores
  mudarem juntos, confira a seção 9 antes de concluir.
