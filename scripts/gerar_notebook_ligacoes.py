# -*- coding: utf-8 -*-
"""
PASSO 3 — Gera o notebook `ligacoes_genai/GEN_AI_LIGACOES.ipynb`, adaptado do
motor GenAI do NPS-PJ (`Exemplos/GEN_AI_NPS_CXPJ 2.ipynb`) para rodar os prompts
de analise de ligacao via llm-gate da Localiza.

Reprodutivel: edite as celulas aqui e rode de novo.
Execute:  python scripts/gerar_notebook_ligacoes.py
"""
import json
from pathlib import Path

SAIDA = Path(__file__).parent.parent / "ligacoes_genai" / "GEN_AI_LIGACOES.ipynb"

MD_INTRO = r"""# GEN AI — Análise de Ligações (Localiza Frota PJ)

Motor adaptado do `GEN_AI_NPS_CXPJ`. Classifica ligações de vendas B2B pelos
prompts do framework de análise, via **llm-gate / API OpenAI**.

## Como rodar
1. Ajuste a célula **CONFIG** (versão, pastas, modelo).
2. Garanta a variável de ambiente `API_KEY` (chave do llm-gate).
3. Rode as células em ordem.

## Versões
| Versão | Prompts | Chamadas/ligação |
|---|---|---|
| **basica** | P1 (desfecho + B1–B10), P2 (tipo), P3 (problemas), P5 (Challenger), P9 (abertura/fechamento) | 4 |
| **completa** | + P4/P6/P7/P8/P10/P11/P13/P15 | ~7 |

`completa` só roda os prompts que tiverem aba correspondente em
`Classificacoes_ligacoes.xlsx`. Hoje só P1/P2/P3/P5/P9 estão prontos — os demais
são ignorados com aviso até a taxonomia + exemplos deles serem construídos.

## Entrada
Pasta com CSVs `;`-separados, UTF-8, colunas do export padrão:
`cd_contato_master;cd_segmento;data_hora_inicio;direcao;nome_agente_1;time_agente_1;habilidades_agente_1;transcricao_limpa;Cliente;Data`
- `cd_segmento` = ID único da ligação (chave de tudo).
- `transcricao_limpa` no formato `AGENTE: ... | CLIENTE: ...` (é normalizada para `A:/C:`).
- Linhas sem transcrição são separadas e **não** vão para a API.

## Saída (em `PASTA_SAIDA`)
- `_resultados.jsonl` — 1 linha por (ligação × grupo de prompt), resposta crua + tokens/custo. **Incremental** (re-rodar pula o que já foi feito).
- `P1.csv … P9.csv` — 1 linha por ligação por prompt.
- `CONSOLIDADO.csv` — 1 linha por `cd_segmento`, todos os prompts juntos + `nome_agente_1`/`time_agente_1`/`direcao`.
- `_sem_transcricao.csv` — ligações puladas por falta de texto.
"""

CFG = r'''# ============================ CONFIG ============================
from pathlib import Path

VERSAO = "basica"                 # "basica" | "completa"

# Pasta com os CSVs de ligação (formato de 10 colunas). Um ou mais arquivos.
PASTA_ENTRADA = Path(r"C:\Users\SEU_USUARIO\...\chamadas\agosto")
PASTA_SAIDA   = Path(r"C:\Users\SEU_USUARIO\...\resultados_ligacoes\agosto")

# Pasta onde estão Classificacoes_ligacoes.xlsx e Exemplos_ligacoes.xlsx
# (por padrão, a mesma deste notebook).
PASTA_APOIO   = Path.cwd()
ARQ_CLASSIF   = PASTA_APOIO / "Classificacoes_ligacoes.xlsx"
ARQ_EXEMPLOS  = PASTA_APOIO / "Exemplos_ligacoes.xlsx"

MODELO             = "gpt-4o-mini"
MODELO_POR_PROMPT  = {}            # ex: {"P5": "gpt-4o"} — sobe o modelo só de um grupo
MAX_WORKERS        = 7
MAX_EXEMPLOS_POR_PROMPT = 10       # few-shot: nº de exemplos por prompt no system
LIMITE_LIGACOES    = None          # None = todas; int p/ teste rápido (ex: 20)
MAX_TENTATIVAS     = 3
TIMEOUT_S          = 120

PASTA_SAIDA.mkdir(parents=True, exist_ok=True)
print("versão:", VERSAO, "| entrada:", PASTA_ENTRADA, "| saída:", PASTA_SAIDA)
'''

