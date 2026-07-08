"""
Etapa 3 do pipeline diario de ligacoes.

Le os batches .txt crus gerados por analisar_gemini_ligacoes_diarias.py em
resultados/gemini_ligacoes_diarias/<data>/, parseia as 6 sub-tabelas CSV
(P1, P2, P5, P6, P9, P10 - mesma receita de parsing ja usada em
cruzamento_hipoteses.py/cruzar_reservas.py: glob por padrao -> dedupe por
numero de batch mantendo o maior arquivo -> alternar dentro/fora de cada
sub-tabela pela linha de cabecalho -> split por virgula), junta tudo por
(cliente_id, data), acrescenta carteira/distrital/cnae (lidos do JSON de
entrada da Etapa 1) e grava 1 JSON por dia com 1 objeto por ligacao.

Rodar depois que analisar_gemini_ligacoes_diarias.py tiver terminado um dia:
  python scripts/compilar_gemini_ligacoes_diarias.py
"""
import json
import re
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
GEMINI_DIR = BASE / "resultados" / "gemini_ligacoes_diarias"
ENTRADA_DIR = BASE / "dados_ligacoes_diarias" / "entrada"
SAIDA_DIR = BASE / "dados_ligacoes_diarias" / "analisado"

_AB = {"AB1", "AB2", "AB3", "AB4", "AB5"}
_FC = {"FC1", "FC2", "FC3", "FC4", "FC5"}
_PM = {"PM1", "PM2", "PM3", "PM4", "PM5", "PM6"}


def limpar_texto_livre(s):
    s = s.strip()
    if len(s) >= 2 and s[0] == '"' and s[-1] == '"':
        s = s[1:-1].strip()
    return s


def normalizar_cod(cod):
    cod = str(cod or "").strip()
    if not cod or cod.lower() == "nan":
        return None
    if cod.endswith(".0"):
        cod = cod[:-2]
    return cod.zfill(8)


def arquivos_validos(pasta, padrao):
    """Dedup por numero de batch, mantendo sempre o maior arquivo (re-runs)."""
    por_batch = defaultdict(list)
    for f in pasta.glob(padrao):
        m = re.match(r"batch(\d+)_", f.name)
        if m:
            por_batch[m.group(1)].append(f)
    return [max(v, key=lambda x: x.stat().st_size) for v in por_batch.values()]


# ---------------------------------------------------------------------------
# Parsers por sub-tabela (todas retornam dict (cid, data) -> campos)
# ---------------------------------------------------------------------------
def parse_p1(pasta):
    out = {}
    for f in arquivos_validos(pasta, "batch*_P1_P2_*.txt"):
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
            cid, data = normalizar_cod(parts[0]), parts[1].strip()
            if not cid:
                continue
            out[(cid, data)] = {
                "duracao_s": parts[2].strip(),
                "desfecho": parts[3].strip(),
                "intencao_entrada": parts[4].strip(),
                "tentativa_comercial_p1": parts[5].strip(),
                **{f"B{i+1}": parts[6 + i].strip().upper() == "SIM" for i in range(10)},
                "score_comercial": parts[16].strip(),
            }
    return out


def parse_p2(pasta):
    out = {}
    for f in arquivos_validos(pasta, "batch*_P1_P2_*.txt"):
        in_p2 = False
        for line in f.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("cliente_id,data,tipo,"):
                in_p2 = True
                continue
            if s.startswith("cliente_id,data,duracao"):
                in_p2 = False
                continue
            if not in_p2 or not s or s.startswith("#") or s.startswith("```"):
                continue
            parts = s.split(",")
            if len(parts) < 6:
                continue
            cid, data = normalizar_cod(parts[0]), parts[1].strip()
            if not cid:
                continue
            out[(cid, data)] = {
                "tipo_ligacao": parts[2].strip(),
                "subtipo_ligacao": parts[3].strip(),
                "quem_iniciou": parts[4].strip(),
                "tentativa_comercial_p2": parts[5].strip(),
            }
    return out


