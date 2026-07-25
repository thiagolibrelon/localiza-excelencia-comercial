"""
Consolida os batches Gemini de JULHO/resultados_gemini/*.txt.

Gera 2 tipos de saida em JULHO/consolidado/:
  1) Um CSV por prompt (P1.csv, P2.csv, P5.csv, P6.csv, P9.csv, P10.csv) —
     linhas cruas, exatamente como o Gemini devolveu, sem cruzamento.
  2) CONSOLIDADO_JULHO.csv — REGRA DE NEGOCIO MANDATORIA: 1 linha por
     segment_id (rastreabilidade total), com todos os prompts (P1/P2/P5/P6/P9/P10)
     juntos na mesma linha. Toda ligacao da base aparece, mesmo que ainda nao
     tenha sido processada por algum prompt (campos ficam em branco - nao
     inventamos valor pra ligacao ainda nao analisada).

Estrategia de casamento (identica a scripts/consolidar_ligacoes.py, adaptada
pra 1 base so):
  - P1 e' a unica tabela com (cliente_id, data, duracao_s) -> chave exata
    contra JULHO/dados_convertidos/julho_completo.json, entao resolve
    segment_id com seguranca.
  - As demais tabelas do MESMO arquivo (P2 dentro de P1_P2) ou do MESMO
    numero de batch (P5/P6 e P9/P10, batch_index.json garante que o numero
    de batch de um cliente e' estavel entre grupos) encaixam POSICIONALMENTE:
    agrupa por cliente_id e casa em ordem. Se a contagem de linhas por
    cliente_id nao bater entre as tabelas sendo casadas, essas linhas ficam
    sem casamento (nao inventamos posicao) e entram no contador de
    "nao resolvidos" impresso no final.
  - P10 (promessas) e' tabela filha (0..N por ligacao) sem campo de ligacao
    unico -> agregada por cliente_id dentro do batch e replicada nas linhas
    desse cliente naquele batch (colunas p10_*).

Idempotente: sempre rele tudo do zero e reescreve os CSVs. Roda depois de
analisar_gemini_julho.py (ver run_gemini_julho_daily.bat).
"""
import csv
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).parent.parent
IN_DIR = ROOT / "JULHO" / "resultados_gemini"
OUT_DIR = ROOT / "JULHO" / "consolidado"
MASTER_JSON = ROOT / "JULHO" / "dados_convertidos" / "julho_completo.json"

# ---------------------------------------------------------------------------
# Definicao de cada prompt: colunas e onde estao os campos de texto livre
# (numero de colunas fixas ANTES e DEPOIS do campo de texto livre, que pode
# conter virgula sem aspas e quebraria um split(",") ingenuo)
# ---------------------------------------------------------------------------
P1_COLS = ["cliente_id", "data", "duracao_s", "desfecho", "intencao_entrada", "tentativa_comercial",
           "B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9", "B10", "score_comercial"]
P2_COLS = ["cliente_id", "data", "tipo", "subtipo", "quem_iniciou", "tentativa_comercial"]
P5_COLS = ["cliente_id", "data", "teve_challenger", "codigos_challenger", "frase_resumo", "resultado_imediato", "qualidade"]
P6_COLS = ["cliente_id", "data", "oportunidades_perdidas", "descricao_curta", "valor_potencial_R$"]
P9_COLS = ["cliente_id", "data", "tipo_abertura", "usou_nome", "tipo_fechamento", "proximo_passo_claro", "prazo_definido", "desfecho_p9"]
P10_COLS = ["promise_id", "cliente_id", "data", "tipo_promessa", "frase_resumo", "prazo_prometido", "risco_nao_cumprimento"]

# grupo de arquivo -> [(header_prefix, nome_prompt, cols, n_prefixo, n_sufixo), ...]
GRUPOS = {
    "P1_P2": [
        ("cliente_id,data,duracao", "P1", P1_COLS, None, None),
        ("cliente_id,data,tipo,", "P2", P2_COLS, None, None),
    ],
    "P5_P6": [
        ("cliente_id,data,teve_challenger", "P5", P5_COLS, 4, 2),   # frase_resumo = campo livre
        ("cliente_id,data,oportunidades_perdidas", "P6", P6_COLS, 3, 1),  # descricao_curta = campo livre
    ],
    "P9_P10": [
        ("cliente_id,data,tipo_abertura", "P9", P9_COLS, None, None),
        ("promise_id,cliente_id", "P10", P10_COLS, 4, 2),  # frase_resumo = campo livre
    ],
}

