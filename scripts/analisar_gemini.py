"""
Analise de ligacoes Localiza via Gemini 2.5 Flash.

Configuracao:
  - 26 batches de ~50 ligacoes (cabem no limite de output do free tier)
  - 3 grupos de prompts prioritarios: P1_P2, P5_P6, P9_P10
  - Max 20 chamadas por execucao (cota diaria do free tier)
  - Skip automatico de arquivos ja completos (>4000 bytes)
  - Sintese final gerada apenas quando todos os batches estiverem prontos

Rotina:
  Qui: python analisar_gemini.py  -> P1_P2 batches 1-20
  Sex: python analisar_gemini.py  -> P1_P2 21-26 + P5_P6 1-14
  Sab: python analisar_gemini.py  -> P5_P6 15-26 + P9_P10 1-8
  Dom: python analisar_gemini.py  -> P9_P10 9-26 + sintese
"""
import json
import os
import time
from pathlib import Path
from datetime import datetime

from google import genai
from google.genai import types

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
FILE_PATH        = str(Path(__file__).parent.parent / "dados" / "LIG")
OUTPUT_DIR       = Path(__file__).parent.parent / "resultados" / "gemini_v2"
ENV_FILE         = Path(__file__).parent.parent / ".env"

MODEL            = "gemini-2.5-flash"
BATCH_SIZE       = 50    # ligacoes por batch — cabe no limite de output do free tier
MAX_CALLS        = 20    # cota diaria do free tier
MAX_LIG_PER_CALL = 60    # batches com mais ligacoes sao divididos em 2 chamadas
MIN_OUTPUT_BYTES = 4000  # abaixo disso = arquivo truncado, sera re-rodado

# Grupos de prompts prioritarios para a analise de fechamento
GRUPOS_PRIORITY  = ["P1_P2", "P5_P6", "P9_P10"]

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

calls_made = 0

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def salvar(nome, texto):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    p = OUTPUT_DIR / nome
    p.write_text(texto, encoding="utf-8")
    log(f"  -> Salvo: {p.name} ({len(texto)} chars)")

def ja_existe(b_idx, grupo):
    best = None
    for f in sorted(OUTPUT_DIR.glob(f"batch{b_idx:02d}_{grupo}_*.txt"), key=lambda x: x.stat().st_size, reverse=True):
        if f.stat().st_size < 200:
            continue
        content = f.read_text(encoding="utf-8")
        if "[TRUNCADO: MAX_TOKENS]" in content:
            log(f"  Arquivo {f.name} truncado — removendo para re-processar")
            f.unlink()
            continue
        if "[ERRO:" in content:
            continue
        # arquivo valido — prefere o maior; para batches grandes exige MIN_OUTPUT_BYTES
        if f.stat().st_size >= MIN_OUTPUT_BYTES:
            return f
        best = best or f  # guarda menor valido (ex: ultimo batch com poucos clientes)
    if best:
        log(f"  Arquivo {best.name} pequeno ({best.stat().st_size} bytes) mas valido — assumindo completo")
    return best

def chamar_gemini(prompt, max_tokens=8192):
    global calls_made
    for tentativa in range(4):
        try:
            resp = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.1,
                    thinking_config=types.ThinkingConfig(thinking_budget=0),
                ),
            )
            calls_made += 1
            texto = resp.text
            finish = resp.candidates[0].finish_reason if resp.candidates else "?"
            usage = resp.usage_metadata
            log(f"    finish={finish} | out={usage.candidates_token_count}tk | think={usage.thoughts_token_count}tk")
            if str(finish) in ("FinishReason.MAX_TOKENS", "MAX_TOKENS"):
                texto += "\n\n[TRUNCADO: MAX_TOKENS]"
            return texto
        except Exception as e:
            wait = 60 * (tentativa + 1)
            log(f"  Erro (tentativa {tentativa+1}): {e} - aguardando {wait}s")
            time.sleep(wait)
    return "[ERRO: falha apos 4 tentativas]"

