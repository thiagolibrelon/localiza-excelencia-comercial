"""
Compara a qualidade de classificacao (Prompt P1_P2) entre gemini-2.5-flash
(ja rodado, resultados/gemini_v2/batch01_P1_P2_*.txt) e 4 modelos com cota
diaria maior, usando o MESMO batch01 (primeiros 50 clientes de dados/LIG).

Objetivo: decidir se algum modelo "mais simples"/com mais cota mantem
qualidade suficiente pra assumir prompts do framework (ex: P3, P4, P8, P11-15
que hoje nao tem cobertura automatizada nenhuma).
"""
import json
import os
from pathlib import Path

from google import genai
from google.genai import types

FILE_PATH = Path(__file__).parent.parent / "dados" / "LIG"
ENV_FILE = Path(__file__).parent.parent / ".env"
OUT_DIR = Path(__file__).parent.parent / "resultados" / "comparacao_modelos"
BATCH_SIZE = 50

MODELOS_TESTE = [
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemma-4-26b-a4b-it",
    "gemma-4-31b-it",
]

for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

client = genai.Client(api_key=os.environ["GEMINI_API_KEY_1"])

CONTEXTO = """
Empresa: Localiza (locacao de veiculos mensais para PJ)
Vendedor = "A" | Cliente = "C"
STT fragmentado - junte turns do mesmo speaker. <unk> = inaudivel, ignore.
"""

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

def main():
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    items = list(data.items())[:BATCH_SIZE]
    batch_data = dict(items)
    n_lig = sum(len(v) for v in batch_data.values())
    print(f"Batch01: {len(batch_data)} clientes, {n_lig} ligacoes (mesmo recorte usado no run original)")

    trans_completo = formatar_ligacoes(batch_data)
    prompt_completo = prompt_p1_p2(trans_completo)

    # subconjunto pequeno (5 clientes) pra modelos com TPM baixo (Gemma: 16K/min)
    sub_data = dict(items[:5])
    trans_pequeno = formatar_ligacoes(sub_data)
    prompt_pequeno = prompt_p1_p2(trans_pequeno)
    n_lig_pequeno = sum(len(v) for v in sub_data.values())
    print(f"Subconjunto pequeno: {len(sub_data)} clientes, {n_lig_pequeno} ligacoes (pra modelos com TPM baixo)")

    OUT_DIR.mkdir(parents=True, exist_ok=True)

    # (modelo, usa_thinking_config, prompt a usar)
    CONFIGS = [
        ("gemini-3.1-flash-lite", True, prompt_completo, "completo"),
        ("gemini-3.5-flash-lite", False, prompt_completo, "completo"),
        ("gemma-4-26b-a4b-it", False, prompt_pequeno, "pequeno"),
        ("gemma-4-31b-it", False, prompt_pequeno, "pequeno"),
    ]

    for modelo, usa_thinking, prompt, tamanho in CONFIGS:
        print(f"\n=== {modelo} ({tamanho}) ===")
        cfg_kwargs = dict(max_output_tokens=8192, temperature=0.1)
        if usa_thinking:
            cfg_kwargs["thinking_config"] = types.ThinkingConfig(thinking_budget=0)
        try:
            resp = client.models.generate_content(
                model=modelo,
                contents=prompt,
                config=types.GenerateContentConfig(**cfg_kwargs),
            )
            texto = resp.text or ""
            finish = resp.candidates[0].finish_reason if resp.candidates else "?"
            usage = resp.usage_metadata
            think_tk = getattr(usage, "thoughts_token_count", None)
            print(f"finish={finish} | in={usage.prompt_token_count}tk | out={usage.candidates_token_count}tk | think={think_tk}tk")
            nome_arquivo = modelo.replace("/", "_") + f"_batch01_P1_P2_{tamanho}.txt"
            (OUT_DIR / nome_arquivo).write_text(texto, encoding="utf-8")
            print(f"Salvo: {nome_arquivo} ({len(texto)} chars)")
        except Exception as e:
            print(f"ERRO: {e}")

if __name__ == "__main__":
    main()
