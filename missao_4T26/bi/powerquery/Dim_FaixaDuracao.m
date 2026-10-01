// =====================================================================================================================
// Dim_FaixaDuracao.m  —  faixas de duração da ligação de negociação (página 6). Habilitar carga.
// Relacionamento: Dim_FaixaDuracao[Faixa] 1 → * Fato_Ligacoes[FaixaDuracao]
// Limites (segundos, intervalo fechado à direita): ≤120 · ≤300 · ≤480 · ≤720 · >720. Mesmos cortes de Fato_Ligacoes[FaixaDuracao].
// =====================================================================================================================
let
    Linhas = {
        {"< 2 min",   1,   0,  120},
        {"2–5 min",   2, 120,  300},
        {"5–8 min",   3, 300,  480},
        {"8–12 min",  4, 480,  720},
        {"> 12 min",  5, 720, 99999}
    },
    Tabela = Table.FromRows(Linhas, {"Faixa", "Ordem", "DeSeg", "AteSeg"}),
    Tipado = Table.TransformColumnTypes(Tabela, {{"Faixa", type text}, {"Ordem", Int64.Type}, {"DeSeg", Int64.Type}, {"AteSeg", Int64.Type}})
in
    Tipado
