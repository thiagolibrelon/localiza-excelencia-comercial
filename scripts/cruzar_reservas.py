"""
Cruza o desfecho classificado pela IA (fechou/interessou/nao_era_venda) nas
1.275 ligacoes originais com o historico real de reservas, para validar se
"fechou" nos dados da IA corresponde a uma reserva de fato criada/fechada
perto da data da ligacao.

Output: resultados/cruzamento_reservas.csv e relatorio no console.
"""
import csv
import re
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict, Counter

GEMINI_DIR   = Path(__file__).parent.parent / "resultados" / "gemini_v2"
RESERVAS_CSV = Path(__file__).parent.parent / "dados" / "recebidos" / "reservas_jun_jul.csv"
OUTPUT_CSV   = Path(__file__).parent.parent / "resultados" / "cruzamento_reservas.csv"

JANELA_ANTES = 3    # dias antes da ligacao ainda conta (reserva feita pouco antes de retornar a ligacao)
JANELA_DEPOIS = 30  # dias depois da ligacao para considerar "resultado da ligacao"


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
# 1) Carrega desfechos classificados pela IA (P1_P2), pegando o maior arquivo
#    valido por numero de batch (evita duplicata de reprocessamento)
# ---------------------------------------------------------------------------
por_batch = defaultdict(list)
for f in GEMINI_DIR.glob("batch*_P1_P2_*.txt"):
    m = re.match(r"batch(\d+)_P1_P2_", f.name)
    if m:
        por_batch[m.group(1)].append(f)

arquivos_validos = []
for b, files in por_batch.items():
    melhor = max(files, key=lambda x: x.stat().st_size)
    arquivos_validos.append(melhor)

chamadas = []  # (cliente_id_norm, data_ligacao, desfecho)
for f in sorted(arquivos_validos):
    content = f.read_text(encoding="utf-8")
    in_p1 = False
    for line in content.splitlines():
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

print(f"Ligacoes classificadas carregadas: {len(chamadas)}")

# ---------------------------------------------------------------------------
# 2) Carrega reservas: cliente_id_norm -> lista de datas relevantes
#    (prioriza data_criacao_reserva; se vazia, usa data_fechamento_efetiva)
# ---------------------------------------------------------------------------
reservas_por_cliente = defaultdict(list)
with open(RESERVAS_CSV, encoding="utf-8") as f:
    for row in csv.DictReader(f, delimiter=";"):
        cid = norm_id(row["CODIGO_VENCEDOR"])
        d_criacao = parse_data_hora(row.get("data_criacao_reserva"))
        d_fecha   = parse_data_hora(row.get("data_fechamento_efetiva"))
        d_ref = d_criacao or d_fecha
        if d_ref:
            reservas_por_cliente[cid].append(d_ref)

for cid in reservas_por_cliente:
    reservas_por_cliente[cid].sort()

print(f"Clientes com reserva datada: {len(reservas_por_cliente)}")

# ---------------------------------------------------------------------------
# 3) Cruza: para cada ligacao, ha reserva na janela [-JANELA_ANTES, +JANELA_DEPOIS] dias?
# ---------------------------------------------------------------------------
resultado = []
for cid, data_lig, desfecho in chamadas:
    datas_reserva = reservas_por_cliente.get(cid, [])
    tem_reserva_proxima = False
    dias_ate_reserva = ""
    for d in datas_reserva:
        delta = (d - data_lig).days
        if -JANELA_ANTES <= delta <= JANELA_DEPOIS:
            tem_reserva_proxima = True
            dias_ate_reserva = delta
            break
    resultado.append({
        "cliente_id": cid,
        "data_ligacao": data_lig.strftime("%Y-%m-%d"),
        "desfecho_ia": desfecho,
        "tem_cliente_na_base_reservas": cid in reservas_por_cliente,
        "tem_reserva_proxima": tem_reserva_proxima,
        "dias_ate_reserva": dias_ate_reserva,
    })

OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
    w = csv.DictWriter(f, fieldnames=list(resultado[0].keys()))
    w.writeheader()
    w.writerows(resultado)

# ---------------------------------------------------------------------------
# 4) Relatorio agregado por desfecho
# ---------------------------------------------------------------------------
print(f"\nSalvo: {OUTPUT_CSV}")
print(f"\nJanela usada: -{JANELA_ANTES} a +{JANELA_DEPOIS} dias da ligacao\n")

por_desfecho = defaultdict(list)
for r in resultado:
    por_desfecho[r["desfecho_ia"]].append(r)

print(f"{'desfecho_ia':<25} {'n_ligacoes':>10} {'no_universo_reservas':>20} {'com_reserva_proxima':>20} {'%_validado':>12}")
for desfecho, linhas in sorted(por_desfecho.items(), key=lambda x: -len(x[1])):
    n = len(linhas)
    no_universo = sum(1 for r in linhas if r["tem_cliente_na_base_reservas"])
    com_reserva = sum(1 for r in linhas if r["tem_reserva_proxima"])
    pct = f"{100*com_reserva/no_universo:.1f}%" if no_universo else "n/a"
    print(f"{desfecho:<25} {n:>10} {no_universo:>20} {com_reserva:>20} {pct:>12}")
