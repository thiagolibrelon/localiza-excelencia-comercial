// =====================================================================================================================
// Atualizacao.m  —  carimbo da última atualização do modelo (horário de Brasília). Habilitar carga.
// Alimenta C3 (latência) e o texto "Dados até … · atualizado em …" do cabeçalho de todas as páginas.
// =====================================================================================================================
let
    Agora = DateTime.From(DateTimeZone.SwitchZone(DateTimeZone.UtcNow(), -3)),
    Tabela = #table(type table [Quando = datetime], {{Agora}})
in
    Tabela
