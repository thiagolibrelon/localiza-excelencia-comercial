"""
Análise completa das ligações Localiza — Prompts 13, 14 e 15.
Roda em batches via API do Claude e salva resultados em /resultados_analise/
"""
import json
import os
import re
import time
import sys
from pathlib import Path
from datetime import datetime

import anthropic

# ---------------------------------------------------------------------------
# Carrega .env local se existir (ANTHROPIC_API_KEY=sk-ant-...)
# ---------------------------------------------------------------------------
_env_file = Path(__file__).parent.parent / ".env"
if _env_file.exists():
    for _line in _env_file.read_text(encoding="utf-8").splitlines():
        _line = _line.strip()
        if _line and not _line.startswith("#") and "=" in _line:
            _k, _v = _line.split("=", 1)
            os.environ.setdefault(_k.strip(), _v.strip())

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
FILE_PATH = str(Path(__file__).parent.parent / "dados" / "LIG")
OUTPUT_DIR = str(Path(__file__).parent.parent / "resultados")
INTERMEDIATE_DIR = str(Path(__file__).parent.parent / "resultados" / "intermediarios")

HAIKU  = "claude-haiku-4-5-20251001"
SONNET = "claude-sonnet-4-6"

BATCH_CALLS     = 25   # ligações por batch (P13 / P15)
BATCH_CLIENTS   = 10   # clientes por batch (P15)
MIN_SELLER_CALLS = 5   # mínimo de ligações para incluir vendedor no P14

# ---------------------------------------------------------------------------
# Nomes brasileiros comuns — ajuda a filtrar falsos positivos no regex
# ---------------------------------------------------------------------------
NOMES_BR = {
    "Ana","Bruna","Camila","Carla","Cristiane","Eliane","Eli","Flavia","Flavio",
    "Gabriela","Gabriel","Geraldo","Guilherme","Isadora","Isaias","Juliana",
    "Liliane","Lilian","Lucas","Luma","Marcos","Matheus","Paulo","Pedro","Ramiro",
    "Rodrigo","Rosana","Sheila","Stephanie","Talita","Tamires","Tatiana","Tawana",
    "Tauana","Thais","Thalita","Vitor","Bruno","Everton","Fabio","Felipe",
    "Francisco","Lenia","Lumia","Duna","Tais","Elton","Cristiano","Sandra",
    "Renata","Patricia","Fernanda","Eduardo","Ricardo","Daniel","Marcelo",
}

