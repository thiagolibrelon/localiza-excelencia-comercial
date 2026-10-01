# Especificação dos visuais — BI v1 (Excelência Comercial · venda interna DVINT)

> Cada linha é um visual do Power BI Desktop: tipo, campos, medidas (definidas em `dax/medidas.dax`), filtros de visual e observações. Os IDs (1.1, 1.2…) são os mesmos das imagens em `mockups/` (versão anotada).
> **Escopo:** `v1` = entra na publicação de 07/10 · `v1.1` = depende de consulta ou dado extra, entra depois (já desenhado nas imagens) · `v1.2` = página 9, relatório do vendedor: só depois da conversa com a Gerência/RH e do RLS testado.
> Todas as medidas citadas existem em `dax/medidas.dax`. Valores esperados de setembro: `reconciliacao.csv`.

## Elementos comuns a todas as páginas

| ID | Elemento | Tipo | Escopo | Campo / medida | Observação |
|---|---|---|---|---|---|
| G1 | Navegador de páginas | Botões de página (navegador) | v1 | — | Ação: navegar para a página. Fixo no painel esquerdo, mesma posição nas 8 páginas. |
| G2 | Período | Segmentação · intervalo de datas | v1 | Dim_Calendario[Data] | Sincronizada entre todas as páginas. Padrão: mês corrente. Páginas 1 e 8 ignoram a seleção nos cartões de 'dia de referência'. |
| G3 | Distrital | Segmentação · lista suspensa | v1 | Dim_Carteira[DISTRITAL] | Sincronizada entre todas as páginas. Seleção múltipla. |
| G4 | Carteira | Segmentação · lista suspensa | v1 | Dim_Carteira[CARTEIRA] | Sincronizada. Na página 7 vira seleção única (carteira vs mediana). |
| G5 | Cabeçalho de dados | Cartão de texto | v1 | [Texto Cabecalho] | 'Dados até … · duração até … · atualizado em …'. Em todas as páginas, canto inferior do painel. |
| G6 | Aviso de baseline provisório | Cartão de texto | v1 | [Texto Baseline] | Remover (ou trocar o texto) quando o baseline for congelado em 09/10. |

**Formato do canvas:** 1280 × 720 px (16:9), tema `tema/Excelencia_Comercial.json`, painel de navegação e segmentações à esquerda (168 px), conteúdo à direita.

**Interações padrão:** filtros cruzados ligados entre visuais da mesma página, exceto onde a observação disser o contrário; segmentações Período, Distrital e Carteira sincronizadas entre páginas; página 7 usa Carteira com seleção única.

## Página 1 · Dia

**Pergunta de decisão:** O que mudou ontem e exige ação hoje?  
**Quem usa:** Excelência Comercial, Gerência Operacional (leitura diária, 5 min)

