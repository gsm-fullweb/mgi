from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    KeepTogether,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(r"C:\Users\Richard Wagner\Documents\Grupo MGI")
OUTPUT = ROOT / "outputs" / "propostas" / "PROPOSTA-RENOVACAO-SEO-GRUPO-MGI-12-MESES.pdf"

NAVY = colors.HexColor("#103754")
BLUE = colors.HexColor("#176A9A")
ORANGE = colors.HexColor("#F28C28")
INK = colors.HexColor("#263746")
MUTED = colors.HexColor("#667887")
PALE = colors.HexColor("#EDF4F8")
LIGHT = colors.HexColor("#F7F9FB")
GREEN = colors.HexColor("#23865C")
WHITE = colors.white


def register_fonts():
    fonts = Path(r"C:\Windows\Fonts")
    pdfmetrics.registerFont(TTFont("Arial", str(fonts / "arial.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Bold", str(fonts / "arialbd.ttf")))
    pdfmetrics.registerFont(TTFont("Arial-Italic", str(fonts / "ariali.ttf")))


register_fonts()

styles = getSampleStyleSheet()
styles.add(
    ParagraphStyle(
        "TitleMGI",
        fontName="Arial-Bold",
        fontSize=28,
        leading=33,
        textColor=WHITE,
        spaceAfter=8,
    )
)
styles.add(
    ParagraphStyle(
        "SubtitleMGI",
        fontName="Arial",
        fontSize=13,
        leading=19,
        textColor=colors.HexColor("#DCEAF2"),
    )
)
styles.add(
    ParagraphStyle(
        "H1MGI",
        fontName="Arial-Bold",
        fontSize=18,
        leading=22,
        textColor=NAVY,
        spaceBefore=5,
        spaceAfter=10,
    )
)
styles.add(
    ParagraphStyle(
        "H2MGI",
        fontName="Arial-Bold",
        fontSize=12,
        leading=16,
        textColor=BLUE,
        spaceBefore=7,
        spaceAfter=5,
    )
)
styles.add(
    ParagraphStyle(
        "BodyMGI",
        fontName="Arial",
        fontSize=9.4,
        leading=14,
        textColor=INK,
        spaceAfter=6,
    )
)
styles.add(
    ParagraphStyle(
        "SmallMGI",
        fontName="Arial",
        fontSize=7.8,
        leading=11,
        textColor=MUTED,
    )
)
styles.add(
    ParagraphStyle(
        "BulletMGI",
        fontName="Arial",
        fontSize=9.2,
        leading=13.5,
        textColor=INK,
        leftIndent=13,
        firstLineIndent=-7,
        bulletIndent=4,
        spaceAfter=3,
    )
)
styles.add(
    ParagraphStyle(
        "CardTitle",
        fontName="Arial-Bold",
        fontSize=11,
        leading=14,
        textColor=NAVY,
        alignment=TA_CENTER,
    )
)
styles.add(
    ParagraphStyle(
        "HeaderCell",
        fontName="Arial-Bold",
        fontSize=9,
        leading=12,
        textColor=WHITE,
        alignment=TA_CENTER,
    )
)
styles.add(
    ParagraphStyle(
        "CardPrice",
        fontName="Arial-Bold",
        fontSize=16,
        leading=19,
        textColor=ORANGE,
        alignment=TA_CENTER,
    )
)
styles.add(
    ParagraphStyle(
        "CenterSmall",
        fontName="Arial",
        fontSize=8,
        leading=11,
        textColor=INK,
        alignment=TA_CENTER,
    )
)
styles.add(
    ParagraphStyle(
        "QuoteMGI",
        fontName="Arial-Italic",
        fontSize=8.7,
        leading=13,
        textColor=INK,
        leftIndent=10,
        rightIndent=10,
        borderColor=ORANGE,
        borderWidth=0,
        borderPadding=8,
        backColor=PALE,
    )
)


def p(text, style="BodyMGI"):
    return Paragraph(text, styles[style])


def bullets(items):
    return [p(f"• {item}", "BulletMGI") for item in items]


def section(title):
    return [p(title, "H1MGI"), Table([[""]], colWidths=[170 * mm], rowHeights=[1.2 * mm],
                                    style=TableStyle([("BACKGROUND", (0, 0), (-1, -1), ORANGE)])), Spacer(1, 4 * mm)]


def header_footer(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, height - 15 * mm, width, 15 * mm, fill=1, stroke=0)
    canvas.setFont("Arial-Bold", 8)
    canvas.setFillColor(WHITE)
    canvas.drawString(20 * mm, height - 9.5 * mm, "GRUPO MGI  |  SEO, CONTEÚDO E GERAÇÃO DE LEADS")
    canvas.setFillColor(colors.HexColor("#CCDDE8"))
    canvas.setFont("Arial", 7)
    canvas.drawRightString(width - 20 * mm, height - 9.5 * mm, "Proposta comercial • 27/07/2026")
    canvas.setStrokeColor(colors.HexColor("#D8E2E8"))
    canvas.line(20 * mm, 13 * mm, width - 20 * mm, 13 * mm)
    canvas.setFont("Arial", 7)
    canvas.setFillColor(MUTED)
    canvas.drawString(20 * mm, 8 * mm, "Documento confidencial • Validade: 15 dias")
    canvas.drawRightString(width - 20 * mm, 8 * mm, f"Página {doc.page}")
    canvas.restoreState()


def cover(canvas, doc):
    canvas.saveState()
    width, height = A4
    canvas.setFillColor(NAVY)
    canvas.rect(0, 0, width, height, fill=1, stroke=0)
    canvas.setFillColor(BLUE)
    canvas.circle(width + 15 * mm, height - 34 * mm, 58 * mm, fill=1, stroke=0)
    canvas.setFillColor(ORANGE)
    canvas.rect(0, 0, width, 9 * mm, fill=1, stroke=0)
    canvas.setFillColor(colors.HexColor("#215374"))
    canvas.rect(18 * mm, height - 51 * mm, 36 * mm, 3 * mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Arial-Bold", 13)
    canvas.drawString(18 * mm, height - 43 * mm, "GRUPO MGI")
    canvas.setFont("Arial-Bold", 28)
    canvas.drawString(18 * mm, height - 91 * mm, "SEO, CONTEÚDO")
    canvas.drawString(18 * mm, height - 104 * mm, "E GERAÇÃO DE LEADS")
    canvas.setFillColor(colors.HexColor("#DCEAF2"))
    canvas.setFont("Arial", 14)
    canvas.drawString(18 * mm, height - 120 * mm, "Expansão para todo o portfólio e site corporativo")
    canvas.setFillColor(ORANGE)
    canvas.roundRect(18 * mm, height - 158 * mm, 67 * mm, 17 * mm, 3 * mm, fill=1, stroke=0)
    canvas.setFillColor(WHITE)
    canvas.setFont("Arial-Bold", 12)
    canvas.drawCentredString(51.5 * mm, height - 151.5 * mm, "PROJETO DE 12 MESES")
    canvas.setFillColor(colors.HexColor("#BFD3DF"))
    canvas.setFont("Arial", 9)
    canvas.drawString(18 * mm, 29 * mm, "mgi.com.br")
    canvas.drawRightString(width - 18 * mm, 29 * mm, "27 de julho de 2026")
    canvas.restoreState()


doc = BaseDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    leftMargin=20 * mm,
    rightMargin=20 * mm,
    topMargin=22 * mm,
    bottomMargin=18 * mm,
    title="Proposta SEO Grupo MGI — 12 meses",
    author="Cuidar Connect",
)

frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
doc.addPageTemplates(
    [
        PageTemplate(id="Cover", frames=frame, onPage=cover),
        PageTemplate(id="Content", frames=frame, onPage=header_footer),
    ]
)

story = [Spacer(1, 230 * mm), PageBreak()]
doc.handle_nextPageTemplate("Content")

story += section("1. Resumo executivo")
story += [
    p(
        "O projeto atual está concentrado em <b>locação de impressoras e outsourcing de impressão</b>. "
        "A nova etapa amplia a responsabilidade para o site institucional, soluções, locações, serviços, "
        "softwares, cases, blog e páginas de geração de leads."
    ),
    p(
        "A expansão envolve mais de 20 frentes comerciais. Por isso, a proposta deixa de ser uma ação de uma "
        "única vertical e passa a ser uma <b>operação corporativa contínua de aquisição orgânica</b>, com "
        "arquitetura, conteúdo, landing pages, SEO técnico, conversão e mensuração."
    ),
]

summary_table = Table(
    [
        [p("ESCOPO ANTERIOR", "CardTitle"), p("NOVO ESCOPO", "CardTitle"), p("RECOMENDAÇÃO", "CardTitle")],
        [
            p("1 vertical<br/>Outsourcing de impressão", "CenterSmall"),
            p("Site completo<br/>+20 frentes comerciais", "CenterSmall"),
            p("<b>Plano Crescimento</b><br/>12 meses", "CenterSmall"),
        ],
        [
            p("R$ 3.000/mês", "CardPrice"),
            p("Operação integrada", "CardPrice"),
            p("R$ 9.800/mês", "CardPrice"),
        ],
    ],
    colWidths=[56 * mm, 56 * mm, 56 * mm],
    rowHeights=[13 * mm, 23 * mm, 20 * mm],
)
summary_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), PALE),
            ("BACKGROUND", (2, 1), (2, -1), colors.HexColor("#FFF4E8")),
            ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#C9D7E0")),
            ("INNERGRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D7E1E7")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ]
    )
)
story += [Spacer(1, 4 * mm), summary_table, Spacer(1, 6 * mm)]
story += [p("Objetivos principais", "H2MGI")]
story += bullets(
    [
        "Aumentar a presença orgânica do Grupo MGI no Google e em mecanismos de busca com IA;",
        "Criar páginas orientadas às intenções de compra de cada produto e serviço;",
        "Gerar oportunidades qualificadas por formulário, telefone e WhatsApp;",
        "Organizar produtos em clusters e fortalecer a autoridade temática do domínio;",
        "Medir a contribuição do tráfego orgânico para a geração de demanda.",
    ]
)

