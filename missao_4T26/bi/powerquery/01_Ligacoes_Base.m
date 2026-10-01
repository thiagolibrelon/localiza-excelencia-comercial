// =====================================================================================================================
// 01_Ligacoes_Base.m  —  consulta de STAGING (desmarcar "Habilitar carga": ela não vai para o modelo)
//
// É a consulta original ("Consulta Power Bi") com o SQL parametrizado e SEM nenhum filtro de linha, só junções.
// Quem filtra e calcula é a `Fato_Ligacoes`. Assim a página "Qualidade do dado" (consulta `Diagnostico_Pipeline`)
// enxerga as linhas que o pipeline descartaria (fora do DVINT, sem carteira, "Not Started") em vez de escondê-las (M-07).
//
// Dependências (já existentes no seu arquivo): F_Carteiras_Equipe, Tempo_de_ligação, Ligações Classificadas.
// Parâmetros: pInclusaoDesde.
//
// O QUE MUDOU EM RELAÇÃO À CONSULTA ORIGINAL
//   M-05  data de corte do SQL virou o parâmetro pInclusaoDesde (antes: '2026-09-01' escrito dentro do texto)
//   M-07  nenhum filtro aqui; `ForaDVINT` e `SemCarteira` viram colunas para o diagnóstico
//   M-10  o filtro `status <> "Not Started"` e o teste de tipo_interacao foram para a Fato (aqui só marcamos)
//   O restante do SQL é idêntico ao original (mesmas 4 tabelas, mesmas colunas, mesmas junções).
// =====================================================================================================================
let
    ConsultaSQL =
        "WITH meta AS (
          SELECT
            CAST(call_object AS STRING) AS call_object_str,
            ARRAY_AGG(
              segment_id
              ORDER BY segment_id
              LIMIT 1
            )[OFFSET(0)] AS segment_id
          FROM `lclz-dados.rac_negociacao.fll_rac_corp_transcricoes_metadata`
          GROUP BY call_object_str
        )

        SELECT
          vis.id_transcricao,
          vis.data_visita_ev,
          vis.status,
          vis.tipo_ligacao,
          vis.tipo_interacao,
          vis.matricula_ev_createdby,
          vis.nome_createdby,
          vis.codigo_cliente,
          meta.segment_id,

          analise.resumo AS resumo_analise,
          analise.objetivo,
          analise.objetivo_atingido,
          analise.oportunidades,
          analise.oportunidades_boleano,
          analise.nota_oportunidades,
          analise.demanda_venda_eminente,
          analise.demanda_venda_eminente_boleano,
          analise.nota_demanda_venda,
          analise.venda,
          analise.demanda_de_atendimento,
          analise.demanda_de_atendimento_boleano,
          analise.nota_demanda_atendimento,
          analise.necessidade_nova_visita,
          analise.necessidade_nova_visita_boleano,
          analise.urgencia_nova_visita,
          analise.motivo_nova_visita,
          analise.data_sugerida_nova_visita,
          analise.falou_tomador_decisao,
          analise.falou_secretaria_eletronica,
          analise.frota_propria,
          analise.frota_propria_boleano,
          analise.volume_frota_propria,
          analise.aluguel_concorrencia,
          analise.aluguel_concorrencia_boleano,
          analise.volume_aluguel_concorrencia,
          analise.matricula_ev,
          analise.codigo_cliente AS codigo_cliente_analise,

          spin.resumo AS resumo_spin,
          spin.spin_situacao,
          spin.nota_spin_situacao,
          spin.spin_problema,
          spin.nota_spin_problema,
          spin.spin_implicacao,
          spin.nota_spin_implicacao,
          spin.spin_necessidade_solucao,
          spin.nota_spin_necessidade_solucao,
          spin.nota_final_spin,

          categ.categoria_principal,
          categ.score_consultivo,
          categ.score_tentativa_de_contato_comercial,
          categ.score_suporte,
          categ.score_comercial

        FROM `lclz-dados.rac_negociacao.fll_rac_corp_transcricoes_visitas_internas` vis

        LEFT JOIN meta
          ON CAST(vis.objeto_ligacao AS STRING) = meta.call_object_str

        LEFT JOIN `lclz-dados.rac_negociacao.fll_rac_corp_transcricoes_analise_llm` analise
          ON meta.segment_id = analise.segment_id

        LEFT JOIN `lclz-dados.rac_negociacao.fll_rac_corp_transcricoes_analise_spinselling_llm` spin
          ON meta.segment_id = spin.segment_id

        LEFT JOIN `lclz-dados.rac_negociacao.fll_rac_corp_transcricoes_analise_categorizacao_llm` categ
          ON meta.segment_id = categ.segment_id

        WHERE DATE(vis.DATA_INCLUSAO_REGISTRO) >= '"
        & Date.ToText(pInclusaoDesde, [Format = "yyyy-MM-dd", Culture = "en-US"])
        & "'",

    Fonte = Odbc.Query(
        "dsn=lclz-dados",
        ConsultaSQL,
        [CommandTimeout = #duration(0, 0, 30, 0)]
    ),

    // ---- carteira / distrital / divisional (junção à esquerda: nada some aqui) ------------------------------------
    JuncaoCarteira = Table.NestedJoin(
        Fonte, {"matricula_ev_createdby"},
        F_Carteiras_Equipe, {"MATRICULA"},
        "F_Carteiras_Equipe", JoinKind.LeftOuter
    ),
    CarteiraExpandida = Table.ExpandTableColumn(
        JuncaoCarteira, "F_Carteiras_Equipe",
        {"DIVISIONAL", "DISTRITAL", "CARTEIRA"}, {"DIVISIONAL", "DISTRITAL", "CARTEIRA"}
    ),

    // ---- duração (tabela Tempo_de_ligação, chave = id_transcricao) --------------------------------------------------
    JuncaoDuracao = Table.NestedJoin(
        CarteiraExpandida, {"id_transcricao"},
        Tempo_de_ligação, {"Id"},
        "Tempo_de_ligação", JoinKind.LeftOuter
    ),
    DuracaoExpandida = Table.ExpandTableColumn(
        JuncaoDuracao, "Tempo_de_ligação",
        {"CallDurationInSeconds"}, {"CallDurationInSeconds"}
    ),

    // ---- classificador GPT (tabela Ligações Classificadas, chave = segment_id) --------------------------------------
    ColunasGPT = {
        "cd_segmento", "fonte_classificacao", "era_venda", "p1_desfecho", "p2_tipo", "p1_tentativa_comercial",
        "evidencia_venda", "p1_trecho_venda", "tem_problema", "p3_problemas_identificados", "p3_problema_principal",
        "p3_foi_resolvido_na_ligacao", "p3_evidencias", "p3_trechos", "p3_trechos_status", "p3_outro_descricao",
        "p5_teve_challenger", "p5_codigos_challenger", "p5_qualidade", "p5_trouxe_dado", "p5_conectou_situacao",
        "p5_cliente_reagiu", "p5_frase_vendedor", "p5_reacao_cliente", "p5_challenger_sem_dado", "p5_trecho_challenger",
        "p5_trecho_status", "p1_desfecho_original", "p2_tipo_original"
    },
    JuncaoGPT = Table.NestedJoin(
        DuracaoExpandida, {"segment_id"},
        #"Ligações Classificadas", {"cd_segmento"},
        "Ligações Classificadas", JoinKind.LeftOuter
    ),
    GPTExpandido = Table.ExpandTableColumn(JuncaoGPT, "Ligações Classificadas", ColunasGPT, ColunasGPT),

    // ---- marcações para o diagnóstico (sem remover linha) -----------------------------------------------------------
    ForaDVINT = Table.AddColumn(GPTExpandido, "ForaDVINT", each [DIVISIONAL] <> "DVINT", type logical),
    SemCarteira = Table.AddColumn(ForaDVINT, "SemCarteira", each [CARTEIRA] = null, type logical)
in
    SemCarteira