| ID | Visual | Tipo | Escopo | Eixo / campos | Medidas | Filtros do visual | Observações |
|---|---|---|---|---|---|---|---|
| 1.1 | Carga operacional (K1) · GPT | Cartão (valor + 2 linhas de apoio) | v1 | — | [K1 D-1] · apoio: [Delta K1 D-1 vs Dia Anterior pp], [K1 MM5 D-1] | Nenhum (ignora a segmentação de data) | Cor do valor: [Cor K1 Meta]. |
| 1.2 | Carga operacional · Gemini | Cartão | v1 | — | [K1 Gemini D-1] | — | Segunda régua. Se GPT e Gemini divergirem em tendência, olhar a página 8. |
| 1.3 | Negociação (K7) | Cartão | v1 | — | [K7 D-1] | — | Meta de K7 a calibrar em 09/10. |
| 1.4 | Pendências geradas (K2) | Cartão | v1 | — | [K2 D-1] · apoio: [K2 por Dia Util] | — | Problema não resolvido na ligação. |
| 1.5 | Horas de conversa | Cartão | v1 | — | [Horas D-1] · apoio: [Ligacoes D-1] | — | Base do K1 do dia. |
| 1.6 | Carga operacional por dia — duas réguas | Gráfico de linhas | v1 | Eixo: Dim_Calendario[Data] | [K1 Carga Operacional], [K1 Gemini Suporte], [K1 MM5], [K1 Baseline], [K1 Meta Geral] | Visual: Dim_Calendario[EhDiaUtil] = Verdadeiro e [Dias Uteis com Dado] ≥ 1 | Baseline e meta como séries tracejadas. K1 MM5 tracejada na cor do K1 GPT. |
| 1.7 | Alertas do dia | 3 cartões de texto empilhados (v1) + 2 alertas (v1.1) | v1 | — | [Alerta K1], [Alerta Cobertura], [Alerta Pendencias] | — | v1.1: alerta de mudança de régua e pico de P1 (dependem da coluna de versão do classificador, pedido novo N1 (ver README_BI_v1.md)). |
| 1.8 | Últimos 7 dias úteis | Tabela | v1 | Linhas: Dim_Calendario[Data] | [K1 Carga Operacional], [K7 Negociacao], [K2 Pendencias], [Horas Base KPI], [C1 Cobertura Classificacao], [C2 Cobertura Duracao] | Visual: [Ultimos 7 Uteis] = 1 | Barras de dados em K1 e K2; ícone de alerta quando C1 ou C2 < 95%. |
| 1.9 | Carteiras com mais pendências ontem | Tabela | v1 | Linhas: Dim_Carteira[CARTEIRA] | [Ligacoes D-1], [K2 D-1], [K1 D-1], [K1 MM5 D-1], [Desvio K1 vs MM5 pp] | Visual: [Ligacoes D-1] ≥ 8 · Top 6 por [K2 D-1] | Mínimo de 8 ligações porque K1 diário de carteira com menos que isso oscila 20–50 p.p. sem significado. Clique filtra a página. |

## Página 2 · Semana

**Pergunta de decisão:** A tendência piora ou melhora?  
**Quem usa:** Gerência Operacional e Comercial (leitura de segunda, 08h)

| ID | Visual | Tipo | Escopo | Eixo / campos | Medidas | Filtros do visual | Observações |
|---|---|---|---|---|---|---|---|
| 2.1 | K1 da semana | Cartão (valor + variação) | v1 | — | [K1 Semana Ref] · apoio: [Delta K1 Semana Ref pp] | — | Aviso 'semana parcial' quando [Dias Uteis Semana Ref] < 5. |
| 2.2 | K7 da semana | Cartão (valor + variação) | v1 | — | [K7 Semana Ref] · apoio: [Delta K7 Semana Ref pp] | — |  |
| 2.3 | Pendências por dia útil | Cartão | v1 | — | [K2 por Dia Semana Ref] | — |  |
| 2.4 | Horas de conversa | Cartão | v1 | — | [Horas Semana Ref] · apoio: [Dias Uteis Semana Ref] | — |  |
| 2.5 | Carga operacional por semana | Colunas agrupadas | v1 | Eixo: Dim_Calendario[SemanaRotulo] | [K1 Carga Operacional], [K1 Gemini Suporte], [K1 Baseline], [K1 Meta Geral] | Visual: [Dias Uteis com Dado] ≥ 1 | Baseline e meta como séries de linha. |
| 2.6 | Negociação (K7) × taxa de problema (K6) | Colunas e linha | v1 | Eixo: Dim_Calendario[SemanaRotulo] | Colunas: [K7 Negociacao] · Linha: [K6 Taxa de Problema] | Visual: [Dias Uteis com Dado] ≥ 1 | K6 sobe depois de 15/09 junto com a mudança da régua do GPT: não interpretar como piora real. |
| 2.7 | Matriz semanal | Matriz | v1 | Linhas: Dim_Calendario[SemanaRotulo] | [Dias Uteis com Dado], [Horas Base KPI], [K1 Carga Operacional], [Delta K1 vs Semana Anterior pp], [K1 Gemini Suporte], [K7 Negociacao], [Delta K7 vs Semana Anterior pp], [K6 Taxa de Problema], [K2 Pendencias], [K2 por Dia Util] | — | Ícones nos deltas: ▲ laranja = carga subiu, ▼ azul = carga caiu (invertido para K7). |
| 2.8 | Leitura de segunda · 08h | Caixa de texto | v1 | — | (texto fixo) | — | Três perguntas: o que piorou? o que fazemos? quem faz até quando? Decisões registradas em ata fora do BI (C5 da missão). |

