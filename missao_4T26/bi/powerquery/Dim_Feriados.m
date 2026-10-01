// =====================================================================================================================
// Dim_Feriados.m  —  feriados nacionais que não são dia útil para a venda interna no 4T26. Habilitar carga.
// Usada por Dim_Calendario[EhDiaUtil]. De 01 a 22/09/2026 há 16 dias de semana − 1 feriado (07/09, segunda) = 15 dias úteis, a base do baseline. Conferir com o calendário da área e incluir feriados municipais/pontes se houver.
// =====================================================================================================================
let
    Linhas = {
        {#date(2026, 9, 7),   "Independência do Brasil"},
        {#date(2026, 10, 12), "Nossa Senhora Aparecida"},
        {#date(2026, 11, 2),  "Finados"},
        {#date(2026, 11, 20), "Consciência Negra"},
        {#date(2026, 12, 25), "Natal"}
    },
    Tabela = Table.FromRows(Linhas, type table [Data = date, Feriado = text])
in
    Tabela
