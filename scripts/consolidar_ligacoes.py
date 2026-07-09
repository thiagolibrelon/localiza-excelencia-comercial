"""
Consolida todas as analises (Gemini P1/P2/P5/P6/P9/P10 + exploracao Fable P3/P4/P7/P8/P11/P13/P14/P15)
num unico arquivo, 1 linha por ligacao (segment_id), 1 bloco de colunas por prompt.

Chave de identidade: segment_id (unico por ligacao nos dois arquivos-fonte).

Estrategia de casamento (matching):
- P1 e P9 sao as unicas tabelas que dao base para resolver segment_id com seguranca:
  P1 tem (cliente_id, data, duracao_s) -> chave exata contra a base bruta.
  As demais tabelas (P2, P5, P6, P9, P10) NAO tem duracao_s, entao sao encaixadas
  posicionalmente: dentro do MESMO arquivo (P2 encaixa com P1; P6 encaixa com P5),
  ou pelo MESMO numero de batch (P5/P6 e P9/P10 encaixam na ordem de segment_id
  já resolvida via P1_P2 daquele batch), agrupando por cliente_id e casando en
  ordem. Se a contagem de linhas por cliente_id nao bater entre as duas tabelas
  sendo casadas, essas linhas ficam sem casamento (nao inventamos posicao).
- P10 (promessas) e' tabela filha (0..N por ligacao) sem campo de ligacao unico
  -> agregada por cliente_id dentro do batch (nao por segment_id especifico) e
  replicada nas linhas desse cliente naquele batch. Ver colunas p10_*.
- P3/P7 (exploracao 456 ligacoes) e P4/P8/P11/P13/P14/P15 (exploracao 151 ligacoes,
  so novo lote) sao passes AGREGADOS (nao by-ligacao) - so os poucos exemplos
  citados como "Cliente <cod>" nos markdowns viram nota pontual. Colunas de
  "amostrado" (SIM/NAO) marcam quais ligacoes estavam no lote, mesmo sem nota.

Rodar de novo quando novos batches/exploracoes forem gerados - o script e' idempotente
(sempre relê tudo do zero e regera o CSV).
"""
import json
import re
import csv
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).parent.parent
OUT_CSV = ROOT / "resultados" / "consolidado" / "CONSOLIDADO_LIGACOES.csv"

# ---------------------------------------------------------------------------
# 1) Tabela mestre (todas as ligacoes, segment_id como chave)
# ---------------------------------------------------------------------------
def carregar_base(path, base_label):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    rows = {}
    for cid, calls in data.items():
        for call in calls:
            sid = call["segment_id"]
            rows[sid] = {
                "segment_id": sid,
                "base_origem": base_label,
                "cliente_id": cid,
                "data": call.get("data", "?")[:10],
                "duracao_s": str(call.get("duracao", "")),
                "sentimento": call.get("sentimento", ""),
            }
    return rows

print("Carregando bases brutas...")
master = {}
master.update(carregar_base(ROOT / "dados" / "LIG", "BASE_ANTIGA_1275"))
master.update(carregar_base(ROOT / "dados" / "recebidos" / "bloco_lig_recebido_01.json", "NOVO_LOTE_5348"))
print(f"Total de ligacoes na base mestre: {len(master)}")

# lookup (cliente_id, data, duracao_s) -> [segment_id,...]
key_p1 = defaultdict(list)
# lookup (cliente_id, data) -> [segment_id,...] em ordem de aparicao no JSON (usado p/ casar tabelas sem duracao)
key_dia = defaultdict(list)
for sid, r in master.items():
    key_p1[(r["cliente_id"], r["data"], r["duracao_s"])].append(sid)
    key_dia[(r["cliente_id"], r["data"])].append(sid)

colisoes_p1 = sum(1 for v in key_p1.values() if len(v) > 1)
print(f"Colisoes (cliente+data+duracao repetido): {colisoes_p1}")

