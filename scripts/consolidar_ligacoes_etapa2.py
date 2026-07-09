"""
Etapa 2: incorpora a exploracao Fable (P3/P7 em 456 ligacoes; P4/P8/P11/P13/P14/P15
em 151 ligacoes do novo lote) na base montada pela etapa 1, e escreve o CSV final.

Como essas exploracoes sao passes AGREGADOS (tabelas de frequencia por lote, nao
por ligacao), o que da pra anexar por ligacao especifica e':
  - uma flag "amostrado" (SIM) pra toda ligacao que estava no lote analisado
  - uma nota curta SE aquela ligacao foi citada como exemplo nominal no markdown
    (via regex "Cliente <cod>"), senao fica em branco mesmo estando amostrada
Rodar depois de scripts/consolidar_ligacoes.py (usa o pickle intermediario dele).
"""
import re
import csv
import pickle
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
OUT_CSV = ROOT / "resultados" / "consolidado" / "CONSOLIDADO_LIGACOES.csv"

with open(ROOT / "resultados" / "consolidado" / "_intermediario.pkl", "rb") as f:
    D = pickle.load(f)

master = D["master"]
dados_p1, dados_p2 = D["dados_p1"], D["dados_p2"]
dados_p5, dados_p6 = D["dados_p5"], D["dados_p6"]
dados_p9, dados_p10_agg = D["dados_p9"], D["dados_p10_agg"]
sid_para_batch_cliente = D["sid_para_batch_cliente"]

# lookup (cliente_id, data, duracao_s) -> [segment_id,...] (reconstruido igual a etapa 1)
key_p1 = defaultdict(list)
for sid, r in master.items():
    key_p1[(r["cliente_id"], r["data"], r["duracao_s"])].append(sid)

def segment_ids_do_arquivo_amostra(path):
    """Le um arquivo de lote de amostra (formato '=== LIGACAO | Base:.. | Cliente:.. |
    Data:.. | Dur:..s | Sent:.. ===') e resolve os segment_id correspondentes."""
    texto = path.read_text(encoding="utf-8")
    sids = []
    for m in re.finditer(r"=== LIGACAO \| Base:(\S+) \| Cliente:(\S+) \| Data:(\S+) \| Dur:(\S+)s \| Sent:(\S+) ===", texto):
        base, cid, data, dur, sent = m.groups()
        candidatos = key_p1.get((cid, data, dur), [])
        if candidatos:
            sids.append(candidatos[0])
    return sids

def extrair_notas_cliente(md_texto):
    """Extrai, por cliente citado no markdown, o trecho da linha/bullet onde apareceu."""
    notas = defaultdict(list)
    for linha in md_texto.splitlines():
        for m in re.finditer(r"[Cc]liente\s+(\d{4,8})", linha):
            cid = m.group(1)
            trecho = linha.strip().lstrip("-*").strip()
            if len(trecho) > 240:
                trecho = trecho[:237] + "..."
            notas[cid].append(trecho)
    return notas

# ---------------------------------------------------------------------------
# P3/P7 — 12 lotes (amostra combinada de 456 ligacoes, ambas as bases)
# ---------------------------------------------------------------------------
p3_p7_amostrado = set()
p3_p7_nota = {}  # segment_id -> nota (concatenando P3+P7 se houver as duas)

lotes_p3_p7 = ['02','03','04','06','07','08','09','10','11','12','13','14']
for lote in lotes_p3_p7:
    input_path = ROOT / "resultados" / "exploracao_fable" / "inputs" / f"batch{lote}.txt"
    output_path = ROOT / "resultados" / "exploracao_fable" / "outputs" / f"batch{lote}_resultado.md"
    if not input_path.exists() or not output_path.exists():
        continue
    sids = segment_ids_do_arquivo_amostra(input_path)
    p3_p7_amostrado.update(sids)

    md = output_path.read_text(encoding="utf-8")
    notas_por_cliente = extrair_notas_cliente(md)
    # mapeia sid -> cliente_id pra aplicar a nota certa
    for sid in sids:
        cid = master[sid]["cliente_id"]
        if cid in notas_por_cliente:
            existentes = p3_p7_nota.get(sid, "")
            novas = " | ".join(notas_por_cliente[cid][:2])
            p3_p7_nota[sid] = (existentes + " || " + novas) if existentes else novas

print(f"P3/P7 — ligacoes amostradas: {len(p3_p7_amostrado)} | com nota especifica: {len(p3_p7_nota)}")

# ---------------------------------------------------------------------------
# P4/P8/P11/P13/P14/P15 — 4 lotes (151 ligacoes, so novo lote)
# ---------------------------------------------------------------------------
p4_amostrado = set()
p4_nota = {}

lotes_p4 = ['01','02','03','04']
for lote in lotes_p4:
    input_path = ROOT / "resultados" / "exploracao_fable" / "inputs_novo_lote_363" / f"lote{lote}.txt"
    output_path = ROOT / "resultados" / "exploracao_fable" / "outputs_novo_lote_363" / f"lote{lote}_resultado.md"
    if not input_path.exists() or not output_path.exists():
        continue
    sids = segment_ids_do_arquivo_amostra(input_path)
    p4_amostrado.update(sids)

    md = output_path.read_text(encoding="utf-8")
    notas_por_cliente = extrair_notas_cliente(md)
    for sid in sids:
        cid = master[sid]["cliente_id"]
        if cid in notas_por_cliente:
            existentes = p4_nota.get(sid, "")
            novas = " | ".join(notas_por_cliente[cid][:2])
            p4_nota[sid] = (existentes + " || " + novas) if existentes else novas

