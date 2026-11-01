#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de Bon de Livraison & Facture Word (.docx) pour GazExpress Bénin
Entreprise : 18 EITHING SARL (Kétou, Bénin)
Direction : M. Hubert C. TOKPANOU (DG) / M. Pedro S. KPONON (Gérant)
"""

import sys
import os
from datetime import datetime
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Applique une couleur de fond hexadécimale à une cellule de tableau."""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tc_pr.append(shd)

def generer_facture_word(commande=None, output_path="Facture_GazExpress_Modele.docx"):
    """Génère un document Word (.docx) professionnel conforme pour GazExpress Bénin."""
    if commande is None:
        commande = {
            "numero": "CMD-8028",
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "client_nom": "M. Pedro KPONON",
            "client_tel": "+229 44 66 95 87",
            "client_adresse": "Cotonou - Akpakpa Sacré-Cœur (Zone Ambassade)",
            "article": "Bouteille 6 kg (Standard) - Recharge / Échange",
            "format": "6 kg",
            "marque_echangee": "Oryx Gaz (Interchangeable avec Bénin Gaz / Puma / ProGaz)",
            "prix_bouteille": 4950,
            "distance_m": 996,
            "frais_livraison": 1000,
            "total_payer": 5950,
            "moyen_paiement": "MTN Mobile Money Bénin (*880#)",
            "statut_paiement": "Confirmé (Réf: MTN-20261101-99812)",
            "livreur_nom": "Bio Chabi (Moto Tricycle Cargo - Plateau)",
            "livreur_tel": "+229 97 00 11 22",
            "depot_depart": "Dépôt Central Gaz Akpakpa (Cotonou)",
            "code_otp": "4892"
        }

    doc = Document()

    # Définition des marges (2 cm tout autour)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)

    # 1. En-tête Entreprise
    header_table = doc.add_table(rows=1, cols=2)
    header_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    header_table.autofit = False

    cell_gauche = header_table.cell(0, 0)
    cell_gauche.width = Inches(4.0)
    p_gauche = cell_gauche.paragraphs[0]
    p_gauche.paragraph_format.space_after = Pt(2)
    run_nom = p_gauche.add_run("18 EITHING SARL\n")
    run_nom.bold = True
    run_nom.font.size = Pt(14)
    run_nom.font.color.rgb = RGBColor(26, 43, 76)

    run_sub = p_gauche.add_run("GazExpress Bénin • Vente de gaz domestique, Logistique & Négoce\n")
    run_sub.font.size = Pt(9)
    run_sub.font.color.rgb = RGBColor(100, 116, 139)

    run_addr = p_gauche.add_run("Kétou, République du Bénin\nEmail : contact@18eithing.bj | Tél / WhatsApp : +229 44 66 95 87\nSite web : www.18eithing.bj")
    run_addr.font.size = Pt(8.5)
    run_addr.font.color.rgb = RGBColor(100, 116, 139)

    cell_droite = header_table.cell(0, 1)
    cell_droite.width = Inches(2.8)
    p_droite = cell_droite.paragraphs[0]
    p_droite.alignment = WD_ALIGN_PARAGRAPH.RIGHT

    run_titre = p_droite.add_run("BON DE LIVRAISON\n& FACTURE OFFICIELLE\n")
    run_titre.bold = True
    run_titre.font.size = Pt(12)
    run_titre.font.color.rgb = RGBColor(224, 86, 36)

    run_ref = p_droite.add_run(f"N° Commande : {commande['numero']}\nDate : {commande['date']}")
    run_ref.font.size = Pt(9.5)
    run_ref.bold = True
    run_ref.font.color.rgb = RGBColor(30, 41, 59)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 2. Encadrés Coordonnées Client & Livreur
    info_table = doc.add_table(rows=1, cols=2)
    info_table.alignment = WD_TABLE_ALIGNMENT.CENTER

    c_cli = info_table.cell(0, 0)
    c_cli.width = Inches(3.4)
    set_cell_background(c_cli, "F8FAFC")
    p_cli = c_cli.paragraphs[0]
    p_cli.add_run("DESTINATAIRE (CLIENT)\n").bold = True
    p_cli.add_run(f"Nom : {commande['client_nom']}\n")
    p_cli.add_run(f"Téléphone : {commande['client_tel']}\n")
    p_cli.add_run(f"Adresse : {commande['client_adresse']}")
    p_cli.runs[0].font.color.rgb = RGBColor(26, 43, 76)

    c_liv = info_table.cell(0, 1)
    c_liv.width = Inches(3.4)
    set_cell_background(c_liv, "F8FAFC")
    p_liv = c_liv.paragraphs[0]
    p_liv.add_run("SERVICE DE LIVRAISON\n").bold = True
    p_liv.add_run(f"Livreur : {commande['livreur_nom']}\n")
    p_liv.add_run(f"Téléphone : {commande['livreur_tel']}\n")
    p_liv.add_run(f"Dépôt d'enlèvement : {commande['depot_depart']}")
    p_liv.runs[0].font.color.rgb = RGBColor(26, 43, 76)

    doc.add_paragraph().paragraph_format.space_after = Pt(10)

    # 3. Tableau des Articles et Tarification
    items_table = doc.add_table(rows=3, cols=4)
    items_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Désignation de la prestation", "Quantité", "Tarif Unitaire (FCFA)", "Total (FCFA)"]
    widths = [Inches(3.5), Inches(0.9), Inches(1.2), Inches(1.2)]

    # Ligne d'en-tête du tableau
    for idx, name in enumerate(headers):
        cell = items_table.cell(0, idx)
        cell.width = widths[idx]
        set_cell_background(cell, "1E293B")
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER if idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
        run = p.add_run(name)
        run.bold = True
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(255, 255, 255)

    # Ligne 1 : Bouteille de Gaz
    row1 = items_table.rows[1]
    c0 = row1.cells[0]
    c0.paragraphs[0].add_run(f"{commande['article']}\n").bold = True
    r_sub = c0.paragraphs[0].add_run(f"Interchangeabilité respectée : {commande['marque_echangee']}")
    r_sub.font.size = Pt(8)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(100, 116, 139)

    row1.cells[1].paragraphs[0].add_run("1").alignment = WD_ALIGN_PARAGRAPH.CENTER
    row1.cells[2].paragraphs[0].add_run(f"{commande['prix_bouteille']:,} F").alignment = WD_ALIGN_PARAGRAPH.RIGHT
    row1.cells[3].paragraphs[0].add_run(f"{commande['prix_bouteille']:,} F").alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Ligne 2 : Frais de Livraison (palier kilométrique)
    row2 = items_table.rows[2]
    c1 = row2.cells[0]
    c1.paragraphs[0].add_run("Frais de livraison express à domicile\n").bold = True
    r_dist = c1.paragraphs[0].add_run(f"Distance mesurée : {commande['distance_m']} m (Tarification au palier de 500m)")
    r_dist.font.size = Pt(8)
    r_dist.font.italic = True
    r_dist.font.color.rgb = RGBColor(100, 116, 139)

    row2.cells[1].paragraphs[0].add_run("1").alignment = WD_ALIGN_PARAGRAPH.CENTER
    row2.cells[2].paragraphs[0].add_run(f"{commande['frais_livraison']:,} F").alignment = WD_ALIGN_PARAGRAPH.RIGHT
    row2.cells[3].paragraphs[0].add_run(f"{commande['frais_livraison']:,} F").alignment = WD_ALIGN_PARAGRAPH.RIGHT

    # Application de bordures et espacements sur les lignes
    for row in items_table.rows[1:]:
        for cell in row.cells:
            cell.paragraphs[0].paragraph_format.space_before = Pt(4)
            cell.paragraphs[0].paragraph_format.space_after = Pt(4)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # 4. Bloc Total & Paiement
    tot_table = doc.add_table(rows=2, cols=2)
    tot_table.alignment = WD_TABLE_ALIGNMENT.CENTER

    cell_pay = tot_table.cell(0, 0)
    cell_pay.width = Inches(4.2)
    p_pay = cell_pay.paragraphs[0]
    p_pay.add_run("Mode de règlement : ").bold = True
    p_pay.add_run(f"{commande['moyen_paiement']}\n")
    p_pay.add_run("État de la transaction : ").bold = True
    p_pay.add_run(f"{commande['statut_paiement']}\n")
    p_pay.add_run("Reversement garanti livreur : ").bold = True
    p_pay.add_run("500 FCFA net (inclus dans la livraison)")

    cell_tot = tot_table.cell(0, 1)
    cell_tot.width = Inches(2.6)
    set_cell_background(cell_tot, "EA580C")
    p_tot = cell_tot.paragraphs[0]
    p_tot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_t1 = p_tot.add_run("TOTAL RÉGLÉ\n")
    r_t1.font.size = Pt(10)
    r_t1.font.color.rgb = RGBColor(255, 255, 255)
    r_t2 = p_tot.add_run(f"{commande['total_payer']:,} FCFA")
    r_t2.bold = True
    r_t2.font.size = Pt(16)
    r_t2.font.color.rgb = RGBColor(255, 255, 255)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # 5. Sécurité anti-fraude & Code OTP
    otp_p = doc.add_paragraph()
    otp_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    otp_run = otp_p.add_run(f"🔒 CODE DE LIVRAISON CLIENT (ANTI-FRAUDE) : {commande['code_otp']}\n")
    otp_run.bold = True
    otp_run.font.size = Pt(12)
    otp_run.font.color.rgb = RGBColor(22, 101, 52)
    sub_otp = otp_p.add_run("Ne communiquez ce code au livreur qu'après réception physique et vérification de la conformité de votre bouteille de gaz.")
    sub_otp.font.size = Pt(8.5)
    sub_otp.font.italic = True

    # 6. Pied de page légal et signatures
    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    sig_table = doc.add_table(rows=1, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER

    sig1 = sig_table.cell(0, 0)
    sig1.width = Inches(3.4)
    sig1.paragraphs[0].add_run("Signature du Client Réceptionnaire :\n\n\n__________________________").font.size = Pt(9)

    sig2 = sig_table.cell(0, 1)
    sig2.width = Inches(3.4)
    sig2.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    sig2.paragraphs[0].add_run("Pour 18 EITHING SARL (La Direction) :\nM. Hubert C. TOKPANOU / M. Pedro S. KPONON\n\n__________________________").font.size = Pt(9)

    doc.save(output_path)
    print(f"Facture Word générée avec succès : {output_path}")
    return output_path

if __name__ == "__main__":
    sortie = sys.argv[1] if len(sys.argv) > 1 else "Facture_GazExpress_Modele.docx"
    generer_facture_word(output_path=sortie)