# ---------------------------------------------------------------------------
# 2) Parsing generico de blocos CSV dentro de um arquivo de resposta do Gemini
# ---------------------------------------------------------------------------
def extrair_blocos_csv(texto, header_prefixes):
    """
    header_prefixes: lista ordenada de prefixos de header (ex: ["cliente_id,data,duracao",
    "cliente_id,data,tipo,"]) que marcam o INICIO de cada tabela, na ordem em que aparecem.
    Retorna dict {indice_da_tabela: [linhas_csv,...]} concatenando TODAS as ocorrencias
    (batches grandes divididos em 2 chamadas geram o padrao 2x).
    """
    tabelas = defaultdict(list)
    estado = None  # indice da tabela atual, ou None
    for line in texto.splitlines():
        s = line.strip()
        if not s or s.startswith("```") or s.startswith("#"):
            continue
        matched_novo = None
        for i, pref in enumerate(header_prefixes):
            if s.startswith(pref):
                matched_novo = i
                break
        if matched_novo is not None:
            estado = matched_novo
            continue
        if estado is not None:
            tabelas[estado].append(s)
    return tabelas

def parse_csv_linhas(linhas, n_campos_esperado, n_prefixo=None, n_sufixo=None):
    """
    n_prefixo/n_sufixo: quando informados, os campos entre o prefixo fixo e o
    sufixo fixo sao tratados como UM campo de texto livre (juntando de volta
    com virgula) - necessario porque o Gemini as vezes gera texto livre com
    virgula sem aspas, o que quebraria o alinhamento num split(",") ingenuo.
    """
    out = []
    for s in linhas:
        parts = [p.strip() for p in s.split(",")]
        if n_prefixo is not None and n_sufixo is not None:
            n_meio_esperado = n_campos_esperado - n_prefixo - n_sufixo  # normalmente 1
            if len(parts) < n_prefixo + n_sufixo + 1:
                continue
            prefixo = parts[:n_prefixo]
            sufixo = parts[-n_sufixo:] if n_sufixo > 0 else []
            meio = [",".join(parts[n_prefixo:len(parts)-n_sufixo])]
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

# ---------------------------------------------------------------------------
# 3) P1_P2 — resolve segment_id via (cliente,data,duracao); P2 encaixa por posicao no MESMO arquivo
# ---------------------------------------------------------------------------
P1_COLS = ["cliente_id","data","duracao_s","desfecho","intencao_entrada","tentativa_comercial",
           "B1","B2","B3","B4","B5","B6","B7","B8","B9","B10","score_comercial"]
P2_COLS = ["cliente_id","data","tipo","subtipo","quem_iniciou","tentativa_comercial"]

dados_p1 = {}   # segment_id -> dict campos P1
dados_p2 = {}   # segment_id -> dict campos P2
# ordem de segment_id resolvida por (base,batch_num,cliente_id) -> [segment_id em ordem]
ordem_por_batch = defaultdict(lambda: defaultdict(list))

nao_resolvidos_p1 = 0

def processar_p1_p2(path, base_label, batch_num):
    global nao_resolvidos_p1
    texto = path.read_text(encoding="utf-8")
    blocos = extrair_blocos_csv(texto, ["cliente_id,data,duracao", "cliente_id,data,tipo,"])
    linhas_p1 = parse_csv_linhas(blocos.get(0, []), len(P1_COLS))
    linhas_p2 = parse_csv_linhas(blocos.get(1, []), len(P2_COLS))

    # resolve segment_id para cada linha P1 via chave exata
    p1_resolvidas = []  # (segment_id, linha)
    for linha in linhas_p1:
        cid, data, dur = linha[0], linha[1], linha[2]
        candidatos = key_p1.get((cid, data, dur), [])
        # remove os que ja foram usados por OUTRA linha p1 deste mesmo processamento (evita reuso indevido)
        candidatos_livres = [c for c in candidatos if c not in dados_p1]
        alvo = candidatos_livres[0] if candidatos_livres else (candidatos[0] if candidatos else None)
        if alvo is None:
            nao_resolvidos_p1 += 1
            continue
        p1_resolvidas.append((alvo, linha))
        dados_p1[alvo] = dict(zip(P1_COLS, linha))
        ordem_por_batch[(base_label, batch_num)][cid].append(alvo)

    # encaixa P2 por posicao dentro do mesmo cliente_id, no mesmo arquivo
    p1_por_cliente = defaultdict(list)
    for sid, linha in p1_resolvidas:
        p1_por_cliente[linha[0]].append(sid)
    p2_por_cliente = agrupar_por_cliente(linhas_p2)
    for cid, sids in p1_por_cliente.items():
        linhas_c = p2_por_cliente.get(cid, [])
        for sid, linha in zip(sids, linhas_c):
            dados_p2[sid] = dict(zip(P2_COLS, linha))

