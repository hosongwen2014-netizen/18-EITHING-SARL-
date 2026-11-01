@echo off
chcp 65001 >nul
title GazExpress Bénin - 18 EITHING SARL
color 0A

echo ======================================================================
echo          GAZEXPRESS BENIN - 18 EITHING SARL (KETOU, BENIN)
echo    Livraison Express de Gaz Domestique - Plateforme Operationnelle
echo ======================================================================
echo.
echo Verification de l'installation de Python sur votre ordinateur...
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo [ERREUR] Python n'est pas detecte sur votre systeme Windows !
    echo.
    echo Veuillez installer Python 64-bit depuis https://www.python.org/downloads/
    echo Pensez bien a cocher la case : "Add python.exe to PATH" lors de l'installation.
    echo.
    pause
    exit /b 1
)

echo [OK] Python est bien installe !
echo.
echo Demarrage du serveur local GazExpress sur le port 8080...
start "" http://localhost:8080/index.html
echo.
echo L'application s'ouvre dans votre navigateur web.
echo Pour arreter le serveur, fermez simplement cette fenetre noire.
echo ======================================================================
echo.

python -m http.server 8080
