// =====================================================================================================================
// Tentativa_Seq.m  —  número da tentativa (1ª, 2ª, 3ª…) de cada ligação ativa para o mesmo cliente (v1.1, página 6).
// Relacionamento 1:1 por id_transcricao com Fato_Ligacoes. Responde: a taxa de atendimento sobe, cai ou fica igual na 2ª, 3ª, 4ª tentativa?
// (setembro: 36,5% · 30,5% · 33,5% · 32,8% ⇒ insistir compensa; a 2ª tentativa é a que mais deixamos de fazer).
// =====================================================================================================================
let
    Fonte    = Table.SelectRows(Fato_Ligacoes, each [tipo_ligacao] = "Outbound" and [CodigoCliente8] <> null and [DataHora] <> null),
    Minima   = Table.SelectColumns(Fonte, {"id_transcricao", "CodigoCliente8", "DataHora"}),
    Ordenada = Table.Buffer(Table.Sort(Minima, {{"CodigoCliente8", Order.Ascending}, {"DataHora", Order.Ascending}})),
    Grupos   = Table.Group(
        Ordenada, {"CodigoCliente8"},
        {{"T", each Table.AddIndexColumn(_, "TentativaSeq", 1, 1, Int64.Type), type table}}
    ),
    Expandida = Table.ExpandTableColumn(Grupos, "T", {"id_transcricao", "TentativaSeq"})
in
    Expandida
