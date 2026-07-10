"""
Gera apresentacao/RMR_Diretoria_5slides.pptx a partir de apresentacao/CONTEUDO_5SLIDES_DIRETORIA.md,
usando o design de apresentacao/RMR_Padrao_3slides.pptx como referencia visual:
- Header executivo: logo "ALETHEIA RAC" (topo direita), titulo em paragrafo unico
  (frase forte em negrito + continuacao com os dados em texto regular), linha
  divisoria fina, eyebrow (legenda em caixa alta) centralizada.
- Rodape centralizado com a assinatura padrao Aletheia RAC.
- Fundo branco, fonte Segoe UI, paleta: preto #1A1A1A, cinza #444444/#8A8A8A,
  azul de destaque #2A78D6, linhas #E4E4E2.
"""
from pptx import Presentation
from pptx.util import Emu, Pt, Inches
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

FONT = "Segoe UI"

PRETO = RGBColor(0x1A, 0x1A, 0x1A)
CINZA_TXT = RGBColor(0x44, 0x44, 0x44)
CINZA_CLARO = RGBColor(0x8A, 0x8A, 0x8A)
AZUL = RGBColor(0x2A, 0x78, 0xD6)
LINHA = RGBColor(0xE4, 0xE4, 0xE2)
BRANCO = RGBColor(0xFF, 0xFF, 0xFF)
CARD_BG = RGBColor(0xF7, 0xF7, 0xF7)

SLIDE_W = Emu(12191695)
SLIDE_H = Emu(6858000)

MARGEM_X = Emu(502920)
LARGURA_CONTEUDO = Emu(11183112)
DIREITA = Emu(502920 + 11183112)

FOOTER_TXT = ("Aletheia RAC — Inteligência Comercial Frota PJ — base auditada de "
              "6.623 ligações (jun–jul/2026) — RMR 09/07/2026")


def set_run(r, text, size, bold=False, italic=False, color=PRETO, font=FONT):
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.name = font
    r.font.color.rgb = color
    return r


def add_header(slide, eyebrow, title_bold, title_regular):
    # logo
    logo = slide.shapes.add_textbox(Emu(10332720), Emu(320040), Emu(1463040), Emu(822960))
    tf = logo.text_frame
    tf.word_wrap = True
    p1 = tf.paragraphs[0]
    p1.alignment = PP_ALIGN.RIGHT
    set_run(p1.add_run(), "ALETHEIA", 15, bold=True, color=PRETO)
    p2 = tf.add_paragraph()
    p2.alignment = PP_ALIGN.RIGHT
    set_run(p2.add_run(), "RAC", 15, bold=True, color=AZUL)

    # titulo (paragrafo unico: frase forte + continuacao com dados)
    tbox = slide.shapes.add_textbox(MARGEM_X, Emu(320040), Emu(9509760), Emu(1371600))
    tf = tbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    set_run(p.add_run(), title_bold, 13.5, bold=True, color=PRETO)
    set_run(p.add_run(), title_regular, 13.5, bold=False, color=CINZA_TXT)

    # linha divisoria
    line = slide.shapes.add_connector(1, MARGEM_X, Emu(1417320), DIREITA, Emu(1417320))
    line.line.color.rgb = LINHA
    line.line.width = Emu(9525)

    # eyebrow
    ebox = slide.shapes.add_textbox(MARGEM_X, Emu(1691640), Emu(10241280), Emu(320040))
    tf = ebox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    set_run(p.add_run(), eyebrow, 11.5, bold=False, color=CINZA_CLARO)


def add_footer(slide):
    fbox = slide.shapes.add_textbox(MARGEM_X, Emu(6473952), Emu(11155680), Emu(320040))
    tf = fbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    set_run(p.add_run(), FOOTER_TXT, 9.5, bold=False, color=CINZA_CLARO)


def new_slide(prs):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide.background.fill.solid()
    slide.background.fill.fore_color.rgb = BRANCO
    return slide


def add_rounded_card(slide, left, top, width, height, fill=CARD_BG, line_color=LINHA):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.adjustments[0] = 0.045
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill
    shape.line.color.rgb = line_color
    shape.line.width = Emu(9525)
    shape.shadow.inherit = False
    return shape


