"""
Amostra estratificada (~1.350 ligacoes, proporcional entre base antiga e novo lote)
para exploracao P3 (problemas recorrentes) + P7 (cross-sell/upsell) via Fable.
Gera lotes pequenos (~38 ligacoes/lote, seguro para contexto de um agente) em
resultados/exploracao_fable/inputs/.
"""
import json
import random
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT_DIR = ROOT / "resultados" / "exploracao_fable" / "inputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

SEED = 42
AMOSTRA_TOTAL = 1350
BATCH_SIZE_LIGACOES = 38

def carregar(path, base_label):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    items = []
    for cid, calls in data.items():
        for call in calls:
            items.append((base_label, cid, call))
    return items

antiga = carregar(ROOT / "dados" / "LIG", "BASE_ANTIGA_1275")
nova   = carregar(ROOT / "dados" / "recebidos" / "bloco_lig_recebido_01.json", "NOVO_LOTE_5348")

total_real = len(antiga) + len(nova)
frac = AMOSTRA_TOTAL / total_real
n_antiga = round(len(antiga) * frac)
n_nova   = round(len(nova) * frac)

random.seed(SEED)
amostra_antiga = random.sample(antiga, n_antiga)
amostra_nova   = random.sample(nova, n_nova)
amostra = amostra_antiga + amostra_nova
random.shuffle(amostra)

print(f"Base antiga: {len(antiga)} total -> amostra {n_antiga}")
print(f"Novo lote:   {len(nova)} total -> amostra {n_nova}")
print(f"Amostra total: {len(amostra)}")

def formatar(base_label, cid, call):
    conv = "\n".join(f"{s}: {t}" for s, t in call.get("conversa", []))
    return (
        f"=== LIGACAO | Base:{base_label} | Cliente:{cid} | "
        f"Data:{call.get('data','?')[:10]} | Dur:{call.get('duracao','?')}s | "
        f"Sent:{call.get('sentimento','?')} ===\n{conv}"
    )

n_batches = (len(amostra) + BATCH_SIZE_LIGACOES - 1) // BATCH_SIZE_LIGACOES
for i in range(n_batches):
    chunk = amostra[i*BATCH_SIZE_LIGACOES:(i+1)*BATCH_SIZE_LIGACOES]
    texto = "\n\n".join(formatar(*item) for item in chunk)
    fname = OUT_DIR / f"batch{i+1:02d}.txt"
    fname.write_text(texto, encoding="utf-8")

print(f"Gerados {n_batches} arquivos de lote (~{BATCH_SIZE_LIGACOES} ligacoes cada) em {OUT_DIR}")