## Página 3 · Mês

**Pergunta de decisão:** Estamos no caminho da meta?  
**Quem usa:** Chefia (acompanhamento mensal)

| ID | Visual | Tipo | Escopo | Eixo / campos | Medidas | Filtros do visual | Observações |
|---|---|---|---|---|---|---|---|
| 3.1 | K1 do período vs meta | Medidor | v1 | — | Valor: [K1 Carga Operacional] · Destino: [K1 Meta Geral] · Mín 0 · Máx 0,8 | — | Baseline (43,2%) como marca adicional desenhada em texto no título; o medidor nativo só tem o destino. |
| 3.2 | Horas operacionais | Cartão | v1 | — | [Horas Operacionais] · apoio: [Horas Base KPI] | — |  |
| 3.3 | Horas devolvidas vs baseline | Cartão | v1 | — | [Horas Devolvidas Equiv] | — | Zero no mês do baseline; vira a métrica de sucesso a partir de outubro. |
| 3.4 | Horas excedentes (K3) | Cartão | v1 | — | [K3 Horas Excedentes] · apoio: [K3 Horas Excedentes Mes Equiv] | — | Custo extra em horas das ligações com problema vs ligação sem problema. |
| 3.5 | Pendências (K2) | Cartão | v1 | — | [K2 Pendencias] · apoio: [K2 por Dia Util] | — |  |
| 3.6 | Como ler este baseline | Cartão de texto | v1 | — | [Texto Baseline] | — | Remover o aviso após o congelamento (09/10). |
| 3.7 | Para onde vai o tempo do time | Barra 100% empilhada | v1 | Legenda: Fato_Ligacoes[GrupoTempo] | [Seg Base KPI] | Visual: GrupoTempo ≠ 'Não classificado (GPT)' | Cores: laranja = operacional com problema, laranja claro = operacional sem problema, azul = negociação, azul claro = relacionamento, cinza = sem conteúdo. |
| 3.8 | Composição do tempo | Tabela | v1 | Linhas: Fato_Ligacoes[GrupoTempo] | [Ligacoes Base KPI], [Horas Base KPI], [Pct Tempo do Grupo], [TMA Geral (s)] | Visual: GrupoTempo ≠ 'Não classificado (GPT)' |  |
| 3.9 | Simulador: reduzir ligações P1 | Segmentação (seleção única) | v1 | Param_ReducaoP1[Value] | — | — | 0 a 100% de 10 em 10. Padrão 30% (medida [Simulacao Reducao P1 pct]). |
| 3.10 | Resultado da simulação | 3 cartões | v1 | — | [Simulacao Horas Devolvidas P1 Mes], [Simulacao Efeito no K1 pp], [Horas P1 Mes Equiv] | — | A simulação é aritmética (horas de P1 × % escolhido), não previsão. |

## Página 4 · Problemas

**Pergunta de decisão:** Onde o tempo se perde e o que fica pendente?  
**Quem usa:** Gerência Operacional (donos dos 3 maiores códigos de problema)

