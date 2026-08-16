import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_RIGHT, TA_LEFT, TA_JUSTIFY

def generate_pdf_letterhead():
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
    LIGHT_BG = colors.HexColor("#F8F5F0")

    # Header Paragraph Styles
    title_style = ParagraphStyle(
        'HeaderTitle',
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=NAVY
    )
    slogan_style = ParagraphStyle(
        'HeaderSlogan',
        fontName='Helvetica-Oblique',
        fontSize=10,
        leading=13,
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

    header_left = [
        Paragraph("18 EITHING SARL", title_style),
        Paragraph("Conseil • Logistique • Recyclage & Valorisation Industrielle", slogan_style)
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

    story.append(Spacer(1, 40))

    # Signatures Table
    sig_title = ParagraphStyle('SigTitle', fontName='Helvetica-Bold', fontSize=9.5, leading=12, alignment=TA_CENTER, textColor=NAVY)
    sig_sub = ParagraphStyle('SigSub', fontName='Helvetica-Oblique', fontSize=8.5, leading=11, alignment=TA_CENTER, textColor=GRAY)

    sig_cell1 = [Paragraph("<b>M. Hubert C. TOKPANOU</b>", sig_title), Paragraph("Directeur Général<br/><i>Pôle Finance, Supply Chain & Logistique</i>", sig_sub)]
    sig_cell2 = [Paragraph("<b>M. Pedro S. KPONON</b>", sig_title), Paragraph("Gérant<br/><i>Pôle SST, Ergonomie & Santé au Travail</i>", sig_sub)]

    sig_table = Table([[sig_cell1, sig_cell2]], colWidths=[250, 250])
    sig_table.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
    ]))
    story.append(sig_table)

    story.append(Spacer(1, 60))

    # Footer
    footer_style = ParagraphStyle(
        'FooterText',
        fontName='Helvetica',
        fontSize=7.5,
        leading=10,
        alignment=TA_CENTER,
        textColor=GRAY
    )

    story.append(HRFlowable(width="100%", thickness=1, color=NAVY, spaceAfter=6, spaceBefore=10))
    story.append(Paragraph("<b>18 EITHING SARL</b> — Société à Responsabilité Limitée au capital social de 5 000 000 FCFA<br/>"
                           "Siège social : Kétou, Département du Plateau, République du Bénin — RCCM : RB/KET/2026-B-1234 — IFU : 3202612345678<br/>"
                           "Email : contact@18eithing.bj — Web : www.18eithing.bj — Téléphone / WhatsApp : +229 44 66 95 87", footer_style))

    doc.build(story)
    print("Document Papier en Tête PDF généré : PAPIER_EN_TETE_18_EITHING.pdf")

if __name__ == '__main__':
    generate_pdf_letterhead()