IMPORTS = r'''# ==================== IMPORTS + ENDPOINT ====================
import os, re, csv, json, time, uuid, math, unicodedata, logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests
import pandas as pd
from tqdm.auto import tqdm

csv.field_size_limit(10_000_000)

URL = "https://llm-gate-np.localiza.dev/llm-gate/v2/chat/completions"
HEADERS = {
    "Content-Type": "application/json",
    "X-Correlation-ID": str(uuid.uuid4()),
    "api_key": os.getenv("API_KEY"),
}
assert HEADERS["api_key"], "Defina a variável de ambiente API_KEY (chave do llm-gate)."

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
log = logging.getLogger("ligacoes")

# Teste de conectividade (descomente para checar)
# r = requests.post(URL, headers=HEADERS, json={"model": MODELO,
#     "messages": [{"role": "user", "content": "ping"}]}, timeout=TIMEOUT_S)
# print(r.status_code, r.text[:300])
'''

TAXONOMIA = r'''# ============ TAXONOMIA + EXEMPLOS (das planilhas) ============
# Classificacoes_ligacoes.xlsx: uma aba por prompt, colunas
#   grupo | codigo | rotulo | descricao | peso
# Exemplos_ligacoes.xlsx: uma aba por prompt, colunas
#   trecho_transcricao | classificacao | motivo | ... (+ forca p/ ordenar)

def _abas(caminho, col_chave):
    """Le todas as abas; acha a linha de cabecalho pela presenca de `col_chave`."""
    cru = pd.read_excel(caminho, sheet_name=None, header=None)
    out = {}
    for nome, df in cru.items():
        hdr = None
        for i in range(min(8, len(df))):
            if col_chave in [str(x).strip() for x in df.iloc[i].tolist()]:
                hdr = i
                break
        if hdr is None:
            continue
        d = df.iloc[hdr + 1:].copy()
        d.columns = [str(x).strip() for x in df.iloc[hdr].tolist()]
        out[nome] = d.reset_index(drop=True)
    return out

_clf = _abas(ARQ_CLASSIF, "codigo")
_exs = _abas(ARQ_EXEMPLOS, "trecho_transcricao")

TAXO = {}          # prompt -> texto pronto pro system
EXEMPLOS = {}      # prompt -> texto pronto pro system
PESOS_B = {}       # prompt P1 -> {B1: peso, ...}

for p, df in _clf.items():
    df = df.dropna(subset=["codigo"])
    linhas = []
    grupo_atual = None
    for _, r in df.iterrows():
        g = str(r["grupo"]).strip()
        if g != grupo_atual:
            linhas.append(f"\n[{g}]")
            grupo_atual = g
        peso = "" if pd.isna(r.get("peso")) or r.get("peso") == "" else f"  (peso {int(r['peso'])})"
        linhas.append(f"  {r['codigo']} = {r['rotulo']}: {r['descricao']}{peso}")
        if p == "P1" and g == "comportamento":
            PESOS_B[str(r["codigo"]).strip()] = int(r["peso"])
    TAXO[p] = "\n".join(linhas).strip()

ORDEM_FORCA = {"FORTE": 0, "OK": 1, "FRACO": 2}
for p, df in _exs.items():
    if "forca" in df.columns:
        df = df.assign(_o=df["forca"].map(lambda x: ORDEM_FORCA.get(str(x), 9))).sort_values("_o")
    blocos = []
    for i, r in enumerate(df.head(MAX_EXEMPLOS_POR_PROMPT).itertuples(), 1):
        blocos.append(
            f"--- exemplo {i} ---\nTRANSCRICAO:\n{r.trecho_transcricao}\n"
            f"CLASSIFICACAO: {r.classificacao}\nMOTIVO: {r.motivo}"
        )
    EXEMPLOS[p] = "\n\n".join(blocos)

print("taxonomia:", list(TAXO), "| exemplos:", {k: EXEMPLOS[k].count("--- exemplo") for k in EXEMPLOS})
print("pesos B (P1):", PESOS_B)
'''

