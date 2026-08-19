"""
SCORING DE POTENCIAL COMERCIAL — LOCALIZA FROTA PJ (BASE JULHO)
===================================================
Copia adaptada de scripts/scoring_potencial.py — MESMA lógica/pesos, sem
alteração nenhuma no critério, apenas trocando a fonte de dados para a base
de Julho (pipeline diário incremental) e os caminhos de saída, para não
sobrescrever os resultados de Junho e permitir comparação lado a lado.

Avalia cada ligação em múltiplas dimensões extraídas do framework de 15 prompts.
Sem LLM — 100% determinístico e auditável.

Output:
  JULHO/scoring_potencial_julho.csv      — linha por ligação, todos os campos
  JULHO/scoring_distribuicao_julho.txt   — relatório executivo de distribuição
"""

import json
import re
from pathlib import Path
from datetime import datetime
from collections import Counter, defaultdict

# ---------------------------------------------------------------------------
# CAMINHOS DOS ARQUIVOS
# ---------------------------------------------------------------------------
FILE_PATH  = Path(__file__).parent.parent / "JULHO" / "dados_convertidos" / "julho_completo.json"
OUTPUT_DIR = Path(__file__).parent.parent / "JULHO"


# ===========================================================================
# DICIONÁRIOS DE SINAIS
# ===========================================================================
# Cada dicionário abaixo é a lista exata de palavras que buscamos na transcrição.
# São auditáveis: qualquer pessoa pode ler e entender o que o script detecta.
# A lógica é simples: se essas palavras aparecem no contexto certo, o
# comportamento foi detectado. Se não aparecem, não foi.
# ===========================================================================


# ---------------------------------------------------------------------------
# SINAIS DE ABERTURA DA LIGAÇÃO (Framework P9 — AB1 a AB5)
#
# O tipo de abertura importa porque define o tom da ligação.
# AB1 (contextualizada) é a mais eficaz: o vendedor chega com informação,
# não como um estranho. O cliente percebe que o vendedor conhece o histórico.
# ---------------------------------------------------------------------------

# AB1 — Abertura CONTEXTUALIZADA: vendedor menciona algo específico do cliente
# "Vi aqui", "no seu contrato", "você já alugou com a gente" = vendedor preparado
# Ligações com abertura contextualizada têm maior chance de o cliente ouvir.
SINAIS_ABERTURA_CONTEXTUAL = [
    "vi aqui", "no seu cadastro", "no seu histórico", "no seu contrato",
    "você já", "vocês já", "última vez", "contrato anterior", "no sistema aqui",
    "já é cliente", "já alugaram", "já utilizaram", "desde que",
    "acompanhando sua conta", "seu cadastro", "sua conta aqui",
    "você me ligou antes", "você entrou em contato",
]

# AB2 — Abertura RELACIONAL: vendedor usa o nome e cria conexão pessoal
# "Oi [nome], como você está?" — mais informal, mas humaniza a ligação
SINAIS_ABERTURA_RELACIONAL = [
    "como você está", "como vai", "tudo bem com você", "tudo certo",
    "como estão as coisas", "muito tempo", "faz tempo",
]

# AB3 — Abertura GENÉRICA: não contextualiza, não personaliza
# "Em que posso ajudar?" = o cliente sabe que o vendedor não sabe nada sobre ele
SINAIS_ABERTURA_GENERICA = [
    "em que posso ajudar", "posso ajudar", "como posso te ajudar",
    "aqui é da localiza", "central de atendimento", "setor comercial",
]

# AB5 — Abertura DE PROTEÇÃO: ligar apenas para "manter o cadastro ativo"
# É a abertura mais fraca — o vendedor não tem objetivo comercial claro,
# e o cliente percebe isso. Resultado: quase nunca gera negócio.
SINAIS_ABERTURA_PROTECAO = [
    "manter o cadastro ativo", "cadastro ativo", "verificar o cadastro",
    "confirmar os dados", "atualizar o cadastro", "o cadastro de vocês",
    "para não perder o cadastro", "não tivemos o prazer", "ainda não nos utilizaram",
]


# ---------------------------------------------------------------------------
# SINAIS DE FECHAMENTO (Framework P9 — FC1 a FC5)
#
# O fechamento é o comportamento com maior impacto isolado no resultado.
# A diferença entre "qualquer coisa me chama" (FC3) e "te ligo terça às 10"
# (FC1) define se há continuidade ou se a oportunidade vai para o arquivo morto.
# ---------------------------------------------------------------------------

# FC1 — COMPROMISSO DUPLO: tanto vendedor quanto cliente assumem um próximo passo
# com data e horário definidos. É o fechamento mais eficaz e o mais raro:
# apareceu apenas 5 vezes em toda a base analisada.
# Detectamos palavras que indicam que AMBOS assumiram compromisso.
SINAIS_FC1_VENDEDOR = [
    "te ligo na", "te ligo amanhã", "te ligo segunda", "te ligo terça",
    "te ligo quarta", "te ligo quinta", "te ligo sexta",
    "retorno amanhã", "retorno na segunda", "entro em contato amanhã",
    "você me confirma até", "você me responde até", "me dá um retorno até",
    "aguardo seu retorno até", "preciso da sua resposta até",
    "vamos fazer o seguinte", "combinado então", "fica assim então",
    "deixa agendado para", "agenda para",
]

SINAIS_FC1_CLIENTE = [
    # Palavras do CLIENTE que indicam que ele também assumiu um compromisso
    "amanhã eu te ligo", "amanhã eu retorno", "segunda eu falo",
    "vou pensar e te dou retorno", "te respondo até", "vou confirmar até",
    "pode ligar amanhã", "combinado", "tá bom, amanhã",
]

# FC2 — PRÓXIMO PASSO SÓ DO VENDEDOR: apenas o vendedor age, cliente não comprometeu
# "Vou te mandar a proposta" sem o cliente assumir quando vai responder.
SINAIS_FC2 = [
    "vou te mandar", "vou enviar", "te mando hoje", "mando por e-mail",
    "mando no whatsapp", "te passo o contato", "deixo meu número",
]

# FC3 — FECHAMENTO VAGO: "qualquer coisa me chama" — sem próximo passo, sem prazo
# Este é o padrão dominante do time. Toda ligação que termina assim
# vai para o arquivo morto. O cliente não tem razão para voltar a ligar.
SINAIS_FC3 = [
    "qualquer coisa me chama", "surgindo demanda", "pode nos procurar",
    "à disposição", "qualquer necessidade", "qualquer dúvida me fala",
    "pode me ligar quando precisar", "estou à sua disposição",
    "se precisar é só ligar", "qualquer coisa pode entrar em contato",
    "pode me acionar", "fico à disposição",
]

# FC5 — FECHAMENTO DIRETIVO: vendedor diz claramente o que o cliente precisa fazer
# "Preciso da CNH e CNPJ até as 16h" — direto, sem margem para postergar.
SINAIS_FC5 = [
    "preciso que você envie", "preciso receber", "você precisa mandar",
    "necessário que você", "para eu dar andamento você precisa",
    "só consigo fechar se", "para garantir você precisa",
]


# ---------------------------------------------------------------------------
# SINAIS DE DIAGNÓSTICO (Framework P1 — B1, peso=2)
#
# Vendedor que faz diagnóstico antes de apresentar preço fecha mais.
# Os dados mostraram +43,1pp de diferença entre quem faz e quem não faz.
# Buscamos perguntas de contexto: cidade, período, modelo, km, quem usa.
# ---------------------------------------------------------------------------
SINAIS_DIAGNOSTICO = [
    "como está", "como é que", "qual é a", "quanto roda", "tem demanda",
    "como funciona", "tem alguma", "como que vocês", "qual seria", "tem interesse",
    "quais são", "como vocês", "quantos carros", "qual é a necessidade",
    "me conta", "me fala um pouco", "como está a frota",
    "qual cidade", "a partir de quando", "por quanto tempo",
    "qual modelo", "quantos km", "quem vai usar", "para quantos colaboradores",
    "qual a demanda", "como é a operação de vocês",
]

# ---------------------------------------------------------------------------
# DENSIDADE DE PERGUNTAS (proxy de B1)
#
# Uma forma de medir diagnóstico sem IA: simplesmente contar quantas perguntas
# (marcadas com "?") o vendedor fez. Vendedor que fecha faz mais perguntas.
# Isso não é opinião — é o que os dados confirmaram.
# Um vendedor que pergunta pouco está monologando; um que pergunta muito está
# entendendo o cliente antes de propor. A lógica é intuitiva.
# ---------------------------------------------------------------------------
# (sem dicionário aqui — detectado contando "?" nos turnos do vendedor)


