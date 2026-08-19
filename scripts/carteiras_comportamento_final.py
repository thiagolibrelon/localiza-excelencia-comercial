"""
Agregação FINAL por carteira — combina:
  1) O scoring heuristico determinístico (mesma lógica/pesos de
     scripts/scoring_potencial.py) sobre a base total já cobrindo as 3
     origens: resultados/scoring_potencial_combinado_total.csv (13.264 linhas
     = piloto 1.275 + novo_lote 5.348 + julho 6.641; Parte D).
  2) A taxa de fechamento REAL (p1_desfecho, extraído por LLM via P1) por
     carteira, cruzando CONSOLIDADO_LIGACOES.csv + CONSOLIDADO_JULHO.csv
     pelo mapa ampliado de carteiras (Parte E):
     resultados/cruzamento_ligacoes_diarias/clientes_combinado.csv.

Amostra mínima de 15 ligações resolvidas para entrar no ranking de taxa de
fechamento real (mesmo critério já usado no dashboard/por_carteira.csv).

Saida: resultados/cruzamento_ligacoes_diarias/carteiras_comportamento_final.csv
"""
import csv
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "resultados" / "cruzamento_ligacoes_diarias"

SCORING_COMBINADO = BASE / "resultados" / "scoring_potencial_combinado_total.csv"
MAPA_CLIENTES = OUT_DIR / "clientes_combinado.csv"
LIGACOES_JUNHO = BASE / "resultados" / "consolidado" / "CONSOLIDADO_LIGACOES.csv"
LIGACOES_JULHO = BASE / "JULHO" / "consolidado" / "CONSOLIDADO_JULHO.csv"

FECHOU = {"fechou_novo", "fechou_upsell", "fechou_renovacao"}
AMOSTRA_MINIMA = 15


def normalizar_cod(cod):
    return str(cod).strip().zfill(8)


def carregar_carteiras():
    mapa = {}
    with open(MAPA_CLIENTES, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            mapa[row["cod"]] = row["carteira"]
    return mapa


def main():
    mapa = carregar_carteiras()

    # --- 1) Agregacao comportamental (heuristica), igual carteiras_comportamento.py ---
    agg_heur = defaultdict(lambda: {
        "n": 0, "score_total": 0, "fc1": 0, "fc3": 0,
        "ch1": 0, "ch6": 0, "upsell": 0, "urgencia": 0,
        "diagnostico": 0, "tem_promessa_sem_prazo": 0,
    })
    with open(SCORING_COMBINADO, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cod = normalizar_cod(row["client_id"])
            carteira = mapa.get(cod, "SEM_REGISTRO")
            a = agg_heur[carteira]
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

    # --- 2) Taxa de fechamento REAL (p1_desfecho), igual metodologia da Parte C item 10 ---
    agg_real = defaultdict(lambda: {"n_resolvido": 0, "n_fechou": 0})
    for caminho in (LIGACOES_JUNHO, LIGACOES_JULHO):
        with open(caminho, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                cid = row.get("cliente_id", "").strip()
                if not cid:
                    continue
                # SEMINFO_* nao tem Cod para cruzar -> cai em SEM_REGISTRO
                # (mantido na soma para bater com o total canonico de
                # p1_desfecho resolvido da Parte C, item 2/3).
                cod = cid if cid.startswith("SEMINFO_") else normalizar_cod(cid)
                carteira = mapa.get(cod, "SEM_REGISTRO")
                desf = row.get("p1_desfecho", "").strip()
                if desf == "":
                    continue
                a = agg_real[carteira]
                a["n_resolvido"] += 1
                if desf in FECHOU:
                    a["n_fechou"] += 1

    # --- Junta as duas agregacoes por carteira ---
    todas_carteiras = set(agg_heur.keys()) | set(agg_real.keys())
    cols = ["carteira", "n_ligacoes_heuristico", "score_medio", "ch1_pct", "b5_upsell_pct",
            "b6_urgencia_pct", "b1_diagnostico_pct", "fc1_pct", "fc3_pct",
            "promessas_sem_prazo_pct",
            "n_resolvido_real", "n_fechou_real", "taxa_fechamento_real_pct",
            "amostra_minima_15_ok"]
    linhas = []
    for carteira in todas_carteiras:
        h = agg_heur.get(carteira, {"n": 0})
        r = agg_real.get(carteira, {"n_resolvido": 0, "n_fechou": 0})
        n = h.get("n", 0)
        n_res = r["n_resolvido"]
        linha = {
            "carteira": carteira,
            "n_ligacoes_heuristico": n,
            "score_medio": round(h["score_total"] / n, 2) if n else "",
            "ch1_pct": round(100 * h["ch1"] / n, 1) if n else "",
            "b5_upsell_pct": round(100 * h["upsell"] / n, 1) if n else "",
            "b6_urgencia_pct": round(100 * h["urgencia"] / n, 1) if n else "",
            "b1_diagnostico_pct": round(100 * h["diagnostico"] / n, 1) if n else "",
            "fc1_pct": round(100 * h["fc1"] / n, 1) if n else "",
            "fc3_pct": round(100 * h["fc3"] / n, 1) if n else "",
            "promessas_sem_prazo_pct": round(100 * h["tem_promessa_sem_prazo"] / n, 1) if n else "",
            "n_resolvido_real": n_res,
            "n_fechou_real": r["n_fechou"],
            "taxa_fechamento_real_pct": round(100 * r["n_fechou"] / n_res, 1) if n_res else "",
            "amostra_minima_15_ok": int(n_res >= AMOSTRA_MINIMA),
        }
        linhas.append(linha)

    linhas.sort(key=lambda r: -r["n_resolvido_real"])

    out_path = OUT_DIR / "carteiras_comportamento_final.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        w.writerows(linhas)

    elegiveis = [l for l in linhas if l["carteira"] != "SEM_REGISTRO" and l["amostra_minima_15_ok"] == 1]
    elegiveis.sort(key=lambda r: -r["taxa_fechamento_real_pct"])

    print(f"{len(linhas)} carteiras no total (incl. SEM_REGISTRO).")
    print(f"Carteiras elegiveis para ranking (>= {AMOSTRA_MINIMA} ligacoes resolvidas, excl. SEM_REGISTRO): {len(elegiveis)}")
    sem_reg = next((l for l in linhas if l["carteira"] == "SEM_REGISTRO"), None)
    if sem_reg:
        print(f"SEM_REGISTRO: n_resolvido_real={sem_reg['n_resolvido_real']} n_fechou_real={sem_reg['n_fechou_real']} taxa={sem_reg['taxa_fechamento_real_pct']}%")
    print(f"\nSalvo em {out_path}")
    print("\nTOP 5 por taxa_fechamento_real_pct:")
    for l in elegiveis[:5]:
        print(f"  {l['carteira']:<10} n_resolvido={l['n_resolvido_real']:>5} n_fechou={l['n_fechou_real']:>4} taxa={l['taxa_fechamento_real_pct']}%")
    print("BOTTOM 5 por taxa_fechamento_real_pct:")
    for l in elegiveis[-5:]:
        print(f"  {l['carteira']:<10} n_resolvido={l['n_resolvido_real']:>5} n_fechou={l['n_fechou_real']:>4} taxa={l['taxa_fechamento_real_pct']}%")


if __name__ == "__main__":
    main()
