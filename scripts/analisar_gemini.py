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
    for f in OUTPUT_DIR.glob(f"batch{b_idx:02d}_{grupo}_*.txt"):
        if f.stat().st_size >= MIN_OUTPUT_BYTES:
            content = f.read_text(encoding="utf-8")
            if "[TRUNCADO: MAX_TOKENS]" in content:
                log(f"  Arquivo {f.name} truncado — removendo para re-processar")
                f.unlink()
                return None
            return f
    return None

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

def prompt_sintese_final(todos_outputs, n_ligacoes, n_batches):
    return f"""Voce e analista senior de performance comercial da Localiza.

Analise completa de {n_ligacoes} ligacoes reais de vendas B2B em {n_batches} batches.
Dados: P1 (conversao + scores B1-B10), P5 (Challenger), P6 (oportunidades perdidas), P9 (abertura/fechamento), P10 (promessas).

{todos_outputs}

## HIPOTESES SOBRE "O QUE O VENDEDOR FAZ PARA FECHAR UM CONTRATO"

### 1. RANKING DE COMPORTAMENTOS (B1-B10) POR CORRELACAO COM FECHAMENTO
Para cada comportamento, calcule:
- frequencia em ligacoes com desfecho positivo (fechou_novo|fechou_renovacao|fechou_upsell)
- frequencia em ligacoes sem fechamento
- forca da correlacao
Formato tabela: comportamento | descricao | freq_fechou | freq_nao_fechou | correlacao

### 2. TOP 10 HIPOTESES (rankeadas por forca de evidencia)
Para cada hipotese:
HIPOTESE: [afirmacao direta]
EVIDENCIA: [n ligacoes/vendedores]
EXEMPLO: [frase real das transcricoes]
CONFIANCA: alta|media|baixa

### 3. PADROES DE ABERTURA E FECHAMENTO
- Qual tipo de abertura (AB1-AB5) correlaciona com fechamento?
- Qual tipo de fechamento (FC1-FC5) e mais comum nos vendedores top?
- FC3 ("qualquer coisa me chama") vs FC1 (compromisso duplo): diferenca nos resultados?

### 4. OPORTUNIDADES PERDIDAS EM R$ (total estimado)
- Total de receita mensal nao capturada
- Top 3 tipos de oportunidade perdida (OP1-OP8)
- Estimativa de impacto anual

### 5. TOP 5 ACOES PARA OS PROXIMOS 30 DIAS
Ordenadas por impacto estimado em receita. Especificas, acionaveis.

Use numeros reais dos dados. Seja direto e objetivo."""

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
    todos_outputs = []
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
                resultado = existente.read_text(encoding="utf-8")
                todos_outputs.append(f"=== BATCH {b_idx:02d} - {grupo} ===\n{resultado}")
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
            todos_outputs.append(f"=== BATCH {b_idx:02d} - {grupo} ===\n{resultado}")
            time.sleep(5)

    # Sintese final — so roda quando todos os batches de todos os grupos estiverem prontos
    if todos_prontos:
        log("")
        log("Todos os batches completos. Gerando sintese final...")
        n_total = sum(len(v) for v in data.values())
        sintese = chamar_gemini(
            prompt_sintese_final("\n\n".join(todos_outputs), n_total, n_bat),
            max_tokens=8192,
        )
        salvar(f"SINTESE_FINAL_{ts}.txt", sintese)

    log("")
    log(f"Chamadas usadas hoje: {calls_made}/{MAX_CALLS}")
    log("Pronto.")

if __name__ == "__main__":
    main()
