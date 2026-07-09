"""
Prepara lotes de texto (ligacoes formatadas) para exploracao via Fable (P3 + P7),
combinando a base antiga (dados/LIG) e o novo lote (dados/recebidos/bloco_lig_recebido_01.json).
Cada lote vira um arquivo .txt em resultados/exploracao_fable/inputs/.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT_DIR = ROOT / "resultados" / "exploracao_fable" / "inputs"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BATCH_SIZE_LIGACOES = 200

def carregar(path, base_label):
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    items = []
    for cid, calls in data.items():
        for call in calls:
            items.append((base_label, cid, call))
    return items

todos = []
todos += carregar(ROOT / "dados" / "LIG", "BASE_ANTIGA_1275")
todos += carregar(ROOT / "dados" / "recebidos" / "bloco_lig_recebido_01.json", "NOVO_LOTE_5348")

print(f"Total ligacoes combinadas: {len(todos)}")

def formatar(base_label, cid, call):
    conv = "\n".join(f"{s}: {t}" for s, t in call.get("conversa", []))
    return (
        f"=== LIGACAO | Base:{base_label} | Cliente:{cid} | "
        f"Data:{call.get('data','?')[:10]} | Dur:{call.get('duracao','?')}s | "
        f"Sent:{call.get('sentimento','?')} ===\n{conv}"
    )

n_batches = (len(todos) + BATCH_SIZE_LIGACOES - 1) // BATCH_SIZE_LIGACOES
for i in range(n_batches):
    chunk = todos[i*BATCH_SIZE_LIGACOES:(i+1)*BATCH_SIZE_LIGACOES]
    texto = "\n\n".join(formatar(*item) for item in chunk)
    fname = OUT_DIR / f"batch{i+1:02d}.txt"
    fname.write_text(texto, encoding="utf-8")

print(f"Gerados {n_batches} arquivos de lote em {OUT_DIR}")
