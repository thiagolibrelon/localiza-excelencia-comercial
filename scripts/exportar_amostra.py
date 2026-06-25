import json, re, random
from pathlib import Path

random.seed(42)

with open(Path(__file__).parent.parent / "dados" / "LIG", "r", encoding="utf-8") as f:
    data = json.load(f)

NOMES = {"Bruna","Lucas","Everton","Isaias","Carla","Gabriel","Rodrigo",
         "Gabriela","Camila","Ramiro","Ana","Thais","Luma","Matheus","Tawana",
         "Tatiana","Paulo","Guilherme","Bruno","Geraldo","Talita","Francisco"}

def extract_seller(call):
    pats = [
        r"aqui [eé] (?:o |a )?([A-Za-záéíóúâêîôûãõ]{3,})",
        r"meu nome [eé] ([A-Za-záéíóúâêîôûãõ]{3,})",
        r"(?:sou|chamo)[- ](?:o |a )?([A-Za-záéíóúâêîôûãõ]{3,})",
    ]
    for sp, txt in call.get("conversa", [])[:6]:
        if sp != "A":
            continue
        for p in pats:
            m = re.search(p, txt, re.I)
            if m:
                n = m.group(1).capitalize()
                if n in NOMES:
                    return n
    return "N/A"

def fmt(cid, call, seller):
    conv = "\n".join(f"{s}: {t}" for s, t in call.get("conversa", []))
    data_str = call.get("data", "?")[:10]
    dur = call.get("duracao", "?")
    sent = call.get("sentimento", "?")
    return (
        f"=== LIGAÇÃO | Cliente:{cid} | Vendedor:{seller} | "
        f"Data:{data_str} | Dur:{dur}s | Sent:{sent} ===\n{conv}"
    )

by_seller = {}
no_seller = []
for cid, calls in data.items():
    for call in calls:
        s = extract_seller(call)
        if s != "N/A":
            by_seller.setdefault(s, []).append((cid, call, s))
        else:
            no_seller.append((cid, call, "N/A"))

amostra = []
for seller, items in by_seller.items():
    amostra.extend(random.sample(items, min(5, len(items))))
random.shuffle(no_seller)
amostra.extend(no_seller[:20])
random.shuffle(amostra)

batch_size = 35
for i in range(0, len(amostra), batch_size):
    batch = amostra[i:i + batch_size]
    n = i // batch_size + 1
    texto = f"BATCH {n} — {len(batch)} ligações\n\n"
    texto += "\n\n".join(fmt(cid, call, s) for cid, call, s in batch)
    out = Path(__file__).parent.parent / "amostras" / f"amostra_batch{n}.txt"
    out.write_text(texto, encoding="utf-8")
    print(f"Batch {n}: {len(batch)} ligações — {out.stat().st_size // 1024}KB")

print("Exportação concluída!")