| ID | Visual | Tipo | Escopo | Eixo / campos | Medidas | Filtros do visual | Observações |
|---|---|---|---|---|---|---|---|
| 4.1 | Taxa de problema (K6) | Cartão | v1 | — | [K6 Taxa de Problema] | — | Só acompanhar: sensível à versão do classificador. |
| 4.2 | Pendências (K2) | Cartão | v1 | — | [K2 Pendencias] · apoio: [K2 por Dia Util] | — |  |
| 4.3 | Resolução na ligação (K4) | Cartão | v1 | — | [K4 Resolucao na Ligacao] | — | Meta do piloto: ≥ 20% nos códigos priorizados. |
| 4.4 | Reincidência (K5) | Cartão | v1 | — | [K5 Reincidencia] | — | Calculada no contexto de filtro (mês, distrital, carteira). |
| 4.5 | Horas excedentes (K3) | Cartão | v1 | — | [K3 Horas Excedentes] · apoio: [K3 Horas Excedentes Mes Equiv] | — |  |
| 4.6 | Pareto do tempo em problema | Colunas e linha | v1 | Eixo: Dim_Problema[Rotulo] (ordenar por [Horas com Problema] decrescente) | Colunas: [Horas com Problema] · Linha: [Pareto Acumulado] | Visual: Dim_Problema[Codigo] ≠ 'nenhum' · Top 8 | Clique filtra a tabela 4.9. |
| 4.7 | Resolução por código | Barras 100% empilhadas | v1 | Eixo: Dim_Problema[Rotulo] · Legenda: Fato_Ligacoes[p3_foi_resolvido_na_ligacao] | [Ligacoes Problema] | Visual: top 4 códigos por [Ligacoes Problema] | Ordem da legenda: SIM, PARCIAL, NAO. |
| 4.8 | Taxa de problema por origem | Colunas | v1 | Eixo: Fato_Ligacoes[tipo_ligacao] | [K6 Base Duracao] · rótulo: [Pct Problemas Outbound] | — | A ligação receptiva tem o dobro da taxa de problema, mas 80% dos problemas nascem em ligação ativa. |
| 4.9 | Carteiras com mais tempo em problema | Tabela | v1 | Linhas: Dim_Carteira[CARTEIRA] | [Ligacoes GPT], [Ligacoes Problema], [K6 Taxa de Problema], [Horas com Problema], [K2 Pendencias], [Ligacoes P1] | Visual: [Carteira Elegivel] = 1 · Top 8 por [Horas com Problema] | Drill-through (v1.1): ficha da carteira. |

## Página 5 · Carteiras

**Pergunta de decisão:** Quais carteiras concentram a carga?  
**Quem usa:** Gerência Comercial e distritais

| ID | Visual | Tipo | Escopo | Eixo / campos | Medidas | Filtros do visual | Observações |
|---|---|---|---|---|---|---|---|
| 5.1 | Carga operacional por carteira | Barras horizontais (com rolagem) | v1 | Eixo: Dim_Carteira[CARTEIRA] (ordenar por [K1 Carga Operacional] decrescente) | [K1 Carga Operacional] · cor condicional: [Cor K1 Carteira] · linha de referência: [K1 Mediana Carteiras] | Visual: [Carteira Elegivel] = 1 | Tooltip: [Ligacoes GPT], [Horas Base KPI], [K6 Taxa de Problema], [Posicao K1 Carteira]. |
| 5.2 | Carga operacional por distrital | Colunas | v1 | Eixo: Dim_Carteira[DISTRITAL] | [K1 Carga Operacional] | — | Interação com 5.1 desligada (não filtrar). |
| 5.3 | X% dos clientes concentram Y% do tempo | Barras horizontais | v1 | Eixo: Param_TopPct[Pct] | [Pct Tempo Top N Clientes] | — | Mostra se o problema é de poucos clientes (1% dos clientes = 20% do tempo). |
| 5.4 | Mínimo de ligações por carteira | Segmentação (seleção única) | v1 | Param_MinLigacoes[Value] | — | — | Padrão 40. Define quem entra em ranking e mediana. |
| 5.5 | Resumo das carteiras | 3 cartões | v1 | — | [Carteiras Elegiveis], [K1 Mediana Carteiras], [K1 Min Carteira] · [K1 Max Carteira] | — |  |

## Página 6 · Tempo e ritmo