CONTEXTO = r'''# =============== CONTEXTO DE NEGÓCIO + SCHEMAS ===============
PAPEL = (
    "Voce e um analista de comportamento comercial em locacao de veiculos "
    "corporativos (Localiza Frota PJ). Recebe UMA ligacao e a classifica pelos "
    "prompts pedidos. Assertividade importa mais que velocidade. Classifique "
    "apenas pelo que esta explicito na transcricao — nao invente. "
    "No texto: 'A' = vendedor (agente), 'C' = cliente. STT fragmentado: junte "
    "turns consecutivos do mesmo speaker. <unk> e [NOME] = ignore."
)

REGRAS_NEGOCIO = (
    "Regras do negocio de locacao PJ da Localiza:\n"
    "- Duas formas de retirar o carro: Fast Retirada Digital (app, sem atendimento humano; "
    "cliente ideal e 'autonomo'/'touchless') ou balcao com atendente.\n"
    "- Janela da Retirada Digital: de 1h30 antes ate 2h depois do horario agendado.\n"
    "- Produtos adicionais (custo extra): Telemetria, Protecao Total/cobertura de avarias, "
    "Upgrade de categoria, Km adicional, Contrato anual (trava preco 12m), Condutor adicional/ilimitado, "
    "Veiculos eletricos. Esclarecer forma de pagamento (faturado x cartao) NAO e upsell.\n"
    "- Carros devem ser entregues limpos e abastecidos; tag de pedagio colada no parabrisa "
    "(as vezes precisa ativar no balcao).\n"
    "- Cliente paga caucao (pre-autorizacao) na retirada, devolvida ao fim da locacao.\n"
    "- Quando falta a categoria reservada, a agencia da um upgrade gratuito — nem sempre percebido "
    "como beneficio pelo cliente.\n"
    "- Regra diaria x mensal: locacao curta cobrada como diaria costuma sair mais cara que o mensal; "
    "'fazer a conta' pro cliente (dias x diaria vs mensal) e um argumento comercial classico (B5/CH1).\n"
    "- Atendimento humano nas lojas e remoto (0800) para sinistro/pane fora da loja.\n"
    "- Programa fidelidade: clientes fieis podem receber upgrade fidelidade.\n"
    "- Localiza Pesados (caminhao, cavalo, carreta) e um negocio separado do RAC (leves, inclui picape/fiorino)."
)

# Chaves que o modelo deve devolver por prompt (formato JSON)
SCHEMA = {
 "P1": ('{"desfecho": "<fechou_novo|fechou_renovacao|fechou_upsell|interessou_nao_fechou|nao_era_venda|sem_conteudo>", '
        '"intencao_entrada": "<cliente_queria|vendedor_puxou|misto|indefinido>", '
        '"tentativa_comercial": "<SIM|NAO>", '
        '"B": ["<lista dos B1..B10 presentes; [] se nenhum>"], '
        '"motivo": "<1 frase>"}'),
 "P2": ('{"tipo": "<nova_venda|renovacao|upsell|retencao|suporte_operacional|pos_venda_sinistro|'
        'pos_venda_manutencao|cobranca|onboarding|duvida_contrato|misto|sem_conteudo>", '
        '"subtipo": "<curto ou vazio>", "quem_iniciou": "<vendedor|cliente|indefinido>", '
        '"tentativa_comercial": "<SIM|NAO>"}'),
 "P3": ('{"problemas": ["<lista P1..P12; [\\"nenhum\\"] se nao houver>"], '
        '"quem_relatou": "<cliente|vendedor_detectou|nenhum>", '
        '"foi_resolvido": "<SIM|NAO|PARCIAL|nenhum>", '
        '"escalou_para": "<0800|supervisora|IT|nao_escalou|nenhum>", "observacao": "<1 frase>"}'),
 "P5": ('{"teve_challenger": "<SIM|NAO>", "codigos_challenger": ["<lista CH1..CH7; [] se NAO>"], '
        '"resultado_imediato": "<cliente_aceitou|cliente_refletiu|sem_reacao_visivel>", '
        '"qualidade": "<alta|media|baixa>", "frase_resumo": "<1 frase>"}'),
 "P9": ('{"tipo_abertura": "<AB1|AB2|AB3|AB4|AB5>", "usou_nome": "<SIM|NAO>", '
        '"tipo_fechamento": "<FC1|FC2|FC3|FC4|FC5>", '
        '"proximo_passo_claro": "<SIM|NAO>", "prazo_definido": "<SIM|NAO>", "observacao": "<1 frase>"}'),
 # completa (placeholders — precisam da aba de taxonomia + exemplos)
 "P4": '{"health_score": {}}', "P6": '{"oportunidades_perdidas": []}',
 "P7": '{"produtos": {}}', "P8": '{"objecoes": []}', "P10": '{"promessas": []}',
 "P11": '{"sinais_competitivos": []}', "P13": '{"padroes": []}', "P15": '{"eventos_raros": []}',
}

# Grupos de prompt por versao (cada grupo = 1 chamada de API)
GRUPOS = {
    "basica":   [["P1", "P2"], ["P3"], ["P5"], ["P9"]],
    "completa": [["P1", "P2"], ["P3", "P7"], ["P5", "P6"], ["P9", "P10"],
                 ["P4", "P8", "P11"], ["P13", "P15"]],
}

def prompts_disponiveis(lista):
    return [p for p in lista if p in TAXO]

GRUPOS_ATIVOS = []
for g in GRUPOS[VERSAO]:
    disp = prompts_disponiveis(g)
    if not disp:
        log.warning("grupo %s ignorado — sem taxonomia (%s)", g, ARQ_CLASSIF.name)
        continue
    if disp != g:
        log.warning("grupo %s: rodando so %s (resto sem taxonomia)", g, disp)
    GRUPOS_ATIVOS.append(disp)
print("grupos ativos:", GRUPOS_ATIVOS)


def montar_mensagens(grupo, transcricao):
    partes = [PAPEL, REGRAS_NEGOCIO]
    for p in grupo:
        partes.append(f"### {p} — taxonomia\n{TAXO[p]}")
        if EXEMPLOS.get(p):
            partes.append(f"### {p} — exemplos ja classificados corretamente\n{EXEMPLOS[p]}")
    esquema = ", ".join(f'"{p}": {SCHEMA[p]}' for p in grupo)
    partes.append(
        "Responda SOMENTE um objeto JSON valido, sem texto fora dele, no formato:\n"
        "{ " + esquema + " }"
    )
    return [{"role": "system", "content": "\n\n".join(partes)},
            {"role": "user", "content": transcricao or "Sem transcricao disponivel."}]
'''

