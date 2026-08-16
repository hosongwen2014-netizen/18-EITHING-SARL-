import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def generate_word_letterhead():
    doc = docx.Document()

    # Page Margins (0.6 inch margins for clean header)
    for section in doc.sections:
        section.top_margin = Inches(0.6)
        section.bottom_margin = Inches(0.6)
        section.left_margin = Inches(0.7)
        section.right_margin = Inches(0.7)

    # Base Font
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)

    # Header Table
    table = doc.add_table(rows=1, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    cell_left = table.cell(0, 0)
    cell_right = table.cell(0, 1)

    # Left Cell: Brand Name & Slogan
    p_left = cell_left.paragraphs[0]
    p_left.paragraph_format.space_after = Pt(2)
    r_brand = p_left.add_run("18 EITHING SARL\n")
    r_brand.font.name = 'Arial'
    r_brand.font.size = Pt(20)
    r_brand.font.bold = True
    r_brand.font.color.rgb = RGBColor(0x0E, 0x2C, 0x43) # Dark Navy

    r_slogan = p_left.add_run("Conseil • Logistique • Recyclage & Valorisation Industrielle")
    r_slogan.font.size = Pt(9.5)
    r_slogan.font.italic = True
    r_slogan.font.color.rgb = RGBColor(0xC9, 0x9B, 0x5B) # Gold

    # Right Cell: Contact Info
    p_right = cell_right.paragraphs[0]
    p_right.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_right.paragraph_format.space_after = Pt(0)

    r_contact = p_right.add_run(
        "Siège social : Kétou, Département du Plateau, Bénin\n"
        "Tél / WhatsApp : +229 44 66 95 87\n"
        "Email : contact@18eithing.bj\n"
        "Site Web : www.18eithing.bj"
    )
    r_contact.font.size = Pt(8.5)
    r_contact.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    # Divider Line (Gold Bar)
    p_divider = doc.add_paragraph()
    p_divider.paragraph_format.space_before = Pt(6)
    p_divider.paragraph_format.space_after = Pt(18)
    pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="18" w:space="1" w:color="C99B5B"/></w:pBdr>')
    p_divider._element.get_or_add_pPr().append(pBdr)

    # Letter Header Metadata
    p_date = doc.add_paragraph()
    p_date.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_date.paragraph_format.space_after = Pt(12)
    r_date = p_date.add_run("Kétou, le .................................... 2026")
    r_date.font.bold = True
    r_date.font.color.rgb = RGBColor(0x0E, 0x2C, 0x43)

    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.space_after = Pt(8)
    r_ref = p_ref.add_run("Réf : 18EITHING/DG/2026/N° ........")
    r_ref.font.bold = True
    r_ref.font.color.rgb = RGBColor(0x0E, 0x2C, 0x43)

    p_obj = doc.add_paragraph()
    p_obj.paragraph_format.space_after = Pt(20)
    r_obj = p_obj.add_run("Objet : ...........................................................................................................................................................")
    r_obj.font.bold = True
    r_obj.font.color.rgb = RGBColor(0x0E, 0x2C, 0x43)

    # Letter Body Template Text
    p_body = doc.add_paragraph()
    p_body.paragraph_format.space_after = Pt(12)
    p_body.paragraph_format.line_spacing = 1.2
    r_b = p_body.add_run(
        "Madame, Monsieur,\n\n"
        "Nous avons l'honneur de porter à votre attention la présente correspondance administrative relative aux activités industrielles, logistiques et commerciales de la société 18 EITHING SARL.\n\n"
        "Implantée au cœur de la commune de Kétou (Département du Plateau, Bénin), notre structure est spécialisée dans la valorisation, le broyage et le recyclage industriel des déchets plastiques rigides (Polypropylène - PP et Polyéthylène Haute Densité - PEHD), ainsi que dans le conseil stratégique et la logistique de santé.\n\n"
        "Restant à votre entière disposition pour tout renseignement complémentaire, nous vous prions d'agréer, Madame, Monsieur, l'expression de nos salutations distinguées."
    )
    r_b.font.size = Pt(11)

    # Signature Block
    p_space = doc.add_paragraph()
    p_space.paragraph_format.space_after = Pt(30)

    sig_table = doc.add_table(rows=1, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER

    s_left = sig_table.cell(0, 0)
    s_right = sig_table.cell(0, 1)

    p_sl = s_left.paragraphs[0]
    p_sl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sl1 = p_sl.add_run("M. Hubert C. TOKPANOU\n")
    r_sl1.font.bold = True
    r_sl1.font.color.rgb = RGBColor(0x0E, 0x2C, 0x43)
    r_sl2 = p_sl.add_run("Directeur Général\nPôle Finance, Supply Chain & Logistique")
    r_sl2.font.italic = True
    r_sl2.font.size = Pt(9.5)

    p_sr = s_right.paragraphs[0]
    p_sr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_sr1 = p_sr.add_run("M. Pedro S. KPONON\n")
    r_sr1.font.bold = True
    r_sr1.font.color.rgb = RGBColor(0x0E, 0x2C, 0x43)
    r_sr2 = p_sr.add_run("Gérant\nPôle SST, Ergonomie & Santé au Travail")
    r_sr2.font.italic = True
    r_sr2.font.size = Pt(9.5)

    # Footer Divider Line
    p_fdiv = doc.add_paragraph()
    p_fdiv.paragraph_format.space_before = Pt(40)
    p_fdiv.paragraph_format.space_after = Pt(6)
    pBdrF = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="8" w:space="1" w:color="0E2C43"/></w:pBdr>')
    p_fdiv._element.get_or_add_pPr().append(pBdrF)

    # Footer Legal Info
    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_foot = p_foot.add_run(
        "18 EITHING SARL — Société à Responsabilité Limitée au capital social de 5 000 000 FCFA\n"
        "Siège social : Kétou, Département du Plateau, République du Bénin — RCCM : RB/KET/2026-B-1234 — IFU : 3202612345678\n"
        "Email : contact@18eithing.bj — Web : www.18eithing.bj — Téléphone / WhatsApp : +229 44 66 95 87"
    )
    r_foot.font.size = Pt(8)
    r_foot.font.color.rgb = RGBColor(0x66, 0x66, 0x66)

    doc.save("PAPIER_EN_TETE_18_EITHING.docx")
    print("Document Papier en Tête Word généré : PAPIER_EN_TETE_18_EITHING.docx")

if __name__ == '__main__':
    generate_word_letterhead()
