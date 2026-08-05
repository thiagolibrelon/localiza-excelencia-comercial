"""
Analise do lote JULHO (recebido em 22/07/2026, dados de 01-21/07) via Gemini 2.5 Flash.

Copia de analisar_gemini_novo_lote.py, com FILE_PATH/OUTPUT_DIR redirecionados
pra pasta JULHO/ (o usuario passou a alimentar essa pasta diariamente com as
ligacoes do dia anterior). Ver scripts/converter_julho.py para o pre-processamento
que gera o JSON de entrada (agrupa por CLIENTE, corrige encoding cp1252->utf-8,
usa cd_segmento como ID unico porque cd_contato_master vem corrompido/notacao
cientifica do Excel).

IMPORTANTE: compartilha a MESMA cota diaria (MAX_CALLS=20) e a mesma API key do
analisar_gemini_novo_lote.py — os dois nao devem rodar no mesmo horario/dia se
ambos tiverem trabalho pendente, senao competem pela cota. Em 22/07/2026 o
novo_lote estava 100% completo (0 chamadas usadas), entao a cota inteira do dia
ficou livre pra este script. Ver JULHO/PLANO_PROCESSAMENTO.md para o cronograma.

Rotina esperada (comecando 22/07/2026):
  ~14-15 dias a 20 chamadas/dia pra zerar o backlog de 01-21/07 (6.813 ligacoes),
  depois acompanha o fluxo diario normal (arquivo re-roda do zero, idempotente).
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
FILE_PATH        = str(Path(__file__).parent.parent / "JULHO" / "dados_convertidos" / "julho_completo.json")
OUTPUT_DIR       = Path(__file__).parent.parent / "JULHO" / "resultados_gemini"
ENV_FILE         = Path(__file__).parent.parent / ".env"

MODEL            = "gemini-2.5-flash"
BATCH_SIZE       = 60    # clientes por batch
MAX_CALLS_POR_KEY = 20   # cota diaria do free tier, por projeto/key
MAX_LIG_PER_CALL = 100   # batches com mais ligacoes sao divididos em 2 chamadas
MAX_OUTPUT_TOKENS = 32768  # 4x o original (8192) — modelo suporta ate ~65535
MIN_OUTPUT_BYTES = 4000  # abaixo disso = arquivo truncado, sera re-rodado
SLEEP_ENTRE_CHAMADAS = 65  # segundos — free tier limita 250.000 tokens de INPUT/minuto;
                            # 65s garante que cada chamada cai numa janela nova (visto na pratica:
                            # 2 chamadas de ~124 ligacoes em sequencia rapida estouraram o limite)

# Grupos de prompts prioritarios para a analise de fechamento
# Ordem = fila: cada grupo so comeca a consumir chamadas depois que os
# anteriores estiverem 100% completos (todos os batches de um grupo antes do
# proximo), compartilhando a MESMA cota diaria (mesmas GEMINI_API_KEY_N) —
# sem precisar de coordenacao manual entre os prompts.
# P4_P8_P11: health score (por cliente) + objecoes/inteligencia competitiva
#   (por evento) — consolidado em CONSOLIDADO_JULHO.csv via consolidar_julho.py.
# P13_P15: padroes emergentes + eventos raros — exploratorio de base inteira,
#   sem "1 linha por ligacao"; salvo como texto por lote (batchNN_P13_P15_*.txt),
#   NAO entra no CSV consolidado (revisar manualmente, como os relatorios Fable).
# P14 (diferencas entre vendedores) fica de fora de proposito: a base nao tem
#   identidade de vendedor, so carteira — ja respondido de forma mais
#   confiavel por resultados/cruzamento_ligacoes_diarias/carteiras_comportamento_final.csv.
GRUPOS_PRIORITY  = ["P1_P2", "P5_P6", "P9_P10", "P3_P7", "P4_P8_P11", "P13_P15"]

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------
for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
    line = line.strip()
    if line and not line.startswith("#") and "=" in line:
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip())

# Cada GEMINI_API_KEY_N pode viver num projeto Google diferente, e a cota
# diaria do free tier (GenerateRequestsPerDayPerProjectPerModel) e por
# projeto. Com N keys de projetos distintos, o teto vira N * 20/dia.
# Projetos criados recentemente podem nao ter acesso ao MODEL default (ex:
# GEMINI_API_KEY_2 nao tem gemini-2.5-flash liberado - 404 "no longer
# available to new users"), entao cada key aceita um modelo proprio via
# GEMINI_API_KEY_N_MODEL (fallback pro MODEL global se nao definido).
_KEY_ENV_NAMES = ["GEMINI_API_KEY_1", "GEMINI_API_KEY_2", "GEMINI_API_KEY_3"]
keys = []
for env_name in _KEY_ENV_NAMES:
    valor = os.environ.get(env_name)
    if valor:
        keys.append({
            "nome": env_name,
            "client": genai.Client(api_key=valor),
            "model": os.environ.get(f"{env_name}_MODEL", MODEL),
            "calls": 0,
            "exhausted": False,
        })

if not keys:
    raise RuntimeError("Nenhuma GEMINI_API_KEY_N encontrada no .env")

MAX_CALLS = MAX_CALLS_POR_KEY * len(keys)

calls_made = 0
quota_exhausted = False

def _key_ativa():
    """Primeira key com cota disponivel hoje."""
    for k in keys:
        if not k["exhausted"] and k["calls"] < MAX_CALLS_POR_KEY:
            return k
    return None

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)

def salvar(nome, texto):
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    p = OUTPUT_DIR / nome
    p.write_text(texto, encoding="utf-8")
    log(f"  -> Salvo: {p.name} ({len(texto)} chars)")

BATCH_INDEX_PATH = Path(__file__).parent.parent / "JULHO" / "dados_convertidos" / "batch_index.json"

def carregar_indice_batch():
    if BATCH_INDEX_PATH.exists():
        return json.loads(BATCH_INDEX_PATH.read_text(encoding="utf-8"))
    return {}

def salvar_indice_batch(indice):
    BATCH_INDEX_PATH.write_text(json.dumps(indice, ensure_ascii=False), encoding="utf-8")

def batch_tem_saida(b_idx):
    return any(OUTPUT_DIR.glob(f"batch{b_idx:02d}_*"))

def atribuir_batches(data, size):
    """
    Atribui cada cliente a um numero de batch de forma ESTAVEL entre execucoes.
    Sem isso: converter_julho.py reconstroi o JSON do zero a cada dia (novos
    clientes entram no meio da ordem de insercao), e um batching posicional
    (items[i:i+size]) muda a composicao de TODOS os batches a cada execucao —
    "ja_existe(b_idx)" acha o arquivo batch01_P1_P2_*.txt antigo e pula,
    mas ele passa a representar um grupo de clientes diferente do batch01 novo.
    Ja causou descarte de batches em 22/07/2026.

    Estrategia: uma vez que um batch tenha QUALQUER saida gravada (Gemini ja
    rodou pra ele, em qualquer grupo), ele fica congelado pra sempre — os
    clientes que estao nele nunca mudam. Clientes novos (de um dia seguinte)
    sempre entram em batches novos ou no unico batch ainda "aberto" (sem
    nenhuma saida gravada ainda).
    """
    indice = carregar_indice_batch()

    max_batch = max(indice.values(), default=0)
    batch_aberto = max_batch if max_batch and not batch_tem_saida(max_batch) else max_batch + 1
    contagem_batch_aberto = sum(1 for v in indice.values() if v == batch_aberto)

    # preserva a ordem de insercao do JSON (nao ordena por cliente_id) —
    # importante no bootstrap, pra que o indice inicial reproduza exatamente
    # a composicao dos batches que ja foram processados antes deste fix
    novos_clientes = [cid for cid in data if cid not in indice]
    for cid in novos_clientes:
        if contagem_batch_aberto >= size:
            batch_aberto += 1
            contagem_batch_aberto = 0
        indice[cid] = batch_aberto
        contagem_batch_aberto += 1

    salvar_indice_batch(indice)

    batches_dict = {}
    for cid, ligacoes in data.items():
        b = indice[cid]
        batches_dict.setdefault(b, {})[cid] = ligacoes

    n_bat = max(batches_dict.keys(), default=0)
    return [batches_dict.get(i, {}) for i in range(1, n_bat + 1)]


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
        if f.stat().st_size >= MIN_OUTPUT_BYTES:
            return f
        best = best or f
    if best:
        log(f"  Arquivo {best.name} pequeno ({best.stat().st_size} bytes) mas valido — assumindo completo")
    return best

def chamar_gemini(prompt, max_tokens=MAX_OUTPUT_TOKENS):
    global calls_made, quota_exhausted
    for tentativa in range(4):
        k = _key_ativa()
        if k is None:
            log("  Cota diaria esgotada em todas as keys - encerrando execucao (reseta ~4h BRT)")
            quota_exhausted = True
            return None
        try:
            resp = k["client"].models.generate_content(
                model=k["model"],
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=max_tokens,
                    temperature=0.1,
                    thinking_config=types.ThinkingConfig(thinking_budget=0),
                ),
            )
            calls_made += 1
            k["calls"] += 1
            texto = resp.text
            finish = resp.candidates[0].finish_reason if resp.candidates else "?"
            usage = resp.usage_metadata
            log(f"    [{k['nome']}/{k['model']} {k['calls']}/{MAX_CALLS_POR_KEY}] finish={finish} | in={usage.prompt_token_count}tk | out={usage.candidates_token_count}tk | think={usage.thoughts_token_count}tk")
            if str(finish) in ("FinishReason.MAX_TOKENS", "MAX_TOKENS"):
                texto += "\n\n[TRUNCADO: MAX_TOKENS]"
            return texto
        except Exception as e:
            msg = str(e)
            if "GenerateRequestsPerDayPerProjectPerModel" in msg:
                log(f"  Cota diaria esgotada em {k['nome']} - tentando proxima key")
                k["exhausted"] = True
                continue
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
# Prompts (identicos aos de analisar_gemini.py)
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

def prompt_p3_p7(trans):
    return f"""Voce e analista de Customer Success e de expansao de receita em contas B2B de locacao de frotas corporativas.
{CONTEXTO}