# ---------------------------------------------------------------------------
# Utilitários
# ---------------------------------------------------------------------------
def log(msg: str):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def salvar(path: Path, texto: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(texto, encoding="utf-8")
    log(f"Salvo → {path.name}")

def carregar_intermediario(path: Path) -> str | None:
    if path.exists():
        log(f"Reaproveitando intermediário: {path.name}")
        return path.read_text(encoding="utf-8")
    return None

def extract_seller(call: dict) -> str:
    """Tenta extrair o nome do vendedor (A) na conversa."""
    patterns = [
        r"aqui [eé] (?:o |a )?([A-Za-záéíóúâêîôûãõàèìòùÁÉÍÓÚÂÊÎÔÛÃÕ]{3,})",
        r"meu nome [eé] ([A-Za-záéíóúâêîôûãõàèìòùÁÉÍÓÚÂÊÎÔÛÃÕ]{3,})",
        r"(?:^|\s)(?:sou|chamo)[- ](?:o |a )?([A-Za-záéíóúâêîôûãõàèìòùÁÉÍÓÚÂÊÎÔÛÃÕ]{3,})",
        r"(?:fala |falo )([A-Za-záéíóúâêîôûãõàèìòùÁÉÍÓÚÂÊÎÔÛÃÕ]{3,})",
    ]
    for speaker, text in call.get("conversa", [])[:6]:
        if speaker != "A":
            continue
        for pat in patterns:
            m = re.search(pat, text, re.I)
            if m:
                nome = m.group(1).strip().capitalize()
                if nome in NOMES_BR or (nome[0].isupper() and len(nome) >= 4):
                    stopwords = {"executivo","executiva","responsavel","nova","novo",
                                 "gerente","gestora","gestor","consultora","consultor",
                                 "localiza","locar","empresa","conta","aqui","bom",
                                 "boa","prezado","prezada"}
                    if nome.lower() not in stopwords:
                        return nome
    return "Nao_Identificado"

def format_call(client_id: str, call: dict) -> str:
    conversa = "\n".join(f"{s}: {t}" for s, t in call.get("conversa", []))
    return (
        f"--- LIGAÇÃO | Cliente:{client_id} | "
        f"Data:{call.get('data','?')[:10]} | "
        f"Duração:{call.get('duracao','?')}s | "
        f"Sentimento:{call.get('sentimento','?')} ---\n"
        f"{conversa}"
    )

# ---------------------------------------------------------------------------
# API
# ---------------------------------------------------------------------------
client_api: anthropic.Anthropic | None = None

def api_call(prompt: str, model: str = HAIKU, max_tokens: int = 4096) -> str:
    global client_api
    if client_api is None:
        client_api = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    for attempt in range(4):
        try:
            resp = client_api.messages.create(
                model=model,
                max_tokens=max_tokens,
                messages=[{"role": "user", "content": prompt}],
            )
            return resp.content[0].text
        except anthropic.RateLimitError:
            wait = 30 * (attempt + 1)
            log(f"  Rate limit — aguardando {wait}s...")
            time.sleep(wait)
        except Exception as e:
            log(f"  Erro API (tentativa {attempt+1}): {e}")
            if attempt < 3:
                time.sleep(10 * (attempt + 1))
    return "[ERRO: falha na API após 4 tentativas]"

# ---------------------------------------------------------------------------
# PROMPT 13 — Surpresas e Padrões Emergentes
# ---------------------------------------------------------------------------
PROMPT13_BATCH = """Você é um pesquisador de comportamento comercial B2B.
Empresa: Localiza (locação mensal PJ) | Vendedor=A | Cliente=C

Analise as transcrições abaixo e identifique padrões que NÃO são óbvios:

S1 — Comportamentos inesperados dos vendedores
S2 — Comportamentos/padrões dos clientes
S3 — Assuntos recorrentes sem categoria clara
S4 — Sinais fracos (churn, expansão, mudança societária, competidor)

TRANSCRIÇÕES:
{transcricoes}

Retorne APENAS CSV (sem explicação, sem markdown):
categoria,codigo,descricao,frequencia_estimada,impacto_potencial,evidencias

impacto_potencial = alto/medio/baixo
Máximo 15 linhas. Pule linhas sem relevância real."""

PROMPT13_SINTESE = """Você é um pesquisador sênior de comportamento comercial B2B (Localiza).

Abaixo estão achados de {n_batches} lotes de análise de {n_calls} ligações:

{achados}

TAREFA: Síntese final consolidada.

1. Tabela CSV consolidada (sem duplicatas, frequências somadas, ordenado por impacto):
categoria,codigo,descricao,frequencia_total,impacto_potencial,evidencias

2. Perguntas de síntese:
Q1 - Qual foi a descoberta mais surpreendente desta base?
Q2 - Que comportamento relevante NÃO é medido por nenhum prompt atual?
Q3 - Se pudesse criar apenas UM novo prompt, qual seria? (escreva o prompt completo)
Q4 - Quais padrões têm maior potencial de impactar RECEITA?
Q5 - Quais padrões têm maior potencial de impactar RETENÇÃO?"""

def run_prompt13(all_calls_fmt: list[str], n_calls: int) -> str:
    log("=== PROMPT 13: Padrões Emergentes ===")
    batches = [all_calls_fmt[i:i+BATCH_CALLS] for i in range(0, len(all_calls_fmt), BATCH_CALLS)]
    log(f"  {len(batches)} batches de até {BATCH_CALLS} ligações")

    resultados = []
    for i, batch in enumerate(batches, 1):
        inter_path = Path(INTERMEDIATE_DIR) / f"p13_batch_{i:03d}.txt"
        cached = carregar_intermediario(inter_path)
        if cached:
            resultados.append(cached)
            continue
        log(f"  Batch {i}/{len(batches)}...")
        prompt = PROMPT13_BATCH.format(transcricoes="\n\n".join(batch))
        resultado = api_call(prompt)
        salvar(inter_path, resultado)
        resultados.append(resultado)
        time.sleep(1.5)

    log("  Sintetizando P13...")
    sintese_prompt = PROMPT13_SINTESE.format(
        n_batches=len(batches),
        n_calls=n_calls,
        achados="\n\n--- LOTE ---\n".join(resultados),
    )
    return api_call(sintese_prompt, model=SONNET, max_tokens=6000)

# ---------------------------------------------------------------------------
# PROMPT 14 — Diferenças entre Vendedores
# ---------------------------------------------------------------------------
PROMPT14_VENDEDOR = """Você é um analista de performance comercial (Localiza).

Analise as ligações do vendedor "{vendedor}" ({n_lig} ligações disponíveis, mostrando {n_amostra}).

Extraia o perfil comportamental em:
D1 — Estrutura da conversa (abertura, corpo, encerramento, duração média)
D2 — Linguagem (vocabulário recorrente, tom, objetividade)
D3 — Relacionamento (uso do nome do cliente, referências a histórico, rapport)
D4 — Comportamento comercial (oferta, investigação de necessidade, exploração)
D5 — Gestão de objeções (resposta, exploração antes de responder)

Métricas adicionais:
- Taxa de sentimento positivo nas ligações analisadas
- Duração média (segundos)
- Comportamento mais marcante (1 frase)

LIGAÇÕES:
{ligacoes}

Seja objetivo. Use bullet points por dimensão."""

PROMPT14_COMPARACAO = """Você é um analista de performance comercial sênior (Localiza).

Abaixo estão os perfis comportamentais de {n_vendedores} vendedores:

{perfis}

TAREFA: Análise comparativa completa.

1. Tabela CSV comparativa:
tema,comportamento_observado,top_performers,vendedores_medianos,diferenca_chave,impacto_estimado

2. Análise narrativa:
- O que os melhores vendedores fazem que os demais raramente fazem?
- O que os vendedores medianos fazem em excesso ou de forma errada?
- Existe algum comportamento EXCLUSIVO dos top performers?
- Se o time todo copiasse apenas 3 comportamentos dos melhores, quais seriam?
- Qual vendedor deveria ser o benchmark para treinamento? Por quê?
- Ranking de vendedores por performance estimada (do melhor ao mais fraco) com justificativa."""

def run_prompt14(calls_by_seller: dict[str, list[str]]) -> str:
    log("=== PROMPT 14: Diferenças entre Vendedores ===")
    vendedores_validos = {
        v: calls for v, calls in calls_by_seller.items()
        if v != "Nao_Identificado" and len(calls) >= MIN_SELLER_CALLS
    }
    log(f"  {len(vendedores_validos)} vendedores com {MIN_SELLER_CALLS}+ ligações")

    perfis = {}
    for vendedor, calls in sorted(vendedores_validos.items(), key=lambda x: -len(x[1])):
        inter_path = Path(INTERMEDIATE_DIR) / f"p14_vendedor_{vendedor}.txt"
        cached = carregar_intermediario(inter_path)
        if cached:
            perfis[vendedor] = cached
            continue
        amostra = calls[:20]
        log(f"  Analisando {vendedor} ({len(calls)} ligações, amostra={len(amostra)})...")
        prompt = PROMPT14_VENDEDOR.format(
            vendedor=vendedor,
            n_lig=len(calls),
            n_amostra=len(amostra),
            ligacoes="\n\n".join(amostra),
        )
        resultado = api_call(prompt, max_tokens=3000)
        salvar(inter_path, resultado)
        perfis[vendedor] = resultado
        time.sleep(1.5)

    log("  Comparando vendedores...")
    perfis_texto = "\n\n".join(
        f"=== VENDEDOR: {v} ({len(calls_by_seller[v])} ligações) ===\n{p}"
        for v, p in perfis.items()
    )
    comparacao_prompt = PROMPT14_COMPARACAO.format(
        n_vendedores=len(perfis),
        perfis=perfis_texto,
    )
    return api_call(comparacao_prompt, model=SONNET, max_tokens=6000)

# ---------------------------------------------------------------------------
# PROMPT 15 — Eventos Raros de Alto Impacto
# ---------------------------------------------------------------------------
PROMPT15_BATCH = """Você é um analista de Revenue Intelligence (Localiza).
Vendedor=A | Cliente=C

IGNORE o que é comum. Procure APENAS eventos raros com impacto desproporcional:

R1 — Expansão (contratação, nova filial, crescimento de frota, novos contratos)
R2 — Churn (ameaça de saída, comparação com concorrente, insatisfação persistente)
R3 — Intel competitiva (migração de fornecedor, teste com concorrente, múltiplos fornecedores)
R4 — Influência (indicação espontânea, apresentação de contato, referência positiva)
R5 — Mudança estrutural (fusão, aquisição, troca de gestor, reestruturação)

LIGAÇÕES:
{ligacoes}

Para CADA evento raro encontrado retorne UMA linha CSV:
cliente_id,data,categoria,descricao_evento,impacto_potencial,acao_recomendada

impacto_potencial = alto/medio/baixo
Se não houver eventos raros neste lote: retorne exatamente "SEM_EVENTOS"
NÃO invente — só registre o que está explicitamente na conversa."""

PROMPT15_SINTESE = """Você é um analista de Revenue Intelligence sênior (Localiza).

Abaixo estão todos os eventos raros identificados em {n_calls} ligações de {n_clients} clientes:

{eventos}

TAREFA: Consolidação e priorização.

1. Tabela CSV final (sem duplicatas, ordenada por impacto_potencial desc):
cliente_id,data,categoria,descricao_evento,impacto_potencial,acao_recomendada

2. Análise estratégica:
- Top 5 clientes para ação IMEDIATA (com justificativa específica)
- Principal risco de churn identificado na base
- Principal oportunidade de expansão identificada
- Padrão de inteligência competitiva mais relevante
- Ações recomendadas para a liderança comercial"""

def run_prompt15(calls_by_client: dict[str, list[str]], n_calls: int) -> str:
    log("=== PROMPT 15: Eventos Raros de Alto Impacto ===")
    clients_list = list(calls_by_client.items())
    batches = [clients_list[i:i+BATCH_CLIENTS] for i in range(0, len(clients_list), BATCH_CLIENTS)]
    log(f"  {len(batches)} batches de até {BATCH_CLIENTS} clientes")

    todos_eventos = []
    for i, batch in enumerate(batches, 1):
        inter_path = Path(INTERMEDIATE_DIR) / f"p15_batch_{i:04d}.txt"
        cached = carregar_intermediario(inter_path)
        if cached:
            if cached.strip() != "SEM_EVENTOS":
                todos_eventos.append(cached)
            continue
        log(f"  Batch {i}/{len(batches)}...")
        ligacoes_texto = ""
        for client_id, calls in batch:
            ligacoes_texto += f"\n=== CLIENTE {client_id} ===\n"
            ligacoes_texto += "\n\n".join(calls[:4])  # max 4 calls por cliente
        prompt = PROMPT15_BATCH.format(ligacoes=ligacoes_texto)
        resultado = api_call(prompt)
        salvar(inter_path, resultado)
        if resultado.strip() not in ("SEM_EVENTOS", "[ERRO: falha na API após 4 tentativas]"):
            todos_eventos.append(resultado)
        time.sleep(1.5)

    if not todos_eventos:
        return "Nenhum evento raro identificado na base."

    log("  Sintetizando eventos raros...")
    sintese_prompt = PROMPT15_SINTESE.format(
        n_calls=n_calls,
        n_clients=len(clients_list),
        eventos="\n\n--- LOTE ---\n".join(todos_eventos),
    )
    return api_call(sintese_prompt, model=SONNET, max_tokens=6000)

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
def main():
    log("Carregando LIG...")
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        data: dict = json.load(f)

    total_clients = len(data)
    total_calls   = sum(len(v) for v in data.values())
    log(f"Carregado: {total_clients} clientes | {total_calls} ligações")

    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    Path(INTERMEDIATE_DIR).mkdir(parents=True, exist_ok=True)

    # Organizar dados
    log("Organizando dados e extraindo vendedores...")
    all_calls_fmt:    list[str]             = []
    calls_by_client:  dict[str, list[str]]  = {}
    calls_by_seller:  dict[str, list[str]]  = {}
    seller_per_call:  dict[str, str]        = {}  # segment_id → seller

    for client_id, calls in data.items():
        client_fmts = []
        for call in calls:
            fmt  = format_call(client_id, call)
            nome = extract_seller(call)
            sid  = call.get("segment_id", "")
            seller_per_call[sid] = nome
            all_calls_fmt.append(fmt)
            client_fmts.append(fmt)
            calls_by_seller.setdefault(nome, []).append(fmt)
        calls_by_client[client_id] = client_fmts

    log("Distribuição de vendedores identificados:")
    for v, c in sorted(calls_by_seller.items(), key=lambda x: -len(x[1])):
        if v != "Nao_Identificado" and len(c) >= MIN_SELLER_CALLS:
            log(f"  {v}: {len(c)} ligações")
    n_id = len(calls_by_seller.get("Nao_Identificado", []))
    log(f"  Nao_Identificado: {n_id} ligações (excluídos do P14)")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    # --- Prompt 13 ---
    r13 = run_prompt13(all_calls_fmt, total_calls)
    salvar(Path(OUTPUT_DIR) / f"prompt13_padroes_{ts}.txt", r13)

    # --- Prompt 14 ---
    r14 = run_prompt14(calls_by_seller)
    salvar(Path(OUTPUT_DIR) / f"prompt14_vendedores_{ts}.txt", r14)

    # --- Prompt 15 ---
    r15 = run_prompt15(calls_by_client, total_calls)
    salvar(Path(OUTPUT_DIR) / f"prompt15_eventos_raros_{ts}.txt", r15)

    log("=" * 60)
    log(f"ANÁLISE COMPLETA! Resultados em: {OUTPUT_DIR}")
    log("=" * 60)

if __name__ == "__main__":
    main()
