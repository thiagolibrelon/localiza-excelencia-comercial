// =====================================================================================================================
// Resumo_Time.m  —  totais do TIME por dia e grupo de tempo, SEM carteira. Só para a página "Meu painel" (v1.2).
// Por que existe: com RLS na carteira, qualquer medida sobre a Fato devolve só a carteira do vendedor; "o time" precisa de uma tabela
// que não passe pelo filtro. Contém apenas agregados do time inteiro (nada por carteira, vendedor ou cliente).
// Relacionamento: Dim_Calendario[Data] 1 → * Resumo_Time[Data].
// =====================================================================================================================
let
    Fonte = Fato_Ligacoes,
    Grupo = Table.Group(
        Fonte, {"Data", "GrupoTempo"},
        {
            {"SegBase",       each List.Sum(Table.Column(Table.SelectRows(_, each [BaseKPI] = true), "DuracaoSeg")), type nullable number},
            {"Tentativas",    each Table.RowCount(_), Int64.Type},
            {"Atendidas",     each Table.RowCount(Table.SelectRows(_, each [EhCompleted] = true)), Int64.Type},
            {"Positivas",     each Table.RowCount(Table.SelectRows(_, each [ClasseLigacao] = "POSITIVA")), Int64.Type},
            {"Informativas",  each Table.RowCount(Table.SelectRows(_, each [ClasseLigacao] = "INFORMATIVA")), Int64.Type},
            {"Detratoras",    each Table.RowCount(Table.SelectRows(_, each [ClasseLigacao] = "DETRATORA")), Int64.Type}
        }
    )
in
    Grupo
