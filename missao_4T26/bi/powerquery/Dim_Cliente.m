// =====================================================================================================================
// Dim_Cliente.m  —  uma linha por código de cliente (8 dígitos). Só para a página "Meu painel" (v1.2) e para o K5.
// Relacionamento: Dim_Cliente[CodigoCliente8] 1 → * Fato_Ligacoes[CodigoCliente8] (e 1 → * Retornos_Devidos[CodigoCliente8]).
// ATENÇÃO (RLS): o RLS filtra Dim_Carteira → Fato; esta dimensão não é filtrada. Os visuais só listam clientes com medida
// não vazia (que passa pela Fato já filtrada), mas quem tiver permissão de "Compilar" no conjunto de dados poderia listar todos os
// códigos. Para vendedores: dar apenas permissão de visualização (sem Compilar) e publicar o relatório do vendedor em app.
// =====================================================================================================================
let
    Fonte = Table.SelectColumns(Fato_Ligacoes, {"CodigoCliente8"}),
    SemNulo = Table.SelectRows(Fonte, each [CodigoCliente8] <> null),
    Unico = Table.Distinct(SemNulo)
in
    Unico
