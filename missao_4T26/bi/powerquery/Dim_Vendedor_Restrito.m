// =====================================================================================================================
// Dim_Vendedor_Restrito.m  —  matrícula e nome por carteira. NÃO carregar no modelo publicado para a empresa toda.
// A missão decidiu mostrar o vendedor pela CARTEIRA; o nome só entra num modelo/relatório com RLS (gestão) ou na ficha de
// drill-through de acesso restrito. Se for usar: carregar, ocultar a tabela, relacionar por CARTEIRA e aplicar o papel de RLS "Gestao".
// =====================================================================================================================
let
    Fonte   = Table.SelectRows(Ligacoes_Base, each [ForaDVINT] = false),
    Colunas = Table.SelectColumns(Fonte, {"CARTEIRA", "matricula_ev_createdby", "nome_createdby"}),
    Unica   = Table.Distinct(Colunas, {"CARTEIRA"}),
    Renomeada = Table.RenameColumns(Unica, {{"matricula_ev_createdby", "Matricula"}, {"nome_createdby", "Vendedor"}})
in
    Renomeada
