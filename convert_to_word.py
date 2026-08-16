import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def set_cell_background(cell, fill_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=140, bottom=140, left=180, right=180):
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(f'''
            <w:tblBorders {nsdecls("w")}>
                <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:left w:val="none"/>
                <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:right w:val="none"/>
                <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
                <w:insideV w:val="none"/>
            </w:tblBorders>
        ''')
        tblPr[0].append(borders)

def make_callout_box(doc, title_text, body_text, bg_color="F4F6F9", border_color="0E2C43", title_color_rgb=RGBColor(0x0E, 0x2C, 0x43), body_color_rgb=RGBColor(0x33, 0x33, 0x33)):
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=180, bottom=180, left=240, right=240)

    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(f'''
        <w:tcBorders {nsdecls("w")}>
            <w:left w:val="single" w:sz="24" w:space="0" w:color="{border_color}"/>
            <w:top w:val="none"/>
            <w:right w:val="none"/>
            <w:bottom w:val="none"/>
        </w:tcBorders>
    ''')
    tcPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(4)
    run_t = p.add_run(title_text)
    run_t.font.name = 'Arial'
    run_t.font.size = Pt(11)
    run_t.font.bold = True
    run_t.font.color.rgb = title_color_rgb

    p2 = cell.add_paragraph()
    p2.paragraph_format.space_before = Pt(2)
    p2.paragraph_format.space_after = Pt(0)
    run_b = p2.add_run(body_text)
    run_b.font.name = 'Calibri'
    run_b.font.size = Pt(10.5)
    run_b.font.italic = True
    run_b.font.color.rgb = body_color_rgb

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

