# Auditoria do painel MVP v1.0: produto, análises e front-end

> 13/10/2026 · feita antes de escrever qualquer código da v2.
> **Objeto:** `painel.html` v1.0 (commit `a381463`), o CSV de setembro que alimenta o painel e o memo de setembro para a RMR (fotos de 13/10).
> **Medições:** o painel foi aberto no Chromium em quatro tamanhos de tela; a densidade e os cliques foram contados por página; os números do memo foram recalculados com o CSV.

---

## 0. Em 1 minuto

1. **O memo e o painel não mostram os mesmos números.**
   - O memo fala em 8.008 ligações, 1.342 problemas e 192 fechamentos.
   - O CSV do painel tem 6.232 ligações classificadas, 963 problemas e 150 fechamentos.
   - As **taxas** batem (diferença de até 2 p.p.); os **volumes** são de 27% a 39% maiores no memo.
   - Se alguém abrir o painel na RMR, os números não conversam com o memo. É o item mais urgente (seção 1).
2. **O painel conta uma história e o memo conta outra.**
   - O painel abre pelo **tempo**: carga operacional de 43,2% do tempo de ligação.
   - O memo abre por **conversão e fricções**: 8,5% de fechamento, 22,8% das conversas com problema e 3 códigos que concentram 64,5% dos problemas.
   - Isso combina com o "projeto maior que redução de tempo" que o chefe pediu. A v2 deve abrir pela história do memo e manter o tempo como uma das lentes.
3. **"Setembro é a baseline", mas o painel ainda diz "provisório".**
   - As metas estão fixas no código e não há registro de qual versão do classificador gerou cada número.
   - Outubro classificado pelo C12, comparado com um setembro de versões misturadas, mostra **variações falsas**.
4. **"Parece colado" é literal.** O painel é um slide de 1280×720 px ampliado ou reduzido por zoom:
   - ocupa 67% da largura de uma tela de 1920 px e 50% de uma de 2560 px;
   - num notebook de 1366 px a fonte cai para 10,8 px;
   - não tem nenhuma dica ao passar o mouse (tooltip) em nenhuma página, e as páginas 2, 6 e 8 não têm nenhum elemento clicável;
   - cada clique redesenha a página inteira, e a lista da página 5 volta ao topo quando se clica numa carteira.
5. **Recomendação para a v2:**
   - um site responsivo, com gráficos interativos (Apache ECharts num arquivo local, que funciona sem internet);
   - filtros globais que se aplicam ao clicar em qualquer gráfico, e drill até a carteira e o código de problema;
   - uma página **"Resultado do mês"** que é o próprio memo;
   - um **acompanhamento das prioridades** com dono, medida e meta.

**Decisões que preciso de você** estão na seção 8. São 7, e as 3 primeiras travam o resto.

---

## 1. Memo × painel: os números não batem (crítico)

Setembro, com as mesmas definições aplicadas ao CSV do painel (`Consulta Power Bi`, 18.144 tentativas em setembro):

| Indicador do memo | Memo | CSV do painel | Diferença |
|---|---|---|---|
| Ligações analisadas | **8.008** | 6.232 classificadas (6.217 atendidas) | memo +28% |
| Ligações com conversa | **5.887** | 4.601 (classificadas, sem "sem_conteudo") | +28% |
| Interações classificadas como venda | **2.252** | 1.776 (desfecho ≠ "não era venda") | +27% |
| Fechamentos · taxa | **192 · 8,5%** | 150 · **8,4%** | taxa igual |
| Conversas com problema | **1.342 · 22,8%** | 963 · **20,9%** | +1,9 p.p. |
| Acesso + cobrança + crédito PJ | **866 · 64,5%** (403 / 237 / 226) | 639 · **66,4%** (305 / 173 / 161) | ordem igual |
| Resolvidos na ligação | **126 · 9,4%** | 94 · **9,8%** | taxa igual |
| Parcial / não / sem desfecho | 727 / 485 / 4 | 492 / 374 / 3 | proporções próximas |
| Preço e competitividade (P14) | **68 · 85,3% não resolvido** | 38 · **84,2%** não resolvido | taxa igual |
| Challenger → fechamento | **10,6%** (alta qualidade) **vs 8,1%** | 9,8% (teve Challenger) vs 8,1% | ver 1.2 |

