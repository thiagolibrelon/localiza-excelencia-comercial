// =====================================================================================================================
// Dim_Carteira.m  —  uma linha por carteira da venda interna (DVINT). Habilitar carga.
// Relacionamento: Dim_Carteira[CARTEIRA] 1 → * Fato_Ligacoes[CARTEIRA]  (filtro Dim → Fato)
//
// Carteira ↔ matrícula é 1:1 no CSV de setembro (67 = 67). O BI usa a CARTEIRA como rótulo padrão (decisão da missão);
// MATRICULA e nome NÃO entram nesta tabela (ver Dim_Vendedor_Restrito.m).
// Se uma carteira tiver duas matrículas na origem (troca de vendedor), Table.Distinct mantém a primeira: conferir a contagem.
// =====================================================================================================================
let
    Fonte    = F_Carteiras_Equipe,
    SoDVINT  = Table.SelectRows(Fonte, each [DIVISIONAL] = "DVINT" and [CARTEIRA] <> null),
    Colunas  = Table.SelectColumns(SoDVINT, {"DIVISIONAL", "DISTRITAL", "CARTEIRA"}),
    Unica    = Table.Distinct(Colunas, {"CARTEIRA"}),
    Tipado   = Table.TransformColumnTypes(Unica, {{"DIVISIONAL", type text}, {"DISTRITAL", type text}, {"CARTEIRA", type text}})
in
    Tipado