CARREGAR = r'''# ==================== CARREGAR LIGAÇÕES ====================
COLS = ["cd_contato_master", "cd_segmento", "data_hora_inicio", "direcao",
        "nome_agente_1", "time_agente_1", "habilidades_agente_1",
        "transcricao_limpa", "Cliente", "Data"]

def _fix(s):
    if not isinstance(s, str):
        return ""
    # conserta mojibake cp1252->utf8 comum no export; U+FFFD e perda real, mantem
    try:
        s = s.encode("cp1252", "ignore").decode("utf-8", "ignore") if "Ã" in s or "�\xa0" in s else s
    except Exception:
        pass
    return s

def _norm_transcricao(t):
    t = _fix(t or "").strip()
    if not t:
        return ""
    t = re.sub(r"\bAGENTE\s*:", "\nA:", t)
    t = re.sub(r"\bCLIENTE\s*:", "\nC:", t)
    t = t.replace(" | ", "\n").replace("|", "\n")
    linhas = [ln.strip() for ln in t.splitlines() if len(ln.strip()) > 2]
    return "\n".join(linhas)

registros, sem_transcricao = [], []
arquivos = sorted([p for p in PASTA_ENTRADA.iterdir() if p.is_file()])
assert arquivos, f"nenhum arquivo em {PASTA_ENTRADA}"

for arq in arquivos:
    txt = arq.read_text(encoding="utf-8", errors="replace")
    for row in csv.DictReader(txt.splitlines(), delimiter=";"):
        seg = (row.get("cd_segmento") or "").strip()
        if not seg:
            continue
        conv = _norm_transcricao(row.get("transcricao_limpa"))
        base = {
            "cd_segmento": seg,
            "cliente_id": (row.get("Cliente") or "").strip(),
            "data": (row.get("Data") or "").strip(),
            "direcao": (row.get("direcao") or "").strip(),
            "nome_agente_1": (row.get("nome_agente_1") or "").strip(),
            "time_agente_1": (row.get("time_agente_1") or "").strip(),
        }
        if len(conv) < 40:
            sem_transcricao.append(base)
        else:
            registros.append({**base, "transcricao": conv})

# dedup por cd_segmento (mantem 1º)
vistos = set()
registros = [r for r in registros if not (r["cd_segmento"] in vistos or vistos.add(r["cd_segmento"]))]
if LIMITE_LIGACOES:
    registros = registros[:LIMITE_LIGACOES]

pd.DataFrame(sem_transcricao).to_csv(PASTA_SAIDA / "_sem_transcricao.csv", index=False, encoding="utf-8")
print(f"{len(registros)} ligações para analisar | {len(sem_transcricao)} sem transcrição (salvas)")
print(f"chamadas previstas: {len(registros) * len(GRUPOS_ATIVOS)} ({len(GRUPOS_ATIVOS)} grupos/ligação)")
'''