story.append(PageBreak())
story += section("2. Abrangência do novo projeto")

portfolio = [
    ["Soluções", "Locações", "Serviços e software"],
    [
        "Concessão de crédito<br/>Apontamento de produção<br/>Automação da força de vendas<br/>Comprovação de entrega<br/>Emissão de contas em campo<br/>Gestão eletrônica de documentos",
        "Outsourcing de impressão<br/>Notebooks e dispositivos móveis<br/>Tablets e smartphones<br/>Notebooks, tablets, celulares e coletores robustos",
        "Assistência técnica<br/>Proteção total<br/>Contratos de manutenção<br/>Personalização inicial<br/>MyIN<br/>Mototalk",
    ],
    [
        "Operação de loja<br/>Ordem de serviço em campo<br/>Prontuário eletrônico<br/>PDV<br/>Suporte e mentoria remota<br/>WMS",
        "Landing pages locais e setoriais<br/>Páginas de conversão",
        "Site institucional<br/>Cases<br/>Blog<br/>Contato e conversões",
    ],
]
portfolio_table = Table(
    [[p(c, "HeaderCell") for c in portfolio[0]]]
    + [[p(c, "SmallMGI") for c in row] for row in portfolio[1:]],
    colWidths=[56 * mm] * 3,
)
portfolio_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("BACKGROUND", (0, 1), (-1, -1), LIGHT),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CDD9E0")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 7),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ]
    )
)
story += [portfolio_table, Spacer(1, 6 * mm)]
story += [p("Princípio de priorização", "H2MGI")]
story += [
    p(
        "O portfólio não será trabalhado de forma aleatória. A cada trimestre, as frentes serão classificadas "
        "por potencial de busca, valor comercial, maturidade da oferta, concorrência e capacidade de atendimento. "
        "Essa priorização concentra esforço onde há maior chance de gerar demanda."
    ),
    p(
        "<b>Importante:</b> a inclusão de todo o site significa responsabilidade estratégica sobre o conjunto, "
        "mas a produção mensal permanece limitada pela capacidade contratada em cada plano."
    ),
]

