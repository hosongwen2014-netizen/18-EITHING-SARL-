# Formules Clés & Rappels Fondamentaux - Licence Nationale en Logistique & Transport

Ce document regroupe les formules et concepts fondamentaux nécessaires pour résoudre avec précision les sujets de l'Examen National de Licence en Logistique & Transport.

---

## 1. Gestion des Stocks et des Approvisionnements

### Formule de Wilson (Quantité Économique Commandée - QEC / EOQ)
$$\text{QEC} = \sqrt{\frac{2 \times D \times Cl}{Cc}}$$
- **D** : Demande annuelle (en unités)
- **Cl** (ou $Ca$) : Coût de lancement/passation d'une commande
- **Cc** (ou $Cp$) : Coût de possession d'une unité en stock par an ($Cc = u \times i$ où $u$ est le prix unitaire et $i$ le taux de possession annuel)

### Nombre d'optimale de commandes ($N^*$)
$$N^* = \frac{D}{\text{QEC}}$$

### Période Économique / Cadence d'Approvisionnement ($T^*$)
$$T^* = \frac{360}{N^*}$$ (en jours) ou $\frac{12}{N^*}$ (en mois)

### Coût Total de Gestion des Stocks ($CT$)
$$CT = \text{Coût d'achat} + \text{Coût de lancement} + \text{Coût de possession}$$
$$CT(Q) = (D \times u) + \left(\frac{D}{Q} \times Cl\right) + \left(\frac{Q}{2} \times Cc\right)$$

### Stock de Sécurité ($SS$)
$$SS = Z \times \sigma \times \sqrt{L}$$
- **Z** : Facteur correspondant au niveau de service souhaité
- **$\sigma$** : Écart-type de la demande
- **L** : Délai de réapprovisionnement (Lead Time)

---

## 2. Commerce International & Incoterms 2020

### Classification des Incoterms 2020
1. **Multimodaux** : EXW, FCA, CPT, CIP, DAP, DPU, DDP
2. **Maritimes / Voies Navigables** : FAS, FOB, CFR, CIF

### Calcul de la Valeur en Douane à l'Importation
- **Assiette des Droits de Douane (Valeur CAF / CIF)** :
  $$\text{Valeur CAF} = \text{FOB} + \text{Fret} + \text{Assurance}$$
- **Droits de Douane (DD)** : $\text{Valeur CAF} \times \text{Taux DD}$
- **Taxes douanières (ex: TVA, Statistique, etc.)** calculées sur $(\text{Valeur CAF} + \text{DD} + \dots)$

---

## 3. Gestion des Transports & Calculs de Coûts

### Règle du Payant Pour (Règle du Taux Dégressif)
- On compare le coût réel : $\text{Poids réel} \times \text{Tarif tranche réelle}$
- Avec le coût de la tranche supérieure : $\text{Poids minimum tranche sup.} \times \text{Tarif tranche sup.}$
- On retient le coût le plus avantageux pour le chargeur.

### Rapport Poids / Volume (Ratios d'équivalence)
- **Maritime** : $1 \text{ tonne} = 1 \text{ m}^3$ (Ratio 1:1, Poids payant = $\max(\text{Masse en tonnes}, \text{Volume en m}^3)$)
- **Aérien** : $1 \text{ tonne} = 6 \text{ m}^3$ (ou $1 \text{ kg} = 6000 \text{ cm}^3 / 6 \text{ dm}^3$, Poids payant = $\max(\text{Poids réel kg}, \frac{\text{Volume m}^3}{0,006})$)
- **Routier** : $1 \text{ tonne} = 3 \text{ m}^3$ (Ratio 1:3)

---

## 4. Gestion d'Entrepôt et Plateformes

### Taux de Remplissage / D'occupation
$$\text{Taux d'occupation} = \frac{\text{Emplacements occupés}}{\text{Emplacements totaux disponibles}} \times 100$$

### Rotation des Stocks (Turnover)
$$\text{Ratios de rotation} = \frac{\text{Consommation ou Sorties de la période}}{\text{Stock moyen de la période}}$$
$$\text{Stock Moyen} = \frac{\text{Stock Initial} + \text{Stock Final}}{2}$$

---