# ---------------------------------------------------------------------------
# Formatacao das ligacoes
# ---------------------------------------------------------------------------
def formatar_ligacoes(data_subset):
    linhas = []
    for cid, calls in data_subset.items():
        for call in calls:
            conv = "\n".join(f"{s}: {t}" for s, t in call.get("conversa", []))
            linhas.append(
                f"=== LIGACAO | Cliente:{cid} | "
                f"Data:{call.get('data','?')[:10]} | "
                f"Dur:{call.get('duracao','?')}s | "
                f"Sent:{call.get('sentimento','?')} ===\n{conv}"
            )
    return "\n\n".join(linhas)

CONTEXTO = """
Empresa: Localiza (locacao de veiculos mensais para PJ)
Vendedor = "A" | Cliente = "C"
STT fragmentado - junte turns do mesmo speaker. <unk> = inaudivel, ignore.
"""

# ---------------------------------------------------------------------------
# Prompts
# ---------------------------------------------------------------------------
def prompt_p1_p2(trans):
    return f"""Voce e analista de comportamento comercial em locacao de veiculos corporativos.
{CONTEXTO}

Analise CADA ligacao abaixo e retorne CSV linha a linha. Nao pule nenhuma ligacao.

### CSV-P1 (Conversao)
cliente_id,data,duracao_s,desfecho,intencao_entrada,tentativa_comercial,B1,B2,B3,B4,B5,B6,B7,B8,B9,B10,score_comercial

desfecho: fechou_novo|fechou_renovacao|fechou_upsell|interessou_nao_fechou|nao_era_venda
intencao: cliente_queria|vendedor_puxou|misto|indefinido
B1-B10: SIM/NAO | pesos: B1=2,B2=1,B3=2,B4=2,B5=2,B6=3,B7=1,B8=1,B9=1,B10=3
score_comercial: soma dos pesos dos SIM (max 18)

B1=diagnostico antes do produto | B2=ancora de preco alto | B3=usou historico do cliente
B4=avisou risco ao cliente | B5=upsell conectado a dor | B6=urgencia com fato verificavel
B7=prometeu batalhar internamente | B8=ligou proativamente | B9=conhecimento pessoal
B10=perguntou sobre concorrente/frota propria

### CSV-P2 (Tipo de Ligacao)
cliente_id,data,tipo,subtipo,quem_iniciou,tentativa_comercial

tipo: nova_venda|renovacao|upsell|retencao|suporte_operacional|pos_venda_sinistro|pos_venda_manutencao|cobranca|onboarding|duvida_contrato|misto|sem_conteudo

IMPORTANTE: processe TODAS as {len(trans.split('=== LIGACAO'))-1} ligacoes. Retorne P1 completo, depois P2 completo. Sem explicacoes.

LIGACOES:
{trans}"""

def prompt_p5_p6(trans):
    return f"""Voce e especialista em Challenger Sale e coaching de vendas B2B.
{CONTEXTO}

Analise CADA ligacao e retorne CSV. Nao pule nenhuma ligacao.

### CSV-P5 (Comportamentos Challenger)
cliente_id,data,teve_challenger,codigos_challenger,frase_resumo,resultado_imediato,qualidade

CH1=Custo oculto revelado | CH2=ROI calculado | CH3=Urgencia por regra real
CH4=Concorrente superado com dado | CH5=Dor->produto conectado
CH6=Antecipacao de problema | CH7=Descoberta de necessidade nao declarada
resultado_imediato: cliente_aceitou|cliente_refletiu|sem_reacao_visivel
qualidade: alta|media|baixa
Se nao teve challenger: teve_challenger=NAO, demais campos=nenhum

### CSV-P6 (Oportunidades Perdidas)
cliente_id,data,oportunidades_perdidas,descricao_curta,valor_potencial_R$

OP1=Suporte sem pergunta comercial | OP2=Dor sem produto conectado | OP3=Fechamento sem urgencia
OP4=Referral nao solicitado | OP5=Dado estrategico nao explorado
OP6=Upsell obvio nao tentado | OP7=Churn nao detectado | OP8=Escalada desnecessaria
valor_potencial_R$: estimativa mensal (telemetria=50/v, protecao=80/v, anual=200, eletrico=3600/v)
Se nao ha oportunidade perdida: oportunidades_perdidas=nenhuma

IMPORTANTE: processe TODAS as {len(trans.split('=== LIGACAO'))-1} ligacoes. Retorne P5 completo, depois P6 completo. Sem explicacoes.

LIGACOES:
{trans}"""

