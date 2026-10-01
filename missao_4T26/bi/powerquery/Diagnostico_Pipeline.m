// =====================================================================================================================
// Diagnostico_Pipeline.m  —  contagens de cobertura da carga (M-07). Habilitar carga. Alimenta a página 8 "Qualidade do dado".
// Cada linha é uma verificação: quantas linhas falham, em que base, e em que nível o time deve se preocupar.
// Esta tabela é reavaliada em CADA atualização: se uma junção quebrar (ex.: Tempo_de_ligação parou de atualizar), o número sobe aqui
// em vez de a carga continuar "verde" com a coluna toda vazia.
// =====================================================================================================================
let
    Base    = Ligacoes_Base,
    DVINT   = Table.SelectRows(Base, each [ForaDVINT] = false),
    Compl   = Table.SelectRows(DVINT, each [status] = "Completed"),
    N       = (t as table) as number => Table.RowCount(t),
    Distintos = (t as table, col as text) as number => List.Count(List.Distinct(Table.Column(t, col))),

    Linhas = {
        // {Ordem, Verificacao, Falhas, Base, Gravidade (Informativo/Atencao/Critico), Limite aceito (% da base), O que fazer}
        {1, "Linhas lidas do SQL",                                     N(Base),                                              N(Base),  "Informativo", null, "Conferir contra a execução anterior (queda brusca = filtro de data ou DSN)"},
        {2, "Linhas fora do DVINT ou sem carteira (descartadas)",      N(Table.SelectRows(Base, each [ForaDVINT])),          N(Base),  "Atencao",     0.05, "Matrícula sem cadastro em F_Carteiras_Equipe: atualizar a tabela de equipe"},
        {3, "Status 'Not Started' (descartadas)",                      N(Table.SelectRows(DVINT, each [status] = "Not Started")), N(DVINT), "Informativo", null, "Sem ação; só acompanhar"},
        {4, "id_transcricao duplicado",                                 N(DVINT) - Distintos(DVINT, "id_transcricao"),        N(DVINT), "Critico",     0,    "Junção multiplicando linhas (Tempo_de_ligação ou Ligações Classificadas com chave repetida)"},
        {5, "Completed sem segment_id (sem elo com a transcrição)",     N(Table.SelectRows(Compl, each [segment_id] = null)), N(Compl), "Critico",     0.02, "Tabela metadata sem o call_object: avisar o time de dados"},
        {6, "Completed sem análise Gemini (Aletheia)",                  N(Table.SelectRows(Compl, each [resumo_analise] = null)), N(Compl), "Atencao",  0.10, "Fila de análise atrasada. Hoje vira 'SEM ANALISE' (M-01), não mais 'DETRATORA'"},
        {7, "Completed sem classificação GPT",                          N(Table.SelectRows(Compl, each [fonte_classificacao] = null)), N(Compl), "Critico", 0.05, "Rodar o classificador do dia (C1 da missão: meta ≥ 95%)"},
        {8, "Completed sem duração (Tempo_de_ligação)",                 N(Table.SelectRows(Compl, each [CallDurationInSeconds] = null)), N(Compl), "Critico", 0.05, "Tabela de tempo parada (em setembro parou em 22/09: C2 da missão)"},
        {9, "Linhas sem codigo_cliente",                                N(Table.SelectRows(DVINT, each [codigo_cliente] = null)), N(DVINT), "Atencao",   0.10, "Reincidência e recontato ficam subestimados"},
        {10, "Linhas sem data_visita_ev",                               N(Table.SelectRows(DVINT, each [data_visita_ev] = null)), N(DVINT), "Critico",   0,    "Sem data a ligação some das séries"}
    },
    Tabela = Table.FromRows(Linhas, {"Ordem", "Verificacao", "Falhas", "Base", "Gravidade", "LimitePct", "Acao"}),
    Pct    = Table.AddColumn(Tabela, "Pct", each if [Base] = 0 then null else [Falhas] / [Base], type nullable number),
    Status = Table.AddColumn(
        Pct, "Status",
        each if [LimitePct] = null then "ℹ"
             else if [Pct] = null then "ℹ"
             else if [Pct] <= [LimitePct] then "OK"
             else if [Gravidade] = "Critico" then "CRITICO" else "ATENCAO",
        type text
    ),
    Tipado = Table.TransformColumnTypes(Status, {{"Ordem", Int64.Type}, {"Falhas", Int64.Type}, {"Base", Int64.Type}, {"LimitePct", type nullable number}, {"Pct", type nullable number}})
in
    Tipado
