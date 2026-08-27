"""
PASSO 2 — Minera candidatos a exemplos few-shot para os prompts de ligacao,
a partir das ~9.500 ligacoes que o Gemini ja classificou em JULHO/.

Entrada:
  JULHO/dados_convertidos/julho_completo.json   (transcricoes, cliente_id -> [ligacoes])
  JULHO/consolidado/P{1,2,3,5,9}.csv            (classificacoes)

Saida:
  ligacoes_genai/Exemplos_ligacoes_CANDIDATOS.xlsx   (uma aba por prompt)

O que o script faz:
  - casa cada linha de CSV com a transcricao SO quando o par (cliente_id, data)
    e 1:1 nos dois lados (1 unica linha no CSV e 1 unica ligacao na transcricao)
    -> exemplo sem ambiguidade;
  - descarta linhas com valor fora da taxonomia (o ruido conhecido: `tipo`=207,
    `teve_challenger`=CH1, etc.);
  - cobre cada codigo / balde da taxonomia com ate N candidatos, priorizando
    ligacoes de tamanho medio (mais faceis de validar);
  - faz um scrub LEVE de nomes proprios no vocativo. O scrub DEFINITIVO e parte
    da validacao humana — ver coluna `revisar_nomes`.

O usuario valida: abre o xlsx, na coluna `usar` deixa em branco pra manter ou
poe "x" pra descartar, corrige `classificacao` e escreve `motivo`. O resultado
vira ligacoes_genai/Exemplos_ligacoes.xlsx (passo posterior).

Execute:  python scripts/minerar_exemplos_ligacoes.py
"""
from pathlib import Path
import json
import re
import csv as _csv
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

RAIZ = Path(__file__).parent.parent
TRANSCR = RAIZ / "JULHO" / "dados_convertidos" / "julho_completo.json"
CONSOL = RAIZ / "JULHO" / "consolidado"
SAIDA = RAIZ / "ligacoes_genai" / "Exemplos_ligacoes_CANDIDATOS.xlsx"

MAX_POR_ALVO = 4          # candidatos por codigo/balde
TRECHO_MAX = 3500         # chars do trecho de transcricao
TRECHO_HEAD = 2300        # se maior que TRECHO_MAX: cabeca + [...] + cauda
TRECHO_TAIL = 1000
ALVO_CHARS = (350, 2600)  # faixa de tamanho "facil de validar" (preferida)

# ---------------------------------------------------------------------------
# Taxonomia valida (para descartar ruido dos CSVs)
# ---------------------------------------------------------------------------
DESFECHOS = {"fechou_novo", "fechou_renovacao", "fechou_upsell",
             "interessou_nao_fechou", "nao_era_venda", "sem_conteudo"}
INTENCOES = {"cliente_queria", "vendedor_puxou", "misto", "indefinido"}
SIMNAO = {"SIM", "NAO", "NA"}
TIPOS = {"nova_venda", "renovacao", "upsell", "retencao", "suporte_operacional",
         "pos_venda_sinistro", "pos_venda_manutencao", "cobranca", "onboarding",
         "duvida_contrato", "misto", "sem_conteudo"}
QUEM_INI = {"vendedor", "cliente", "indefinido"}
PROBS = {f"P{i}" for i in range(1, 13)}
CH = {f"CH{i}" for i in range(1, 8)}
QUALID = {"alta", "media", "baixa", "nenhum"}
AB = {f"AB{i}" for i in range(1, 6)}
FC = {f"FC{i}" for i in range(1, 6)}