### 1.1 O que isso quer dizer
- **As conclusões do memo se sustentam.** As taxas, a ordem dos códigos e a baixa resolução aparecem nas duas bases.
- **Os volumes vêm de outra base.** No CSV do painel, a classificação GPT de setembro vai só até 25/09 e mistura versões do
  prompt (há um salto na taxa de problema em 15/09). A explicação mais provável é que o memo use **setembro inteiro
  reprocessado com o classificador novo (C12)**, que é o E2 do plano. **Isso é hipótese: preciso que você confirme qual
  arquivo o memo usou.**
- **Risco na RMR:** o painel mostra 963 problemas e o memo, 1.342. Quem comparar vai perder a confiança nos dois.
- **Risco nas decisões:** se o painel comparar outubro (classificado pelo C12) com o setembro atual (versões misturadas),
  vai mostrar melhora ou piora que é só mudança de régua.

### 1.2 Observações sobre o conteúdo do memo (para a apresentação)

| Ponto | Situação | Sugestão |
|---|---|---|
| Escopo | Bom: diz que setembro é a baseline e que agosto é só contexto | Dizer numa linha o **período** (01–30/09), o **escopo** (DVINT? RAC inteiro?) e a **versão do classificador** |
| Challenger | 10,6% vs 8,1% parece grande, mas o memo não mostra o tamanho da amostra | No CSV, 9,8% (IC 95%: 7,2% a 13,2%, n = 387) vs 8,1% (6,7% a 9,6%, n = 1.389): os intervalos se sobrepõem. O próprio memo já diz que "não demonstra o efeito". Mostrar o n e apresentar como **hipótese a testar no piloto**, não como resultado |
| Taxa de fechamento de 8,5% | Vem do desfecho dado pelo classificador, não do sistema de vendas | Dizer "fechamento identificado na conversa". Validar contra o CRM quando possível (no CSV, o desfecho dá 150 fechamentos e a flag `venda`, 148) |
| Resolução parcial | Representa 54% dos problemas | "Parcial" é ambíguo; vale validar uma amostra de cerca de 50 ligações com a operação antes de usar como meta |
| Tempo (carga operacional) | Não aparece no memo | Decidir se o K1 de tempo continua sendo o indicador da missão ou vira uma lente secundária (decisão 3) |
| Prioridades | A foto mostra só a 1ª: melhorar a conversão · Liderança Comercial · treino · taxa de fechamento | Mande o memo inteiro: cada prioridade vira uma linha do acompanhamento no painel (seção 2.4) |

---

## 2. Produto

### 2.1 Para quem e para quê

| Quem | Quando | Pergunta | O que o v1 entrega hoje |
|---|---|---|---|
| Gerência Operacional | Todo dia, cerca de 5 min | O que mudou ontem e o que faço hoje? | Página 1 (bom), mas os alertas não dizem o que fazer |
| Reunião de segunda | Semanal, 15 min | Piorou ou melhorou? Quais são as 2 ações? | Página 2 + roteiro (bom); não guarda as decisões |
| RMR / diretoria | Mensal | Qual é o resultado do mês contra a baseline e as prioridades? | **Não tem.** O memo é feito fora do painel |
| Liderança Comercial | Semanal | Onde treinar para converter mais? | Página 7 mostra Challenger e SPIN, **mas não o efeito na conversão** |
| Vendedores (fase 2) | Diário | Como foi meu dia e quem retomar? | Fora do v1 (decisão de 13/10) |

### 2.2 O que manter
- Uma pergunta por página.
- Filtros de período, distrital e carteira.
- Carteira por código, sem nome.
- Página de qualidade do dado.
- Números conferidos contra a reconciliação (135 de 135).
- Texto livre fora do painel (LGPD).
- Registro de uso para medir adoção.
- Paleta LDS.

### 2.3 Achados