# ---------------------------------------------------------------------------
# SINAIS DE URGÊNCIA (Framework P1 — B6, peso=3)
#
# Urgência com FATO VERIFICÁVEL é o terceiro maior preditor de fechamento.
# A diferença de "urgência real" vs "urgência inventada":
#   Real:     "seu contrato vence em 15 dias"
#   Inventada: "temos uma promoção especial só hoje" (sem embasamento)
# Buscamos palavras que indicam prazo real, não promoção genérica.
# ---------------------------------------------------------------------------
SINAIS_URGENCIA = [
    "hoje", "amanhã", "prazo", "vence", "último dia", "agora mesmo",
    "essa semana", "antes que", "só até", "contrato encerra",
    "data limite", "renovar agora", "fechar ainda hoje",
    "disponibilidade limitada", "último disponível", "só tem",
    "a tabela vai subir", "reajuste em", "preço vai mudar",
]


# ---------------------------------------------------------------------------
# SINAIS DE SONDAGEM DE CONCORRENTE / FROTA PRÓPRIA (Framework P1 — B10, peso=3)
#
# Este é o comportamento com MAIOR correlação com fechamento nos dados:
# +54,9pp de diferença entre quem pergunta e quem não pergunta.
# Quando o vendedor pergunta sobre frota própria ou outros fornecedores,
# ele consegue contextualizar a proposta e rebater com dado real.
# Quando não pergunta, propõe no escuro.
# ---------------------------------------------------------------------------
SINAIS_SONDAGEM_CONCORRENTE = [
    "outra locadora", "frota própria", "tem frota", "outra empresa de locação",
    "usa alguma outra", "aluga em outro lugar", "tem veículo próprio",
    "tem carro próprio", "movida", "unidas", "móvel locadora",
    "outros fornecedores", "trabalham com outras", "tem parceria com",
    "além da localiza", "além de nós", "além das locações com a gente",
    "frota de vocês", "carro zero", "assinatura de veículo",
]


# ---------------------------------------------------------------------------
# SINAIS DE UPSELL CONECTADO À DOR (Framework P1 — B5, peso=2)
#
# B5 é o único comportamento com 0% nos não-fechamentos: toda vez que
# o vendedor conectou um produto à dor real do cliente, converteu.
# Buscamos menção a produtos específicos no discurso do VENDEDOR —
# não é upsell genérico ("temos outros produtos"), é upsell conectado
# a uma necessidade revelada na ligação.
# ---------------------------------------------------------------------------
SINAIS_UPSELL = [
    "proteção total", "proteção adicional", "cobertura total",
    "telemetria", "rastreamento", "gestão de frota",
    "upgrade", "categoria superior", "carro maior", "carro melhor",
    "quilometragem maior", "pacote de km",
    "plano mensal ao invés", "contrato anual", "contrato fixo",
    "elétrico", "híbrido", "veículo pesado", "caminhão", "localiza pesados",
    "seguro adicional", "assistência 24h",
    "webcorp", "portal de gestão", "acesso multiusuário",
]


# ---------------------------------------------------------------------------
# SINAIS DE HISTÓRICO DO CLIENTE (Framework P1 — B3, peso=2)
#
# Vendedor que referencia informações anteriores demonstra que o cliente
# não é um número — é uma conta com histórico. Isso gera credibilidade
# e reduz o atrito para continuar a conversa.
# ---------------------------------------------------------------------------
SINAIS_HISTORICO = [
    "vi aqui", "no cadastro", "no seu histórico", "na nossa base", "você já",
    "vocês já alugaram", "faz tempo que", "última vez que", "contrato anterior",
    "no sistema aqui", "já é cliente", "desde", "você me ligou",
    "você entrou em contato antes", "na sua última locação",
    "no contrato anterior de vocês", "o seu contrato de",
]


# ---------------------------------------------------------------------------
# SINAIS DE ALERTA DE RISCO (Framework P1 — B4, peso=2)
#
# Vendedor que alerta o cliente sobre um risco real cria urgência verdadeira.
# Não é manipulação — é informação que o cliente precisa e não tinha.
# Exemplo: "se não renovarmos agora, o contrato vira diária avulsa — 40% mais caro"
# ---------------------------------------------------------------------------
SINAIS_ALERTA = [
    "fique atento", "cuidado com", "antes que", "se não renovar", "risco de",
    "pode gerar multa", "vai cobrar", "vai perder", "importante que",
    "precisa ficar sabendo", "atenção para",
    "se não fizer agora", "corre o risco de", "pode impactar",
    "não vai conseguir", "pode perder a disponibilidade",
]


# ---------------------------------------------------------------------------
# SINAIS DE CHALLANGER — CUSTO OCULTO (Framework P5 — CH1)
#
# CH1 é revelar um custo que o cliente não estava calculando.
# "O preço deles parece menor, mas na hora do sinistro..." = CH1.
# Quando o vendedor usa esse argumento, muda a percepção do cliente
# sobre o que é "mais barato". É uma técnica de reframing de preço.
# ---------------------------------------------------------------------------
SINAIS_CH1_CUSTO_OCULTO = [
    "mas o que acontece", "na hora do sinistro", "sem a cobertura",
    "taxa de operação", "custo real", "conta tudo",
    "km excedente", "vai cobrar", "não está incluso neles",
    "você vai pagar por fora", "no final fica mais caro",
    "quando calcular tudo", "custo total", "cobertura deles",
    "o que eles não falam", "o que está escondido",
    "frota própria tem custo de", "ipva", "depreciação", "manutenção própria",
]

# ---------------------------------------------------------------------------
# SINAIS DE ANTECIPAÇÃO DE PROBLEMA (Framework P5 — CH6)
#
# CH6 é alertar o cliente sobre um problema que ele ainda não percebeu.
# "Com esse crescimento de motoristas, seu km vai estourar em setembro"
# = vendedor que pensa pelo cliente. Gera confiança e urgência real.
# ---------------------------------------------------------------------------
SINAIS_CH6_ANTECIPACAO = [
    "vai estourar", "vai ultrapassar", "logo você vai precisar",
    "com esse crescimento", "no ritmo que", "projetando",
    "antes que vire um problema", "antes que aconteça",
    "evitar que", "prevenir", "antes que você perceba",
    "alta temporada", "período de alta demanda", "disponibilidade vai cair",
    "prazo de entrega aumenta", "vai faltar carro",
]


# ---------------------------------------------------------------------------
# SINAIS DE OBJEÇÃO DE PREÇO (detectados no discurso do CLIENTE)
#
# Objeção de preço é a mais comum nas vendas B2B de locação.
# Precisamos saber QUANDO o cliente faz a objeção para verificar
# se o vendedor respondeu com argumento (rebuttal) ou capitulou.
# ---------------------------------------------------------------------------
SINAIS_OBJECAO_PRECO = [
    "está caro", "muito caro", "tá caro", "achei caro",
    "mais barato", "mais em conta", "outro lugar mais barato",
    "concorrente mais barato", "movida mais barata", "unidas mais barata",
    "desconto", "não tenho esse orçamento", "está fora do orçamento",
    "não consigo pagar", "preciso de um desconto", "tem como baixar",
    "não cabe no budget", "valor alto", "preço alto",
]

# SINAIS DE REBUTTAL — resposta do vendedor à objeção com argumento real
# Quando o vendedor responde com DADO (não com "vou ver o que posso fazer"),
# ele tem muito mais chance de converter. Capitular em silêncio = perda certa.
SINAIS_REBUTTAL = [
    "mas olha", "se você calcular", "comparando", "na verdade",
    "o que acontece", "mas considera", "inclui", "está incluso",
    "sem custo adicional", "já está no preço",
    "a diferença é", "no total fica", "quando conta",
    "o custo real", "taxa de operação", "você vai economizar",
    "se comparar com frota própria", "com manutenção inclusa",
    "sem franquia", "sem custo de sinistro", "você não vai pagar",
]


# ---------------------------------------------------------------------------
# SINAIS DE PROMESSA (Framework P10)
#
# Toda promessa que o vendedor faz é um compromisso com o cliente.
# Promessa SEM prazo = alto risco de não ser cumprida = perda de confiança.
# Promessa COM prazo = o cliente sabe quando esperar = confiança mantida.
# Buscamos: (a) a promessa, (b) se tem uma data/prazo próxima a ela.
# ---------------------------------------------------------------------------
SINAIS_PROMESSA = [
    "vou te mandar", "vou enviar", "te ligo", "vou verificar", "vou resolver",
    "vou contestar", "vou fazer", "vou entrar em contato", "vou solicitar",
    "providencio", "vou checar", "vou confirmar", "vou falar com",
    "vou acionar", "vou escalar", "vou tratar", "vou retornar",
]

# Palavras que indicam prazo numa promessa — se aparecem junto com a promessa,
# ela tem deadline; se não aparecem, é promessa no ar.
SINAIS_PRAZO_PROMESSA = [
    "hoje", "amanhã", "agora", "em seguida", "em breve",
    "até segunda", "até terça", "até quarta", "até quinta", "até sexta",
    "essa semana", "até o final do dia", "até as", "até meio-dia",
    "até as 17", "até as 18", "até as 16", "até as 15",
    "em 24 horas", "em 48 horas", "até o fim do dia",
]