# ---------------------------------------------------------------------------
# Scrub de nomes proprios (agressivo — exemplo few-shot nao depende de nome).
# Regra: toda palavra Capitalizada que NAO esteja em inicio de frase e NAO esteja
# na whitelist vira [NOME]. Over-scrub (cidade, empresa) e aceitavel; o que nao
# pode e vazar nome de vendedor/cliente. `revisar_nomes` ainda sinaliza sobras.
# ---------------------------------------------------------------------------
_WHITELIST = {
    "localiza", "rac", "pj", "cnpj", "cpf", "cnh", "nome", "brasil",
    "meoo", "zarp", "seminovos", "unidas", "movida",
    "whatsapp", "app", "sac", "iph", "seg", "segunda", "terca", "terça",
    "quarta", "quinta", "sexta", "sabado", "sábado", "domingo",
    "janeiro", "fevereiro", "marco", "março", "abril", "maio", "junho", "julho",
    "agosto", "setembro", "outubro", "novembro", "dezembro",
    "deus", "nossa", "senhor", "senhora", "dona", "doutor", "doutora",
    "sim", "nao", "não", "ok", "ta", "tá", "entao", "então", "bom", "boa", "ola", "olá",
    "oi", "alo", "alô", "tchau", "obrigado", "obrigada", "desculpa", "pois", "aham",
}
_WHITELIST |= {
    "isso", "tudo", "perfeito", "entendi", "certo", "claro", "opa", "uhum",
    "exato", "consigo", "pode", "deixa", "olha", "agora", "beleza", "opcao",
    "aguarda", "aguarde", "pera", "espera", "consegue", "vou", "estou", "voce",
    "peraí", "perai", "hum", "eita", "poxa", "putz", "caramba", "legal",
}
_RE_VOCATIVO = re.compile(
    r"\b(oi|ol[aá]|al[oô]|bom dia|boa tarde|boa noite|obrigad[oa]|brigad[oa]|tchau|"
    r"falar com|com [oa]|senhor[a]?|dona|sr|sra|dr|dra|aqui [eé] [oa]?|meu nome [eé]|"
    r"quem fala [eé]|[eé] [oa])[,:]?\s+([A-ZÀ-Ý][a-zà-ÿ]+(?:\s+[A-ZÀ-Ý][a-zà-ÿ]+){0,2})",
    re.IGNORECASE,
)
# nome no meio da fala (nao e inicio de frase)
_RE_CAP_MEIO = re.compile(r"([.!?:]\s+|\n\s*)?([A-ZÀ-Ý][a-zà-ÿ]{2,})")
# nome como vocativo/identificacao no inicio de turno: "C: Matheus?" / "A: Cristiane,"
_RE_CAP_TURNO = re.compile(r"(^|\n)([AC]: )([A-ZÀ-Ý][a-zà-ÿ]{2,})(?=[?,!.]|\s*$|\n)", re.M)


# vocativo apos fim de frase: "... boa tarde. Matheus, ..." / "obrigada, Ana!"
_RE_VOC_PONT = re.compile(r"([.!?,]\s+|\n[AC]: )([A-ZÀ-Ý][a-zà-ÿ]{2,})(?=[,!?])")


def scrub_nomes(txt):
    txt = _RE_VOCATIVO.sub(lambda m: f"{m.group(1)} [NOME]", txt)
    txt = _RE_VOC_PONT.sub(
        lambda m: m.group(1) + (m.group(2) if m.group(2).lower() in _WHITELIST else "[NOME]"),
        txt,
    )
    txt = _RE_CAP_TURNO.sub(
        lambda m: m.group(1) + m.group(2) + (m.group(3) if m.group(3).lower() in _WHITELIST else "[NOME]"),
        txt,
    )

    def _sub(m):
        prefixo, palavra = m.group(1), m.group(2)
        if prefixo:                       # inicio de frase / apos ':' — preserva
            return m.group(0)
        if palavra.lower() in _WHITELIST:
            return m.group(0)
        return "[NOME]"

    return _RE_CAP_MEIO.sub(_sub, txt)


# ---------------------------------------------------------------------------
def colapsar(conversa):
    out = []
    for sp, tx in conversa:
        tx = (tx or "").strip()
        if len(tx) < 2:
            continue
        if out and out[-1][0] == sp:
            out[-1][1] += " " + tx
        else:
            out.append([sp, tx])
    return out


def tem_mojibake(txt):
    return "�" in txt or "Ã£" in txt or "Ã©" in txt or "Ã§" in txt


def formatar_trecho(conversa):
    linhas = [f"{sp}: {tx}" for sp, tx in colapsar(conversa)]
    txt = "\n".join(linhas)
    if tem_mojibake(txt):
        return None, len(linhas)
    if len(txt) > TRECHO_MAX:
        txt = txt[:TRECHO_HEAD].rsplit("\n", 1)[0] + "\n[...]\n" + txt[-TRECHO_TAIL:].split("\n", 1)[-1]
    return scrub_nomes(txt), len(linhas)


def carregar_transcricoes():
    """(cliente_id, data10) -> conversa, SO quando ha exatamente 1 ligacao nesse dia."""
    data = json.loads(TRANSCR.read_text(encoding="utf-8"))
    por_dia = {}
    for cid, ligs in data.items():
        for lig in ligs:
            d = (lig.get("data") or "")[:10]
            por_dia.setdefault((cid, d), []).append(lig)
    return {k: v[0]["conversa"] for k, v in por_dia.items() if len(v) == 1}


def carregar_csv(nome):
    linhas = []
    with open(CONSOL / nome, encoding="utf-8", newline="") as f:
        for row in _csv.DictReader(f):
            linhas.append(row)
    # (cliente_id, data) -> row, SO quando 1:1
    cont = {}
    for r in linhas:
        cont.setdefault((r["cliente_id"], r["data"]), []).append(r)
    return {k: v[0] for k, v in cont.items() if len(v) == 1}


