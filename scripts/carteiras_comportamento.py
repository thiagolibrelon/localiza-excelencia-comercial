"""
Agrega comportamentos comerciais (scoring_potencial.csv) por CARTEIRA
(nao por vendedor/nome) usando o mapeamento cliente -> carteira gerado
em resultados/cruzamento_ligacoes_diarias/clientes.csv.

Saida: resultados/cruzamento_ligacoes_diarias/carteiras_comportamento.csv
"""
import csv
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "resultados" / "cruzamento_ligacoes_diarias"


def normalizar_cod(cod):
    return str(cod).strip().zfill(8)


def carregar_carteiras():
    mapa = {}
    with open(OUT_DIR / "clientes.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            mapa[row["cod"]] = row["carteira"]
    return mapa


def main():
    mapa = carregar_carteiras()

    agg = defaultdict(lambda: {
        "n": 0, "score_total": 0, "fc1": 0, "fc3": 0,
        "ch1": 0, "ch6": 0, "upsell": 0, "urgencia": 0,
        "diagnostico": 0, "tem_promessa_sem_prazo": 0,
    })

    with open(BASE / "resultados" / "scoring_potencial.csv", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cod = normalizar_cod(row["client_id"])
            carteira = mapa.get(cod, "SEM_REGISTRO")
            a = agg[carteira]
            a["n"] += 1
            a["score_total"] += float(row["score_total"])
            a["fc1"] += 1 if row["tipo_fechamento"] == "FC1_compromisso_duplo" else 0
            a["fc3"] += 1 if row["tipo_fechamento"] == "FC3_vago" else 0
            a["ch1"] += int(row["tem_ch1"])
            a["ch6"] += int(row["tem_ch6"])
            a["upsell"] += int(row["tem_upsell"])
            a["urgencia"] += int(row["tem_urgencia"])
            a["diagnostico"] += int(row["tem_diagnostico"])
            a["tem_promessa_sem_prazo"] += 1 if int(row["promessas_sem_prazo"]) >= 1 else 0

    cols = ["carteira", "n_ligacoes", "score_medio", "ch1_pct", "b5_upsell_pct",
            "b6_urgencia_pct", "b1_diagnostico_pct", "fc1_pct", "fc3_pct",
            "promessas_sem_prazo_pct"]
    linhas = []
    for carteira, a in agg.items():
        n = a["n"]
        linhas.append({
            "carteira": carteira,
            "n_ligacoes": n,
            "score_medio": round(a["score_total"] / n, 2),
            "ch1_pct": round(100 * a["ch1"] / n, 1),
            "b5_upsell_pct": round(100 * a["upsell"] / n, 1),
            "b6_urgencia_pct": round(100 * a["urgencia"] / n, 1),
            "b1_diagnostico_pct": round(100 * a["diagnostico"] / n, 1),
            "fc1_pct": round(100 * a["fc1"] / n, 1),
            "fc3_pct": round(100 * a["fc3"] / n, 1),
            "promessas_sem_prazo_pct": round(100 * a["tem_promessa_sem_prazo"] / n, 1),
        })

    linhas.sort(key=lambda r: -r["n_ligacoes"])

    with open(OUT_DIR / "carteiras_comportamento.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(linhas)

    print(f"{len(linhas)} carteiras. Salvo em {OUT_DIR / 'carteiras_comportamento.csv'}")
    print("\nTop 15 por volume de ligacoes:")
    for l in linhas[:15]:
        print(l)


if __name__ == "__main__":
    main()