**Pergunta de decisão:** Que duração e que cadência rendem mais?  
**Quem usa:** Gerência Comercial, Excelência Comercial

| ID | Visual | Tipo | Escopo | Eixo / campos | Medidas | Filtros do visual | Observações |
|---|---|---|---|---|---|---|---|
| 6.1 | Taxa de fechamento por duração | Colunas com barras de erro | v1 | Eixo: Dim_FaixaDuracao[Faixa] (ordenar por Ordem) | [Taxa de Fechamento] · barras de erro: [Taxa Fechamento IC Inferior], [Taxa Fechamento IC Superior] | — | Intervalo de Wilson 95%. Não existe duração única ótima: a taxa sobe com a duração, mas a ligação longa também é a de negócio maior. |
| 6.2 | Fechamentos por hora | Colunas | v1 | Eixo: Dim_FaixaDuracao[Faixa] | [Fechamentos por Hora] | — | Produtividade do tempo de telefone: ≈ 1 fechamento/h de 5 min em diante. |
| 6.3 | Onde está o tempo e onde estão os fechamentos | Colunas agrupadas | v1 | Eixo: Dim_FaixaDuracao[Faixa] | [Pct Tempo na Faixa], [Pct Fechamentos na Faixa] | — |  |
| 6.4 | Funil das tentativas | Barra 100% empilhada | v1 | Legenda: Fato_Ligacoes[status] | [Tentativas] | — | Atendida (Completed), sem sucesso, em aberto. |
| 6.5 | Atendimento por hora (Brasília) | Colunas | v1 | Eixo: Fato_Ligacoes[Hora] | [Taxa Atendimento] · rótulo: [Tentativas] | Visual: Hora entre 8 e 18 | Valida o fuso: o vale do almoço tem que aparecer em 12–13h. |
| 6.6 | Tentativas por vendedor por dia da semana | Colunas agrupadas | v1 | Eixo: Dim_Calendario[DiaSemanaNome] (ordenar por DiaSemanaNum) | [Tentativas por Vendedor por Dia], [Atendidas por Vendedor por Dia] | Visual: DiaSemanaNum ≤ 5 | Sexta tem ≈ 29% menos tentativas por vendedor que a segunda. |
| 6.7 | Clientes sem 2ª tentativa | 2 cartões | v1.1 | — | [Clientes Uma Tentativa Sem Sucesso], [Conversas Potenciais 2a Tentativa] | — | Exige Cliente_Contato e Tentativa_Seq. |
| 6.8 | Atendimento por nº da tentativa | Colunas | v1.1 | Eixo: Tentativa_Seq[TentativaSeq] | [Taxa Atendimento] | Visual: TentativaSeq ≤ 4 | Exige Tentativa_Seq. |
| 6.9 | Retornos pedidos pelo cliente | 2 cartões + colunas | v1.1 | Eixo (colunas): Retornos_Devidos[FaixaUrgencia] | [Retornos Devidos], [Retorno no Prazo %] | — | Exige Retornos_Devidos. A urgência declarada não prioriza o retorno (22% / 26% / 28%). |

## Página 7 · Competências

**Pergunta de decisão:** Onde treinar?  
**Quem usa:** Aprendizagem, Gerência Comercial, coaches

