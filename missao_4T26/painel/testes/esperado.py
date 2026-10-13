"""Recalcula com pandas, direto do CSV, os indicadores que testes/numeros.js compara com o painel.

Uso: python testes/esperado.py "C:\\caminho\\consulta.csv" > esperado.json
"""
import contextlib
import io
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import atualizar_painel as ap  # noqa: E402


def calc(s, m):
    x = s[m]
    d = lambda a, b: float(a / b) if b else None  # noqa: E731
    b = x[x["base"]]
    prob = x["prob"]
    pc_ = x[prob & x["cod"].notna()].groupby("cod").size()
    return {"tent": int(len(x)), "atend": int(x["comp"].sum()), "an": int(x["an"].sum()), "conv": int(x["conv"].sum()),
            "opp": int(x["opp"].sum()), "fech": int(x["fech"].sum()), "txFech": d(x["fech"].sum(), x["opp"].sum()),
            "prob": int(prob.sum()), "txProb": d(prob.sum(), x["conv"].sum()), "res": d((prob & x["res"].eq("SIM")).sum(), prob.sum()),
            "pend": int(x["pend"].sum()), "k1": d(b.loc[b["op"], "dur"].sum(), b["dur"].sum()), "horas": float(b["dur"].sum() / 3600),
            "ch": d(x["ch"].sum(), x["conv"].sum()), "chAlta": d((x["chq"] == 3).sum(), x["conv"].sum()),
            "dado": d(x["dado_s"].sum(), x["dado_n"].sum()), "rea": d(x["rea_s"].sum(), x["rea_n"].sum()),
            "sf": float(x["sf"].mean()) if x["sf"].notna().any() else None, "si1": d((x["si"] == 1).sum(), x["si"].notna().sum()),
            "dec": d(x["dec_s"].sum(), x["dec_n"].sum()), "tc": d(x["tc_s"].sum(), x["tc_n"].sum()),
            "clientes": int(x.loc[x["cod"].notna(), "cod"].nunique()), "k5": d(pc_[pc_ >= 2].sum(), pc_.sum())}


def main():
    with contextlib.redirect_stdout(io.StringIO()):
        s, _ = ap.preparar(ap.carregar(sys.argv[1]))
    mes = (s["dt"] >= "2026-09-01") & (s["dt"] <= "2026-09-30")
    print(json.dumps({"set": calc(s, mes),
                      "S1I05A_0122": calc(s, (s["dt"] >= "2026-09-01") & (s["dt"] <= "2026-09-22") & (s["carteira"] == "S1I05A")),
                      "DTIN4_set": calc(s, mes & (s["distrital"] == "DTIN4"))}))


if __name__ == "__main__":
    main()