| # | Achado | Gravidade |
|---|---|---|
| P-1 | O painel não conta a história do memo: o tempo vem primeiro e a conversão e as fricções estão espalhadas | Alta |
| P-2 | Não há página de resultado do mês (baseline × mês × variação) que sirva de fonte do memo | Alta |
| P-3 | Não fecha o ciclo da ação: as prioridades do memo (dono, ação, medida) não aparecem nem são acompanhadas | Alta |
| P-4 | Não existe funil comercial (ligações → conversas → oportunidades de venda → fechamentos), que é a 1ª linha do memo | Alta |
| P-5 | O destaque "preço sem resolução" (P14) não aparece: a resolução por código mostra só os 4 códigos com mais ligações | Média |
| P-6 | O destaque Challenger → conversão não aparece: a página 7 mostra taxas de Challenger, mas não a conversão | Média |
| P-7 | Jargão: K1, K2, K4, K5, K6, K7, C1 e C2 sem explicação na tela | Média |
| P-8 | Páginas muito densas: 6 a 13 visuais e 260 a 420 palavras por página; tudo com o mesmo peso, sem hierarquia | Média |
| P-9 | "O que mudou" existe só na página 1; as outras não comparam com a baseline nem com o período anterior | Média |
| P-10 | Não exporta (imagem, CSV, PDF) e não tem modo de apresentação para a RMR | Média |
| P-11 | Não há orientação de primeiro uso nem glossário | Baixa |

### 2.4 Arquitetura proposta para a v2 (site)

```
┌──────────────────────────────────────────────────────────────────────────────────────────────┐
│ Excelência Comercial · DVINT     [Período ▾] [Distrital ▾] [Carteira 🔍] [Código ▾]   Comparar: │
│                                   filtros ativos: [DTIN2 ×] [P1 ×]          (•) baseline ( ) anterior │
├───────────────┬──────────────────────────────────────────────────────────────────────────────┤
│ Início        │  CARTÕES COM MINIGRÁFICO: fechamento 8,5% ▲ · problemas 22,8% ▼ · resolução 9,4%  │
│ Resultado mês │  · carga operacional 43% · cobertura 95%   (clique no cartão = vai para o detalhe) │
│ Conversão     ├──────────────────────────────────────────────────────────────────────────────┤
│ Fricções      │  GRÁFICO PRINCIPAL INTERATIVO (tooltip, zoom no tempo, clique filtra tudo)     │
│ Tempo         ├────────────────────────────────┬─────────────────────────────────────────────┤
│ Carteiras     │  QUEBRA (código / carteira)     │  "O QUE FAZER": 3 ações sugeridas pelas regras │
│ Contato       ├────────────────────────────────┴─────────────────────────────────────────────┤
│ Prioridades   │  TABELA DE DETALHE (ordenável, busca, exporta CSV)                              │
│ Confiança     │                                                                                 │
└───────────────┴──────────────────────────────────────────────────────────────────────────────┘
```

| Seção v2 | Substitui | Conteúdo | Por quê |
|---|---|---|---|
| **Início** | p1 Dia | Ontem contra a média de 5 dias e contra a baseline; alertas com a ação sugerida e um link para o detalhe | Rotina diária da Gerência |
| **Resultado do mês** | (novo) | Espelho do memo: tese, tabela baseline × mês × variação, destaques gerados pelas regras, prioridades. Imprime em PDF e congela o mês apresentado | Fonte única da RMR |
| **Conversão** | parte da p6 e p7 | Funil comercial; fechamento por carteira, duração, Challenger e SPIN, sempre com n e intervalo de confiança | Prioridade 1 do memo |
| **Fricções** | p4 | Volume e taxa; **todos** os códigos; resolução de qualquer código; reincidência; origem; pendências | Destaques 2 e 3 do memo |
| **Tempo** | p3 | Carga operacional (K1) nas duas réguas, composição do tempo, simulador | Lente de capacidade (missão original) |
| **Carteiras** | p5 | Dispersão volume × taxa; ficha da carteira (drill: tudo da carteira numa tela) | Onde agir |
| **Contato e cadência** | resto da p6 | Funil de tentativas, mapa de calor dia da semana × hora, 2ª tentativa, retornos | Alavanca de produtividade |
| **Prioridades** | (novo) | Cada prioridade do memo: dono, ação, medida, baseline, atual, meta, status | Fechar o ciclo decisão → resultado |
| **Confiança do dado** | p8 | Cobertura, versão do classificador por dia, verificações, uso do painel | Saber se dá para confiar no número de hoje |

