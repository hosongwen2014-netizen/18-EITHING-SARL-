# GazExpress Bénin 🇧🇯

**GazExpress** est une application web progressive (PWA) développée pour **18 EITHING SARL** servant d'interface nationale entre les clients utilisant le gaz domestique au Bénin, les points de vente agréés, les livreurs partenaires et la direction de l'entreprise.

---

## 🚀 Fonctionnalités Clés Réalisées

1. **Recensement & Géolocalisation des Points de Vente de Gaz :**
   - Base de données géolocalisée de dépôts agréés (Cotonou, Abomey-Calavi, Porto-Novo, Kétou, Parakou, etc.).
   - Visualisation interactive sur carte OpenStreetMap avec détails des stocks (Recharge vs Achat complet pour les formats 6 kg et 12,5 kg).
   - Formulaire d'enregistrement immédiat de nouveaux points de vente.

2. **Géolocalisation du Client par rapport au Dépôt le Plus Proche :**
   - Détection GPS native (ou repère déplaçable au doigt/souris).
   - Calcul de distance orthodromique précis (formule de Haversine).
   - Détermination instantanée du dépôt le plus proche.

3. **Moteur de Facturation de la Livraison selon la Distance & Format :**
   - **Format 6 kg (Standard) :** 500 FCFA les 500 m, 1 000 FCFA pour 1 km (1 000 m), puis +500 FCFA par tranche entamée de 500 m au-delà d'1 km (ex. 1,2 km = 1 500 FCFA).
   - **Format 12,5 kg (Grand Format) :** 700 FCFA les 500 m, 1 400 FCFA pour 1 km (1 000 m), puis +700 FCFA par tranche entamée de 500 m au-delà d'1 km.

4. **Paiement Mobile Money (Tous Réseaux Bénin) :**
   - Intégration de **MTN Mobile Money (*880#)**, **Moov Money (*155#)** et **Celtiis Cash (*888#)**.
   - Validation dynamique des préfixes des numéros de téléphone béninois.
   - Simulateur de push USSD interactif avec saisie du code PIN secret.

5. **Interconnexion Entreprise, MoMo et Banques :**
   - Passerelle pour réceptionner les paiements sur le compte marchand 18 EITHING SARL.
   - Module de virement bancaire automatique vers **Bank of Africa Bénin (BOA)**.
   - Génération téléchargeable de l'ordre de virement journalier.

6. **Point Journalier des Ventes & Dispatching des Marges Bénéficiaires :**
   - Chiffre d'affaires journalier global en direct.
   - Part Dépôts réapprovisionnement.
   - Part Livreurs : Rémunération garantie à **500 FCFA fixe net par course**.
   - Marge brute & nette entreprise (marge gaz + marge livraison).
   - Exportation du journal des ventes au format CSV/Excel.

7. **Suivi & Recrutement des Livreurs Géolocalisés :**
   - Attribution automatique de la course au livreur le plus proche.
   - Espace livreur avec portefeuille virtuel et demande de retrait MoMo.
   - Formulaire de recrutement et d'inscription de nouveaux livreurs sur la plateforme.

---

## 🛠️ Stack Technique
- HTML5 / CSS3 moderne (Responsive & PWA).
- JavaScript ES6 modulaire (`js/data.js`, `js/calculator.js`, `js/payment.js`, `js/app.js`).
- Cartographie OpenStreetMap & Leaflet.js.
- Tests unitaires automatisés sous Node.js (`tests/`).