| ID | Visual | Tipo | Escopo | Eixo / campos | Medidas | Filtros do visual | Observações |
|---|---|---|---|---|---|---|---|
| 7.1 | Challenger: o que acontece na conversa | Barras horizontais | v1 | Eixo: Dim_Habilidade[Habilidade] (Grupo = 'Taxa', 4 primeiras linhas) | [Habilidade Valor] | Visual: Dim_Habilidade[Ordem] ≤ 4 | Denominadores diferentes: teve Challenger = ligações classificadas; dado/conecta/reage = ligações com a pergunta respondida. |
| 7.2 | SPIN: nota média e % de nota 1 | Colunas | v1 | Eixo: Dim_Habilidade[Habilidade] (Grupo = 'Nota') | [Habilidade Valor] · rótulo: [SPIN Implicacao Nota 1 %] (na coluna Implicação) | Visual: Dim_Habilidade[Grupo] = 'Nota' | Implicação é a competência mais fraca (nota 1 em metade das análises). |
| 7.3 | Carteira vs mediana das carteiras (taxas) | Barras agrupadas | v1 | Eixo: Dim_Habilidade[Habilidade] | [Habilidade Valor], [Habilidade Mediana] | Visual: Dim_Habilidade[Grupo] = 'Taxa' · exige uma carteira selecionada | Sem carteira selecionada, mostra o time contra a própria mediana. |
| 7.4 | Carteira vs mediana das carteiras (notas SPIN) | Barras agrupadas | v1 | Eixo: Dim_Habilidade[Habilidade] | [Habilidade Valor], [Habilidade Mediana] | Visual: Dim_Habilidade[Grupo] = 'Nota' |  |
| 7.5 | Carteiras com maior oportunidade de treino | Tabela | v1 | Linhas: Dim_Carteira[CARTEIRA] | [SPIN Implicacao], [SPIN Implicacao Nota 1 %], [Taxa Trouxe Dado], [Taxa Challenger], [Ligacoes GPT] | Visual: [Carteira Elegivel] = 1 · Bottom 6 por [SPIN Implicacao] | Base para formar as turmas da trilha (projeto 8.1 do plano de oportunidades). |
| 7.6 | Trecho para coaching | Cartão de texto (acesso restrito) | v1.1 | Textos_Restrito | (trechos mascarados) | RLS: só gestão | NÃO publicar no modelo da empresa toda (LGPD). |

## Página 8 · Qualidade do dado

**Pergunta de decisão:** Posso confiar nos números de hoje?  
**Quem usa:** Excelência Comercial (dono do BI), time de dados

| ID | Visual | Tipo | Escopo | Eixo / campos | Medidas | Filtros do visual | Observações |
|---|---|---|---|---|---|---|---|
| 8.1 | Cobertura de classificação (C1) | Cartão com ícone | v1 | — | [C1 Cobertura Classificacao] | — | Meta ≥ 95%. |
| 8.2 | Cobertura de duração (C2) | Cartão com ícone | v1 | — | [C2 Cobertura Duracao] | — | Meta ≥ 95%. |
| 8.3 | Atendimentos sem análise Gemini | Cartão | v1 | — | [Completed sem Gemini] | — | Eram 'DETRATORA' na consulta antiga (M-01). |
| 8.4 | Última atualização (C3) | Cartão | v1 | — | [Ultima Atualizacao] · apoio: [Horas desde Atualizacao] | — | Meta: atualizado até 08h do dia útil. O horário do mockup é ilustrativo. |
| 8.5 | Colunas do CSV por uso | Cartão (3 valores) | v1 | Dicionario_Colunas[uso_recomendado] | Contagem de linhas por valor | — | 46 usar · 34 com ressalva · 8 não usar. |
| 8.6 | Cobertura por dia (C1 e C2) | Gráfico de linhas | v1 | Eixo: Dim_Calendario[Data] | [C1 Cobertura Classificacao], [C2 Cobertura Duracao], linha de meta [Limite_Cobertura] | Visual: EhDiaUtil = Verdadeiro | Mostra o corte de 22/09 (duração) e de 28/09 (classificação). |
| 8.7 | Taxa de problema por dia (GPT) | Gráfico de linhas | v1 | Eixo: Dim_Calendario[Data] | [K6 Taxa de Problema] | Visual: [Ligacoes GPT] ≥ 1 | Salto em 15/09 = mudança de versão da régua. Anotar no gráfico enquanto não houver coluna de versão. |
| 8.8 | Verificações da carga | Tabela | v1 | Linhas: Diagnostico_Pipeline[Verificacao] | Falhas, Base, Pct, LimitePct, Status | — | Formatação condicional por [Status]: OK, ATENCAO, CRITICO. |
| 8.9 | Campos com valor-sentinela | Barras horizontais | v1 | Eixo: Dicionario_Colunas[coluna] | pct_sentinela | Visual: Top 7 por pct_sentinela | Campos que parecem preenchidos mas são 'sem dados necessários' (volume de frota, concorrência…). |

