// =====================================================================================================================
// Textos_Restrito.m  —  textos livres do Aletheia/GPT para coaching (v1.1). NÃO entra no modelo da empresa toda.
//
// POR QUÊ: os resumos e trechos citam nome de vendedor (46% dos resumos trazem o primeiro nome) e podem trazer nome e telefone de
// contato do cliente. Em PJ isso ainda é dado pessoal do interlocutor (LGPD). Por isso ficam numa tabela separada, que só deve ser
// carregada no modelo/relatório de gestão com RLS, e nunca no relatório publicado para a empresa.
// Mascaramento aplicado aqui: nome completo e primeiro nome do VENDEDOR → "[vendedor]". NÃO mascara nome/telefone do cliente;
// o acesso restrito é a proteção. Opção futura: pedir ao time de dados a máscara na origem (pedido novo N2, ver README_BI_v1.md).
// =====================================================================================================================
let
    Fonte   = Table.SelectRows(Ligacoes_Base, each [ForaDVINT] = false and [status] = "Completed"),
    Colunas = {"resumo_analise", "objetivo", "oportunidades", "demanda_venda_eminente", "motivo_nova_visita", "resumo_spin",
               "spin_situacao", "spin_problema", "spin_implicacao", "spin_necessidade_solucao", "evidencia_venda", "p1_trecho_venda",
               "p3_evidencias", "p3_trechos", "p3_outro_descricao", "p5_frase_vendedor", "p5_reacao_cliente", "p5_trecho_challenger"},
    Pedaco  = Table.SelectColumns(Fonte, {"id_transcricao", "CARTEIRA", "nome_createdby"} & Colunas),
    Mascara = (texto as any, nome as any) as any =>
        if texto = null or nome = null then texto
        else
            let
                t0 = Text.From(texto),
                completo = Text.Trim(Text.From(nome)),
                primeiro = Text.BeforeDelimiter(completo & " ", " "),
                t1 = Text.Replace(t0, completo, "[vendedor]"),
                t2 = if Text.Length(primeiro) >= 3 then Text.Replace(t1, primeiro, "[vendedor]") else t1
            in t2,
    Mascarada = List.Accumulate(
        Colunas, Pedaco,
        (estado, col) => Table.AddColumn(estado, "__tmp_" & col, each Mascara(Record.Field(_, col), [nome_createdby]))
    ),
    // troca cada coluna original pela mascarada e remove o nome do vendedor
    Substituida = List.Accumulate(
        Colunas, Mascarada,
        (estado, col) => Table.RenameColumns(Table.RemoveColumns(estado, {col}), {{"__tmp_" & col, col}})
    ),
    SemNome = Table.RemoveColumns(Substituida, {"nome_createdby"})
in
    SemNome