story.append(PageBreak())
story += section("3. Escopo recomendado — Plano Crescimento")

scope_groups = [
    (
        "Estratégia e arquitetura",
        [
            "Auditoria técnica, de conteúdo e conversão;",
            "Pesquisa de palavras-chave por produto, segmento e região;",
            "Arquitetura de páginas e clusters temáticos;",
            "Planejamento editorial e priorização trimestral;",
            "Análise periódica de concorrentes orgânicos.",
        ],
    ),
    (
        "SEO técnico e manutenção",
        [
            "Indexação, sitemap, robots.txt, canonicals e redirecionamentos;",
            "Exclusões do Search Console e páginas alternativas com canonical;",
            "Títulos, descrições, headings, links internos e URLs;",
            "Dados estruturados aplicáveis;",
            "Search Console, Analytics e saúde técnica;",
            "Até 10 horas mensais de ajustes em WordPress, não cumulativas.",
        ],
    ),
    (
        "Páginas comerciais e conversão",
        [
            "Manutenção dos ativos e landing pages existentes;",
            "Até 2 novas páginas comerciais ou landing pages por mês;",
            "Até 8 páginas existentes otimizadas por mês;",
            "Copywriting, CTAs, formulários e recomendações de CRO;",
            "Integração com canais já disponíveis no site.",
        ],
    ),
    (
        "Conteúdo, autoridade e gestão",
        [
            "Até 4 artigos de blog por mês;",
            "1 case por trimestre, com insumos e aprovação da MGI;",
            "Conteúdo preparado para busca tradicional e mecanismos com IA;",
            "Painel, relatório executivo e reunião mensal;",
            "Revisão trimestral de prioridades e metas.",
        ],
    ),
]