def prox_do_alvo(n):
    lo, hi = ALVO_CHARS
    if lo <= n <= hi:
        return 0
    return min(abs(n - lo), abs(n - hi))


def coletar(pares, alvos):
    """
    pares: lista de dicts com pelo menos {chave, n_chars, ...}
    alvos: dict alvo -> funcao(row)->bool
    retorna lista de (alvo, par) cobrindo cada alvo com ate MAX_POR_ALVO,
    ordem estavel (sem aleatoriedade).
    """
    escolhidos = []
    usados = set()
    for alvo, teste in alvos.items():
        cand = [p for p in pares if teste(p["row"])]
        cand.sort(key=lambda p: (prox_do_alvo(p["n_chars"]), p["chave"][0]))
        n = 0
        for p in cand:
            if n >= MAX_POR_ALVO:
                break
            k = (alvo, p["chave"])
            if p["chave"] in usados and n >= 2:
                continue  # ja apareceu noutro alvo; garante ao menos 2 frescos
            escolhidos.append((alvo, p))
            usados.add(p["chave"])
            n += 1
    return escolhidos


# ---------------------------------------------------------------------------
# Alvos por prompt
# ---------------------------------------------------------------------------
def alvos_p1():
    a = {}
    for d in sorted(DESFECHOS):
        a[f"desfecho={d}"] = (lambda r, d=d: r["desfecho"] == d)
    for i in range(1, 11):
        b = f"B{i}"
        a[f"{b}=SIM"] = (lambda r, b=b: r.get(b) == "SIM")
    return a


def limpa_p1(r):
    return (r["desfecho"] in DESFECHOS
            and r["intencao_entrada"] in INTENCOES
            and all(r.get(f"B{i}") in SIMNAO for i in range(1, 11)))


def classif_p1(r):
    bs = "+".join(f"B{i}" for i in range(1, 11) if r.get(f"B{i}") == "SIM") or "nenhum"
    return (f"desfecho={r['desfecho']}; intencao_entrada={r['intencao_entrada']}; "
            f"tentativa_comercial={r['tentativa_comercial']}; SIM=[{bs}]; "
            f"score_comercial={r['score_comercial']}")


def alvos_p2():
    a = {}
    for t in sorted(TIPOS):
        a[f"tipo={t}"] = (lambda r, t=t: r["tipo"] == t)
    return a


def limpa_p2(r):
    return r["tipo"] in TIPOS and r["quem_iniciou"] in QUEM_INI


def classif_p2(r):
    return (f"tipo={r['tipo']}; subtipo={r['subtipo']}; quem_iniciou={r['quem_iniciou']}; "
            f"tentativa_comercial={r['tentativa_comercial']}")


def _prob_set(r):
    return set(str(r["problemas_identificados"]).replace(" ", "").split("+"))


def alvos_p3():
    a = {"problema=nenhum": (lambda r: _prob_set(r) == {"nenhum"})}
    for i in range(1, 13):
        p = f"P{i}"
        a[f"problema={p}"] = (lambda r, p=p: p in _prob_set(r))
    return a


def limpa_p3(r):
    s = _prob_set(r)
    return s == {"nenhum"} or s <= PROBS


def classif_p3(r):
    return (f"problemas={r['problemas_identificados']}; quem_relatou={r['quem_relatou']}; "
            f"foi_resolvido={r['foi_resolvido_na_ligacao']}; escalou_para={r['escalou_para']}")


def _ch_set(r):
    return set(re.split(r"[;+]", str(r["codigos_challenger"]).replace(" ", "")))


def alvos_p5():
    a = {
        "teve_challenger=NAO": (lambda r: r["teve_challenger"] == "NAO"),
        "qualidade=alta": (lambda r: r["teve_challenger"] == "SIM" and r["qualidade"] == "alta"),
        "qualidade=baixa": (lambda r: r["teve_challenger"] == "SIM" and r["qualidade"] == "baixa"),
    }
    for i in range(1, 8):
        c = f"CH{i}"
        a[f"{c}"] = (lambda r, c=c: c in _ch_set(r))
    return a


def limpa_p5(r):
    if r["teve_challenger"] not in {"SIM", "NAO"}:
        return False
    if r["qualidade"] not in QUALID:
        return False
    if r["teve_challenger"] == "NAO":
        return True
    return _ch_set(r) <= CH and len(_ch_set(r) & CH) >= 1


