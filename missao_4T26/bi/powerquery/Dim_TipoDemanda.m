// =====================================================================================================================
// Dim_TipoDemanda.m  —  de-para de p2_tipo (GPT) para o grupo de tempo do K1/K7. Habilitar carga.
// Relacionamento: Dim_TipoDemanda[p2_tipo] 1 → * Fato_Ligacoes[p2_tipo]
// Esta tabela é a definição OFICIAL de "carga operacional completa" (decisão da missão): tudo que não é negociação.
// Obs.: o grupo da ligação com problema depende de tem_problema (coluna GrupoTempo da Fato); aqui é só o tipo.
// =====================================================================================================================
let
    Linhas = {
        {"nova_venda",                 "Nova venda",                  "Negociação",     1},
        {"upsell",                     "Upsell",                      "Negociação",     2},
        {"renovacao",                  "Renovação",                   "Negociação",     3},
        {"retencao",                   "Retenção",                    "Negociação",     4},
        {"misto",                      "Misto (venda + operação)",    "Negociação",     5},
        {"suporte_operacional",        "Suporte operacional",         "Operacional",    6},
        {"supporte_operacional",       "Suporte operacional (grafia)","Operacional",    6},
        {"cobranca",                   "Cobrança",                    "Operacional",    7},
        {"pos_venda_manutencao",       "Pós-venda: manutenção",       "Operacional",    8},
        {"pos_venda_sinistro",         "Pós-venda: sinistro",         "Operacional",    9},
        {"duvida_contrato",            "Dúvida de contrato",          "Operacional",   10},
        {"relacionamento_sem_demanda", "Relacionamento sem demanda",  "Relacionamento",11},
        {"onboarding",                 "Onboarding",                  "Relacionamento",12},
        {"sem_conteudo",               "Sem conteúdo",                "Sem conteúdo",  13}
    },
    Tabela = Table.FromRows(Linhas, {"p2_tipo", "Descricao", "GrupoCarga", "Ordem"}),
    Tipado = Table.TransformColumnTypes(Tabela, {{"p2_tipo", type text}, {"Descricao", type text}, {"GrupoCarga", type text}, {"Ordem", Int64.Type}})
in
    Tipado
