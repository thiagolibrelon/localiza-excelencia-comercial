"""
Etapa 1 do pipeline diario de ligacoes.

Le os 3 exports brutos do dia (Cliente, Transcricao, Cliente_fixo, formato de
amostra em scripts/Diario), junta tudo pelo cliente/segmento, e gera 1 JSON
do dia no mesmo formato ja consumido pelo pipeline de analise via Gemini
(schema de dados/LIG e dados/recebidos/bloco_lig_recebido_01.json), soh que
com carteira/distrital/cnae embutidos por cliente.

Rodar todo dia (localmente):
  1. Sobrescrever os 3 arquivos em dados/ligacoes_diarias_bruto/
     (cliente.csv, transcricao.csv, cliente_fixo.csv) com o export do dia.
  2. python scripts/gerar_ligacoes_diarias.py
  3. Conferir o resumo impresso no console.
  4. git add dados_ligacoes_diarias/entrada/ligacoes_<data>.json + commit + push.
"""
import csv
import json
import unicodedata
from collections import Counter
from datetime import datetime, date
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
RAW_DIR = BASE / "dados" / "ligacoes_diarias_bruto"
CLIENTE_CSV = RAW_DIR / "cliente.csv"
TRANSCRICAO_CSV = RAW_DIR / "transcricao.csv"
CLIENTE_FIXO_CSV = RAW_DIR / "cliente_fixo.csv"
OUT_DIR = BASE / "dados_ligacoes_diarias" / "entrada"

SPEAKER_MAP = {"CLIENTE": "C", "AGENTE": "A", "ATENDENTE": "A", "VENDEDOR": "A"}


# ---------------------------------------------------------------------------
# Utilidades
# ---------------------------------------------------------------------------
def slug(texto):
    texto = unicodedata.normalize("NFKD", str(texto))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return texto.strip().lower()


def ler_csv_auto(caminho):
    """Detecta virgula vs tabulacao pela primeira linha e retorna DictReader materializado."""
    with open(caminho, encoding="utf-8", newline="") as f:
        primeira_linha = f.readline()
        delimitador = "\t" if primeira_linha.count("\t") > primeira_linha.count(",") else ","
        f.seek(0)
        leitor = csv.DictReader(f, delimiter=delimitador)
        linhas = list(leitor)
        campos_por_slug = {slug(c): c for c in (leitor.fieldnames or [])}
    return linhas, campos_por_slug


def valor(row, campos_por_slug, *slugs_possiveis):
    for s in slugs_possiveis:
        campo = campos_por_slug.get(s)
        if campo is not None:
            return row.get(campo)
    return None


def normalizar_cod(cod):
    cod = str(cod or "").strip()
    if not cod or cod.lower() == "nan":
        return None
    if cod.endswith(".0"):
        cod = cod[:-2]
    return cod.zfill(8)


def normalizar_num(v):
    v = str(v or "").strip()
    if not v or v.lower() == "nan":
        return None
    if v.endswith(".0"):
        v = v[:-2]
    return v


def corrigir_mojibake(texto):
    if not texto:
        return texto
    if not any(ch in texto for ch in ("Ã", "Â")):
        return texto
    try:
        return texto.encode("latin-1").decode("utf-8")
    except (UnicodeDecodeError, UnicodeEncodeError):
        return texto


def parse_conversa(texto):
    if not texto:
        return []
    turnos = []
    for parte in texto.split(" | "):
        parte = parte.strip()
        if not parte:
            continue
        if ": " in parte:
            speaker_raw, fala = parte.split(": ", 1)
        else:
            speaker_raw, fala = "?", parte
        speaker = SPEAKER_MAP.get(speaker_raw.strip().upper(), (speaker_raw.strip()[:1] or "?"))
        turnos.append([speaker, fala.strip()])
    return turnos


def parse_timestamp(v):
    if not v:
        return None
    v = v.strip()
    if v.endswith(" UTC"):
        v = v[:-4]
    for fmt in ("%Y-%m-%d %H:%M:%S.%f", "%Y-%m-%d %H:%M:%S"):
        try:
            return datetime.strptime(v, fmt)
        except ValueError:
            continue
    return None


def calcular_duracao(inicio, fim):
    dt_i, dt_f = parse_timestamp(inicio), parse_timestamp(fim)
    if dt_i and dt_f:
        return round((dt_f - dt_i).total_seconds())
    return None


