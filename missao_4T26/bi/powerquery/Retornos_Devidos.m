// =====================================================================================================================
// Retornos_Devidos.m  —  ligações em que a análise pediu nova visita com data sugerida JÁ VENCIDA (v1.1, página 6).
// Cada linha traz RetornoNoPrazo = existe nova ligação (qualquer status) do mesmo cliente depois desta e até a data sugerida + 2 dias.
// Relacionamento 1:1 por id_transcricao com Fato_Ligacoes. (setembro: 1.634 devidos, 27,1% no prazo; 22,6% / 26,1% / 28,2% nas
// urgências 1–3 / 4–6 / 7–10 — a urgência declarada NÃO prioriza o retorno.)
// =====================================================================================================================
let
    ToleranciaDias = 2,
    UltimaData = List.Max(Table.Column(Fato_Ligacoes, "Data")),
    Base = Table.SelectRows(
        Fato_Ligacoes,
        each [EhCompleted] and [TemAnaliseGemini] and [CodigoCliente8] <> null and [necessidade_nova_visita_boleano] = true
             and [DataSugerida] <> null and [DataSugerida] > [Data] and [DataSugerida] <= UltimaData
    ),
    BaseMin = Table.SelectColumns(Base, {"id_transcricao", "CodigoCliente8", "DataHora", "Data", "DataSugerida", "urgencia_nova_visita", "CARTEIRA"}),
    Todas   = Table.Buffer(Table.SelectColumns(Table.SelectRows(Fato_Ligacoes, each [CodigoCliente8] <> null and [DataHora] <> null), {"CodigoCliente8", "DataHora", "Data"})),
    Juncao  = Table.NestedJoin(BaseMin, {"CodigoCliente8"}, Todas, {"CodigoCliente8"}, "Prox", JoinKind.LeftOuter),
    Marcada = Table.AddColumn(
        Juncao, "RetornoNoPrazo",
        each Table.RowCount(Table.SelectRows([Prox], (r) => r[DataHora] > [DataHora] and r[Data] <= Date.AddDays([DataSugerida], ToleranciaDias))) > 0,
        type logical
    ),
    FaixaUrgencia = Table.AddColumn(
        Marcada, "FaixaUrgencia",
        each if [urgencia_nova_visita] = null then null else if [urgencia_nova_visita] <= 3 then "1–3" else if [urgencia_nova_visita] <= 6 then "4–6" else "7–10",
        type nullable text
    ),
    Final = Table.RemoveColumns(FaixaUrgencia, {"Prox"})
in
    Final