Analise CADA ligacao abaixo e retorne CSV linha a linha. Nao pule nenhuma ligacao.
NUNCA use virgula dentro de um campo — troque por ";" ou "/" se precisar separar itens dentro do mesmo campo.

### CSV-P3 (Problemas Recorrentes)
cliente_id,data,problemas_identificados,quem_relatou,foi_resolvido_na_ligacao,escalou_para

problemas_identificados: codigos separados por "+" (ex: P1+P3), ou "nenhum" se a ligacao nao teve problema.
So marque um codigo se o problema for tema central ou relevante da ligacao — NAO marque por mencao
tangencial de 1 palavra-chave sem um problema real por tras dela.
P1=Acesso/sistema(portal fora do ar,senha,biometria) | P2=Faturamento/cobranca(boleto errado,fatura errada)
P3=Multa/infracao | P4=Manutencao/substituto(carro em oficina,sem substituto)
P5=Condutor/cadastro(troca de condutor,habilitacao) | P6=Km excedente(cobranca incorreta,plano errado)
P7=Disponibilidade(carro reservado indisponivel) | P8=Franquia/agencia(processo diferente em franqueada)
P9=Sinistro(acidente,franquia de dano)
P10=Reserva/sistema(reserva nao aparece no sistema, status incorreto, erro ao criar/editar uma reserva,
bug reproduzivel do fluxo de reserva). NAO marcar P10 quando for so duvida de como navegar/usar o
portal sem nenhum erro real (isso e "nenhum", nao P10), nem quando o assunto real da ligacao for outro
(fatura, cadastro, troca de contato comercial) e "reserva" so aparecer de passagem.
P11=Outro
P12=Manipulacao de pesquisa/NPS (vendedor pede/dita a nota — marcar quem_relatou=vendedor_detectou,foi_resolvido_na_ligacao=NAO)
quem_relatou: cliente|vendedor_detectou|nenhum
foi_resolvido_na_ligacao: SIM|NAO|PARCIAL|nenhum
escalou_para: 0800|supervisora|IT|nao_escalou|nenhum

