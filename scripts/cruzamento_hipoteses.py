"""
Cruzamento geral: junta P1_P2 (desfecho limpo + B1-B10) + P5_P6 (Challenger + OP)
+ P9_P10 (abertura/fechamento/promessas) por cliente_id+data, para dar suporte
quantitativo real a cada uma das 9 hipoteses -- nao so ao Challenger/fechamento.
"""
import re
from pathlib import Path
from collections import defaultdict, Counter

GEMINI_DIR = Path(__file__).parent.parent / "resultados" / "gemini_v2"


def arquivos_validos(padrao):
    por_batch = defaultdict(list)
    for f in GEMINI_DIR.glob(padrao):
        m = re.match(r"batch(\d+)_", f.name)
        if m:
            por_batch[m.group(1)].append(f)
    return [max(v, key=lambda x: x.stat().st_size) for v in por_batch.values()]


def norm_id(s):
    try:
        return str(int(s))
    except (ValueError, TypeError):
        return s.strip()


# ---------------------------------------------------------------------------
# 1) P1_P2 -- desfecho limpo + B1-B10
# ---------------------------------------------------------------------------
p1 = {}  # (cid, data) -> dict
for f in arquivos_validos("batch*_P1_P2_*.txt"):
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
        cid, data, desfecho = norm_id(parts[0]), parts[1].strip(), parts[3].strip()
        b_flags = {f"B{i+1}": parts[6 + i].strip().upper() == "SIM" for i in range(10)}
        p1[(cid, data)] = {"desfecho": desfecho, **b_flags}

print(f"P1_P2: {len(p1)} ligações indexadas")

# ---------------------------------------------------------------------------
# 2) P5_P6 -- Challenger (CH) + Oportunidades perdidas (OP)
# ---------------------------------------------------------------------------
p5 = {}  # (cid, data) -> dict
for f in arquivos_validos("batch*_P5_P6_*.txt"):
    in_p5 = in_p6 = False
    for line in f.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("cliente_id,data,teve_challenger"):
            in_p5, in_p6 = True, False
            continue
        if s.startswith("cliente_id,data,oportunidades_perdidas"):
            in_p5, in_p6 = False, True
            continue
        if s.startswith("```") or s.startswith("###"):
            in_p5 = in_p6 = False
            continue
        if in_p5 and s and not s.startswith("#"):
            parts = s.split(",")
            if len(parts) >= 4:
                cid, data = norm_id(parts[0]), parts[1].strip()
                teve = parts[2].strip().upper()
                codigos = [c.strip() for c in re.split(r"[|;]", parts[3]) if c.strip().startswith("CH")]
                entry = p5.setdefault((cid, data), {"CH": [], "OP": []})
                if teve == "SIM":
                    entry["CH"].extend(codigos)
        if in_p6 and s and not s.startswith("#"):
            parts = s.split(",", 4)
            if len(parts) >= 3:
                cid, data = norm_id(parts[0]), parts[1].strip()
                op = parts[2].strip()
                entry = p5.setdefault((cid, data), {"CH": [], "OP": []})
                if op and op != "nenhuma":
                    entry["OP"].extend([o.strip() for o in re.split(r"[|;]", op) if o.strip()])

print(f"P5_P6: {len(p5)} ligações indexadas")

# ---------------------------------------------------------------------------
# 3) P9_P10 -- Abertura (AB) + Fechamento (FC) + Promessas (PM)
# ---------------------------------------------------------------------------
p9 = {}  # (cid, data) -> dict
_AB = {"AB1", "AB2", "AB3", "AB4", "AB5"}
_FC = {"FC1", "FC2", "FC3", "FC4", "FC5"}
_PM = {"PM1", "PM2", "PM3", "PM4", "PM5", "PM6"}

for f in arquivos_validos("batch*_P9_P10_*.txt"):
    in_p9 = in_p10 = False
    for line in f.read_text(encoding="utf-8").splitlines():
        s = line.strip()
        if s.startswith("cliente_id,data,tipo_abertura"):
            in_p9, in_p10 = True, False
            continue
        if s.startswith("promise_id,"):
            in_p9, in_p10 = False, True
            continue
        if s.startswith("```") or s.startswith("==="):
            in_p9 = in_p10 = False
            continue
        if in_p9 and s and not s.startswith("#"):
            parts = s.split(",")
            if len(parts) >= 7:
                cid, data = norm_id(parts[0]), parts[1].strip()
                ab, fc, prazo = parts[2].strip().upper(), parts[4].strip().upper(), parts[6].strip().upper()
                if ab in _AB and fc in _FC:
                    p9[(cid, data)] = {"AB": ab, "FC": fc, "prazo": prazo == "SIM", "PM": []}
        if in_p10 and s and not s.startswith("#"):
            parts = s.split(",", 3)
            if len(parts) >= 4:
                cid, data = norm_id(parts[1]), parts[2].strip()
                pm = parts[3].split(",")[0].strip().upper() if len(parts) > 3 else ""
                # promise_id,cliente_id,data,tipo_promessa,...
                pm_field = s.split(",")
                if len(pm_field) >= 4:
                    pm_v = pm_field[3].strip().upper()
                    if pm_v in _PM:
                        entry = p9.setdefault((cid, data), {"AB": None, "FC": None, "prazo": False, "PM": []})
                        entry["PM"].append(pm_v)

print(f"P9_P10: {len(p9)} ligações indexadas")