print(f"P4/P8/P11/P13/P14/P15 — ligacoes amostradas: {len(p4_amostrado)} | com nota especifica: {len(p4_nota)}")

# ---------------------------------------------------------------------------
# Monta o CSV final
# ---------------------------------------------------------------------------
FIELDS = [
    "segment_id", "base_origem", "cliente_id", "data", "duracao_s", "sentimento",
    # P1
    "p1_desfecho", "p1_intencao_entrada", "p1_tentativa_comercial",
    "p1_B1", "p1_B2", "p1_B3", "p1_B4", "p1_B5", "p1_B6", "p1_B7", "p1_B8", "p1_B9", "p1_B10",
    "p1_score_comercial",
    # P2
    "p2_tipo", "p2_subtipo", "p2_quem_iniciou",
    # P5
    "p5_teve_challenger", "p5_codigos_challenger", "p5_frase_resumo", "p5_resultado_imediato", "p5_qualidade",
    # P6
    "p6_oportunidades_perdidas", "p6_descricao_curta", "p6_valor_potencial_reais",
    # P9
    "p9_tipo_abertura", "p9_usou_nome", "p9_tipo_fechamento", "p9_proximo_passo_claro", "p9_prazo_definido", "p9_desfecho",
    # P10 (agregado por cliente+batch)
    "p10_num_promessas", "p10_tipos", "p10_risco_max",
    # P3 (exploratorio)
    "p3_amostrado", "p3_nota",
    # P7 (exploratorio)
    "p7_amostrado", "p7_nota",
    # P4/P8/P11/P13/P14/P15 (exploratorio, so novo lote)
    "p4_p8_p11_p13_p14_p15_amostrado", "p4_p8_p11_p13_p14_p15_nota",
]

rows_out = []
for sid, base_info in master.items():
    row = {k: "" for k in FIELDS}
    row["segment_id"] = sid
    row["base_origem"] = base_info["base_origem"]
    row["cliente_id"] = base_info["cliente_id"]
    row["data"] = base_info["data"]
    row["duracao_s"] = base_info["duracao_s"]
    row["sentimento"] = base_info["sentimento"]

    if sid in dados_p1:
        p1 = dados_p1[sid]
        row["p1_desfecho"] = p1["desfecho"]
        row["p1_intencao_entrada"] = p1["intencao_entrada"]
        row["p1_tentativa_comercial"] = p1["tentativa_comercial"]
        for b in [f"B{i}" for i in range(1, 11)]:
            row[f"p1_{b}"] = p1[b]
        row["p1_score_comercial"] = p1["score_comercial"]

    if sid in dados_p2:
        p2 = dados_p2[sid]
        row["p2_tipo"] = p2["tipo"]
        row["p2_subtipo"] = p2["subtipo"]
        row["p2_quem_iniciou"] = p2["quem_iniciou"]

    if sid in dados_p5:
        p5 = dados_p5[sid]
        row["p5_teve_challenger"] = p5["teve_challenger"]
        row["p5_codigos_challenger"] = p5["codigos_challenger"]
        row["p5_frase_resumo"] = p5["frase_resumo"]
        row["p5_resultado_imediato"] = p5["resultado_imediato"]
        row["p5_qualidade"] = p5["qualidade"]

    if sid in dados_p6:
        p6 = dados_p6[sid]
        row["p6_oportunidades_perdidas"] = p6["oportunidades_perdidas"]
        row["p6_descricao_curta"] = p6["descricao_curta"]
        row["p6_valor_potencial_reais"] = p6["valor_potencial_R$"]

    if sid in dados_p9:
        p9 = dados_p9[sid]
        row["p9_tipo_abertura"] = p9["tipo_abertura"]
        row["p9_usou_nome"] = p9["usou_nome"]
        row["p9_tipo_fechamento"] = p9["tipo_fechamento"]
        row["p9_proximo_passo_claro"] = p9["proximo_passo_claro"]
        row["p9_prazo_definido"] = p9["prazo_definido"]
        row["p9_desfecho"] = p9["desfecho_p9"]

    bc = sid_para_batch_cliente.get(sid)
    if bc and bc in dados_p10_agg:
        p10 = dados_p10_agg[bc]
        row["p10_num_promessas"] = p10["p10_num_promessas"]
        row["p10_tipos"] = p10["p10_tipos"]
        row["p10_risco_max"] = p10["p10_risco_max"]

    if sid in p3_p7_amostrado:
        row["p3_amostrado"] = "SIM"
        row["p7_amostrado"] = "SIM"
        if sid in p3_p7_nota:
            row["p3_nota"] = p3_p7_nota[sid]
            row["p7_nota"] = p3_p7_nota[sid]

    if sid in p4_amostrado:
        row["p4_p8_p11_p13_p14_p15_amostrado"] = "SIM"
        if sid in p4_nota:
            row["p4_p8_p11_p13_p14_p15_nota"] = p4_nota[sid]

    rows_out.append(row)

rows_out.sort(key=lambda r: (r["base_origem"], r["cliente_id"], r["data"]))

OUT_CSV.parent.mkdir(parents=True, exist_ok=True)
with open(OUT_CSV, "w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(rows_out)

print(f"\nCSV final escrito em: {OUT_CSV}")
print(f"Total de linhas: {len(rows_out)}")