### CSV-P7 (Cross-sell e Upsell)
cliente_id,data,duracao_s,produtos_mencionados,produtos_ofertados,janela_perdida,produto_janela,descricao_curta

produtos_mencionados/produtos_ofertados: codigos separados por "+" (ex: PR1+PR3), ou "nenhum"
PR1=Aluguel mensal leve(RAC,core) | PR2=Aluguel pesado(caminhao,carreta — NAO inclui PR1) | PR3=Telemetria
PR4=Protecao total/cobertura de avarias | PR5=Upgrade de categoria | PR6=Km adicional | PR7=Contrato anual
PR8=Veiculos eletricos | PR9=ZARP | PR10=Meoo | PR11=Venda de Seminovos
PR12=Gestao de frotas (contrato longo, cliente adquire veiculo personalizavel, administrado pela Localiza — diferente de PR7)
janela_perdida: SIM se o cliente disse algo que se conecta a um produto e o vendedor NAO ofereceu | NAO caso contrario
produto_janela: qual codigo PR se aplicaria a janela perdida (ou "nenhum" se janela_perdida=NAO)
Exemplos de janela: multa em condutor errado->PR3 | frota propria/personalizacao->PR12 | sinistro com franquia alta->PR4 | renova ha 3+ meses sem personalizacao->PR7 | perfil sustentavel->PR8
descricao_curta: frase curta explicando a janela perdida (campo LIVRE, unico que pode conter texto descritivo — ainda assim SEM virgula), ou "nenhuma"

