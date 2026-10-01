// =====================================================================================================================
// Fato_Ligacoes.m  —  tabela fato do BI (UMA linha por tentativa de ligação). Habilitar carga.
//
// Fonte: Ligacoes_Base (staging). Aqui ficam os filtros, as colunas derivadas e a lista de colunas que vão para o modelo.
//
// REGRAS QUE ESTA CONSULTA MATERIALIZA (cada uma é uma coluna; as medidas DAX só somam/contam):
//   EhGPT, TemProblema, EhOperacional, EhNegociacao, GrupoTempo, BaseKPI, BaseGemini ... ver bloco "Derivadas".
//
// CORREÇÕES DA CONSULTA ORIGINAL (ids do relatório de auditoria, AUDITORIA_DADOS_E_OPORTUNIDADES.md):
//   M-01  Completed SEM análise Gemini deixa de ser DETRATORA: vira "SEM ANALISE" (657 ligações = 26% das 2.511 "detratoras")
//   M-02  `Chave` (carteira + mês, sem ano) é mantida só por compatibilidade; o BI usa `ChaveAnoMes` (carteira + AAAAMM)
//   M-03  ramo morto da regra removido (ndv>=8 & A=0 é impossível porque A já inclui ndv>=8); resultado idêntico ao original
//   M-04  A (demanda de venda) usa só campos vivos (S, nota_demanda_venda, oportunidades); sem nota_demanda_atendimento
//   M-06  data/hora em horário de Brasília por parâmetro (pFusoHoras); no CSV de setembro nenhuma data muda (0 de 19.078)
//   M-09  IGNORAR deixa de misturar dois motivos: IGNORAR (não concluída) e SECRETARIA (secretária eletrônica)
//   M-10  filtros sem efeito (tipo_interacao, "Not Started") ficam como salvaguarda, sem alterar linhas hoje
//   Privacidade  textos livres (resumos, trechos, frases) NÃO vêm para esta tabela: ficam em Textos_Restrito.
//
// RECONCILIAÇÃO com a consulta original (setembro): POSITIVA 2.015 = 2.015 · INFORMATIVA 1.652 = 1.652 ·
// DETRATORA 2.511 = 1.854 DETRATORA + 657 SEM ANALISE · IGNORAR 12.900 = 12.582 IGNORAR + 318 SECRETARIA.
// =====================================================================================================================
let
    Fonte = Ligacoes_Base,

    // ---- listas de domínio (única definição; K1 = carga operacional completa) --------------------------------------
    OPERACIONAIS   = {"suporte_operacional", "supporte_operacional", "cobranca", "pos_venda_manutencao",
                      "pos_venda_sinistro", "duvida_contrato"},   // "supporte_" é erro de digitação do classificador (1 linha); mantido
    NEGOCIACAO     = {"nova_venda", "upsell", "renovacao", "retencao", "misto"},
    RELACIONAMENTO = {"relacionamento_sem_demanda", "onboarding"},

    // ---- filtros (salvaguardas; ver M-07: as contagens descartadas aparecem em Diagnostico_Pipeline) --------------
    SoDVINT      = Table.SelectRows(Fonte, each [ForaDVINT] = false),
    SemNaoIniciada = Table.SelectRows(SoDVINT, each [status] <> "Not Started"),

    // ---- data e hora (M-06) -------------------------------------------------------------------------------------
    DataHora = Table.AddColumn(
        SemNaoIniciada, "DataHora",
        each try DateTime.From([data_visita_ev]) + #duration(0, pFusoHoras, 0, 0) otherwise null,
        type nullable datetime
    ),
    Data = Table.AddColumn(DataHora, "Data", each if [DataHora] = null then null else Date.From([DataHora]), type nullable date),
    Hora = Table.AddColumn(Data, "Hora", each if [DataHora] = null then null else Time.Hour(DateTime.Time([DataHora])), Int64.Type),
    DiaSemanaNum = Table.AddColumn(Hora, "DiaSemanaNum", each if [Data] = null then null else Date.DayOfWeek([Data], Day.Monday) + 1, Int64.Type),   // 1 = segunda … 7 = domingo
    SemanaInicio = Table.AddColumn(DiaSemanaNum, "SemanaInicio", each if [Data] = null then null else Date.StartOfWeek([Data], Day.Monday), type nullable date),

    // ---- chaves ---------------------------------------------------------------------------------------------------
    Chave = Table.AddColumn(
        SemanaInicio, "Chave",   // legado: carteira + mês SEM ano (M-02). Não usar em relacionamentos novos.
        each if [CARTEIRA] <> null and [Data] <> null then Text.From([CARTEIRA]) & Text.PadStart(Text.From(Date.Month([Data])), 2, "0") else null,
        type nullable text
    ),
    ChaveAnoMes = Table.AddColumn(
        Chave, "ChaveAnoMes",
        each if [CARTEIRA] <> null and [Data] <> null then Text.From([CARTEIRA]) & Text.From(Date.Year([Data]) * 100 + Date.Month([Data])) else null,
        type nullable text
    ),
    // codigo_cliente perde o zero à esquerda na origem (19,3% com menos de 8 dígitos): normaliza para 8 posições
    CodigoCliente8 = Table.AddColumn(
        ChaveAnoMes, "CodigoCliente8",
        each if [codigo_cliente] = null or Text.Trim(Text.From([codigo_cliente])) = "" then null else Text.PadStart(Text.Trim(Text.From([codigo_cliente])), 8, "0"),
        type nullable text
    ),

    // ---- duração ----------------------------------------------------------------------------------------------------
    DuracaoSeg = Table.AddColumn(
        CodigoCliente8, "DuracaoSeg",
        each try Number.From([CallDurationInSeconds]) otherwise null,
        type nullable number
    ),
    FaixaDuracao = Table.AddColumn(
        DuracaoSeg, "FaixaDuracao",
        each let d = [DuracaoSeg] in
             if d = null then null
             else if d <= 120 then "< 2 min"
             else if d <= 300 then "2–5 min"
             else if d <= 480 then "5–8 min"
             else if d <= 720 then "8–12 min"
             else "> 12 min",
        type nullable text
    ),

    // ---- classificação POSITIVA/INFORMATIVA/DETRATORA corrigida (M-01, M-03, M-04, M-09) -----------------------------
    // A coluna original continua disponível como Classe_Legada para a reconciliação dos primeiros dias.
    ClasseLegada = Table.AddColumn(
        FaixaDuracao, "Classe_Legada",
        each
            if [status] <> "Completed" or ([tipo_interacao] <> "Remota - Procurei o cliente" and [tipo_interacao] <> "Remota - O cliente nos procurou") then "IGNORAR"
            else let
                R   = if [objetivo_atingido] = true then 1 else 0,
                S   = if [demanda_venda_eminente_boleano] = true then 1 else 0,
                ndv = [nota_demanda_venda],
                A   = if [demanda_venda_eminente_boleano] = true
                         or ([necessidade_nova_visita_boleano] = true and ndv <> null and ndv >= 8)
                         or (ndv <> null and ndv >= 8)
                         or ([oportunidades_boleano] = true and [nota_oportunidades] <> null and [nota_oportunidades] >= 7)
                      then 1 else 0,
                decisor = if [falou_tomador_decisao] = true then 1 else 0
            in
                if [falou_secretaria_eletronica] = true then "IGNORAR"
                else if R = 1 and (A = 1 or S = 1) then "POSITIVA"
                else if R = 1 and A = 0 then "INFORMATIVA"
                else if R = 0 or (ndv <> null and ndv >= 8 and A = 0 and decisor = 0) then "DETRATORA"
                else "INFORMATIVA",
        type text
    ),
    ClasseLigacao = Table.AddColumn(
        ClasseLegada, "ClasseLigacao",
        each
            if [status] <> "Completed" or ([tipo_interacao] <> "Remota - Procurei o cliente" and [tipo_interacao] <> "Remota - O cliente nos procurou") then "IGNORAR"
            else if [falou_secretaria_eletronica] = true then "SECRETARIA"
            else if [resumo_analise] = null then "SEM ANALISE"   // M-01: antes caía em DETRATORA porque os booleanos nulos viravam R = 0
            else let
                R = [objetivo_atingido] = true,
                ndv = [nota_demanda_venda],
                A = [demanda_venda_eminente_boleano] = true
                    or (ndv <> null and ndv >= 8)
                    or ([oportunidades_boleano] = true and [nota_oportunidades] <> null and [nota_oportunidades] >= 7)
            in
                if R and A then "POSITIVA" else if R then "INFORMATIVA" else "DETRATORA",
        type text
    ),

    // ---- Derivadas: tudo que as medidas DAX precisam (booleanos explícitos, sem null) --------------------------------
    EhCompleted = Table.AddColumn(ClasseLigacao, "EhCompleted", each [status] = "Completed", type logical),
    EhGPT       = Table.AddColumn(EhCompleted, "EhGPT", each [fonte_classificacao] = "gpt", type logical),
    TemProblema = Table.AddColumn(EhGPT, "TemProblema", each [tem_problema] = "SIM", type logical),
    EhOperacional = Table.AddColumn(
        TemProblema, "EhOperacional",   // K1: problema OU suporte/cobrança/pós-venda/dúvida de contrato
        each [TemProblema] or List.Contains(OPERACIONAIS, [p2_tipo]), type logical
    ),
    EhTipoNegociacao = Table.AddColumn(
        EhOperacional, "EhTipoNegociacao",  // tipo da conversa é de negociação, COM ou SEM problema (base da análise de tempo por faixa)
        each List.Contains(NEGOCIACAO, [p2_tipo]), type logical
    ),
    EhNegociacao = Table.AddColumn(
        EhTipoNegociacao, "EhNegociacao",   // K7: negociação SEM problema (nova venda, upsell, renovação, retenção, misto)
        each [EhTipoNegociacao] and not [EhOperacional], type logical
    ),
    GrupoTempo = Table.AddColumn(
        EhNegociacao, "GrupoTempo",
        each
            if not [EhGPT] then "Não classificado (GPT)"
            else if [TemProblema] then "Operacional — com problema"
            else if List.Contains(OPERACIONAIS, [p2_tipo]) then "Operacional — sem problema"
            else if List.Contains(NEGOCIACAO, [p2_tipo]) then "Negociação"
            else if List.Contains(RELACIONAMENTO, [p2_tipo]) then "Relacionamento"
            else if [p2_tipo] = "sem_conteudo" then "Sem conteúdo"
            else "Outro",
        type text
    ),
    BaseKPI = Table.AddColumn(
        GrupoTempo, "BaseKPI",          // base do K1/K7: classificada pelo GPT e com duração informada
        each [EhGPT] and [DuracaoSeg] <> null, type logical
    ),
    TemAnaliseGemini = Table.AddColumn(BaseKPI, "TemAnaliseGemini", each [resumo_analise] <> null, type logical),
    BaseGemini = Table.AddColumn(
        TemAnaliseGemini, "BaseGemini", // base do K1 pela régua Gemini (categoria_principal = Suporte)
        each [EhCompleted] and [DuracaoSeg] <> null and [TemAnaliseGemini], type logical
    ),
    Pendencia = Table.AddColumn(
        BaseGemini, "Pendencia",        // K2: problema não resolvido na ligação (resolução ≠ SIM)
        each [TemProblema] and [p3_foi_resolvido_na_ligacao] <> "SIM", type logical
    ),
    Fechou = Table.AddColumn(
        Pendencia, "Fechou",            // GPT: fechou_novo / fechou_renovacao / fechou_upsell
        each [p1_desfecho] <> null and Text.StartsWith([p1_desfecho], "fechou"), type logical
    ),
    FechouOuVenda = Table.AddColumn(
        Fechou, "FechouOuVenda",        // união GPT + Gemini (`venda`): kappa entre as duas réguas é só 0,46, então mostramos a união
        each [Fechou] or (try Text.Lower(Text.From([venda])) = "true" otherwise false), type logical
    ),
    TeveChallenger = Table.AddColumn(FechouOuVenda, "TeveChallenger", each [p5_teve_challenger] = "SIM", type logical),
    TrouxeDado = Table.AddColumn(TeveChallenger, "TrouxeDado", each [p5_trouxe_dado] = "SIM", type logical),
    ConectouSituacao = Table.AddColumn(TrouxeDado, "ConectouSituacao", each [p5_conectou_situacao] = "SIM", type logical),
    ClienteReagiu = Table.AddColumn(ConectouSituacao, "ClienteReagiu", each [p5_cliente_reagiu] = "SIM", type logical),
    DataSugerida = Table.AddColumn(
        ClienteReagiu, "DataSugerida",  // vem como texto dd/MM/aaaa ou "sem dados necessários"
        each try Date.FromText(Text.From([data_sugerida_nova_visita]), [Format = "dd/MM/yyyy", Culture = "pt-BR"]) otherwise null,
        type nullable date
    ),

    // ---- colunas que vão para o modelo (sem texto livre, sem as 8 colunas "não usar" da auditoria) ----------------------
    Selecionadas = Table.SelectColumns(DataSugerida, {
        // chaves e tempo
        "id_transcricao", "segment_id", "DataHora", "Data", "Hora", "DiaSemanaNum", "SemanaInicio",
        // carteira e cliente
        "CARTEIRA", "Chave", "ChaveAnoMes", "CodigoCliente8",
        // telefonia
        "status", "tipo_ligacao", "DuracaoSeg", "FaixaDuracao", "EhCompleted",
        // classificação e bases
        "ClasseLigacao", "Classe_Legada", "EhGPT", "BaseKPI", "TemAnaliseGemini", "BaseGemini",
        // GPT venda / problema / Challenger
        "fonte_classificacao", "era_venda", "p1_desfecho", "p2_tipo", "p1_tentativa_comercial",
        "tem_problema", "p3_problema_principal", "p3_foi_resolvido_na_ligacao",
        "p5_teve_challenger", "p5_codigos_challenger", "p5_qualidade",
        // derivadas
        "TemProblema", "EhOperacional", "EhTipoNegociacao", "EhNegociacao", "GrupoTempo", "Pendencia", "Fechou", "FechouOuVenda",
        "TeveChallenger", "TrouxeDado", "ConectouSituacao", "ClienteReagiu",
        // Gemini (só campos estruturados)
        "objetivo_atingido", "oportunidades_boleano", "nota_oportunidades", "demanda_venda_eminente_boleano", "nota_demanda_venda",
        "necessidade_nova_visita_boleano", "urgencia_nova_visita", "DataSugerida", "falou_tomador_decisao", "falou_secretaria_eletronica",
        "nota_spin_situacao", "nota_spin_problema", "nota_spin_implicacao", "nota_spin_necessidade_solucao", "nota_final_spin",
        "categoria_principal", "score_consultivo", "score_tentativa_de_contato_comercial", "score_suporte", "score_comercial"
    }),

    // ---- tipos -------------------------------------------------------------------------------------------------------
    Tipado = Table.TransformColumnTypes(Selecionadas, {
        {"Hora", Int64.Type}, {"DiaSemanaNum", Int64.Type},
        {"nota_oportunidades", type nullable number}, {"nota_demanda_venda", type nullable number}, {"urgencia_nova_visita", type nullable number},
        {"nota_spin_situacao", type nullable number}, {"nota_spin_problema", type nullable number}, {"nota_spin_implicacao", type nullable number},
        {"nota_spin_necessidade_solucao", type nullable number}, {"nota_final_spin", type nullable number},
        {"score_consultivo", type nullable number}, {"score_tentativa_de_contato_comercial", type nullable number},
        {"score_suporte", type nullable number}, {"score_comercial", type nullable number}
    })
in
    Tipado