def prompt_p9_p10(trans):
    return f"""Voce e especialista em comportamento comercial e Customer Success B2B.
{CONTEXTO}

Analise CADA ligacao e retorne CSV. Nao pule nenhuma ligacao.

### CSV-P9 (Abertura e Fechamento)
cliente_id,data,tipo_abertura,usou_nome,tipo_fechamento,proximo_passo_claro,prazo_definido,desfecho

AB1=Contextualizada | AB2=Relacional | AB3=Generica | AB4=Reativa | AB5=De protecao
FC1=Compromisso duplo(vendedor+cliente+prazo) | FC2=Proximo passo so do vendedor
FC3=Convite generico("se precisar me chama") | FC4=Aberto | FC5=Diretivo
proximo_passo_claro: SIM|NAO | prazo_definido: SIM|NAO

### CSV-P10 (Promessas)
promise_id,cliente_id,data,tipo_promessa,frase_resumo,prazo_prometido,risco_nao_cumprimento

promise_id: [cliente_id]-PM-[001,002...]
PM1=Resolve na ligacao | PM2=Envia documento | PM3=Liga de volta | PM4=Encaminha terceiro
PM5=Negocia internamente | PM6=Promessa implicita
risco: baixo|medio|alto|muito_alto
Se nao ha promessa na ligacao, nao inclua linha no P10.

IMPORTANTE: processe TODAS as {len(trans.split('=== LIGACAO'))-1} ligacoes. Retorne P9 completo, depois P10 completo. Sem explicacoes.

LIGACOES:
{trans}"""

B_DESC = {
    "B1": "diagnostico antes do produto",
    "B2": "ancora de preco alto",
    "B3": "usou historico do cliente",
    "B4": "avisou risco ao cliente",
    "B5": "upsell conectado a dor",
    "B6": "urgencia com fato verificavel",
    "B7": "prometeu batalhar internamente",
    "B8": "ligou proativamente",
    "B9": "conhecimento pessoal",
    "B10": "perguntou sobre concorrente/frota",
}

def agregar_p1_p2(output_files):
    """Agrega CSVs de P1_P2 em stats compactas (sem chamada de API)."""
    from collections import defaultdict
    desfechos = defaultdict(int)
    b_por_desfecho = defaultdict(lambda: defaultdict(int))
    total = 0

    for f in output_files:
        content = f.read_text(encoding="utf-8")
        in_p1 = False
        for line in content.splitlines():
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
            try:
                # normaliza linhas com 16 campos (sem tentativa_comercial)
                if len(parts) == 16:
                    parts.insert(5, "desconhecido")
                desfecho = parts[3].strip()
                desfechos[desfecho] += 1
                total += 1
                for i in range(10):
                    if parts[6 + i].strip().upper() == "SIM":
                        b_por_desfecho[f"B{i+1}"][desfecho] += 1
            except Exception:
                pass

    fechou = sum(desfechos.get(d, 0) for d in ["fechou_novo", "fechou_renovacao", "fechou_upsell"])
    int_nao = desfechos.get("interessou_nao_fechou", 0)
    nao_venda = desfechos.get("nao_era_venda", 0)

    linhas = [f"## DADOS P1_P2 — {total} ligacoes processadas (todos os batches)"]
    linhas.append(f"\n### Distribuicao de desfechos")
    linhas.append(f"- Fechou (novo+renovacao+upsell): {fechou} ({100*fechou/total:.1f}%)" if total else "- sem dados")
    linhas.append(f"- Interessou, nao fechou: {int_nao} ({100*int_nao/total:.1f}%)" if total else "")
    linhas.append(f"- Nao era venda (suporte/ops): {nao_venda} ({100*nao_venda/total:.1f}%)" if total else "")
    for d, n in desfechos.items():
        if d not in ("fechou_novo","fechou_renovacao","fechou_upsell","interessou_nao_fechou","nao_era_venda"):
            linhas.append(f"- {d}: {n}")

    linhas.append(f"\n### Comportamentos B1-B10 — freq em fechou vs interessou_nao_fechou")
    linhas.append("| Comp | Descricao | Freq fechou | Freq int_nao_fechou | Delta |")
    linhas.append("|---|---|---|---|---|")
    for b in [f"B{i}" for i in range(1, 11)]:
        fc = sum(b_por_desfecho[b].get(d, 0) for d in ["fechou_novo","fechou_renovacao","fechou_upsell"])
        nf = b_por_desfecho[b].get("interessou_nao_fechou", 0)
        fp = 100*fc/fechou if fechou else 0
        np_ = 100*nf/int_nao if int_nao else 0
        linhas.append(f"| {b} | {B_DESC.get(b,'')} | {fp:.1f}% ({fc}/{fechou}) | {np_:.1f}% ({nf}/{int_nao}) | {fp-np_:+.1f}pp |")

    return "\n".join(linhas)