IMPORTANTE: processe TODAS as {len(trans.split('=== LIGACAO'))-1} ligacoes. Retorne P3 completo, depois P7 completo. Sem explicacoes.

LIGACOES:
{trans}"""


def prompt_p4_p8_p11(trans):
    return f"""Voce e analista de Customer Success, treinamento de vendas e inteligencia competitiva B2B.
{CONTEXTO}

Analise as ligacoes abaixo e retorne CSV linha a linha. NUNCA use virgula dentro de um campo — troque por ";" ou "/" se precisar.

### CSV-P4 (Health Score do Cliente) — UMA LINHA POR CLIENTE (nao por ligacao), agregando todas as ligacoes desse cliente no lote
cliente_id,total_ligacoes,volume,adimplencia,fidelidade,engajamento,complexidade_operacional,potencial_upsell,score_total,risco_churn

Pontue cada dimensao 0/1/2 (0=negativo,1=neutro,2=positivo) com base em TODOS os sinais das ligacoes desse cliente no lote:
volume=frota estavel/crescendo vs devolucao sem reposicao | adimplencia=faturas em dia vs atraso/risco bloqueio
fidelidade=confirma exclusividade vs menciona concorrente/compara preco | engajamento=responde rapido/acessa portal vs dificil contatar
complexidade_operacional=poucos problemas recorrentes(2) vs multiplos problemas sistemicos(0) | potencial_upsell=abertura para produto novo(2) vs frota estagnada sem abertura(0)
score_total: soma das 6 dimensoes (0-12) | risco_churn: baixo|medio|alto

### CSV-P8 (Objecoes) — uma linha por objecao identificada (pode haver 0 a N por ligacao; se a ligacao nao teve objecao, nao gere linha para ela)
cliente_id,data,tipo_objecao,resposta_vendedor_codigo,eficacia,desfecho_da_objecao

tipo_objecao: OB1=preco/valor | OB2=prazo/adiamento | OB3=demanda baixa | OB4=produto inadequado | OB5=problema nao resolvido | OB6=burocracia/aprovacao | OB7=indisponibilidade
resposta_vendedor_codigo: R1=validou e explorou | R2=usou dado do cliente | R3=criou urgencia | R4=posicionou como aliado | R5=capitulou sem explorar | R6=argumentou sem ouvir
eficacia: alta|media|baixa | desfecho_da_objecao: superada|adiada|perdida

