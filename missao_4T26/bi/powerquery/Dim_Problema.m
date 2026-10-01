// =====================================================================================================================
// Dim_Problema.m  —  legenda dos códigos de problema (P1–P15) do classificador GPT. Habilitar carga.
// Relacionamento: Dim_Problema[Codigo] 1 → * Fato_Ligacoes[p3_problema_principal]
// Fonte da legenda: repositório do projeto (prompt P3 do classificador). Se o prompt mudar, esta é a única tabela a editar.
// "nenhum" = ligação sem problema; mantida na dimensão para não gerar "(Em branco)" nos visuais.
// =====================================================================================================================
let
    Linhas = {
        {"P1",  "Acesso/sistema",               1},
        {"P2",  "Faturamento/cobrança",         2},
        {"P3",  "Multa/infração",               3},
        {"P4",  "Manutenção/substituto",        4},
        {"P5",  "Condutor/cadastro",            5},
        {"P6",  "Km excedente",                 6},
        {"P7",  "Disponibilidade",              7},
        {"P8",  "Franquia/agência",             8},
        {"P9",  "Sinistro",                     9},
        {"P10", "Reserva/sistema",             10},
        {"P11", "Outro",                       11},
        {"P12", "Manipulação de pesquisa/NPS", 12},
        {"P13", "Crédito/cadastro PJ",         13},
        {"P14", "Preço/competitividade",       14},
        {"P15", "Tag de pedágio",              15},
        {"nenhum", "Sem problema",             99}
    },
    Tabela = Table.FromRows(Linhas, {"Codigo", "Descricao", "Ordem"}),
    Rotulo = Table.AddColumn(Tabela, "Rotulo", each if [Codigo] = "nenhum" then [Descricao] else [Codigo] & " · " & [Descricao], type text),
    Tipado = Table.TransformColumnTypes(Rotulo, {{"Codigo", type text}, {"Descricao", type text}, {"Ordem", Int64.Type}})
in
    Tipado
