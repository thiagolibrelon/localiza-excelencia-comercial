# Medidas por escopo (gerado a partir de `especificacao_visuais.md` e das dependências entre medidas em `dax/medidas.dax`)

Total em medidas.dax: **166**. Criar na ordem em que aparecem no arquivo (cada medida só usa as de cima).

| Grupo | Medidas | Quando |
|---|---|---|
| Núcleo | 88 | Páginas 1–5 e 8 (só visuais v1), com as dependências. **Criar primeiro.** |
| Reconciliação e KPIs de apoio | 14 | K1a/K1b, K8/K9, checagens do modelo (M-01), metas de piloto. Criar na sexta, junto com a reconciliação. |
| Páginas 6 e 7 | 34 | Se houver tempo antes de 07/10; senão entram na v1.1. |
| Página 9 · Meu painel (v1.2) | 19 | Relatório do vendedor; exige Dim_Cliente, Resumo_Time e Retornos_Devidos. |
| v1.1 e apoio | 11 | Cliente_Contato, Tentativa_Seq, Retornos_Devidos (exigem consultas extras) e sobras. |

## Núcleo
- Atendidas
- Ligacoes GPT
- Ligacoes Base KPI
- Seg Base KPI
- Horas Base KPI
- Dias Uteis com Dado
- Dias com Classificacao
- Dados ate
- Ultimo Dia com Duracao
- Data Referencia
- Dia Util Anterior
- Seg Operacional
- K1 Carga Operacional
- K7 Negociacao
- K1 Gemini Suporte
- Horas Operacionais
- K1 Baseline
- K1 Meta Geral
- Horas Devolvidas Equiv
- Ligacoes Problema
- K6 Taxa de Problema
- K2 Pendencias
- K2 por Dia Util
- K4 Resolucao na Ligacao
- K5 Reincidencia
- Ligacoes Problema Base KPI
- K6 Base Duracao
- Pct Problemas Outbound
- TMA Problema (s)
- TMA Sem Problema (s)
- K3 Horas Excedentes
- K3 Horas Excedentes Mes Equiv
- Horas com Problema
- Pareto Acumulado
- Simulacao Reducao P1 pct
- Horas P1
- Simulacao Horas Devolvidas P1 Mes
- Simulacao Efeito no K1 pp
- Min Ligacoes Carteira
- Carteira Elegivel
- K1 Mediana Carteiras
- Carteiras Elegiveis
- Posicao K1 Carteira
- Cor K1 Carteira
- Pct Tempo Top N Clientes
- K1 MM5
- K1 D-1
- K1 Dia Anterior
- K7 D-1
- K2 D-1
- Horas D-1
- K1 MM5 D-1
- Desvio K1 vs MM5 pp
- Alerta K1
- K1 Semana Anterior
- Delta K1 vs Semana Anterior pp
- K7 Semana Anterior
- Delta K7 vs Semana Anterior pp
- Cor K1 Meta
- C1 Cobertura Classificacao
- C2 Cobertura Duracao
- Completed sem Gemini
- Ultima Atualizacao
- Horas desde Atualizacao
- Texto Cabecalho
- Texto Baseline
- Alerta Cobertura
- K1 Gemini D-1
- Ligacoes D-1
- Delta K1 D-1 vs Dia Anterior pp
- Alerta Pendencias
- Ultimos 7 Uteis
- Semana Referencia
- K1 Semana Ref
- K1 Semana Ref Anterior
- Delta K1 Semana Ref pp
- K7 Semana Ref
- K7 Semana Ref Anterior
- Delta K7 Semana Ref pp
- K2 por Dia Semana Ref
- Horas Semana Ref
- Dias Uteis Semana Ref
- Pct Tempo do Grupo
- TMA Geral (s)
- Ligacoes P1
- Horas P1 Mes Equiv
- K1 Min Carteira
- K1 Max Carteira

## Reconciliação e KPIs de apoio
- K1a Com Problema
- K1b Operacional Sem Problema
- K8 Relacionamento
- K9 Sem Conteudo
- Dif K1 GPT vs Gemini pp
- Horas Negociacao
- K1 Meta Piloto
- K7 Baseline
- Delta K1 vs Baseline pp
- Progresso da Meta
- Razao TMA
- Completed sem GPT
- Linhas SEM ANALISE
- Linhas Detratora Legada

## Páginas 6 e 7
- Tentativas
- Taxa Atendimento
- Ligacoes Negociacao
- Fechamentos
- Taxa de Fechamento
- Taxa Fechamento IC Inferior
- Taxa Fechamento IC Superior
- Fechamentos por Hora
- Pct Tempo na Faixa
- Pct Fechamentos na Faixa
- Vendedor Dias
- Tentativas por Vendedor por Dia
- Atendidas por Vendedor por Dia
- Taxa Challenger
- Taxa Trouxe Dado
- Taxa Conectou Situacao
- Taxa Cliente Reagiu
- SPIN Situacao
- SPIN Problema
- SPIN Implicacao
- SPIN Necessidade
- SPIN Implicacao Nota 1 %
- Falou com Decisor %
- Mediana Taxa Challenger
- Mediana Taxa Trouxe Dado
- Mediana Taxa Conectou Situacao
- Mediana Taxa Cliente Reagiu
- Mediana SPIN Situacao
- Mediana SPIN Problema
- Mediana SPIN Implicacao
- Mediana SPIN Necessidade
- Mediana Falou com Decisor %
- Habilidade Valor
- Habilidade Mediana

## Página 9 · Meu painel (v1.2)
- K1 Time
- K7 Time
- Pct Tempo Grupo Time
- Taxa Atendimento Time
- Conversas Detratoras
- Conversas com Analise
- Pct Conversas Detratoras
- Pct Conversas Detratoras Time
- Dif K1 vs Time pp
- Ultimo Contato
- Dias sem Contato
- Flag Pendencia
- Flag Retorno Vencido
- Flag Sem 2a Tentativa
- Itens Retomar
- Motivo Retomar
- Clientes com Pendencia
- Clientes Retorno Vencido
- Clientes Sem 2a Tentativa

## v1.1 e apoio
- Seg Total Duracao
- Share Codigo no Problema
- K7 Mediana Carteiras
- K6 Mediana Carteiras
- Clientes com Codigo
- Clientes Outbound
- Clientes Uma Tentativa Sem Sucesso
- Taxa Atendimento 2a Tentativa
- Conversas Potenciais 2a Tentativa
- Retornos Devidos
- Retorno no Prazo %