# ---------------------------------------------------------------------------
# Parsing (identico a scripts/consolidar_ligacoes.py)
# ---------------------------------------------------------------------------
def extrair_blocos_csv(texto, header_prefixes):
    tabelas = defaultdict(list)
    estado = None
    for line in texto.splitlines():
        s = line.strip()
        if not s or s.startswith("```") or s.startswith("#"):
            continue
        matched = None
        for i, pref in enumerate(header_prefixes):
            if s.startswith(pref):
                matched = i
                break
        if matched is not None:
            estado = matched
            continue
        if estado is not None:
            tabelas[estado].append(s)
    return tabelas

def parse_csv_linhas(linhas, n_campos_esperado, n_prefixo=None, n_sufixo=None):
    out = []
    for s in linhas:
        parts = [p.strip() for p in s.split(",")]
        if n_prefixo is not None and n_sufixo is not None:
            if len(parts) < n_prefixo + n_sufixo + 1:
                continue
            prefixo = parts[:n_prefixo]
            sufixo = parts[-n_sufixo:] if n_sufixo > 0 else []
            meio = [",".join(parts[n_prefixo:len(parts) - n_sufixo])]
            parts = prefixo + meio + sufixo
        else:
            if len(parts) == n_campos_esperado - 1:
                parts.insert(5, "desconhecido")  # normaliza P1 com 16 campos (falta tentativa_comercial)
            if len(parts) < n_campos_esperado:
                continue
        out.append(parts[:n_campos_esperado])
    return out

def agrupar_por_cliente(linhas, idx_cliente=0):
    grupos = defaultdict(list)
    for linha in linhas:
        grupos[linha[idx_cliente]].append(linha)
    return grupos

def batch_num_do_nome(nome):
    m = re.match(r"batch(\d+)_", nome)
    return int(m.group(1)) if m else None

def arquivos_validos_por_batch(grupo):
    """1 arquivo por numero de batch — o maior (batches truncados geram
    arquivo pequeno; a proxima execucao apaga e regrava o valido)."""
    arquivos = sorted(IN_DIR.glob(f"batch*_{grupo}_*.txt"), key=lambda p: p.stat().st_size, reverse=True)
    vistos = set()
    escolhidos = []
    for f in arquivos:
        bn = batch_num_do_nome(f.name)
        if bn is None or bn in vistos:
            continue
        vistos.add(bn)
        escolhidos.append(f)
    return sorted(escolhidos, key=lambda f: batch_num_do_nome(f.name))

# ---------------------------------------------------------------------------
# Master (segment_id -> dados brutos da ligacao)
# ---------------------------------------------------------------------------
def carregar_master():
    with open(MASTER_JSON, encoding="utf-8") as f:
        data = json.load(f)
    rows = {}
    for cid, calls in data.items():
        for call in calls:
            sid = call["segment_id"]
            rows[sid] = {
                "segment_id": sid,
                "cliente_id": cid,
                "data": call.get("data", "?")[:10],
                "duracao_s": str(call.get("duracao", "")),
                "sentimento": call.get("sentimento", ""),
            }
    return rows

# ---------------------------------------------------------------------------
# Resolucao de segment_id por prompt
# ---------------------------------------------------------------------------
dados_p1, dados_p2 = {}, {}
dados_p5, dados_p6 = {}, {}
dados_p9 = {}
dados_p10_agg = {}  # (batch_num, cliente_id) -> dict resumo
ordem_por_batch = defaultdict(lambda: defaultdict(list))  # batch_num -> cliente_id -> [segment_id em ordem]

nao_resolvidos = {"p1": 0, "p2": 0, "p5": 0, "p6": 0, "p9": 0, "p10": 0}

