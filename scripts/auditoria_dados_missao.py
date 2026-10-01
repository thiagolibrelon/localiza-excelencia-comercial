"""Auditoria da missao 4T26 usando SOMENTE o CSV da consulta do Power BI (e a logica do codigo M que o gerou).
Nada do repositorio (junho, julho, diarias, exemplos) e usado. Reproduz os numeros de
missao_4T26/AUDITORIA_DADOS_E_OPORTUNIDADES.md.

COMO USAR:
  python auditoria_dados_missao.py "Consulta Power Bi - Copia.csv" [--saida missao_4T26/anexos]

Escreve (so agregados e metadados; sem nome de vendedor, sem cliente, sem trecho de transcricao):
  dicionario_dados_setembro.csv   perfil das 88 colunas (bloco, preenchimento, dominio, saturacao, uso recomendado)
  serie_diaria_set_2026.csv       assinatura diaria do classificador GPT (para enxergar mudanca de versao)
  carteira_set_2026.csv           metricas por carteira (>= 40 ligacoes classificadas ate 22/09)
  tempo_otimo_set_2026.csv        faixas de duracao x resultado em ligacoes de negociacao
Convencoes: horario do CSV em UTC (corrigido -3h para BRT); booleanos VERDADEIRO/FALSO; codigo_cliente com 8 digitos;
duracao so existe para Completed ate 22/09.
"""
import argparse
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
OPERACIONAIS = ["suporte_operacional", "supporte_operacional", "cobranca", "pos_venda_manutencao",
                "pos_venda_sinistro", "duvida_contrato"]
NEGOCIACAO = ["nova_venda", "upsell", "renovacao", "retencao", "misto"]
FIM_DURACAO = "2026-09-22"
SENTINELAS = {"sem dados necessários", "nenhum", "Sem Classificação", "nao_aplicavel", "NENHUM"}