def parse_p5(pasta):
    out = {}
    for f in arquivos_validos(pasta, "batch*_P5_P6_*.txt"):
        in_p5 = False
        for line in f.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("cliente_id,data,teve_challenger"):
                in_p5 = True
                continue
            if s.startswith("cliente_id,data,oportunidades_perdidas"):
                in_p5 = False
                continue
            if not in_p5 or not s or s.startswith("#") or s.startswith("```") or s.startswith("###"):
                continue
            # cliente_id,data,teve_challenger,codigos_challenger,frase_resumo,resultado_imediato,qualidade
            esq = s.split(",", 2)  # [cid, data, resto]
            if len(esq) < 3:
                continue
            resto = esq[2].rsplit(",", 2)  # [codigos+frase, resultado_imediato, qualidade]
            if len(resto) < 3:
                continue
            meio = resto[0].split(",", 1)  # [teve_challenger, codigos+frase] ou so [teve_challenger]
            teve = meio[0].strip()
            resto2 = meio[1].split(",", 1) if len(meio) > 1 else ["", ""]
            codigos = resto2[0].strip()
            frase = limpar_texto_livre(resto2[1]) if len(resto2) > 1 else ""
            cid, data = normalizar_cod(esq[0]), esq[1].strip()
            if not cid:
                continue
            out[(cid, data)] = {
                "teve_challenger": teve.upper() == "SIM",
                "codigos_challenger": [c.strip() for c in re.split(r"[|;]", codigos) if c.strip().startswith("CH")],
                "frase_resumo_challenger": frase,
                "resultado_imediato_challenger": resto[1].strip(),
                "qualidade_challenger": resto[2].strip(),
            }
    return out


def parse_p6(pasta):
    out = {}
    for f in arquivos_validos(pasta, "batch*_P5_P6_*.txt"):
        in_p6 = False
        for line in f.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("cliente_id,data,oportunidades_perdidas"):
                in_p6 = True
                continue
            if s.startswith("cliente_id,data,teve_challenger") or s.startswith("```") or s.startswith("###"):
                in_p6 = False
                continue
            if not in_p6 or not s or s.startswith("#"):
                continue
            # cliente_id,data,oportunidades_perdidas,descricao_curta,valor_potencial_R$
            esq = s.split(",", 2)  # [cid, data, resto]
            if len(esq) < 3:
                continue
            resto = esq[2].rsplit(",", 1)  # [op+descricao, valor]
            if len(resto) < 2:
                continue
            meio = resto[0].split(",", 1)
            op = meio[0].strip()
            desc = limpar_texto_livre(meio[1]) if len(meio) > 1 else ""
            cid, data = normalizar_cod(esq[0]), esq[1].strip()
            if not cid:
                continue
            oportunidades = [o.strip() for o in re.split(r"[|;]", op) if o.strip() and o.strip() != "nenhuma"]
            out[(cid, data)] = {
                "oportunidades_perdidas": oportunidades,
                "descricao_oportunidade_perdida": desc,
                "valor_potencial_oportunidade": resto[1].strip(),
            }
    return out


def parse_p9(pasta):
    out = {}
    for f in arquivos_validos(pasta, "batch*_P9_P10_*.txt"):
        in_p9 = False
        for line in f.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("cliente_id,data,tipo_abertura"):
                in_p9 = True
                continue
            if s.startswith("promise_id,"):
                in_p9 = False
                continue
            if not in_p9 or not s or s.startswith("#") or s.startswith("```") or s.startswith("==="):
                continue
            parts = s.split(",")
            if len(parts) < 8:
                continue
            cid, data = normalizar_cod(parts[0]), parts[1].strip()
            ab, fc = parts[2].strip().upper(), parts[4].strip().upper()
            if not cid or ab not in _AB or fc not in _FC:
                continue
            out[(cid, data)] = {
                "tipo_abertura": ab,
                "usou_nome": parts[3].strip().upper() == "SIM",
                "tipo_fechamento": fc,
                "proximo_passo_claro": parts[5].strip().upper() == "SIM",
                "prazo_definido": parts[6].strip().upper() == "SIM",
                "desfecho_p9": parts[7].strip(),
            }
    return out


