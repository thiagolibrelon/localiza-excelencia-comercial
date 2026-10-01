"""Gera os dados agregados que alimentam os prototipos (wireframe do BI e trilha do vendedor) a partir do CSV de setembro.

COMO USAR:
  python gerar_dados_prototipos.py "Consulta Power Bi - Copia.csv" [--saida dados_prototipos.json]

Saida: um JSON com agregados por dia, semana, carteira e faixa de duracao. Sem nome de vendedor, sem codigo de cliente, sem trecho
de transcricao (os trechos das licoes sao escolhidos e mascarados a mao em missao_4T26/prototipos/).
Reaproveita as definicoes de scripts/auditoria_dados_missao.py (carga operacional, negociacao, janela de duracao ate 22/09).
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

from auditoria_dados_missao import FIM_DURACAO, NEGOCIACAO, carregar

LEGENDA_P = {"P1": "Acesso/sistema", "P2": "Faturamento/cobrança", "P3": "Multa/infração", "P4": "Manutenção/substituto",
             "P5": "Condutor/cadastro", "P6": "Km excedente", "P7": "Disponibilidade", "P8": "Franquia/agência", "P9": "Sinistro",
             "P10": "Reserva/sistema", "P11": "Outro", "P12": "Manipulação de pesquisa/NPS", "P13": "Crédito/cadastro PJ",
             "P14": "Preço/competitividade", "P15": "Tag de pedágio"}


def r(x, n=4):
    return None if x is None or (isinstance(x, float) and np.isnan(x)) else round(float(x), n)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--saida", default="dados_prototipos.json")
    a = ap.parse_args()
    cru, s = carregar(a.csv)
    g = s[s["gpt"]].copy()
    out = {"meta": {"janela": ["2026-08-31", "2026-09-30"], "duracao_ate": FIM_DURACAO, "linhas": int(len(s)), "colunas": int(cru.shape[1])}}

    # ---- diario
    dias = []
    for d, x in s.groupby(s["dt"].dt.date):
        ds = str(d)
        comp = x[x["comp"]]
        gx = x[x["gpt"]]
        dg = gx[gx["dur"].notna()]
        em = comp[comp["dur"].notna() & comp["resumo_analise"].notna()]
        k1g = dg.loc[dg["op"], "dur"].sum() / dg["dur"].sum() if len(dg) else None
        k7 = dg.loc[dg["neg"], "dur"].sum() / dg["dur"].sum() if len(dg) else None
        k1m = em.loc[em["categoria_principal"] == "Suporte", "dur"].sum() / em["dur"].sum() if len(em) else None
        pend = int(((gx["prob"]) & (gx["p3_foi_resolvido_na_ligacao"] != "SIM")).sum())
        dias.append({"d": ds, "tent": int(len(x)), "comp": int(len(comp)), "gpt": int(len(gx)),
                     "c1": r(comp["fonte_classificacao"].notna().mean()) if len(comp) else None,
                     "c2": r(comp["dur"].notna().mean()) if len(comp) else None,
                     "k1_gpt": r(k1g), "k1_gem": r(k1m), "k7": r(k7), "pend": pend,
                     "prob": r(gx["prob"].mean()) if len(gx) else None,
                     "p1": r((gx["p3_problema_principal"] == "P1").mean()) if len(gx) else None,
                     "ch": r(gx["ch"].mean()) if len(gx) else None,
                     "horas": r(dg["dur"].sum() / 3600, 2) if len(dg) else None})
    out["diario"] = dias

    # ---- semanal
    w = s[(s["dt"] >= "2026-09-01") & (s["dt"] <= FIM_DURACAO)]
    dg = w[w["gpt"] & w["dur"].notna()].copy()
    em = w[w["comp"] & w["dur"].notna() & w["resumo_analise"].notna()].copy()
    sem = []
    s_all = s.copy()
    s_all["sem"] = s_all["dt"].dt.to_period("W").astype(str)
    dg["sem"] = dg["dt"].dt.to_period("W").astype(str)
    em["sem"] = em["dt"].dt.to_period("W").astype(str)
    for k, x in dg.groupby("sem"):
        e = em[em["sem"] == k]
        gx = g[g["dt"].dt.to_period("W").astype(str) == k]
        sem.append({"sem": k.split("/")[0][5:].replace("-", "/") if False else k, "h": r(x["dur"].sum() / 3600, 1),
                    "k1_gpt": r(x.loc[x["op"], "dur"].sum() / x["dur"].sum()), "k1_gem": r(e.loc[e["categoria_principal"] == "Suporte", "dur"].sum() / e["dur"].sum()),
                    "k7": r(x.loc[x["neg"], "dur"].sum() / x["dur"].sum()), "prob": r(gx["prob"].mean()),
                    "pend": int(((gx["prob"]) & (gx["p3_foi_resolvido_na_ligacao"] != "SIM")).sum()),
                    "dias": int(x["dt"].nunique())})
    out["semanal"] = sem

    # ---- mensal / alocacao
    d = dg.copy()
    tot = d["dur"].sum()
    out["mensal"] = {"horas": r(tot / 3600, 1), "ligacoes": int(len(d)),
                     "operacional": r(d.loc[d["op"], "dur"].sum() / tot), "com_problema": r(d.loc[d["prob"], "dur"].sum() / tot),
                     "negociacao": r(d.loc[d["neg"], "dur"].sum() / tot),
                     "relacionamento": r(d.loc[d["p2_tipo"].isin(["relacionamento_sem_demanda", "onboarding"]) & ~d["op"], "dur"].sum() / tot),
                     "sem_conteudo": r(d.loc[d["p2_tipo"].eq("sem_conteudo") & ~d["op"], "dur"].sum() / tot),
                     "gem": {k: r(v) for k, v in (em.groupby("categoria_principal")["dur"].sum() / em["dur"].sum()).items()},
                     "tma_prob": r(d.loc[d["prob"], "dur"].mean(), 0), "tma_sem": r(d.loc[~d["prob"], "dur"].mean(), 0)}

    # ---- problemas
    p = d[d["prob"]]
    par = p.groupby("p3_problema_principal")["dur"].agg(n="size", s="sum").sort_values("s", ascending=False)
    out["pareto"] = [{"cod": c, "nome": LEGENDA_P.get(c, c), "n": int(v["n"]), "h": r(v["s"] / 3600, 1), "pct": r(v["s"] / par["s"].sum())} for c, v in par.head(8).iterrows()]
    pg = g[g["prob"] & (g["dt"] <= FIM_DURACAO)]
    out["resolucao"] = {k: r(v) for k, v in pg["p3_foi_resolvido_na_ligacao"].value_counts(normalize=True).items()}
    out["origem"] = {"inbound": r(d.loc[d["tipo_ligacao"] == "Inbound", "prob"].mean()), "outbound": r(d.loc[d["tipo_ligacao"] == "Outbound", "prob"].mean()),
                     "outbound_do_total_com_problema": r(p["tipo_ligacao"].eq("Outbound").mean())}
    cp = g[g["prob"] & g["cod"].notna() & (g["dt"] <= FIM_DURACAO)]
    vc = cp["cod"].value_counts()
    out["reincidencia"] = r(vc[vc >= 2].sum() / vc.sum())

    # ---- carteira e distrital
    gc = g[g["dt"] <= FIM_DURACAO]

    def por_carteira(x):
        dd = x[x["dur"].notna()]
        t = max(dd["dur"].sum(), 1)
        gem = s[(s["CARTEIRA"] == x.name) & (s["dt"] <= FIM_DURACAO) & s["resumo_analise"].notna()]
        return pd.Series({"n": len(x), "h": dd["dur"].sum() / 3600, "k1": dd.loc[dd["op"], "dur"].sum() / t, "k7": dd.loc[dd["neg"], "dur"].sum() / t,
                          "prob": x["prob"].mean(), "ch": x["ch"].mean(), "dado": (x["p5_trouxe_dado"] == "SIM").mean(),
                          "conecta": (x["p5_conectou_situacao"] == "SIM").mean(), "reage": (x["p5_cliente_reagiu"] == "SIM").mean(),
                          "spin_s": gem["nota_spin_situacao_n"].mean(), "spin_p": gem["nota_spin_problema_n"].mean(),
                          "spin_i": gem["nota_spin_implicacao_n"].mean(), "spin_n": gem["nota_spin_necessidade_solucao_n"].mean(),
                          "decisor": gem["falou_tomador_decisao_b"].mean(), "tma": dd["dur"].mean()})
    cart = gc.groupby("CARTEIRA").apply(por_carteira, include_groups=False)
    cart = cart[cart["n"] >= 40].join(s.groupby("CARTEIRA").agg(tent=("comp", "size"), atend=("comp", "mean"), distrital=("DISTRITAL", "first")))
    out["carteiras"] = [{"c": c, "dist": row["distrital"], **{k: r(row[k]) for k in cart.columns if k != "distrital"}} for c, row in cart.iterrows()]
    out["mediana_carteira"] = {k: r(cart[k].median()) for k in cart.columns if k != "distrital"}
    dist = gc.groupby("DISTRITAL").apply(lambda x: pd.Series({"n": len(x), "k1": x[x["dur"].notna() & x["op"]]["dur"].sum() / x["dur"].sum(),
                                                               "prob": x["prob"].mean()}), include_groups=False)
    out["distritais"] = [{"d": k, "n": int(v["n"]), "k1": r(v["k1"]), "prob": r(v["prob"])} for k, v in dist.iterrows()]

    # ---- concentracao de clientes no tempo
    cc = s[s["cod"].notna()].groupby("cod").agg(h=("dur", lambda x: x.sum() / 3600), n=("comp", "size"), prob=("prob", "sum")).sort_values("h", ascending=False)
    totc = cc["h"].sum()
    out["clientes"] = {"total": int(len(cc)), "curva": [{"pct_clientes": q, "pct_tempo": r(cc["h"].head(max(1, int(len(cc) * q / 100))).sum() / totc)} for q in (1, 2, 5, 10, 20, 50, 100)],
                       "top10": [{"rank": i + 1, "h": r(v["h"], 1), "pct": r(v["h"] / totc), "ligacoes": int(v["n"]), "problemas": int(v["prob"])} for i, (_, v) in enumerate(cc.head(10).iterrows())]}

    # ---- tempo e ritmo
    nz = g[g["p2_tipo"].isin(NEGOCIACAO) & g["dur"].notna() & (g["dt"] <= FIM_DURACAO)].copy()
    nz["fv"] = nz["fech"] | (nz["venda_b"] == True)
    nz["faixa"] = pd.cut(nz["dur"], [0, 120, 300, 480, 720, 100000], labels=["< 2 min", "2–5 min", "5–8 min", "8–12 min", "> 12 min"])
    fx = []
    for f, x in nz.groupby("faixa", observed=True):
        k, n_ = int(x["fv"].sum()), len(x)
        z = 1.96
        pp = k / n_
        den = 1 + z * z / n_
        cen = pp + z * z / (2 * n_)
        am = z * np.sqrt(pp * (1 - pp) / n_ + z * z / (4 * n_ * n_))
        fx.append({"faixa": f, "n": n_, "k": k, "taxa": r(pp), "lo": r((cen - am) / den), "hi": r((cen + am) / den), "h": r(x["dur"].sum() / 3600, 1), "fph": r(k / (x["dur"].sum() / 3600), 2)})
    out["faixas"] = fx
    out["status"] = {k: int(v) for k, v in s["status"].value_counts().items()}
    o = s[s["tipo_ligacao"].eq("Outbound") & s["cod"].notna()].sort_values(["cod", "ts"])
    cl = o.groupby("cod").agg(tent=("comp", "size"), ok=("comp", "max"), ult=("ts", "max"))
    nunca = cl[~cl["ok"]]
    o["nt"] = o.groupby("cod").cumcount() + 1
    out["recontato"] = {"clientes": int(len(cl)), "nunca": int(len(nunca)), "uma_tentativa": int((nunca["tent"] == 1).sum()),
                        "uma_ate_23_09": int(((nunca["tent"] == 1) & (nunca["ult"] <= "2026-09-23")).sum()),
                        "cadencia": {str(k): r(v) for k, v in o[o["nt"] <= 4].groupby("nt")["comp"].mean().items()}}
    out["hora"] = [{"h": int(h), "n": int(v["size"]), "atend": r(v["mean"])} for h, v in s.groupby("hora")["comp"].agg(["size", "mean"]).iterrows() if 8 <= h <= 18]
    vd = s.groupby(["matricula_ev_createdby", "dt"]).agg(t=("comp", "size"), c=("comp", "sum")).reset_index()
    vd["dow"] = vd["dt"].dt.dayofweek
    out["capacidade_dow"] = [{"dow": int(k), "tent": r(v["t"], 1), "atend": r(v["c"], 1)} for k, v in vd.groupby("dow")[["t", "c"]].mean().iterrows()]
    ac = s[s["comp"] & s["resumo_analise"].notna() & s["cod"].notna()].copy()
    b = ac[(ac["necessidade_nova_visita_boleano_b"] == True) & ac["sug"].notna() & (ac["sug"] <= "2026-09-30") & (ac["sug"] > ac["dt"])].copy()
    m = b.merge(s[s["cod"].notna()][["cod", "ts", "dt"]], on="cod", suffixes=("", "_n"))
    m = m[m["ts_n"] > m["ts"]]
    m["np"] = m["dt_n"] <= m["sug"] + pd.Timedelta(days=2)
    b["np"] = b["id_transcricao"].map(m.groupby("id_transcricao")["np"].max()).fillna(False)
    grp = b.groupby(pd.cut(b["urgencia_nova_visita_n"], [0, 3, 6, 10], labels=["1–3", "4–6", "7–10"]), observed=True)["np"].agg(["size", "mean"])
    out["retorno"] = {"devidos": int(len(b)), "no_prazo": r(b["np"].mean()), "por_urgencia": [{"u": str(k), "n": int(v["size"]), "taxa": r(v["mean"])} for k, v in grp.iterrows()]}

    # ---- competencias globais
    out["competencias"] = {"ch_completo": r(g["ch"].mean()), "dado": r((g["p5_trouxe_dado"] == "SIM").sum() / g["p5_trouxe_dado"].notna().sum()),
                           "conecta": r((g["p5_conectou_situacao"] == "SIM").sum() / g["p5_conectou_situacao"].notna().sum()),
                           "reage": r((g["p5_cliente_reagiu"] == "SIM").sum() / g["p5_cliente_reagiu"].notna().sum()),
                           "spin": {k: {"media": r(s[c].mean(), 2), "nota1": r((s[c].dropna() == 1).mean())} for k, c in
                                    [("Situação", "nota_spin_situacao_n"), ("Problema", "nota_spin_problema_n"), ("Implicação", "nota_spin_implicacao_n"),
                                     ("Necessidade", "nota_spin_necessidade_solucao_n")]},
                           "decisor": r(s["falou_tomador_decisao_b"].mean())}

    # ---- qualidade do dado
    out["qualidade"] = {"colunas": {"usar": 46, "ressalva": 34, "nao_usar": 8},
                        "sentinelas": [{"campo": "volume_aluguel_concorrencia", "pct": 0.992}, {"campo": "volume_frota_propria", "pct": 0.952},
                                       {"campo": "aluguel_concorrencia", "pct": 0.868}, {"campo": "frota_propria", "pct": 0.861},
                                       {"campo": "spin_implicacao", "pct": 0.332}, {"campo": "data_sugerida_nova_visita", "pct": 0.224},
                                       {"campo": "motivo_nova_visita", "pct": 0.213}],
                        "m_code": {"detratora_sem_analise": int((s["comp"] & s["resumo_analise"].isna()).sum()),
                                   "detratora_total": int(((s["comp"]) & (s["Classificação tipo de ligação"] == "DETRATORA")).sum()),
                                   "chave_31_08": int((s["dt"] == "2026-08-31").sum()), "completed_sem_gpt": int((s["comp"] & s["fonte_classificacao"].isna()).sum())}}
    Path(a.saida).write_text(json.dumps(out, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print("ok", a.saida, len(json.dumps(out)) // 1024, "KB")


if __name__ == "__main__":
    main()
