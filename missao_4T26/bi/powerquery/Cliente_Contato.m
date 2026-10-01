// =====================================================================================================================
// Cliente_Contato.m  —  uma linha por cliente com tentativas de ligação ATIVA (outbound) no período (v1.1, página 6).
// Relacionamento: Cliente_Contato[CodigoCliente8] 1 → * Fato_Ligacoes[CodigoCliente8].
// Responde: quantos clientes ficaram com UMA tentativa sem sucesso e nenhuma segunda? (setembro: 2.985; a 2ª tentativa é atendida
// em 30,5% das vezes ⇒ ≈ 900 conversas/mês que hoje não acontecem).
// =====================================================================================================================
let
    Fonte   = Table.SelectRows(Fato_Ligacoes, each [tipo_ligacao] = "Outbound" and [CodigoCliente8] <> null and [DataHora] <> null),
    Grupo   = Table.Group(
        Fonte, {"CodigoCliente8"},
        {
            {"Tentativas", each Table.RowCount(_), Int64.Type},
            {"Atendidas",  each List.Count(List.Select(Table.Column(_, "EhCompleted"), each _ = true)), Int64.Type},
            {"PrimeiraTentativa", each List.Min(Table.Column(_, "DataHora")), type nullable datetime},
            {"UltimaTentativa",   each List.Max(Table.Column(_, "DataHora")), type nullable datetime}
        }
    ),
    NuncaAtendeu = Table.AddColumn(Grupo, "NuncaAtendeu", each [Atendidas] = 0, type logical),
    UmaSoSemSucesso = Table.AddColumn(NuncaAtendeu, "UmaTentativaSemSucesso", each [Tentativas] = 1 and [Atendidas] = 0, type logical)
in
    UmaSoSemSucesso
