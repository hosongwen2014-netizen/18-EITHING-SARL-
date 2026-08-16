import os
import cairosvg
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY

def generate_logo_png():
    svg_content = '''<svg width="760" height="520" viewBox="0 0 760 520" fill="none" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="panelBg" x1="80" y1="30" x2="700" y2="490" gradientUnits="userSpaceOnUse">
      <stop stop-color="#0E2C43"/>
      <stop offset="1" stop-color="#163E5D"/>
    </linearGradient>
    <linearGradient id="gold" x1="208" y1="122" x2="488" y2="408" gradientUnits="userSpaceOnUse">
      <stop stop-color="#F2D4A1"/>
      <stop offset="0.35" stop-color="#D6AA5E"/>
      <stop offset="0.7" stop-color="#B8843D"/>
      <stop offset="1" stop-color="#F7DFA8"/>
    </linearGradient>
    <linearGradient id="silver" x1="180" y1="330" x2="580" y2="450" gradientUnits="userSpaceOnUse">
      <stop stop-color="#F8F3EA"/>
      <stop offset="1" stop-color="#C5C5C5"/>
    </linearGradient>
  </defs>

  <rect x="40" y="40" width="680" height="430" rx="38" fill="url(#panelBg)"/>
  <rect x="40" y="40" width="680" height="430" rx="38" stroke="#C79A55" stroke-width="6"/>

  <g>
    <path d="M218 117C278 77 301 78 338 110C364 133 368 163 342 186C326 201 303 209 272 211C245 213 219 206 196 186C163 159 164 122 218 117Z" fill="none" stroke="url(#gold)" stroke-width="8" stroke-linecap="round"/>
    <path d="M485 118C540 79 609 84 646 117C660 129 671 147 670 170C665 211 622 238 575 238C531 238 501 220 465 187C428 152 433 118 485 118Z" fill="none" stroke="url(#gold)" stroke-width="8" stroke-linecap="round"/>
  </g>

  <g>
    <text x="215" y="250" fill="url(#gold)" font-size="180" font-weight="700" font-family="DejaVu Sans, Georgia, serif">18</text>
    <text x="430" y="248" fill="url(#gold)" font-size="78" font-weight="600" font-family="DejaVu Sans, Georgia, serif">SARL</text>
    <text x="180" y="350" fill="url(#gold)" font-size="104" font-weight="700" font-family="DejaVu Sans, Georgia, serif">EITHING</text>
    <text x="150" y="420" fill="url(#silver)" font-size="56" font-weight="400" font-style="italic" font-family="DejaVu Sans, Georgia, serif">Everything you need.</text>
  </g>

  <g>
    <rect x="220" y="425" width="320" height="46" rx="23" fill="#E8C47A" fill-opacity="0.18"/>
    <text x="380" y="456" text-anchor="middle" fill="url(#gold)" font-size="26" font-weight="600" font-family="DejaVu Sans, Georgia, serif">Conseils &amp; assistance</text>
  </g>
</svg>'''
    cairosvg.svg2png(bytestring=svg_content.encode('utf-8'), write_to='logo_18_eithing.png')

