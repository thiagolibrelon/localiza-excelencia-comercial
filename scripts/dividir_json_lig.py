"""
Divide um JSON no formato LIG ({"id_cliente": [chamadas...], ...}, linha unica)
em blocos menores para copiar/colar manualmente.

Como usar:
1. Ajuste ARQUIVO_ENTRADA para o nome do seu arquivo (ex: as 6000 ligacoes novas).
2. Rode: python dividir_json_lig.py
3. Serao gerados bloco_lig_01.json, bloco_lig_02.json, ... na mesma pasta,
   cada um um dict JSON valido com um subconjunto dos clientes.
4. Abra cada bloco_lig_XX.json no Bloco de Notas, selecione tudo (Ctrl+A),
   copie (Ctrl+C) e cole no chat, avisando "bloco X de N".
"""
import json

ARQUIVO_ENTRADA = "novas_ligacoes.json"   # troque para o nome real do seu arquivo
TAMANHO_ALVO_BYTES = 2_000_000            # ~2MB por bloco, ajustavel

with open(ARQUIVO_ENTRADA, "r", encoding="utf-8") as f:
    dados = json.load(f)

clientes = list(dados.keys())
blocos = []
bloco_atual = {}
tamanho_atual = 0

for cid in clientes:
    trecho = json.dumps({cid: dados[cid]}, ensure_ascii=False)
    bloco_atual[cid] = dados[cid]
    tamanho_atual += len(trecho.encode("utf-8"))
    if tamanho_atual >= TAMANHO_ALVO_BYTES:
        blocos.append(bloco_atual)
        bloco_atual = {}
        tamanho_atual = 0

if bloco_atual:
    blocos.append(bloco_atual)

for i, bloco in enumerate(blocos, start=1):
    nome_saida = f"bloco_lig_{i:02d}.json"
    with open(nome_saida, "w", encoding="utf-8") as f:
        json.dump(bloco, f, ensure_ascii=False)
    print(f"{nome_saida}: {len(bloco)} clientes")

print(f"\nTotal: {len(clientes)} clientes em {len(blocos)} blocos.")
