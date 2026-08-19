"""
Gera lotes de texto com TODAS as ligacoes da base (antiga + novo lote) para
exploracao P3 (problemas recorrentes) + P7 (cross-sell/upsell) via Fable,
substituindo a amostra parcial anterior (1.350 sorteadas, so 456 rodadas) por
cobertura de 100% das ligacoes.

Saida em resultados/exploracao_fable/inputs_completo/loteNNN.txt (mesmo
formato "=== LIGACAO | ... ===" usado no restante do pipeline, entao
scripts/consolidar_ligacoes_etapa2.py consegue casar segment_id sem mudanca).

Rodar so uma vez (nao e' idempotente por sorteio - aqui e' ordem fixa, entao
rodar de novo regera os mesmos arquivos). Depois, cada lote e' colado
manualmente no Fable e o resultado salvo em
resultados/exploracao_fable/outputs_completo/loteNNN_resultado.md.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT_DIR = ROOT / "resultados" / "exploracao_fable" / "inputs_completo"
OUT_DIR.mkdir(parents=True, exist_ok=True)

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
nova = carregar(ROOT / "dados" / "recebidos" / "bloco_lig_recebido_01.json", "NOVO_LOTE_5348")

# ordem fixa (nao sorteio) para cobertura total ser reprodutivel e auditavel
todos = sorted(antiga + nova, key=lambda item: (item[0], item[1], item[2].get("data", "")))

print(f"Base antiga: {len(antiga)} ligacoes")
print(f"Novo lote:   {len(nova)} ligacoes")
print(f"Total (cobertura 100%): {len(todos)} ligacoes")


def formatar(base_label, cid, call):
    conv = "\n".join(f"{s}: {t}" for s, t in call.get("conversa", []))
    return (
        f"=== LIGACAO | Base:{base_label} | Cliente:{cid} | "
        f"Data:{call.get('data', '?')[:10]} | Dur:{call.get('duracao', '?')}s | "
        f"Sent:{call.get('sentimento', '?')} ===\n{conv}"
    )


n_batches = (len(todos) + BATCH_SIZE_LIGACOES - 1) // BATCH_SIZE_LIGACOES
for i in range(n_batches):
    chunk = todos[i * BATCH_SIZE_LIGACOES:(i + 1) * BATCH_SIZE_LIGACOES]
    texto = "\n\n".join(formatar(*item) for item in chunk)
    fname = OUT_DIR / f"lote{i + 1:03d}.txt"
    fname.write_text(texto, encoding="utf-8")

print(f"Gerados {n_batches} lotes (~{BATCH_SIZE_LIGACOES} ligacoes cada) em {OUT_DIR}")