### CSV-P11 (Inteligencia Competitiva) — uma linha por sinal competitivo identificado (0 a N por ligacao; sem sinal = sem linha)
cliente_id,data,tipo_sinal,concorrente_mencionado,vendedor_explorou

tipo_sinal: IC1=mencao direta a concorrente | IC2=confirmacao de exclusividade | IC3=historico de migracao | IC4=frota propria revelada | IC5=comparacao implicita(sem citar empresa) | IC6=vendedor sondou ativamente | IC7=risco competitivo detectado(cliente aberto a avaliar alternativas)
concorrente_mencionado: unidas|movida|localfrio|ouro_verde|outro|nenhum
vendedor_explorou: SIM|NAO|nao_aplicavel

IMPORTANTE: processe TODOS os {len(trans.split('=== LIGACAO'))-1} clientes/ligacoes do lote. Retorne P4 completo (1 linha por cliente), depois P8 completo, depois P11 completo. Sem explicacoes.

LIGACOES:
{trans}"""


def prompt_p13_p15(trans):
    return f"""Voce e pesquisador de comportamento comercial B2B e analista de Revenue Intelligence.
{CONTEXTO}

Seu trabalho NAO e validar taxonomias ja existentes (B1-B10, CH1-CH7, OP1-OP8, AB1-AB5, FC1-FC5 ja estao cobertos em outros prompts).
Procure padroes RECORRENTES e eventos RAROS de alto impacto que NAO estao capturados por essas taxonomias.

### CSV-P13 (Padroes Emergentes) — so inclua padroes que se repetem em VARIAS ligacoes do lote (nao eventos isolados)
categoria,codigo,descricao,frequencia_estimada,impacto_potencial,clientes_exemplo

categoria: S1=comportamento inesperado do vendedor | S2=comportamento recorrente do cliente | S3=assunto recorrente sem categoria atual | S4=sinal fraco recorrente
codigo: [categoria]-[numero sequencial no lote, ex: S1-01]
frequencia_estimada: numero aproximado de ocorrencias no lote | impacto_potencial: alto|medio|baixo
clientes_exemplo: 2-3 cliente_id separados por ";" onde o padrao apareceu

### CSV-P15 (Eventos Raros de Alto Impacto) — eventos que aparecem POUCAS vezes mas tem impacto desproporcional (nao repita algo ja listado no P13)
cliente_id,data,categoria,evento_raro,impacto_potencial,acao_recomendada

categoria: R1=expansao(contratacao,nova filial,crescimento de frota,novo contrato) | R2=churn(ameaca explicita de saida,insatisfacao recorrente) | R3=inteligencia competitiva(migracao de fornecedor,teste com concorrente) | R4=influencia(indicacao oferecida,contato apresentado) | R5=mudanca estrutural(fusao,aquisicao,troca de gestor)
impacto_potencial: alto|medio|baixo

Se o lote nao tiver nenhum padrao emergente relevante ou evento raro, retorne as duas tabelas so com o cabecalho (sem linhas) — nao invente para preencher.

IMPORTANTE: analise o lote inteiro de uma vez (nao ligacao por ligacao) antes de responder. Retorne P13 completo, depois P15 completo. Sem explicacoes.

