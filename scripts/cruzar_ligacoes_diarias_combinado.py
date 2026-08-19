"""
Copia adaptada de scripts/cruzar_ligacoes_diarias.py — MESMA lógica de
cruzamento com a base de diárias (Cod de 8 dígitos como chave), mas monta
a lista de clientes de ENTRADA a partir da UNIÃO das 3 fontes de ligações
(em vez de só dados/LIG, que cobre apenas o piloto):

  - dados/LIG                                        (piloto,    1.275 ligações)
  - dados/recebidos/bloco_lig_recebido_01.json        (novo lote, 5.348 ligações)
  - JULHO/dados_convertidos/julho_completo.json       (julho,     6.641 ligações)

Chaves "SEMINFO_*" (ligações sem cliente identificado na origem, sem Cod
para cruzar) são ignoradas.

A base de diárias (diarias_00_24/25_49/50_74/75_99.json) já cobre todos os
Cod da empresa — o gargalo estava só na lista de clientes de entrada.

Os contadores de desfecho (n_fechou / n_interessou / n_nao_era_venda) agora
vêm de p1_desfecho em resultados/consolidado/CONSOLIDADO_LIGACOES.csv (cobre
piloto+novo_lote) e JULHO/consolidado/CONSOLIDADO_JULHO.csv (cobre julho),
em vez de resultados/cruzamento_reservas.csv (que só cobria os 1.275 do
piloto) — isso amplia a cobertura desses contadores também.

Não sobrescreve resultados/cruzamento_ligacoes_diarias/clientes.csv (original,
só piloto) — grava em clientes_combinado.csv para permitir comparação.

Saida: resultados/cruzamento_ligacoes_diarias/clientes_combinado.csv
"""
import csv
import json
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

FONTES_LIGACOES = [
    ("piloto",    BASE / "dados" / "LIG"),
    ("novo_lote", BASE / "dados" / "recebidos" / "bloco_lig_recebido_01.json"),
    ("julho",     BASE / "JULHO" / "dados_convertidos" / "julho_completo.json"),
]

FONTES_DESFECHO = [
    BASE / "resultados" / "consolidado" / "CONSOLIDADO_LIGACOES.csv",
    BASE / "JULHO" / "consolidado" / "CONSOLIDADO_JULHO.csv",
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


def carregar_qtd_ligacoes_uniao():
    """
    Une as 3 fontes de ligacoes por Cod normalizado, somando qtd_ligacoes
    de cada uma. Ignora chaves SEMINFO_* (sem Cod).
    """
    qtd_por_cod = defaultdict(int)
    origens_por_cod = defaultdict(set)
    ignoradas_seminfo = 0
    ignoradas_seminfo_calls = 0

    for nome_fonte, caminho in FONTES_LIGACOES:
        with open(caminho, encoding="utf-8") as f:
            data = json.load(f)
        for cod_raw, chamadas in data.items():
            if str(cod_raw).startswith("SEMINFO_"):
                ignoradas_seminfo += 1
                ignoradas_seminfo_calls += len(chamadas)
                continue
            cod = normalizar_cod(cod_raw)
            qtd_por_cod[cod] += len(chamadas)
            origens_por_cod[cod].add(nome_fonte)

    print(f"  Chaves SEMINFO_* ignoradas: {ignoradas_seminfo} clientes / {ignoradas_seminfo_calls} ligacoes")
    return qtd_por_cod, origens_por_cod


def carregar_desfechos():
    """
    Conta desfechos (p1_desfecho) por Cod normalizado, combinando
    CONSOLIDADO_LIGACOES.csv (piloto+novo_lote) e CONSOLIDADO_JULHO.csv (julho).
    """
    desf = defaultdict(lambda: {"fechou": 0, "interessou": 0, "nao_venda": 0})
    for caminho in FONTES_DESFECHO:
        with open(caminho, encoding="utf-8") as f:
            for row in csv.DictReader(f):
                cid = row.get("cliente_id", "").strip()
                if not cid or cid.startswith("SEMINFO_"):
                    continue
                cod = normalizar_cod(cid)
                d = row.get("p1_desfecho", "").strip()
                if d in FECHOU:
                    desf[cod]["fechou"] += 1
                elif d == "interessou_nao_fechou":
                    desf[cod]["interessou"] += 1
                elif d == "nao_era_venda":
                    desf[cod]["nao_venda"] += 1
    return desf


def volume_am_ad(registro):
    am_total = 0
    ad_total = 0
    for _mes, (am, ad) in registro.get("h", {}).items():
        am_total += am
        ad_total += ad
    return am_total, ad_total


def main():
    print("Carregando base de diarias...")
    diarias = carregar_diarias()

    print("Carregando uniao das 3 fontes de ligacoes...")
    qtd_por_cod, origens_por_cod = carregar_qtd_ligacoes_uniao()
    total_clientes_uniao = len(qtd_por_cod)
    total_ligacoes_uniao = sum(qtd_por_cod.values())
    print(f"  Clientes unicos na uniao (Cod normalizado): {total_clientes_uniao}")
    print(f"  Ligacoes totais na uniao (com Cod): {total_ligacoes_uniao}")

    print("Carregando desfechos (p1_desfecho) combinados...")
    desfechos = carregar_desfechos()

    linhas = []
    sem_diaria = 0

    for cod, qtd_ligacoes in qtd_por_cod.items():
        registro = diarias.get(cod)
        d = desfechos.get(cod, {"fechou": 0, "interessou": 0, "nao_venda": 0})

        if registro is None:
            sem_diaria += 1
            linhas.append({
                "cod": cod,
                "carteira": "SEM_REGISTRO",
                "cnae": "SEM_REGISTRO",
                "origens": "+".join(sorted(origens_por_cod[cod])),
                "qtd_ligacoes": qtd_ligacoes,
                "volume_am": "",
                "volume_ad": "",
                "volume_total": "",
                "ligacoes_por_mil_diarias": "",
                "n_fechou": d["fechou"],
                "n_interessou_nao_fechou": d["interessou"],
                "n_nao_era_venda": d["nao_venda"],
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
            "origens": "+".join(sorted(origens_por_cod[cod])),
            "qtd_ligacoes": qtd_ligacoes,
            "volume_am": am,
            "volume_ad": ad,
            "volume_total": total,
            "ligacoes_por_mil_diarias": round(razao, 2) if razao is not None else "",
            "n_fechou": d["fechou"],
            "n_interessou_nao_fechou": d["interessou"],
            "n_nao_era_venda": d["nao_venda"],
        })

    out_path = OUT_DIR / "clientes_combinado.csv"
    with open(out_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0].keys()))
        w.writeheader()
        w.writerows(linhas)

    com_carteira = total_clientes_uniao - sem_diaria
    print(f"\nOK. {len(linhas)} clientes (uniao) processados.")
    print(f"  COM carteira mapeada: {com_carteira} ({com_carteira/total_clientes_uniao*100:.1f}%)")
    print(f"  SEM_REGISTRO (sem match em diarias_*): {sem_diaria} ({sem_diaria/total_clientes_uniao*100:.1f}%)")
    print(f"  Antes (so piloto): 1109/1109 elegiveis, cobertura sobre a base combinada de 10.337 clientes = {1109/10337*100:.1f}%")
    print(f"Saida em: {out_path}")


if __name__ == "__main__":
    main()
