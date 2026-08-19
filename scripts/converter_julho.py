"""
Converte os brutos recebidos em JULHO/ (exports semicolon-delimited, encoding UTF-8)
para o mesmo formato JSON usado por dados/recebidos/bloco_lig_recebido_01.json:
  { "cliente_id_8digitos": [ {segment_id, data, duracao, sentimento, conversa: [[A/C, texto], ...]}, ... ] }

cd_contato_master vem corrompido (Excel converteu pra notacao cientifica, ex "7,11E+11" -
colapsa milhares de IDs distintos em 1-2 valores por arquivo). NAO USAR essa coluna.
Usar cd_segmento (uuid, unico por linha) como segment_id e CLIENTE como identificador do cliente.

Dois formatos de entrada:
1. ARQUIVOS (formato antigo, 01-21/07): export de 37 colunas, 1 arquivo por bloco de dias.
2. PASTAS_FORMATO_NOVO (formato novo, padrao a partir de 22/07/2026): 1 arquivo por dia
   (nome = dia do mes, sem extensao), so 10 colunas. NAO tem data_hora_fim (logo, sem
   duracao de ligacao - decisao do usuario em 04/08/2026: seguir sem esse campo, nao
   pedir no export) nem status_transcricao (redundante - validado que status="success"
   equivale 100% a transcricao_limpa nao-vazio no formato antigo). Em troca, traz
   direcao/nome_agente_1/time_agente_1, que o formato antigo tambem tem mas nunca foram
   extraidos aqui - capturados agora pra eventualmente preencher o gap de "quem vendeu"
   (ver nota H10 na memoria do projeto).

Idempotente: sempre reprocessa tudo do zero e regrava o JSON combinado.
"""
import csv
import json
from pathlib import Path
from datetime import datetime

JULHO_DIR = Path(__file__).parent.parent / "JULHO"
ARQUIVOS = [
    "arq1 - correto (1).txt",
    "arq1 (1).2",
    "arq2 (1).txt",
    "arq2 (1).2",
]
# Pastas com arquivos diarios no formato novo (10 colunas) - adicionar novas pastas
# aqui conforme forem chegando (ex: proximo mes, proximo range de dias).
PASTAS_FORMATO_NOVO = [
    JULHO_DIR / "Ligações_22_31",
]
OUT_PATH = JULHO_DIR / "dados_convertidos" / "julho_completo.json"


def parse_dt(s):
    # "2026-07-06 17:34:51.000000 UTC"
    s = s.strip().replace(" UTC", "")
    return datetime.strptime(s, "%Y-%m-%d %H:%M:%S.%f")


def transcricao_para_conversa(texto):
    turnos = []
    for parte in texto.split("|"):
        parte = parte.strip()
        if not parte or ":" not in parte:
            continue
        speaker, fala = parte.split(":", 1)
        speaker = speaker.strip().upper()
        if speaker == "AGENTE":
            cod = "A"
        elif speaker == "CLIENTE":
            cod = "C"
        else:
            continue
        fala = fala.strip()
        if fala:
            turnos.append([cod, fala])
    return turnos


def processar_arquivo_formato_novo(caminho, dados, stats):
    n_usadas = 0
    with open(caminho, encoding="utf-8", errors="replace", newline="") as fh:
        reader = csv.DictReader(fh, delimiter=";")
        for row in reader:
            stats["linhas"] += 1
            transcricao = row["transcricao_limpa"].strip()
            # sem status_transcricao neste formato - texto vazio e equivalente
            # (validado contra o formato antigo: status=success <=> texto nao-vazio)
            if not transcricao:
                stats["sem_transcricao"] += 1
                continue

            cliente_raw = row["Cliente"].strip()
            segment_id = row["cd_segmento"].strip()

            if cliente_raw in ("", "0"):
                stats["sem_cliente"] += 1
                continue

            # Cliente so numerico = ID real. Qualquer outra coisa (ex: "Sem
            # Codigo", que vem corrompido na fonte) e placeholder sem vinculo
            # confiavel - mesma logica do "Sem Informacao" do formato antigo:
            # mantem a ligacao com chave sintetica propria, sem agrupar todas
            # sob a mesma chave (evita "cliente" fantasma gigante).
            if not cliente_raw.isdigit():
                cliente = f"SEMINFO_{segment_id}"
                stats["sem_info_mantida"] = stats.get("sem_info_mantida", 0) + 1
            else:
                cliente = cliente_raw.zfill(8)

            try:
                dt_ini = parse_dt(row["data_hora_inicio"])
            except Exception:
                dt_ini = None

            conversa = transcricao_para_conversa(transcricao)
            if not conversa:
                stats["sem_transcricao"] += 1
                continue

            registro = {
                "segment_id": segment_id,
                "data": (dt_ini.isoformat() + "Z") if dt_ini else None,
                "duracao": None,  # formato novo nao tem data_hora_fim
                "sentimento": "",
                "conversa": conversa,
                "direcao": row.get("direcao", "").strip(),
                "agente_id": row.get("nome_agente_1", "").strip(),
                "time_agente": row.get("time_agente_1", "").strip(),
            }
            dados.setdefault(cliente, []).append(registro)
            stats["usadas"] += 1
            n_usadas += 1
    stats["por_arquivo"][caminho.name] = n_usadas


