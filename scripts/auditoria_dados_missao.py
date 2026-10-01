"""Auditoria e mapa de oportunidades da missao 4T26 — reproduz os numeros de
missao_4T26/AUDITORIA_DADOS_E_OPORTUNIDADES.md a partir do CSV da consulta do Power BI + consolidados do repo.

COMO USAR:
  python auditoria_dados_missao.py "Consulta Power Bi - Copia.csv" [--saida missao_4T26/anexos]

Le: CSV de setembro (obrigatorio), JULHO/consolidado/CONSOLIDADO_JULHO.csv, resultados/consolidado/CONSOLIDADO_LIGACOES.csv
e diarias_*.json (da raiz do repo). Escreve so agregados (por dia, por carteira, por faixa de duracao) — sem nome de vendedor,
sem cliente, sem trecho de transcricao.
Convencoes: horario do CSV esta em UTC (corrigido -3h para BRT); booleanos vem como VERDADEIRO/FALSO;
codigo_cliente perde o zero a esquerda (normalizado para 8 digitos); janela com duracao = ate 22/09.
"""
import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
OPERACIONAIS = ["suporte_operacional", "supporte_operacional", "cobranca", "pos_venda_manutencao",
                "pos_venda_sinistro", "duvida_contrato"]
NEGOCIACAO = ["nova_venda", "upsell", "renovacao", "retencao", "misto"]
FAIXAS = [0, 30, 60, 120, 180, 300, 480, 720, 1200, 100000]
ROTULOS = ["<30s", "30-60s", "1-2m", "2-3m", "3-5m", "5-8m", "8-12m", "12-20m", ">20m"]
FIM_DURACAO = "2026-09-22"


def num(s):
    return pd.to_numeric(s.astype("string").str.replace(",", "."), errors="coerce")


def carregar_setembro(caminho):
    s = pd.read_csv(caminho, sep=";", encoding="utf-8-sig", dtype=str, low_memory=False)
    s["ts"] = pd.to_datetime("1899-12-30") + pd.to_timedelta(num(s["data_visita_ev"]), unit="D") - pd.Timedelta(hours=3)
    s["dt"] = s["ts"].dt.normalize()
    s["hora"] = s["ts"].dt.hour
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
    for c in ["objetivo_atingido", "demanda_venda_eminente_boleano", "falou_tomador_decisao", "necessidade_nova_visita_boleano"]:
        s[c + "_b"] = s[c].map({"VERDADEIRO": True, "FALSO": False})
    for c in ["nota_final_spin", "nota_demanda_venda", "nota_demanda_atendimento"]:
        s[c + "_n"] = num(s[c])
    return s


