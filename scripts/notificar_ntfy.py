"""
Envia uma notificacao push (via ntfy.sh) resumindo a ultima execucao do
run_gemini_novo_lote_daily.bat. Chamado no final do .bat, depois do
analisar_gemini_novo_lote.py.

Para receber no celular: instale o app "ntfy" (Android/iOS) e assine o
topico abaixo (Configuracoes > Adicionar subscricao > cole o mesmo nome).
"""

import json
import re
import urllib.request
from pathlib import Path

TOPIC = "thiago-liga-gemini-o7h0wqmw5f"
LOG_PATH = Path(__file__).resolve().parent.parent / "resultados" / "gemini_novo_lote" / "log_execucao.txt"


def ultima_execucao(texto):
    blocos = re.split(r"===== Execucao agendada:.*=====", texto)
    return blocos[-1] if blocos else texto


def resumir(bloco):
    salvos = re.findall(r"-> Salvo: (batch\d+_\S+)", bloco)

    if "Todos os batches completos" in bloco:
        status = "Todos os batches concluidos!"
    elif "chamadas atingido" in bloco:
        status = "Limite diario do Gemini atingido - continua amanha."
    elif salvos:
        status = "Execucao concluida."
    else:
        status = "Execucao rodou mas nao processou nenhum batch (confira o log)."

    return f"{status} Batches processados hoje: {len(salvos)}."


def notificar(mensagem, titulo="Gemini Novo Lote"):
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
    if not LOG_PATH.exists():
        notificar("Log nao encontrado apos a execucao agendada.")
        return

    texto = LOG_PATH.read_text(encoding="utf-8", errors="ignore")
    bloco = ultima_execucao(texto)
    notificar(resumir(bloco))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[notificar_ntfy] falha ao enviar notificacao: {e}")