for index in range(0, len(scope_groups), 2):
    row = []
    for title, items in scope_groups[index : index + 2]:
        content = [p(title, "H2MGI")] + bullets(items)
        row.append(content)
    table = Table([row], colWidths=[83 * mm, 83 * mm])
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
                ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#D0DCE3")),
                ("INNERGRID", (0, 0), (-1, -1), 0.6, colors.HexColor("#D0DCE3")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story += [table, Spacer(1, 4 * mm)]

story += [
    p(
        "<b>Capacidade anual do plano:</b> até 24 novas páginas comerciais, 48 artigos, 96 otimizações "
        "de páginas existentes, 120 horas de WordPress e 4 cases, respeitando os limites mensais."
    ),
    p(
        "A correção técnica inclui robots.txt, sitemap, canonicals, duplicidades e exclusões do Search Console "
        "dentro da capacidade mensal. Desenvolvimento personalizado, servidor, banco de dados, tema ou código "
        "de terceiros que exceda essa capacidade será diagnosticado e orçado separadamente."
    )
]

story.append(PageBreak())
story += section("4. Plano de trabalho — 12 meses")

roadmap = [
    ["Período", "Foco", "Principais entregas"],
    [
        "Meses 1–2",
        "Fundamentos",
        "Auditoria completa; inventário de páginas; analytics e conversões; palavras-chave; clusters; correções críticas; prioridades.",
    ],
    [
        "Meses 3–5",
        "Maior potencial",
        "Páginas comerciais prioritárias; landing pages; links internos; dados estruturados; conteúdos de apoio; CTAs e formulários.",
    ],
    [
        "Meses 6–9",
        "Escala e autoridade",
        "Expansão para outras linhas; publicação recorrente; cases; páginas com potencial e baixa conversão; consolidação dos clusters.",
    ],
    [
        "Meses 10–12",
        "Consolidação",
        "Revisão de desempenho; atualização de conteúdos; otimização para IA; correção de canibalização; plano do ciclo seguinte.",
    ],
]
roadmap_table = Table(
    [[p(c, "HeaderCell") for c in roadmap[0]]]
    + [[p(row[0], "CenterSmall"), p(row[1], "CenterSmall"), p(row[2], "SmallMGI")] for row in roadmap[1:]],
    colWidths=[25 * mm, 36 * mm, 107 * mm],
    rowHeights=[12 * mm, 30 * mm, 30 * mm, 30 * mm, 30 * mm],
)
roadmap_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("BACKGROUND", (0, 1), (-1, -1), LIGHT),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD7DE")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
        ]
    )
)
story += [roadmap_table, Spacer(1, 6 * mm)]
story += [p("Ritmo de gestão", "H2MGI")]
story += bullets(
    [
        "Planejamento detalhado no início de cada trimestre;",
        "Execução e publicações ao longo de cada mês;",
        "Relatório e reunião mensal de acompanhamento;",
        "Ajustes de prioridade conforme dados e necessidades comerciais.",
    ]
)