# ---------------------------------------------------------------------------
# SINAIS COMPETITIVOS mencionados pelo CLIENTE (Framework P11)
#
# Quando o CLIENTE menciona um concorrente, é um sinal de alerta:
# ou ele está avaliando alternativas, ou já tem proposta de outro lugar.
# O vendedor que detecta e responde a isso defende o contrato.
# O vendedor que ignora perde a conta sem saber por quê.
# ---------------------------------------------------------------------------
SINAIS_COMPETITIVO_CLIENTE = [
    "unidas", "movida", "móvel", "hertz", "avis", "localfrio",
    "outra locadora", "frota própria", "carro próprio", "veículo próprio",
    "outro fornecedor", "outra empresa", "mais barato em outro",
    "carro zero", "assinatura de carro", "programa de assinatura",
    "comprar um carro", "financiamento de carro",
]


# ---------------------------------------------------------------------------
# SINAIS DE EXPANSÃO DO CLIENTE (Framework P15 — R1)
#
# Cliente que sinaliza crescimento tem mais veículos para locar.
# Essa é a oportunidade mais valiosa: não é converter novo cliente,
# é expandir conta que já existe. Custo de aquisição zero.
# ---------------------------------------------------------------------------
SINAIS_EXPANSAO = [
    "nova filial", "nova unidade", "abrindo", "expandindo", "crescendo",
    "mais carros", "mais veículos", "novos funcionários", "novo contrato",
    "nova obra", "nova região", "contratação", "nova equipe",
    "aumentar frota", "precisar de mais", "ampliar", "novos projetos",
    "ganhamos uma licitação", "novo cliente nosso", "nova operação",
]

# ---------------------------------------------------------------------------
# SINAIS DE CHURN (Framework P15 — R2)
#
# Cliente que sinaliza saída é prioridade máxima de retenção.
# Esses sinais raramente aparecem de forma explícita — quando aparecem,
# o vendedor precisa agir imediatamente. Ignorar = perder a conta.
# ---------------------------------------------------------------------------
SINAIS_CHURN = [
    "cancelar", "não vou mais", "vai cortar", "excluir a localiza",
    "não tenho interesse", "vou devolver tudo", "encerrar contrato",
    "desistir", "resolver em outro lugar", "não vou renovar",
    "estou pensando em encerrar", "quero cancelar", "rescindir",
    "devolução de frota", "reduzir frota", "cortar custos",
]

# ---------------------------------------------------------------------------
# SINAIS OPERACIONAIS (ligação de suporte puro — Framework P2)
#
# Ligação com muitos sinais operacionais e ZERO sinais comerciais = suporte puro.
# Isso representa 62% das ligações na base. Não é que não tinha oportunidade —
# é que o vendedor tratou como suporte e não tentou nada comercial.
# ---------------------------------------------------------------------------
SINAIS_OPERACIONAL = [
    "biometria", "senha", "acesso", "portal fora", "boleto", "avaria",
    "oficina", "sinistro", "multa de infração", "condutor",
    "fatura incorreta", "bloqueio", "manutenção", "nota fiscal",
    "documento", "cnh", "contrato de locação", "termo de uso",
    "devolução", "entrega do carro", "retirada do carro",
    "troca de carro", "carro com defeito", "guincho",
]

# ---------------------------------------------------------------------------
# SINAIS COMERCIAIS (Framework P2 — natureza da ligação)
#
# Palavras que indicam que ALGUMA atividade comercial aconteceu na ligação.
# Se o vendedor disse essas palavras, pelo menos tentou. Se não disse, não tentou.
# ---------------------------------------------------------------------------
SINAIS_COMERCIAL = [
    "proposta", "valor", "cotação", "desconto", "renovar", "migrar",
    "contrato", "reserva", "fechar", "locação", "mensal", "diário",
    "tabela de preços", "simulação", "orçamento", "disponibilidade",
    "quilometragem", "plano", "categoria", "modelo disponível",
]

# ---------------------------------------------------------------------------
# PRODUTOS MENCIONADOS (Framework P7 — cross-selling)
#
# A Localiza tem mais de 12 produtos no portfólio B2B.
# A maioria dos vendedores oferta apenas 2-3. Mapeamos quais produtos
# foram mencionados para identificar onde estão as oportunidades perdidas.
# ---------------------------------------------------------------------------
SINAIS_PRODUTOS = {
    "telemetria":     ["telemetria", "rastreamento", "gestão de frota", "monitoramento"],
    "protecao_total": ["proteção total", "cobertura total", "sem franquia"],
    "eletrico":       ["elétrico", "híbrido", "ev", "veículo elétrico"],
    "pesados":        ["pesado", "caminhão", "localiza pesados", "van", "utilitário"],
    "mensal_fixo":    ["mensal fixo", "contrato fixo", "12 meses", "contrato anual"],
    "mensal_flex":    ["mensal flex", "flexível", "sem fidelidade", "sem multa"],
    "diario":         ["diária", "diário", "locação curta", "curta duração"],
    "webcorp":        ["webcorp", "portal", "plataforma", "gestão online"],
}


# ===========================================================================
# FUNÇÕES DE ANÁLISE
# ===========================================================================

def extrair_textos(call):
    """
    Separa a transcrição por speaker: tudo que o Vendedor (A) disse,
    tudo que o Cliente (C) disse, e a conversa completa.
    Também conta os turnos de fala de cada um.
    """
    conv = call.get("conversa", [])

    # Texto completo de cada speaker, em minúsculas para facilitar a busca
    texto_a = " ".join(t.lower() for s, t in conv if s == "A")
    texto_c = " ".join(t.lower() for s, t in conv if s == "C")
    full    = texto_a + " " + texto_c

    # Turnos = número de vezes que cada um falou (não o tamanho, apenas a vez)
    turns_a = sum(1 for s, _ in conv if s == "A")
    turns_c = sum(1 for s, _ in conv if s == "C")

    # Palavras = proxy melhor que turnos para medir quem dominou a conversa
    words_a = len(texto_a.split())
    words_c = len(texto_c.split())

    # Primeiro a falar = quem iniciou a ligação
    primeiro_speaker = conv[0][0] if conv else "?"

    return texto_a, texto_c, full, turns_a, turns_c, words_a, words_c, primeiro_speaker, conv


def conta_sinais(texto, lista):
    """Conta quantos sinais da lista aparecem no texto."""
    return sum(1 for s in lista if s in texto)


def tem_sinal(texto, lista):
    """Verifica se ao menos um sinal da lista aparece no texto."""
    return any(s in texto for s in lista)


def detectar_abertura(conv, texto_a):
    """
    Classifica o tipo de abertura da ligação olhando os primeiros turnos do vendedor.

    Por que os primeiros turnos? A abertura define o tom da ligação inteira.
    Um vendedor que abre com contexto do cliente (AB1) tem muito mais chance
    de o cliente ouvir do que um que abre com "em que posso ajudar?" (AB3).

    Olhamos apenas os primeiros 3 turnos do vendedor — depois disso,
    a conversa já foi estabelecida.
    """
    # Pega o texto dos primeiros turnos do vendedor
    primeiros_turnos_a = []
    count = 0
    for s, t in conv:
        if s == "A":
            primeiros_turnos_a.append(t.lower())
            count += 1
            if count >= 3:
                break
    abertura_texto = " ".join(primeiros_turnos_a)

    if tem_sinal(abertura_texto, SINAIS_ABERTURA_PROTECAO):
        return "AB5_protecao"       # Pior: "manter cadastro ativo"
    elif tem_sinal(abertura_texto, SINAIS_ABERTURA_GENERICA):
        return "AB3_generica"       # Fraca: "em que posso ajudar?"
    elif tem_sinal(abertura_texto, SINAIS_ABERTURA_CONTEXTUAL):
        return "AB1_contextual"     # Forte: usa histórico do cliente
    elif tem_sinal(abertura_texto, SINAIS_ABERTURA_RELACIONAL):
        return "AB2_relacional"     # Boa: cria conexão pessoal
    else:
        return "AB4_reativa"        # Neutra: reativa ao que o cliente trouxe