LOOP = r'''# ==================== LOOP PARALELO (API) ====================
ARQ_JSONL = PASTA_SAIDA / "_resultados.jsonl"

feitos = set()
if ARQ_JSONL.exists():
    for ln in ARQ_JSONL.read_text(encoding="utf-8").splitlines():
        try:
            d = json.loads(ln)
            if d.get("ok"):
                feitos.add((d["cd_segmento"], d["grupo_id"]))
        except Exception:
            pass
print(f"{len(feitos)} (ligação×grupo) já processados — serão pulados")

_lock_file = __import__("threading").Lock()
_acc = {"tokens": 0, "custo": 0.0, "erros": 0}

def _chamar(modelo, mensagens):
    payload = {"model": modelo, "messages": mensagens, "temperature": 0,
               "response_format": {"type": "json_object"}}
    for tent in range(1, MAX_TENTATIVAS + 1):
        try:
            r = requests.post(URL, headers=HEADERS, json=payload, timeout=TIMEOUT_S)
            if r.status_code == 200:
                j = r.json()
                cont = j["choices"][0]["message"]["content"]
                usage = j.get("usage", {}) or {}
                custo = (((j.get("cost") or {}).get("token") or {}).get("total"))
                return json.loads(cont), {
                    "prompt_tokens": usage.get("prompt_tokens") or usage.get("promptTokens"),
                    "completion_tokens": usage.get("completion_tokens") or usage.get("completionTokens"),
                    "total_tokens": usage.get("total_tokens") or usage.get("totalTokens"),
                    "custo": custo,
                }
            log.warning("HTTP %s (tent %s): %s", r.status_code, tent, r.text[:200])
        except Exception as e:
            log.warning("erro (tent %s): %s", tent, e)
        time.sleep(5 * tent)
    return None, None

def processar(reg):
    linhas_out = []
    for grupo in GRUPOS_ATIVOS:
        gid = "_".join(grupo)
        if (reg["cd_segmento"], gid) in feitos:
            continue
        modelo = next((MODELO_POR_PROMPT[p] for p in grupo if p in MODELO_POR_PROMPT), MODELO)
        msgs = montar_mensagens(grupo, reg["transcricao"])
        resp, meta = _chamar(modelo, msgs)
        rec = {
            "cd_segmento": reg["cd_segmento"], "cliente_id": reg["cliente_id"],
            "data": reg["data"], "direcao": reg["direcao"],
            "nome_agente_1": reg["nome_agente_1"], "time_agente_1": reg["time_agente_1"],
            "grupo_id": gid, "modelo": modelo, "ts": datetime.now().isoformat(timespec="seconds"),
            "ok": resp is not None, "resposta": resp, "meta": meta,
        }
        if resp is None:
            with _lock_file:
                _acc["erros"] += 1
        elif meta:
            with _lock_file:
                _acc["tokens"] += meta.get("total_tokens") or 0
                _acc["custo"] += meta.get("custo") or 0.0
        linhas_out.append(rec)
    return linhas_out

with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
    futs = [ex.submit(processar, r) for r in registros]
    with open(ARQ_JSONL, "a", encoding="utf-8") as f:
        for fut in tqdm(as_completed(futs), total=len(futs)):
            for rec in fut.result():
                with _lock_file:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
                    f.flush()

print(f"tokens: {_acc['tokens']:,} | custo estimado: US$ {_acc['custo']:.2f} | erros: {_acc['erros']}")
'''

