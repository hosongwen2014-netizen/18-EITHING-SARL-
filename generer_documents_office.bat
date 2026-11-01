@echo off
chcp 65001 >nul
title GazExpress Bénin - Générateur Word et Excel
color 0B

echo ======================================================================
echo          18 EITHING SARL - OUTILS WORD ET EXCEL GAZEXPRESS
echo ======================================================================
echo.
echo 1. Installation des modules Office (python-docx et openpyxl)...
pip install -r requirements.txt
echo.
echo 2. Génération de la Facture Word (.docx)...
python outils/generer_facture_word.py Facture_Officielle_GazExpress.docx
echo.
echo 3. Génération du Rapport Comptable Excel (.xlsx)...
python outils/generer_rapport_excel.py Rapport_Comptable_GazExpress.xlsx
echo.
echo ======================================================================
echo Terminé avec succès ! Vos fichiers Word et Excel sont prêts dans le dossier.
echo ======================================================================
echo.
pause
