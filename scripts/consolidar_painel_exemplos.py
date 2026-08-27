"""
Consolida o painel de agentes sobre os candidatos a exemplo — DECIDE POR MAIORIA.
Rodou com 7 votantes (agente_8 falhou por max_output_tokens). Ajuste AGN abaixo
se rodar com outro numero.

Entrada:
  ligacoes_genai/_panel/candidatos.json
  ligacoes_genai/_panel/_gabarito.json          (rotulo do Gemini, so referencia)
  ligacoes_genai/_panel/agente_{1..N}.json

Saida:
  ligacoes_genai/Exemplos_ligacoes.xlsx          -> RESULTADO FINAL. classificacao
      = maioria (pluralidade) dos 8 no eixo primario; campos graduados (B1..B10,
      CH, intencao, etc.) tambem por maioria. motivo = motivo mais completo entre
      os agentes que votaram com a maioria. Colunas trecho|classificacao|motivo no
      padrao do Exemplos.xlsx do NPS + colunas de diagnostico (apagaveis).
  ligacoes_genai/Exemplos_ligacoes_REVISAR.xlsx  -> so onde NAO ha maioria (empate
      >=2 opcoes no topo do eixo primario). Precisa de decisao humana.

Eixo primario (o que a maioria decide): P1=desfecho, P2=tipo, P3=conjunto de
problemas, P5=teve_challenger+qualidade, P9=tipo_abertura+tipo_fechamento.

forca do consenso: FORTE >=7 votos | OK 5-6 | FRACO pluralidade <=4.

Execute:  python scripts/consolidar_painel_exemplos.py
"""
from pathlib import Path
import json
import re
import unicodedata
from collections import Counter
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

RAIZ = Path(__file__).parent.parent
PANEL = RAIZ / "ligacoes_genai" / "_panel"
OUT_FINAL = RAIZ / "ligacoes_genai" / "Exemplos_ligacoes.xlsx"
OUT_REV = RAIZ / "ligacoes_genai" / "Exemplos_ligacoes_REVISAR.xlsx"
AGN = [f"ag{i}" for i in range(1, 8)]  # agente_8 falhou (max_output_tokens); 7 votantes
PROMPTS = ["P1", "P2", "P3", "P5", "P9"]


def na(s):
    s = "".join(c for c in unicodedata.normalize("NFD", str(s)) if unicodedata.category(c) != "Mn")
    return s.strip()


def sn(v):
    v = na(v).upper()
    if v in ("SIM", "S", "TRUE", "YES"):
        return "SIM"
    if v in ("NAO", "N", "FALSE", "NO"):
        return "NAO"
    return na(v).lower()


def lst(v):
    if v is None:
        return ()
    if isinstance(v, str):
        v = re.split(r"[;+,/]", v)
    it = [na(x).upper().replace(" ", "") for x in v]
    it = [x for x in it if x and x not in ("NENHUM", "NA", "[]", "-", "NONE")]
    return tuple(sorted(set(it)))


def qual(v):
    v = na(v).lower()
    return {"medio": "media", "média": "media", "médio": "media", "": "nenhum"}.get(v, v)