def classif_p5(r):
    return (f"teve_challenger={r['teve_challenger']}; codigos={r['codigos_challenger']}; "
            f"resultado_imediato={r['resultado_imediato']}; qualidade={r['qualidade']} "
            f"| resumo_gemini: {r['frase_resumo']}")


def alvos_p9():
    a = {}
    for x in sorted(AB):
        a[f"abertura={x}"] = (lambda r, x=x: r["tipo_abertura"] == x)
    for x in sorted(FC):
        a[f"fechamento={x}"] = (lambda r, x=x: r["tipo_fechamento"] == x)
    return a


def limpa_p9(r):
    return r["tipo_abertura"] in AB and r["tipo_fechamento"] in FC


def classif_p9(r):
    return (f"abertura={r['tipo_abertura']}; usou_nome={r['usou_nome']}; "
            f"fechamento={r['tipo_fechamento']}; proximo_passo_claro={r['proximo_passo_claro']}; "
            f"prazo_definido={r['prazo_definido']}; desfecho_p9={r['desfecho_p9']}")


PROMPTS = {
    "P1": (limpa_p1, alvos_p1, classif_p1),
    "P2": (limpa_p2, alvos_p2, classif_p2),
    "P3": (limpa_p3, alvos_p3, classif_p3),
    "P5": (limpa_p5, alvos_p5, classif_p5),
    "P9": (limpa_p9, alvos_p9, classif_p9),
}

# ---------------------------------------------------------------------------
COLS = ["usar", "prompt", "alvo", "cliente_id", "data", "n_turns", "n_chars",
        "classificacao_gemini", "trecho_transcricao", "motivo", "revisar_nomes"]
LARG = [6, 7, 22, 12, 12, 8, 8, 52, 90, 40, 12]
HEAD_FILL = PatternFill("solid", fgColor="1F4E78")
HEAD_FONT = Font(color="FFFFFF", bold=True)


def build():
    print("Carregando transcricoes 1:1 ...")
    trans = carregar_transcricoes()
    print(f"  {len(trans)} pares (cliente,data) com ligacao unica")

    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    total = 0

    for pcod, (limpa, alvos_fn, classif) in PROMPTS.items():
        csvmap = carregar_csv(f"{pcod}.csv")
        pares = []
        for chave, row in csvmap.items():
            if chave not in trans:
                continue
            if not limpa(row):
                continue
            trecho, nt = formatar_trecho(trans[chave])
            if trecho is None or nt < 4:
                continue
            pares.append({"chave": chave, "row": row, "trecho": trecho,
                          "n_turns": nt, "n_chars": len(trecho)})
        escolhidos = coletar(pares, alvos_fn())

        ws = wb.create_sheet(pcod)
        ws.append([f"{pcod} — candidatos a exemplo (valide: 'usar'=x descarta; corrija 'classificacao_gemini'; escreva 'motivo')"])
        ws["A1"].font = Font(bold=True, size=12)
        ws.append([])
        ws.append(COLS)
        for c in range(1, len(COLS) + 1):
            ws.cell(row=3, column=c).fill = HEAD_FILL
            ws.cell(row=3, column=c).font = HEAD_FONT

        vistos = set()
        for alvo, p in escolhidos:
            cid, data = p["chave"]
            flag = "conferir" if _tem_nome_solto(p["trecho"]) else ""
            ws.append(["", pcod, alvo, cid, data, p["n_turns"], p["n_chars"],
                       classif(p["row"]), p["trecho"], "", flag])
            r = ws.max_row
            ws.cell(row=r, column=8).alignment = Alignment(wrap_text=True, vertical="top")
            ws.cell(row=r, column=9).alignment = Alignment(wrap_text=True, vertical="top")
            vistos.add(p["chave"])
            total += 1

        for i, w in enumerate(LARG, 1):
            ws.column_dimensions[get_column_letter(i)].width = w
        ws.freeze_panes = "A4"
        print(f"  {pcod}: {len(pares)} pares limpos -> {ws.max_row - 3} candidatos "
              f"({len(vistos)} ligacoes distintas)")

    SAIDA.parent.mkdir(parents=True, exist_ok=True)
    wb.save(SAIDA)
    print(f"\nOK -> {SAIDA}  ({total} candidatos no total)")


def _tem_nome_solto(txt):
    """Sobra do scrub: palavra Capitalizada no meio da fala fora da whitelist."""
    for m in re.finditer(r"(?<=[a-zà-ÿ]\s)([A-ZÀ-Ý][a-zà-ÿ]{2,})", txt):
        if m.group(1).lower() not in _WHITELIST:
            return True
    return False


if __name__ == "__main__":
    build()