_AB_VALIDOS = {"AB1","AB2","AB3","AB4","AB5"}
_FC_VALIDOS = {"FC1","FC2","FC3","FC4","FC5"}
_PM_VALIDOS = {"PM1","PM2","PM3","PM4","PM5","PM6"}
_SN_VALIDOS = {"SIM","NAO"}

def agregar_p9_p10(output_files):
    """Agrega CSVs de P9_P10 em distribuicoes compactas (sem chamada de API)."""
    import re
    from collections import defaultdict
    ab = defaultdict(int)
    fc = defaultdict(int)
    pm = defaultdict(int)
    prazo = defaultdict(int)
    nome = defaultdict(int)
    total_lig = 0
    total_pm = 0

    for f in output_files:
        content = f.read_text(encoding="utf-8")
        in_p9 = in_p10 = False
        for line in content.splitlines():
            s = line.strip()
            if s.startswith("cliente_id,data,tipo_abertura"):
                in_p9, in_p10 = True, False
                continue
            if s.startswith("promise_id,"):
                in_p9, in_p10 = False, True
                continue
            if s.startswith("```") or s.startswith("==="):
                in_p9 = in_p10 = False
                continue
            if in_p9 and s and not s.startswith("#"):
                parts = s.split(",")
                if len(parts) >= 7:
                    try:
                        ab_v  = parts[2].strip().upper()
                        nom_v = parts[3].strip().upper()
                        fc_v  = parts[4].strip().upper()
                        prz_v = parts[6].strip().upper()
                        if ab_v in _AB_VALIDOS and fc_v in _FC_VALIDOS:
                            ab[ab_v] += 1
                            fc[fc_v] += 1
                            if nom_v in _SN_VALIDOS:
                                nome[nom_v] += 1
                            if prz_v in _SN_VALIDOS:
                                prazo[prz_v] += 1
                            total_lig += 1
                    except Exception:
                        pass
            if in_p10 and s and not s.startswith("#"):
                parts = s.split(",")
                if len(parts) >= 4:
                    try:
                        pm_v = parts[3].strip().upper()
                        if pm_v in _PM_VALIDOS:
                            pm[pm_v] += 1
                            total_pm += 1
                    except Exception:
                        pass

    linhas = [f"## DADOS P9_P10 — {total_lig} ligacoes | {total_pm} promessas com codigo PM (todos os batches)"]

    linhas.append("\n### Tipo de Abertura (AB1-AB5)")
    for k in sorted(ab):
        linhas.append(f"- {k}: {ab[k]} ({100*ab[k]/total_lig:.1f}%)" if total_lig else f"- {k}: {ab[k]}")

    linhas.append("\n### Tipo de Fechamento (FC1-FC5)")
    for k in sorted(fc):
        linhas.append(f"- {k}: {fc[k]} ({100*fc[k]/total_lig:.1f}%)" if total_lig else f"- {k}: {fc[k]}")

    linhas.append(f"\n### Prazo definido: SIM={prazo.get('SIM',0)} ({100*prazo.get('SIM',0)/total_lig:.1f}%) | NAO={prazo.get('NAO',0)}" if total_lig else "")
    linhas.append(f"### Usou nome do cliente: SIM={nome.get('SIM',0)} ({100*nome.get('SIM',0)/total_lig:.1f}%)" if total_lig else "")

    linhas.append("\n### Tipos de Promessa (PM1-PM6) — apenas registros com codigo estruturado")
    for k in sorted(pm):
        linhas.append(f"- {k}: {pm[k]} ({100*pm[k]/total_pm:.1f}%)" if total_pm else f"- {k}: {pm[k]}")

    return "\n".join(linhas)