def extrair(prompt, cl):
    """-> (primario:tuple, graduado:dict campo->valor-normalizado)"""
    cl = cl or {}
    g = lambda k, *alt: next((cl[x] for x in (k, *alt) if x in cl and cl[x] not in (None, "")), "")
    if prompt == "P1":
        prim = (na(g("desfecho")).lower(),)
        bset = set(lst(g("B", "comportamentos")))
        grad = {f"B{i}": ("SIM" if f"B{i}" in bset else "NAO") for i in range(1, 11)}
        grad["intencao_entrada"] = na(g("intencao_entrada")).lower()
        grad["tentativa_comercial"] = sn(g("tentativa_comercial"))
    elif prompt == "P2":
        prim = (na(g("tipo")).lower(),)
        grad = {"quem_iniciou": na(g("quem_iniciou")).lower(),
                "tentativa_comercial": sn(g("tentativa_comercial"))}
    elif prompt == "P3":
        prim = (lst(g("problemas", "problemas_identificados")),)
        grad = {"quem_relatou": na(g("quem_relatou")).lower(),
                "foi_resolvido": na(g("foi_resolvido", "foi_resolvido_na_ligacao")).lower(),
                "escalou_para": na(g("escalou_para")).lower()}
    elif prompt == "P5":
        prim = (sn(g("teve_challenger")), qual(g("qualidade")))
        grad = {"CH_set": lst(g("codigos", "codigos_challenger")),
                "resultado_imediato": na(g("resultado_imediato")).lower()}
    elif prompt == "P9":
        prim = (na(g("tipo_abertura", "abertura")).upper(), na(g("tipo_fechamento", "fechamento")).upper())
        grad = {"proximo_passo_claro": sn(g("proximo_passo_claro")),
                "prazo_definido": sn(g("prazo_definido"))}
    else:
        prim, grad = ((na(json.dumps(cl, sort_keys=True)),), {})
    return prim, grad


def _c(txt, nome):
    m = re.search(rf"{nome}\s*=\s*([^;|]+)", txt or "")
    return m.group(1).strip() if m else ""


def extrair_gemini(prompt, txt):
    txt = txt or ""
    if prompt == "P1":
        m = re.search(r"SIM\s*=\s*\[([^\]]*)\]", txt)
        bs = "" if (not m or na(m.group(1)).lower() in ("nenhum", "")) else m.group(1)
        cl = {"desfecho": _c(txt, "desfecho"), "intencao_entrada": _c(txt, "intencao_entrada"),
              "tentativa_comercial": _c(txt, "tentativa_comercial"),
              "B": re.split(r"[;+,/]", bs) if bs else []}
    elif prompt == "P2":
        cl = {"tipo": _c(txt, "tipo"), "quem_iniciou": _c(txt, "quem_iniciou"),
              "tentativa_comercial": _c(txt, "tentativa_comercial")}
    elif prompt == "P3":
        cl = {"problemas": _c(txt, "problemas"), "quem_relatou": _c(txt, "quem_relatou"),
              "foi_resolvido": _c(txt, "foi_resolvido"), "escalou_para": _c(txt, "escalou_para")}
    elif prompt == "P5":
        cl = {"teve_challenger": _c(txt, "teve_challenger"), "codigos": _c(txt, "codigos"),
              "resultado_imediato": _c(txt, "resultado_imediato"), "qualidade": _c(txt, "qualidade")}
    elif prompt == "P9":
        cl = {"tipo_abertura": _c(txt, "abertura"), "tipo_fechamento": _c(txt, "fechamento"),
              "proximo_passo_claro": _c(txt, "proximo_passo_claro"), "prazo_definido": _c(txt, "prazo_definido")}
    else:
        cl = {}
    return extrair(prompt, cl)


def fmt_prim(prompt, prim):
    if prompt in ("P1", "P2"):
        return prim[0]
    if prompt == "P3":
        return "+".join(prim[0]) or "nenhum"
    if prompt in ("P5", "P9"):
        return f"{prim[0]}/{prim[1]}"
    return str(prim)


def maioria(valores):
    """-> (valor_top, n_top, empate_bool)"""
    cont = Counter(valores)
    ordenado = cont.most_common()
    top_v, top_n = ordenado[0]
    empate = len(ordenado) > 1 and ordenado[1][1] == top_n
    return top_v, top_n, empate