def generate_pdf_letterhead():
    generate_logo_png()
    pdf_filename = "PAPIER_EN_TETE_18_EITHING.pdf"
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=A4,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Colors
    NAVY = colors.HexColor("#0E2C43")
    GOLD = colors.HexColor("#C99B5B")
    GRAY = colors.HexColor("#555555")

    # Header Paragraph Styles
    title_style = ParagraphStyle(
        'HeaderTitle',
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=NAVY
    )
    slogan_style = ParagraphStyle(
        'HeaderSlogan',
        fontName='Helvetica-Oblique',
        fontSize=9,
        leading=12,
        textColor=GOLD
    )
    contact_style = ParagraphStyle(
        'HeaderContact',
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        alignment=TA_RIGHT,
        textColor=GRAY
    )

    logo_img = Image('logo_18_eithing.png', width=130, height=89)

    header_left = [
        logo_img,
        Paragraph("<b>18 EITHING SARL</b>", title_style),
        Paragraph("Raison sociale : 18 EITHING SARL<br/>"
                  "Conseil • Logistique • Recyclage & Valorisation Industrielle", slogan_style)
    ]

    header_right = [
        Paragraph("<b>Siège social :</b> Kétou, Département du Plateau, Bénin<br/>"
                  "<b>Téléphone / WhatsApp :</b> +229 44 66 95 87<br/>"
                  "<b>Email :</b> contact@18eithing.bj<br/>"
                  "<b>Site Web :</b> www.18eithing.bj", contact_style)
    ]

    header_table = Table([[header_left, header_right]], colWidths=[310, 212])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
    ]))

    # Body Placeholder
    date_style = ParagraphStyle(
        'DateStyle',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        alignment=TA_RIGHT,
        textColor=NAVY
    )

    body_style = ParagraphStyle(
        'BodyText',
        fontName='Helvetica',
        fontSize=10.5,
        leading=15,
        alignment=TA_JUSTIFY,
        textColor=colors.HexColor("#222222")
    )

    ref_style = ParagraphStyle(
        'RefStyle',
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=NAVY
    )

    story = []
    story.append(header_table)
    story.append(HRFlowable(width="100%", thickness=2.5, color=GOLD, spaceAfter=15, spaceBefore=4))

    story.append(Paragraph("Kétou, le .................................... 2026", date_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>Réf :</b> 18EITHING/DG/2026/N° ........", ref_style))
    story.append(Spacer(1, 15))

    story.append(Paragraph("<b>Objet :</b> ...........................................................................................................................................................", ref_style))
    story.append(Spacer(1, 20))

    # Example letter body placeholder
    story.append(Paragraph("Madame, Monsieur,<br/><br/>"
                           "Nous avons l'honneur de porter à votre attention la présente correspondance administrative relative aux activités industrielles, logistiques et commerciales de la société <b>18 EITHING SARL</b>.<br/><br/>"
                           "Implantée au cœur de la commune de Kétou (Département du Plateau, Bénin), notre structure est spécialisée dans la valorisation, le broyage et le recyclage industriel des déchets plastiques rigides (Polypropylène - PP et Polyéthylène Haute Densité - PEHD), ainsi que dans le conseil stratégique et la logistique de santé.<br/><br/>"
                           "Restant à votre entière disposition pour tout renseignement complémentaire, nous vous prions d'agréer, Madame, Monsieur, l'expression de nos salutations distinguées.", body_style))

    story.append(Spacer(1, 35))

    # Empty Signature / Stamp Area
    sig_title = ParagraphStyle('SigTitle', fontName='Helvetica-Bold', fontSize=10, leading=13, alignment=TA_RIGHT, textColor=NAVY)
    sig_sub = ParagraphStyle('SigSub', fontName='Helvetica-Oblique', fontSize=9, leading=12, alignment=TA_RIGHT, textColor=GRAY)

    sig_cell = [
        Paragraph("<b>Signature et Cachet Officiel :</b>", sig_title),
        Spacer(1, 45), # Empty space for signature and official stamp
        Paragraph("<i>(Emplacement réservé au cachet et à la signature)</i>", sig_sub)
    ]

    sig_table = Table([[ "", sig_cell ]], colWidths=[260, 252])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(sig_table)

    story.append(Spacer(1, 25))

    # Footer
    footer_style = ParagraphStyle(
        'FooterText',
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        alignment=TA_CENTER,
        textColor=GRAY
    )

    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=6, spaceBefore=10))
    story.append(Paragraph("<b>18 EITHING SARL</b> — Société à Responsabilité Limitée au capital social de 5 000 000 FCFA<br/>"
                           "Siège social : Kétou, Département du Plateau, République du Bénin — RCCM : RB/KET/2026-B-1234 — IFU : 3202612345678<br/>"
                           "Email : contact@18eithing.bj — Web : www.18eithing.bj — Téléphone / WhatsApp : +229 44 66 95 87", footer_style))

    doc.build(story)
    print("Document Papier en Tête PDF avec Logo officiel généré : PAPIER_EN_TETE_18_EITHING.pdf")

if __name__ == '__main__':
    generate_pdf_letterhead()