def agregar_p5_p6(output_files):
    """Agrega CSVs de P5_P6 em stats compactas (sem chamada de API)."""
    from collections import defaultdict
    ch_sim = 0
    ch_nao = 0
    ch_codigos = defaultdict(int)
    ch_qualidade = defaultdict(int)
    ch_resultado = defaultdict(int)
    ch_exemplos = []

    op_tipos = defaultdict(int)
    op_valor = defaultdict(float)
    total_p6 = 0

    for f in output_files:
        content = f.read_text(encoding="utf-8")
        in_p5 = in_p6 = False
        for line in content.splitlines():
            s = line.strip()
            if s.startswith("cliente_id,data,teve_challenger"):
                in_p5, in_p6 = True, False
                continue
            if s.startswith("cliente_id,data,oportunidades_perdidas"):
                in_p5, in_p6 = False, True
                continue
            if s.startswith("```") or s.startswith("###"):
                in_p5 = in_p6 = False
                continue

            if in_p5 and s and not s.startswith("#"):
                parts = s.split(",")
                if len(parts) >= 4:
                    try:
                        teve = parts[2].strip().upper()
                        if teve == "SIM":
                            ch_sim += 1
                            for cod in parts[3].strip().replace("|", ";").split(";"):
                                cod = cod.strip()
                                if cod and cod != "nenhum" and cod.startswith("CH"):
                                    ch_codigos[cod] += 1
                            resultado_v = parts[5].strip() if len(parts) >= 6 else ""
                            if resultado_v in ("cliente_aceitou", "cliente_refletiu", "sem_reacao_visivel"):
                                ch_resultado[resultado_v] += 1
                            qual_v = parts[6].strip() if len(parts) >= 7 else ""
                            if qual_v in ("alta", "media", "baixa"):
                                ch_qualidade[qual_v] += 1
                            if len(ch_exemplos) < 5 and len(parts) >= 5 and parts[4].strip() not in ("nenhum", ""):
                                ch_exemplos.append(parts[4].strip()[:120])
                        elif teve == "NAO":
                            ch_nao += 1
                    except Exception:
                        pass

            if in_p6 and s and not s.startswith("#"):
                parts = s.split(",", 4)
                if len(parts) >= 3:
                    try:
                        op = parts[2].strip()
                        if op and op != "nenhuma":
                            op_tipos[op] += 1
                            if len(parts) >= 5:
                                v = parts[4].strip()
                                if v not in ("nenhum", "", "0"):
                                    try:
                                        op_valor[op] += float(v)
                                    except ValueError:
                                        pass
                        total_p6 += 1
                    except Exception:
                        pass

    total_ch = ch_sim + ch_nao
    linhas = [f"## DADOS P5_P6 — {total_ch} ligacoes com Challenger | {total_p6} oportunidades avaliadas (todos os batches)"]

    linhas.append(f"\n### Challenger Sale (P5)")
    linhas.append(f"- Ligacoes COM Challenger: {ch_sim} ({100*ch_sim/total_ch:.1f}%)" if total_ch else "- sem dados")
    linhas.append(f"- Ligacoes SEM Challenger: {ch_nao} ({100*ch_nao/total_ch:.1f}%)" if total_ch else "")
    linhas.append(f"- Codigos mais frequentes (CH1-CH7):")
    for k in sorted(ch_codigos, key=lambda x: ch_codigos[x], reverse=True):
        linhas.append(f"  - {k}: {ch_codigos[k]}")
    linhas.append(f"- Qualidade: {dict(ch_qualidade)}")
    linhas.append(f"- Resultado imediato: {dict(ch_resultado)}")
    if ch_exemplos:
        linhas.append(f"- Exemplos de frases Challenger: " + " | ".join(ch_exemplos[:3]))

    total_ops = sum(op_tipos.values())
    linhas.append(f"\n### Oportunidades Perdidas (P6) — {total_ops} oportunidades identificadas em {total_p6} ligacoes")
    for k in sorted(op_tipos, key=lambda x: op_tipos[x], reverse=True):
        pct = 100*op_tipos[k]/total_ops if total_ops else 0
        val = op_valor.get(k, 0)
        linhas.append(f"- {k}: {op_tipos[k]} ({pct:.1f}%) | valor estimado R${val:.0f}/mes na amostra")
    total_val = sum(op_valor.values())
    escala = total_p6 / len(output_files) if output_files else 1
    linhas.append(f"\n- Valor total identificado na amostra: R${total_val:.0f}/mes")
    if total_ch > 0:
        razao = total_p6 / total_ch
        linhas.append(f"- Media de {razao:.1f} oportunidade/ligacao na amostra")

    return "\n".join(linhas)


