"""
Cruza a base de ligacoes (dados/LIG) com a base de diarias (diarias_*.json)
usando o Cod do cliente (8 digitos) como chave. Nao usa nome de cliente nem
nome de vendedor - agrupamentos por pessoa usam apenas "carteira".

Saidas:
  resultados/cruzamento_ligacoes_diarias/clientes.csv   (1 linha por cliente)
  resultados/cruzamento_ligacoes_diarias/por_carteira.csv
  resultados/cruzamento_ligacoes_diarias/por_cnae.csv
  resultados/cruzamento_ligacoes_diarias/resumo.txt
"""
import csv
import json
import statistics
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
OUT_DIR = BASE / "resultados" / "cruzamento_ligacoes_diarias"
OUT_DIR.mkdir(parents=True, exist_ok=True)

DIARIAS_FILES = [
    "diarias_00_24.json",
    "diarias_25_49.json",
    "diarias_50_74.json",
    "diarias_75_99.json",
]

FECHOU = {"fechou_novo", "fechou_upsell", "fechou_renovacao"}


def normalizar_cod(cod):
    return str(cod).strip().zfill(8)


def carregar_diarias():
    diarias = {}
    for nome in DIARIAS_FILES:
        caminho = BASE / nome
        with open(caminho, encoding="utf-8") as f:
            payload = json.load(f)
        diarias.update(payload.get("d", {}))
    return diarias


def carregar_lig():
    with open(BASE / "dados" / "LIG", encoding="utf-8") as f:
        return json.load(f)


