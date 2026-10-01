"""Baseline da carga operacional da venda interna (missao 4T26) a partir do CSV da consulta do Power BI.

COMO USAR:
  python baseline_carga_operacional.py "Consulta Power Bi - Copia.csv" [--ini 2026-09-01] [--fim 2026-09-22]

Base: ligacoes classificadas pelo GPT (fonte_classificacao = gpt) COM duracao (CallDurationInSeconds).
Carga por problema = tempo de ligacao com tem_problema = SIM / tempo total de ligacao da base.
Carga ampla       = problema OU p2_tipo operacional (suporte, cobranca, pos-venda, duvida de contrato).
Imprime os numeros citados em missao_4T26/PLANO_MISSAO_4T26.md (rastreabilidade: toda metrica tem origem).
Nao grava nada e nao imprime nome de vendedor nem de cliente.
"""
import argparse

import numpy as np
import pandas as pd

OPERACIONAIS = ["suporte_operacional", "supporte_operacional", "cobranca", "pos_venda_manutencao",
                "pos_venda_sinistro", "duvida_contrato"]


def carregar(caminho):
    df = pd.read_csv(caminho, sep=";", encoding="utf-8-sig", dtype=str, low_memory=False)
    serial = pd.to_numeric(df["Data"], errors="coerce")  # o export do Power BI traz a data como serial do Excel
    df["dt"] = pd.to_datetime("1899-12-30") + pd.to_timedelta(serial, unit="D")
    if serial.isna().any():  # export com data em texto (AAAA-MM-DD)
        df.loc[serial.isna(), "dt"] = pd.to_datetime(df.loc[serial.isna(), "Data"], errors="coerce", format="%Y-%m-%d")
    df["dur"] = pd.to_numeric(df["CallDurationInSeconds"].str.replace(",", "."), errors="coerce")
    return df


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv")
    ap.add_argument("--ini", default="2026-09-01")
    ap.add_argument("--fim", default="2026-09-22")
    a = ap.parse_args()

    df = carregar(a.csv)
    gpt = df[df["fonte_classificacao"].eq("gpt") & df["dt"].between(a.ini, a.fim)].copy()
    d = gpt[gpt["dur"].notna()].copy()
    d["prob"] = d["tem_problema"].eq("SIM")
    d["ampla"] = d["prob"] | d["p2_tipo"].isin(OPERACIONAIS)
    print(f"Periodo {a.ini} a {a.fim} | classificadas GPT: {len(gpt)} | com duracao: {len(d)} ({len(d) / len(gpt):.0%})")

    horas = d["dur"].sum() / 3600
    h_prob = d.loc[d["prob"], "dur"].sum() / 3600
    h_ampla = d.loc[d["ampla"], "dur"].sum() / 3600
    print(f"Horas medidas {horas:.1f} | com problema {h_prob:.1f} ({h_prob / horas:.1%}) | ampla {h_ampla:.1f} ({h_ampla / horas:.1%})")
    print(f"Ligacoes com problema: {d['prob'].mean():.1%} ({int(d['prob'].sum())})")

    tma_p, tma_n = d.loc[d["prob"], "dur"].mean(), d.loc[~d["prob"], "dur"].mean()
    print(f"TMA com problema {tma_p:.0f}s | sem {tma_n:.0f}s | razao {tma_p / tma_n:.2f}x | "
          f"mediana {d.loc[d['prob'], 'dur'].median():.0f}s vs {d.loc[~d['prob'], 'dur'].median():.0f}s")
    print(f"Horas excedentes (n_prob x (TMA_prob - TMA_sem)): {d['prob'].sum() * (tma_p - tma_n) / 3600:.1f} h")

    res = gpt.loc[gpt["tem_problema"].eq("SIM"), "p3_foi_resolvido_na_ligacao"].value_counts(normalize=True)
    print("Resolucao do problema na ligacao:", {k: f"{v:.1%}" for k, v in res.items()})

    pareto = d[d["prob"]].groupby("p3_problema_principal")["dur"].agg(["size", "sum"]).sort_values("sum", ascending=False)
    pareto["horas"] = pareto["sum"] / 3600
    pareto["pct"] = pareto["sum"] / pareto["sum"].sum()
    pareto["acum"] = pareto["pct"].cumsum()
    print("Pareto do tempo com problema (codigo P3):")
    print(pareto[["size", "horas", "pct", "acum"]].head(6).round(3).to_string())

    por_tipo = d.groupby("tipo_ligacao").agg(lig=("dur", "size"), taxa_prob=("prob", "mean"))
    print("Por tipo de ligacao:\n", por_tipo.round(3).to_string())

    cp = gpt[gpt["tem_problema"].eq("SIM") & gpt["codigo_cliente"].notna()]
    vc = cp["codigo_cliente"].value_counts()
    print(f"Reincidencia: {vc[vc >= 2].sum() / vc.sum():.1%} das ligacoes com problema sao de clientes com 2+ no periodo")

    d["metade"] = np.where(d["dt"] < "2026-09-15", "02-14/09", "15-22/09")
    cmp = d[d["dt"] >= "2026-09-02"].groupby("metade").apply(
        lambda x: pd.Series({"taxa_prob": x["prob"].mean(), "carga_prob": x.loc[x["prob"], "dur"].sum() / x["dur"].sum()}),
        include_groups=False)
    print("Estabilidade da regua (mudanca de nivel no meio do mes):\n", cmp.round(3).to_string())


if __name__ == "__main__":
    main()