A página **Semana** deixa de existir sozinha e vira uma escolha de **granularidade** (dia, semana ou mês) que vale em todas
as seções. O roteiro de segunda vai para Prioridades.

---

## 3. Análises

| # | Achado | Risco para a decisão | Proposta |
|---|---|---|---|
| A-1 | **Régua (versão do classificador)**: setembro mistura versões (salto em 15/09); o C12 entrou em 23–25/09 | Variação falsa entre meses | Versão gravada por linha; o painel marca as trocas de régua e só calcula a variação contra a baseline com a mesma régua |
| A-2 | **Baseline** são constantes no código, rotuladas como "provisório" | Meta e variação erradas | Arquivo `baseline.json` congelado (valor, janela, n, régua, fonte). Indicadores de **contagem** usam setembro inteiro; indicadores de **tempo** usam 01–22/09 (só há duração até aí). As duas janelas aparecem na tela |
| A-3 | **Definições** divergem: "com conversa", "interação de venda", o denominador da taxa de problema (GPT 20,3% vs conversas 20,9%) e K1 por tempo vs participação por contagem | Dois números para a mesma pergunta | Um dicionário único (memo = painel), com a definição no ⓘ de cada indicador |
| A-4 | **Amostra e ruído**: o K1 diário de carteira usa no mínimo 8 ligações; não há intervalo de confiança nas taxas, exceto na faixa de duração | Agir por ruído | n sempre visível; intervalo de 95% nas taxas; aviso "diferença dentro da margem"; mínimo por nível (dia, semana, mês) |
| A-5 | **Causalidade**: Challenger e duração aparecem associados à conversão, e a ligação longa pode durar mais *porque* é venda | Treinar e cobrar a coisa errada | Rótulo "associação"; provar no piloto contra o grupo de controle (plano, seção 6) |
| A-6 | **Faltam as análises do memo** | O memo continua sendo feito à mão | Funil comercial; conversão com e sem Challenger (n e IC); resolução de qualquer código (P14); problemas por 100 conversas, por carteira; pendências por código |
| A-7 | **Verdade de campo**: o fechamento vem do classificador, não do CRM; "parcial" corresponde a 54% dos problemas | Meta sobre um rótulo instável | Amostra de validação de cerca de 50 ligações com a operação; cruzar com vendas quando houver acesso |
| A-8 | **Duração parou em 22/09** | Os indicadores de tempo param | Chamado de duração (plano E5); enquanto isso, o painel mostra só as lentes por contagem |
| A-9 | Visuais de baixo valor para decisão: medidor (gauge), tentativas por vendedor por dia, concentração de clientes na tela principal | Ruído visual | Medidor vira barra de progresso; os outros dois descem para o detalhe |
| A-10 | Ranking de carteira só por taxa | Carteira pequena no topo | Dispersão taxa × volume, com tamanho por horas; ordenar por impacto (excesso × volume) |

---

## 4. Front-end e experiência

### 4.1 Diagnóstico (medido)

| O que | Medida | Por que dá a sensação de "colado" |
|---|---|---|
| Layout | Quadro fixo de 1280×720 px com posições absolutas e zoom | É um slide: não usa a tela (67% da largura em 1920 px, 50% em 2560 px) e reduz a fonte em notebook (10,8 px em 1366 px) |
| Gráficos | SVG montado como texto, redesenhado a cada clique | Nada responde ao mouse; sem animação e sem foco |
| Tooltips | **0** em todas as páginas | Para ver um número, ele tem de estar escrito; por isso o excesso de rótulos e texto |
| Cliques | Páginas 2, 6 e 8: **0** elementos clicáveis; páginas 3 e 7: 6 a 7 | Gráfico não leva a lugar nenhum |
| Redesenho | Cada clique troca o HTML da página inteira | Pisca, perde o foco e perde a rolagem (página 5: rolagem de 400 px vai para 0 ao clicar numa carteira) |
| Filtros | Só no menu lateral; sem indicação de "filtros ativos" | Usuário esquece que há filtro ligado |
| Tabelas | Sem ordenação, sem busca, sem exportação | Não dá para investigar |
| Datas | Campo de data no formato do navegador | Em navegador em inglês aparece mm/dd |
| Saída | Sem imagem, CSV, PDF ou modo apresentação | RMR depende de print da tela |
| Acessibilidade | SVG sem título e sem descrição; vermelho e verde sem outro código visual em parte das legendas | Daltonismo (cerca de 8% dos homens) e leitores de tela |
| Desempenho | Troca de página em cerca de 75 ms; `dados.js` com cerca de 0,55 MB por mês | **Bom**, não é gargalo |