def parse_p10(pasta):
    """Retorna dict (cid, data) -> lista de promessas (pode ter mais de 1 por ligacao)."""
    out = defaultdict(list)
    for f in arquivos_validos(pasta, "batch*_P9_P10_*.txt"):
        in_p10 = False
        for line in f.read_text(encoding="utf-8").splitlines():
            s = line.strip()
            if s.startswith("promise_id,"):
                in_p10 = True
                continue
            if s.startswith("cliente_id,data,tipo_abertura") or s.startswith("```") or s.startswith("==="):
                in_p10 = False
                continue
            if not in_p10 or not s or s.startswith("#"):
                continue
            # promise_id,cliente_id,data,tipo_promessa,frase_resumo,prazo_prometido,risco_nao_cumprimento
            esq = s.split(",", 4)  # [promise_id, cid, data, tipo_promessa, resto]
            if len(esq) < 5:
                continue
            resto = esq[4].rsplit(",", 2)  # [frase, prazo, risco]
            if len(resto) < 3:
                continue
            tipo_pm = esq[3].strip().upper()
            if tipo_pm not in _PM:
                continue
            cid, data = normalizar_cod(esq[1]), esq[2].strip()
            if not cid:
                continue
            out[(cid, data)].append({
                "promise_id": esq[0].strip(),
                "tipo_promessa": tipo_pm,
                "frase_resumo": limpar_texto_livre(resto[0]),
                "prazo_prometido": resto[1].strip(),
                "risco_nao_cumprimento": resto[2].strip(),
            })
    return out


# ---------------------------------------------------------------------------
# Metadados da Etapa 1 (carteira/distrital/cnae por cliente)
# ---------------------------------------------------------------------------
def carregar_metadados_clientes(data_str):
    caminho = ENTRADA_DIR / f"ligacoes_{data_str}.json"
    if not caminho.exists():
        return {}
    with open(caminho, encoding="utf-8") as f:
        entrada = json.load(f)
    return {
        cod: {
            "carteira": info.get("carteira", "SEM_CARTEIRA"),
            "distrital": info.get("distrital", ""),
            "cnae": info.get("cnae", "SEM_CNAE"),
        }
        for cod, info in entrada.items()
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def compilar_dia(pasta_dia, data_str):
    p1 = parse_p1(pasta_dia)
    p2 = parse_p2(pasta_dia)
    p5 = parse_p5(pasta_dia)
    p6 = parse_p6(pasta_dia)
    p9 = parse_p9(pasta_dia)
    p10 = parse_p10(pasta_dia)
    metadados = carregar_metadados_clientes(data_str)

    todas_keys = set(p1) | set(p2) | set(p5) | set(p6) | set(p9) | set(p10)
    if not todas_keys:
        return []

    linhas = []
    for cid, data in sorted(todas_keys):
        meta = metadados.get(cid, {"carteira": "SEM_CARTEIRA", "distrital": "", "cnae": "SEM_CNAE"})
        row = {"cliente_id": cid, "data": data, **meta}
        row.update(p1.get((cid, data), {}))
        row.update(p2.get((cid, data), {}))
        row.update(p5.get((cid, data), {}))
        row.update(p6.get((cid, data), {}))
        row.update(p9.get((cid, data), {}))
        row["promessas"] = p10.get((cid, data), [])
        linhas.append(row)
    return linhas


def main():
    if not GEMINI_DIR.exists():
        print(f"Nenhuma saida do Gemini encontrada em {GEMINI_DIR}. Nada a fazer.")
        return

    SAIDA_DIR.mkdir(parents=True, exist_ok=True)

    for pasta_dia in sorted(p for p in GEMINI_DIR.iterdir() if p.is_dir()):
        data_str = pasta_dia.name
        saida = SAIDA_DIR / f"ligacoes_analisadas_{data_str}.json"
        if saida.exists():
            print(f"{data_str}: ja compilado ({saida.name}) — pulando.")
            continue

        linhas = compilar_dia(pasta_dia, data_str)
        if not linhas:
            print(f"{data_str}: nenhuma linha parseada (batches ausentes ou vazios) — pulando.")
            continue

        with open(saida, "w", encoding="utf-8") as f:
            json.dump(linhas, f, ensure_ascii=False, separators=(",", ":"))

        com_desfecho = sum(1 for r in linhas if r.get("desfecho"))
        print(f"{data_str}: {len(linhas)} ligacoes compiladas ({com_desfecho} com desfecho) -> {saida}")


if __name__ == "__main__":
    main()
