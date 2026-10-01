// =====================================================================================================================
// 00_parametros.m  —  Parâmetros do BI "Excelência Comercial — Venda interna (DVINT)"
//
// COMO CRIAR: Power Query > Gerenciar Parâmetros > Novo Parâmetro (um por bloco abaixo) ou colar cada bloco numa
// consulta em branco (Editor Avançado). Os nomes precisam ser exatamente estes: as demais consultas os referenciam.
// =====================================================================================================================

// ---------------------------------------------------------------------------------------------------------------------
// pInclusaoDesde  (Tipo: Data · Obrigatório)
// Filtro de data de INCLUSÃO do registro no SQL (antes ficava fixo em '2026-09-01' dentro do texto da consulta — M-05).
// Com 2026-09-01 o universo é o mesmo do CSV de setembro (19.078 linhas, 31/08 a 30/09). Para o BI diário manter o valor
// e deixar a base crescer; para olhar só o trimestre mude para #date(2026,10,1) quando o baseline estiver congelado.
// ---------------------------------------------------------------------------------------------------------------------
#date(2026, 9, 1) meta [IsParameterQuery = true, Type = "Date", IsParameterQueryRequired = true]

// ---------------------------------------------------------------------------------------------------------------------
// pFusoHoras  (Tipo: Número decimal · Obrigatório)
// Horas somadas ao timestamp de `data_visita_ev` para chegar no horário de Brasília (M-06). O campo vem em UTC:
// -3 = Brasília sem horário de verão. VALIDAR no primeiro refresh: o histograma de ligações por hora (página 6 do BI)
// deve mostrar o vale do almoço entre 12h e 13h. Se o vale cair às 15h–16h, o fuso está dobrado: coloque 0.
// ---------------------------------------------------------------------------------------------------------------------
-3 meta [IsParameterQuery = true, Type = "Number", IsParameterQueryRequired = true]

// (O mínimo de ligações por carteira é um parâmetro what-if do DAX: ver ../dax/calendario_e_dimensoes.dax, tabela `Param_MinLigacoes`.)