def add_accent_bar(slide, left, top, height, color=AZUL, width=Emu(41275)):
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    bar.fill.solid()
    bar.fill.fore_color.rgb = color
    bar.line.fill.background()
    bar.shadow.inherit = False
    return bar


def add_quote_card(slide, left, top, width, height, turns, attribution_bold, attribution_rest, insight=None):
    """turns: lista de (speaker, texto). speaker in {'Cliente','Vendedor','Vendedora'}."""
    add_rounded_card(slide, left, top, width, height)
    add_accent_bar(slide, left, top, height)

    pad_x = Emu(228600)
    inner_left = Emu(left + pad_x)
    inner_w = Emu(width - pad_x - Emu(160000))

    tbox = slide.shapes.add_textbox(inner_left, Emu(top + Emu(160000)), inner_w, Emu(height - Emu(320000)))
    tf = tbox.text_frame
    tf.word_wrap = True

    first = True
    for speaker, texto in turns:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(6)
        set_run(p.add_run(), f"{speaker}: ", 11.5, bold=True, color=PRETO)
        set_run(p.add_run(), f"“{texto}”", 11.5, bold=False, italic=True, color=CINZA_TXT)

    p = tf.add_paragraph()
    p.space_before = Pt(10)
    r = p.add_run()
    set_run(r, f"— {attribution_bold}", 10.5, bold=True, color=AZUL)
    r2 = p.add_run()
    set_run(r2, f" {attribution_rest}", 10.5, bold=False, color=CINZA_CLARO)

    if insight:
        p = tf.add_paragraph()
        p.space_before = Pt(8)
        set_run(p.add_run(), insight, 10.5, bold=False, italic=True, color=CINZA_TXT)


def add_number_card(slide, left, top, width, height, numero, texto):
    add_rounded_card(slide, left, top, width, height, fill=BRANCO)
    tbox = slide.shapes.add_textbox(Emu(left + Emu(228600)), Emu(top + Emu(160000)),
                                     Emu(width - Emu(457200)), Emu(height - Emu(320000)))
    tf = tbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    set_run(p.add_run(), numero, 26, bold=True, color=AZUL)
    p2 = tf.add_paragraph()
    p2.space_before = Pt(6)
    set_run(p2.add_run(), texto, 12, bold=False, color=PRETO)


def add_table_row(slide, y, cols, bold=False, color=PRETO, size=12):
    for (text, x, w, align) in cols:
        tbox = slide.shapes.add_textbox(Emu(x), Emu(y), Emu(w), Emu(320040))
        tf = tbox.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = align
        set_run(p.add_run(), text, size, bold=bold, color=color)


def add_separator(slide, y, x0=MARGEM_X, x1=None, color=LINHA, weight=6350):
    if x1 is None:
        x1 = Emu(x0 + Emu(6900000))
    line = slide.shapes.add_connector(1, x0, Emu(y), x1, Emu(y))
    line.line.color.rgb = color
    line.line.width = Emu(weight)


def add_section_label(slide, left, top, width, text):
    tbox = slide.shapes.add_textbox(left, top, width, Emu(320040))
    tf = tbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    set_run(p.add_run(), text, 12, bold=True, color=PRETO)
    add_separator(slide, top + 320040, x0=left, x1=Emu(left + width), color=LINHA, weight=9525)
    return Emu(top + 320040 + 91440)


def add_bullet_list(slide, left, top, width, items, font_size=12, gap=Pt(10)):
    """items: lista de strings simples, com marcador de destaque em azul."""
    tbox = slide.shapes.add_textbox(left, top, width, Emu(4000000))
    tf = tbox.text_frame
    tf.word_wrap = True
    first = True
    for texto in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = gap
        set_run(p.add_run(), "●  ", font_size, bold=False, color=AZUL)
        set_run(p.add_run(), texto, font_size, bold=False, color=CINZA_TXT)


def add_next_steps(slide, left, top, width, items, font_size=12, gap=Pt(10)):
    """items: lista de tuplas (texto, prazo)."""
    tbox = slide.shapes.add_textbox(left, top, width, Emu(4000000))
    tf = tbox.text_frame
    tf.word_wrap = True
    first = True
    for i, (texto, prazo) in enumerate(items, start=1):
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.space_after = Pt(2)
        set_run(p.add_run(), f"{i}. ", font_size, bold=True, color=AZUL)
        set_run(p.add_run(), texto, font_size, bold=False, color=PRETO)
        p2 = tf.add_paragraph()
        p2.space_after = gap
        set_run(p2.add_run(), f"     {prazo}", font_size - 1.5, bold=False, italic=True, color=CINZA_CLARO)


