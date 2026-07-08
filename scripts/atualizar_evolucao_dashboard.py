"""
Le todos os dados_ligacoes_diarias/analisado/ligacoes_analisadas_<data>.json,
calcula os agregados por dia, e atualiza o bloco EVOLUCAO_DIARIA embutido em
apresentacao/dashboardv2.html (aba "Evolucao Diaria").

O dashboard e um arquivo HTML estatico (sem fetch/servidor), entao os dados
sao regravados diretamente no JS entre os marcadores:
  /* EVOLUCAO_DIARIA:START */
  const EVOLUCAO_DIARIA = [...];
  /* EVOLUCAO_DIARIA:END */

Rodar sempre que compilar_gemini_ligacoes_diarias.py gerar um novo dia:
  python scripts/atualizar_evolucao_dashboard.py
"""
import json
import re
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
ANALISADO_DIR = BASE / "dados_ligacoes_diarias" / "analisado"
DASHBOARD = BASE / "apresentacao" / "dashboardv2.html"

FECHOU = {"fechou_novo", "fechou_renovacao", "fechou_upsell"}

MARCADOR_INICIO = "/* EVOLUCAO_DIARIA:START */"
MARCADOR_FIM = "/* EVOLUCAO_DIARIA:END */"


def calcular_dia(linhas):
    total = len(linhas)
    n_fechou = sum(1 for r in linhas if r.get("desfecho") in FECHOU)
    n_challenger = sum(1 for r in linhas if r.get("teve_challenger") is True)

    scores = []
    for r in linhas:
        try:
            scores.append(int(r.get("score_comercial")))
        except (TypeError, ValueError):
            continue

    return {
        "data": None,  # preenchido pelo chamador
        "total_ligacoes": total,
        "taxa_fechamento_pct": round(100 * n_fechou / total, 2) if total else 0.0,
        "score_comercial_medio": round(sum(scores) / len(scores), 2) if scores else 0.0,
        "teve_challenger_pct": round(100 * n_challenger / total, 2) if total else 0.0,
    }


def coletar_evolucao():
    if not ANALISADO_DIR.exists():
        return []

    evolucao = []
    for arquivo in sorted(ANALISADO_DIR.glob("ligacoes_analisadas_*.json")):
        data_str = arquivo.stem.replace("ligacoes_analisadas_", "")
        with open(arquivo, encoding="utf-8") as f:
            linhas = json.load(f)
        if not linhas:
            continue
        dia = calcular_dia(linhas)
        dia["data"] = data_str
        evolucao.append(dia)

    evolucao.sort(key=lambda d: d["data"])
    return evolucao


def atualizar_dashboard(evolucao):
    html = DASHBOARD.read_text(encoding="utf-8")
    if MARCADOR_INICIO not in html or MARCADOR_FIM not in html:
        raise SystemExit(
            f"Marcadores {MARCADOR_INICIO!r}/{MARCADOR_FIM!r} nao encontrados em {DASHBOARD}. "
            "A aba 'Evolucao Diaria' precisa existir no HTML antes de rodar este script."
        )

    bloco_json = json.dumps(evolucao, ensure_ascii=False, separators=(",", ":"))
    novo_bloco = f"{MARCADOR_INICIO}\nconst EVOLUCAO_DIARIA = {bloco_json};\n{MARCADOR_FIM}"

    padrao = re.compile(
        re.escape(MARCADOR_INICIO) + r".*?" + re.escape(MARCADOR_FIM),
        re.DOTALL,
    )
    html_novo, n = padrao.subn(novo_bloco, html)
    if n != 1:
        raise SystemExit(f"Esperava substituir 1 bloco, substitui {n}. Abortando sem gravar.")

    DASHBOARD.write_text(html_novo, encoding="utf-8")


def main():
    evolucao = coletar_evolucao()
    atualizar_dashboard(evolucao)

    if not evolucao:
        print(f"Nenhum arquivo em {ANALISADO_DIR}. Bloco EVOLUCAO_DIARIA gravado vazio.")
        return

    print(f"{len(evolucao)} dia(s) processado(s):")
    for d in evolucao:
        print(f"  {d['data']}: {d['total_ligacoes']} ligacoes | "
              f"fechamento {d['taxa_fechamento_pct']}% | "
              f"score medio {d['score_comercial_medio']} | "
              f"challenger {d['teve_challenger_pct']}%")
    print(f"Dashboard atualizado: {DASHBOARD}")


if __name__ == "__main__":
    main()
