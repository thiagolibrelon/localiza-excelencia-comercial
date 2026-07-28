"""
Envia uma notificacao push (via ntfy.sh) avisando que a execucao diaria do
Gemini Julho comecou. Chamado no run_gemini_julho_daily.bat, logo antes de
analisar_gemini_julho.py (que e quem de fato consome a cota/faz as chamadas).

Mesmo topico de notificar_ntfy.py (que avisa o resumo no FINAL da execucao).
"""
import json
import urllib.request

TOPIC = "thiago-liga-gemini-o7h0wqmw5f"


def main():
    payload = json.dumps({
        "topic": TOPIC,
        "title": "Gemini Julho",
        "message": "Iniciando execucao de hoje (chamadas ao Gemini comecando agora)...",
    }).encode("utf-8")

    req = urllib.request.Request(
        "https://ntfy.sh/",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=15) as resp:
        resp.read()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[notificar_inicio_ntfy] falha ao enviar notificacao: {e}")