def processar_p1_p2(path, batch_num, key_p1):
    texto = path.read_text(encoding="utf-8")
    blocos = extrair_blocos_csv(texto, ["cliente_id,data,duracao", "cliente_id,data,tipo,"])
    linhas_p1 = parse_csv_linhas(blocos.get(0, []), len(P1_COLS))
    linhas_p2 = parse_csv_linhas(blocos.get(1, []), len(P2_COLS))

    p1_resolvidas = []
    for linha in linhas_p1:
        cid, data, dur = linha[0], linha[1], linha[2]
        candidatos = key_p1.get((cid, data, dur), [])
        candidatos_livres = [c for c in candidatos if c not in dados_p1]
        alvo = candidatos_livres[0] if candidatos_livres else (candidatos[0] if candidatos else None)
        if alvo is None:
            nao_resolvidos["p1"] += 1
            continue
        p1_resolvidas.append((alvo, linha))
        dados_p1[alvo] = dict(zip(P1_COLS, linha))
        ordem_por_batch[batch_num][cid].append(alvo)

    p1_por_cliente = defaultdict(list)
    for sid, linha in p1_resolvidas:
        p1_por_cliente[linha[0]].append(sid)
    p2_por_cliente = agrupar_por_cliente(linhas_p2)
    for cid, sids in p1_por_cliente.items():
        linhas_c = p2_por_cliente.get(cid, [])
        if len(sids) != len(linhas_c):
            nao_resolvidos["p2"] += abs(len(sids) - len(linhas_c))
        for sid, linha in zip(sids, linhas_c):
            dados_p2[sid] = dict(zip(P2_COLS, linha))

def processar_p5_p6(path, batch_num):
    texto = path.read_text(encoding="utf-8")
    blocos = extrair_blocos_csv(texto, ["cliente_id,data,teve_challenger", "cliente_id,data,oportunidades_perdidas"])
    linhas_p5 = parse_csv_linhas(blocos.get(0, []), len(P5_COLS), n_prefixo=4, n_sufixo=2)
    linhas_p6 = parse_csv_linhas(blocos.get(1, []), len(P6_COLS), n_prefixo=3, n_sufixo=1)

    p5_por_cliente = agrupar_por_cliente(linhas_p5)
    ordem_batch = ordem_por_batch.get(batch_num, {})

    p5_resolvidas_por_cliente = defaultdict(list)
    for cid, linhas_c in p5_por_cliente.items():
        sids = ordem_batch.get(cid, [])
        if len(sids) != len(linhas_c):
            nao_resolvidos["p5"] += len(linhas_c)
            continue
        for sid, linha in zip(sids, linhas_c):
            dados_p5[sid] = dict(zip(P5_COLS, linha))
            p5_resolvidas_por_cliente[cid].append(sid)

    p6_por_cliente = agrupar_por_cliente(linhas_p6)
    for cid, sids in p5_resolvidas_por_cliente.items():
        linhas_c = p6_por_cliente.get(cid, [])
        if len(sids) != len(linhas_c):
            nao_resolvidos["p6"] += abs(len(sids) - len(linhas_c))
        for sid, linha in zip(sids, linhas_c):
            dados_p6[sid] = dict(zip(P6_COLS, linha))

def processar_p9_p10(path, batch_num):
    texto = path.read_text(encoding="utf-8")
    blocos = extrair_blocos_csv(texto, ["cliente_id,data,tipo_abertura", "promise_id,cliente_id"])
    linhas_p9 = parse_csv_linhas(blocos.get(0, []), len(P9_COLS))
    linhas_p10 = parse_csv_linhas(blocos.get(1, []), len(P10_COLS), n_prefixo=4, n_sufixo=2)

    p9_por_cliente = agrupar_por_cliente(linhas_p9)
    ordem_batch = ordem_por_batch.get(batch_num, {})
    for cid, linhas_c in p9_por_cliente.items():
        sids = ordem_batch.get(cid, [])
        if len(sids) != len(linhas_c):
            nao_resolvidos["p9"] += len(linhas_c)
            continue
        for sid, linha in zip(sids, linhas_c):
            dados_p9[sid] = dict(zip(P9_COLS, linha))

    p10_por_cliente = agrupar_por_cliente(linhas_p10, idx_cliente=1)
    for cid, linhas_c in p10_por_cliente.items():
        if cid not in ordem_batch:
            nao_resolvidos["p10"] += len(linhas_c)
            continue
        tipos = [l[3] for l in linhas_c]
        riscos = [l[6] for l in linhas_c]
        dados_p10_agg[(batch_num, cid)] = {
            "p10_num_promessas": str(len(linhas_c)),
            "p10_tipos": ";".join(tipos),
            "p10_risco_max": max(riscos, key=lambda r: {"baixo": 0, "medio": 1, "alto": 2, "muito_alto": 3}.get(r, 0)) if riscos else "",
        }