# ---------------------------------------------------------------------------
# 4) P5_P6 — encaixa por (base,batch,cliente) usando a ordem ja resolvida em P1_P2
# ---------------------------------------------------------------------------
P5_COLS = ["cliente_id","data","teve_challenger","codigos_challenger","frase_resumo","resultado_imediato","qualidade"]
P6_COLS = ["cliente_id","data","oportunidades_perdidas","descricao_curta","valor_potencial_R$"]

dados_p5 = {}
dados_p6 = {}
nao_resolvidos_p5 = 0

def processar_p5_p6(path, base_label, batch_num):
    global nao_resolvidos_p5
    texto = path.read_text(encoding="utf-8")
    blocos = extrair_blocos_csv(texto, ["cliente_id,data,teve_challenger", "cliente_id,data,oportunidades_perdidas"])
    # frase_resumo (campo 4, indice 0-based) e' texto livre -> prefixo=4 (cliente,data,teve_challenger,codigos), sufixo=2 (resultado,qualidade)
    linhas_p5 = parse_csv_linhas(blocos.get(0, []), len(P5_COLS), n_prefixo=4, n_sufixo=2)
    # descricao_curta (campo 3) e' texto livre -> prefixo=3 (cliente,data,oportunidades), sufixo=1 (valor_potencial)
    linhas_p6 = parse_csv_linhas(blocos.get(1, []), len(P6_COLS), n_prefixo=3, n_sufixo=1)

    p5_por_cliente = agrupar_por_cliente(linhas_p5)
    ordem_batch = ordem_por_batch.get((base_label, batch_num), {})

    p5_resolvidas_por_cliente = defaultdict(list)
    for cid, linhas_c in p5_por_cliente.items():
        sids = ordem_batch.get(cid, [])
        if len(sids) != len(linhas_c):
            nao_resolvidos_p5 += len(linhas_c)
            continue
        for sid, linha in zip(sids, linhas_c):
            dados_p5[sid] = dict(zip(P5_COLS, linha))
            p5_resolvidas_por_cliente[cid].append(sid)

    p6_por_cliente = agrupar_por_cliente(linhas_p6)
    for cid, sids in p5_resolvidas_por_cliente.items():
        linhas_c = p6_por_cliente.get(cid, [])
        for sid, linha in zip(sids, linhas_c):
            dados_p6[sid] = dict(zip(P6_COLS, linha))

# ---------------------------------------------------------------------------
# 5) P9_P10 — P9 encaixa por (base,batch,cliente); P10 (promessas) agregado por cliente+batch
# ---------------------------------------------------------------------------
P9_COLS = ["cliente_id","data","tipo_abertura","usou_nome","tipo_fechamento","proximo_passo_claro","prazo_definido","desfecho_p9"]
P10_COLS_RAW = ["promise_id","cliente_id","data","tipo_promessa","frase_resumo","prazo_prometido","risco_nao_cumprimento"]

dados_p9 = {}
dados_p10_agg = {}  # (base,batch,cliente_id) -> dict resumo
nao_resolvidos_p9 = 0

def processar_p9_p10(path, base_label, batch_num):
    global nao_resolvidos_p9
    texto = path.read_text(encoding="utf-8")
    blocos = extrair_blocos_csv(texto, ["cliente_id,data,tipo_abertura", "promise_id,cliente_id"])
    linhas_p9 = parse_csv_linhas(blocos.get(0, []), len(P9_COLS))
    # frase_resumo (campo 4) e' texto livre -> prefixo=4 (promise_id,cliente,data,tipo_promessa), sufixo=2 (prazo,risco)
    linhas_p10 = parse_csv_linhas(blocos.get(1, []), len(P10_COLS_RAW), n_prefixo=4, n_sufixo=2)

    p9_por_cliente = agrupar_por_cliente(linhas_p9)
    ordem_batch = ordem_por_batch.get((base_label, batch_num), {})
    for cid, linhas_c in p9_por_cliente.items():
        sids = ordem_batch.get(cid, [])
        if len(sids) != len(linhas_c):
            nao_resolvidos_p9 += len(linhas_c)
            continue
        for sid, linha in zip(sids, linhas_c):
            dados_p9[sid] = dict(zip(P9_COLS, linha))

    p10_por_cliente = agrupar_por_cliente(linhas_p10, idx_cliente=1)
    for cid, linhas_c in p10_por_cliente.items():
        tipos = [l[3] for l in linhas_c]
        riscos = [l[6] for l in linhas_c]
        dados_p10_agg[(base_label, batch_num, cid)] = {
            "p10_num_promessas": str(len(linhas_c)),
            "p10_tipos": ";".join(tipos),
            "p10_risco_max": max(riscos, key=lambda r: {"baixo":0,"medio":1,"alto":2,"muito_alto":3}.get(r,0)) if riscos else "",
        }

