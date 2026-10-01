// =====================================================================================================================
// Dicionario_Colunas.m  —  perfil das 88 colunas do CSV de setembro (bloco, preenchimento, valor-sentinela, uso recomendado). Página 8.
// Origem: missao_4T26/anexos/dicionario_dados_setembro.csv (gerado por scripts/auditoria_dados_missao.py). Tabela ESTÁTICA: atualizar
// quando o dicionário for regerado. Apontar o caminho para onde o arquivo estiver (SharePoint/OneDrive ou pasta de rede).
// =====================================================================================================================
let
    Caminho = "C:\caminho\para\dicionario_dados_setembro.csv",
    Fonte   = Csv.Document(File.Contents(Caminho), [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Cabec   = Table.PromoteHeaders(Fonte, [PromoteAllScalars = true]),
    Tipado  = Table.TransformColumnTypes(Cabec, {{"pct_do_total", type number}, {"pct_da_base", type number}, {"pct_sentinela", type number}}, "en-US")
in
    Tipado