# ---------------------------------------------------------------------------
# 4) JOIN por (cliente_id, data)
# ---------------------------------------------------------------------------
todas_keys = set(p1) | set(p5) | set(p9)
master = []
for key in todas_keys:
    row = {"cid": key[0], "data": key[1]}
    row.update(p1.get(key, {}))
    row["CH"] = p5.get(key, {}).get("CH", [])
    row["OP"] = p5.get(key, {}).get("OP", [])
    row["AB"] = p9.get(key, {}).get("AB")
    row["FC"] = p9.get(key, {}).get("FC")
    row["prazo"] = p9.get(key, {}).get("prazo", False)
    row["PM"] = p9.get(key, {}).get("PM", [])
    master.append(row)

n_com_desfecho = sum(1 for r in master if r.get("desfecho"))
n_com_fc = sum(1 for r in master if r.get("FC"))
n_com_ambos = sum(1 for r in master if r.get("desfecho") and r.get("FC"))
print(f"\nTotal ligações no master (união): {len(master)}")
print(f"  com desfecho (P1_P2): {n_com_desfecho}")
print(f"  com FC (P9_P10): {n_com_fc}")
print(f"  com AMBOS (join real): {n_com_ambos}")


def fechou(desfecho):
    return desfecho in ("fechou_novo", "fechou_renovacao", "fechou_upsell")


# ---------------------------------------------------------------------------
# HIPOTESE: Fechamento (H2) -- FC x desfecho LIMPO (join real)
# ---------------------------------------------------------------------------
print("\n=== H2 — FC (tipo de fechamento) x desfecho real (só linhas com join) ===")
fc_stats = defaultdict(lambda: Counter())
for r in master:
    if r.get("FC") and r.get("desfecho"):
        fc_stats[r["FC"]][r["desfecho"]] += 1
for fc in ["FC1", "FC2", "FC3", "FC4", "FC5"]:
    c = fc_stats.get(fc, Counter())
    total = sum(c.values())
    if not total:
        print(f"  {fc}: sem dados no join")
        continue
    fech = sum(c[d] for d in c if fechou(d))
    print(f"  {fc}: n={total} | fechou={fech} ({100*fech/total:.1f}%) | detalhe={dict(c)}")

# ---------------------------------------------------------------------------
# HIPOTESE: Challenger (CH) x desfecho LIMPO
# ---------------------------------------------------------------------------
print("\n=== Challenger — CH x desfecho real (só linhas com join) ===")
ch_stats = defaultdict(lambda: Counter())
for r in master:
    if r.get("desfecho"):
        for ch in r["CH"]:
            ch_stats[ch][r["desfecho"]] += 1
for ch, c in sorted(ch_stats.items(), key=lambda x: -sum(x[1].values())):
    total = sum(c.values())
    fech = sum(c[d] for d in c if fechou(d))
    print(f"  {ch}: n={total} | fechou={fech} ({100*fech/total:.1f}%) | detalhe={dict(c)}")

# ---------------------------------------------------------------------------
# HIPOTESE H4 — B10 (perguntou concorrente) x desfecho, e timing
# ---------------------------------------------------------------------------
print("\n=== H4 — B10 (perguntou concorrência) x desfecho ===")
b10_stats = Counter()
b10_total = Counter()
for r in master:
    if r.get("desfecho"):
        b10_total["com_B10" if r.get("B10") else "sem_B10"] += 1
        if fechou(r["desfecho"]):
            b10_stats["com_B10" if r.get("B10") else "sem_B10"] += 1
for k in ["com_B10", "sem_B10"]:
    t = b10_total.get(k, 0)
    f = b10_stats.get(k, 0)
    print(f"  {k}: n={t} | fechou={f} ({100*f/t:.1f}%)" if t else f"  {k}: sem dados")

# ---------------------------------------------------------------------------
# HIPOTESE H9 — PM2 (WhatsApp) frequência e prazo
# ---------------------------------------------------------------------------
print("\n=== H9 — Promessas: WhatsApp (PM2) vs outros tipos ===")
pm_counter = Counter()
for r in master:
    for pm in r["PM"]:
        pm_counter[pm] += 1
total_pm = sum(pm_counter.values())
for pm, n in pm_counter.most_common():
    print(f"  {pm}: {n} ({100*n/total_pm:.1f}%)" if total_pm else "")

# ---------------------------------------------------------------------------
# HIPOTESE H8 — OP4 (referral não pedido) frequência
# ---------------------------------------------------------------------------
print("\n=== H8 — Oportunidades perdidas (OP1-OP8) frequência ===")
op_counter = Counter()
for r in master:
    for op in r["OP"]:
        op_counter[op] += 1
total_op = sum(op_counter.values())
for op, n in op_counter.most_common():
    print(f"  {op}: {n} ({100*n/total_op:.1f}%)")

# ---------------------------------------------------------------------------
# HIPOTESE: Abertura (AB) x desfecho
# ---------------------------------------------------------------------------
print("\n=== Abertura (AB1-AB5) x desfecho ===")
ab_stats = defaultdict(lambda: Counter())
for r in master:
    if r.get("AB") and r.get("desfecho"):
        ab_stats[r["AB"]][r["desfecho"]] += 1
for ab, c in sorted(ab_stats.items(), key=lambda x: -sum(x[1].values())):
    total = sum(c.values())
    fech = sum(c[d] for d in c if fechou(d))
    print(f"  {ab}: n={total} | fechou={fech} ({100*fech/total:.1f}%)")
