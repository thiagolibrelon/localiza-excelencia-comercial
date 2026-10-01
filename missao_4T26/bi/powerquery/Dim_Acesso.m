// =====================================================================================================================
// Dim_Acesso.m  —  lista de acesso do RLS (ver ../dax/rls.dax). Substituir a origem pela lista real; o formato é o que importa.
// Colunas: Email (o mesmo UPN do Power BI Service) · Papel (Gestao | Distrital | Carteira) · DISTRITAL · CARTEIRA.
// Mantida pela Excelência Comercial; desabilitar "Incluir no relatório" não é necessário, mas ocultar a tabela sim.
// =====================================================================================================================
let
    // Exemplo com Excel no SharePoint: Excel.Workbook(Web.Contents("https://SUA-EMPRESA.sharepoint.com/.../Acesso_BI_Excelencia.xlsx"), null, true){[Item="Acesso", Kind="Table"]}[Data]
    Fonte = #table(
        type table [Email = text, Papel = text, DISTRITAL = text, CARTEIRA = text],
        {
            {"exemplo.gestor@empresa.com.br",   "Gestao",    null,    null},
            {"exemplo.distrital@empresa.com.br", "Distrital", "DTIN1", null},
            {"exemplo.vendedor@empresa.com.br",  "Carteira",  null,    "COI01A"}
        }
    )
in
    Fonte