### 4.2 O que "parecer um site" exige
1. **Layout responsivo** (grade CSS): ocupa a tela toda, rola na vertical e funciona de 1366 a 2560 px.
2. **Cabeçalho fixo** com os filtros globais e "chips" dos filtros ativos (× para tirar).
3. **Hierarquia em quatro níveis** em cada seção: cartões → gráfico principal → quebra → tabela de detalhe.
4. **Todo gráfico com:**
   - tooltip (valor, n, intervalo de confiança, variação contra a baseline);
   - destaque ao passar o mouse;
   - clique que filtra todo o painel;
   - legenda que liga e desliga séries;
   - transição animada.
5. **Drill-down:** carteira → ficha da carteira; código → detalhe do código; dia → dia de referência.
6. **Comparar com** (baseline ou período anterior) e **granularidade** (dia, semana ou mês), em todo o painel.
7. **Cartões com minigráfico** (sparkline) e seta de variação; clique leva ao detalhe.
8. **Ajuda no contexto:** ⓘ com a definição do indicador; primeiro acesso com um tour de 4 passos.
9. **Saída:**
   - PNG de cada gráfico e CSV de cada tabela;
   - PDF da página "Resultado do mês";
   - **modo apresentação** (tela cheia, fonte maior, ← → entre seções).
10. **Atualização sem piscar:** só o que mudou é redesenhado; rolagem e foco são mantidos.

### 4.3 Opções de tecnologia

| Opção | Interatividade | Funciona sem internet (`file://`) | Peso | Esforço da v2 | Manutenção |
|---|---|---|---|---|---|
| A. SVG próprio (atual) + camada de interação | Média, cada recurso feito à mão | Sim | ~0 | Alto | Difícil (tudo é código próprio) |
| **B. Apache ECharts em arquivo local** (recomendado) | **Alta e nativa**: tooltip, zoom, seleção, legenda, clique, animação, exportar imagem, padrões para daltonismo | **Sim** (arquivo `vendor/echarts.min.js` na pasta) | ~1 MB (há versão enxuta) | Médio | Boa: biblioteca madura, licença Apache 2.0 |
| C. Chart.js | Média | Sim | ~0,2 MB | Médio | Boa, mas menos tipos de gráfico (Pareto, mapa de calor e combinações dão mais trabalho) |
| D. Power BI | Alta | Não se aplica | — | — | Adiado por decisão de 13/10 até medir o uso |

**Recomendação: B.**
- A biblioteca fica na própria pasta do SharePoint, copiada pelo `atualizar_painel.py` (que já copia o `painel.html`).
- Nada depende de CDN, que pode ser bloqueado pela rede da empresa.
- O HTML único de 200 KB vira três arquivos: `painel.html`, `app.js` e `vendor/`, o que facilita a manutenção.
- A paleta LDS e a fonte Inter continuam.

### 4.4 Desenho visual
- Uma cor de destaque por gráfico. Vermelho e verde só com significado (piorou/melhorou) e sempre com seta ou ícone junto.
- Escala tipográfica fixa: 32 / 20 / 14 / 12 px. Rótulos só nos pontos-chave; o resto vai para o tooltip.
- Espaço em branco no lugar de bordas; cartões mais leves; no máximo 5 cartões por linha.

---

## 5. Dados e engenharia

| # | Achado | Proposta |
|---|---|---|
| E-1 | Fonte do painel ≠ fonte do memo | O `atualizar_painel.py` passa a ler a base do memo (saída do C12?), com um adaptador de colunas. **Preciso do arquivo ou de um exemplo** |
| E-2 | Baseline e metas no código | `baseline.json` (congelado e versionado) + `config.json` (metas e limites) na pasta do painel |
| E-3 | Os testes (135 conferências, layout, cliques) existem só na sessão | Levar para o repositório (`painel/testes/`) e rodar antes de publicar cada versão |
| E-4 | Sem contrato de dados | Na atualização: checar o esquema, a versão do classificador e o volume do dia contra a média (alerta de queda), e detectar dia duplicado |
| E-5 | Crescimento | Cerca de 0,55 MB por mês, ou 7 MB por ano: manter 13 meses e congelar uma **foto de cada mês** para a RMR (o número apresentado não muda se o dado for reprocessado) |
| E-6 | `.bat` nunca rodou em Windows | Testar no seu PC: caminho com espaço e acento, SmartScreen, permissão de `logs` |
| E-7 | Versão do painel | Versão no rodapé + histórico de mudanças no LEIA-ME |