BLOCOS = {
    "A. Identificadores e chaves": ["id_transcricao", "segment_id", "cd_segmento", "codigo_cliente", "codigo_cliente_analise",
                                    "matricula_ev_createdby", "matricula_ev", "nome_createdby"],
    "B. CRM e telefonia": ["data_visita_ev", "status", "tipo_ligacao", "tipo_interacao", "DIVISIONAL", "DISTRITAL", "CARTEIRA",
                           "Data", "Chave", "CallDurationInSeconds"],
    "C. Regra do Power Query": ["Classificação tipo de ligação"],
    "D. Aletheia (Gemini) — análise da ligação": [
        "resumo_analise", "objetivo", "objetivo_atingido", "oportunidades", "oportunidades_boleano", "nota_oportunidades",
        "demanda_venda_eminente", "demanda_venda_eminente_boleano", "nota_demanda_venda", "venda", "demanda_de_atendimento",
        "demanda_de_atendimento_boleano", "nota_demanda_atendimento", "necessidade_nova_visita", "necessidade_nova_visita_boleano",
        "urgencia_nova_visita", "motivo_nova_visita", "data_sugerida_nova_visita", "falou_tomador_decisao",
        "falou_secretaria_eletronica", "frota_propria", "frota_propria_boleano", "volume_frota_propria", "aluguel_concorrencia",
        "aluguel_concorrencia_boleano", "volume_aluguel_concorrencia"],
    "E. Aletheia (Gemini) — SPIN Selling": ["resumo_spin", "spin_situacao", "nota_spin_situacao", "spin_problema", "nota_spin_problema",
                                            "spin_implicacao", "nota_spin_implicacao", "spin_necessidade_solucao",
                                            "nota_spin_necessidade_solucao", "nota_final_spin"],
    "F. Aletheia (Gemini) — categorização": ["categoria_principal", "score_consultivo", "score_tentativa_de_contato_comercial",
                                             "score_suporte", "score_comercial"],
    "G. Classificador GPT — venda": ["fonte_classificacao", "era_venda", "p1_desfecho", "p2_tipo", "p1_tentativa_comercial",
                                     "evidencia_venda", "p1_trecho_venda", "p1_desfecho_original", "p2_tipo_original"],
    "H. Classificador GPT — problemas": ["tem_problema", "p3_problemas_identificados", "p3_problema_principal",
                                         "p3_foi_resolvido_na_ligacao", "p3_evidencias", "p3_trechos", "p3_trechos_status",
                                         "p3_outro_descricao"],
    "I. Classificador GPT — Challenger": ["p5_teve_challenger", "p5_codigos_challenger", "p5_qualidade", "p5_trouxe_dado",
                                          "p5_conectou_situacao", "p5_cliente_reagiu", "p5_frase_vendedor", "p5_reacao_cliente",
                                          "p5_challenger_sem_dado", "p5_trecho_challenger", "p5_trecho_status"],
}
# descricao inferida do nome e dos valores (o CSV nao traz dicionario)
DESC = {
    "id_transcricao": "ID da ligação no CRM (chave da junção com Tempo_de_ligação)", "segment_id": "ID do segmento de transcrição (chave das tabelas Aletheia)",
    "cd_segmento": "Mesmo ID, vindo da tabela Ligações Classificadas", "codigo_cliente": "Código do cliente (perde zero à esquerda)",
    "codigo_cliente_analise": "Código do cliente dentro da tabela de análise", "matricula_ev_createdby": "Matrícula do vendedor que registrou",
    "matricula_ev": "Matrícula do vendedor na análise", "nome_createdby": "Nome do vendedor",
    "data_visita_ev": "Data e hora da ligação (serial Excel, UTC)", "status": "Status no CRM (Completed, Sem Sucesso, Open)",
    "tipo_ligacao": "Inbound ou Outbound", "tipo_interacao": "Remota: procurei o cliente / cliente nos procurou", "DIVISIONAL": "Divisional (filtro DVINT)",
    "DISTRITAL": "Distrital (DTIN1–5)", "CARTEIRA": "Carteira do vendedor", "Data": "Dia da ligação derivado no Power Query",
    "Chave": "Carteira + número do mês (chave para metas)", "CallDurationInSeconds": "Duração da ligação em segundos (tabela Tempo_de_ligação)",
    "Classificação tipo de ligação": "POSITIVA / INFORMATIVA / DETRATORA / IGNORAR (regra do Power Query)",
    "resumo_analise": "Resumo narrativo da ligação", "objetivo": "Objetivo da ligação (texto)", "objetivo_atingido": "Objetivo foi atingido?",
    "oportunidades": "Oportunidades identificadas (texto)", "oportunidades_boleano": "Há oportunidade?", "nota_oportunidades": "Nota da oportunidade (0–10)",
    "demanda_venda_eminente": "Demanda de venda iminente (texto)", "demanda_venda_eminente_boleano": "Há demanda de venda iminente?",
    "nota_demanda_venda": "Nota da demanda de venda (0–10)", "venda": "Venda realizada na ligação?", "demanda_de_atendimento": "Demanda de atendimento (texto)",
    "demanda_de_atendimento_boleano": "Há demanda de atendimento?", "nota_demanda_atendimento": "Nota da demanda de atendimento",
    "necessidade_nova_visita": "Necessidade de nova visita (texto)", "necessidade_nova_visita_boleano": "Precisa de nova visita?",
    "urgencia_nova_visita": "Urgência da nova visita (1–10)", "motivo_nova_visita": "Motivo da nova visita (texto)",
    "data_sugerida_nova_visita": "Data sugerida para a nova visita (dd/mm/aaaa)", "falou_tomador_decisao": "Falou com o tomador de decisão?",
    "falou_secretaria_eletronica": "Caiu em secretária eletrônica?", "frota_propria": "Frota própria (texto)", "frota_propria_boleano": "Cliente tem frota própria?",
    "volume_frota_propria": "Volume da frota própria", "aluguel_concorrencia": "Aluguel com concorrente (texto)",
    "aluguel_concorrencia_boleano": "Aluga de concorrente?", "volume_aluguel_concorrencia": "Volume alugado do concorrente",
    "resumo_spin": "Resumo da ligação sob a ótica SPIN", "spin_situacao": "Evidência SPIN — Situação (texto)", "nota_spin_situacao": "Nota SPIN Situação (1–5)",
    "spin_problema": "Evidência SPIN — Problema (texto)", "nota_spin_problema": "Nota SPIN Problema (1–5)", "spin_implicacao": "Evidência SPIN — Implicação (texto)",
    "nota_spin_implicacao": "Nota SPIN Implicação (1–5)", "spin_necessidade_solucao": "Evidência SPIN — Necessidade de solução (texto)",
    "nota_spin_necessidade_solucao": "Nota SPIN Necessidade (1–5)", "nota_final_spin": "Nota final SPIN (1–5)",
    "categoria_principal": "Categoria da ligação (Suporte, Comercial, Consultivo, Tentativa de contato comercial)", "score_consultivo": "Score consultivo (0–1)",
    "score_tentativa_de_contato_comercial": "Score de tentativa de contato comercial (0–1)", "score_suporte": "Score de suporte (0–1)",
    "score_comercial": "Score comercial (0–1)", "fonte_classificacao": "Origem da classificação (gpt, auto_curta)", "era_venda": "Era uma ligação de venda?",
    "p1_desfecho": "Desfecho comercial (fechou, interessou, não era venda…)", "p2_tipo": "Tipo da ligação (nova venda, suporte, cobrança…)",
    "p1_tentativa_comercial": "Houve tentativa comercial?", "evidencia_venda": "Evidência da venda (texto curto)", "p1_trecho_venda": "Trecho literal da venda",
    "p1_desfecho_original": "Desfecho original (antes de ajuste de regra)", "p2_tipo_original": "Tipo original (antes de ajuste de regra)",
    "tem_problema": "A ligação tem problema?", "p3_problemas_identificados": "Códigos dos problemas (P1…P15)", "p3_problema_principal": "Problema principal",
    "p3_foi_resolvido_na_ligacao": "Problema resolvido na ligação (SIM, PARCIAL, NAO)", "p3_evidencias": "Evidência do problema (texto)",
    "p3_trechos": "Trecho literal do problema", "p3_trechos_status": "Status da busca do trecho", "p3_outro_descricao": "Descrição quando o problema é \"Outro\"",
    "p5_teve_challenger": "Teve Challenger?", "p5_codigos_challenger": "Códigos Challenger (CH1–CH7)", "p5_qualidade": "Qualidade do Challenger (alta, media, baixa)",
    "p5_trouxe_dado": "Trouxe dado concreto?", "p5_conectou_situacao": "Conectou à situação do cliente?", "p5_cliente_reagiu": "Cliente reagiu?",
    "p5_frase_vendedor": "Frase do vendedor", "p5_reacao_cliente": "Reação do cliente", "p5_challenger_sem_dado": "Challenger sem dado concreto?",
    "p5_trecho_challenger": "Trecho literal do Challenger", "p5_trecho_status": "Status da busca do trecho",
}
# colunas que o perfil automatico nao sabe julgar sozinho
NAO_USAR = {
    "nota_demanda_atendimento": "constante (0 em 100%)", "p2_tipo_original": "1 valor em toda a base", "p1_desfecho_original": "3 valores em toda a base",
    "volume_frota_propria": "95% é 'sem dados necessários'", "volume_aluguel_concorrencia": "99% é 'sem dados necessários'",
    "codigo_cliente_analise": "duplica codigo_cliente", "matricula_ev": "duplica matricula_ev_createdby", "tipo_interacao": "redundante com tipo_ligacao",
}
RESSALVA = {
    "codigo_cliente": "normalizar para 8 dígitos; 7,8% nulos", "data_visita_ev": "UTC: subtrair 3h", "CallDurationInSeconds": "só Completed e só até 22/09",
    "Chave": "linhas de 31/08 recebem mês 08", "Classificação tipo de ligação": "DETRATORA inclui 657 Completed sem análise",
    "oportunidades_boleano": "VERDADEIRO em 92%", "demanda_de_atendimento_boleano": "VERDADEIRO em 81%",
    "necessidade_nova_visita_boleano": "VERDADEIRO em 79%", "venda": "concorda só em parte com p1_desfecho (kappa 0,46)",
    "p1_desfecho": "versão do classificador muda no mês", "p2_tipo": "versão do classificador muda no mês",
    "tem_problema": "taxa 13,6% → 27,4% em 15/09", "p3_problema_principal": "taxa muda em 15/09", "p5_qualidade": "83% 'alta' (sem variância)",
    "categoria_principal": "'Sem Classificação' = ligação sem análise", "resumo_analise": "contém nomes de pessoas",
    "resumo_spin": "contém nomes de pessoas", "status": "613 conversas GPT estão fora de Completed",
}


