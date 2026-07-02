"""
Tenta isolar se a LIGACAO gerou a reserva, nao so se coincidiu no tempo.

Duas analises:
  A) RITMO ANTES x DEPOIS: para cada ligacao, compara quantas reservas o
     cliente abriu nos 30 dias ANTES vs 30 dias DEPOIS da ligacao. Cada
     cliente e' seu proprio controle (isola o ruido de clientes que ja
     reservam muito o tempo todo). Compara o delta medio entre categorias
     de desfecho -- se fechou_* tem delta maior que nao_era_venda, e' sinal
     real de impacto, nao coincidencia de base ativa.

  B) PRIMEIRA RESERVA DA VIDA: para ligacoes fechou_novo, usa o historico
     completo (2013-2026) para checar se a reserva mais proxima da ligacao
     e' a PRIMEIRA reserva que esse cliente ja fez. Sinal mais limpo de
     conversao real de cliente novo.
"""
import csv
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

GEMINI_DIR   = Path(__file__).parent.parent / "resultados" / "gemini_v2"
RESERVAS_CSV = Path(__file__).parent.parent / "dados" / "recebidos" / "reservas_jun_jul.csv"
OUT_A        = Path(__file__).parent.parent / "resultados" / "cruzamento_ritmo.csv"
OUT_B        = Path(__file__).parent.parent / "resultados" / "cruzamento_primeira_reserva.csv"

JANELA = 30  # dias antes / depois


def norm_id(s):
    try:
        return str(int(s))
    except (ValueError, TypeError):
        return s


def parse_data_hora(s):
    s = (s or "").strip()
    if not s:
        return None
    for fmt in ("%d/%m/%Y %H:%M", "%d/%m/%Y"):
        try:
            return datetime.strptime(s, fmt)
        except ValueError:
            continue
    return None


# ---------------------------------------------------------------------------
# Carrega ligacoes classificadas (maior arquivo valido por batch)
# ---------------------------------------------------------------------------
por_batch = defaultdict(list)
for f in GEMINI_DIR.glob("batch*_P1_P2_*.txt"):
    m = re.match(r"batch(\d+)_P1_P2_", f.name)
    if m:
        por_batch[m.group(1)].append(f)
arquivos_validos = [max(v, key=lambda x: x.stat().st_size) for v in por_batch.values()]

chamadas = []
for f in sorted(arquivos_validos):
    in_p1 = False
    for line in f.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("cliente_id,data,duracao"):
            in_p1 = True
            continue
        if s.startswith("cliente_id,data,tipo,"):
            in_p1 = False
            continue
        if not in_p1 or not s or s.startswith("#") or s.startswith("```"):
            continue
        parts = s.split(",")
        if len(parts) < 16:
            continue
        if len(parts) == 16:
            parts.insert(5, "desconhecido")
        cid, data_str, desfecho = parts[0].strip(), parts[1].strip(), parts[3].strip()
        try:
            data_lig = datetime.strptime(data_str, "%Y-%m-%d")
        except ValueError:
            continue
        chamadas.append((norm_id(cid), data_lig, desfecho))

print(f"Ligacoes classificadas: {len(chamadas)}")

# ---------------------------------------------------------------------------
# Carrega TODAS as datas de reserva por cliente (historico completo, 2013-2026)
# ---------------------------------------------------------------------------
reservas_por_cliente = defaultdict(list)
with open(RESERVAS_CSV, encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter=";"):
        cid = norm_id(row["CODIGO_VENCEDOR"])
        d = parse_data_hora(row.get("data_criacao_reserva")) or parse_data_hora(row.get("data_fechamento_efetiva"))
        if d:
            reservas_por_cliente[cid].append(d)
for cid in reservas_por_cliente:
    reservas_por_cliente[cid].sort()

# ---------------------------------------------------------------------------
# ANALISE A -- ritmo antes x depois (cliente e' seu proprio controle)
# ---------------------------------------------------------------------------
linhas_a = []
for cid, data_lig, desfecho in chamadas:
    todas = reservas_por_cliente.get(cid, [])
    if not todas:
        continue
    antes  = sum(1 for d in todas if data_lig - timedelta(days=JANELA) <= d < data_lig)
    depois = sum(1 for d in todas if data_lig <= d <= data_lig + timedelta(days=JANELA))
    linhas_a.append({
        "cliente_id": cid, "data_ligacao": data_lig.strftime("%Y-%m-%d"),
        "desfecho_ia": desfecho, "reservas_antes_30d": antes,
        "reservas_depois_30d": depois, "delta": depois - antes,
    })

with open(OUT_A, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(linhas_a[0].keys()))
    w.writeheader()
    w.writerows(linhas_a)

print(f"\nSalvo: {OUT_A}")
print(f"\n=== A) RITMO DE RESERVAS ANTES x DEPOIS (janela {JANELA}d, cliente e' o proprio controle) ===")
print(f"{'desfecho_ia':<25} {'n':>6} {'media_antes':>13} {'media_depois':>13} {'delta_medio':>13}")
por_desfecho_a = defaultdict(list)
for r in linhas_a:
    por_desfecho_a[r["desfecho_ia"]].append(r)
for desfecho, rs in sorted(por_desfecho_a.items(), key=lambda x: -len(x[1])):
    n = len(rs)
    m_antes  = sum(r["reservas_antes_30d"] for r in rs) / n
    m_depois = sum(r["reservas_depois_30d"] for r in rs) / n
    m_delta  = sum(r["delta"] for r in rs) / n
    print(f"{desfecho:<25} {n:>6} {m_antes:>13.2f} {m_depois:>13.2f} {m_delta:>13.2f}")

# ---------------------------------------------------------------------------
# ANALISE B -- primeira reserva da vida (so faz sentido para fechou_novo)
# ---------------------------------------------------------------------------
linhas_b = []
for cid, data_lig, desfecho in chamadas:
    if desfecho != "fechou_novo":
        continue
    todas = reservas_por_cliente.get(cid, [])
    if not todas:
        continue
    # reserva mais proxima da ligacao dentro de +/-30d
    candidatas = [d for d in todas if abs((d - data_lig).days) <= JANELA]
    if not candidatas:
        continue
    mais_proxima = min(candidatas, key=lambda d: abs((d - data_lig).days))
    primeira_da_vida = todas[0]
    e_primeira = (mais_proxima == primeira_da_vida)
    linhas_b.append({
        "cliente_id": cid, "data_ligacao": data_lig.strftime("%Y-%m-%d"),
        "reserva_mais_proxima": mais_proxima.strftime("%Y-%m-%d"),
        "primeira_reserva_historico": primeira_da_vida.strftime("%Y-%m-%d"),
        "e_primeira_reserva_da_vida": e_primeira,
        "total_reservas_historico": len(todas),
    })

if linhas_b:
    with open(OUT_B, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas_b[0].keys()))
        w.writeheader()
        w.writerows(linhas_b)
    print(f"\nSalvo: {OUT_B}")

n_b = len(linhas_b)
n_primeira = sum(1 for r in linhas_b if r["e_primeira_reserva_da_vida"])
print(f"\n=== B) PRIMEIRA RESERVA DA VIDA (so fechou_novo, historico 2013-2026) ===")
print(f"Ligacoes fechou_novo com cliente no universo de reservas: {n_b}")
print(f"Dessas, a reserva mais proxima E a primeira reserva da vida do cliente: {n_primeira} ({100*n_primeira/n_b:.1f}%)" if n_b else "sem dados")
