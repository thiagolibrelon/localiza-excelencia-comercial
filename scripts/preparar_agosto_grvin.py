"""Filtra o export bruto de agosto (37/36 colunas) para o time GRVIN e projeta
no schema canonico de 10 colunas usado por ligacoes_genai/GEN_AI_LIGACOES.ipynb.

Entrada:  _pacote_rmr/dados/ligacoes_15356.csv (schema bruto Iceberg, 36 colunas,
          sem coluna "CLIENTE" nesta exportacao).
Saida:    chamadas/agosto/<dia> — um arquivo por dia util, CSV ';'-delimitado,
          UTF-8, schema:
          cd_contato_master;cd_segmento;data_hora_inicio;direcao;nome_agente_1;
          time_agente_1;habilidades_agente_1;transcricao_limpa;Cliente;Data

Filtros: time_agente_1 == "LL_GRVIN" (unico valor com "GRVIN" no lote),
status_transcricao == "success", transcricao_limpa com >=40 caracteres depois
de strip (mesmo limiar do notebook).

Reproduzivel — rodar de novo sempre que o CSV de origem mudar.
"""
import csv
from collections import Counter, defaultdict
from pathlib import Path

csv.field_size_limit(10_000_000)

ORIGEM = Path(__file__).parent.parent / "_pacote_rmr" / "dados" / "ligacoes_15356.csv"
SAIDA_DIR = Path(__file__).parent.parent / "chamadas" / "agosto"
TIME_ALVO = "LL_GRVIN"

COLS_SAIDA = [
    "cd_contato_master", "cd_segmento", "data_hora_inicio", "direcao",
    "nome_agente_1", "time_agente_1", "habilidades_agente_1",
    "transcricao_limpa", "Cliente", "Data",
]


def main():
    SAIDA_DIR.mkdir(parents=True, exist_ok=True)

    por_dia = defaultdict(list)
    motivos_excluidos = Counter()
    total = 0

    with open(ORIGEM, encoding="utf-8", newline="") as f:
        leitor = csv.DictReader(f)
        for row in leitor:
            total += 1

            if (row.get("time_agente_1") or "").strip() != TIME_ALVO:
                motivos_excluidos["outro_time"] += 1
                continue
            if (row.get("status_transcricao") or "").strip() != "success":
                motivos_excluidos["status_nao_success"] += 1
                continue

            transcricao = (row.get("transcricao_limpa") or "").strip()
            if len(transcricao) < 40:
                motivos_excluidos["transcricao_curta_ou_vazia"] += 1
                continue

            data_hora = (row.get("data_hora_inicio") or "").strip()
            dia = data_hora[:10]  # YYYY-MM-DD

            saida = {
                "cd_contato_master": row.get("cd_contato_master", ""),
                "cd_segmento": row.get("cd_segmento", ""),
                "data_hora_inicio": data_hora,
                "direcao": row.get("direcao", ""),
                "nome_agente_1": row.get("nome_agente_1", ""),
                "time_agente_1": row.get("time_agente_1", ""),
                "habilidades_agente_1": row.get("habilidades_agente_1", ""),
                "transcricao_limpa": transcricao,
                "Cliente": "",  # export bruto nao tem coluna CLIENTE
                "Data": dia,
            }
            por_dia[dia].append(saida)

    for dia, linhas in sorted(por_dia.items()):
        nome_arquivo = dia[8:10]  # so o dia do mes, seguindo o padrao "22","23"...
        caminho = SAIDA_DIR / nome_arquivo
        with open(caminho, "w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=COLS_SAIDA, delimiter=";")
            w.writeheader()
            w.writerows(linhas)

    print(f"total linhas no CSV de origem: {total}")
    print(f"excluidas: {dict(motivos_excluidos)}")
    aptas = sum(len(v) for v in por_dia.values())
    print(f"aptas (GRVIN, success, transcricao valida): {aptas}")
    print(f"arquivos gerados em {SAIDA_DIR}:")
    for dia in sorted(por_dia):
        print(f"  {dia[8:10]} ({dia}): {len(por_dia[dia])} ligacoes")


if __name__ == "__main__":
    main()