def detectar_fechamento(conv, texto_a, texto_c):
    """
    Classifica o tipo de fechamento olhando os últimos turnos da ligação.

    Por que os últimos turnos? O fechamento é o que fica na memória do cliente.
    Uma ligação ótima com um fechamento vago vai para o arquivo morto.
    Uma ligação mediana com um fechamento forte tem continuidade.

    Hierarquia de prioridade: FC1 > FC5 > FC2 > FC3 (FC4 = nenhum dos anteriores)
    """
    # Pega os últimos 5 turnos de cada speaker
    ultimos_a = []
    ultimos_c = []
    for s, t in reversed(conv):
        if s == "A" and len(ultimos_a) < 5:
            ultimos_a.append(t.lower())
        elif s == "C" and len(ultimos_c) < 5:
            ultimos_c.append(t.lower())
        if len(ultimos_a) >= 5 and len(ultimos_c) >= 5:
            break

    fechamento_a = " ".join(ultimos_a)
    fechamento_c = " ".join(ultimos_c)

    # FC1: compromisso dos DOIS lados — o mais raro e mais eficaz
    # Para ser FC1, tanto o vendedor quanto o cliente precisam ter assumido algo
    vendedor_assumiu = tem_sinal(fechamento_a, SINAIS_FC1_VENDEDOR)
    cliente_assumiu  = tem_sinal(fechamento_c, SINAIS_FC1_CLIENTE) or tem_sinal(fechamento_c, ["combinado", "pode ser", "tá bom", "certo", "ok"])

    if vendedor_assumiu and cliente_assumiu:
        return "FC1_compromisso_duplo"   # Melhor: ambos assumiram

    # FC5: vendedor diretivo — diz o que o cliente precisa fazer
    if tem_sinal(fechamento_a, SINAIS_FC5):
        return "FC5_diretivo"

    # FC2: só o vendedor tem próximo passo — cliente não assumiu nada
    if tem_sinal(fechamento_a, SINAIS_FC1_VENDEDOR) or tem_sinal(fechamento_a, SINAIS_FC2):
        return "FC2_so_vendedor"

    # FC3: fechamento vago — "qualquer coisa me chama"
    if tem_sinal(texto_a, SINAIS_FC3):
        return "FC3_vago"               # Pior: sem próximo passo

    return "FC4_aberto"                  # Nada definido


def calcular_densidade_perguntas(conv):
    """
    Conta quantas perguntas o vendedor fez durante toda a ligação.

    Por que isso importa? Perguntas são diagnóstico.
    Vendedor que faz muitas perguntas está entendendo o cliente.
    Vendedor que não pergunta está monologando.

    Dos dados: ligações que fecham têm densidade de perguntas maior.
    Medimos pela quantidade de "?" nos turnos do vendedor.
    """
    perguntas = 0
    turnos_vendedor = 0
    for s, t in conv:
        if s == "A":
            turnos_vendedor += 1
            perguntas += t.count("?")

    # Perguntas por turno: normaliza pelo tamanho da ligação
    densidade = round(perguntas / turnos_vendedor, 2) if turnos_vendedor > 0 else 0
    return perguntas, densidade


def detectar_objecao_e_rebuttal(conv):
    """
    Detecta se houve objeção de preço do cliente e se o vendedor respondeu
    com argumento (rebuttal) ou em silêncio/capitulação.

    Por que isso importa? Objeção não tratada é venda perdida.
    Mas não basta responder — precisa responder com DADO, não com
    "vejo o que posso fazer" (que é capitulação disfarçada).

    Lógica: buscamos a objeção no discurso do cliente e, nos 3 turnos
    seguintes do vendedor, buscamos palavras de argumento real.
    """
    objecao_detectada  = False
    rebuttal_detectado = False

    conv_list = list(conv)
    for i, (s, t) in enumerate(conv_list):
        # Cliente faz objeção de preço
        if s == "C" and tem_sinal(t.lower(), SINAIS_OBJECAO_PRECO):
            objecao_detectada = True

            # Vendedor responde nos próximos 3 turnos?
            proximos_turnos_vendedor = [
                txt.lower() for spk, txt in conv_list[i+1:i+7]
                if spk == "A"
            ][:3]

            if any(tem_sinal(turno, SINAIS_REBUTTAL) for turno in proximos_turnos_vendedor):
                rebuttal_detectado = True
                break

    return objecao_detectada, rebuttal_detectado


def detectar_promessa_sem_prazo(conv):
    """
    Verifica se o vendedor fez promessas SEM definir um prazo.

    Por que isso importa? Promessa sem prazo é promessa esquecida.
    "Vou te mandar" sem "hoje" ou "amanhã" = o cliente fica esperando
    sem saber quando. A confiança vai corroendo.

    Promessa COM prazo: "vou te mandar ainda hoje" = o cliente sabe.
    Promessa SEM prazo: "vou te mandar" = o cliente não sabe quando esperar.

    Contamos o número de promessas sem prazo — quanto maior, maior o risco.
    """
    promessas_sem_prazo = 0
    for s, t in conv:
        if s != "A":
            continue
        texto = t.lower()
        if tem_sinal(texto, SINAIS_PROMESSA):
            # Verifica se há algum prazo na mesma frase (janela de 60 caracteres)
            for sinal in SINAIS_PROMESSA:
                if sinal in texto:
                    pos = texto.find(sinal)
                    janela = texto[max(0, pos-20):pos+60]
                    if not tem_sinal(janela, SINAIS_PRAZO_PROMESSA):
                        promessas_sem_prazo += 1
    return promessas_sem_prazo