def main():
    doc = docx.Document()

    # Margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)

    # Base Styles
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x2B, 0x2B, 0x2B)

    # Document Header / Banner
    header_table = doc.add_table(rows=1, cols=1)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    h_cell = header_table.cell(0, 0)
    set_cell_background(h_cell, "0E2C43") # Dark Navy
    set_cell_margins(h_cell, top=280, bottom=280, left=280, right=280)

    p_title = h_cell.paragraphs[0]
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("DOSSIER STRATÉGIQUE D'INVESTISSEMENT\nET PLAN D'AFFAIRES INDUSTRIEL")
    r_title.font.name = 'Arial'
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    p_sub = h_cell.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(0)
    r_sub = p_sub.add_run("18 EITHING SARL — Kétou, Bénin\nUnité Industrielle de Recyclage et Broyage des Déchets Plastiques (PP & PEHD)")
    r_sub.font.name = 'Calibri'
    r_sub.font.size = Pt(12)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0xD9, 0xB6, 0x77) # Gold Accent

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_after = Pt(12)

    # Executive Info Box
    make_callout_box(
        doc,
        "SYNTHÈSE DU PROJET & DIRECTION GÉNÉRALE",
        "• Implantation : Kétou (Département du Plateau, République du Bénin)\n"
        "• Dirigeants : M. Hubert C. TOKPANOU (DG - Finance & Supply Chain) & M. Pedro S. KPONON (Gérant - SST & Ergonomie)\n"
        "• Besoin de financement : 28 000 000 FCFA (CAPEX & BFR de démarrage)\n"
        "• Capacité industrielle : 52,8 Tonnes/mois de plastique rigide (45 Tonnes de broyat marchand PP/PEHD)",
        bg_color="F4EFE9",
        border_color="C99B5B"
    )

    def add_sec_heading(text, level=1):
        h = doc.add_paragraph()
        h.paragraph_format.keep_with_next = True
        run = h.add_run(text)
        run.font.name = 'Arial'
        run.bold = True

        if level == 1:
            h.paragraph_format.space_before = Pt(18)
            h.paragraph_format.space_after = Pt(6)
            run.font.size = Pt(14)
            run.font.color.rgb = RGBColor(0x0E, 0x2C, 0x43) # Navy

            # Add bottom accent line under H1
            pBdr = parse_xml(f'<w:pBdr {nsdecls("w")}><w:bottom w:val="single" w:sz="12" w:space="4" w:color="C99B5B"/></w:pBdr>')
            h._element.get_or_add_pPr().append(pBdr)

        elif level == 2:
            h.paragraph_format.space_before = Pt(14)
            h.paragraph_format.space_after = Pt(4)
            run.font.size = Pt(12)
            run.font.color.rgb = RGBColor(0xB6, 0x6A, 0x3F) # Copper / Brown accent
        elif level == 3:
            h.paragraph_format.space_before = Pt(10)
            h.paragraph_format.space_after = Pt(2)
            run.font.size = Pt(11)
            run.font.color.rgb = RGBColor(0x1F, 0x2D, 0x3D)

    # --- SECTION 1 ---
    add_sec_heading("1. RÉSUMÉ EXÉCUTIF & THÈSE D'INVESTISSEMENT", 1)

    add_sec_heading("1.1 Problématique environnementale et opportunité industrielle au Bénin", 2)
    p = doc.add_paragraph("La gestion des déchets solides ménagers et industriels constitue l'un des défis majeurs du développement urbain et économique en République du Bénin. Chaque année, plus de 100 000 tonnes de plastiques rigides et souples sont générées sur l'ensemble du territoire national, dont seule une fraction inférieure à 8 % fait l'objet d'un recyclage formel. Le reste s'accumule dans la nature, bouche les réseaux d'évacuation d'eaux pluviales ou brûle à l'air libre, générant des risques sanitaires et écologiques majeurs.")
    p.paragraph_format.space_after = Pt(6)

    p = doc.add_paragraph("Parallèlement, l'industrie manufacturière régionale (plasturgie, emballages, BTP, canalisations) fait face à un coût d'approvisionnement élevé en résines vierges importées (PP, PEHD), directement impactées par la volatilité des cours mondiaux du pétrole et le coût du fret maritime.")
    p.paragraph_format.space_after = Pt(6)

    p = doc.add_paragraph("18 EITHING SARL apporte une réponse industrielle concrète en structurant la filière de collecte et de transformation primaire des plastiques rigides (PP et PEHD) en broyats calibrés de haute qualité, répondant aux standards des plasturgistes béninois et sous-régionaux (Nigeria, Togo).")
    p.paragraph_format.space_after = Pt(6)

    add_sec_heading("1.2 Proposition de valeur unique : Positionnement Kétou vs Littoral/Cotonou", 2)
    p = doc.add_paragraph("Contrairement aux rares initiatives concentrées dans la zone saturée du Littoral (Cotonou, Akpakpa) caractérisée par un coût du foncier exorbitant, des coûts salariaux élevés et une concurrence acharnée sur le gisement local de déchets, 18 EITHING SARL positionne son unité industrielle de broyage à Kétou (Plateau).")
    p.paragraph_format.space_after = Pt(6)

    doc.add_paragraph("Ce choix d'implantation stratégique offre des avantages comparatifs déterminants :").paragraph_format.space_after = Pt(4)

    for bullet in [
        ("Gisement transfrontalier et territorial massif : ", "Accès direct aux flux de plastiques rigides ménagers et agricoles des départements du Plateau, de Zou, de la Colline, ainsi qu'aux flux informels de la frontière nigériane (à proximité immédiate d'Ihara et d'Igangan)."),
        ("Coût d'exploitation et foncier compétitif : ", "Optimisation majeure du CAPEX d'implantation et des charges fixes d'exploitation (loyer industriel et main-d'œuvre locale qualifiée)."),
        ("Nœud logistique stratégique : ", "Proximité des grands axes routiers RNIE 4 et RN3 permettant de desservir à la fois le marché du Littoral (Cotonou) et les marchés d'exportation sous-régionaux.")
    ]:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(3)
        r1 = bp.add_run(bullet[0])
        r1.bold = True
        r1.font.color.rgb = RGBColor(0x0E, 0x2C, 0x43)
        bp.add_run(bullet[1])

    add_sec_heading("1.3 Gouvernance et synergie d'expertises des fondateurs", 2)
    p = doc.add_paragraph("La direction de 18 EITHING SARL repose sur un tandem exécutif hautement complémentaire, combinant rigueur financière, excellence logistique et maîtrise de la santé au travail :")
    p.paragraph_format.space_after = Pt(6)

    for founder, role, details in [
        ("M. Hubert C. TOKPANOU", "Directeur Général (Pôle Logistique, Supply Chain & Finance)", [
            "Expertise approfondie en ingénierie logistique, négociation commerciale, gestion financière et structuration de flux d'approvisionnement complexes.",
            "En charge du pilotage de la rentabilité, des relations bancaires et investisseurs, de l'optimisation des coûts de transport et de la sécurisation des contrats d'approvisionnement et de vente."
        ]),
        ("M. Pedro S. KPONON", "Gérant (Pôle SST, Ergonomie & Santé/Psychologie du Travail)", [
            "Expert en Santé et Sécurité au Travail (SST), organisation ergonomique des postes et santé mentale/psychologie industrielle.",
            "En charge de la conception ergonomique du site, de la réduction de la pénibilité physique sur la chaîne de tri/broyage, de la conformité environnementale et de la politique Zéro Accident."
        ])
    ]:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(4)
        p.paragraph_format.space_after = Pt(2)
        r_f = p.add_run(f"• {founder} ")
        r_f.bold = True
        r_f.font.color.rgb = RGBColor(0x0E, 0x2C, 0x43)
        r_r = p.add_run(f"– {role}")
        r_r.italic = True
        for d in details:
            sub_p = doc.add_paragraph(style='List Bullet 2')
            sub_p.paragraph_format.space_after = Pt(2)
            sub_p.add_run(d)

    # --- SECTION 2 ---
    add_sec_heading("2. INGÉNIERIE STRATÉGIQUE & MODÈLE D'AFFAIRES (BUSINESS MODEL CANVAS)", 1)

    add_sec_heading("2.1 Analyse synthétique du Business Model Canvas (BMC)", 2)

    bmc_data = [
        ("1. Partenaires Clés", ["Associations de collecteurs informels et grossistes de déchets (Plateau/Zou).", "Municipalités de Kétou, Pobè et Sakété (concessions de tri).", "Fournisseurs d'équipements industriels et sous-traitants de maintenance.", "Industriels plasturgistes locaux et régionaux (acheteurs de broyat PP/PEHD)."]),
        ("2. Activités Clés", ["Sourcing, pesée et achat des déchets plastiques rigides.", "Tri qualitatif par résine (PP vs PEHD) et par couleur.", "Lavage, décontamination primaire et séchage.", "Broyage industriel et calibrage (grilles 8-10 mm).", "Conditionnement en Big Bags (25-50 kg) et livraison."]),
        ("3. Ressources Clés", ["Ligne industrielle de broyage 15 HP et bacs de lavage à recirculation.", "Terrain industriel sécurisé de 1 500 m² à Kétou.", "Réseau logistique de collecte et capital humain formé aux règles SST."]),
        ("4. Proposition de Valeur", ["Pour les plasturgistes : Broyats purs à 98 %, réduction de 35 % du coût matière vs résine vierge.", "Pour la collectivité : Assainissement territorial, création d'emplois locaux pérennes."]),
        ("5. Relations Clients", ["Contrats d'approvisionnement pluriannuels à volumes et prix garantis.", "Assistance technique, fourniture d'échantillons et garantie de régularité."]),
        ("6. Canaux de Distribution", ["Vente directe B2B via l'équipe commerciale interne.", "Livraisons directes par camionnage dédié vers Cotonou et Porto-Novo."]),
        ("7. Segments de Clientèle", ["Fabricants d'emballages plastiques rigides et conduits BTP.", "Unités d'injection/soufflage d'ustensiles ménagers (bassines, seaux).", "Exportateurs sous-régionaux."]),
        ("8. Structure de Coûts", ["Achats de matière brute plastique aux collecteurs (FCFA/kg).", "Consommation d'énergie (Sbee triphasé + groupe secours) et carburant.", "Masse salariale (10 personnes) et maintenance préventive."]),
        ("9. Flux de Revenus", ["Vente au tonnage de broyat PP calibré.", "Vente au tonnage de broyat PEHD calibré.", "Prestations de broyage à façon pour tiers."])
    ]

    for title_bmc, items_bmc in bmc_data:
        add_sec_heading(title_bmc, 3)
        for item in items_bmc:
            bp = doc.add_paragraph(style='List Bullet')
            bp.paragraph_format.space_after = Pt(2)
            bp.add_run(item)

    add_sec_heading("2.2 Cartographie des flux d'approvisionnement (4 Bassins Logistiques)", 2)
    for zone in [
        ("Zone 1 : Bassin Principal de Kétou & Plateau", "Collecte directe, proximité immédiate, faible coût logistique."),
        ("Zone 2 : Bassin Sud - Littoral / Porto-Novo", "Rapatriement optimisé par retours à vide des camions de livraison."),
        ("Zone 3 : Bassin Centre & Ouest - Zou / Collines", "Points de regroupement partenaires à Abomey, Bohicon et Dassa."),
        ("Zone 4 : Axe Transfrontalier Nigeria", "Sourcing complémentaire sur opportunités de marché à Ihara/Igangan.")
    ]:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(3)
        r_z = bp.add_run(f"{zone[0]} : ")
        r_z.bold = True
        r_z.font.color.rgb = RGBColor(0x0E, 0x2C, 0x43)
        bp.add_run(zone[1])

    # --- SECTION 3 ---
    add_sec_heading("3. PROCESSUS TECHNIQUE & INGÉNIERIE OPÉRATIONNELLE", 1)

    add_sec_heading("3.1 Description séquentielle du processus de production (7 Étapes)", 2)
    steps = [
        ("Étape 1 : Réception et Pesée à l'Entrée", "Contrôle des lots entrants sur pèse-essieu, enregistrement informatique de la provenance, du poids brut et de la catégorie de plastique."),
        ("Étape 2 : Tri Manuel Sélectif et Dépollution", "Séparation rigoureuse par famille polymère (PP vs PEHD) et retrait systématique des corps étrangers (métaux, verre, papier, PVC/PET)."),
        ("Étape 3 : Pré-lavage et Dégraissage", "Trempage dans des bacs de décantation afin d'éliminer les boues, sables et matières organiques superficielles."),
        ("Étape 4 : Broyage Industriel Mécanique", "Alimentation continue du broyeur 15 HP équipé de lames en acier au chrome à haute résistance. Passage à travers une grille de 8 à 10 mm."),
        ("Étape 5 : Lavage Continu & Rinçage", "Lavage haute efficacité des paillettes broyées avec système de clarification et de recyclage de l'eau en circuit fermé."),
        ("Étape 6 : Séchage & Dépoussiérage", "Essorage centrifuge mécanique suivi d'un passage en serre solaire thermiquement optimisée (< 1 % d'humidité)."),
        ("Étape 7 : Contrôle Qualité & Conditionnement", "Inspection visuelle et granulométrique, ensachage sous Big Bags de 25 kg ou 50 kg, étiquetage et stockage sur palettes.")
    ]
    for s_title, s_desc in steps:
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(3)
        p.paragraph_format.space_after = Pt(3)
        r1 = p.add_run(f"• {s_title} : ")
        r1.bold = True
        r1.font.color.rgb = RGBColor(0x0E, 0x2C, 0x43)
        p.add_run(s_desc)

    add_sec_heading("3.2 Fiche technique des équipements majeurs", 2)
    for eq_title, eq_specs in [
        ("Broyeur Industriel 15 HP (Lame Heavy Duty)", ["Moteur : 11 kW (15 HP) - Triphasé 380V", "Capacité nominale : 250 à 350 kg/heure", "Rotor : 3 lames mobiles + 2 lames fixes en acier spécial anti-abrasion", "Grille de calibrage : 8 mm / 10 mm interchangeable"]),
        ("Système de Bacs de Lavage et Clarification", ["Bacs inox / PEHD haute résistance de 3 000 Litres", "Pompe de recirculation et filtres à débris"]),
        ("Serres Solaire de Séchage & Centrifugeuse", ["Séchoir centrifuge rotatif 3 kW", "Zone de séchage sous serre thermiquement optimisée"]),
        ("Balances & Pèse-Palettes", ["Pèse-palette électronique de précision (capacité 2 tonnes, précision 500 g)"])
    ]:
        add_sec_heading(eq_title, 3)
        for spec in eq_specs:
            bp = doc.add_paragraph(style='List Bullet')
            bp.paragraph_format.space_after = Pt(2)
            bp.add_run(spec)

    add_sec_heading("3.3 Plan de gestion Santé, Sécurité au Travail (SST) et Ergonomie", 2)
    p = doc.add_paragraph("Conformément à l'expertise apportée par M. Pedro S. KPONON, l'unité de Kétou intègre les meilleurs standards ergonomiques et préventifs :")
    p.paragraph_format.space_after = Pt(4)

    for sst_cat, sst_items in [
        ("Réduction de la Pénibilité Physique", ["Tables de tri surélevées à hauteur réglable évitant les courbures lombaires.", "Utilisation de transpalettes hydrauliques et gerbeurs pour supprimer le port manuel > 25 kg."]),
        ("Protection Biologique, Auditive et Respiratoire", ["Port obligatoire des EPI : Masques FFP2, casques anti-bruit / bouchons moulés (< 85 dB), gants anti-coupure et chaussures S3."]),
        ("Aspiration à la source", ["Aspiration centralisée des poussières légères au niveau de la sortie du broyeur."]),
        ("Programme de Santé Mentale et Suivi Ergonomique", ["Rotation systématique des postes toutes les 2 heures entre le tri, le lavage et l'emballage.", "Entretiens individuels réguliers de suivi psychologique du travail et gestion du stress."])
    ]:
        add_sec_heading(sst_cat, 3)
        for item in sst_items:
            bp = doc.add_paragraph(style='List Bullet')
            bp.paragraph_format.space_after = Pt(2)
            bp.add_run(item)

    # --- SECTION 4 ---
    add_sec_heading("4. PLAN D'EXÉCUTION & CHRONOGRAMME DE DÉPLOIEMENT (12 SEMAINES)", 1)

    roadmap = [
        ("Semaines 1 à 2", "Finalisation juridique, levée de fonds bancaires, signature du bail du site industriel de Kétou."),
        ("Semaines 3 à 4", "Aménagement du site (dalle béton, raccordement Sbee Triphasé, bassins de décantation water-recycling)."),
        ("Semaines 5 à 6", "Commande, réception et installation de la ligne de broyage 15 HP et des équipements annexes."),
        ("Semaines 7 à 8", "Essais à vide, calibrage des lames, mise en place des protocoles SST et formation du personnel."),
        ("Semaines 9 à 10", "Lancement des campagnes d'achat de collecte de rodage (stock de sécurité de 20 tonnes de matière brute)."),
        ("Semaines 11 à 12", "Lancement de la production continue, livraison des premiers lots B2B et montée en puissance vers la capacité nominale.")
    ]
    for sem, desc in roadmap:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(3)
        r_s = bp.add_run(f"{sem} : ")
        r_s.bold = True
        r_s.font.color.rgb = RGBColor(0x0E, 0x2C, 0x43)
        bp.add_run(desc)

    # --- SECTION 5 ---
    add_sec_heading("5. MODÉLISATION FINANCIÈRE & RENTABILITÉ", 1)
    doc.add_paragraph("(Tous les montants sont exprimés en Francs CFA - FCFA)").paragraph_format.space_after = Pt(6)

    add_sec_heading("5.1 Hypothèses de calcul et paramètres économiques", 2)
    hypotheses = [
        ("Capacité de traitement nominale : ", "300 kg / heure"),
        ("Temps de travail : ", "8 heures / jour, 22 jours / mois (176 heures / mois)"),
        ("Volume mensuel traité : ", "52,8 Tonnes de matière brute"),
        ("Rendement de transformation : ", "85 % (soit 45 Tonnes de broyat marchand / mois)"),
        ("Prix moyen d'achat matière brute : ", "100 FCFA / kg"),
        ("Prix moyen de vente broyat PP/PEHD : ", "450 FCFA / kg (soit 450 000 FCFA / Tonne)")
    ]
    for h_label, h_val in hypotheses:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(2)
        r_l = bp.add_run(h_label)
        r_l.bold = True
        bp.add_run(h_val)

    def create_styled_table(doc, headers, rows_data):
        table = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table)

        # Header Row
        hdr_cells = table.rows[0].cells
        for i, header_text in enumerate(headers):
            hdr_cells[i].text = header_text
            set_cell_background(hdr_cells[i], "0E2C43")
            set_cell_margins(hdr_cells[i], top=140, bottom=140, left=160, right=160)
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if i == len(headers) - 1 else WD_ALIGN_PARAGRAPH.LEFT
            for run in p.runs:
                run.font.name = 'Arial'
                run.font.size = Pt(10)
                run.font.bold = True
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

        # Data Rows
        for r_idx, row in enumerate(rows_data):
            row_cells = table.rows[r_idx + 1].cells
            is_total_row = "TOTAL" in row[0].upper()
            bg_color = "EAEFF5" if is_total_row else ("F9FAFC" if r_idx % 2 == 1 else "FFFFFF")

            for c_idx, val in enumerate(row):
                row_cells[c_idx].text = val
                set_cell_background(row_cells[c_idx], bg_color)
                set_cell_margins(row_cells[c_idx], top=120, bottom=120, left=160, right=160)
                p = row_cells[c_idx].paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.RIGHT if (c_idx > 0 and val.replace(' ', '').replace('-', '').replace('%', '').replace('.', '').replace(',', '').isdigit()) else WD_ALIGN_PARAGRAPH.LEFT
                for run in p.runs:
                    run.font.name = 'Calibri'
                    run.font.size = Pt(10)
                    if is_total_row or c_idx == 0:
                        run.font.bold = True
                    if is_total_row:
                        run.font.color.rgb = RGBColor(0x0E, 0x2C, 0x43)

        doc.add_paragraph().paragraph_format.space_after = Pt(8)

    add_sec_heading("5.2 Plan d'Investissement Initial (CAPEX)", 2)
    capex_headers = ["Poste d'Investissement", "Description / Détails", "Montant (FCFA)"]
    capex_rows = [
        ["Aménagements du site & Génie Civil", "Dalle technique, bassins de lavage, bureau", "4 500 000"],
        ["Ligne de Broyage Industrielle 15 HP", "Broyeur, jeux de lames, tableau électrique", "7 800 000"],
        ["Équipements de Lavage & Séchage", "Bacs inox, pompes, centrifugeuse, serre solaire", "3 200 000"],
        ["Matériel Logistique & Manutention", "Gerbeur, transpalettes, pèse-palettes, Big Bags", "2 500 000"],
        ["Installation Électrique & Groupe Sécurité", "Câblage triphasé, armoire, groupe 20 kVA", "3 500 000"],
        ["Frais d'Établissement & Licences", "Immatriculation, étude d'impact, conformité SST", "1 500 000"],
        ["Fonds de Roulement Initial (BFR)", "Stock matière brute (1 mois) + trésorerie", "5 000 000"],
        ["TOTAL CAPEX REQUIS", "Investissement Total Démarrage", "28 000 000"]
    ]
    create_styled_table(doc, capex_headers, capex_rows)

    add_sec_heading("5.3 Modélisation des Charges d'Exploitation Mensuelles (OPEX)", 2)
    opex_headers = ["Poste de Dépense OPEX", "Base de Calcul Mensuelle", "Montant Mensuel (FCFA)"]
    opex_rows = [
        ["Achat Matière Première Brute", "52,8 Tonnes x 100 FCFA/kg", "5 280 000"],
        ["Consommation Énergie & Eau", "Sbee triphasé + carburant groupe secours", "750 000"],
        ["Masse Salariale (10 Personnes)", "DG, Gérant SST, 6 Opérateurs, 2 Chauffeurs", "2 100 000"],
        ["Transport & Logistique de collecte", "Carburant camions, frais d'approche", "1 200 000"],
        ["Maintenance Préventive & Lames", "Rechargement lames, vidanges, consommables", "450 000"],
        ["Frais Généraux & Assurances", "Loyer terrain Kétou, télécoms, comptabilité", "500 000"],
        ["TOTAL OPEX MENSUEL", "Coût de Fonctionnement Mensuel", "10 280 000"]
    ]
    create_styled_table(doc, opex_headers, opex_rows)

    add_sec_heading("5.4 Compte de Résultat Prévisionnel (Année 1)", 2)
    pnl_headers = ["Poste du Compte de Résultat", "Calcul Mensuel (FCFA)", "Année 1 - 12 Mois (FCFA)"]
    pnl_rows = [
        ["CHIFFRE D'AFFAIRES (CA)", "45 T x 450 000 FCFA/T", "243 000 000"],
        ["Achats Matières Premières", "-5 280 000 FCFA", "-63 360 000"],
        ["MARGE BRUTE DE PRODUCTION", "14 970 000 FCFA", "179 640 000"],
        ["Autres Charges Externe & OPEX", "-5 000 000 FCFA", "-60 000 000"],
        ["EXCÉDENT BRUT D'EXPLOITATION (EBITDA)", "9 970 000 FCFA", "119 640 000"],
        ["Amortissements des Équipements (20%)", "-350 000 FCFA", "-4 200 000"],
        ["RÉSULTAT NET AVANT IMPÔT", "9 620 000 FCFA", "115 440 000"]
    ]
    create_styled_table(doc, pnl_headers, pnl_rows)

    add_sec_heading("5.5 Indicateurs Clés de Rentabilité (KPIs)", 2)
    for kpi, val in [
        ("Marge Brute de Production : ", "73.9 %"),
        ("Marge d'EBITDA : ", "59.1 %"),
        ("Retour sur Investissement (ROI) : ", "Moins de 6 mois d'exploitation continue"),
        ("Point Mort (Seuil de Rentabilité) : ", "18,5 Tonnes / mois (soit 41 % de la capacité maximale)")
    ]:
        bp = doc.add_paragraph(style='List Bullet')
        bp.paragraph_format.space_after = Pt(2)
        r_k = bp.add_run(kpi)
        r_k.bold = True
        bp.add_run(val)

    # --- SECTION 6 ---
    add_sec_heading("6. ANALYSE CRITIQUE DES RISQUES ET PLAN DE MITIGATION", 1)
    risk_headers = ["Risque Identifié", "Niveau", "Plan de Mitigation Concret (18 EITHING SARL)"]
    risk_rows = [
        ["Saisonnalité / Pénurie approvisionnement", "Moyen", "Stock de sécurité de 30 jours + diversification géographique sur 4 départements."],
        ["Coupures d'électricité (Sbee)", "Élevé", "Acquisition d'un groupe électrogène industriel de secours 20 kVA dédié."],
        ["Contamination des plastiques (PP/PEHD)", "Élevé", "Tri à 2 niveaux + test de densité par flottaison systématique avant broyage."],
        ["Usure prématurée des lames de broyeur", "Moyen", "Contrat d'affûtage local + stock permanent de 2 jeux de lames de rechange."],
        ["Accidents du travail / Pénibilité", "Moyen", "Supervision SST M. Pedro KPONON, port des EPI obligatoire, rotation des postes."]
    ]
    create_styled_table(doc, risk_headers, risk_rows)

    # --- SECTION 7 ---
    add_sec_heading("7. CONCLUSION & DEMANDE DE FINANCEMENT", 1)
    p = doc.add_paragraph("Le projet porté par 18 EITHING SARL à Kétou combine une opportunité économique à haute rentabilité, une utilité écologique majeure pour la gestion des déchets au Bénin, et une gouvernance expérimentée et complémentaire.")
    p.paragraph_format.space_after = Pt(6)

    make_callout_box(
        doc,
        "DEMANDE DE FINANCEMENT BANCAIRE / INVESTISSEUR",
        "Pour soutenir le démarrage de l'unité industrielle et couvrir le besoin d'investissement (CAPEX) et de BFR de démarrage, 18 EITHING SARL sollicite un accompagnement financier à hauteur de 28 000 000 FCFA sous forme de concours bancaire ou d'apport en fonds propres.",
        bg_color="F4EFE9",
        border_color="0E2C43",
        title_color_rgb=RGBColor(0x0E, 0x2C, 0x43),
        body_color_rgb=RGBColor(0x2B, 0x2B, 0x2B)
    )

    p_sign = doc.add_paragraph()
    p_sign.paragraph_format.space_before = Pt(16)
    p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_s1 = p_sign.add_run("Dossier établi à Kétou, République du Bénin.\nPour la Direction Générale,\n")
    r_s1.italic = True
    r_s2 = p_sign.add_run("M. Hubert C. TOKPANOU & M. Pedro S. KPONON")
    r_s2.bold = True
    r_s2.font.color.rgb = RGBColor(0x0E, 0x2C, 0x43)

    doc.save("DOSSIER_STRATEGIQUE_18_EITHING.docx")
    print("Nouveau document Word DOSSIER_STRATEGIQUE_18_EITHING.docx régénéré avec succès!")

if __name__ == '__main__':
    main()