def num(s):
    return pd.to_numeric(s.astype("string").str.replace(",", "."), errors="coerce")


def carregar(caminho):
    cru = pd.read_csv(caminho, sep=";", encoding="utf-8-sig", dtype=str, low_memory=False).replace("", np.nan)
    s = cru.copy()
    s["ts"] = pd.to_datetime("1899-12-30") + pd.to_timedelta(num(s["data_visita_ev"]), unit="D") - pd.Timedelta(hours=3)
    s["dt"] = s["ts"].dt.normalize()
    s["hora"] = s["ts"].dt.hour
    s["dow"] = s["ts"].dt.dayofweek
    s["dur"] = num(s["CallDurationInSeconds"])
    s["comp"] = s["status"].eq("Completed")
    s["gpt"] = s["fonte_classificacao"].eq("gpt")
    s["prob"] = s["tem_problema"].eq("SIM")
    s["ch"] = s["p5_teve_challenger"].eq("SIM")
    s["fech"] = s["p1_desfecho"].fillna("").str.startswith("fechou")
    s["inter"] = s["p1_desfecho"].eq("interessou_nao_fechou")
    s["op"] = s["prob"] | s["p2_tipo"].isin(OPERACIONAIS)
    s["neg"] = s["p2_tipo"].isin(NEGOCIACAO) & ~s["op"]
    s["cod"] = s["codigo_cliente"].str.strip().str.zfill(8)
    s["sug"] = pd.to_datetime(s["data_sugerida_nova_visita"], format="%d/%m/%Y", errors="coerce")
    for c in ["objetivo_atingido", "demanda_venda_eminente_boleano", "falou_tomador_decisao", "necessidade_nova_visita_boleano",
              "oportunidades_boleano", "demanda_de_atendimento_boleano", "frota_propria_boleano", "aluguel_concorrencia_boleano",
              "falou_secretaria_eletronica"]:
        s[c + "_b"] = s[c].map({"VERDADEIRO": True, "FALSO": False})
    s["venda_b"] = s["venda"].map({"True": True, "False": False})
    for c in ["nota_final_spin", "nota_demanda_venda", "nota_oportunidades", "nota_spin_situacao", "nota_spin_problema",
              "nota_spin_implicacao", "nota_spin_necessidade_solucao", "urgencia_nova_visita"]:
        s[c + "_n"] = num(s[c])
    return cru, s