def parece_data(v):
    v = str(v or "").strip()
    if not v:
        return False
    for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
        try:
            datetime.strptime(v[:10], fmt)
            return True
        except ValueError:
            continue
    return False


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    for caminho in (CLIENTE_CSV, TRANSCRICAO_CSV, CLIENTE_FIXO_CSV):
        if not caminho.exists():
            raise SystemExit(f"Arquivo bruto nao encontrado: {caminho}")

    cliente_rows, cliente_slugs = ler_csv_auto(CLIENTE_CSV)
    transcricao_rows, transc_slugs = ler_csv_auto(TRANSCRICAO_CSV)
    fixo_rows, fixo_slugs = ler_csv_auto(CLIENTE_FIXO_CSV)

    # ---- indices de transcricao pelas 2 chaves candidatas ----
    por_segmento, por_contato = {}, {}
    for row in transcricao_rows:
        seg = valor(row, transc_slugs, "cd_segmento")
        if seg:
            por_segmento[seg.strip()] = row
        contato = normalizar_num(valor(row, transc_slugs, "cd_contato_master"))
        if contato:
            por_contato[contato] = row

    # ---- decide qual chave casa mais no arquivo do dia ----
    matches_segmento = sum(
        1 for r in cliente_rows
        if (valor(r, cliente_slugs, "segment_id") or "").strip() in por_segmento
    )
    matches_contato = sum(
        1 for r in cliente_rows
        if normalizar_num(valor(r, cliente_slugs, "call_object")) in por_contato
    )
    primaria, secundaria = (
        ("segment_id", "call_object") if matches_segmento >= matches_contato
        else ("call_object", "segment_id")
    )
    print(f"Chave escolhida como principal: {primaria} "
          f"(segment_id={matches_segmento} matches, call_object={matches_contato} matches)")

    # ---- cliente_fixo indexado por codigo normalizado ----
    fixo_por_cod = {}
    datas_estranhas = 0
    for row in fixo_rows:
        cod = normalizar_cod(valor(row, fixo_slugs, "codigo do cliente"))
        if not cod:
            continue
        data_locacao = valor(row, fixo_slugs, "data ultima locacao")
        if data_locacao and not parece_data(data_locacao):
            datas_estranhas += 1
        fixo_por_cod[cod] = {
            "carteira": valor(row, fixo_slugs, "carteira") or "SEM_CARTEIRA",
            "distrital": valor(row, fixo_slugs, "distrital") or "",
            "cnae": valor(row, fixo_slugs, "divisao cnae") or "SEM_CNAE",
        }

    # ---- monta o join final ----
    clientes = {}
    sem_codigo_cliente = 0
    sem_transcricao = 0
    sem_cliente_fixo = 0
    usados_segment_id = 0
    usados_call_object = 0
    datas_registro = Counter()

    for row in cliente_rows:
        codigo_cliente = normalizar_cod(valor(row, cliente_slugs, "codigo_cliente"))
        segment_id = (valor(row, cliente_slugs, "segment_id") or "").strip()
        call_object = valor(row, cliente_slugs, "call_object")
        data_inclusao = valor(row, cliente_slugs, "data_inclusao_registro")
        if data_inclusao:
            datas_registro[data_inclusao[:10]] += 1

        if not codigo_cliente:
            sem_codigo_cliente += 1
            continue

        transc_row = None
        chave_usada = None
        if primaria == "segment_id":
            transc_row = por_segmento.get(segment_id)
            chave_usada = "segment_id" if transc_row else None
            if not transc_row:
                transc_row = por_contato.get(normalizar_num(call_object))
                chave_usada = "call_object" if transc_row else None
        else:
            transc_row = por_contato.get(normalizar_num(call_object))
            chave_usada = "call_object" if transc_row else None
            if not transc_row:
                transc_row = por_segmento.get(segment_id)
                chave_usada = "segment_id" if transc_row else None

        if chave_usada == "segment_id":
            usados_segment_id += 1
        elif chave_usada == "call_object":
            usados_call_object += 1

        if transc_row:
            texto = corrigir_mojibake(valor(transc_row, transc_slugs, "transcricao_limpa") or "")
            conversa = parse_conversa(texto)
            data_ligacao = valor(transc_row, transc_slugs, "data_hora_inicio") or data_inclusao
            duracao = calcular_duracao(
                valor(transc_row, transc_slugs, "data_hora_inicio"),
                valor(transc_row, transc_slugs, "data_hora_fim"),
            )
        else:
            sem_transcricao += 1
            conversa = []
            data_ligacao = data_inclusao
            duracao = None

        info_fixo = fixo_por_cod.get(codigo_cliente)
        if info_fixo is None:
            sem_cliente_fixo += 1
            info_fixo = {"carteira": "SEM_REGISTRO", "distrital": "", "cnae": "SEM_REGISTRO"}

        registro = clientes.setdefault(codigo_cliente, {
            "carteira": info_fixo["carteira"],
            "distrital": info_fixo["distrital"],
            "cnae": info_fixo["cnae"],
            "ligacoes": [],
        })
        registro["ligacoes"].append({
            "segment_id": segment_id,
            "data": data_ligacao,
            "duracao": duracao,
            "conversa": conversa,
        })

    # ---- data do arquivo de saida: dia mais comum em data_inclusao_registro ----
    if datas_registro:
        data_arquivo = datas_registro.most_common(1)[0][0]
    else:
        data_arquivo = date.today().isoformat()

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    caminho_saida = OUT_DIR / f"ligacoes_{data_arquivo}.json"
    with open(caminho_saida, "w", encoding="utf-8") as f:
        json.dump(clientes, f, ensure_ascii=False, separators=(",", ":"))

    total_ligacoes = sum(len(c["ligacoes"]) for c in clientes.values())
    print("=" * 60)
    print(f"Linhas lidas em Cliente:        {len(cliente_rows)}")
    print(f"Linhas lidas em Transcricao:     {len(transcricao_rows)}")
    print(f"Linhas lidas em Cliente_fixo:    {len(fixo_rows)}")
    print(f"Casadas via segment_id:          {usados_segment_id}")
    print(f"Casadas via call_object:         {usados_call_object}")
    print(f"Sem transcricao correspondente:  {sem_transcricao}")
    print(f"Sem codigo_cliente (descartadas):{sem_codigo_cliente}")
    print(f"Sem registro em Cliente_fixo:    {sem_cliente_fixo}")
    if datas_estranhas:
        print(f"AVISO: {datas_estranhas} linha(s) de Cliente_fixo com 'Data ultima locacao' "
              f"que nao parece data - confira o alinhamento das colunas do export.")
    print(f"Total de clientes no arquivo:    {len(clientes)}")
    print(f"Total de ligacoes no arquivo:    {total_ligacoes}")
    print(f"Arquivo gerado: {caminho_saida}")


if __name__ == "__main__":
    main()