def carregar_desfechos():
    caminho = BASE / "resultados" / "cruzamento_reservas.csv"
    desfechos = defaultdict(list)
    with open(caminho, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cod = normalizar_cod(row["cliente_id"])
            desfechos[cod].append(row["desfecho_ia"])
    return desfechos


def volume_am_ad(registro):
    am_total = 0
    ad_total = 0
    for _mes, (am, ad) in registro.get("h", {}).items():
        am_total += am
        ad_total += ad
    return am_total, ad_total


def main():
    diarias = carregar_diarias()
    lig = carregar_lig()
    desfechos = carregar_desfechos()

    linhas = []
    sem_diaria = 0

    for cod_raw, chamadas in lig.items():
        cod = normalizar_cod(cod_raw)
        qtd_ligacoes = len(chamadas)
        registro = diarias.get(cod)

        desf_lista = desfechos.get(cod, [])
        n_fechou = sum(1 for d in desf_lista if d in FECHOU)
        n_interessou = sum(1 for d in desf_lista if d == "interessou_nao_fechou")
        n_nao_venda = sum(1 for d in desf_lista if d == "nao_era_venda")

        if registro is None:
            sem_diaria += 1
            linhas.append({
                "cod": cod,
                "carteira": "SEM_REGISTRO",
                "cnae": "SEM_REGISTRO",
                "qtd_ligacoes": qtd_ligacoes,
                "volume_am": "",
                "volume_ad": "",
                "volume_total": "",
                "ligacoes_por_mil_diarias": "",
                "n_fechou": n_fechou,
                "n_interessou_nao_fechou": n_interessou,
                "n_nao_era_venda": n_nao_venda,
            })
            continue

        carteira = registro.get("k") or "SEM_CARTEIRA"
        cnae = registro.get("c") or "SEM_CNAE"
        am, ad = volume_am_ad(registro)
        total = am + ad
        razao = (qtd_ligacoes / (total / 1000)) if total > 0 else None

        linhas.append({
            "cod": cod,
            "carteira": carteira,
            "cnae": cnae,
            "qtd_ligacoes": qtd_ligacoes,
            "volume_am": am,
            "volume_ad": ad,
            "volume_total": total,
            "ligacoes_por_mil_diarias": round(razao, 2) if razao is not None else "",
            "n_fechou": n_fechou,
            "n_interessou_nao_fechou": n_interessou,
            "n_nao_era_venda": n_nao_venda,
        })

    # ---- CSV por cliente ----
    with open(OUT_DIR / "clientes.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        w.writerows(linhas)

    # ---- Agregacao por carteira ----
    por_carteira = defaultdict(lambda: {
        "num_clientes": 0, "qtd_ligacoes": 0, "volume_am": 0, "volume_ad": 0,
        "n_fechou": 0, "n_interessou": 0, "n_nao_venda": 0,
    })
    for l in linhas:
        c = por_carteira[l["carteira"]]
        c["num_clientes"] += 1
        c["qtd_ligacoes"] += l["qtd_ligacoes"]
        if l["volume_am"] != "":
            c["volume_am"] += l["volume_am"]
            c["volume_ad"] += l["volume_ad"]
        c["n_fechou"] += l["n_fechou"]
        c["n_interessou"] += l["n_interessou_nao_fechou"]
        c["n_nao_venda"] += l["n_nao_era_venda"]

    with open(OUT_DIR / "por_carteira.csv", "w", newline="", encoding="utf-8") as f:
        cols = ["carteira", "num_clientes", "qtd_ligacoes", "volume_am", "volume_ad",
                "volume_total", "ligacoes_por_mil_diarias", "n_fechou", "n_interessou",
                "n_nao_venda", "taxa_fechamento_pct"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for carteira, c in sorted(por_carteira.items(), key=lambda kv: -kv[1]["qtd_ligacoes"]):
            total = c["volume_am"] + c["volume_ad"]
            razao = round(c["qtd_ligacoes"] / (total / 1000), 2) if total > 0 else ""
            n_analisadas = c["n_fechou"] + c["n_interessou"] + c["n_nao_venda"]
            taxa = round(100 * c["n_fechou"] / n_analisadas, 1) if n_analisadas > 0 else ""
            w.writerow({
                "carteira": carteira, "num_clientes": c["num_clientes"],
                "qtd_ligacoes": c["qtd_ligacoes"], "volume_am": c["volume_am"],
                "volume_ad": c["volume_ad"], "volume_total": total,
                "ligacoes_por_mil_diarias": razao, "n_fechou": c["n_fechou"],
                "n_interessou": c["n_interessou"], "n_nao_venda": c["n_nao_venda"],
                "taxa_fechamento_pct": taxa,
            })

    # ---- Agregacao por CNAE ----
    por_cnae = defaultdict(lambda: {
        "num_clientes": 0, "qtd_ligacoes": 0, "volume_am": 0, "volume_ad": 0,
        "n_fechou": 0, "n_interessou": 0, "n_nao_venda": 0,
    })
    for l in linhas:
        c = por_cnae[l["cnae"]]
        c["num_clientes"] += 1
        c["qtd_ligacoes"] += l["qtd_ligacoes"]
        if l["volume_am"] != "":
            c["volume_am"] += l["volume_am"]
            c["volume_ad"] += l["volume_ad"]
        c["n_fechou"] += l["n_fechou"]
        c["n_interessou"] += l["n_interessou_nao_fechou"]
        c["n_nao_venda"] += l["n_nao_era_venda"]

    with open(OUT_DIR / "por_cnae.csv", "w", newline="", encoding="utf-8") as f:
        cols = ["cnae", "num_clientes", "qtd_ligacoes", "volume_am", "volume_ad",
                "volume_total", "ligacoes_por_mil_diarias", "n_fechou", "n_interessou",
                "n_nao_venda", "taxa_fechamento_pct"]
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for cnae, c in sorted(por_cnae.items(), key=lambda kv: -kv[1]["qtd_ligacoes"]):
            total = c["volume_am"] + c["volume_ad"]
            razao = round(c["qtd_ligacoes"] / (total / 1000), 2) if total > 0 else ""
            n_analisadas = c["n_fechou"] + c["n_interessou"] + c["n_nao_venda"]
            taxa = round(100 * c["n_fechou"] / n_analisadas, 1) if n_analisadas > 0 else ""
            w.writerow({
                "cnae": cnae, "num_clientes": c["num_clientes"],
                "qtd_ligacoes": c["qtd_ligacoes"], "volume_am": c["volume_am"],
                "volume_ad": c["volume_ad"], "volume_total": total,
                "ligacoes_por_mil_diarias": razao, "n_fechou": c["n_fechou"],
                "n_interessou": c["n_interessou"], "n_nao_venda": c["n_nao_venda"],
                "taxa_fechamento_pct": taxa,
            })

    # ---- Correlacao qtd_ligacoes x volume_total (so clientes com registro) ----
    pares = [(l["qtd_ligacoes"], l["volume_total"]) for l in linhas if l["volume_total"] != ""]
    xs = [p[0] for p in pares]
    ys = [p[1] for p in pares]
    try:
        correl = statistics.correlation(xs, ys)
    except Exception:
        correl = None

    with open(OUT_DIR / "resumo.txt", "w", encoding="utf-8") as f:
        f.write("Cruzamento ligacoes x diarias (AM/AD) x CNAE x carteira\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Total clientes na base de ligacoes (LIG): {len(lig)}\n")
        f.write(f"Total ligacoes: {sum(len(v) for v in lig.values())}\n")
        f.write(f"Clientes SEM registro na base de diarias: {sem_diaria}\n")
        f.write(f"Clientes COM registro na base de diarias: {len(lig) - sem_diaria}\n\n")
        f.write(f"Correlacao (qtd_ligacoes x volume_total AM+AD), clientes com registro: "
                f"{correl:.3f}\n" if correl is not None else "Correlacao: N/A\n")
        f.write("\nInterpretacao: correlacao proxima de 0 = esforco de ligacao NAO\n"
                "acompanha o volume de diarias do cliente (efeito nao proporcional).\n"
                "Correlacao alta positiva = clientes maiores recebem mais ligacoes\n"
                "(esperado). Negativa = clientes pequenos recebem mais atencao que\n"
                "clientes grandes (possivel ma alocacao de esforco comercial).\n")
        f.write(f"\nArquivos gerados em {OUT_DIR}\\:\n")
        f.write("  - clientes.csv (1 linha por cliente/Cod)\n")
        f.write("  - por_carteira.csv (agregado por carteira, sem nome de vendedor)\n")
        f.write("  - por_cnae.csv (agregado por CNAE)\n")

    print(f"OK. {len(linhas)} clientes processados, {sem_diaria} sem registro em diarias.")
    print(f"Correlacao qtd_ligacoes x volume_total: {correl}")
    print(f"Saida em: {OUT_DIR}")


if __name__ == "__main__":
    main()