def titulo(t):
    print(f"\n=== {t} ===")


def dicionario(cru, saida):
    gem = cru["resumo_analise"].notna()
    gpt = cru["fonte_classificacao"].notna()
    bases = {"D": ("com análise Gemini", gem), "E": ("com análise Gemini", gem), "F": ("com análise Gemini", gem),
             "G": ("com classificação GPT", gpt), "H": ("com classificação GPT", gpt), "I": ("com classificação GPT", gpt)}
    finas = {"p3_evidencias": cru["tem_problema"].eq("SIM"), "p3_trechos": cru["tem_problema"].eq("SIM"),
             "p3_trechos_status": cru["tem_problema"].eq("SIM"), "p3_outro_descricao": cru["tem_problema"].eq("SIM"),
             "p5_frase_vendedor": cru["p5_teve_challenger"].eq("SIM"), "p5_reacao_cliente": cru["p5_teve_challenger"].eq("SIM"),
             "p5_trecho_challenger": cru["p5_teve_challenger"].eq("SIM"), "p5_trecho_status": cru["p5_teve_challenger"].eq("SIM"),
             "p1_trecho_venda": cru["era_venda"].eq("SIM"), "evidencia_venda": cru["era_venda"].eq("SIM"),
             "CallDurationInSeconds": cru["status"].eq("Completed")}
    linhas = []
    for bloco, cols in BLOCOS.items():
        for c in cols:
            nome, base = bases.get(bloco[0], ("todas as linhas", pd.Series(True, index=cru.index)))
            if c in finas:
                nome, base = {"CallDurationInSeconds": "Completed"}.get(c, "linhas aplicáveis"), finas[c]
            x = cru[c].dropna()
            n = len(x)
            vc = x.value_counts()
            numerica = pd.to_numeric(x.str.replace(",", "."), errors="coerce")
            eh_num = n > 0 and numerica.notna().mean() > 0.95 and c not in (
                "codigo_cliente", "codigo_cliente_analise", "matricula_ev", "matricula_ev_createdby", "id_transcricao", "segment_id",
                "cd_segmento", "Data", "data_visita_ev", "urgencia_nova_visita")
            topo = vc.index[0] if n else ""
            pct_topo = vc.iloc[0] / n if n else np.nan
            sent = x.isin(SENTINELAS).mean() if n else np.nan
            alertas = []
            if x.nunique() == 1:
                alertas.append("constante")
            elif pct_topo >= 0.9 and x.nunique() <= 12:
                alertas.append("saturado (≥ 90% no mesmo valor)")
            if sent >= 0.2:
                alertas.append("valor-sentinela frequente")
            if (cru[c].notna() & base).sum() / max(base.sum(), 1) < 0.1:
                alertas.append("esparso (< 10% da base aplicável)")
            uso = "Usar"
            if c in NAO_USAR:
                uso = "Não usar"
            elif c in RESSALVA or alertas:
                uso = "Usar com ressalva"
            linhas.append({"bloco": bloco, "coluna": c, "descricao": DESC[c], "base_aplicavel": nome, "linhas_base": int(base.sum()),
                           "preenchido": n, "pct_do_total": n / len(cru), "pct_da_base": (cru[c].notna() & base).sum() / max(base.sum(), 1),
                           "valores_distintos": x.nunique(), "valor_mais_comum": str(topo)[:50], "pct_valor_mais_comum": pct_topo,
                           "pct_sentinela": sent, "minimo": numerica.min() if eh_num else np.nan, "media": numerica.mean() if eh_num else np.nan,
                           "maximo": numerica.max() if eh_num else np.nan, "alerta": "; ".join(alertas),
                           "uso_recomendado": uso, "observacao": NAO_USAR.get(c, RESSALVA.get(c, ""))})
    d = pd.DataFrame(linhas)
    d.round(4).to_csv(saida / "dicionario_dados_setembro.csv", index=False, encoding="utf-8-sig")
    titulo("0. Dicionário das 88 colunas")
    print(d.groupby("bloco").agg(colunas=("coluna", "size"), usar=("uso_recomendado", lambda x: (x == "Usar").sum()),
                                 ressalva=("uso_recomendado", lambda x: (x == "Usar com ressalva").sum()),
                                 nao_usar=("uso_recomendado", lambda x: (x == "Não usar").sum())).to_string())
    print("Total:", d["uso_recomendado"].value_counts().to_dict())