def build():
    prs = Presentation()
    prs.slide_width = SLIDE_W
    prs.slide_height = SLIDE_H

    body_top = Emu(2057400)
    body_bottom = Emu(6473952)

    def centered_top(height, region_top=None, region_bottom=body_bottom):
        region_top = Emu(body_top + Emu(320040)) if region_top is None else region_top
        avail = region_bottom - region_top
        return Emu(region_top + max(0, (avail - height) // 2))

    # ---------------- SLIDE 1 — Gancho ----------------
    s = new_slide(prs)
    add_header(
        s,
        "GANCHO — A PERGUNTA QUE ABRIU O PROJETO",
        "“O que o vendedor faz para fechar um contrato?” ",
        ("Pergunta feita pelo CEO/diretoria no início do projeto. 6.623 ligações analisadas por IA "
         "entre junho e julho de 2026 (1.275 da base piloto + 5.348 do lote seguinte) — não é amostra, "
         "99,6% já têm desfecho e comportamento mapeados."),
    )
    cards = [
        ("1", "O mercado real é menor do que parece"),
        ("2", "A plataforma consome tempo comercial que poderia ser venda"),
        ("3", "Não é um comportamento isolado — os bons comportamentos se somam"),
    ]
    gap = Emu(228600)
    card_w = Emu((11183112 - 2 * 228600) // 3)
    card_h = Inches(1.9)
    label_region_top = Emu(body_top + Emu(320040) + Emu(365760))
    card_top = centered_top(card_h, region_top=label_region_top)
    x = MARGEM_X
    for numero, texto in cards:
        add_number_card(s, x, card_top, card_w, card_h, numero, texto)
        x = Emu(x + card_w + gap)
    label = s.shapes.add_textbox(MARGEM_X, body_top, Emu(11183112), Emu(320040))
    tf = label.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    set_run(p.add_run(), "3 HIPÓTESES EMERGIRAM DOS DADOS (detalhe nos próximos slides)", 11, bold=True, color=CINZA_TXT)
    add_footer(s)

    # ---------------- SLIDE 2 — Hipótese 1 ----------------
    def hip_slide(eyebrow, title_bold, title_regular, quote_kwargs, quote_h=Inches(2.6)):
        sl = new_slide(prs)
        add_header(sl, eyebrow, title_bold, title_regular)
        top = centered_top(quote_h)
        add_quote_card(sl, MARGEM_X, top, Emu(11183112), quote_h, **quote_kwargs)
        add_footer(sl)
        return sl

    hip_slide(
        "HIPÓTESE 1 DE 3",
        "Antes de julgar o time, é preciso medir o esforço certo. ",
        ("57,4% das ligações não era venda (suporte, senha, cadastro, biometria), 37,3% interessou mas não "
         "fechou e apenas 5,1% fechou. Dentro do “não era venda”, 26,5% (1.002 ligações — 15% da base) "
         "eram prospecção nova sem tração, 90% iniciada pelo próprio vendedor."),
        dict(
            turns=[
                ("Cliente", "Eu queria saber, não sei se era no WhatsApp ou no e-mail, para eu poder fazer a "
                             "renovação, né? (...) Tá, eu vou mandar de novo, então, que é o link de prorrogação "
                             "do contrato, né?"),
            ],
            attribution_bold="Cliente 25966050",
            attribution_rest="· 170s · fechou renovação · score comercial: 0",
            insight=("Renovou por inércia — sem nenhum comportamento comercial. O contrato “fechou” "
                      "sozinho; o risco é que migre pra concorrência do mesmo jeito, por inércia, quando alguém "
                      "ligar primeiro com proposta ativa."),
        ),
    )

    # ---------------- SLIDE 3 — Hipótese 2 ----------------
    s = new_slide(prs)
    add_header(
        s,
        "HIPÓTESE 2 DE 3",
        "O vendedor virou suporte de sistema em boa parte do dia. ",
        ("65,6% dos problemas relatados se concentram em 4 tipos — faturamento/cobrança 19,3%, acesso/sistema "
         "18,2%, condutor/cadastro 16,1%, reserva/sistema 11,9%. 39,9% de toda oportunidade perdida da base é "
         "ligação que encerra sem nenhuma pergunta comercial."),
    )
    half_w = Emu((11183112 - 228600) // 2)
    card_h3 = Inches(2.4)
    card_top = centered_top(card_h3)
    add_quote_card(
        s, MARGEM_X, card_top, half_w, card_h3,
        turns=[("Cliente", "Estou tentando fazer uma reserva... a partir do momento que pede a nacionalidade "
                            "ele para e trava!")],
        attribution_bold="Cliente 17015435",
        attribution_rest="· bug confirmado no sistema",
        insight=("Vendedor só pode prometer avisar quando voltar. Ligação inteira de suporte a um problema que "
                  "não é do cliente nem do vendedor."),
    )
    add_quote_card(
        s, Emu(MARGEM_X + half_w + Emu(228600)), card_top, half_w, card_h3,
        turns=[("Cliente", "precisei alugar um carro, tive que passar no cartão... era tão fácil pela "
                            "plataforma.")],
        attribution_bold="Cliente 20148743",
        attribution_rest="· deixou de alugar por não acessar login/senha",
        insight="Receita perdida silenciosamente — não por preço ou produto, por acesso quebrado.",
    )
    add_footer(s)

    # ---------------- SLIDE 4 — Hipótese 3 ----------------
    s = new_slide(prs)
    add_header(
        s,
        "HIPÓTESE 3 DE 3 — A COMBINAÇÃO QUE MULTIPLICA O FECHAMENTO",
        "Duas coisas separam quem fecha: conectar o produto certo à dor do cliente, e mostrar por que a "
        "Localiza é melhor que a concorrência — com dado real, não papo genérico. ",
        ("Feitas juntas e bem executadas, multiplicam o fechamento por 6,25x sobre quem não faz nenhuma das "
         "duas. Uma tentativa malfeita de comparação com o concorrente fica abaixo da média da base — só a "
         "bem executada funciona."),
    )

    half_w = Emu((11183112 - 228600) // 2)
    left_x = MARGEM_X
    right_x = Emu(MARGEM_X + half_w + Emu(228600))

    label_top = Emu(body_top + Emu(320040))
    content_top = add_section_label(s, left_x, label_top, half_w, "A CONTA: DE 3,2% A 20,0%")

    col_combo_x = left_x
    col_combo_w = Emu(half_w * 62 // 100)
    col_n_x = Emu(left_x + col_combo_w)
    col_n_w = Emu(half_w * 16 // 100)
    col_taxa_x = Emu(col_n_x + col_n_w)
    col_taxa_w = Emu(half_w - col_combo_w - col_n_w)

    add_table_row(
        s, content_top,
        [
            ("COMBINAÇÃO DE COMPORTAMENTOS", col_combo_x, col_combo_w, PP_ALIGN.LEFT),
            ("N", col_n_x, col_n_w, PP_ALIGN.RIGHT),
            ("FECHOU", col_taxa_x, col_taxa_w, PP_ALIGN.RIGHT),
        ],
        bold=True, color=CINZA_CLARO, size=9,
    )
    add_separator(s, content_top + 320040, x0=left_x, x1=Emu(left_x + half_w), weight=12700, color=PRETO)

    linhas_combo = [
        ("Nenhum dos dois", "4.885", "3,2%", False),
        ("Upsell na dor, sozinho", "68", "13,2%", False),
        ("Boa comparação, sozinha", "1.228", "9,1%", False),
        ("Os dois juntos", "225", "20,0%", True),
    ]
    y = content_top + 320040 + 91440
    row_h = 448056
    for combo, n, taxa, destaque in linhas_combo:
        cor = AZUL if destaque else PRETO
        add_table_row(
            s, y,
            [
                (combo, col_combo_x, col_combo_w, PP_ALIGN.LEFT),
                (n, col_n_x, col_n_w, PP_ALIGN.RIGHT),
            ],
            bold=destaque, color=cor, size=12,
        )
        add_table_row(
            s, y, [(taxa, col_taxa_x, col_taxa_w, PP_ALIGN.RIGHT)],
            bold=True, color=cor, size=12,
        )
        add_separator(s, y + row_h - 45720, x0=left_x, x1=Emu(left_x + half_w), weight=6350)
        y += row_h

    result_top = Emu(y + 137160)
    add_rounded_card(s, left_x, result_top, half_w, Inches(0.8), fill=CARD_BG)
    rbox = s.shapes.add_textbox(Emu(left_x + 182880), Emu(result_top + 91440), Emu(half_w - 365760), Inches(0.62))
    tf = rbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    set_run(p.add_run(), "3,2% → 20,0% = ", 14, bold=False, color=CINZA_TXT)
    set_run(p.add_run(), "6,25x", 16, bold=True, color=AZUL)
    set_run(p.add_run(), " mais fechamento fazendo os dois, bem feitos", 12, bold=False, color=CINZA_TXT)

    quote_h = Emu(Emu(result_top + Inches(0.8)) - content_top)
    add_quote_card(
        s, right_x, content_top, half_w, quote_h,
        turns=[
            ("Cliente", "Eu posso fazer o pagamento pelo cartão da empresa? [...] eu precisaria que ele retirasse "
                        "se eu fizesse o pagamento por aqui ou faturado."),
            ("Vendedora", "O bom de ser faturado pra empresa é que o seu condutor vai retirar sem nenhuma "
                          "burocracia. Ele não tem que apresentar nenhum cartão nominal, nenhum pagamento de "
                          "caução — igual lá na pessoa física, que geralmente é duas vezes o valor da caução."),
        ],
        attribution_bold="Cliente 14683216",
        attribution_rest="· 1.180s · fechou novo contrato",
        insight=("Isso é comparação bem feita: conectou a dúvida específica do cliente a uma vantagem concreta "
                  "e verificável — não uma afirmação genérica de que “vale a pena”."),
    )

    note_top = Emu(result_top + Inches(0.8) + Emu(137160))
    nbox = s.shapes.add_textbox(MARGEM_X, note_top, Emu(11183112), Emu(320040))
    tf = nbox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    set_run(p.add_run(), "Já existe um guia de treinamento pronto sobre como executar bem essa comparação "
                          "(critério objetivo de 3 pontos, com exemplos reais bons e ruins da própria base) — "
                          "a análise já virou ação.", 10.5, bold=False, italic=True, color=CINZA_TXT)
    add_footer(s)

    # ---------------- SLIDE 5 — Portfólio ----------------
    s = new_slide(prs)
    add_header(
        s,
        "PORTFÓLIO — MENÇÕES NA BASE INTEIRA",
        "O cliente já fala do que quer comprar — só falta alguém perguntar. ",
        ("Contagem de menções na base inteira de 6.623 ligações: frota pesada, elétrico, telemetria e gestão de "
         "frota aparecem centenas de vezes — não é nicho, é conversa recorrente que o time já está tendo."),
    )
    tbl_top = Emu(body_top + Emu(320040))
    col_prod_x = MARGEM_X
    col_prod_w = Emu(2971800)
    col_piloto_x = Emu(3474720)
    col_piloto_w = Emu(1097280)
    col_novo_x = Emu(4663440)
    col_novo_w = Emu(1097280)
    col_total_x = Emu(5852160)
    col_total_w = Emu(1005840)
    tbl_w = Emu(col_total_x + col_total_w - col_prod_x)

    add_table_row(
        s, tbl_top,
        [
            ("PRODUTO", col_prod_x, col_prod_w, PP_ALIGN.LEFT),
            ("PILOTO (1.275)", col_piloto_x, col_piloto_w, PP_ALIGN.RIGHT),
            ("NOVO LOTE (5.348)", col_novo_x, col_novo_w, PP_ALIGN.RIGHT),
            ("TOTAL", col_total_x, col_total_w, PP_ALIGN.RIGHT),
        ],
        bold=True, color=CINZA_CLARO, size=9.5,
    )
    add_separator(s, tbl_top + 320040, x0=col_prod_x, x1=Emu(col_prod_x + tbl_w), weight=12700, color=PRETO)

    linhas = [
        ("Frota pesada / caminhão / picape", 175, 537),
        ("Elétrico / HB20 / TAO", 119, 383),
        ("Telemetria", 79, 341),
        ("Gestão de frota", 80, 288),
        ("Seminovos", 16, 45),
        ("ZARP", 1, 4),
        ("Meoo", 0, 0),
    ]
    y = tbl_top + 320040 + 91440
    row_h = 411480
    for nome, piloto, novo in linhas:
        total = piloto + novo
        add_table_row(
            s, y,
            [
                (nome, col_prod_x, col_prod_w, PP_ALIGN.LEFT),
                (f"{piloto}", col_piloto_x, col_piloto_w, PP_ALIGN.RIGHT),
                (f"{novo}", col_novo_x, col_novo_w, PP_ALIGN.RIGHT),
            ],
            bold=False, color=PRETO, size=11.5,
        )
        add_table_row(
            s, y,
            [(f"{total}", col_total_x, col_total_w, PP_ALIGN.RIGHT)],
            bold=True, color=AZUL, size=11.5,
        )
        add_separator(s, y + row_h - 45720, x0=col_prod_x, x1=Emu(col_prod_x + tbl_w), weight=6350)
        y += row_h

    quote_x = Emu(col_total_x + col_total_w + 274320)
    quote_w = Emu(DIREITA - quote_x)
    add_quote_card(
        s, quote_x, tbl_top, quote_w, Emu(body_bottom - tbl_top),
        turns=[
            ("Vendedor", "A gente também aluga pesado, cê sabia? Caminhão, picape. Olha, se você soubesse antes "
                         "talvez tivesse locado em vez de comprar o pequeno."),
            ("Cliente", "Me passa isso! Me passa a cotação disso aí."),
        ],
        attribution_bold="Cliente 22153452",
        attribution_rest="· 7-8 carros leves + 2 caminhões próprios fora da Localiza",
        insight=("Descoberto por acidente, numa pergunta de curiosidade — não por script. A consistência entre "
                  "amostras independentes já justifica testar um script de sondagem."),
    )
    add_footer(s)

    # ---------------- SLIDE 6 — Sumário executivo ----------------
    s = new_slide(prs)
    add_header(
        s,
        "SUMÁRIO EXECUTIVO",
        "Resumo do mês e próximos passos. ",
        ("6.623 ligações analisadas em junho–julho de 2026, taxa de fechamento de 5,1% — três hipóteses "
         "confirmadas sobre o que separa quem fecha de quem não fecha."),
    )
    col_gap = Emu(457200)
    col_w = Emu((11183112 - 457200) // 2)
    col_left_x = MARGEM_X
    col_right_x = Emu(MARGEM_X + col_w + col_gap)
    section_top = Emu(body_top + Emu(320040))

    content_top_l = add_section_label(s, col_left_x, section_top, col_w, "RESUMO DO MÊS")
    add_bullet_list(
        s, col_left_x, content_top_l, col_w,
        [
            "6.623 ligações analisadas por IA (jun–jul/2026) — 1.275 da base piloto + 5.348 do novo lote",
            "5,1% de taxa de fechamento — 57,4% das ligações nem era venda, o que exige medir o esforço "
            "sobre a base certa",
            "39,9% de toda oportunidade perdida é ligação que encerra sem nenhuma pergunta comercial — "
            "vendedor virando suporte de sistema",
            "Upsell ligado à dor do cliente + boa comparação com o concorrente, juntos, multiplicam o "
            "fechamento por 6,25x",
        ],
        font_size=12,
    )

    content_top_r = add_section_label(s, col_right_x, section_top, col_w, "PRIORIDADES E PRÓXIMOS PASSOS")
    add_next_steps(
        s, col_right_x, content_top_r, col_w,
        [
            ("Treinar upsell conectado à dor do cliente — guia já pronto", "2 semanas"),
            ("Tirar do vendedor os problemas de acesso/sistema e faturamento, hoje resolvidos na ligação "
             "comercial", "2 semanas"),
            ("Testar script de sondagem de portfólio (frota pesada, elétrico, telemetria, gestão de frota)",
             "2 semanas"),
            ("Concluir aprofundamento da análise na base combinada de 6.623 ligações", "Em andamento"),
        ],
        font_size=12,
    )
    add_footer(s)

    out = "apresentacao/RMR_Diretoria_5slides.pptx"
    prs.save(out)
    print("Gerado:", out, "-", len(prs.slides), "slides")


if __name__ == "__main__":
    build()
