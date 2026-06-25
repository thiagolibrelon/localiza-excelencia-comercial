"""
SCORING DE POTENCIAL COMERCIAL — LOCALIZA FROTA PJ
===================================================
Avalia cada ligação em 3 dimensões extraídas dos 15 prompts do framework.
Roda em segundos nas 1275 ligações. Sem LLM — 100% determinístico.

Output: resultados_analise/scoring_potencial.csv
        resultados_analise/scoring_distribuicao.txt
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict

# ---------------------------------------------------------------------------
# Caminhos
# ---------------------------------------------------------------------------
FILE_PATH  = Path(__file__).parent.parent / "dados" / "LIG"
OUTPUT_DIR = Path(__file__).parent.parent / "resultados"

# ---------------------------------------------------------------------------
# DICIONÁRIOS DE SINAIS
# Cada lista é auditável — mostra exatamente o que buscamos na transcrição.
# ---------------------------------------------------------------------------

# P1 — B1: Pergunta diagnóstica antes de oferecer produto
SINAIS_DIAGNOSTICO = [
    "como está", "como é que", "qual é a", "quanto roda", "tem demanda",
    "como funciona", "tem alguma", "como que vocês", "qual seria", "tem interesse",
    "quais são", "como vocês", "quantos carros", "qual é a necessidade",
    "me conta", "me fala um pouco", "como está a frota",
]

# P1 — B6: Urgência criada com fato verificável
SINAIS_URGENCIA = [
    "hoje", "amanhã", "prazo", "vence", "último dia", "agora mesmo",
    "essa semana", "antes que", "só até", "contrato encerra",
    "data limite", "renovar agora", "fechar ainda hoje",
]

# P1 — B10: Vendedor sondou concorrente ou frota própria
SINAIS_SONDAGEM_CONCORRENTE = [
    "outra locadora", "frota própria", "tem frota", "outra empresa de locação",
    "usa alguma outra", "aluga em outro lugar", "tem veículo próprio",
    "tem carro próprio", "movida", "unidas", "móvel locadora",
]

# P1 — B5: Upsell conectado à dor revelada
SINAIS_UPSELL = [
    "proteção", "telemetria", "upgrade", "quilometragem maior", "categoria superior",
    "mensal ao invés", "contrato anual", "elétrico", "seminovo", "plano de km",
    "cobertura total", "seguro adicional",
]

# P1 — B3: Vendedor usou histórico do cliente
SINAIS_HISTORICO = [
    "vi aqui", "no cadastro", "no seu histórico", "na nossa base", "você já",
    "vocês já alugaram", "faz tempo que", "última vez que", "contrato anterior",
    "no sistema aqui", "já é cliente", "desde",
]

# P1 — B4: Vendedor alertou o cliente de algo
SINAIS_ALERTA = [
    "fique atento", "cuidado com", "antes que", "se não renovar", "risco de",
    "pode gerar multa", "vai cobrar", "vai perder", "importante que",
    "precisa ficar sabendo", "atenção para",
]

# P9 — FC: Fechamento com próximo passo claro
SINAIS_PROXIMO_PASSO = [
    "combinado", "fica assim então", "te ligo na", "retorno amanhã",
    "segunda-feira", "essa semana te ligo", "até terça", "deixa agendado",
    "vamos fazer o seguinte", "próximo passo", "você me confirma até",
]

# P9 — FC3/FC4: Fechamento vago (penaliza)
SINAIS_FECHAMENTO_VAGO = [
    "qualquer coisa me chama", "surgindo demanda", "pode me procurar",
    "à disposição", "qualquer necessidade", "qualquer dúvida",
]

# P10 — Promessas feitas pelo vendedor
SINAIS_PROMESSA = [
    "vou te mandar", "vou enviar", "te ligo", "vou verificar", "vou resolver",
    "vou contestar", "vou fazer", "vou entrar em contato", "vou solicitar",
    "providencio", "vou checar", "vou confirmar",
]

# P11 — Sinais competitivos mencionados pelo CLIENTE
SINAIS_COMPETITIVO_CLIENTE = [
    "unidas", "movida", "móvel", "hertz", "avis", "localfrio",
    "outra locadora", "frota própria", "carro próprio", "veículo próprio",
    "outro fornecedor", "outra empresa", "mais barato em outro",
]

# P15 — R1: Expansão (cliente sinalizou crescimento)
SINAIS_EXPANSAO = [
    "nova filial", "nova unidade", "abrindo", "expandindo", "crescendo",
    "mais carros", "mais veículos", "novos funcionários", "novo contrato",
    "mineradora", "nova obra", "nova região", "contratação",
    "aumentar frota", "precisar de mais",
]

# P15 — R2: Churn (cliente sinalizou saída)
SINAIS_CHURN = [
    "cancelar", "não vou mais", "vai cortar", "excluir a localiza",
    "não tenho interesse", "vou devolver tudo", "encerrar contrato",
    "desistir", "resolver em outro lugar",
]

# P2 — Operacional puro (reduz potencial)
SINAIS_OPERACIONAL = [
    "biometria", "senha", "acesso", "portal fora", "boleto", "avaria",
    "oficina", "sinistro", "multa de infração", "condutor",
    "fatura incorreta", "bloqueio", "manutenção",
]

# P2 — Comercial (aumenta potencial)
SINAIS_COMERCIAL = [
    "proposta", "valor", "cotação", "desconto", "renovar", "migrar",
    "contrato", "reserva", "fechar", "locação", "mensal", "diário",
]

# ---------------------------------------------------------------------------
# FUNÇÃO DE SCORING
# ---------------------------------------------------------------------------
def extrair_textos(call):
    """Separa texto do vendedor (A), cliente (C) e full."""
    conv = call.get("conversa", [])
    texto_a = " ".join(t.lower() for s, t in conv if s == "A")
    texto_c = " ".join(t.lower() for s, t in conv if s == "C")
    full    = texto_a + " " + texto_c
    turns_a = sum(1 for s, _ in conv if s == "A")
    turns_c = sum(1 for s, _ in conv if s == "C")
    primeiro_speaker = conv[0][0] if conv else "?"
    return texto_a, texto_c, full, turns_a, turns_c, primeiro_speaker

def conta_sinais(texto, lista):
    return sum(1 for s in lista if s in texto)

def tem_sinal(texto, lista):
    return any(s in texto for s in lista)

def avaliar_ligacao(client_id, call):
    """
    Avalia uma ligação e retorna score, nível e razões detalhadas.
    Score total: 0-30 pontos divididos em 3 dimensões de 0-10.
    """
    texto_a, texto_c, full, turns_a, turns_c, primeiro = extrair_textos(call)
    duracao = call.get("duracao", 0)

    score_contexto   = 0
    score_cliente    = 0
    score_vendedor   = 0
    razoes           = []
    penalidades      = []
    sinais_detectados = {}

    # -----------------------------------------------------------------------
    # DIMENSÃO 1 — CONTEXTO (0-10)
    # Fonte: P2 (tipo de ligação) + P12 (talk ratio) + duração
    # Pergunta: "Esta ligação tem ambiente favorável para ação comercial?"
    # -----------------------------------------------------------------------

    # D1.1 — Duração (proxy de profundidade)
    # Fonte: P12 — ligações longas têm mais turns e mais conteúdo qualificável
    if duracao >= 600:
        score_contexto += 4
        razoes.append("[D1] Duração >10 min → conversa profunda com múltiplos temas")
    elif duracao >= 300:
        score_contexto += 3
        razoes.append("[D1] Duração >5 min → conversa substantiva")
    elif duracao >= 120:
        score_contexto += 2
        razoes.append("[D1] Duração >2 min → conteúdo suficiente para análise")
    elif duracao >= 30:
        score_contexto += 1
        razoes.append("[D1] Duração curta mas com conteúdo mínimo")
    else:
        penalidades.append("[D1] Duração <30s → ligação superficial ou sem conteúdo")

    # D1.2 — Vendedor iniciou (proativo)
    # Fonte: P1 B8 — ligar proativamente é comportamento comercial
    if primeiro == "A":
        score_contexto += 2
        razoes.append("[D1] Vendedor ligou proativamente (B8)")
    else:
        score_contexto += 1
        razoes.append("[D1] Cliente iniciou — contexto ainda aproveitável")

    # D1.3 — Natureza da ligação
    # Fonte: P2 — ligação puramente operacional tem menos janela comercial
    n_op  = conta_sinais(full, SINAIS_OPERACIONAL)
    n_com = conta_sinais(texto_a, SINAIS_COMERCIAL)
    sinais_detectados["comercial_count"] = n_com
    sinais_detectados["operacional_count"] = n_op

    if n_com >= 3:
        score_contexto += 4
        razoes.append(f"[D1] {n_com} sinais comerciais no discurso do vendedor")
    elif n_com >= 1:
        score_contexto += 2
        razoes.append(f"[D1] {n_com} sinal(is) comercial(is) detectado(s)")
    elif n_op >= 3 and n_com == 0:
        score_contexto -= 2
        penalidades.append(f"[D1] Ligação puramente operacional ({n_op} sinais op., 0 comerciais)")

    score_contexto = max(0, min(10, score_contexto))

    # -----------------------------------------------------------------------
    # DIMENSÃO 2 — SINAIS DO CLIENTE (0-10)
    # Fonte: P11 (intel competitiva) + P15 (eventos raros) + P4 (health)
    # Pergunta: "O cliente revelou oportunidade que justifica ação?"
    # -----------------------------------------------------------------------

    # D2.1 — Expansão (sinal mais forte de oportunidade)
    # Fonte: P15 R1 — empresa em crescimento = mais veículos = receita nova
    if tem_sinal(texto_c, SINAIS_EXPANSAO):
        score_cliente += 4
        razoes.append("[D2] Cliente sinalizou expansão/crescimento (P15-R1)")
        sinais_detectados["expansao"] = True

    # D2.2 — Concorrente mencionado pelo cliente
    # Fonte: P11 IC1/IC5 — cliente que fala de concorrente está avaliando alternativas
    if tem_sinal(texto_c, SINAIS_COMPETITIVO_CLIENTE):
        score_cliente += 3
        razoes.append("[D2] Cliente mencionou concorrente ou frota própria (P11-IC1)")
        sinais_detectados["concorrente_cliente"] = True

    # D2.3 — Sinal de churn
    # Fonte: P15 R2 + P4 — cliente em risco = urgência de retenção = potencial alto
    if tem_sinal(texto_c, SINAIS_CHURN):
        score_cliente += 3
        razoes.append("[D2] Sinal de churn detectado — oportunidade de retenção crítica (P15-R2)")
        sinais_detectados["churn"] = True

    # D2.4 — Dores reveladas que mapeiam para produtos
    # Fonte: P6 OP2 — dor sem produto conectado é oportunidade perdida identificada
    n_dores = conta_sinais(texto_c, SINAIS_OPERACIONAL)
    if n_dores >= 2:
        score_cliente += 2
        razoes.append(f"[D2] {n_dores} dores do cliente detectadas — janela de produto (P6-OP2)")
    elif n_dores == 1:
        score_cliente += 1
        razoes.append("[D2] 1 dor do cliente detectada — janela de produto pequena")

    score_cliente = max(0, min(10, score_cliente))

    # -----------------------------------------------------------------------
    # DIMENSÃO 3 — COMPORTAMENTO DO VENDEDOR (0-10)
    # Fonte: P1 (B1-B10) + P5 (Challenger) + P9 (Abertura/Fechamento) + P10 (Promessas)
    # Pergunta: "O vendedor aplicou os comportamentos que fecham contratos?"
    # -----------------------------------------------------------------------

    # D3.1 — Pergunta diagnóstica (B1)
    # Fonte: P1 B1 — diagnóstico antes do produto é o 2° comportamento mais correlacionado
    # com fechamento no framework (peso 2)
    if tem_sinal(texto_a, SINAIS_DIAGNOSTICO):
        score_vendedor += 2
        razoes.append("[D3] Pergunta diagnóstica antes do produto (B1, peso=2)")
        sinais_detectados["diagnostico"] = True

    # D3.2 — Sondagem de concorrente (B10)
    # Fonte: P1 B10 — comportamento de MAIOR peso no framework (peso=3)
    # Vendedor que pergunta sobre concorrente abre a conversa de valor
    if tem_sinal(texto_a, SINAIS_SONDAGEM_CONCORRENTE):
        score_vendedor += 3
        razoes.append("[D3] Vendedor sondou concorrência/frota própria (B10, peso=3 — maior do framework)")
        sinais_detectados["sondagem_concorrente"] = True
    elif sinais_detectados.get("concorrente_cliente") and not sinais_detectados.get("sondagem_concorrente"):
        penalidades.append("[D3] Cliente citou concorrente mas vendedor NÃO explorou (oportunidade perdida P11)")

    # D3.3 — Urgência com fato verificável (B6)
    # Fonte: P1 B6 — 2° maior peso do framework (peso=3); cria ancoragem temporal
    if tem_sinal(texto_a, SINAIS_URGENCIA):
        score_vendedor += 3
        razoes.append("[D3] Urgência criada com fato verificável (B6, peso=3)")
        sinais_detectados["urgencia"] = True

    # D3.4 — Upsell conectado à dor (B5)
    # Fonte: P1 B5 + P7 — upsell desconectado não converte; conectado à dor sim
    if tem_sinal(texto_a, SINAIS_UPSELL) and n_com >= 2:
        score_vendedor += 2
        razoes.append("[D3] Tentativa de upsell detectada no contexto comercial (B5)")
        sinais_detectados["upsell"] = True

    # D3.5 — Usou histórico do cliente (B3)
    # Fonte: P1 B3 — personalização com histórico aumenta credibilidade e relevância
    if tem_sinal(texto_a, SINAIS_HISTORICO):
        score_vendedor += 1
        razoes.append("[D3] Vendedor usou histórico/dados do cliente (B3)")
        sinais_detectados["historico"] = True

    # D3.6 — Qualidade do fechamento (P9)
    # Fonte: P9 FC1/FC2 vs FC3/FC4 — fechamento sem próximo passo deixa cliente sem âncora
    if tem_sinal(texto_a, SINAIS_PROXIMO_PASSO):
        score_vendedor += 2
        razoes.append("[D3] Fechamento com próximo passo concreto (P9-FC1/FC2)")
        sinais_detectados["proximo_passo"] = True
    elif tem_sinal(texto_a, SINAIS_FECHAMENTO_VAGO):
        penalidades.append("[D3] Fechamento vago 'qualquer coisa me chama' (P9-FC3/FC4)")

    # D3.7 — Promessa feita (P10)
    # Fonte: P10 — promessa é sinal de comprometimento; sem prazo = risco alto
    if tem_sinal(texto_a, SINAIS_PROMESSA):
        score_vendedor += 1
        razoes.append("[D3] Promessa feita pelo vendedor (P10)")
        sinais_detectados["promessa"] = True

    score_vendedor = max(0, min(10, score_vendedor))

    # -----------------------------------------------------------------------
    # SCORE TOTAL E CLASSIFICAÇÃO
    # -----------------------------------------------------------------------
    score_total = score_contexto + score_cliente + score_vendedor

    if score_total >= 20:
        nivel = "ALTO"
    elif score_total >= 13:
        nivel = "MEDIO"
    elif score_total >= 7:
        nivel = "BAIXO"
    else:
        nivel = "SEM_POTENCIAL"

    return {
        "client_id":          client_id,
        "data":               call.get("data", "?")[:10],
        "duracao_s":          duracao,
        "sentimento":         call.get("sentimento", "?"),
        "nivel":              nivel,
        "score_total":        score_total,
        "score_contexto":     score_contexto,
        "score_cliente":      score_cliente,
        "score_vendedor":     score_vendedor,
        "razoes":             " | ".join(razoes),
        "penalidades":        " | ".join(penalidades),
        "sinais":             sinais_detectados,
        "turns_vendedor":     turns_a,
        "turns_cliente":      turns_c,
        "talk_ratio_vendedor": round(turns_a / (turns_a + turns_c), 2) if (turns_a + turns_c) > 0 else 0,
    }

# ---------------------------------------------------------------------------
# MAIN — processa todas as ligações e gera outputs
# ---------------------------------------------------------------------------
def main():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Carregando LIG...")
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_calls = sum(len(v) for v in data.values())
    print(f"  {len(data)} clientes | {total_calls} ligações")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Processa todas as ligações
    resultados = []
    for client_id, calls in data.items():
        for call in calls:
            r = avaliar_ligacao(client_id, call)
            resultados.append(r)

    # -----------------------------------------------------------------------
    # Salva CSV principal
    # -----------------------------------------------------------------------
    csv_path = OUTPUT_DIR / "scoring_potencial.csv"
    cabecalho = (
        "client_id,data,duracao_s,sentimento,nivel,score_total,"
        "score_contexto,score_cliente,score_vendedor,"
        "turns_vendedor,turns_cliente,talk_ratio_vendedor,"
        "tem_diagnostico,tem_urgencia,tem_sondagem_concorrente,"
        "tem_upsell,tem_churn,tem_expansao,tem_proximo_passo,"
        "razoes,penalidades\n"
    )
    linhas = [cabecalho]
    for r in resultados:
        s = r["sinais"]
        linha = (
            f"{r['client_id']},{r['data']},{r['duracao_s']},{r['sentimento']},"
            f"{r['nivel']},{r['score_total']},"
            f"{r['score_contexto']},{r['score_cliente']},{r['score_vendedor']},"
            f"{r['turns_vendedor']},{r['turns_cliente']},{r['talk_ratio_vendedor']},"
            f"{int(s.get('diagnostico',False))},{int(s.get('urgencia',False))},"
            f"{int(s.get('sondagem_concorrente',False))},{int(s.get('upsell',False))},"
            f"{int(s.get('churn',False))},{int(s.get('expansao',False))},"
            f"{int(s.get('proximo_passo',False))},"
            f"\"{r['razoes']}\",\"{r['penalidades']}\"\n"
        )
        linhas.append(linha)
    csv_path.write_text("".join(linhas), encoding="utf-8")
    print(f"  CSV salvo: {csv_path.name}")

    # -----------------------------------------------------------------------
    # Relatório de distribuição e insights
    # -----------------------------------------------------------------------
    dist = Counter(r["nivel"] for r in resultados)
    total = len(resultados)

    # Agrupa por vendedor (dos que conseguimos identificar nos sinais)
    # Usa campo "razoes" para identificar comportamentos
    por_nivel  = defaultdict(list)
    for r in resultados:
        por_nivel[r["nivel"]].append(r)

    # Métricas por nível
    def media(lista, campo):
        vals = [r[campo] for r in lista if r[campo] is not None]
        return round(sum(vals) / len(vals), 1) if vals else 0

    # Sinais mais comuns nas ligações ALTO
    altos = por_nivel["ALTO"]
    sinais_alto = {
        "diagnostico":           sum(1 for r in altos if r["sinais"].get("diagnostico")),
        "urgencia":              sum(1 for r in altos if r["sinais"].get("urgencia")),
        "sondagem_concorrente":  sum(1 for r in altos if r["sinais"].get("sondagem_concorrente")),
        "upsell":                sum(1 for r in altos if r["sinais"].get("upsell")),
        "churn":                 sum(1 for r in altos if r["sinais"].get("churn")),
        "expansao":              sum(1 for r in altos if r["sinais"].get("expansao")),
        "proximo_passo":         sum(1 for r in altos if r["sinais"].get("proximo_passo")),
    }

    # Top 10 ligações com maior potencial
    top10 = sorted(resultados, key=lambda r: r["score_total"], reverse=True)[:10]

    # Ligações com churn ou expansão (ação imediata)
    urgentes = [r for r in resultados if r["sinais"].get("churn") or r["sinais"].get("expansao")]

    relatorio = f"""
