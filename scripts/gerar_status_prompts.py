"""
Gera resultados/consolidado/STATUS_PROMPTS.md com o progresso de cada prompt
(quantas ligacoes/lotes ja rodaram vs quanto falta), lendo direto dos arquivos
de batch/lote em disco (nao depende do CSV consolidado estar atualizado).

Rodar sempre que quiser atualizar o acompanhamento:
    python scripts/gerar_status_prompts.py
"""
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
OUT_MD = ROOT / "resultados" / "consolidado" / "STATUS_PROMPTS.md"

MARCADORES_RUIM = ("[TRUNCADO", "[ERRO", "MAX_TOKENS")


def batch_num(nome, prefixo="batch"):
    m = re.match(rf"{prefixo}(\d+)[_.]", nome)
    return int(m.group(1)) if m else None


def contar_ligacoes_lote(path):
    return len(re.findall(r"=== LIGACAO \|", path.read_text(encoding="utf-8", errors="ignore")))


def status_gemini(pasta, fase, total_batches):
    """Escaneia resultados/<pasta>/batchNN_<fase>_*.txt, usa o maior arquivo por
    batch (reprocessamentos), e marca truncado/erro como pendente."""
    arquivos = sorted((ROOT / "resultados" / pasta).glob(f"batch*_{fase}_*.txt"),
                       key=lambda p: p.stat().st_size, reverse=True)
    vistos = {}
    for f in arquivos:
        n = batch_num(f.name)
        if n is None or n in vistos:
            continue
        vistos[n] = f

    ok, pendentes = [], []
    for n in range(1, total_batches + 1):
        f = vistos.get(n)
        if f is None:
            pendentes.append(n)
            continue
        conteudo = f.read_text(encoding="utf-8", errors="ignore")
        if any(m in conteudo for m in MARCADORES_RUIM) or f.stat().st_size < 100:
            pendentes.append(n)
        else:
            ok.append(n)
    return ok, pendentes


def status_lotes_fable(input_dir, output_dir, input_prefixo="lote", output_sufixo="_resultado.md"):
    """Escaneia lotes de exploracao Fable: um lote 'feito' precisa ter arquivo de
    saida correspondente ao de entrada."""
    inputs = {}
    for f in sorted(input_dir.glob(f"{input_prefixo}*.txt")):
        n = batch_num(f.name, prefixo=input_prefixo)
        if n is not None:
            inputs[n] = f

    ok, pendentes = [], []
    for n, f_in in sorted(inputs.items()):
        f_out = output_dir / f"{input_prefixo}{n:02d}{output_sufixo}"
        if f_out.exists():
            ok.append(n)
        else:
            pendentes.append(n)
    return inputs, ok, pendentes


def fmt_pct(feito, total):
    return f"{feito / total * 100:.1f}%" if total else "n/a"


def fmt_lista(nums):
    """Comprime em faixas (1, 2, 3, 5 -> '1-3, 5') pra nao estourar a linha da tabela
    quando ha dezenas/centenas de pendentes."""
    if not nums:
        return "-"
    nums = sorted(nums)
    faixas = []
    inicio = fim = nums[0]
    for n in nums[1:]:
        if n == fim + 1:
            fim = n
            continue
        faixas.append(str(inicio) if inicio == fim else f"{inicio}-{fim}")
        inicio = fim = n
    faixas.append(str(inicio) if inicio == fim else f"{inicio}-{fim}")
    return ", ".join(faixas)


linhas = []
agora = datetime.now().strftime("%Y-%m-%d %H:%M")
linhas.append("# Status dos prompts — acompanhamento\n")
linhas.append(f"_Gerado em {agora} por `scripts/gerar_status_prompts.py` — rode o script de novo para atualizar._\n")

# ---------------------------------------------------------------------------
# Gemini: base antiga (gemini_v2, 23 batches) + novo lote (gemini_novo_lote, 74 batches)
# ---------------------------------------------------------------------------
linhas.append("## Gemini — P1/P2, P5/P6, P9/P10\n")
linhas.append("| Base | Fase | Batches OK | Total | % | Pendentes |")
linhas.append("|---|---|---|---|---|---|")