def sintese_existe():
    for f in sorted(OUTPUT_DIR.glob("SINTESE_FINAL_*.txt"), key=lambda x: x.stat().st_size, reverse=True):
        content = f.read_text(encoding="utf-8")
        if "[TRUNCADO: MAX_TOKENS]" in content:
            log(f"  Sintese {f.name} truncada — removendo para re-processar")
            f.unlink()
            continue
        if f.stat().st_size > 2000:
            log(f"  Sintese valida encontrada: {f.name} ({f.stat().st_size} bytes)")
            return f
    return None


def prompt_sintese_final(stats_p1p2, stats_p9p10, stats_p5p6, n_ligacoes, n_batches):
    return f"""Voce e analista senior de performance comercial da Localiza.

Analise de {n_ligacoes} ligacoes B2B (1.109 clientes, {n_batches} batches).
Pergunta central: O que o vendedor faz para fechar um contrato?

INSTRUCAO CRITICA: Use APENAS os numeros ja calculados abaixo. NAO some, NAO liste valores individuais, NAO recalcule nada. Escreva diretamente a analise usando os totais prontos.

## DADOS QUANTITATIVOS (todos os {n_batches} batches, pre-calculados)

{stats_p1p2}

{stats_p9p10}

{stats_p5p6}

---

Agora escreva a sintese completa nas 5 secoes abaixo, usando APENAS os numeros acima:

### 1. RANKING DE COMPORTAMENTOS (B1-B10)
Tabela: comportamento | freq_fechou | freq_int_nao_fechou | delta | interpretacao em 1 linha

### 2. TOP 10 HIPOTESES
HIPOTESE: [afirmacao direta]
EVIDENCIA: [cite os numeros exatos dos dados acima]
CONFIANCA: alta|media|baixa

### 3. PADROES DE ABERTURA E FECHAMENTO
AB1-AB5: qual domina e o que isso significa. FC1 vs FC3: diferenca de resultado. Prazo_definido: impacto.

### 4. OPORTUNIDADES PERDIDAS
Use os totais ja calculados do P5_P6. Extrapole para 1.275 ligacoes com multiplicador simples. Top 3 tipos de OP com impacto em R$.

### 5. TOP 5 ACOES PARA OS PROXIMOS 30 DIAS
Especificas, com metrica de sucesso. Ordene por impacto em receita.

Use numeros reais dos dados. Seja conciso e direto."""

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    global calls_made

    log("Carregando LIG...")
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    items  = list(data.items())
    n      = len(items)
    size   = BATCH_SIZE
    n_bat  = (n + size - 1) // size
    batches = [dict(items[i:i+size]) for i in range(0, n, size)]

    log(f"Total: {n} clientes | {n_bat} batches de ~{size} ligacoes")
    log(f"Grupos priority: {GRUPOS_PRIORITY}")
    log(f"Chamadas max hoje: {MAX_CALLS}")
    log(f"Output dir: {OUTPUT_DIR}")
    log("")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    todos_prontos = True

    grupos_funcs = {
        "P1_P2": prompt_p1_p2,
        "P5_P6": prompt_p5_p6,
        "P9_P10": prompt_p9_p10,
    }

    for grupo in GRUPOS_PRIORITY:
        fn = grupos_funcs[grupo]
        log(f"{'='*60}")
        log(f"GRUPO {grupo}")
        log(f"{'='*60}")

        for b_idx, batch_data in enumerate(batches, 1):
            if calls_made >= MAX_CALLS:
                log(f"Limite de {MAX_CALLS} chamadas atingido. Rode novamente amanha.")
                todos_prontos = False
                return

            existente = ja_existe(b_idx, grupo)
            if existente:
                log(f"  Batch {b_idx:02d}/{n_bat} [{grupo}] - ja existe ({existente.stat().st_size} bytes)")
                continue

            n_lig = sum(len(v) for v in batch_data.values())
            if n_lig > MAX_LIG_PER_CALL:
                log(f"  Batch {b_idx:02d}/{n_bat} [{grupo}] - {n_lig} ligacoes (grande) | chamadas {calls_made+1}-{calls_made+2}/{MAX_CALLS}")
                items_list = list(batch_data.items())
                mid = len(items_list) // 2
                half1 = dict(items_list[:mid])
                half2 = dict(items_list[mid:])
                r1 = chamar_gemini(fn(formatar_ligacoes(half1)), max_tokens=8192)
                if calls_made >= MAX_CALLS:
                    log(f"Limite de {MAX_CALLS} chamadas atingido. Rode novamente amanha.")
                    todos_prontos = False
                    return
                r2 = chamar_gemini(fn(formatar_ligacoes(half2)), max_tokens=8192)
                resultado = r1 + "\n\n" + r2
            else:
                log(f"  Batch {b_idx:02d}/{n_bat} [{grupo}] - {n_lig} ligacoes | chamada {calls_made+1}/{MAX_CALLS}")
                resultado = chamar_gemini(fn(formatar_ligacoes(batch_data)), max_tokens=8192)

            nome_arquivo = f"batch{b_idx:02d}_{grupo}_{ts}.txt"
            salvar(nome_arquivo, resultado)
            time.sleep(5)

    # Sintese final — so roda quando todos os batches de todos os grupos estiverem prontos
    if todos_prontos:
        existente = sintese_existe()
        if existente:
            log(f"Sintese ja existe e e valida — pulando.")
        elif calls_made >= MAX_CALLS:
            log("Limite de chamadas atingido — sintese sera gerada na proxima execucao.")
        else:
            log("")
            log("Todos os batches completos. Gerando sintese final (prompt compacto)...")
            p1p2_files  = sorted(OUTPUT_DIR.glob("batch*_P1_P2_*.txt"))
            p9p10_files = sorted(OUTPUT_DIR.glob("batch*_P9_P10_*.txt"))
            p5p6_files  = sorted(OUTPUT_DIR.glob("batch*_P5_P6_*.txt"))

            stats_p1p2  = agregar_p1_p2(p1p2_files)
            stats_p9p10 = agregar_p9_p10(p9p10_files)
            stats_p5p6  = agregar_p5_p6(p5p6_files)

            n_total = sum(len(v) for v in data.values())
            sintese = chamar_gemini(
                prompt_sintese_final(stats_p1p2, stats_p9p10, stats_p5p6, n_total, n_bat),
                max_tokens=8192,
            )
            salvar(f"SINTESE_FINAL_{ts}.txt", sintese)

    log("")
    log(f"Chamadas usadas hoje: {calls_made}/{MAX_CALLS}")
    log("Pronto.")

if __name__ == "__main__":
    main()