# ---------------------------------------------------------------------------
# Saida 1: CSV cru por prompt (mantido para depuracao/inspecao rapida)
# ---------------------------------------------------------------------------
def escrever_csvs_por_prompt():
    linhas_por_prompt = defaultdict(list)
    cols_por_prompt = {}
    for grupo, specs in GRUPOS.items():
        header_prefixes = [spec[0] for spec in specs]
        for f in arquivos_validos_por_batch(grupo):
            texto = f.read_text(encoding="utf-8")
            blocos = extrair_blocos_csv(texto, header_prefixes)
            for i, (_, nome_prompt, cols, n_pref, n_suf) in enumerate(specs):
                cols_por_prompt[nome_prompt] = cols
                linhas_por_prompt[nome_prompt].extend(parse_csv_linhas(blocos.get(i, []), len(cols), n_pref, n_suf))

    for nome_prompt, cols in cols_por_prompt.items():
        out_path = OUT_DIR / f"{nome_prompt}.csv"
        with open(out_path, "w", encoding="utf-8", newline="") as fp:
            writer = csv.writer(fp)
            writer.writerow(cols)
            writer.writerows(linhas_por_prompt[nome_prompt])
        print(f"  -> {out_path.relative_to(ROOT)}: {len(linhas_por_prompt[nome_prompt])} linhas")

# ---------------------------------------------------------------------------
# Saida 2: CONSOLIDADO_JULHO.csv — 1 linha por segment_id, todos os prompts juntos
# ---------------------------------------------------------------------------
FIELDS_MASTER = [
    "segment_id", "cliente_id", "data", "duracao_s", "sentimento",
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
]

def escrever_consolidado(master):
    sid_para_batch_cliente = {}
    for batch_num, por_cliente in ordem_por_batch.items():
        for cid, sids in por_cliente.items():
            for sid in sids:
                sid_para_batch_cliente[sid] = (batch_num, cid)

    rows_out = []
    for sid, base_info in master.items():
        row = {k: "" for k in FIELDS_MASTER}
        row["segment_id"] = sid
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

        rows_out.append(row)

    rows_out.sort(key=lambda r: (r["cliente_id"], r["data"]))

    out_path = OUT_DIR / "CONSOLIDADO_JULHO.csv"
    with open(out_path, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS_MASTER)
        writer.writeheader()
        writer.writerows(rows_out)

    print(f"\n-> {out_path.relative_to(ROOT)}: {len(rows_out)} linhas (1 por segment_id)")
    print(f"   cobertura: P1={len(dados_p1)} P2={len(dados_p2)} P5={len(dados_p5)} P6={len(dados_p6)} P9={len(dados_p9)} P10(clientes/batch)={len(dados_p10_agg)}")
    print(f"   nao resolvidos (mismatch de contagem, nao inventado): {nao_resolvidos}")

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    print("Carregando base mestre (JULHO/dados_convertidos/julho_completo.json)...")
    master = carregar_master()
    print(f"Total de ligacoes na base mestre: {len(master)}")

    key_p1 = defaultdict(list)
    for sid, r in master.items():
        key_p1[(r["cliente_id"], r["data"], r["duracao_s"])].append(sid)

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    print("\nProcessando P1_P2...")
    for f in arquivos_validos_por_batch("P1_P2"):
        processar_p1_p2(f, batch_num_do_nome(f.name), key_p1)
    print(f"P1 resolvidas: {len(dados_p1)} | P2 resolvidas: {len(dados_p2)}")

    print("\nProcessando P5_P6...")
    for f in arquivos_validos_por_batch("P5_P6"):
        processar_p5_p6(f, batch_num_do_nome(f.name))
    print(f"P5 resolvidas: {len(dados_p5)} | P6 resolvidas: {len(dados_p6)}")

    print("\nProcessando P9_P10...")
    for f in arquivos_validos_por_batch("P9_P10"):
        processar_p9_p10(f, batch_num_do_nome(f.name))
    print(f"P9 resolvidas: {len(dados_p9)} | P10 (agregados por cliente+batch): {len(dados_p10_agg)}")

    print("\nEscrevendo CSVs por prompt (JULHO/consolidado/)...")
    escrever_csvs_por_prompt()

    escrever_consolidado(master)
    print("\nOK - consolidacao concluida.")

if __name__ == "__main__":
    main()