CONSOLIDA = r'''# ==================== CONSOLIDAÇÃO → CSVs ====================
recs = [json.loads(l) for l in ARQ_JSONL.read_text(encoding="utf-8").splitlines() if l.strip()]
recs = [r for r in recs if r.get("ok") and r.get("resposta")]

PESOS = {**{f"B{i}": 0 for i in range(1, 11)}, **PESOS_B}

def _lista(v):
    if isinstance(v, list):
        return [str(x).strip().upper() for x in v if str(x).strip().lower() not in ("", "nenhum", "na")]
    if isinstance(v, str):
        return [x.strip().upper() for x in re.split(r"[;,+/]", v) if x.strip().lower() not in ("", "nenhum", "na")]
    return []

por_prompt = {}          # prompt -> {cd_segmento: {campos}}
for r in recs:
    resp = r["resposta"]
    if not isinstance(resp, dict):
        continue
    for p, obj in resp.items():
        if not isinstance(obj, dict):
            obj = {"valor": obj}
        row = {"cd_segmento": r["cd_segmento"], "cliente_id": r["cliente_id"], "data": r["data"]}
        if p == "P1":
            bs = _lista(obj.get("B"))
            row.update(desfecho=obj.get("desfecho"), intencao_entrada=obj.get("intencao_entrada"),
                       tentativa_comercial=obj.get("tentativa_comercial"),
                       **{b: ("SIM" if b in bs else "NAO") for b in PESOS},
                       score_comercial=sum(PESOS[b] for b in bs if b in PESOS),
                       motivo=obj.get("motivo"))
        elif p == "P5":
            row.update(teve_challenger=obj.get("teve_challenger"),
                       codigos_challenger="+".join(_lista(obj.get("codigos_challenger"))) or "nenhum",
                       resultado_imediato=obj.get("resultado_imediato"),
                       qualidade=obj.get("qualidade"), frase_resumo=obj.get("frase_resumo"))
        elif p == "P3":
            row.update(problemas="+".join(_lista(obj.get("problemas"))) or "nenhum",
                       quem_relatou=obj.get("quem_relatou"), foi_resolvido=obj.get("foi_resolvido"),
                       escalou_para=obj.get("escalou_para"), observacao=obj.get("observacao"))
        else:
            row.update({k: (("+".join(_lista(v))) if isinstance(v, list) else v) for k, v in obj.items()})
        por_prompt.setdefault(p, {})[r["cd_segmento"]] = row

for p, d in por_prompt.items():
    pd.DataFrame(list(d.values())).to_csv(PASTA_SAIDA / f"{p}.csv", index=False, encoding="utf-8-sig")

# CONSOLIDADO: 1 linha por cd_segmento
meta_por_seg = {r["cd_segmento"]: r for r in recs}
todos_seg = sorted({s for d in por_prompt.values() for s in d})
linhas = []
for seg in todos_seg:
    m = meta_por_seg.get(seg, {})
    linha = {"cd_segmento": seg, "cliente_id": m.get("cliente_id"), "data": m.get("data"),
             "direcao": m.get("direcao"), "nome_agente_1": m.get("nome_agente_1"),
             "time_agente_1": m.get("time_agente_1")}
    for p, d in por_prompt.items():
        for k, v in d.get(seg, {}).items():
            if k not in ("cd_segmento", "cliente_id", "data"):
                linha[f"{p.lower()}_{k}"] = v
    linhas.append(linha)
pd.DataFrame(linhas).to_csv(PASTA_SAIDA / "CONSOLIDADO.csv", index=False, encoding="utf-8-sig")

print("CSVs gerados em", PASTA_SAIDA)
for p, d in sorted(por_prompt.items()):
    print(f"  {p}.csv: {len(d)} ligações")
print(f"  CONSOLIDADO.csv: {len(linhas)} ligações")
'''