---

## 6. Governança, LGPD e adoção
- **Registro de acesso:** avisar antes de ligar (texto pronto no LEIA-ME) e mostrar só contagens.
  - Meta de adoção sugerida: 80% da gerência abrindo o painel 3 ou mais vezes por semana, durante 4 semanas.
- **Carteira identifica o vendedor** para quem é do time: a pasta continua restrita à gestão. A fase dos vendedores exige
  uma pasta por carteira.
- **Decisões registradas** (página Prioridades) são a prova de valor do painel para a diretoria, além dos acessos.
- **Trechos de ligação** seguem fora do painel.

---

## 7. Backlog priorizado

Esforço: P = até meio dia · M = 1 a 2 dias · G = 3 a 5 dias.

| Onda | # | Item | Esforço | Depende de |
|---|---|---|---|---|
| **0 · antes da RMR** | 1 | Fonte única: confirmar a base do memo e alinhar as definições (seção 1) | P | Decisão 1 |
| | 2 | Ajustes no memo: escopo e régua numa linha; n do Challenger; "fechamento identificado na conversa" | P | — |
| | 3 | Se a RMR for antes da v2: **não abrir o painel v1 ao vivo**, ou recarregá-lo com a base do memo | P | Decisão 1 |
| **1 · v2 base** | 4 | Layout de site responsivo + cabeçalho com filtros e chips + ECharts local | G | Decisão 4 |
| | 5 | Tooltips, clique que filtra, legenda interativa e transições em todos os gráficos | M | 4 |
| | 6 | `baseline.json` + `config.json` + "comparar com" baseline ou período anterior | M | Decisão 2 |
| | 7 | Seções Início, Resultado do mês, Conversão e Fricções (com todos os códigos e P14) | G | 4, 6 |
| | 8 | Testes no repositório (conferência, layout, cliques) | P | — |
| **2 · gestão** | 9 | Prioridades (dono, medida, meta, status) + roteiro de segunda | M | Decisão 6 |
| | 10 | Ficha da carteira (drill) + dispersão volume × taxa | M | 4 |
| | 11 | Contato: mapa de calor dia × hora, 2ª tentativa, retornos | M | 4 |
| | 12 | Exportações (PNG, CSV, PDF) + modo apresentação + foto congelada do mês | M | 7 |
| | 13 | Glossário ⓘ + tour de primeiro acesso | P | 7 |
| **3 · depois** | 14 | Fase dos vendedores (pasta e dados por carteira) | G | Adoção da gerência |
| | 15 | Validação do fechamento contra o CRM e da resolução "parcial" com a operação | M | Acesso ao dado |

---

## 8. Decisões que preciso de você

1. **Fonte única.** Qual arquivo gerou o memo (8.008 ligações)? O painel passa a ler essa base? Se for a saída do
   classificador C12, me mande o caminho ou um exemplo com as colunas.
2. **Baseline oficial.** Setembro inteiro, com qual régua (C12?), para os indicadores de contagem; e 01–22/09 para os de
   tempo (por causa da duração)? A partir daí o painel deixa de dizer "provisório".
3. **Indicador principal para a diretoria.** Conversão + fricções (como no memo), com o tempo como lente, ou o K1 de tempo
   continua sendo o indicador da missão?
4. **Tecnologia do front-end.** ECharts em arquivo local (recomendado) ou SVG próprio?
5. **Arquitetura da v2.** As 9 seções da 2.4 servem? Algo sai ou entra?
6. **Prioridades no painel.** As prioridades do memo viram um acompanhamento com dono e meta? Mande o memo inteiro.
7. **Data da RMR.** Ela define o que entra na onda 0 e se o painel vai ou não para a reunião.
