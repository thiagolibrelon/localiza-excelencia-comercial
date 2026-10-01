// =====================================================================================================================
// Dim_Challenger.m  —  legenda dos códigos Challenger CH1–CH7. Habilitar carga.
// Uso na v1: só rótulo (página 7). Os códigos por ligação vêm em Fato_Ligacoes[p5_codigos_challenger] como texto com
// vários códigos ("CH6;CH3"); a contagem por código fica para a v1.1 (tabela ponte), então esta dimensão NÃO tem relacionamento na v1.
// =====================================================================================================================
let
    Linhas = {
        {"CH1", "Custo oculto revelado",                    1},
        {"CH2", "ROI calculado",                            2},
        {"CH3", "Urgência por regra real",                  3},
        {"CH4", "Concorrente ou alternativa superada com dado", 4},
        {"CH5", "Dor revelada → produto conectado",         5},
        {"CH6", "Antecipação de problema",                  6},
        {"CH7", "Descoberta de necessidade não declarada",  7}
    },
    Tabela = Table.FromRows(Linhas, {"Codigo", "Descricao", "Ordem"}),
    Tipado = Table.TransformColumnTypes(Tabela, {{"Codigo", type text}, {"Descricao", type text}, {"Ordem", Int64.Type}})
in
    Tipado
