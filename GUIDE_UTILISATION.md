# Guide d'Utilisation, d'Appropriation et de Test de GazExpress Bénin 🇧🇯

Bienvenue dans le guide officiel de **GazExpress**, l'application développée pour **18 EITHING SARL**. Ce document vous explique pas à pas comment accéder au projet, comment vous l'approprier et comment tester toutes ses fonctionnalités.

---

## 1. Comment Accéder au Projet et le Lancer

L'application a été conçue comme une **Application Web Progressive (PWA)** sans dépendance complexe. Cela signifie qu'elle fonctionne immédiatement sur n'importe quel ordinateur, tablette ou smartphone.

### Méthode A : Lancer le projet sur votre ordinateur (Local)
1. Ouvrez un terminal dans le dossier du projet.
2. Lancez un serveur web local léger avec Python :
   ```bash
   python3 -m http.server 8080
   ```
3. Ouvrez votre navigateur internet (Chrome, Safari, Firefox, Edge) et rendez-vous sur :
   ```
   http://localhost:8080
   ```
   ou double-cliquez directement sur le fichier `index.html`.

### Méthode B : Mettre le projet en ligne pour tout le Bénin (Netlify / GitHub Pages / 18eithing.bj)
Comme votre domaine officiel est **18eithing.bj** et que votre infrastructure utilise déjà Netlify :
- Il vous suffit de pousser ces fichiers sur votre dépôt GitHub.
- Netlify déploie automatiquement le site en quelques secondes.
- Vos clients et livreurs peuvent alors y accéder directement via :
  `https://gaz.18eithing.bj` ou `https://18eithing.bj`.

---

## 2. Comment s'Approprier le Projet (Personnalisation)

Tous les paramètres stratégiques de votre entreprise sont centralisés dans des fichiers clairs et commentés :

- **Modifier les prix officiels ou les formats de bouteilles :**
  Ouvrez le fichier `js/data.js` et modifiez la constante `INITIAL_PRODUCTS`.
- **Ajuster les barèmes de livraison ou la commission livreur :**
  Dans `js/data.js`, modifiez `DELIVERY_RATES` (ex: `driverPayout: 500`).
- **Gérer les banques et vos RIB d'entreprise :**
  Dans `js/data.js`, la liste `CONNECTED_BANKS` contient toutes les banques du Bénin avec leurs RIB / IBAN.
- **Ajouter des dépôts ou livreurs par défaut :**
  Modifiez `INITIAL_DEPOTS` ou `INITIAL_DRIVERS` dans `js/data.js`.

---

## 3. Guide Pas à Pas pour Essayer l'Application

L'application comporte 4 espaces accessibles via les onglets en haut de l'écran :

### 🛒 Étape 1 : Tester une Commande Client
1. Allez sur l'onglet **Espace Client**.
2. Observez la détection de votre position GPS ou déplacez le repère bleu (la maison 🏠) sur la carte.
3. Choisissez le type d'opération :
   - **🔄 Échange / Recharge**
   - **✨ Premier Achat Complet (Consignation)**
4. Sélectionnez le format : **6 kg** (Standard) ou **12,5 kg** (Grand format).
5. Regardez le devis instantané :
   - Le point de vente le plus proche est sélectionné automatiquement avec calcul exact de la distance.
   - Les frais de livraison sont calculés selon le barème officiel (500 F les 500 m pour 6 kg / 700 F les 500 m pour 12,5 kg).
6. Choisissez votre réseau MoMo (**MTN MoMo**, **Moov Money** ou **Celtiis Cash**) et saisissez votre numéro.
7. Cliquez sur **Valider et Payer avec MoMo** :
   - Le simulateur push USSD apparaît.
   - Tapez le code secret (ex: `1234`) et confirmez.
   - La commande est validée ! Un **Code Secret OTP Client à 4 chiffres** s'affiche en vert dans le suivi en direct.

### 🛵 Étape 2 : Tester l'Espace Livreur
1. Cliquez sur l'onglet **Espace Livreur** en haut.
2. Vous voyez :
   - Le nom du livreur connecté (ex: Bio Chabi).
   - Le solde de son portefeuille virtuel (ses gains cumulés).
   - Son statut (**En service / Disponible**, En cours de livraison, Hors service).