LIGACOES:
{trans}"""


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

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    global calls_made

    log("Carregando novo lote...")
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    n = len(data)
    size = BATCH_SIZE
    batches = atribuir_batches(data, size)
    n_bat = len(batches)

    log(f"Total: {n} clientes | {n_bat} batches de ~{size} clientes (indice estavel em {BATCH_INDEX_PATH.name})")
    log(f"Grupos priority: {GRUPOS_PRIORITY}")
    log(f"Chamadas max hoje: {MAX_CALLS} | max_output_tokens: {MAX_OUTPUT_TOKENS}")
    log(f"Output dir: {OUTPUT_DIR}")
    log("")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    todos_prontos = True

    grupos_funcs = {
        "P1_P2": prompt_p1_p2,
        "P5_P6": prompt_p5_p6,
        "P9_P10": prompt_p9_p10,
        "P3_P7": prompt_p3_p7,
        "P4_P8_P11": prompt_p4_p8_p11,
        "P13_P15": prompt_p13_p15,
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
                # divide em quantos pedacos forem necessarios (nao so 2) —
                # lotes de JULHO tem distribuicao de ligacoes/cliente muito mais
                # desigual que o novo_lote (ex: batch01 tinha 744 ligacoes,
                # um split em 2 ainda estourava o limite de tokens/min)
                # bin-packing guloso por CONTAGEM DE LIGACOES (nao por numero de
                # clientes) — clientes tem volume de ligacoes muito desigual
                # entre si, dividir a lista de clientes em partes iguais nao
                # garante partes com ligacoes equilibradas
                partes = []
                parte_atual = {}
                lig_atual = 0
                for cid, ligacoes in batch_data.items():
                    if lig_atual + len(ligacoes) > MAX_LIG_PER_CALL and parte_atual:
                        partes.append(parte_atual)
                        parte_atual = {}
                        lig_atual = 0
                    parte_atual[cid] = ligacoes
                    lig_atual += len(ligacoes)
                if parte_atual:
                    partes.append(parte_atual)
                log(f"  Batch {b_idx:02d}/{n_bat} [{grupo}] - {n_lig} ligacoes (grande) | dividido em {len(partes)} chamadas ({calls_made+1}-{calls_made+len(partes)}/{MAX_CALLS})")
                resultados = []
                for i, parte in enumerate(partes, 1):
                    n_lig_parte = sum(len(v) for v in parte.values())
                    log(f"    parte {i}/{len(partes)} - {n_lig_parte} ligacoes")
                    r = chamar_gemini(fn(formatar_ligacoes(parte)))
                    if quota_exhausted:
                        log("Rode novamente mais tarde/amanha.")
                        todos_prontos = False
                        return
                    if r is None or r.startswith("[ERRO:"):
                        log(f"    parte {i}/{len(partes)} falhou — batch {b_idx:02d} sera reprocessado na proxima execucao")
                        resultados = None
                        break
                    resultados.append(r)
                    if calls_made >= MAX_CALLS:
                        log(f"Limite de {MAX_CALLS} chamadas atingido. Rode novamente amanha.")
                        todos_prontos = False
                        return
                    if i < len(partes):
                        log(f"    aguardando {SLEEP_ENTRE_CHAMADAS}s (limite de tokens/min do free tier)...")
                        time.sleep(SLEEP_ENTRE_CHAMADAS)
                if resultados is None:
                    continue
                resultado = "\n\n".join(resultados)
            else:
                log(f"  Batch {b_idx:02d}/{n_bat} [{grupo}] - {n_lig} ligacoes | chamada {calls_made+1}/{MAX_CALLS}")
                resultado = chamar_gemini(fn(formatar_ligacoes(batch_data)))
                if quota_exhausted:
                    log("Rode novamente mais tarde/amanha.")
                    todos_prontos = False
                    return

            nome_arquivo = f"batch{b_idx:02d}_{grupo}_{ts}.txt"
            salvar(nome_arquivo, resultado)
            log(f"    aguardando {SLEEP_ENTRE_CHAMADAS}s (limite de tokens/min do free tier)...")
            time.sleep(SLEEP_ENTRE_CHAMADAS)

    if todos_prontos:
        existente = sintese_existe()
        if existente:
            log(f"Sintese ja existe e e valida — pulando.")
        elif calls_made >= MAX_CALLS:
            log("Limite de chamadas atingido — sintese sera gerada na proxima execucao.")
        else:
            log("Todos os batches completos, mas sintese e opcional aqui (rode agregacao manualmente se necessario).")

    log("")
    log(f"Chamadas usadas hoje: {calls_made}/{MAX_CALLS}")
    log("Pronto.")

if __name__ == "__main__":
    main()