story.append(PageBreak())
story += section("5. Opções de investimento")

cards = []
plans = [
    ("ESSENCIAL", "R$ 7.500/mês", "Implantação: R$ 8.000<br/><b>Total anual: R$ 98.000</b>", False),
    ("CRESCIMENTO", "R$ 9.800/mês", "Implantação: R$ 12.000<br/><b>Total anual: R$ 129.600</b>", True),
    ("PERFORMANCE", "R$ 13.500/mês", "Implantação: R$ 18.000<br/><b>Total anual: R$ 180.000</b>", False),
]
for name, price, detail, recommended in plans:
    label = f"{name}<br/><font color='#23865C'>RECOMENDADO</font>" if recommended else name
    cards.append([p(label, "CardTitle"), p(price, "CardPrice"), p(detail, "CenterSmall")])

cards_table = Table([cards], colWidths=[56 * mm] * 3, rowHeights=[51 * mm])
card_style = [
    ("BACKGROUND", (0, 0), (-1, -1), LIGHT),
    ("BOX", (0, 0), (-1, -1), 0.7, colors.HexColor("#C7D5DE")),
    ("INNERGRID", (0, 0), (-1, -1), 0.7, colors.HexColor("#C7D5DE")),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
]
card_style.append(("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#EAF6F0")))
card_style.append(("BOX", (1, 0), (1, 0), 1.5, GREEN))
cards_table.setStyle(TableStyle(card_style))
story += [cards_table, Spacer(1, 6 * mm)]