def wilson(k, n, z=1.96):
    if n == 0:
        return np.nan, np.nan
    p = k / n
    d = 1 + z * z / n
    c = p + z * z / (2 * n)
    a = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n))
    return (c - a) / d, (c + a) / d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--saida", default=str(RAIZ / "missao_4T26" / "anexos"))
    a = ap.parse_args()
    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    cru, s = carregar(a.csv)
    g = s[s["gpt"]].copy()
    dicionario(cru, saida)

    titulo("1. Assinatura diária do classificador GPT (mudança de versão)")
    por_dia = s.groupby(s["dt"].dt.date).agg(tentativas=("comp", "size"), completed=("comp", "sum"), classificadas_gpt=("gpt", "sum"),
                                              com_duracao=("dur", "count"))
    gd = g.groupby(g["dt"].dt.date).agg(taxa_problema=("prob", "mean"), taxa_challenger=("ch", "mean"),
                                        taxa_era_venda=("era_venda", lambda x: (x == "SIM").mean()), taxa_fechou=("fech", "mean"))
    por_dia = por_dia.join(gd).round(3)
    por_dia.to_csv(saida / "serie_diaria_set_2026.csv")
    print(por_dia.to_string())

    titulo("2. Duas réguas da carga operacional (por semana, 01–22/09, Completed com duração)")
    w = s[(s["dt"] >= "2026-09-01") & (s["dt"] <= FIM_DURACAO)]
    d_gpt = w[w["gpt"] & w["dur"].notna()].copy()
    d_gem = w[w["comp"] & w["dur"].notna() & w["resumo_analise"].notna()].copy()
    d_gpt["sem"] = d_gpt["dt"].dt.to_period("W")
    d_gem["sem"] = d_gem["dt"].dt.to_period("W")
    t1 = d_gpt.groupby("sem").apply(lambda x: pd.Series({"h_gpt": x["dur"].sum() / 3600, "carga_gpt": x.loc[x["op"], "dur"].sum() / x["dur"].sum()}),
                                    include_groups=False)
    t2 = d_gem.groupby("sem").apply(lambda x: pd.Series({"h_gem": x["dur"].sum() / 3600,
                                                          "suporte_gem": x.loc[x["categoria_principal"] == "Suporte", "dur"].sum() / x["dur"].sum()}),
                                    include_groups=False)
    print(t1.join(t2).round(3).to_string())
    print(f"Período: GPT {d_gpt.loc[d_gpt['op'], 'dur'].sum() / d_gpt['dur'].sum():.1%} ({d_gpt['dur'].sum() / 3600:.1f} h) | "
          f"Gemini Suporte {d_gem.loc[d_gem['categoria_principal'] == 'Suporte', 'dur'].sum() / d_gem['dur'].sum():.1%} ({d_gem['dur'].sum() / 3600:.1f} h)")
    print("Alocação Gemini:", (d_gem.groupby("categoria_principal")["dur"].sum() / d_gem["dur"].sum()).round(3).to_dict())
    print("Duração mediana por categoria Gemini:", d_gem.groupby("categoria_principal")["dur"].median().round(0).to_dict())

    titulo("3. Alocação do tempo (GPT) e composição da carga operacional")
    d = d_gpt.copy()
    d["grupo"] = np.select([d["op"], d["neg"], d["p2_tipo"].isin(["relacionamento_sem_demanda", "onboarding"]), d["p2_tipo"].eq("sem_conteudo")],
                           ["carga_operacional", "negociacao", "relacionamento_sem_demanda", "sem_conteudo"], "outro")
    t = d.groupby("grupo").agg(ligacoes=("dur", "size"), horas=("dur", lambda x: x.sum() / 3600))
    t["pct_tempo"] = t["horas"] / t["horas"].sum()
    print(t.round(3).to_string())
    op = d[d["op"]]
    print(op.assign(c=np.where(op["prob"], "com_problema", op["p2_tipo"])).groupby("c")["dur"].agg(ligacoes="size", horas=lambda x: x.sum() / 3600)
          .sort_values("horas", ascending=False).round(1).to_string())
    n_vend = d["matricula_ev_createdby"].nunique()
    print(f"Vendedores {n_vend} | min/vendedor/dia: conversa {d['dur'].sum() / 60 / n_vend / 15:.1f}, carga operacional {op['dur'].sum() / 60 / n_vend / 15:.1f}")

    titulo("4. Problemas (GPT, com duração)")
    p = d[d["prob"]]
    tma_p, tma_n = p["dur"].mean(), d.loc[~d["prob"], "dur"].mean()
    print(f"TMA com problema {tma_p:.0f}s vs {tma_n:.0f}s ({tma_p / tma_n:.2f}x); excedentes {len(p) * (tma_p - tma_n) / 3600:.1f} h")
    res = g.loc[(g["prob"]) & (g["dt"] <= FIM_DURACAO), "p3_foi_resolvido_na_ligacao"].value_counts(normalize=True).round(3).to_dict()
    print("Resolução (01–22/09, todas as com problema):", res)
    pareto = p.groupby("p3_problema_principal")["dur"].agg(n="size", horas=lambda x: x.sum() / 3600).sort_values("horas", ascending=False)
    pareto["pct"] = pareto["horas"] / pareto["horas"].sum()
    pareto["acum"] = pareto["pct"].cumsum()
    print(pareto.head(6).round(3).to_string())
    print("Taxa de problema por tipo:", d.groupby("tipo_ligacao")["prob"].mean().round(3).to_dict(), "| origem outbound:",
          f"{p['tipo_ligacao'].eq('Outbound').mean():.1%}")
    cp = g[g["prob"] & g["cod"].notna() & (g["dt"] <= FIM_DURACAO)]
    vc = cp["cod"].value_counts()
    print(f"Reincidência: {vc[vc >= 2].sum() / vc.sum():.1%} das ligações com problema são de clientes com 2+")
    pg = g[g["prob"] & (g["dt"] <= FIM_DURACAO)]
    print("Pendências (problema não resolvido) 01–22/09:", int((pg["p3_foi_resolvido_na_ligacao"] != "SIM").sum()), "de", len(pg), "ligações com problema")

    titulo("5. Contactabilidade")
    print("Status:", s["status"].value_counts(normalize=True).round(3).to_dict(), "| Inbound atendido:",
          f"{s.loc[s['tipo_ligacao'] == 'Inbound', 'comp'].mean():.1%} | Outbound: {s.loc[s['tipo_ligacao'] == 'Outbound', 'comp'].mean():.1%}")
    print("Atendimento por hora (BRT):", s.groupby("hora")["comp"].agg(["size", "mean"]).round(3).T.to_string())
    print("Atendimento por dia da semana:", s.groupby("dow")["comp"].mean().round(3).to_dict())
    o = s[s["tipo_ligacao"].eq("Outbound") & s["cod"].notna()].sort_values(["cod", "ts"])
    cl = o.groupby("cod").agg(tent=("comp", "size"), ok=("comp", "max"), ult=("ts", "max"))
    nunca = cl[~cl["ok"]]
    print(f"Clientes outbound {len(cl)} | nunca atenderam {len(nunca)} | 1 tentativa só {(nunca['tent'] == 1).sum()} | "
          f"1 tentativa até 23/09: {((nunca['tent'] == 1) & (nunca['ult'] <= '2026-09-23')).sum()} | 5+ tentativas sem atender: {((nunca['tent'] >= 5)).sum()}")
    o["nt"] = o.groupby("cod").cumcount() + 1
    print("Atendimento por nº da tentativa:", o[o["nt"] <= 4].groupby("nt")["comp"].mean().round(3).to_dict())
    vd = s.groupby(["matricula_ev_createdby", "dt"]).agg(t=("comp", "size"), c=("comp", "sum")).reset_index()
    vd["dow"] = vd["dt"].dt.dayofweek
    print(f"Por vendedor/dia: {vd['t'].mean():.1f} tentativas, {vd['c'].mean():.1f} atendidas | por dia da semana (tentativas):",
          vd.groupby("dow")["t"].mean().round(1).to_dict())
    print("Status Open:", int((s["status"] == "Open").sum()), "| GPT classificadas fora de Completed:", int((s["gpt"] & ~s["comp"]).sum()))
    cc = s[s["cod"].notna()].groupby("cod").agg(h=("dur", lambda x: x.sum() / 3600))
    cc = cc.sort_values("h", ascending=False)
    print(f"Clientes {len(cc)} | top 1% = {cc['h'].head(int(len(cc) * .01)).sum() / cc['h'].sum():.1%} do tempo | top 10% = "
          f"{cc['h'].head(int(len(cc) * .1)).sum() / cc['h'].sum():.1%}")

    titulo("6. Tempo e resultado em ligações de negociação (GPT, 01–22/09, só setembro)")
    nz = g[g["p2_tipo"].isin(NEGOCIACAO) & g["dur"].notna() & (g["dt"] <= FIM_DURACAO)].copy()
    nz["fv"] = nz["fech"] | (nz["venda_b"] == True)
    nz["positiva"] = nz["Classificação tipo de ligação"].eq("POSITIVA")
    faixas = [0, 120, 300, 480, 720, 100000]
    rot = ["<2 min", "2–5 min", "5–8 min", "8–12 min", ">12 min"]
    nz["faixa"] = pd.cut(nz["dur"], faixas, labels=rot)
    linhas = []
    for f, x in nz.groupby("faixa", observed=True):
        k = int(x["fv"].sum())
        lo, hi = wilson(k, len(x))
        h = x["dur"].sum() / 3600
        linhas.append({"faixa": f, "ligacoes": len(x), "horas": h, "fechou_gpt": int(x["fech"].sum()), "venda_gemini": int((x["venda_b"] == True).sum()),
                       "fechou_ou_venda": k, "taxa": k / len(x), "ic95_inf": lo, "ic95_sup": hi, "fechamentos_por_hora": k / h,
                       "pct_positiva": x["positiva"].mean(), "spin_medio": x["nota_final_spin_n"].mean(), "pct_challenger": x["ch"].mean()})
    tab = pd.DataFrame(linhas)
    tab.round(4).to_csv(saida / "tempo_otimo_set_2026.csv", index=False, encoding="utf-8-sig")
    print(tab.round(3).to_string(index=False))
    ge5 = nz[nz["dur"] >= 300]
    print(f"≥ 5 min: {len(ge5) / len(nz):.1%} das ligações, {ge5['fv'].sum() / nz['fv'].sum():.1%} dos fechamentos, {ge5['dur'].sum() / nz['dur'].sum():.1%} do tempo")
    print("Mediana de duração das ligações fechadas por tipo:", nz[nz["fv"]].groupby("p2_tipo")["dur"].median().round(0).to_dict())
    nv = nz[nz["p2_tipo"] == "nova_venda"]
    print("Nova venda por faixa:\n", nv.groupby("faixa", observed=True).agg(n=("fv", "size"), fv=("fv", "sum"), taxa=("fv", "mean"),
                                                                        h=("dur", lambda x: x.sum() / 3600)).assign(fph=lambda t: t["fv"] / t["h"]).round(3).to_string())
    a_ = s[s["comp"] & s["dur"].notna() & (s["dt"] <= FIM_DURACAO) & s["resumo_analise"].notna()].copy()
    a_["pos"] = a_["Classificação tipo de ligação"].eq("POSITIVA")
    a_["f"] = pd.cut(a_["dur"], [0, 60, 120, 300, 480, 720, 100000], labels=["<1", "1–2", "2–5", "5–8", "8–12", ">12"])
    print("POSITIVA por faixa (todas as analisadas):", a_.groupby("f", observed=True)["pos"].mean().round(3).to_dict())
    x = s[s["venda_b"].notna() & s["p1_desfecho"].notna()]
    ga, gb = x["venda_b"] == True, x["fech"]
    po = (ga == gb).mean()
    pe = ga.mean() * gb.mean() + (1 - ga.mean()) * (1 - gb.mean())
    print(f"Venda (Gemini) x fechou (GPT): ambos {int((ga & gb).sum())}, só Gemini {int((ga & ~gb).sum())}, só GPT {int((~ga & gb).sum())}, kappa {(po - pe) / (1 - pe):.2f}")

    titulo("7. Challenger e SPIN (setembro)")
    g["neg_tipo"] = g["p2_tipo"].isin(NEGOCIACAO)
    print(g[g["neg_tipo"]].groupby("ch").agg(n=("ch", "size"), fech=("fech", "mean"), dur_med=("dur", "median"), spin=("nota_final_spin_n", "mean")).round(3).to_string())
    x = g[g["neg_tipo"] & g["dur"].between(300, 720)]
    print("Duração controlada 5–12 min:", x.groupby("ch")["fech"].agg(["size", "mean"]).round(3).to_dict("index"))
    print("Qualidade nos Challenger:", g.loc[g["ch"], "p5_qualidade"].value_counts().to_dict())
    print("Códigos CH:", g.loc[g["ch"], "p5_codigos_challenger"].str.split(r"[+,;| ]").explode().value_counts().head(8).to_dict())
    for c in ["p5_trouxe_dado", "p5_conectou_situacao", "p5_cliente_reagiu", "p5_challenger_sem_dado"]:
        print(c, int((g[c] == "SIM").sum()), f"({(g[c] == 'SIM').sum() / g[c].notna().sum():.1%})")
    for c in ["nota_spin_situacao_n", "nota_spin_problema_n", "nota_spin_implicacao_n", "nota_spin_necessidade_solucao_n"]:
        v = s[c].dropna()
        print(c, f"média {v.mean():.2f} | nota 1 em {(v == 1).mean():.1%}")
    print("Trechos disponíveis:", {c: int(s[c].notna().sum()) for c in ["p5_trecho_challenger", "p3_trechos", "p1_trecho_venda", "p5_frase_vendedor", "p3_evidencias"]})

    titulo("8. Follow-up e decisor")
    ac = s[s["comp"] & s["resumo_analise"].notna() & s["cod"].notna()].copy()
    print(f"Nova visita necessária: {ac['necessidade_nova_visita_boleano_b'].mean():.1%} | data sugerida válida {ac['sug'].notna().mean():.1%} | "
          f"lead mediano {(ac['sug'] - ac['dt']).dt.days.median():.0f} dias")
    b = ac[(ac["necessidade_nova_visita_boleano_b"] == True) & ac["sug"].notna() & (ac["sug"] <= "2026-09-30") & (ac["sug"] > ac["dt"])].copy()
    m = b.merge(s[s["cod"].notna()][["cod", "ts", "dt"]], on="cod", suffixes=("", "_n"))
    m = m[m["ts_n"] > m["ts"]]
    m["no_prazo"] = m["dt_n"] <= m["sug"] + pd.Timedelta(days=2)
    b["no_prazo"] = b["id_transcricao"].map(m.groupby("id_transcricao")["no_prazo"].max()).fillna(False)
    print(f"Retornos devidos até 30/09: {len(b)} | nova tentativa até o prazo+2d: {b['no_prazo'].mean():.1%}")
    print("Por urgência:", b.groupby(pd.cut(b["urgencia_nova_visita_n"], [0, 3, 6, 10]), observed=True)["no_prazo"].agg(["size", "mean"]).round(3).to_dict("index"))
    gg = g[g["neg_tipo"]]
    print("Decisor x resultado (negociação):", gg.groupby("falou_tomador_decisao_b").agg(n=("fech", "size"), fech=("fech", "mean"),
                                                                                       obj=("objetivo_atingido_b", "mean")).round(3).to_dict("index"))
    print(f"Falou com decisor: {s['falou_tomador_decisao_b'].mean():.1%} | secretária eletrônica: {s['falou_secretaria_eletronica_b'].mean():.1%}")
    print("Frota própria (TRUE):", int((s["frota_propria_boleano_b"] == True).sum()), "| aluguel com concorrente (TRUE):", int((s["aluguel_concorrencia_boleano_b"] == True).sum()))
    txt = s["aluguel_concorrencia"].dropna().str.lower()
    print("Menções:", {k: int(txt.str.contains(k).sum()) for k in ["movida", "unidas", "arval"]})

    titulo("9. Código M — checagens")
    c = s[s["comp"]]
    print("Completed sem análise Gemini →", c.loc[c["resumo_analise"].isna(), "Classificação tipo de ligação"].value_counts().to_dict())
    print("Completed:", c["Classificação tipo de ligação"].value_counts().to_dict())
    an = s[s["resumo_analise"].notna()]
    ndv, opb, nop = an["nota_demanda_venda_n"], an["oportunidades_boleano_b"], an["nota_oportunidades_n"]
    A = (an["demanda_venda_eminente_boleano_b"] == True) | ((an["necessidade_nova_visita_boleano_b"] == True) & (ndv >= 8)) | (ndv >= 8) | ((opb == True) & (nop >= 7))
    print(f"Ramo 'ndv>=8 e A=0 e sem decisor' possível? {int(((ndv >= 8) & ~A).sum())} linhas | A verdadeiro em {A.mean():.1%}")
    print("Chave com mês 08 nas linhas de 31/08:", int(((s["dt"] == '2026-08-31') & s["Chave"].str.endswith("08")).sum()), "de", int((s["dt"] == '2026-08-31').sum()))
    print("Valores de status:", s["status"].value_counts().to_dict(), "| DIVISIONAL:", s["DIVISIONAL"].nunique())
    nome = s["nome_createdby"].str.split().str[0].str.lower().fillna("")
    cita = [(n in r) if n else False for n, r in zip(nome, s["resumo_analise"].fillna("").str.lower())]
    print("Resumos que citam o primeiro nome do vendedor:", int(sum(cita)), "de", int(s["resumo_analise"].notna().sum()))

    titulo("10. Carteira (≥ 40 ligações classificadas até 22/09) → anexo")
    gc = g[g["dt"] <= FIM_DURACAO]

    def por_carteira(x):
        dd = x[x["dur"].notna()]
        tot = max(dd["dur"].sum(), 1)
        return pd.Series({"ligacoes_classificadas": len(x), "horas_medidas": dd["dur"].sum() / 3600,
                          "pct_tempo_operacional": dd.loc[dd["op"], "dur"].sum() / tot, "pct_tempo_negociacao": dd.loc[dd["neg"], "dur"].sum() / tot,
                          "taxa_problema": x["prob"].mean(), "taxa_challenger": x["ch"].mean(), "spin_medio": x["nota_final_spin_n"].mean(),
                          "tma_s": dd["dur"].mean(), "taxa_decisor": x["falou_tomador_decisao_b"].mean()})
    cart = gc.groupby("CARTEIRA").apply(por_carteira, include_groups=False)
    cart = cart[cart["ligacoes_classificadas"] >= 40].join(s.groupby("CARTEIRA").agg(
        tentativas=("comp", "size"), taxa_atendimento=("comp", "mean"), distrital=("DISTRITAL", "first")))
    cart.round(3).to_csv(saida / "carteira_set_2026.csv", encoding="utf-8-sig")
    print(cart[["pct_tempo_operacional", "pct_tempo_negociacao", "taxa_problema", "taxa_challenger", "spin_medio", "tma_s", "taxa_atendimento"]]
          .describe().round(3).loc[["mean", "min", "50%", "max"]].to_string())
    dist = gc.groupby("DISTRITAL").apply(por_carteira, include_groups=False)
    print(dist[["ligacoes_classificadas", "pct_tempo_operacional", "taxa_problema", "taxa_challenger", "spin_medio", "tma_s"]].round(3).to_string())
    print("Carteira x matrícula 1:1:", s.groupby("CARTEIRA")["matricula_ev_createdby"].nunique().max(), s.groupby("matricula_ev_createdby")["CARTEIRA"].nunique().max())


if __name__ == "__main__":
    main()