def classificacao_final(prompt, prim, grad_maioria):
    d = grad_maioria
    if prompt == "P1":
        bs = "+".join(f"B{i}" for i in range(1, 11) if d.get(f"B{i}") == "SIM") or "nenhum"
        return (f"desfecho={prim[0]} | intencao_entrada={d.get('intencao_entrada','?')} | "
                f"tentativa_comercial={d.get('tentativa_comercial','?')} | B: {bs}")
    if prompt == "P2":
        return (f"tipo={prim[0]} | quem_iniciou={d.get('quem_iniciou','?')} | "
                f"tentativa_comercial={d.get('tentativa_comercial','?')}")
    if prompt == "P3":
        return (f"problemas={'+'.join(prim[0]) or 'nenhum'} | quem_relatou={d.get('quem_relatou','?')} | "
                f"foi_resolvido={d.get('foi_resolvido','?')} | escalou_para={d.get('escalou_para','?')}")
    if prompt == "P5":
        ch = "+".join(d.get("CH_set", ())) or "nenhum"
        return (f"teve_challenger={prim[0]} | qualidade={prim[1]} | CH: {ch} | "
                f"resultado_imediato={d.get('resultado_imediato','?')}")
    if prompt == "P9":
        return (f"tipo_abertura={prim[0]} | tipo_fechamento={prim[1]} | "
                f"proximo_passo_claro={d.get('proximo_passo_claro','?')} | prazo_definido={d.get('prazo_definido','?')}")
    return str(prim)


HEAD_FILL = PatternFill("solid", fgColor="1F4E78")
HEAD_FONT = Font(color="FFFFFF", bold=True)
WARN = PatternFill("solid", fgColor="FFF2CC")
SPLIT = PatternFill("solid", fgColor="FCE4D6")


def carregar():
    cand = {c["id"]: c for c in json.loads((PANEL / "candidatos.json").read_text(encoding="utf-8"))}
    gab = json.loads((PANEL / "_gabarito.json").read_text(encoding="utf-8"))
    ags, faltam = {}, []
    for a in AGN:
        p = PANEL / f"agente_{a[2:]}.json"
        if not p.exists():
            faltam.append(p.name)
            continue
        ags[a] = {o["id"]: o for o in json.loads(p.read_text(encoding="utf-8"))}
    if faltam:
        raise SystemExit(f"Faltam arquivos de agente: {faltam}")
    return cand, gab, ags, [a for a in AGN if a in ags]


def build():
    cand, gab, ags, agn = carregar()
    n_ag = len(agn)
    finais, revisar = [], []
    resumo = Counter()

    for cid, c in cand.items():
        p = c["prompt"]
        opin = {}
        for a in agn:
            o = ags[a].get(cid, {})
            prim, grad = extrair(p, o.get("classificacao"))
            opin[a] = (prim, grad, o.get("motivo", ""), o.get("confianca", ""))
        gprim, _ = extrair_gemini(p, gab.get(cid, ""))

        prims = [opin[a][0] for a in agn]
        top, topn, empate = maioria(prims)

        # campos graduados: maioria campo a campo
        grad_final, grad_notas = {}, []
        for campo in opin[agn[0]][1]:
            vals = [opin[a][1].get(campo) for a in agn]
            gv, gn, ge = maioria(vals)
            grad_final[campo] = gv
            if gn < n_ag:
                cont = Counter(str(x) for x in vals)
                grad_notas.append(f"{campo}=" + "/".join(f"{n}x{v}" for v, n in cont.most_common()))

        gemini_bate = gprim == top
        base = dict(prompt=p, id=cid, cliente_id=c["cliente_id"], data=c["data"],
                    alvo=c["alvo_amostragem"], trecho=c["trecho_transcricao"])
        dist = "/".join(f"{n}x{fmt_prim(p, v)}" for v, n in Counter(prims).most_common())

        if empate:
            resumo[f"{p}:revisar"] += 1
            row = {**base, "empate": dist, "gemini": fmt_prim(p, gprim),
                   "ruido_graduado": " ; ".join(grad_notas), "decisao_final": "", "motivo": ""}
            for a in agn:
                m = opin[a][2]
                row[a] = fmt_prim(p, opin[a][0]) + (f"  «{m}»" if m else "")
            revisar.append(row)
            continue

        forca = "FORTE" if topn >= 7 else ("OK" if topn >= 5 else "FRACO")
        resumo[f"{p}:{forca}"] += 1
        resumo[f"{p}:final"] += 1
        motivos = sorted((opin[a][2] for a in agn if opin[a][0] == top and opin[a][2]),
                         key=len, reverse=True)
        finais.append({
            **base,
            "classificacao": classificacao_final(p, top, grad_final),
            "motivo": motivos[0] if motivos else "",
            "votos": f"{topn}/{n_ag}",
            "forca": forca,
            "gemini": "bate" if gemini_bate else f"DIVERGE ({fmt_prim(p, gprim)})",
            "distribuicao": dist,
            "ruido_graduado": " ; ".join(grad_notas),
        })

    _final(finais)
    _revisar(revisar)

    print(f"FINAL   -> {OUT_FINAL.name}: {len(finais)}   |   REVISAR -> {OUT_REV.name}: {len(revisar)}   ({n_ag} agentes)\n")
    for p in PROMPTS:
        print(f"  {p}: final {resumo[f'{p}:final']:>2}  "
              f"(FORTE {resumo[f'{p}:FORTE']:>2} / OK {resumo[f'{p}:OK']:>2} / FRACO {resumo[f'{p}:FRACO']:>2})"
              f"   revisar {resumo[f'{p}:revisar']:>2}")
    ndiv = sum(1 for r in finais if r["gemini"].startswith("DIVERGE"))
    print(f"\n  no FINAL, linhas onde o Gemini divergiu da maioria: {ndiv}/{len(finais)}")