## Página 9 · Meu painel (relatório do vendedor)

**Pergunta de decisão:** Como foi meu tempo e quem preciso retomar?  
**Quem usa:** O vendedor, só na própria carteira (RLS 'Carteira'). Relatório separado, mesmo modelo

| ID | Visual | Tipo | Escopo | Eixo / campos | Medidas | Filtros do visual | Observações |
|---|---|---|---|---|---|---|---|
| 9.1 | Meu tempo em negociação | Cartão (valor + comparação) | v1.2 | — | [K7 Negociacao] · apoio: [K7 Time] | RLS: só a minha carteira | Comparação com o time vem de Resumo_Time (fora do RLS). |
| 9.2 | Minha carga operacional | Cartão (valor + comparação) | v1.2 | — | [K1 Carga Operacional] · apoio: [K1 Time], [Dif K1 vs Time pp] | — | Laranja = mais carga que o time. Texto neutro: 'acima/abaixo do time', nunca 'pior'. |
| 9.3 | Atendimento | Cartão (valor + comparação) | v1.2 | — | [Taxa Atendimento] · apoio: [Taxa Atendimento Time], [Atendidas], [Tentativas] | — | Mostra também o último dia (usar [Tentativas] e [Atendidas] com filtro de dia na tooltip). |
| 9.4 | Problemas sem resolução | Cartão | v1.2 | — | [K2 Pendencias] · apoio: [Clientes com Pendencia] | — | Resolução 'na ligação': a medida não sabe se outra ligação resolveu depois. |
| 9.5 | Conversas sem objetivo atingido | Cartão (valor + comparação) | v1.2 | — | [Pct Conversas Detratoras] · apoio: [Pct Conversas Detratoras Time], [Conversas Detratoras], [Conversas com Analise] | — | 'Detratora' é a classe da CONVERSA (objetivo não atingido), não um cliente detrator. Não usar a palavra 'detrator' para cliente. |
| 9.6 | Meu dia a dia | Colunas empilhadas | v1.2 | Eixo: Dim_Calendario[Data] · Legenda: Fato_Ligacoes[GrupoTempo] | [Horas Base KPI] | Visual: [Dias Uteis com Dado] ≥ 1 | Horas de conversa por dia, por tipo de tempo. |
| 9.7 | Para onde foi meu tempo | 2 barras 100% empilhadas (carteira e time) | v1.2 | Legenda: Fato_Ligacoes[GrupoTempo] (carteira) e Resumo_Time[GrupoTempo] (time) | [Seg Base KPI] (carteira) · [Pct Tempo Grupo Time] (time) | — | Mesmas cores da página 3. As duas barras ficam alinhadas para comparar. |
| 9.8 | Problemas que mais tomaram meu tempo | Barras horizontais | v1.2 | Eixo: Dim_Problema[Rotulo] | [Horas com Problema] | Visual: Top 5 por [Horas com Problema], Codigo ≠ 'nenhum' | Quem resolve na origem é a Operação; o vendedor vê para saber o que reportar. |
| 9.9 | Clientes para retomar | Tabela + 3 chips de contagem | v1.2 | Linhas: Dim_Cliente[CodigoCliente8] | [Motivo Retomar], [Ultimo Contato], [Dias sem Contato] · chips: [Clientes com Pendencia], [Clientes Retorno Vencido], [Clientes Sem 2a Tentativa] | Visual: [Itens Retomar] > 0 · Top 8 por [Itens Retomar] | O código do cliente aparece completo no BI (o vendedor o conhece pelo CRM). Quem vê é só o dono da carteira. |

---
Total: 61 visuais v1 · 4 visuais v1.1 · 9 visuais v1.2 (página 9) · 6 elementos comuns.