compare = [
    ["Entrega", "Essencial", "Crescimento", "Performance"],
    ["Novas páginas/mês", "1", "2", "4"],
    ["Artigos/mês", "2", "4", "6"],
    ["Otimizações/mês", "5", "8", "15"],
    ["Horas WordPress/mês", "6", "10", "18"],
    ["Cases", "—", "1/trimestre", "2/trimestre"],
    ["Reuniões", "Mensal", "Mensal", "Quinzenal"],
]
compare_table = Table(
    [[p(c, "HeaderCell") for c in compare[0]]]
    + [[p(row[0], "SmallMGI")] + [p(c, "CenterSmall") for c in row[1:]] for row in compare[1:]],
    colWidths=[55 * mm, 37 * mm, 39 * mm, 37 * mm],
)
compare_table.setStyle(
    TableStyle(
        [
            ("BACKGROUND", (0, 0), (-1, 0), NAVY),
            ("TEXTCOLOR", (0, 0), (-1, 0), WHITE),
            ("BACKGROUND", (2, 1), (2, -1), colors.HexColor("#EAF6F0")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [WHITE, PALE]),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CAD6DD")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 6),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ]
    )
)
story += [compare_table, Spacer(1, 5 * mm)]
story += [
    p(
        "<b>Recomendação:</b> o Plano Crescimento oferece capacidade adequada para trabalhar o portfólio completo "
        "sem transformar a operação em demanda ilimitada."
    )
]

story.append(PageBreak())
story += section("6. Indicadores, responsabilidades e limites")
story += [p("Indicadores acompanhados", "H2MGI")]
story += bullets(
    [
        "Cliques, impressões, posições e tráfego orgânico qualificado;",
        "Conversões por formulário, telefone e WhatsApp, quando mensuráveis;",
        "Taxa de conversão e leads atribuídos ou assistidos pelo orgânico;",
        "Indexação, saúde técnica e evolução dos clusters prioritários;",
        "Entregas realizadas, aprendizados e oportunidades do próximo ciclo.",
    ]
)
story += [p("Responsabilidades da MGI", "H2MGI")]
story += bullets(
    [
        "Fornecer acessos, informações comerciais, imagens e materiais técnicos;",
        "Indicar responsável para prioridades e aprovações em até 5 dias úteis;",
        "Garantir atendimento e registro adequado dos leads recebidos;",
        "Disponibilizar especialistas e clientes para cases, quando aplicável;",
        "Autorizar custos externos de ferramentas, plugins, mídia ou desenvolvimento.",
    ]
)
story += [p("Não incluído", "H2MGI")]
story += bullets(
    [
        "Redesign completo, sistemas, e-commerce, integrações complexas ou área restrita;",
        "Desenvolvimento personalizado que exceda a capacidade mensal ou dependa de tema, plugin, servidor ou terceiros;",
        "Servidor, hospedagem, segurança, correção de invasões ou suporte 24 horas;",
        "Licenças, plugins, imagens, ferramentas e mídia paga;",
        "Redes sociais, e-mail marketing, CRM, automações e atendimento dos leads;",
        "Produção ilimitada de páginas, artigos, alterações ou reuniões.",
    ]
)
story += [
    p(
        "Demandas fora do escopo serão avaliadas e orçadas antes da execução. Entregas e horas mensais não "
        "utilizadas não são cumulativas."
    )
]

story.append(PageBreak())
story += section("7. Condições e transição contratual")
story += [p("Condições comerciais", "H2MGI")]
story += bullets(
    [
        "Vigência de 12 meses;",
        "Implantação: 50% na assinatura e 50% na conclusão da fase inicial, em até 30 dias;",
        "Mensalidades com vencimento em data acordada;",
        "Reajuste após 12 meses pelo IPCA acumulado, ou índice substituto;",
        "Rescisão e multas bilaterais e proporcionais no novo contrato;",
        "Mudanças relevantes de plataforma, arquitetura, volume ou escopo podem gerar revisão comercial.",
    ]
)
story += [p("Substituição do contrato atual", "H2MGI")]
story += [
    p(
        "Para impedir duplicidade de pagamentos, escopos ou penalidades, recomenda-se inserir no novo contrato:",
        "BodyMGI",
    ),
    p(
        "“A partir da data de vigência deste instrumento, fica substituído integralmente, por acordo entre as "
        "partes e sem aplicação de multa rescisória, o contrato de SEO anteriormente firmado para o projeto "
        "MGI — Outsourcing de Impressão. Os ativos já produzidos permanecem integrados ao novo escopo, "
        "considerando-se cumpridas e quitadas as obrigações anteriores até a data de transição, ressalvados "
        "os valores vencidos e não pagos.”",
        "QuoteMGI",
    ),
    Spacer(1, 5 * mm),
    p(
        "O contrato definitivo deve conter anexo de escopo, limites mensais, critérios de aprovação, "
        "responsabilidades, propriedade dos entregáveis e limite de responsabilidade compatível com o valor contratado."
    ),
]
story += [p("Observação sobre resultados", "H2MGI")]
story += [
    p(
        "SEO é uma obrigação de meio. Resultados dependem da concorrência, algoritmos, autoridade do domínio, "
        "condições técnicas, aprovações e atendimento comercial. Não há garantia de posição, tráfego, leads ou faturamento."
    )
]

story.append(PageBreak())
story += section("8. Aprovação e próximos passos")
story += bullets(
    [
        "Escolha do plano e confirmação das prioridades comerciais;",
        "Aprovação desta proposta;",
        "Assinatura do novo contrato e formalização da substituição do contrato atual;",
        "Kickoff, acessos e diagnóstico dos primeiros 90 dias.",
    ]
)
story += [Spacer(1, 10 * mm)]

approval = Table(
    [
        [p("Plano escolhido", "SmallMGI"), ""],
        [p("Pela MGI", "SmallMGI"), ""],
        [p("Nome e cargo", "SmallMGI"), ""],
        [p("Data", "SmallMGI"), ""],
        [p("Pela contratada", "SmallMGI"), ""],
        [p("Data", "SmallMGI"), ""],
    ],
    colWidths=[40 * mm, 128 * mm],
    rowHeights=[16 * mm] * 6,
)
approval.setStyle(
    TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#C9D6DE")),
            ("BACKGROUND", (0, 0), (0, -1), PALE),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 7),
        ]
    )
)
story += [approval, Spacer(1, 12 * mm)]
story += [
    p(
        "<b>Investimento recomendado:</b> R$ 12.000 de implantação + 12 mensalidades de R$ 9.800.<br/>"
        "<b>Total do projeto:</b> R$ 129.600.",
        "QuoteMGI",
    )
]

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
doc.build(story)
print(OUTPUT)
