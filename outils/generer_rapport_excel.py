#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Générateur de Tableau de Bord Comptable et Journal des Marges Excel (.xlsx)
pour GazExpress Bénin - 18 EITHING SARL (Kétou, Bénin)
Direction : M. Hubert C. TOKPANOU (DG) / M. Pedro S. KPONON (Gérant)
"""

import sys
import os
from datetime import datetime, timedelta
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

def creer_rapport_comptable_excel(output_path="Rapport_Comptable_GazExpress.xlsx"):
    """Crée un classeur Excel complet avec suivi des ventes, marges 18 EITHING, commissions livreurs et réconciliation banques/MoMo."""
    wb = openpyxl.Workbook()

    # Style definitions
    font_titre = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    font_section = Font(name="Calibri", size=12, bold=True, color="1E293B")
    font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
    font_data = Font(name="Calibri", size=10)
    font_bold = Font(name="Calibri", size=10, bold=True)
    font_accent = Font(name="Calibri", size=10, bold=True, color="EA580C")

    fill_entete_principale = PatternFill(start_color="1A2B4C", end_color="1A2B4C", fill_type="solid")
    fill_orange = PatternFill(start_color="EA580C", end_color="EA580C", fill_type="solid")
    fill_header_table = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
    fill_zebra = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    fill_total = PatternFill(start_color="E2E8F0", end_color="E2E8F0", fill_type="solid")
    fill_vert = PatternFill(start_color="DCFCE7", end_color="DCFCE7", fill_type="solid")

    thin_border_side = Side(border_style="thin", color="CBD5E1")
    border_cell = Border(left=thin_border_side, right=thin_border_side, top=thin_border_side, bottom=thin_border_side)
    border_top_double = Border(top=Side(border_style="thin", color="000000"), bottom=Side(border_style="double", color="000000"))

    # =========================================================================
    # FEUILLE 1 : JOURNAL DES LIVRAISONS & MARGES
    # =========================================================================
    ws1 = wb.active
    ws1.title = "Journal Ventes & Marges"
    ws1.views.sheetView[0].showGridLines = True

    # Titre du journal
    ws1.merge_cells("A1:K1")
    cell_t1 = ws1["A1"]
    cell_t1.value = "18 EITHING SARL • GAZEXPRESS BÉNIN - JOURNAL DES LIVRAISONS & SUIVI DES MARGES"
    cell_t1.font = font_titre
    cell_t1.fill = fill_entete_principale
    cell_t1.alignment = Alignment(horizontal="center", vertical="center")
    ws1.row_dimensions[1].height = 40

    ws1.merge_cells("A2:K2")
    cell_t2 = ws1["A2"]
    cell_t2.value = f"Arrêté au {datetime.now().strftime('%d/%m/%Y à %H:%M')} | Direction : M. Hubert C. TOKPANOU (DG) & M. Pedro S. KPONON (Gérant)"
    cell_t2.font = Font(name="Calibri", size=9, italic=True, color="64748B")
    cell_t2.alignment = Alignment(horizontal="center", vertical="center")
    ws1.row_dimensions[2].height = 20

    # En-têtes du tableau
    colonnes_ventes = [
        "N° Commande", "Date & Heure", "Client", "Dépôt Origine", "Livreur Assigné",
        "Format", "Prix Bouteille (F)", "Frais Livr. (F)", "Total Client (F)",
        "Gain Livreur Net (F)", "Marge Brute 18 EITHING (F)"
    ]

    ws1.row_dimensions[4].height = 26
    for col_idx, col_name in enumerate(colonnes_ventes, start=1):
        c = ws1.cell(row=4, column=col_idx, value=col_name)
        c.font = font_header
        c.fill = fill_header_table
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

    # Données types simulées
    exemples_commandes = [
        ("CMD-8028", "01/11/2026 09:15", "M. Pedro KPONON", "Dépôt Central Gaz Akpakpa", "Bio Chabi", "6 kg", 4950, 1000, 5950, 500, 500),
        ("CMD-8029", "01/11/2026 09:40", "Mme Awa SOULE", "Dépôt Étoile Rouge", "Bio Chabi", "12.5 kg", 10300, 1400, 11700, 500, 900),
        ("CMD-8030", "01/11/2026 10:05", "Dr. Fabrice HOUNTON", "Dépôt Kétou Centre (Siège)", "Idrissou Mama", "6 kg", 4950, 500, 5450, 500, 0),
        ("CMD-8031", "01/11/2026 10:30", "Société AGRO-BENIN", "Dépôt Calavi Arconville", "Bio Chabi", "12.5 kg", 10300, 2100, 12400, 500, 1600),
        ("CMD-8032", "01/11/2026 11:10", "M. Hubert TOKPANOU", "Dépôt Kétou Centre (Siège)", "Idrissou Mama", "12.5 kg", 10300, 700, 11000, 500, 200),
        ("CMD-8033", "01/11/2026 11:45", "Mme Justine DOSSOU", "Dépôt Porto-Novo Ouando", "Marcelle Gbaguidi", "6 kg", 4950, 1000, 5950, 500, 500),
        ("CMD-8034", "01/11/2026 12:20", "Hôtel La Paix", "Dépôt Pobè Gare", "Marcelle Gbaguidi", "12.5 kg", 10300, 1400, 11700, 500, 900),
    ]

    start_row = 5
    for i, cmd in enumerate(exemples_commandes):
        current_row = start_row + i
        ws1.row_dimensions[current_row].height = 20
        fill_courant = fill_zebra if i % 2 == 1 else PatternFill(fill_type=None)

        for j, val in enumerate(cmd, start=1):
            c = ws1.cell(row=current_row, column=j, value=val)
            c.font = font_data
            c.border = border_cell
            if fill_courant.fill_type:
                c.fill = fill_courant

            # Formatage numérique FCFA
            if j in [7, 8, 9, 10, 11]:
                c.number_format = "#,##0"
                c.alignment = Alignment(horizontal="right", vertical="center")
            elif j in [1, 2, 6]:
                c.alignment = Alignment(horizontal="center", vertical="center")
            else:
                c.alignment = Alignment(horizontal="left", vertical="center")

    # Ligne de Total
    total_row = start_row + len(exemples_commandes)
    ws1.row_dimensions[total_row].height = 24
    ws1.merge_cells(start_row=total_row, start_column=1, end_row=total_row, end_column=6)
    c_tot_label = ws1.cell(row=total_row, column=1, value="TOTAUX DE LA PÉRIODE (FCFA)")
    c_tot_label.font = font_bold
    c_tot_label.alignment = Alignment(horizontal="right", vertical="center")
    c_tot_label.fill = fill_total

    for col in range(1, 7):
        ws1.cell(row=total_row, column=col).border = border_top_double
        ws1.cell(row=total_row, column=col).fill = fill_total

    for col in [7, 8, 9, 10, 11]:
        col_letter = get_column_letter(col)
        c_tot = ws1.cell(row=total_row, column=col)
        c_tot.value = f"=SUM({col_letter}5:{col_letter}{total_row-1})"
        c_tot.font = font_bold
        c_tot.fill = fill_total
        c_tot.border = border_top_double
        c_tot.number_format = "#,##0"
        c_tot.alignment = Alignment(horizontal="right", vertical="center")

    # Mise en évidence marge globale 18 EITHING
    c_marge_tot = ws1.cell(row=total_row, column=11)
    c_marge_tot.font = font_accent

    # =========================================================================
    # FEUILLE 2 : RÉCONCILIATION MOBILE MONEY & BANQUES
    # =========================================================================
    ws2 = wb.create_sheet(title="Réconciliation MoMo & Banques")
    ws2.views.sheetView[0].showGridLines = True

    ws2.merge_cells("A1:G1")
    t2 = ws2["A1"]
    t2.value = "RÉCONCILIATION DES CANAUX DE PAIEMENT - 18 EITHING SARL"
    t2.font = font_titre
    t2.fill = fill_orange
    t2.alignment = Alignment(horizontal="center", vertical="center")
    ws2.row_dimensions[1].height = 36

    headers_momo = ["Canal / Établissement", "Type de Flux", "Code / USSD", "Transactions", "Montant Collecté (F)", "Frais Passerelle (F)", "Net à Verser Compte 18 EITHING (F)"]
    ws2.row_dimensions[3].height = 24
    for idx, name in enumerate(headers_momo, start=1):
        c = ws2.cell(row=3, column=idx, value=name)
        c.font = font_header
        c.fill = fill_header_table
        c.alignment = Alignment(horizontal="center", vertical="center")

    donnees_canaux = [
        ("MTN Mobile Money Bénin", "Mobile Money", "*880#", 4, 35050, 350, 34700),
        ("Moov Money Bénin", "Mobile Money", "*155#", 2, 17150, 170, 16980),
        ("Celtiis Cash (SBIN)", "Mobile Money", "*889#", 1, 12000, 120, 11880),
        ("BOA Bénin (Compte Principal)", "Virement Bancaire", "RIB 01", 1, 45000, 0, 45000),
        ("Ecobank Bénin", "Virement Bancaire", "RIB 02", 0, 0, 0, 0),
        ("Coris Bank International", "Virement Bancaire", "RIB 06", 0, 0, 0, 0),
        ("Espèces à la livraison", "Cash / Livreur", "Reçu sécurisé", 2, 11400, 0, 11400),
    ]

    for i, ligne in enumerate(donnees_canaux, start=4):
        ws2.row_dimensions[i].height = 20
        for j, val in enumerate(ligne, start=1):
            c = ws2.cell(row=i, column=j, value=val)
            c.font = font_data
            c.border = border_cell
            if j in [4, 5, 6, 7]:
                c.number_format = "#,##0"
                c.alignment = Alignment(horizontal="right", vertical="center")
            else:
                c.alignment = Alignment(horizontal="left", vertical="center")

    # =========================================================================
    # FEUILLE 3 : COMMISSIONS LIVREURS (500 F NET / BOUTEILLE)
    # =========================================================================
    ws3 = wb.create_sheet(title="Commissions Livreurs")
    ws3.views.sheetView[0].showGridLines = True

    ws3.merge_cells("A1:F1")
    t3 = ws3["A1"]
    t3.value = "SUIVI DES COMMISSIONS LIVREURS (GARANTIE 500 FCFA NET / LIVRAISON)"
    t3.font = font_titre
    t3.fill = fill_entete_principale
    t3.alignment = Alignment(horizontal="center", vertical="center")
    ws3.row_dimensions[1].height = 36

    headers_livreurs = ["Matricule", "Nom du Livreur", "Véhicule / Zone", "Bouteilles Livrées", "Taux Unitaire Net (F)", "Total Net à Verser (F)"]
    ws3.row_dimensions[3].height = 24
    for idx, name in enumerate(headers_livreurs, start=1):
        c = ws3.cell(row=3, column=idx, value=name)
        c.font = font_header
        c.fill = fill_header_table
        c.alignment = Alignment(horizontal="center", vertical="center")

    donnees_livreurs = [
        ("LIV-01", "Bio Chabi", "Moto Tricycle Cargo (Littoral / Atlantique)", 3, 500, 1500),
        ("LIV-02", "Idrissou Mama", "Moto Dépannage (Plateau / Kétou)", 2, 500, 1000),
        ("LIV-03", "Marcelle Gbaguidi", "Tricycle Sécurisé (Ouémé / Pobè)", 2, 500, 1000),
    ]

    for i, ligne in enumerate(donnees_livreurs, start=4):
        ws3.row_dimensions[i].height = 20
        for j, val in enumerate(ligne, start=1):
            c = ws3.cell(row=i, column=j, value=val)
            c.font = font_data
            c.border = border_cell
            if j in [4, 5, 6]:
                c.number_format = "#,##0"
                c.alignment = Alignment(horizontal="right", vertical="center")
            else:
                c.alignment = Alignment(horizontal="left", vertical="center")

    # Ajustement automatique de la largeur des colonnes sur toutes les feuilles
    for ws in [ws1, ws2, ws3]:
        for col in ws.columns:
            max_len = 0
            col_letter = get_column_letter(col[0].column)
            for cell in col:
                # Ne pas prendre la ligne 1 fusionnée pour calculer la largeur
                if cell.row == 1:
                    continue
                val_str = str(cell.value or "")
                if len(val_str) > max_len:
                    max_len = len(val_str)
            ws.column_dimensions[col_letter].width = max(max_len + 3, 12)

    wb.save(output_path)
    print(f"Classeur Excel comptable généré avec succès : {output_path}")
    return output_path

if __name__ == "__main__":
    sortie = sys.argv[1] if len(sys.argv) > 1 else "Rapport_Comptable_GazExpress.xlsx"
    creer_rapport_comptable_excel(output_path=sortie)