# ---------------------------------------------------------------------------
# 6) roda os parsers em todos os arquivos das 2 bases
# ---------------------------------------------------------------------------
def batch_num_do_nome(nome):
    m = re.match(r"batch(\d+)_", nome)
    return int(m.group(1)) if m else None

print("\nProcessando P1_P2 (todas as bases)...")
for base_label, pasta in [("BASE_ANTIGA_1275", "gemini_v2"), ("NOVO_LOTE_5348", "gemini_novo_lote")]:
    arquivos = sorted((ROOT / "resultados" / pasta).glob("batch*_P1_P2_*.txt"),
                       key=lambda p: p.stat().st_size, reverse=True)
    vistos = set()
    for f in arquivos:
        bn = batch_num_do_nome(f.name)
        if bn in vistos:
            continue  # usa so o maior arquivo por batch (reprocessamentos anteriores)
        vistos.add(bn)
        processar_p1_p2(f, base_label, bn)
print(f"P1 resolvidas: {len(dados_p1)} | P2 resolvidas: {len(dados_p2)} | P1 nao resolvidas: {nao_resolvidos_p1}")

print("\nProcessando P5_P6 (todas as bases)...")
for base_label, pasta in [("BASE_ANTIGA_1275", "gemini_v2"), ("NOVO_LOTE_5348", "gemini_novo_lote")]:
    arquivos = sorted((ROOT / "resultados" / pasta).glob("batch*_P5_P6_*.txt"),
                       key=lambda p: p.stat().st_size, reverse=True)
    vistos = set()
    for f in arquivos:
        bn = batch_num_do_nome(f.name)
        if bn in vistos:
            continue
        vistos.add(bn)
        processar_p5_p6(f, base_label, bn)
print(f"P5 resolvidas: {len(dados_p5)} | P6 resolvidas: {len(dados_p6)} | P5 nao resolvidas (mismatch contagem): {nao_resolvidos_p5}")

print("\nProcessando P9_P10 (todas as bases)...")
for base_label, pasta in [("BASE_ANTIGA_1275", "gemini_v2"), ("NOVO_LOTE_5348", "gemini_novo_lote")]:
    arquivos = sorted((ROOT / "resultados" / pasta).glob("batch*_P9_P10_*.txt"),
                       key=lambda p: p.stat().st_size, reverse=True)
    vistos = set()
    for f in arquivos:
        bn = batch_num_do_nome(f.name)
        if bn in vistos:
            continue
        vistos.add(bn)
        processar_p9_p10(f, base_label, bn)
print(f"P9 resolvidas: {len(dados_p9)} | P9 nao resolvidas (mismatch contagem): {nao_resolvidos_p9}")
print(f"P10 (agregados por cliente+batch): {len(dados_p10_agg)}")

# mapa reverso sid -> (base,batch,cliente) para juntar p10 depois
sid_para_batch_cliente = {}
for (base_label, batch_num), por_cliente in ordem_por_batch.items():
    for cid, sids in por_cliente.items():
        for sid in sids:
            sid_para_batch_cliente[sid] = (base_label, batch_num, cid)

print("\nSalvando resultados intermediarios (pickle-like via json) para a Etapa 2 (exploracao Fable)...")
import pickle
with open(ROOT / "resultados" / "consolidado" / "_intermediario.pkl", "wb") as f:
    pickle.dump({
        "master": master,
        "dados_p1": dados_p1, "dados_p2": dados_p2,
        "dados_p5": dados_p5, "dados_p6": dados_p6,
        "dados_p9": dados_p9, "dados_p10_agg": dados_p10_agg,
        "sid_para_batch_cliente": sid_para_batch_cliente,
        "key_dia": dict(key_dia),
    }, f)
print("OK — etapa 1 concluida.")
