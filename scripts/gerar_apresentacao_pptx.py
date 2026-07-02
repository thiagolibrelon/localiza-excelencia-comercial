"""
Gera apresentacao/Aletheia_Apresentacao_Completa.pptx cobrindo TODO o conteudo
de apresentacao/APRESENTACAO_EXECUTIVA.md (nao so o sumario executivo).

Padrao visual: fundo branco, titulo curto no topo esquerdo, logo "Aletheia"
no topo direito, rodape "Classificacao da Informacao: INTERNA" centralizado.
Cores da marca (mesmas do dashboardv2.html): verde #78DE1F, verde escuro #003418.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pathlib import Path

VERDE       = RGBColor(0x78, 0xDE, 0x1F)
VERDE_ESC   = RGBColor(0x00, 0x34, 0x18)
VERDE_MED   = RGBColor(0x01, 0x84, 0x44)
CINZA_TXT   = RGBColor(0x4A, 0x4A, 0x4A)
CINZA_CLARO = RGBColor(0xAF, 0xAF, 0xAF)
CINZA_FUNDO = RGBColor(0xF2, 0xF2, 0xF2)
VERMELHO    = RGBColor(0xD9, 0x20, 0x20)
AMARELO     = RGBColor(0xCA, 0x8A, 0x04)
ROXO        = RGBColor(0x5B, 0x21, 0xB6)
BRANCO      = RGBColor(0xFF, 0xFF, 0xFF)
CINZA_NEUTRO = RGBColor(0x9A, 0xA5, 0xB4)

FONTE = "Calibri"

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


# ===========================================================================
# HELPERS
# ===========================================================================
def new_slide():
    s = prs.slides.add_slide(BLANK)
    s.background.fill.solid()
    s.background.fill.fore_color.rgb = BRANCO
    return s


def add_textbox(slide, left, top, width, height, text, size=12, bold=False,
                 color=CINZA_TXT, align=PP_ALIGN.LEFT, font=FONTE, italic=False,
                 anchor=None):
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    if anchor:
        tf.vertical_anchor = anchor
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = font
    return box


def add_bullets(slide, left, top, width, height, items, size=11, color=CINZA_TXT,
                 bullet_color=None, line_spacing=1.15, space_after=6):
    """items: lista de (texto_negrito_ou_None, texto_normal, nivel)"""
    box = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = box.text_frame
    tf.word_wrap = True
    for i, (bold_part, normal_part, nivel) in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = nivel
        p.line_spacing = line_spacing
        p.space_after = Pt(space_after)
        marcador = "•  " if nivel == 0 else "-  "
        r0 = p.add_run()
        r0.text = marcador
        r0.font.size = Pt(size)
        r0.font.color.rgb = bullet_color or VERDE_MED
        r0.font.name = FONTE
        if bold_part:
            r1 = p.add_run()
            r1.text = bold_part
            r1.font.bold = True
            r1.font.size = Pt(size)
            r1.font.color.rgb = color
            r1.font.name = FONTE
        r2 = p.add_run()
        r2.text = normal_part
        r2.font.size = Pt(size)
        r2.font.color.rgb = color
        r2.font.name = FONTE
    return box


def add_header(slide, titulo, subtitulo, kicker=None):
    top_title = 0.28
    if kicker:
        add_textbox(slide, 0.5, 0.10, 7.0, 0.25, kicker, size=10, bold=True, color=VERDE_MED)
        top_title = 0.32
    add_textbox(slide, 0.5, top_title, 8.5, 0.5, titulo, size=22, bold=True, color=VERDE_ESC)
    add_textbox(slide, 0.5, top_title + 0.47, 8.5, 0.35, subtitulo, size=13, bold=False, color=CINZA_TXT)
    add_textbox(slide, 9.8, 0.28, 3.0, 0.4, "Aletheia", size=20, bold=True,
                color=VERDE_MED, align=PP_ALIGN.RIGHT)
    add_textbox(slide, 9.8, 0.68, 3.0, 0.3, "RAC · Inteligência Comercial", size=9,
                bold=False, color=CINZA_TXT, align=PP_ALIGN.RIGHT)
    line = slide.shapes.add_connector(1, Inches(0.5), Inches(1.15), Inches(12.83), Inches(1.15))
    line.line.color.rgb = RGBColor(0xE6, 0xE6, 0xE6)
    line.line.width = Pt(1)


def add_footer(slide, page_num=None):
    add_textbox(slide, 0, 7.15, 13.333, 0.3,
                "Classificação da Informação: INTERNA", size=8, color=CINZA_CLARO,
                align=PP_ALIGN.CENTER)
    if page_num:
        add_textbox(slide, 12.6, 7.12, 0.6, 0.3, str(page_num), size=9, color=CINZA_CLARO,
                    align=PP_ALIGN.RIGHT)


def add_table(slide, left, top, width, height, headers, rows, col_widths=None,
              font_size=10.5, header_size=10.5):
    n_rows = len(rows) + 1
    n_cols = len(headers)
    gtable = slide.shapes.add_table(n_rows, n_cols, Inches(left), Inches(top),
                                     Inches(width), Inches(height)).table
    if col_widths:
        for i, w in enumerate(col_widths):
            gtable.columns[i].width = Inches(w)
    for j, h in enumerate(headers):
        cell = gtable.cell(0, j)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = VERDE_ESC
        p = cell.text_frame.paragraphs[0]
        p.font.size = Pt(header_size)
        p.font.bold = True
        p.font.color.rgb = BRANCO
        p.font.name = FONTE
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    for i, row in enumerate(rows, start=1):
        for j, val in enumerate(row):
            cell = gtable.cell(i, j)
            cell.text = str(val)
            cell.fill.solid()
            cell.fill.fore_color.rgb = CINZA_FUNDO if i % 2 == 0 else BRANCO
            p = cell.text_frame.paragraphs[0]
            p.font.size = Pt(font_size)
            p.font.color.rgb = CINZA_TXT
            p.font.name = FONTE
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    return gtable


def add_pergunta_cards(slide, top, perguntas, col_width=5.9, gap=0.5):
    """perguntas: lista de (numero, titulo, resumo, porque). Layout em 1 ou 2 colunas."""
    n = len(perguntas)
    left0 = 0.5
    box_h = (6.9 - top) / ((n + 1) // 2 if n > 1 else 1)
    for idx, (num, titulo, resumo, porque) in enumerate(perguntas):
        col = idx % 2 if n > 1 else 0
        linha = idx // 2 if n > 1 else idx
        left = left0 + col * (col_width + gap)
        y = top + linha * (box_h)
        card_w = col_width if n > 1 else 12.3
        # cartao com fundo leve
        card = slide.shapes.add_shape(1, Inches(left), Inches(y), Inches(card_w), Inches(box_h - 0.15))
        card.fill.solid()
        card.fill.fore_color.rgb = CINZA_FUNDO
        card.line.fill.background()
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        tf.margin_right = Inches(0.15)
        tf.margin_top = Inches(0.08)
        tf.margin_bottom = Inches(0.05)
        p0 = tf.paragraphs[0]
        p0.alignment = PP_ALIGN.LEFT
        r0 = p0.add_run()
        r0.text = f"P{num} — {titulo}"
        r0.font.bold = True
        r0.font.size = Pt(11.5)
        r0.font.color.rgb = VERDE_ESC
        r0.font.name = FONTE
        p1 = tf.add_paragraph()
        p1.alignment = PP_ALIGN.LEFT
        p1.space_before = Pt(3)
        r1 = p1.add_run()
        r1.text = resumo
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = CINZA_TXT
        r1.font.name = FONTE
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.LEFT
        p2.space_before = Pt(3)
        r2 = p2.add_run()
        r2.text = "Por quê: "
        r2.font.size = Pt(9)
        r2.font.italic = True
        r2.font.bold = True
        r2.font.color.rgb = VERDE_MED
        r2.font.name = FONTE
        r3 = p2.add_run()
        r3.text = porque
        r3.font.size = Pt(9)
        r3.font.italic = True
        r3.font.color.rgb = CINZA_TXT
        r3.font.name = FONTE


STATUS_CORES = {
    "Confirmada": VERDE_MED,
    "Confirmada (mais forte)": VERDE_MED,
    "Revisada": AMARELO,
    "Em validação": CINZA_NEUTRO,
    "Nova": ROXO,
}


def add_hipotese_cards(slide, top, hipoteses, cols=3):
    n = len(hipoteses)
    col_w = 12.3 / cols
    rows_n = -(-n // cols)
    box_h = (6.95 - top) / rows_n
    for idx, (num, titulo, status, resumo) in enumerate(hipoteses):
        col = idx % cols
        linha = idx // cols
        left = 0.5 + col * col_w
        y = top + linha * box_h
        card = slide.shapes.add_shape(1, Inches(left), Inches(y), Inches(col_w - 0.15), Inches(box_h - 0.15))
        card.fill.solid()
        card.fill.fore_color.rgb = CINZA_FUNDO
        card.line.fill.background()
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.12)
        tf.margin_right = Inches(0.12)
        tf.margin_top = Inches(0.08)
        p0 = tf.paragraphs[0]
        p0.alignment = PP_ALIGN.LEFT
        r0 = p0.add_run()
        r0.text = f"H{num}  "
        r0.font.bold = True
        r0.font.size = Pt(12)
        r0.font.color.rgb = VERDE_ESC
        r0.font.name = FONTE
        r0b = p0.add_run()
        r0b.text = status
        r0b.font.bold = True
        r0b.font.size = Pt(9)
        r0b.font.color.rgb = STATUS_CORES.get(status, CINZA_NEUTRO)
        r0b.font.name = FONTE
        p1 = tf.add_paragraph()
        p1.alignment = PP_ALIGN.LEFT
        p1.space_before = Pt(2)
        r1 = p1.add_run()
        r1.text = titulo
        r1.font.bold = True
        r1.font.size = Pt(10)
        r1.font.color.rgb = CINZA_TXT
        r1.font.name = FONTE
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.LEFT
        p2.space_before = Pt(3)
        r2 = p2.add_run()
        r2.text = resumo
        r2.font.size = Pt(8.5)
        r2.font.color.rgb = CINZA_TXT
        r2.font.name = FONTE


# ===========================================================================
# SLIDE 1 — CAPA
# ===========================================================================
s = new_slide()
add_textbox(s, 9.8, 0.4, 3.0, 0.4, "Aletheia", size=22, bold=True, color=VERDE_MED, align=PP_ALIGN.RIGHT)
add_textbox(s, 9.8, 0.8, 3.0, 0.3, "RAC · Inteligência Comercial", size=9, color=CINZA_TXT, align=PP_ALIGN.RIGHT)
add_textbox(s, 1.0, 2.9, 11.3, 1.2, "Inteligência Comercial em Ligações B2B", size=36, bold=True, color=VERDE_ESC)
add_textbox(s, 1.0, 3.9, 11.3, 0.6, "Localiza Frota PJ — Análise de 1.275 Ligações", size=18, color=CINZA_TXT)
add_textbox(s, 1.0, 4.5, 11.3, 0.5, "Junho–Julho 2026", size=13, color=CINZA_CLARO)
line = s.shapes.add_connector(1, Inches(1.0), Inches(2.75), Inches(6.0), Inches(2.75))
line.line.color.rgb = VERDE
line.line.width = Pt(2.5)
add_footer(s)

# ===========================================================================
# SLIDE 2 — O PONTO DE PARTIDA
# ===========================================================================
s = new_slide()
add_header(s, "O Ponto de Partida", "Por que este projeto existe", kicker="1 · CONTEXTO")
add_textbox(s, 1.3, 1.9, 10.7, 1.0,
            "“De 1.275 ligações gravadas, o que o vendedor faz para fechar um contrato?”",
            size=22, bold=True, italic=True, color=VERDE_ESC, align=PP_ALIGN.CENTER)
bullets = [
    (None, "Essa é a pergunta central do projeto.", 0),
    (None, "Hipótese de trabalho: os melhores vendedores fazem coisas diferentes dos medianos — e isso pode ser ensinado.", 0),
    (None, "O problema até hoje: sem análise sistemática, a resposta dependia de percepção gerencial, não de dados.", 0),
    (None, "Um gestor acompanha 2-3 ligações por semana. Aqui analisamos 1.275 de uma vez.", 0),
]
add_bullets(s, 1.5, 3.3, 10.3, 2.8, bullets, size=15, line_spacing=1.4, space_after=14)
add_footer(s, 2)

# ===========================================================================
# SLIDE 3 — A BASE DE DADOS
# ===========================================================================
s = new_slide()
add_header(s, "A Base de Dados", "Escopo da análise", kicker="2 · DADOS")
add_table(s, 0.8, 1.6, 8.0, 2.4,
          ["Métrica", "Valor"],
          [
              ["Ligações analisadas (base original, completa)", "1.275"],
              ["Clientes únicos (base original)", "1.109"],
              ["Período", "Junho 2026"],
              ["Fonte", "Gravações de chamadas — Localiza Empresas"],
              ["Formato", "Transcrição por Speech-to-Text"],
          ],
          col_widths=[5.2, 2.8], font_size=12, header_size=12)
box = s.shapes.add_shape(1, Inches(0.8), Inches(4.3), Inches(11.7), Inches(1.6))
box.fill.solid()
box.fill.fore_color.rgb = RGBColor(0xD8, 0xEF, 0xFD)
box.line.fill.background()
tf = box.text_frame
tf.word_wrap = True
tf.margin_left = Inches(0.25)
tf.margin_top = Inches(0.15)
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.LEFT
r = p.add_run()
r.text = "Atualização 01/07/2026: "
r.font.bold = True
r.font.size = Pt(13)
r.font.color.rgb = VERDE_ESC
r.font.name = FONTE
r2 = p.add_run()
r2.text = ("recebido um novo lote de 5.348 ligações (4.434 clientes), ampliando a base "
           "combinada para 6.623 ligações. Scoring automático já rodado nas duas bases. "
           "Análise com IA do novo lote em andamento.")
r2.font.size = Pt(13)
r2.font.color.rgb = RGBColor(0x0B, 0x42, 0x60)
r2.font.name = FONTE
add_footer(s, 3)

# ===========================================================================
# SLIDE 4 — FRAMEWORK: VISAO GERAL (5 CAMADAS)
# ===========================================================================
s = new_slide()
add_header(s, "O Framework de Análise", "15 perguntas, organizadas em 5 camadas", kicker="3 · METODOLOGIA")
camadas = [
    ("CAMADA 1", "O que aconteceu na ligação?", "O desfecho e os comportamentos do vendedor"),
    ("CAMADA 2", "Qual o estado do cliente?", "Os problemas e o valor potencial de cada conta"),
    ("CAMADA 3", "O vendedor usou as técnicas?", "6 dimensões de comportamento comercial"),
    ("CAMADA 4", "O que o mercado está dizendo?", "Concorrência e proporção de fala"),
    ("CAMADA 5", "O que ninguém ainda viu?", "Padrões emergentes, diferenças entre vendedores, eventos raros"),
]
y = 1.9
for i, (num, pergunta, desc) in enumerate(camadas):
    box = s.shapes.add_shape(1, Inches(0.8), Inches(y), Inches(1.7), Inches(0.78))
    box.fill.solid()
    box.fill.fore_color.rgb = VERDE_ESC
    box.line.fill.background()
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = num
    r.font.bold = True
    r.font.size = Pt(13)
    r.font.color.rgb = BRANCO
    r.font.name = FONTE
    add_textbox(s, 2.7, y, 4.4, 0.78, pergunta, size=13, bold=True, color=VERDE_ESC, anchor=MSO_ANCHOR.MIDDLE)
    add_textbox(s, 7.3, y, 5.3, 0.78, desc, size=11, color=CINZA_TXT, anchor=MSO_ANCHOR.MIDDLE)
    y += 0.92
add_footer(s, 4)

# ===========================================================================
# SLIDES 5-9 — CAMADAS 1 a 5 (perguntas detalhadas)
# ===========================================================================
camada1 = [
    (1, "Desfecho e comportamentos do vendedor",
     "Classifica o resultado (fechou / interessado, não fechou / não era venda) e avalia 10 comportamentos com pesos por correlação com fechamento. Score 0-18.",
     "sem saber o desfecho, não há como identificar o que diferencia ligações que fecham."),
    (2, "Tipo de ligação",
     "Classifica a natureza da chamada: nova venda, renovação, expansão, retenção, suporte operacional etc.",
     "misturar suporte com prospecção no mesmo pool distorce qualquer análise."),
]
s = new_slide()
add_header(s, "Camada 1", "O que aconteceu na ligação?", kicker="3 · METODOLOGIA")
add_pergunta_cards(s, 1.9, camada1, col_width=5.9)
add_footer(s, 5)

camada2 = [
    (3, "Problemas recorrentes",
     "Identifica se o cliente relatou problema (plataforma, faturamento, multa, manutenção, sinistro) e se foi resolvido.",
     "problemas não resolvidos aumentam o risco de cancelamento."),
    (4, "Valor potencial do cliente",
     "Pontua o cliente em 6 dimensões: volume de frota, adimplência, tempo de relacionamento, engajamento, complexidade e potencial de expansão.",
     "permite priorizar esforço comercial nos clientes de maior potencial."),
]
s = new_slide()
add_header(s, "Camada 2", "Qual o estado do cliente?", kicker="3 · METODOLOGIA")
add_pergunta_cards(s, 1.9, camada2, col_width=5.9)
add_footer(s, 6)

camada3a = [
    (5, "Comportamentos Challenger",
     "Revelou custo oculto, demonstrou ROI, criou urgência real, usou dado do concorrente, antecipou problema, descobriu necessidade não declarada.",
     "venda consultiva tem a maior correlação com fechamento em B2B complexo."),
    (6, "Oportunidades perdidas",
     "Identifica e estima em R$ as oportunidades que existiam mas não foram aproveitadas.",
     "mostra o custo real de cada ligação mal aproveitada — não é opinião, é R$."),
    (7, "Expansão de portfólio",
     "Mapeia produtos mencionados vs. ofertados. A Localiza tem 12 produtos B2B; a maioria dos vendedores oferta 2-3.",
     "orienta treinamento e script comercial para as janelas não exploradas."),
]
s = new_slide()
add_header(s, "Camada 3 (parte 1)", "O vendedor usou as técnicas?", kicker="3 · METODOLOGIA")
add_pergunta_cards(s, 1.9, camada3a, col_width=5.9)
add_footer(s, 7)

camada3b = [
    (8, "Objeções",
     "Classifica o tipo de objeção (preço, prazo, produto, concorrência) e como o vendedor respondeu.",
     "objeção não tratada é venda perdida."),
    (9, "Abertura e fechamento",
     "Classifica a abertura (contextualizada/relacional/genérica/reativa) e o fechamento (forte/médio/fraco).",
     "o fechamento é o comportamento com maior impacto isolado no resultado."),
    (10, "Promessas do vendedor",
     "Rastreia cada compromisso assumido (vai enviar, vai ligar, vai resolver) com prazo e risco de não cumprimento.",
     "promessa não cumprida é perda de confiança — gestão preventiva de relacionamento."),
]
s = new_slide()
add_header(s, "Camada 3 (parte 2)", "O vendedor usou as técnicas?", kicker="3 · METODOLOGIA")
add_pergunta_cards(s, 1.9, camada3b, col_width=5.9)
add_footer(s, 8)

camada4 = [
    (11, "Inteligência competitiva",
     "Detecta menções a concorrentes (Unidas, Movida, assinatura), frota própria, e se o vendedor aproveitou o sinal.",
     "cada menção de concorrente é uma janela de diferenciação."),
    (12, "Proporção de fala",
     "Mede quanto o vendedor falou vs. o cliente (turnos e tamanho médio das falas).",
     "quem ouve mais, personaliza mais. Quem personaliza mais, fecha mais."),
]
s = new_slide()
add_header(s, "Camada 4", "O que o mercado está dizendo?", kicker="3 · METODOLOGIA")
add_pergunta_cards(s, 1.9, camada4, col_width=5.9)
add_footer(s, 9)

camada5 = [
    (13, "Padrões emergentes",
     "Captura comportamentos novos, temas recorrentes sem categoria, sinais fracos de mudança.",
     "os dados às vezes revelam o que a hipótese inicial não incluía."),
    (14, "Diferenças entre vendedores",
     "Compara 5 dimensões de performance: estrutura, linguagem, relacionamento, comportamento comercial, objeções.",
     "identifica benchmarks reais — não por feeling do gestor, por dado observável."),
    (15, "Eventos raros de alto impacto",
     "Detecta eventos em <5% das ligações mas com impacto desproporcional: expansão de frota, risco de cancelamento.",
     "esses sinais se perdem no volume sem um sistema de detecção."),
]
s = new_slide()
add_header(s, "Camada 5", "O que ninguém ainda viu?", kicker="3 · METODOLOGIA")
add_pergunta_cards(s, 1.9, camada5, col_width=5.9)
add_footer(s, 10)

# ===========================================================================
# SLIDE 11 — ONDE QUEREMOS CHEGAR
# ===========================================================================
s = new_slide()
add_header(s, "Onde Queremos Chegar", "3 perguntas de negócio", kicker="4 · OBJETIVO")
perguntas_negocio = [
    ("Pergunta 1 — Diagnóstico", "“Qual é o nível atual de performance comercial do time?”",
     "Pontuação por vendedor, distribuição de desfechos, taxa de tentativa comercial por ligação"),
    ("Pergunta 2 — Causa", "“O que diferencia as ligações que fecham das que não fecham?”",
     "Quais comportamentos do vendedor correlacionam com desfecho positivo"),
    ("Pergunta 3 — Ação", "“O que fazer nos próximos 30 dias para aumentar conversão?”",
     "Top comportamentos a treinar, clientes para ação imediata, oportunidades não exploradas"),
]
y = 2.0
for titulo, pergunta, resposta in perguntas_negocio:
    add_textbox(s, 0.8, y, 11.7, 0.35, titulo, size=15, bold=True, color=VERDE_ESC)
    add_textbox(s, 0.8, y + 0.4, 11.7, 0.4, pergunta, size=13, italic=True, color=CINZA_TXT)
    add_textbox(s, 0.8, y + 0.82, 11.7, 0.5, "→ " + resposta, size=12, color=VERDE_MED)
    y += 1.55
add_footer(s, 11)

# ===========================================================================
# SLIDE 12 — RESULTADOS SCORING: DISTRIBUICAO (grafico)
# ===========================================================================
s = new_slide()
add_header(s, "Distribuição de Potencial", "Scoring automático (Python, sem IA) — base combinada", kicker="5 · RESULTADOS SCORING")
leitura = (
    "Cada ligação recebe pontuação de 0 a 30 (contexto + sinais do cliente + comportamento do vendedor), "
    "rodado em <30s sem IA generativa. Apenas 5,6% das 6.623 ligações combinadas têm ALTO potencial — "
    "validado entre a base original (6,6%) e o novo lote (5,3%), confirmando que o padrão não é ruído."
)
add_textbox(s, 0.5, 1.35, 12.3, 0.85, leitura, size=11.5, color=CINZA_TXT)
add_textbox(s, 0.5, 2.25, 12.3, 0.35, "Distribuição de Potencial Comercial — 6.623 ligações combinadas",
            size=13, bold=True, color=VERDE_ESC, align=PP_ALIGN.CENTER)
chart_data = CategoryChartData()
chart_data.categories = ["ALTO (≥20)", "MÉDIO (13-19)", "BAIXO (7-12)", "SEM POTENCIAL (0-6)"]
chart_data.add_series("Ligações", (368, 1502, 2480, 2273))
gf = s.shapes.add_chart(XL_CHART_TYPE.COLUMN_CLUSTERED, Inches(1.8), Inches(2.7), Inches(9.7), Inches(3.9), chart_data)
chart = gf.chart
chart.has_legend = False
chart.has_title = False
plot = chart.plots[0]
plot.has_data_labels = True
plot.data_labels.number_format = '#,##0'
plot.data_labels.number_format_is_linked = False
plot.data_labels.font.size = Pt(11)
plot.data_labels.font.bold = True
plot.data_labels.font.color.rgb = VERDE_ESC
cores_pontos = [VERDE, CINZA_NEUTRO, CINZA_NEUTRO, VERMELHO]
for i, pt in enumerate(plot.series[0].points):
    pt.format.fill.solid()
    pt.format.fill.fore_color.rgb = cores_pontos[i]
chart.category_axis.tick_labels.font.size = Pt(10)
chart.category_axis.tick_labels.font.color.rgb = CINZA_TXT
chart.value_axis.tick_labels.font.size = Pt(9)
chart.value_axis.tick_labels.font.color.rgb = CINZA_TXT
chart.value_axis.has_major_gridlines = False
add_footer(s, 12)

# ===========================================================================
# SLIDE 13 — RESULTADOS SCORING: COMPORTAMENTOS + CLIENTES CRITICOS
# ===========================================================================
s = new_slide()
add_header(s, "Alto Potencial e Ação Imediata", "O que aparece nas melhores ligações + clientes críticos", kicker="5 · RESULTADOS SCORING")
add_textbox(s, 0.5, 1.35, 6.2, 0.3, "Comportamentos nas ligações de ALTO potencial (base original, n=84)",
            size=12, bold=True, color=VERDE_ESC)
add_table(s, 0.5, 1.7, 6.4, 3.0,
          ["Comportamento", "Freq."],
          [
              ["Criou urgência com fato real", "93%"],
              ["Fez diagnóstico antes de oferecer", "80%"],
              ["Tentou expandir o contrato", "71%"],
              ["Definiu próximo passo com data", "47%"],
              ["Identificou cliente em expansão", "31%"],
              ["Perguntou sobre concorrência/frota", "19%"],
              ["Identificou risco de cancelamento", "17%"],
          ],
          col_widths=[5.0, 1.4], font_size=10, header_size=10)
add_textbox(s, 7.2, 1.35, 5.6, 0.3, "Clientes críticos — ação imediata (base combinada)",
            size=12, bold=True, color=VERDE_ESC)
add_table(s, 7.2, 1.7, 5.6, 2.2,
          ["Cliente", "Score", "Sinal"],
          [
              ["08208057", "29/30", "Cancelar + expansão"],
              ["10845574", "29/30", "Cancelar + expansão"],
              ["06821416", "29/30", "Cancelar + expansão"],
              ["27247224", "29/30", "Expansão de frota"],
              ["10508823", "29/30", "Expansão de frota"],
          ],
          col_widths=[1.8, 1.2, 2.6], font_size=10, header_size=10)
add_textbox(s, 7.2, 4.1, 5.6, 0.9,
            "376 ligações com sinal de churn ou expansão de frota identificadas na base combinada (6.623 ligações).",
            size=10.5, italic=True, color=CINZA_TXT)
add_footer(s, 13)

# ===========================================================================
# SLIDE 14 — RESULTADOS IA: R$28.490 + DESFECHO
# ===========================================================================
s = new_slide()
add_header(s, "O Número Mais Importante", "R$28.490/mês em oportunidades não tentadas", kicker="6 · RESULTADOS IA")
add_textbox(s, 0.5, 1.35, 6.2, 0.9,
            "44,8% das ligações encerram sem data (\"qualquer coisa me chama\"). A IA estimou o valor "
            "potencial de cada oportunidade perdida com base no contexto da ligação (frota, produto, contrato).",
            size=11, color=CINZA_TXT)
add_table(s, 0.5, 2.35, 6.4, 2.3,
          ["Composição", "Valor/mês"],
          [
              ["OP6 — Upsell óbvio não tentado", "R$23.410"],
              ["OP7 — Churn não detectado", "R$3.600"],
              ["OP1 — Suporte sem pergunta comercial", "R$800"],
              ["Outros", "resto"],
              ["Total", "R$28.490"],
          ],
          col_widths=[4.6, 1.8], font_size=10.5, header_size=10.5)
add_textbox(s, 0.5, 4.75, 6.4, 0.4,
            "Estimativa da IA a partir de 1.149 oportunidades — não é receita confirmada/auditada.",
            size=9, italic=True, color=CINZA_CLARO)
add_textbox(s, 7.2, 1.35, 5.6, 0.3, "Desfecho das 1.275 ligações", size=12, bold=True, color=VERDE_ESC)
add_table(s, 7.2, 1.7, 5.6, 3.0,
          ["Desfecho", "Lig.", "%"],
          [
              ["Não era venda (suporte)", "728", "56,7%"],
              ["Interessou, não fechou", "460", "35,8%"],
              ["Fechou — novo", "63", "4,9%"],
              ["Fechou — upsell", "14", "1,1%"],
              ["Fechou — renovação", "12", "0,9%"],
              ["Sem conteúdo", "7", "0,5%"],
          ],
          col_widths=[3.4, 1.1, 1.1], font_size=10, header_size=10)
add_textbox(s, 7.2, 4.85, 5.6, 0.35, "Total de fechamentos: 89 (7,0%)", size=12, bold=True, color=VERDE_MED)
add_footer(s, 14)

# ===========================================================================
# SLIDE 15 — RESULTADOS IA: CORRELACAO B1-B10 (grafico)
# ===========================================================================
s = new_slide()
add_header(s, "O Que Diferencia Quem Fecha", "Correlação de comportamentos com fechamento (B1-B10)", kicker="6 · RESULTADOS IA")
add_textbox(s, 0.5, 1.35, 12.3, 0.55,
            "B5 (upsell conectado à dor) e B6 (urgência verificável) têm correlação positiva com fechamento. "
            "B1, B8 e B10 — comportamentos de pipeline, não de fechamento imediato — mostram correlação negativa.",
            size=11.5, color=CINZA_TXT)
chart_data2 = CategoryChartData()
chart_data2.categories = ["B5 Upsell/dor", "B6 Urgência", "B1 Diagnóstico", "B10 Concorrente", "B8 Proativo"]
chart_data2.add_series("% Fechou", (21.3, 9.0, 37.1, 4.5, 5.6))
chart_data2.add_series("% Interessou, não fechou", (13.9, 6.5, 49.6, 17.6, 21.5))
gf2 = s.shapes.add_chart(XL_CHART_TYPE.BAR_CLUSTERED, Inches(1.5), Inches(2.1), Inches(10.3), Inches(4.6), chart_data2)
chart2 = gf2.chart
chart2.has_title = False
chart2.has_legend = True
chart2.legend.position = 2  # XL_LEGEND_POSITION.BOTTOM
chart2.legend.include_in_layout = False
chart2.legend.font.size = Pt(10)
plot2 = chart2.plots[0]
plot2.has_data_labels = True
plot2.data_labels.number_format = '0.0"%"'
plot2.data_labels.number_format_is_linked = False
plot2.data_labels.font.size = Pt(9)
plot2.series[0].format.fill.solid()
plot2.series[0].format.fill.fore_color.rgb = VERDE
plot2.series[1].format.fill.solid()
plot2.series[1].format.fill.fore_color.rgb = CINZA_NEUTRO
chart2.category_axis.tick_labels.font.size = Pt(10)
chart2.value_axis.tick_labels.font.size = Pt(9)
chart2.value_axis.has_major_gridlines = False
add_footer(s, 15)

# ===========================================================================
# SLIDES 16-17 — 9 HIPOTESES
# ===========================================================================
hip1 = [
    (1, "A conta da diária vs. mensal converte mais", "Em validação",
     "Vendedor faz o cálculo em voz alta, cliente recalcula. Padrão recorrente, sem amostra controlada ainda."),
    (2, "Fechar sem data é não fechar", "Confirmada",
     "FC3 em 44,8%; FC1 (compromisso duplo) só 31,9%; prazo definido apenas 9%."),
    (3, "A plataforma consome o time comercial", "Confirmada",
     "Biometria (10+), senha (11+), responsável não encontrado (16+). OP1 em ~60% dos casos."),
    (4, "Concorrência protege — mas o timing é tudo", "Revisada",
     "B10 tem correlação NEGATIVA (−13,1pp). Precisa vir antes da decisão. Novo concorrente: Carro Zero."),
    (5, "57% das ligações são suporte puro", "Confirmada",
     "728 de 1.275 (56,7%) = não era venda. 30,2% da base com score zero."),
]
s = new_slide()
add_header(s, "9 Hipóteses (1 de 2)", "O que fecha um contrato", kicker="6 · RESULTADOS IA")
add_hipotese_cards(s, 1.75, hip1, cols=3)
add_footer(s, 16)

hip2 = [
    (6, "Localiza Pesados é invisível", "Nova",
     "Cliente com caminhões nunca recebeu oferta. Quantos dos 1.109 clientes têm frota mista?"),
    (7, "Biometria é vazamento de receita mensurável", "Nova",
     "10% das ligações em suporte de plataforma = ~10 vendas perdidas/semana, de forma silenciosa."),
    (8, "Referral nunca é pedido", "Nova",
     "OP4 sistemático nos 23 batches. A abertura existe; a pergunta nunca é feita."),
    (9, "WhatsApp virou o pseudo-fechamento", "Nova",
     "PM2 = 56,2% de todas as promessas, quase 100% sem prazo. Pipeline gerenciado pela memória do vendedor."),
]
s = new_slide()
add_header(s, "9 Hipóteses (2 de 2)", "O que fecha um contrato", kicker="6 · RESULTADOS IA")
add_hipotese_cards(s, 1.75, hip2, cols=2)
add_footer(s, 17)

# ===========================================================================
# SLIDE 18 — NOVO LOTE: STATUS
# ===========================================================================
s = new_slide()
add_header(s, "Novo Lote em Processamento", "5.348 ligações recebidas em 01/07/2026", kicker="6 · RESULTADOS IA")
status_bullets = [
    ("Scoring automático: ", "completo. Validou a distribuição de potencial da base original (seção 5).", 0),
    ("Análise via IA (desfecho, Challenger, R$): ", "em andamento, rodando no free tier do Gemini (cota diária limitada).", 0),
    ("Prioridade: ", "P1_P2 (desfecho + B1-B10) primeiro, depois P5_P6 (Challenger), depois P9_P10 (abertura/fechamento).", 0),
    ("Previsão: ", "P1_P2 completo por volta de 05-07/07/2026; demais grupos seguem conforme a cota permitir.", 0),
]
add_bullets(s, 0.8, 1.9, 11.7, 2.5, status_bullets, size=13, line_spacing=1.4, space_after=14)
box = s.shapes.add_shape(1, Inches(0.8), Inches(4.6), Inches(11.7), Inches(1.3))
box.fill.solid()
box.fill.fore_color.rgb = RGBColor(0xFE, 0xF9, 0xC3)
box.line.fill.background()
tf = box.text_frame
tf.word_wrap = True
tf.margin_left = Inches(0.25)
tf.margin_top = Inches(0.15)
p = tf.paragraphs[0]
p.alignment = PP_ALIGN.LEFT
r = p.add_run()
r.text = "Importante: "
r.font.bold = True
r.font.size = Pt(12.5)
r.font.color.rgb = RGBColor(0x71, 0x3F, 0x12)
r.font.name = FONTE
r2 = p.add_run()
r2.text = ("os números de desfecho, hipóteses e R$28.490/mês apresentados neste documento ainda se "
           "referem apenas à base original de 1.275 ligações. Serão atualizados quando o novo lote terminar.")
r2.font.size = Pt(12.5)
r2.font.color.rgb = RGBColor(0x71, 0x3F, 0x12)
r2.font.name = FONTE
add_footer(s, 18)

# ===========================================================================
# SLIDE 19 — PROXIMOS PASSOS
# ===========================================================================
s = new_slide()
add_header(s, "Prioridades e Próximos Passos", "O que fazer com esses dados", kicker="7 · PLANO DE AÇÃO")
add_table(s, 0.5, 1.5, 12.3, 5.3,
          ["Ação", "Prazo", "Impacto esperado"],
          [
              ["Ligar para os 5 clientes críticos", "Hoje", "Retenção ou captura de expansão imediata"],
              ["Escalar biometria para produto/operações", "Esta semana", "Libera ~10% da capacidade comercial"],
              ["Treinar CH1 — revelar custo oculto", "2 semanas", "+2,5pp em B6 — mecanismo de urgência com evidência"],
              ["Inserir pergunta comercial em suporte (OP1)", "2 semanas", "~60% sem sondagem — melhora tem impacto imediato"],
              ["Treinar fechamento com data (OP3)", "2 semanas", "FC3 de 44,8% para meta abaixo de 20%"],
              ["Inserir pedido de referral (OP4)", "2 semanas", "Leads qualificados sem custo, hoje esquecido"],
              ["Treinar B5 — upsell conectado à dor", "2 semanas", "+7,4pp — maior diferencial identificado"],
              ["Script de sondagem de frota pesada", "2 semanas", "Abertura de mercado nos 1.109 clientes"],
              ["Concluir análise IA do novo lote", "Em andamento", "Dobra a amostra, valida hipóteses em escala maior"],
          ],
          col_widths=[5.0, 1.8, 5.5], font_size=10.5, header_size=11)
add_footer(s, 19)

# ===========================================================================
OUT = Path(__file__).parent.parent / "apresentacao" / "Aletheia_Apresentacao_Completa.pptx"
prs.save(str(OUT))
print(f"Salvo: {OUT} ({len(prs.slides)} slides)")