def main():
    dados = {}
    stats = {"linhas": 0, "sem_transcricao": 0, "sem_cliente": 0, "sem_info_mantida": 0, "usadas": 0, "por_arquivo": {}}

    for pasta in PASTAS_FORMATO_NOVO:
        if not pasta.exists():
            continue
        for caminho in sorted(pasta.iterdir()):
            if not caminho.is_file():
                continue
            processar_arquivo_formato_novo(caminho, dados, stats)

    for nome_arquivo in ARQUIVOS:
        caminho = JULHO_DIR / nome_arquivo
        n_usadas = 0
        with open(caminho, encoding="utf-8", errors="replace") as fh:
            reader = csv.reader(fh, delimiter=";")
            header = next(reader)
            idx = {campo: header.index(campo) for campo in [
                "cd_segmento", "data_hora_inicio", "data_hora_fim",
                "status_transcricao", "transcricao_limpa", "CLIENTE",
            ]}
            for row in reader:
                if len(row) <= max(idx.values()):
                    continue
                stats["linhas"] += 1
                transcricao = row[idx["transcricao_limpa"]].strip()
                status = row[idx["status_transcricao"]].strip().lower()
                if status != "success" or not transcricao:
                    stats["sem_transcricao"] += 1
                    continue

                cliente_raw = row[idx["CLIENTE"]].strip()
                segment_id = row[idx["cd_segmento"]].strip()

                # CLIENTE="0": excluido por completo (maioria e correio de voz/
                # nao atendida, sem valor de analise por cliente)
                if cliente_raw in ("", "0"):
                    stats["sem_cliente"] += 1
                    continue

                # "Sem Informacao" vem corrompido na fonte (bytes literais de
                # U+FFFD no meio, ex: "Sem Informa��o") — casar por prefixo.
                # Mantemos a ligacao (tem transcricao valida, conversa real),
                # mas SEM agrupar todas sob a mesma chave literal (isso criava
                # um "cliente" fantasma de 480 ligacoes, quebrando o batching).
                # Cada uma vira uma entrada propria via segment_id.
                if cliente_raw.lower().startswith("sem informa"):
                    cliente = f"SEMINFO_{segment_id}"
                    stats["sem_info_mantida"] = stats.get("sem_info_mantida", 0) + 1
                else:
                    cliente = cliente_raw.zfill(8)
                try:
                    dt_ini = parse_dt(row[idx["data_hora_inicio"]])
                    dt_fim = parse_dt(row[idx["data_hora_fim"]])
                    duracao = int((dt_fim - dt_ini).total_seconds())
                except Exception:
                    dt_ini = None
                    duracao = None

                conversa = transcricao_para_conversa(transcricao)
                if not conversa:
                    stats["sem_transcricao"] += 1
                    continue

                registro = {
                    "segment_id": segment_id,
                    "data": (dt_ini.isoformat() + "Z") if dt_ini else None,
                    "duracao": duracao,
                    "sentimento": "",
                    "conversa": conversa,
                }
                dados.setdefault(cliente, []).append(registro)
                stats["usadas"] += 1
                n_usadas += 1
        stats["por_arquivo"][nome_arquivo] = n_usadas

    # remove duplicatas por segment_id (defensivo, caso arquivos se sobreponham)
    for cliente, ligacoes in dados.items():
        vistos = set()
        unicas = []
        for lig in ligacoes:
            if lig["segment_id"] in vistos:
                continue
            vistos.add(lig["segment_id"])
            unicas.append(lig)
        dados[cliente] = unicas

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT_PATH, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False)

    total_ligacoes = sum(len(v) for v in dados.values())
    print(f"Clientes unicos: {len(dados)}")
    print(f"Ligacoes convertidas: {total_ligacoes}")
    print(f"Linhas lidas: {stats['linhas']} | sem transcricao/vazias: {stats['sem_transcricao']} | excluidas (CLIENTE=0): {stats['sem_cliente']} | 'Sem Informacao' mantidas (id sintetico): {stats['sem_info_mantida']} | usadas: {stats['usadas']}")
    print("Por arquivo:", stats["por_arquivo"])
    print(f"Salvo em: {OUT_PATH}")


if __name__ == "__main__":
    main()
