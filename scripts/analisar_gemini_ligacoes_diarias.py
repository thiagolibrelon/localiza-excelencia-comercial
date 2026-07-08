"""
Etapa 2 do pipeline diario de ligacoes.

Le os JSONs gerados por gerar_ligacoes_diarias.py (dados_ligacoes_diarias/entrada/
ligacoes_YYYY-MM-DD.json) e roda a mesma analise via Gemini 2.5 Flash usada em
analisar_gemini_novo_lote.py (grupos de prompt P1_P2, P5_P6, P9_P10), mas:
  - Le/escreve por dia (um OUTPUT_DIR por data, nao um so fixo).
  - Processa o dia mais antigo que ainda nao esta completo primeiro (nao pula
    dias travados por causa de um dia novo ter chegado).
  - BATCH_SIZE bem maior (volume diario e ~300-500 ligacoes, nao os milhares
    do lote historico) - pode precisar de ajuste depois do primeiro dia real
    (acompanhe os logs de in=/out=tokens pra calibrar).

Rodar quando o usuario pedir (depois de ele subir um ligacoes_<data>.json novo):
  python scripts/analisar_gemini_ligacoes_diarias.py
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
BASE          = Path(__file__).parent.parent
ENTRADA_DIR   = BASE / "dados_ligacoes_diarias" / "entrada"
OUTPUT_BASE   = BASE / "resultados" / "gemini_ligacoes_diarias"
ENV_FILE      = BASE / ".env"

MODEL             = "gemini-2.5-flash"
BATCH_SIZE        = 300   # clientes por batch - volume diario cabe quase sempre em 1 batch
MAX_CALLS         = 20    # cota diaria do free tier
MAX_LIG_PER_CALL  = 350   # batches com mais ligacoes sao divididos em 2 chamadas
MAX_OUTPUT_TOKENS = 32768
MIN_OUTPUT_BYTES  = 4000  # abaixo disso = arquivo truncado, sera re-rodado
SLEEP_ENTRE_CHAMADAS = 65  # segundos - limite de tokens/min do free tier

GRUPOS_PRIORITY = ["P1_P2", "P5_P6", "P9_P10"]

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
quota_exhausted = False


def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def salvar(output_dir, nome, texto):
    output_dir.mkdir(parents=True, exist_ok=True)
    p = output_dir / nome
    p.write_text(texto, encoding="utf-8")
    log(f"  -> Salvo: {p.name} ({len(texto)} chars)")


def ja_existe(output_dir, b_idx, grupo):
    if not output_dir.exists():
        return None
    best = None
    for f in sorted(output_dir.glob(f"batch{b_idx:02d}_{grupo}_*.txt"), key=lambda x: x.stat().st_size, reverse=True):
        if f.stat().st_size < 200:
            continue
        content = f.read_text(encoding="utf-8")
        if "[TRUNCADO: MAX_TOKENS]" in content:
            log(f"  Arquivo {f.name} truncado — removendo para re-processar")
            f.unlink()
            continue
        if "[ERRO:" in content:
            continue
        if f.stat().st_size >= MIN_OUTPUT_BYTES:
            return f
        best = best or f
    if best:
        log(f"  Arquivo {best.name} pequeno ({best.stat().st_size} bytes) mas valido — assumindo completo")
    return best


def chamar_gemini(prompt, max_tokens=MAX_OUTPUT_TOKENS):
    global calls_made, quota_exhausted
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
            log(f"    finish={finish} | in={usage.prompt_token_count}tk | out={usage.candidates_token_count}tk | think={usage.thoughts_token_count}tk")
            if str(finish) in ("FinishReason.MAX_TOKENS", "MAX_TOKENS"):
                texto += "\n\n[TRUNCADO: MAX_TOKENS]"
            return texto
        except Exception as e:
            msg = str(e)
            if "GenerateRequestsPerDayPerProjectPerModel" in msg:
                log("  Cota diaria do free tier esgotada - encerrando execucao (sem retry, reseta ~4h BRT)")
                quota_exhausted = True
                return None
            wait = 60 * (tentativa + 1)
            log(f"  Erro (tentativa {tentativa+1}): {e} - aguardando {wait}s")
            time.sleep(wait)
    return "[ERRO: falha apos 4 tentativas]"


# ---------------------------------------------------------------------------
# Formatacao das ligacoes (schema novo: {cod: {carteira, distrital, cnae, ligacoes:[...]}})
# ---------------------------------------------------------------------------
def formatar_ligacoes(data_subset):
    linhas = []
    for cid, registro in data_subset.items():
        for call in registro.get("ligacoes", []):
            conv = "\n".join(f"{s}: {t}" for s, t in call.get("conversa", []))
            linhas.append(
                f"=== LIGACAO | Cliente:{cid} | "
                f"Data:{(call.get('data') or '?')[:10]} | "
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
# Prompts (identicos aos de analisar_gemini_novo_lote.py)
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


GRUPOS_FUNCS = {
    "P1_P2": prompt_p1_p2,
    "P5_P6": prompt_p5_p6,
    "P9_P10": prompt_p9_p10,
}


# ---------------------------------------------------------------------------
# Selecao do arquivo do dia a processar
# ---------------------------------------------------------------------------
def listar_entradas():
    arquivos = sorted(ENTRADA_DIR.glob("ligacoes_*.json"))
    return [(f.stem.replace("ligacoes_", ""), f) for f in arquivos]


def montar_batches(data):
    items = list(data.items())
    n = len(items)
    size = BATCH_SIZE
    n_bat = (n + size - 1) // size if n else 0
    batches = [dict(items[i:i + size]) for i in range(0, n, size)]
    return batches, n_bat


def dia_completo(output_dir, n_bat):
    for grupo in GRUPOS_PRIORITY:
        for b_idx in range(1, n_bat + 1):
            if ja_existe(output_dir, b_idx, grupo) is None:
                return False
    return True


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    global calls_made

    if not ENTRADA_DIR.exists():
        raise SystemExit(f"Pasta de entrada nao existe: {ENTRADA_DIR}")

    entradas = listar_entradas()
    if not entradas:
        log(f"Nenhum arquivo ligacoes_*.json em {ENTRADA_DIR}. Nada a fazer.")
        return

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    for data_str, caminho in entradas:
        with open(caminho, "r", encoding="utf-8") as f:
            data = json.load(f)

        batches, n_bat = montar_batches(data)
        output_dir = OUTPUT_BASE / data_str

        if n_bat == 0:
            log(f"{data_str}: arquivo vazio, pulando.")
            continue

        if dia_completo(output_dir, n_bat):
            log(f"{data_str}: ja esta completo (todos os grupos/batches presentes) — pulando.")
            continue

        n_lig_total = sum(len(v.get("ligacoes", [])) for v in data.values())
        log(f"{'='*60}")
        log(f"DIA {data_str} | {len(data)} clientes | {n_lig_total} ligacoes | {n_bat} batch(es)")
        log(f"{'='*60}")

        for grupo in GRUPOS_PRIORITY:
            fn = GRUPOS_FUNCS[grupo]
            log(f"-- Grupo {grupo} --")

            for b_idx, batch_data in enumerate(batches, 1):
                if calls_made >= MAX_CALLS:
                    log(f"Limite de {MAX_CALLS} chamadas atingido. Rode novamente amanha.")
                    return

                existente = ja_existe(output_dir, b_idx, grupo)
                if existente:
                    log(f"  Batch {b_idx:02d}/{n_bat} [{grupo}] - ja existe ({existente.stat().st_size} bytes)")
                    continue

                n_lig = sum(len(v.get("ligacoes", [])) for v in batch_data.values())
                if n_lig > MAX_LIG_PER_CALL:
                    log(f"  Batch {b_idx:02d}/{n_bat} [{grupo}] - {n_lig} ligacoes (grande) | chamadas {calls_made+1}-{calls_made+2}/{MAX_CALLS}")
                    items_list = list(batch_data.items())
                    mid = len(items_list) // 2
                    half1 = dict(items_list[:mid])
                    half2 = dict(items_list[mid:])
                    r1 = chamar_gemini(fn(formatar_ligacoes(half1)))
                    if quota_exhausted:
                        log("Rode novamente mais tarde/amanha.")
                        return
                    if calls_made >= MAX_CALLS:
                        log(f"Limite de {MAX_CALLS} chamadas atingido. Rode novamente amanha.")
                        return
                    log(f"    aguardando {SLEEP_ENTRE_CHAMADAS}s (limite de tokens/min do free tier)...")
                    time.sleep(SLEEP_ENTRE_CHAMADAS)
                    r2 = chamar_gemini(fn(formatar_ligacoes(half2)))
                    if quota_exhausted:
                        log("Rode novamente mais tarde/amanha.")
                        return
                    resultado = r1 + "\n\n" + r2
                else:
                    log(f"  Batch {b_idx:02d}/{n_bat} [{grupo}] - {n_lig} ligacoes | chamada {calls_made+1}/{MAX_CALLS}")
                    resultado = chamar_gemini(fn(formatar_ligacoes(batch_data)))
                    if quota_exhausted:
                        log("Rode novamente mais tarde/amanha.")
                        return

                nome_arquivo = f"batch{b_idx:02d}_{grupo}_{ts}.txt"
                salvar(output_dir, nome_arquivo, resultado)
                log(f"    aguardando {SLEEP_ENTRE_CHAMADAS}s (limite de tokens/min do free tier)...")
                time.sleep(SLEEP_ENTRE_CHAMADAS)

        log(f"{data_str}: concluido.")

    log("")
    log(f"Chamadas usadas nesta execucao: {calls_made}/{MAX_CALLS}")
    log("Pronto.")


if __name__ == "__main__":
    main()