====================================================================
SCORING DE POTENCIAL COMERCIAL — LOCALIZA FROTA PJ
Rodado em: {datetime.now().strftime('%d/%m/%Y %H:%M')}
Base: {total_calls} ligações | {len(data)} clientes
====================================================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DISTRIBUIÇÃO DE POTENCIAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔴 ALTO          : {dist['ALTO']:>4} ligações ({dist['ALTO']/total*100:5.1f}%)  Score ≥ 20
  🟠 MÉDIO         : {dist['MEDIO']:>4} ligações ({dist['MEDIO']/total*100:5.1f}%)  Score 13–19
  🟡 BAIXO         : {dist['BAIXO']:>4} ligações ({dist['BAIXO']/total*100:5.1f}%)  Score 7–12
  ⚪ SEM POTENCIAL : {dist['SEM_POTENCIAL']:>4} ligações ({dist['SEM_POTENCIAL']/total*100:5.1f}%)  Score 0–6

  Score médio geral: {media(resultados, 'score_total')}
  Score médio ALTO:  {media(altos, 'score_total')}
  Duração média ALTO: {media(altos, 'duracao_s')}s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SINAIS NAS LIGAÇÕES DE ALTO POTENCIAL (n={len(altos)})
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  B1  Diagnóstico antes do produto : {sinais_alto['diagnostico']:>4} ({sinais_alto['diagnostico']/len(altos)*100 if altos else 0:.0f}%)
  B6  Urgência criada               : {sinais_alto['urgencia']:>4} ({sinais_alto['urgencia']/len(altos)*100 if altos else 0:.0f}%)
  B10 Sondagem de concorrente       : {sinais_alto['sondagem_concorrente']:>4} ({sinais_alto['sondagem_concorrente']/len(altos)*100 if altos else 0:.0f}%)
  B5  Upsell tentado                : {sinais_alto['upsell']:>4} ({sinais_alto['upsell']/len(altos)*100 if altos else 0:.0f}%)
  P15 Expansão detectada            : {sinais_alto['expansao']:>4} ({sinais_alto['expansao']/len(altos)*100 if altos else 0:.0f}%)
  P15 Churn detectado               : {sinais_alto['churn']:>4} ({sinais_alto['churn']/len(altos)*100 if altos else 0:.0f}%)
  P9  Próximo passo concreto        : {sinais_alto['proximo_passo']:>4} ({sinais_alto['proximo_passo']/len(altos)*100 if altos else 0:.0f}%)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOP 10 LIGAÇÕES — MAIOR POTENCIAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{"Cliente":<14} {"Data":<12} {"Score":>5} {"Nível":<14} {"Duração":>7}   Destaques
{"-"*14} {"-"*12} {"-"*5} {"-"*14} {"-"*7}   {"-"*40}"""

    for r in top10:
        destaques = []
        if r["sinais"].get("expansao"):         destaques.append("EXPANSÃO")
        if r["sinais"].get("churn"):            destaques.append("CHURN")
        if r["sinais"].get("sondagem_concorrente"): destaques.append("CONCORRENTE")
        if r["sinais"].get("urgencia"):         destaques.append("URGÊNCIA")
        if r["sinais"].get("diagnostico"):      destaques.append("DIAGNÓSTICO")
        relatorio += f"\n{r['client_id']:<14} {r['data']:<12} {r['score_total']:>5} {r['nivel']:<14} {r['duracao_s']:>6}s   {' | '.join(destaques)}"

    relatorio += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
AÇÃO IMEDIATA — CHURN + EXPANSÃO DETECTADOS ({len(urgentes)} ligações)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    for r in sorted(urgentes, key=lambda x: x["score_total"], reverse=True)[:20]:
        tipo = []
        if r["sinais"].get("churn"):   tipo.append("🔴 CHURN")
        if r["sinais"].get("expansao"):tipo.append("🟢 EXPANSÃO")
        relatorio += f"\n  Cliente {r['client_id']} | {r['data']} | Score {r['score_total']} | {' + '.join(tipo)}"

    relatorio += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARQUIVOS GERADOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  scoring_potencial.csv     — linha por ligação com score e sinais
  scoring_distribuicao.txt  — este relatório de distribuição
"""

    dist_path = OUTPUT_DIR / "scoring_distribuicao.txt"
    dist_path.write_text(relatorio, encoding="utf-8")
    print(relatorio.encode("ascii", errors="replace").decode("ascii"))
    print(f"\n  Relatorio salvo: {dist_path.name}")

if __name__ == "__main__":
    main()