def detectar_fluxo_comercial(conv, texto_a):
    """
    Identifica em qual parte da ligação o vendedor fez a tentativa comercial.

    Por que isso importa? O timing importa tanto quanto o comportamento.
    Tentar vender no início, antes de resolver o problema do cliente, irrita.
    Tentar vender no meio, enquanto a conversa ainda está ativa, é ideal.
    Tentar vender apenas no final, quando o cliente já está encerrando, é tarde.
    Não tentar em nenhum momento = suporte puro.

    Dividimos a conversa em 3 partes iguais e detectamos onde apareceu
    o primeiro sinal comercial do vendedor.
    """
    turnos_total = len(conv)
    if turnos_total == 0:
        return "sem_conteudo"

    terco = max(1, turnos_total // 3)

    for i, (s, t) in enumerate(conv):
        if s == "A" and tem_sinal(t.lower(), SINAIS_COMERCIAL):
            if i < terco:
                return "inicio"   # Tentativa logo de cara — pode ser prematuro
            elif i < terco * 2:
                return "meio"     # Ideal: resolveu primeiro, depois tentou
            else:
                return "fim"      # Tardio: cliente já estava encerrando

    return "nao_detectado"    # Sem tentativa comercial identificada


def detectar_produtos_mencionados(full):
    """
    Identifica quais produtos do portfólio foram mencionados na ligação.

    Por que isso importa? A Localiza tem 12+ produtos B2B.
    A maioria dos vendedores menciona apenas 2-3. Saber quais foram
    mencionados vs quais poderiam ter sido mencionados (dado o contexto)
    é o insumo para treinamento de cross-selling (Framework P7).
    """
    mencionados = []
    for produto, sinais in SINAIS_PRODUTOS.items():
        if tem_sinal(full, sinais):
            mencionados.append(produto)
    return mencionados if mencionados else ["nenhum"]


def detectar_concorrente_explorado(conv):
    """
    Verifica se, quando o CLIENTE mencionou um concorrente, o VENDEDOR
    aproveitou para fazer diferenciação (CH1) ou ignorou.

    Por que isso importa? Quando o cliente fala de outro fornecedor,
    é uma abertura para o vendedor posicionar a Localiza.
    Ignorar = deixar o cliente com a impressão de que a alternativa é viável.
    Usar = transformar a menção em argumento de venda.
    """
    cliente_mencionou_concorrente = False
    vendedor_explorou = False

    conv_list = list(conv)
    for i, (s, t) in enumerate(conv_list):
        if s == "C" and tem_sinal(t.lower(), SINAIS_COMPETITIVO_CLIENTE):
            cliente_mencionou_concorrente = True

            # Nos próximos 5 turnos do vendedor, usou argumento de CH1?
            proximos_a = [
                txt.lower() for spk, txt in conv_list[i+1:i+10]
                if spk == "A"
            ][:5]

            if any(tem_sinal(turno, SINAIS_CH1_CUSTO_OCULTO + SINAIS_REBUTTAL) for turno in proximos_a):
                vendedor_explorou = True
                break

    return cliente_mencionou_concorrente, vendedor_explorou


# ===========================================================================
# FUNÇÃO PRINCIPAL DE SCORING
# ===========================================================================

def avaliar_ligacao(client_id, call):
    """
    Avalia uma ligação e retorna TODOS os campos de análise.

    ESTRUTURA DO SCORE (0-30 pontos):
      Dimensão 1 — CONTEXTO (0-10):   "Havia ambiente para ação comercial?"
      Dimensão 2 — CLIENTE   (0-10):  "O cliente revelou oportunidade?"
      Dimensão 3 — VENDEDOR  (0-10):  "O vendedor aplicou os comportamentos certos?"

    Além do score, retornamos análises qualitativas que o CSV captura:
    abertura, fechamento, objeção, promessas, produtos, fluxo, talk ratio.
    """
    texto_a, texto_c, full, turns_a, turns_c, words_a, words_c, primeiro, conv = extrair_textos(call)
    duracao = call.get("duracao", 0)

    score_contexto  = 0
    score_cliente   = 0
    score_vendedor  = 0
    razoes          = []
    penalidades     = []
    sinais_detectados = {}

    # -----------------------------------------------------------------------
    # ANÁLISES QUALITATIVAS (não entram direto no score, mas enriquecem o CSV)
    # -----------------------------------------------------------------------

    tipo_abertura   = detectar_abertura(conv, texto_a)
    tipo_fechamento = detectar_fechamento(conv, texto_a, texto_c)
    n_perguntas, densidade_perguntas = calcular_densidade_perguntas(conv)
    objecao_detectada, rebuttal_detectado = detectar_objecao_e_rebuttal(conv)
    promessas_sem_prazo = detectar_promessa_sem_prazo(conv)
    fluxo_comercial = detectar_fluxo_comercial(conv, texto_a)
    produtos_mencionados = detectar_produtos_mencionados(full)
    concorrente_cliente, concorrente_explorado = detectar_concorrente_explorado(conv)

    # Contagens para o relatório
    n_op  = conta_sinais(full, SINAIS_OPERACIONAL)
    n_com = conta_sinais(texto_a, SINAIS_COMERCIAL)
    sinais_detectados["comercial_count"]    = n_com
    sinais_detectados["operacional_count"]  = n_op
    sinais_detectados["concorrente_cliente"] = concorrente_cliente

    # -----------------------------------------------------------------------
    # DIMENSÃO 1 — CONTEXTO (0-10)
    # "Esta ligação tinha ambiente favorável para ação comercial?"
    #
    # Não é sobre o que o vendedor fez — é sobre o contexto da ligação.
    # Uma ligação de 15 minutos tem muito mais espaço para comercial
    # do que uma de 30 segundos. Uma ligação iniciada pelo vendedor
    # indica intenção comercial já na origem.
    # -----------------------------------------------------------------------

    # D1.1 — DURAÇÃO: proxy de profundidade da conversa
    # Ligações longas permitem diagnóstico, argumento e fechamento.
    # Ligações curtas raramente têm espaço para comportamento comercial.
    # Os thresholds vêm da observação da base: ligações que fecharam
    # têm duração média bem acima das que não fecharam.
    if duracao >= 600:
        score_contexto += 4
        razoes.append("[D1] Duração >10 min → espaço amplo para diagnóstico e negociação")
    elif duracao >= 300:
        score_contexto += 3
        razoes.append("[D1] Duração >5 min → conversa substantiva com múltiplos temas")
    elif duracao >= 120:
        score_contexto += 2
        razoes.append("[D1] Duração >2 min → conteúdo suficiente para análise")
    elif duracao >= 30:
        score_contexto += 1
        razoes.append("[D1] Duração curta mas com conteúdo mínimo detectável")
    else:
        penalidades.append("[D1] Duração <30s → ligação superficial ou sem conteúdo real")

    # D1.2 — QUEM INICIOU: vendedor proativo vs cliente reativo
    # Vendedor que liga com intenção comercial (B8) já está no modo certo.
    # Cliente que liga geralmente está em modo de suporte — contexto diferente.
    if primeiro == "A":
        score_contexto += 2
        razoes.append("[D1] Vendedor iniciou a ligação com intenção comercial (B8)")
    else:
        score_contexto += 1
        razoes.append("[D1] Cliente iniciou — contexto aproveitável mas reativo")

    # D1.3 — NATUREZA DA LIGAÇÃO: comercial vs operacional
    # Ligação cheia de sinais operacionais (biometria, boleto, sinistro) e zero
    # sinais comerciais = suporte puro. Aqui está o risco de desperdiçar tempo
    # do vendedor em chamadas que não tinham potencial comercial nenhum.
    if n_com >= 3:
        score_contexto += 4
        razoes.append(f"[D1] {n_com} sinais comerciais claros no discurso do vendedor")
    elif n_com >= 1:
        score_contexto += 2
        razoes.append(f"[D1] {n_com} sinal(is) comercial(is) detectado(s) — tentativa parcial")
    elif n_op >= 3 and n_com == 0:
        score_contexto -= 2
        penalidades.append(f"[D1] Suporte puro: {n_op} sinais operacionais, 0 comerciais (oportunidade perdida)")

    score_contexto = max(0, min(10, score_contexto))

    # -----------------------------------------------------------------------
    # DIMENSÃO 2 — SINAIS DO CLIENTE (0-10)
    # "O cliente revelou alguma oportunidade que justifica ação?"
    #
    # Aqui buscamos sinais no discurso do CLIENTE — não do vendedor.
    # Expansão, churn, menção de concorrente, dores — tudo isso são
    # informações que o cliente deu, conscientemente ou não.
    # -----------------------------------------------------------------------

    # D2.1 — EXPANSÃO: cliente está crescendo
    # É a oportunidade mais valiosa: conta que já existe querendo mais.
    # Zero custo de aquisição — é só saber perguntar.
    if tem_sinal(texto_c, SINAIS_EXPANSAO):
        score_cliente += 4
        razoes.append("[D2] Cliente sinalizou expansão ou crescimento → oportunidade de receita nova (P15-R1)")
        sinais_detectados["expansao"] = True

    # D2.2 — CONCORRENTE mencionado pelo cliente
    # Cliente que cita outro fornecedor está avaliando alternativas.
    # Cada menção de concorrente é uma janela de diferenciação.
    if concorrente_cliente:
        score_cliente += 3
        razoes.append("[D2] Cliente mencionou concorrente ou frota própria → janela de diferenciação (P11)")

        # Bônus se o vendedor aproveitou; penalidade se ignorou
        if concorrente_explorado:
            score_vendedor += 1   # Conta como bônus no D3 também
            razoes.append("[D2+D3] Vendedor explorou a menção de concorrente com argumento (CH1)")
        else:
            penalidades.append("[D2] Concorrente mencionado mas vendedor NÃO explorou → oportunidade perdida (P11)")

    # D2.3 — CHURN: cliente sinalizou saída
    # É a situação de maior urgência: sinal de que a conta está em risco.
    # Se detectado, a ação não é amanhã — é agora.
    if tem_sinal(texto_c, SINAIS_CHURN):
        score_cliente += 3
        razoes.append("[D2] Sinal de churn detectado → retenção urgente necessária (P15-R2)")
        sinais_detectados["churn"] = True

    # D2.4 — DORES RELATADAS: cliente revelou problemas que mapeiam para produtos
    # Dor sem produto conectado = oportunidade perdida (OP2 no Framework P6).
    # Quanto mais dores o cliente relata, mais janelas de produto existem.
    n_dores = conta_sinais(texto_c, SINAIS_OPERACIONAL)
    if n_dores >= 2:
        score_cliente += 2
        razoes.append(f"[D2] {n_dores} dores/problemas do cliente identificados → janelas de produto (P6-OP2)")
    elif n_dores == 1:
        score_cliente += 1
        razoes.append("[D2] 1 dor do cliente identificada → janela de produto pequena")

    # D2.5 — OBJEÇÃO DE PREÇO: cliente questionou o custo
    # Objeção é um sinal de interesse — quem não está interessado não objeta.
    # Detectar a objeção é importante para saber se o vendedor respondeu.
    if objecao_detectada:
        sinais_detectados["objecao_preco"] = True
        if rebuttal_detectado:
            score_cliente += 1
            razoes.append("[D2] Objeção de preço detectada e rebatida com argumento pelo vendedor")
            sinais_detectados["rebuttal"] = True
        else:
            penalidades.append("[D2] Objeção de preço detectada mas vendedor NÃO rebateu com dado (capitulação)")

    score_cliente = max(0, min(10, score_cliente))

    # -----------------------------------------------------------------------
    # DIMENSÃO 3 — COMPORTAMENTO DO VENDEDOR (0-10)
    # "O vendedor aplicou os comportamentos que os dados mostram que fecham?"
    #
    # Esta dimensão mede diretamente os comportamentos B1-B10 e os padrões
    # de abertura/fechamento. São os comportamentos ENSINÁVEIS — é aqui que
    # o treinamento tem impacto direto.
    # -----------------------------------------------------------------------

    # D3.1 — DIAGNÓSTICO ANTES DO PRODUTO (B1, peso=2 no framework)
    # +43,1pp de diferença nos dados. Vendedor que faz diagnóstico propõe certo.
    # Vendedor que não faz diagnóstico propõe no escuro — e perde mais.
    if tem_sinal(texto_a, SINAIS_DIAGNOSTICO):
        score_vendedor += 2
        razoes.append("[D3] Diagnóstico antes do produto detectado — entendeu antes de propor (B1, peso=2)")
        sinais_detectados["diagnostico"] = True

    # D3.2 — DENSIDADE DE PERGUNTAS: proxy quantitativo de B1
    # Mais perguntas = mais diagnóstico. Simples assim.
    # Não é peso direto no score, mas bônus moderado para quem pergunta mais.
    if densidade_perguntas >= 1.5:
        score_vendedor += 1
        razoes.append(f"[D3] Alta densidade de perguntas ({n_perguntas} perguntas, {densidade_perguntas}/turno) → diagnóstico ativo")
    sinais_detectados["n_perguntas"] = n_perguntas
    sinais_detectados["densidade_perguntas"] = densidade_perguntas

    # D3.3 — SONDAGEM DE CONCORRENTE / FROTA PRÓPRIA (B10, peso=3 — MAIOR DO FRAMEWORK)
    # +54,9pp de diferença. É o comportamento com maior correlação com fechamento.
    # Aparece em apenas 19% das melhores ligações — ou seja, tem espaço enorme pra crescer.
    if tem_sinal(texto_a, SINAIS_SONDAGEM_CONCORRENTE):
        score_vendedor += 3
        razoes.append("[D3] Vendedor sondou concorrência/frota própria — maior preditor de fechamento (B10, peso=3)")
        sinais_detectados["sondagem_concorrente"] = True

    # D3.4 — URGÊNCIA COM FATO VERIFICÁVEL (B6, peso=3)
    # Urgência real ancora o cliente no tempo. "Só até amanhã" com fato real
    # é diferente de "promoção especial hoje" sem embasamento.
    if tem_sinal(texto_a, SINAIS_URGENCIA):
        score_vendedor += 3
        razoes.append("[D3] Urgência criada com fato verificável — ancora o cliente no tempo (B6, peso=3)")
        sinais_detectados["urgencia"] = True

    # D3.5 — UPSELL CONECTADO À DOR (B5, peso=2)
    # 0% nos não-fechamentos — quando conecta produto à dor, converte.
    # Detectamos upsell no contexto comercial (não apenas menção isolada).
    if tem_sinal(texto_a, SINAIS_UPSELL) and n_com >= 2:
        score_vendedor += 2
        razoes.append("[D3] Upsell de produto detectado no contexto comercial — conectou oferta à conversa (B5, peso=2)")
        sinais_detectados["upsell"] = True

    # D3.6 — USOU HISTÓRICO DO CLIENTE (B3, peso=2)
    # Personalização com dado do cliente real = credibilidade e relevância.
    # "Vi aqui que vocês têm 12 veículos" é diferente de "como posso ajudar?"
    if tem_sinal(texto_a, SINAIS_HISTORICO):
        score_vendedor += 1
        razoes.append("[D3] Vendedor referenciou histórico ou dados do cliente — personalização (B3, peso=2)")
        sinais_detectados["historico"] = True

    # D3.7 — CHALLENGER: REVELOU CUSTO OCULTO (CH1)
    # Quando o cliente menciona concorrente mais barato e o vendedor revela
    # o custo que o cliente não havia calculado, isso muda a decisão.
    if tem_sinal(texto_a, SINAIS_CH1_CUSTO_OCULTO):
        score_vendedor += 1
        razoes.append("[D3] Vendedor revelou custo oculto para rebater objeção ou posicionar (CH1 Challenger)")
        sinais_detectados["ch1_custo_oculto"] = True

    # D3.8 — CHALLENGER: ANTECIPAÇÃO DE PROBLEMA (CH6)
    # Alertar o cliente sobre um problema futuro que ele ainda não percebeu
    # demonstra expertise e gera confiança. Cria urgência verdadeira.
    if tem_sinal(texto_a, SINAIS_CH6_ANTECIPACAO):
        score_vendedor += 1
        razoes.append("[D3] Vendedor antecipou problema futuro do cliente — expertise demonstrada (CH6 Challenger)")
        sinais_detectados["ch6_antecipacao"] = True

    # D3.9 — ALERTOU RISCO AO CLIENTE (B4, peso=2)
    # Alerta com dado real = urgência legítima. Diferente de "promoção".
    if tem_sinal(texto_a, SINAIS_ALERTA):
        score_vendedor += 1
        razoes.append("[D3] Vendedor alertou cliente sobre risco real — cria urgência legítima (B4, peso=2)")
        sinais_detectados["alerta"] = True

    # D3.10 — TIPO DE ABERTURA: bônus para abertura contextualizada (AB1)
    # Abertura contextualizada mostra preparo — aumenta a receptividade do cliente.
    if tipo_abertura == "AB1_contextual":
        score_vendedor += 1
        razoes.append("[D3] Abertura contextualizada — vendedor chegou preparado com dados do cliente (AB1)")
    elif tipo_abertura == "AB5_protecao":
        penalidades.append("[D3] Abertura de proteção — 'manter cadastro ativo' não tem objetivo comercial claro (AB5)")

    # D3.11 — TIPO DE FECHAMENTO: o comportamento com maior impacto isolado
    # FC1 vale mais porque é o único que garante continuidade pelos dois lados.
    # FC3 é penalizado porque é o padrão dominante e o menos eficaz.
    if tipo_fechamento == "FC1_compromisso_duplo":
        score_vendedor += 3
        razoes.append("[D3] Fechamento FC1 — compromisso duplo com data dos dois lados (o mais raro e eficaz)")
        sinais_detectados["proximo_passo"] = True
    elif tipo_fechamento == "FC5_diretivo":
        score_vendedor += 2
        razoes.append("[D3] Fechamento FC5 — diretivo: vendedor disse ao cliente o que fazer e quando")
        sinais_detectados["proximo_passo"] = True
    elif tipo_fechamento == "FC2_so_vendedor":
        score_vendedor += 1
        razoes.append("[D3] Fechamento FC2 — próximo passo só do vendedor; cliente não assumiu compromisso")
        sinais_detectados["proximo_passo"] = True
    elif tipo_fechamento == "FC3_vago":
        penalidades.append("[D3] Fechamento FC3 — 'qualquer coisa me chama': sem próximo passo, sem data (maior vazamento do time)")

    # D3.12 — PROMESSAS SEM PRAZO: penalidade por risco de não cumprimento
    # Cada promessa sem prazo é um risco de perda de confiança com o cliente.
    if promessas_sem_prazo >= 2:
        penalidades.append(f"[D3] {promessas_sem_prazo} promessas sem prazo detectadas — alto risco de não cumprimento (P10)")
    elif promessas_sem_prazo == 1:
        penalidades.append("[D3] 1 promessa sem prazo detectada — monitorar se foi cumprida (P10)")
    sinais_detectados["promessas_sem_prazo"] = promessas_sem_prazo

    # D3.13 — TALK RATIO: penalidade se o vendedor falou demais
    # Vendedor que fala >70% das palavras não está ouvindo o cliente.
    # Quem ouve mais, personaliza mais. Quem personaliza mais, fecha mais.
    # (Framework P12 — Talk/Listen Ratio)
    total_words = words_a + words_c
    word_ratio_vendedor = round(words_a / total_words, 2) if total_words > 0 else 0
    if word_ratio_vendedor > 0.70 and total_words > 100:
        penalidades.append(f"[D3] Vendedor falou {word_ratio_vendedor*100:.0f}% das palavras — pouco espaço para o cliente (P12)")
    elif word_ratio_vendedor < 0.35 and total_words > 100:
        razoes.append(f"[D3] Vendedor falou apenas {word_ratio_vendedor*100:.0f}% — boa escuta ativa (P12)")

    score_vendedor = max(0, min(10, score_vendedor))

    # -----------------------------------------------------------------------
    # SCORE TOTAL E CLASSIFICAÇÃO
    # -----------------------------------------------------------------------
    score_total = score_contexto + score_cliente + score_vendedor

    # Os thresholds foram calibrados para separar os 5% melhores (ALTO),
    # o quartil seguinte (MÉDIO) e o resto (BAIXO / SEM POTENCIAL).
    if score_total >= 20:
        nivel = "ALTO"
    elif score_total >= 13:
        nivel = "MEDIO"
    elif score_total >= 7:
        nivel = "BAIXO"
    else:
        nivel = "SEM_POTENCIAL"

    # -----------------------------------------------------------------------
    # RETORNO: todos os campos que o CSV vai capturar
    # -----------------------------------------------------------------------
    return {
        # Identificação
        "client_id":                client_id,
        "data":                     call.get("data", "?")[:10],
        "duracao_s":                duracao,
        "sentimento":               call.get("sentimento", "?"),

        # Score principal
        "nivel":                    nivel,
        "score_total":              score_total,
        "score_contexto":           score_contexto,
        "score_cliente":            score_cliente,
        "score_vendedor":           score_vendedor,

        # Talk ratio (P12)
        "turns_vendedor":           turns_a,
        "turns_cliente":            turns_c,
        "words_vendedor":           words_a,
        "words_cliente":            words_c,
        "word_ratio_vendedor":      word_ratio_vendedor,
        "turn_ratio_vendedor":      round(turns_a / (turns_a + turns_c), 2) if (turns_a + turns_c) > 0 else 0,

        # Comportamentos B1-B10
        "tem_diagnostico":          int(sinais_detectados.get("diagnostico", False)),
        "tem_urgencia":             int(sinais_detectados.get("urgencia", False)),
        "tem_sondagem_concorrente": int(sinais_detectados.get("sondagem_concorrente", False)),
        "tem_upsell":               int(sinais_detectados.get("upsell", False)),
        "tem_historico":            int(sinais_detectados.get("historico", False)),
        "tem_alerta":               int(sinais_detectados.get("alerta", False)),
        "tem_ch1":                  int(sinais_detectados.get("ch1_custo_oculto", False)),
        "tem_ch6":                  int(sinais_detectados.get("ch6_antecipacao", False)),

        # Sinais do cliente
        "tem_churn":                int(sinais_detectados.get("churn", False)),
        "tem_expansao":             int(sinais_detectados.get("expansao", False)),
        "concorrente_cliente":      int(concorrente_cliente),
        "concorrente_explorado":    int(concorrente_explorado),
        "objecao_preco":            int(objecao_detectada),
        "rebuttal_detectado":       int(rebuttal_detectado),

        # Padrões de abertura e fechamento (P9)
        "tipo_abertura":            tipo_abertura,
        "tipo_fechamento":          tipo_fechamento,

        # Perguntas (proxy de diagnóstico)
        "n_perguntas_vendedor":     n_perguntas,
        "densidade_perguntas":      densidade_perguntas,

        # Promessas (P10)
        "promessas_sem_prazo":      promessas_sem_prazo,

        # Fluxo comercial — quando na ligação o vendedor tentou
        "fluxo_comercial":          fluxo_comercial,

        # Produtos mencionados (P7)
        "produtos_mencionados":     "|".join(produtos_mencionados),

        # Diagnóstico textual
        "razoes":                   " | ".join(razoes),
        "penalidades":              " | ".join(penalidades),
    }


# ===========================================================================
# MAIN — processa todas as ligações e gera outputs
# ===========================================================================
def main():
    ts_inicio = datetime.now()
    print(f"[{ts_inicio.strftime('%H:%M:%S')}] Carregando LIG...")
    with open(FILE_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    total_clientes = len(data)
    total_calls    = sum(len(v) for v in data.values())
    print(f"  {total_clientes} clientes | {total_calls} ligações")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # -----------------------------------------------------------------------
    # Processa todas as ligações
    # -----------------------------------------------------------------------
    resultados = []
    for client_id, calls in data.items():
        for call in calls:
            r = avaliar_ligacao(client_id, call)
            resultados.append(r)

    ts_fim = datetime.now()
    tempo_total = (ts_fim - ts_inicio).total_seconds()

    # -----------------------------------------------------------------------
    # SALVA CSV PRINCIPAL — linha por ligação, todos os campos
    # -----------------------------------------------------------------------
    campos = [
        "client_id", "data", "duracao_s", "sentimento",
        "nivel", "score_total", "score_contexto", "score_cliente", "score_vendedor",
        "turns_vendedor", "turns_cliente", "words_vendedor", "words_cliente",
        "word_ratio_vendedor", "turn_ratio_vendedor",
        "tem_diagnostico", "tem_urgencia", "tem_sondagem_concorrente",
        "tem_upsell", "tem_historico", "tem_alerta", "tem_ch1", "tem_ch6",
        "tem_churn", "tem_expansao", "concorrente_cliente", "concorrente_explorado",
        "objecao_preco", "rebuttal_detectado",
        "tipo_abertura", "tipo_fechamento",
        "n_perguntas_vendedor", "densidade_perguntas", "promessas_sem_prazo",
        "fluxo_comercial", "produtos_mencionados",
        "razoes", "penalidades",
    ]

    csv_path = OUTPUT_DIR / "scoring_potencial_julho.csv"
    linhas = [",".join(campos) + "\n"]
    for r in resultados:
        valores = []
        for campo in campos:
            val = r.get(campo, "")
            # Campos de texto: coloca entre aspas e escapa aspas internas
            if isinstance(val, str) and ("," in val or '"' in val or "|" in val):
                val = '"' + val.replace('"', '""') + '"'
            valores.append(str(val))
        linhas.append(",".join(valores) + "\n")
    csv_path.write_text("".join(linhas), encoding="utf-8")
    print(f"  CSV salvo: {csv_path.name} ({len(resultados)} linhas)")

    # -----------------------------------------------------------------------
    # PREPARA DADOS PARA O RELATÓRIO
    # -----------------------------------------------------------------------
    dist      = Counter(r["nivel"] for r in resultados)
    por_nivel = defaultdict(list)
    for r in resultados:
        por_nivel[r["nivel"]].append(r)
    altos = por_nivel["ALTO"]
    n_altos = len(altos) or 1  # evita divisão por zero

    def pct(n, total):
        return f"{n/total*100:.1f}%" if total > 0 else "0%"

    def media(lista, campo):
        vals = [r[campo] for r in lista if isinstance(r.get(campo), (int, float))]
        return round(sum(vals) / len(vals), 1) if vals else 0

    def freq(lista, campo):
        n = sum(1 for r in lista if r.get(campo) == 1 or r.get(campo) is True)
        return n, pct(n, len(lista)) if lista else "0%"

    # Distribuição de aberturas e fechamentos (todas as ligações)
    aberturas  = Counter(r["tipo_abertura"]  for r in resultados)
    fechamentos = Counter(r["tipo_fechamento"] for r in resultados)
    fluxos      = Counter(r["fluxo_comercial"] for r in resultados)

    # Objeções e rebuttal
    total_objecao  = sum(1 for r in resultados if r["objecao_preco"] == 1)
    total_rebuttal = sum(1 for r in resultados if r["rebuttal_detectado"] == 1)
    taxa_rebuttal  = round(total_rebuttal / total_objecao * 100, 1) if total_objecao > 0 else 0

    # Promessas sem prazo
    total_promessas_risco = sum(1 for r in resultados if r["promessas_sem_prazo"] >= 1)

    # Talk ratio médio por nível
    wr_alto  = media(por_nivel["ALTO"],          "word_ratio_vendedor")
    wr_medio = media(por_nivel["MEDIO"],         "word_ratio_vendedor")
    wr_sem   = media(por_nivel["SEM_POTENCIAL"], "word_ratio_vendedor")

    # Perguntas médias por nível
    pq_alto  = media(por_nivel["ALTO"],          "n_perguntas_vendedor")
    pq_sem   = media(por_nivel["SEM_POTENCIAL"], "n_perguntas_vendedor")

    # Concorrente: mencionado vs explorado
    total_conc_cliente  = sum(1 for r in resultados if r["concorrente_cliente"] == 1)
    total_conc_explorado = sum(1 for r in resultados if r["concorrente_explorado"] == 1)
    taxa_explorado = round(total_conc_explorado / total_conc_cliente * 100, 1) if total_conc_cliente > 0 else 0

    # Produtos mais mencionados
    todos_produtos = []
    for r in resultados:
        todos_produtos.extend(r["produtos_mencionados"].split("|"))
    contador_produtos = Counter(p for p in todos_produtos if p != "nenhum")

    # Clientes com churn ou expansão (ação imediata)
    urgentes = [r for r in resultados if r["tem_churn"] == 1 or r["tem_expansao"] == 1]

    # Top 10 por score
    top10 = sorted(resultados, key=lambda r: r["score_total"], reverse=True)[:10]

    # Clientes com maior score agregado (soma de todas as ligações do cliente)
    score_por_cliente = defaultdict(int)
    for r in resultados:
        score_por_cliente[r["client_id"]] += r["score_total"]
    top_clientes = sorted(score_por_cliente.items(), key=lambda x: x[1], reverse=True)[:10]

    # -----------------------------------------------------------------------
    # RELATÓRIO EXECUTIVO
    # -----------------------------------------------------------------------
    relatorio = f"""
====================================================================
SCORING DE POTENCIAL COMERCIAL — LOCALIZA FROTA PJ
Rodado em: {ts_inicio.strftime('%d/%m/%Y %H:%M')}   |   Tempo: {tempo_total:.1f}s
Base: {total_calls} ligações  |  {total_clientes} clientes
====================================================================

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. DISTRIBUIÇÃO DE POTENCIAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  ALTO          : {dist['ALTO']:>5} ligações ({pct(dist['ALTO'], total_calls)})   Score >= 20
  MEDIO         : {dist['MEDIO']:>5} ligações ({pct(dist['MEDIO'], total_calls)})   Score 13-19
  BAIXO         : {dist['BAIXO']:>5} ligações ({pct(dist['BAIXO'], total_calls)})   Score  7-12
  SEM POTENCIAL : {dist['SEM_POTENCIAL']:>5} ligações ({pct(dist['SEM_POTENCIAL'], total_calls)})   Score  0- 6

  Score medio geral : {media(resultados, 'score_total')}
  Score medio ALTO  : {media(altos, 'score_total')}
  Duracao media ALTO: {media(altos, 'duracao_s')}s

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
2. TALK/LISTEN RATIO — quem dominou a conversa (P12)
   Referencia: vendedor ideal fala entre 40% e 60% das palavras.
   Abaixo de 35% = cliente dominou. Acima de 70% = vendedor monologou.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Word ratio medio — ALTO          : {wr_alto*100:.1f}% vendedor
  Word ratio medio — MEDIO         : {wr_medio*100:.1f}% vendedor
  Word ratio medio — SEM POTENCIAL : {wr_sem*100:.1f}% vendedor

  Perguntas medias (ALTO)          : {pq_alto:.1f} por ligacao
  Perguntas medias (SEM POTENCIAL) : {pq_sem:.1f} por ligacao

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
3. TIPOS DE ABERTURA — como o vendedor chegou na ligacao (P9-AB)
   AB1 contextual e AB2 relacional sao as mais eficazes.
   AB5 (protecao) e AB3 (generica) tem menor taxa de avanco comercial.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  AB1 Contextualizada  : {aberturas.get('AB1_contextual',0):>5} ({pct(aberturas.get('AB1_contextual',0), total_calls)})
  AB2 Relacional       : {aberturas.get('AB2_relacional',0):>5} ({pct(aberturas.get('AB2_relacional',0), total_calls)})
  AB3 Generica         : {aberturas.get('AB3_generica',0):>5} ({pct(aberturas.get('AB3_generica',0), total_calls)})
  AB4 Reativa          : {aberturas.get('AB4_reativa',0):>5} ({pct(aberturas.get('AB4_reativa',0), total_calls)})
  AB5 De protecao      : {aberturas.get('AB5_protecao',0):>5} ({pct(aberturas.get('AB5_protecao',0), total_calls)})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
4. TIPOS DE FECHAMENTO — como a ligacao terminou (P9-FC)
   FC1 (compromisso duplo) e FC5 (diretivo) sao os mais eficazes.
   FC3 (vago) e FC4 (aberto) vao para o arquivo morto.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  FC1 Compromisso duplo  : {fechamentos.get('FC1_compromisso_duplo',0):>5} ({pct(fechamentos.get('FC1_compromisso_duplo',0), total_calls)})
  FC2 So do vendedor     : {fechamentos.get('FC2_so_vendedor',0):>5} ({pct(fechamentos.get('FC2_so_vendedor',0), total_calls)})
  FC3 Vago               : {fechamentos.get('FC3_vago',0):>5} ({pct(fechamentos.get('FC3_vago',0), total_calls)})
  FC4 Aberto             : {fechamentos.get('FC4_aberto',0):>5} ({pct(fechamentos.get('FC4_aberto',0), total_calls)})
  FC5 Diretivo           : {fechamentos.get('FC5_diretivo',0):>5} ({pct(fechamentos.get('FC5_diretivo',0), total_calls)})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
5. FLUXO COMERCIAL — quando na ligacao o vendedor tentou vender
   "meio" e' o ideal: resolveu primeiro, depois tentou.
   "nao_detectado" = suporte puro sem tentativa comercial.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  No inicio   : {fluxos.get('inicio',0):>5} ({pct(fluxos.get('inicio',0), total_calls)})
  No meio     : {fluxos.get('meio',0):>5} ({pct(fluxos.get('meio',0), total_calls)})
  No fim      : {fluxos.get('fim',0):>5} ({pct(fluxos.get('fim',0), total_calls)})
  Nao tentou  : {fluxos.get('nao_detectado',0):>5} ({pct(fluxos.get('nao_detectado',0), total_calls)})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
6. OBJECOES DE PRECO — detectadas e respondidas (P8)
   Taxa de rebuttal = quantas objecoes foram respondidas com dado real.
   Abaixo de 50% = o time capitula mais do que argumenta.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Objecoes detectadas          : {total_objecao:>5}
  Respondidas com argumento    : {total_rebuttal:>5} ({taxa_rebuttal}% taxa de rebuttal)
  Sem resposta / capitulacao   : {total_objecao - total_rebuttal:>5}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
7. CONCORRENTES — mencao do cliente e resposta do vendedor (P11)
   Taxa de exploracao = quando o cliente citou outro fornecedor,
   o vendedor aproveitou para diferenciar a Localiza?
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Ligacoes com mencao de concorrente (cliente) : {total_conc_cliente}
  Vendedor explorou com argumento              : {total_conc_explorado} ({taxa_explorado}%)
  Vendedor ignorou a mencao                    : {total_conc_cliente - total_conc_explorado}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
8. PROMESSAS SEM PRAZO — risco de nao cumprimento (P10)
   Promessa sem prazo = cliente nao sabe quando esperar = confianca cai.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Ligacoes com ao menos 1 promessa sem prazo: {total_promessas_risco} ({pct(total_promessas_risco, total_calls)})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
9. PRODUTOS MENCIONADOS — portfolio explorado (P7)
   Quantas vezes cada produto apareceu nas ligacoes.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    for produto, qtd in contador_produtos.most_common():
        relatorio += f"\n  {produto:<20}: {qtd:>5} ({pct(qtd, total_calls)})"

    relatorio += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
10. COMPORTAMENTOS NAS LIGACOES DE ALTO POTENCIAL (n={len(altos)})
    Referencia: o que os melhores {pct(dist['ALTO'], total_calls)} fazem diferente.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    comportamentos_alto = {
        "B1  Diagnostico antes do produto": "tem_diagnostico",
        "B6  Urgencia com fato real":        "tem_urgencia",
        "B10 Sondagem de concorrente":       "tem_sondagem_concorrente",
        "B5  Upsell conectado a dor":        "tem_upsell",
        "B3  Usou historico do cliente":     "tem_historico",
        "B4  Alertou risco ao cliente":      "tem_alerta",
        "CH1 Revelou custo oculto":          "tem_ch1",
        "CH6 Antecipou problema":            "tem_ch6",
        "P15 Expansao detectada":            "tem_expansao",
        "P15 Churn detectado":               "tem_churn",
        "P9  Proximo passo concreto":        "proximo_passo",
    }
    for label, campo in comportamentos_alto.items():
        n = sum(1 for r in altos if r.get(campo) == 1 or r.get(campo) is True)
        relatorio += f"\n  {label:<35}: {n:>4} ({pct(n, len(altos))})"

    relatorio += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
11. TOP 10 LIGACOES — MAIOR POTENCIAL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{"Cliente":<14} {"Data":<12} {"Score":>5}  {"Nivel":<14} {"Dur":>6}s  Destaques"""
    for r in top10:
        destaques = []
        if r["tem_expansao"]           == 1: destaques.append("EXPANSAO")
        if r["tem_churn"]              == 1: destaques.append("CHURN")
        if r["tem_sondagem_concorrente"]== 1: destaques.append("CONCORRENTE")
        if r["tem_urgencia"]           == 1: destaques.append("URGENCIA")
        if r["tem_diagnostico"]        == 1: destaques.append("DIAGNOSTICO")
        if r["tem_ch1"]                == 1: destaques.append("CH1")
        relatorio += f"\n{r['client_id']:<14} {r['data']:<12} {r['score_total']:>5}  {r['nivel']:<14} {r['duracao_s']:>6}s  {' | '.join(destaques)}"

    relatorio += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
12. TOP 10 CLIENTES — MAIOR SCORE ACUMULADO (todas as ligacoes)
    Clientes com maior engajamento comercial total.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{"Cliente":<14}  {"Score total acumulado":>22}"""
    for cid, score in top_clientes:
        relatorio += f"\n{cid:<14}  {score:>22}"

    relatorio += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
13. ACAO IMEDIATA — CHURN + EXPANSAO DETECTADOS ({len(urgentes)} ligacoes)
    Estas ligacoes tem sinais de cancelamento ou crescimento.
    Sao prioridade maxima de retorno.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    for r in sorted(urgentes, key=lambda x: x["score_total"], reverse=True)[:25]:
        tipo = []
        if r["tem_churn"]   == 1: tipo.append("CHURN")
        if r["tem_expansao"]== 1: tipo.append("EXPANSAO")
        relatorio += f"\n  Cliente {r['client_id']:<14} | {r['data']} | Score {r['score_total']:>2} | {' + '.join(tipo)}"

    relatorio += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ARQUIVOS GERADOS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  scoring_potencial_julho.csv       linha por ligacao com todos os campos
  scoring_distribuicao_julho.txt    este relatorio executivo
"""

    dist_path = OUTPUT_DIR / "scoring_distribuicao_julho.txt"
    dist_path.write_text(relatorio, encoding="utf-8")

    # Print sem emojis para compatibilidade de terminal
    print(relatorio.encode("ascii", errors="replace").decode("ascii"))
    print(f"\n  Relatorio salvo: {dist_path.name}")
    print(f"  Tempo total: {tempo_total:.1f}s")


if __name__ == "__main__":
    main()
