"""
Envia uma notificacao push (via ntfy.sh) resumindo a ultima execucao do
run_gemini_julho_daily.bat. Chamado no final do .bat, depois do
consolidar_julho.py.

(O job "Gemini Novo Lote" esta obsoleto/desativado - este script agora
reporta sempre o log do JULHO por padrao.)

Uso: notificar_ntfy.py [caminho_do_log] [titulo]

Para receber no celular: instale o app "ntfy" (Android/iOS) e assine o
topico abaixo (Configuracoes > Adicionar subscricao > cole o mesmo nome).
"""

import json
import re
import sys
import urllib.request
from collections import Counter
from pathlib import Path

TOPIC = "thiago-liga-gemini-o7h0wqmw5f"
BASE_DIR = Path(__file__).resolve().parent.parent
DEFAULT_LOG_PATH = BASE_DIR / "JULHO" / "log_execucao.txt"
DEFAULT_TITULO = "Gemini Julho"


def ultima_execucao(texto):
    blocos = re.split(r"===== Execucao agendada:.*=====", texto)
    return blocos[-1] if blocos else texto


def contar_por_grupo(nomes_batch):
    """Extrai o GRUPO (ex: P9_P10, P3_P7) do nome de cada arquivo salvo
    (formato batchNN_GRUPO_YYYYMMDD_HHMMSS.txt) e conta quantos batches
    de cada grupo foram processados nesta execucao."""
    grupos = Counter()
    for nome in nomes_batch:
        m = re.match(r"batch\d+_(.+)_\d{8}_\d{6}\.txt", nome)
        if m:
            grupos[m.group(1)] += 1
    return grupos


def resumir(bloco):
    salvos = re.findall(r"-> Salvo: (batch\d+_\S+)", bloco)
    grupos = contar_por_grupo(salvos)

    if "Todos os batches completos" in bloco:
        status = "Todos os batches concluidos!"
    elif "Cota diaria esgotada" in bloco or "chamadas atingido" in bloco:
        status = "Cota diaria do Gemini esgotada - continua amanha (reseta ~4h BRT)."
    elif salvos:
        status = "Execucao concluida."
    else:
        status = "Execucao rodou mas nao processou nenhum batch (confira o log)."

    if grupos:
        detalhe = " | ".join(f"{g}: {n}" for g, n in grupos.most_common())
        return f"{status} Batches processados hoje: {len(salvos)} ({detalhe})."
    return f"{status} Batches processados hoje: {len(salvos)}."


def notificar(mensagem, titulo):
    payload = json.dumps({
        "topic": TOPIC,
        "title": titulo,
        "message": mensagem,
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://ntfy.sh/",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        resp.read()


def main():
    log_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_LOG_PATH
    titulo = sys.argv[2] if len(sys.argv) > 2 else DEFAULT_TITULO

    if not log_path.is_absolute():
        log_path = BASE_DIR / log_path

    if not log_path.exists():
        notificar("Log nao encontrado apos a execucao agendada.", titulo)
        return

    texto = log_path.read_text(encoding="utf-8", errors="ignore")
    bloco = ultima_execucao(texto)
    notificar(resumir(bloco), titulo)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[notificar_ntfy] falha ao enviar notificacao: {e}")
