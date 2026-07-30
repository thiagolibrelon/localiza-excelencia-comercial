# -*- coding: utf-8 -*-
"""Gera o JSON detalhado de P3 (tipos de problema) para a nova aba do dashboardv2.html.

Cruza JULHO/consolidado/P3.csv (classificacao por ligacao) com
JULHO/dados_convertidos/julho_completo.json (transcricoes) para montar,
por codigo P1-P12: estatisticas (qtd, % resolvido, % escalado, quem_relatou,
escalou_para) + uma amostra de ligacoes de exemplo com trecho da transcricao.

Saida: resultados/consolidado/p3_problemas_detalhado.json
"""
import csv
import json
from collections import Counter, defaultdict

LABELS = {
    "P1": "Acesso/sistema (portal fora do ar, senha, biometria)",
    "P2": "Faturamento/cobranca (boleto errado, fatura errada)",
    "P3": "Multa/infracao",
    "P4": "Manutencao/substituto (carro em oficina, sem substituto)",
    "P5": "Condutor/cadastro (troca de condutor, habilitacao)",
    "P6": "Km excedente (cobranca incorreta, plano errado)",
    "P7": "Disponibilidade (carro reservado indisponivel)",
    "P8": "Franquia/agencia (processo diferente em franqueada)",
    "P9": "Sinistro (acidente, franquia de dano)",
    "P10": "Reserva/sistema (status incorreto)",
    "P11": "Outro",
    "P12": "Manipulacao de pesquisa/NPS",
}

MAX_TRECHO_CHARS = 4000
EXEMPLOS_POR_CODIGO = 12

with open("JULHO/dados_convertidos/julho_completo.json", encoding="utf-8") as f:
    transcricoes_raw = json.load(f)

# indice cliente_id -> {data(YYYY-MM-DD): [ligacoes]} (pode haver >1 no mesmo dia)
indice = defaultdict(lambda: defaultdict(list))
for cliente_id, ligacoes in transcricoes_raw.items():
    for lig in ligacoes:
        dia = lig["data"][:10]
        indice[cliente_id][dia].append(lig)


def montar_trecho(ligacao):
    linhas = []
    for speaker, texto in ligacao.get("conversa", []):
        prefixo = "Cliente" if speaker == "C" else "Atendente"
        linhas.append(f"{prefixo}: {texto}")
    trecho = "\n".join(linhas)
    if len(trecho) > MAX_TRECHO_CHARS:
        trecho = trecho[:MAX_TRECHO_CHARS] + "\n[...trecho truncado...]"
    return trecho


rows = []
with open("JULHO/consolidado/P3.csv", encoding="utf-8") as f:
    r = csv.DictReader(f)
    for row in r:
        rows.append(row)

total = len(rows)
com_problema = 0
freq = Counter()
resolvido = {k: Counter() for k in LABELS}
escalou = {k: Counter() for k in LABELS}
quem = {k: Counter() for k in LABELS}
exemplos_por_codigo = defaultdict(list)
combo_counter = Counter()

for row in rows:
    probs = row["problemas_identificados"]
    if not probs or probs == "nenhum":
        continue
    com_problema += 1
    codes = [p.strip() for p in probs.split("+") if p.strip()]
    combo_counter[probs] += 1

    cliente_id = row["cliente_id"]
    dia = row["data"]
    candidatos = indice.get(cliente_id, {}).get(dia, [])
    ambiguo = len(candidatos) != 1
    ligacao = candidatos[0] if candidatos else None

    for p in codes:
        if p not in LABELS:
            continue
        freq[p] += 1
        resolvido[p][row["foi_resolvido_na_ligacao"]] += 1
        escalou[p][row["escalou_para"]] += 1
        quem[p][row["quem_relatou"]] += 1

        if ligacao is not None and len(exemplos_por_codigo[p]) < EXEMPLOS_POR_CODIGO * 3:
            exemplos_por_codigo[p].append({
                "cliente_id": cliente_id,
                "data": dia,
                "resolvido": row["foi_resolvido_na_ligacao"],
                "escalou_para": row["escalou_para"],
                "quem_relatou": row["quem_relatou"],
                "outros_codigos": [c for c in codes if c != p],
                "ambiguo_mesmo_dia": ambiguo,
                "duracao_seg": ligacao.get("duracao"),
                "trecho": montar_trecho(ligacao),
            })

# selecao final dos exemplos: prioriza nao-ambiguos e diversidade de resolvido/escalado
def selecionar(exemplos, n):
    nao_ambiguos = [e for e in exemplos if not e["ambiguo_mesmo_dia"]]
    pool = nao_ambiguos if len(nao_ambiguos) >= n else exemplos

    resolvidos_sim = [e for e in pool if e["resolvido"] == "SIM"]
    resolvidos_nao = [e for e in pool if e["resolvido"] != "SIM"]
    escalados = [e for e in pool if e["escalou_para"] not in ("nao_escalou", "nenhum", "")]

    escolhidos = []
    vistos = set()

    def add(lst, k):
        count = 0
        for e in lst:
            key = (e["cliente_id"], e["data"])
            if key in vistos:
                continue
            escolhidos.append(e)
            vistos.add(key)
            count += 1
            if count >= k:
                break

    add(escalados, max(2, n // 3))
    add(resolvidos_nao, max(2, n // 3))
    add(resolvidos_sim, max(2, n // 3))
    add(pool, n)  # completa o restante das vagas com o que sobrar, na ordem original

    return escolhidos[:n]


codigos_out = []
for p in sorted(LABELS, key=lambda x: -freq[x]):
    n = freq[p]
    if n == 0:
        continue
    resol_sim = resolvido[p].get("SIM", 0)
    nao_escal = escalou[p].get("nao_escalou", 0)
    codigos_out.append({
        "codigo": p,
        "label": LABELS[p],
        "qtd": n,
        "pct_dos_problemas": round(n / com_problema * 100, 1),
        "pct_de_todas_ligacoes": round(n / total * 100, 1),
        "pct_resolvido": round(resol_sim / n * 100, 1),
        "pct_escalado": round((n - nao_escal) / n * 100, 1),
        "quem_relatou": dict(quem[p]),
        "escalou_para": dict(escalou[p]),
        "exemplos": selecionar(exemplos_por_codigo[p], EXEMPLOS_POR_CODIGO),
    })

top_combos = [{"combo": c, "qtd": n} for c, n in combo_counter.most_common(15) if "+" in c]

out = {
    "gerado_em": "2026-07-30",
    "fonte": "JULHO/consolidado/P3.csv (base de julho/2026, ~93.6% de cobertura)",
    "total_ligacoes": total,
    "total_com_problema": com_problema,
    "pct_com_problema": round(com_problema / total * 100, 1),
    "codigos": codigos_out,
    "top_combinacoes": top_combos,
}

with open("resultados/consolidado/p3_problemas_detalhado.json", "w", encoding="utf-8") as f:
    json.dump(out, f, ensure_ascii=False, indent=1)

print(f"OK - {len(codigos_out)} codigos, {sum(len(c['exemplos']) for c in codigos_out)} exemplos totais")
for c in codigos_out:
    print(f"  {c['codigo']:4} {c['label']:55} qtd={c['qtd']:4} exemplos={len(c['exemplos'])}")