def titulo(t):
    print(f"\n=== {t} ===")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--saida", default=str(RAIZ / "missao_4T26" / "anexos"))
    a = ap.parse_args()
    saida = Path(a.saida)
    saida.mkdir(parents=True, exist_ok=True)
    s = carregar_setembro(a.csv)
    g = s[s["gpt"]].copy()

    titulo("1. Assinatura do classificador por dia (drift)")
    por_dia = s.groupby(s["dt"].dt.date).agg(
        tentativas=("comp", "size"), completed=("comp", "sum"), classificadas_gpt=("gpt", "sum"),
        com_duracao=("dur", "count"))
    gd = g.groupby(g["dt"].dt.date).agg(taxa_problema=("prob", "mean"), taxa_challenger=("ch", "mean"),
                                        taxa_era_venda=("era_venda", lambda x: (x == "SIM").mean()),
                                        taxa_fechou=("fech", "mean"))
    por_dia = por_dia.join(gd).round(3)
    por_dia.to_csv(saida / "serie_diaria_set_2026.csv")
    print(por_dia.to_string())

    titulo("2. Comparacao entre meses (motores diferentes: Gemini jun/jul x GPT set)")
    jul = pd.read_csv(RAIZ / "JULHO/consolidado/CONSOLIDADO_JULHO.csv", dtype=str)
    jun = pd.read_csv(RAIZ / "resultados/consolidado/CONSOLIDADO_LIGACOES.csv", dtype=str)
    chs = ["SIM", "CHALLENGER", "CH1", "CH2", "CH3", "CH4", "CH5", "CH6", "CH7"]
    linhas = []
    for nome, d in [("Jun (Gemini)", jun), ("Jul (Gemini)", jul), ("Set (GPT C12)", g.rename(columns={}))]:
        x = d[d["p1_desfecho"].notna()]
        linhas.append({"base": nome, "n": len(x), "fechou%": x["p1_desfecho"].str.startswith("fechou").mean() * 100,
                       "nao_era_venda%": (x["p1_desfecho"] == "nao_era_venda").mean() * 100,
                       "challenger%": x["p5_teve_challenger"].fillna("").isin(chs).mean() * 100})
    print(pd.DataFrame(linhas).round(1).to_string(index=False))

    titulo("3. Cobertura e chaves")
    comp = s[s["comp"] & (s["dt"] >= "2026-09-01") & (s["dt"] <= FIM_DURACAO)]
    print(f"Completed 01-22/09 classificadas (qualquer fonte): {comp['fonte_classificacao'].notna().mean():.1%}")
    cp = s[s["comp"]]
    print(f"Duracao presente nas Completed ate 22/09: {cp[cp['dt'] <= FIM_DURACAO]['dur'].notna().mean():.1%} | de 23/09 em diante: "
          f"{cp[cp['dt'] > FIM_DURACAO]['dur'].notna().mean():.1%}")
    print(f"codigo_cliente nulo: {s['codigo_cliente'].isna().mean():.1%} | com menos de 8 digitos: "
          f"{(s['codigo_cliente'].str.len() < 8).mean():.1%} | Completed sem analise_llm: {(s[s['comp']]['resumo_analise'].isna()).sum()}")
    print("nota_demanda_atendimento: min/max", s["nota_demanda_atendimento_n"].min(), s["nota_demanda_atendimento_n"].max(),
          "(campo constante)")
    for c in ["oportunidades_boleano", "necessidade_nova_visita_boleano", "demanda_de_atendimento_boleano"]:
        v = s[c].map({"VERDADEIRO": True, "FALSO": False})
        print(f"{c}: VERDADEIRO em {v.mean():.1%} dos analisados")
    dias = {}
    for f in ["diarias_00_24", "diarias_25_49", "diarias_50_74", "diarias_75_99"]:
        dias.update(json.load(open(RAIZ / f"{f}.json", encoding="utf-8"))["d"])
    ultimo = max(m for v in dias.values() for m in v["h"])
    print(f"Diarias: {len(dias)} codigos, ultimo mes {ultimo} | match com clientes de setembro: "
          f"{s['cod'].isin(dias.keys()).mean():.1%} das linhas")

    titulo("4. Alocacao do tempo de ligacao (01-22/09, GPT com duracao)")
    d = g[g["dur"].notna() & (g["dt"] <= FIM_DURACAO)].copy()
    d["grupo"] = np.select([d["op"], d["neg"], d["p2_tipo"].isin(["relacionamento_sem_demanda", "onboarding"]),
                            d["p2_tipo"].eq("sem_conteudo")],
                           ["carga_operacional", "negociacao", "relacionamento_sem_demanda", "sem_conteudo"], "outro")
    t = d.groupby("grupo").agg(ligacoes=("dur", "size"), horas=("dur", lambda x: x.sum() / 3600))
    t["pct_tempo"] = t["horas"] / t["horas"].sum()
    print(t.round(3).to_string())
    op = d[d["op"]]
    por_tipo = op.assign(componente=np.where(op["prob"], "com_problema", op["p2_tipo"])).groupby("componente")["dur"].agg(
        ligacoes="size", horas=lambda x: x.sum() / 3600)
    print("Composicao da carga operacional:\n", por_tipo.sort_values("horas", ascending=False).round(1).to_string())

    titulo("5. Contactabilidade (todas as tentativas)")
    print("Taxa de atendimento por hora (BRT):\n", s.groupby("hora")["comp"].agg(["size", "mean"]).round(3).T.to_string())
    print("Por tipo:\n", s.groupby("tipo_ligacao")["comp"].agg(["size", "mean"]).round(3).to_string())
    o = s[s["tipo_ligacao"].eq("Outbound") & s["cod"].notna()]
    cl = o.groupby("cod").agg(tent=("comp", "size"), ok=("comp", "max"), ult=("ts", "max"))
    nunca = cl[~cl["ok"]]
    print(f"Clientes outbound {len(cl)} | nunca atenderam {len(nunca)} ({len(nunca) / len(cl):.1%}) | com 1 tentativa so "
          f"{(nunca['tent'] == 1).sum()} | 1 tentativa ate 23/09 sem 2a: {((nunca['tent'] == 1) & (nunca['ult'] <= '2026-09-23')).sum()}")
    o = o.sort_values(["cod", "ts"])
    o["nt"] = o.groupby("cod").cumcount() + 1
    print("Atendimento por numero da tentativa:", o[o["nt"] <= 4].groupby("nt")["comp"].mean().round(3).to_dict())
    pv = s.groupby(["matricula_ev_createdby", "dt"]).agg(t=("comp", "size"), c=("comp", "sum"))
    print(f"Tentativas por vendedor/dia: media {pv['t'].mean():.1f} | atendidas {pv['c'].mean():.1f}")

    titulo("6. Duracao x resultado em ligacoes de negociacao (jun+jul+set pooled)")
    def pool(df, dur, fech, tipo):
        return pd.DataFrame({"dur": pd.to_numeric(df[dur], errors="coerce").astype(float),
                             "fechou": df[fech].astype(bool), "tipo": df[tipo]})
    jun["fechou"] = jun["p1_desfecho"].fillna("").str.startswith("fechou")
    jul["fechou"] = jul["p1_desfecho"].fillna("").str.startswith("fechou")
    base = pd.concat([pool(jun, "duracao_s", "fechou", "p2_tipo"), pool(jul, "duracao_s", "fechou", "p2_tipo"),
                      pool(g, "dur", "fech", "p2_tipo")])
    base = base[base["tipo"].isin(NEGOCIACAO) & base["dur"].notna()].copy()
    base["faixa"] = pd.cut(base["dur"], FAIXAS, labels=ROTULOS)
    f = base.groupby("faixa", observed=True).agg(ligacoes=("fechou", "size"), fechamentos=("fechou", "sum"),
                                                 taxa=("fechou", "mean"), horas=("dur", lambda x: x.sum() / 3600))
    f["fechamentos_por_hora"] = f["fechamentos"] / f["horas"]
    f.round(3).to_csv(saida / "faixa_duracao_negociacao.csv")
    print(f.round(3).to_string())

    titulo("7. Challenger e SPIN em Set (ligacoes GPT)")
    g["neg_tipo"] = g["p2_tipo"].isin(NEGOCIACAO)
    print(g[g["neg_tipo"]].groupby("ch").agg(n=("ch", "size"), fech=("fech", "mean"), inter=("inter", "mean"), dur_med=("dur", "median"),
                                              spin=("nota_final_spin_n", "mean")).round(3).to_string())
    x = g[g["neg_tipo"] & g["dur"].between(300, 720)]
    print("Controlando duracao 5-12m:", x.groupby("ch")["fech"].agg(["size", "mean"]).round(3).to_dict("index"))
    print("Qualidade nos Challenger de Set:", g[g["ch"]]["p5_qualidade"].value_counts().to_dict())
    for c in ["p5_trouxe_dado", "p5_conectou_situacao", "p5_cliente_reagiu"]:
        print(c, (g[c] == "SIM").sum(), f"({(g[c] == 'SIM').sum() / g[c].notna().sum():.1%})")

    titulo("8. Follow-up (nova visita necessaria x proximo contato)")
    ac = s[s["comp"] & s["cod"].notna()].sort_values(["cod", "ts"]).copy()
    ac["dias_prox"] = (ac.groupby("cod")["ts"].shift(-1) - ac["ts"]).dt.total_seconds() / 86400
    w = ac[(ac["necessidade_nova_visita_boleano_b"] == True) & (ac["ts"] <= "2026-09-16")]
    print(f"Ligacoes com nova visita necessaria ate 16/09: {len(w)} | com novo contato em 14d: {(w['dias_prox'] <= 14).mean():.1%}")

    titulo("9. Decisor")
    gg = g[g["neg_tipo"]]
    print(gg.groupby("falou_tomador_decisao_b").agg(n=("fech", "size"), fech=("fech", "mean"),
                                                    obj=("objetivo_atingido_b", "mean")).round(3).to_string())

    titulo("10. Carteira (>=40 ligacoes classificadas ate 22/09) -> anexo")
    gc = g[g["dt"] <= FIM_DURACAO]

    def por_carteira(x):
        dd = x[x["dur"].notna()]
        tot = max(dd["dur"].sum(), 1)
        return pd.Series({"ligacoes_classificadas": len(x), "horas_medidas": dd["dur"].sum() / 3600,
                          "pct_tempo_operacional": dd.loc[dd["op"], "dur"].sum() / tot,
                          "pct_tempo_negociacao": dd.loc[dd["neg"], "dur"].sum() / tot,
                          "taxa_problema": x["prob"].mean(), "taxa_challenger": x["ch"].mean(),
                          "spin_medio": x["nota_final_spin_n"].mean(), "tma_s": dd["dur"].mean(),
                          "taxa_decisor": x["falou_tomador_decisao_b"].mean()})
    cart = gc.groupby("CARTEIRA").apply(por_carteira, include_groups=False)
    cart = cart[cart["ligacoes_classificadas"] >= 40].join(s.groupby("CARTEIRA").agg(
        tentativas=("comp", "size"), taxa_atendimento=("comp", "mean"), distrital=("DISTRITAL", "first")))
    cart.round(3).to_csv(saida / "carteira_set_2026.csv")
    print(cart[["pct_tempo_operacional", "pct_tempo_negociacao", "taxa_problema", "taxa_challenger", "spin_medio", "tma_s"]]
          .describe().round(3).loc[["mean", "min", "50%", "max"]].to_string())
    dist = gc.groupby("DISTRITAL").apply(por_carteira, include_groups=False)
    print(dist[["ligacoes_classificadas", "pct_tempo_operacional", "taxa_problema", "taxa_challenger", "spin_medio", "tma_s"]].round(3).to_string())

    titulo("11. Tamanho do cliente (diarias dos ultimos 3 meses) x problema")
    def vol3(cod):
        v = dias.get(cod)
        if not v:
            return np.nan
        meses = sorted(v["h"])[-3:]
        return sum(sum(v["h"][m]) for m in meses) / len(meses)
    gm = gc[gc["cod"].isin(dias.keys())].copy()
    gm["vol3m"] = gm["cod"].map(vol3)
    gm["quartil"] = pd.qcut(gm["vol3m"].rank(method="first"), 4, labels=["Q1", "Q2", "Q3", "Q4"])
    print(gm.groupby("quartil", observed=True).agg(ligacoes=("prob", "size"), vol_mediano=("vol3m", "median"),
                                                   taxa_problema=("prob", "mean"), tma_s=("dur", "mean")).round(3).to_string())


if __name__ == "__main__":
    main()