bases_gemini = [
    ("Base antiga (1.275 ligações)", "gemini_v2", 23),
    ("Novo lote (5.348 ligações)", "gemini_novo_lote", 74),
]
resumo_gemini = {}
for label, pasta, total in bases_gemini:
    for fase in ["P1_P2", "P5_P6", "P9_P10"]:
        ok, pend = status_gemini(pasta, fase, total)
        resumo_gemini[(pasta, fase)] = (ok, pend, total)
        linhas.append(f"| {label} | {fase} | {len(ok)} | {total} | {fmt_pct(len(ok), total)} | {fmt_lista(pend)} |")

total_ok = sum(len(v[0]) for v in resumo_gemini.values())
total_geral = sum(v[2] for v in resumo_gemini.values())
linhas.append("")
linhas.append(f"**Total geral Gemini (6 combinações base×fase): {total_ok}/{total_geral} batches "
              f"({fmt_pct(total_ok, total_geral)})**\n")

# ---------------------------------------------------------------------------
# Fable: P3/P7 (track antigo, encerrado) + P4/P8/P11/P13/P14/P15 (novo_lote_363, em andamento)
# ---------------------------------------------------------------------------
linhas.append("## Fable — exploração qualitativa\n")

fable_dir = ROOT / "resultados" / "exploracao_fable"

inputs_antigo, ok_antigo, pend_antigo = status_lotes_fable(
    fable_dir / "inputs", fable_dir / "outputs", input_prefixo="batch"
)
inputs_completo, ok_completo, pend_completo = status_lotes_fable(
    fable_dir / "inputs_completo", fable_dir / "outputs_completo", input_prefixo="lote"
)
inputs_363, ok_363, pend_363 = status_lotes_fable(
    fable_dir / "inputs_novo_lote_363", fable_dir / "outputs_novo_lote_363", input_prefixo="lote"
)

lig_ok_completo = sum(contar_ligacoes_lote(inputs_completo[n]) for n in ok_completo)
lig_pend_completo = sum(contar_ligacoes_lote(inputs_completo[n]) for n in pend_completo)
lig_total_completo = lig_ok_completo + lig_pend_completo

lig_ok_363 = sum(contar_ligacoes_lote(inputs_363[n]) for n in ok_363)
lig_pend_363 = sum(contar_ligacoes_lote(inputs_363[n]) for n in pend_363)
lig_total_363 = lig_ok_363 + lig_pend_363

linhas.append("| Prompt(s) | Lotes OK | Total lotes | % lotes | Ligações OK | Ligações totais | Pendentes (lote) |")
linhas.append("|---|---|---|---|---|---|---|")
linhas.append(
    f"| P3/P7 — amostra antiga (`inputs`/`outputs`, encerrada) | {len(ok_antigo)} | {len(inputs_antigo)} | "
    f"{fmt_pct(len(ok_antigo), len(inputs_antigo))} | 456 | 456 | - (não retomar) |"
)
linhas.append(
    f"| P3/P7 — cobertura completa (`inputs_completo`, 100% da base) | {len(ok_completo)} | {len(inputs_completo)} | "
    f"{fmt_pct(len(ok_completo), len(inputs_completo))} | {lig_ok_completo} | {lig_total_completo} | "
    f"{fmt_lista(pend_completo)} |"
)
linhas.append(
    f"| P4/P8/P11/P13/P14/P15 (novo lote, `novo_lote_363`) | {len(ok_363)} | {len(inputs_363)} | "
    f"{fmt_pct(len(ok_363), len(inputs_363))} | {lig_ok_363} | {lig_total_363} | {fmt_lista(pend_363)} |"
)
linhas.append("")
linhas.append(
    "**P3/P7 cobertura completa:** prompt pronto para colar no Fable em "
    "`prompts/prompt_p3_p7_lote_completo.md`. Para cada lote pendente, colar o prompt + "
    "`resultados/exploracao_fable/inputs_completo/loteNNN.txt` no Fable e salvar a resposta em "
    "`resultados/exploracao_fable/outputs_completo/loteNNN_resultado.md`.\n"
)
linhas.append(
    "**Amostra antiga (12 lotes/456 ligações) e a cobertura completa não se sobrepõem por número de "
    "lote, mas cobrem as mesmas ligações** (a completa é superset, ordem fixa em vez de amostra "
    "aleatória) — a antiga fica só como registro histórico, não precisa reprocessar.\n"
)

OUT_MD.write_text("\n".join(linhas), encoding="utf-8")
print(f"Escrito em {OUT_MD}")