MD_NOTAS = r"""## Notas

**Custo / cota.** Cada ligação da versão básica = 4 chamadas. `_acc` mostra tokens
e custo estimado ao fim do loop. Comece com `LIMITE_LIGACOES = 20` para calibrar.

**Modelo por prompt.** Se o P5 (Challenger) vier fraco no `gpt-4o-mini`, suba só ele:
`MODELO_POR_PROMPT = {"P5": "gpt-4o"}` — não precisa mexer no resto.

**Incremental.** `_resultados.jsonl` acumula. Re-rodar o loop só processa o que falta
(por `cd_segmento` × grupo). Para reprocessar tudo, apague o arquivo.

**score_comercial** é recalculado na consolidação a partir dos pesos de `Classificacoes_ligacoes.xlsx`
(não confia na soma do modelo).

**Reconciliação com a RMR.** Depois de rodar a base de um mês, comparar a distribuição
de `desfecho` (P1), a taxa de B5 e a de FC1/FC3 (P9) com os números da RMR. Se baterem
na mesma faixa, o `gpt-4o-mini` serve; se P5/B5 divergir muito, subir o P5 de modelo.

**Versão completa.** Só roda os prompts com aba em `Classificacoes_ligacoes.xlsx`.
Para habilitar P4/P6/P7/P8/P10/P11/P13/P15: criar a aba de taxonomia de cada um
(`scripts/gerar_classificacoes_ligacoes.py`) + minerar exemplos, e ajustar `SCHEMA`.
"""


def cell_md(src):
    return {"cell_type": "markdown", "metadata": {}, "source": src.splitlines(keepends=True)}


def cell_code(src):
    return {"cell_type": "code", "metadata": {}, "execution_count": None,
            "outputs": [], "source": src.strip("\n").splitlines(keepends=True)}


nb = {
    "cells": [
        cell_md(MD_INTRO),
        cell_code(CFG),
        cell_code(IMPORTS),
        cell_code(TAXONOMIA),
        cell_code(CONTEXTO),
        cell_code(CARREGAR),
        cell_code(LOOP),
        cell_code(CONSOLIDA),
        cell_md(MD_NOTAS),
    ],
    "metadata": {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.11"},
    },
    "nbformat": 4,
    "nbformat_minor": 5,
}

SAIDA.parent.mkdir(parents=True, exist_ok=True)
SAIDA.write_text(json.dumps(nb, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"OK -> {SAIDA}  ({len(nb['cells'])} células)")