3. Dans la liste des courses, la nouvelle commande apparaît avec les détails : nom du client, adresse, point de vente et gain garanti de **+500 FCFA**.
4. **Test de sécurité Anti-Fraude :**
   - Si le livreur essaie de valider sans le code OTP ou avec un faux code, l'application bloque la confirmation.
   - Dès qu'il saisit le code OTP que le client lui remet en main propre, la course est validée et ses 500 FCFA sont débloqués sur son portefeuille.
5. Cliquez sur **Demander virement MoMo** pour voir le retrait instantané de son solde.

### 🏬 Étape 3 : Tester l'Espace Points de Vente & Dépôts
1. Cliquez sur l'onglet **Points de Vente & Dépôts**.
2. Vous pouvez :
   - **Inscrire un nouveau livreur partenaire :** Remplissez le nom, téléphone, type d'engin (moto, tricycle) et immatriculation. Il apparaît instantanément sur la plateforme.
   - **Recenser une nouvelle station / dépôt :** Renseignez le nom, la ville et les coordonnées GPS. Le dépôt s'ajoute immédiatement à la carte interactive nationale.
   - Consulter l'état des stocks en direct de chaque dépôt.

### 📊 Étape 4 : Tester le Tableau de Bord Direction & Marges (18 EITHING SARL)
1. Cliquez sur l'onglet **Direction & Marges**.
2. Observez en temps réel :
   - Le **Chiffre d'Affaires Journalier Total** encaissé par MoMo.
   - La **Part Dépôts** (montant réservé pour racheter les bouteilles).
   - La **Rémunération des Livreurs** (somme des forfaits de 500 F).
   - La **Marge Nette Entreprise** (bénéfice net réalisé par 18 EITHING SARL).
3. **Module Multi-Banques :**
   - Sélectionnez la banque réceptrice de votre choix dans le menu déroulant (BOA, Ecobank, UBA, SGB, NSIA, Coris, BIIC...).
   - Cliquez sur **Générer l'Ordre de Virement vers la Banque Sélectionnée** pour télécharger instantanément l'ordre de virement officiel prêt à être transmis à votre banquier.
4. **Point Journalier des Ventes :**
   - Cliquez sur **Exporter le Bilan (CSV/Excel)** pour obtenir le fichier comptable complet de la journée.

---

## 8. Utilisation sous Windows (Office 64-bit & Python)

Si vous utilisez un ordinateur avec **Windows 64 bits et Microsoft Office (Word / Excel 64-bit)**, le projet propose une intégration directe sans aucune configuration complexe.

### 8.1 Démarrage rapide en 1 clic
Double-cliquez simplement sur le fichier :
* `demarrer_gazexpress.bat`

Ce script va automatiquement :
1. Vérifier la présence de Python sur votre machine.
2. Lancer le serveur local sur le port `8080`.
3. Ouvrir votre navigateur internet sur `http://localhost:8080/index.html`.

### 8.2 Génération automatique des Factures Word et Rapports Excel
Double-cliquez sur :
* `generer_documents_office.bat`

Ou exécutez directement en invite de commandes :
```cmd
pip install -r requirements.txt
python outils/generer_facture_word.py
python outils/generer_rapport_excel.py
```

Vous obtiendrez instantanément :
1. **`Facture_GazExpress_Modele.docx` :** Bon de livraison et facture Word aux couleurs de 18 EITHING SARL avec détails de la commande, calcul des frais kilométriques, coordonnées du client, du livreur et code secret OTP anti-fraude.
2. **`Rapport_Comptable_GazExpress.xlsx` :** Classeur Excel 3 feuilles comprenant :
   - Le journal des ventes et marges brutes de 18 EITHING SARL.
   - La réconciliation financière des flux Mobile Money (MTN, Moov, Celtiis) et des 10 banques agréées.
   - Le suivi des commissions nettes des livreurs (500 FCFA net / bouteille).