def _w(ws, larg):
    for i, x in enumerate(larg, 1):
        ws.column_dimensions[get_column_letter(i)].width = x


def _final(rows):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    cols = ["trecho_transcricao", "classificacao", "motivo",
            "id", "cliente_id", "data", "votos", "forca", "gemini", "distribuicao", "ruido_graduado"]
    for p in PROMPTS:
        ws = wb.create_sheet(p)
        ws.append(cols)
        for c in range(1, len(cols) + 1):
            ws.cell(row=1, column=c).fill = HEAD_FILL
            ws.cell(row=1, column=c).font = HEAD_FONT
        sub = sorted([x for x in rows if x["prompt"] == p],
                     key=lambda x: ({"FORTE": 0, "OK": 1, "FRACO": 2}[x["forca"]], x["id"]))
        for r in sub:
            ws.append([r["trecho"], r["classificacao"], r["motivo"], r["id"], r["cliente_id"],
                       r["data"], r["votos"], r["forca"], r["gemini"], r["distribuicao"], r["ruido_graduado"]])
            rr = ws.max_row
            ws.cell(row=rr, column=1).alignment = Alignment(wrap_text=True, vertical="top")
            ws.cell(row=rr, column=11).alignment = Alignment(wrap_text=True, vertical="top")
            if r["gemini"].startswith("DIVERGE"):
                ws.cell(row=rr, column=9).fill = WARN
            if r["forca"] == "FRACO":
                ws.cell(row=rr, column=8).fill = SPLIT
        _w(ws, [95, 46, 46, 8, 12, 12, 8, 8, 24, 34, 40])
        ws.freeze_panes = "B2"
    wb.save(OUT_FINAL)


def _revisar(rows):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    cols = ["prompt", "id", "cliente_id", "data", "empate", "decisao_final", "motivo",
            "ag1", "ag2", "ag3", "ag4", "ag5", "ag6", "ag7", "gemini",
            "ruido_graduado", "alvo", "trecho"]
    for p in PROMPTS:
        ws = wb.create_sheet(p)
        ws.append(cols)
        for c in range(1, len(cols) + 1):
            ws.cell(row=1, column=c).fill = HEAD_FILL
            ws.cell(row=1, column=c).font = HEAD_FONT
        for r in sorted([x for x in rows if x["prompt"] == p], key=lambda x: x["id"]):
            ws.append([r.get(k, "") for k in cols])
            rr = ws.max_row
            for cc in list(range(8, 16)) + [18]:
                ws.cell(row=rr, column=cc).alignment = Alignment(wrap_text=True, vertical="top")
            ws.cell(row=rr, column=5).fill = SPLIT
        _w(ws, [7, 8, 12, 12, 26, 22, 34] + [26] * 8 + [34, 20, 80])
        ws.freeze_panes = "A2"
    wb.save(OUT_REV)


if __name__ == "__main__":
    build()
