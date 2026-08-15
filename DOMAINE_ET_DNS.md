# Guide de Configuration DNS et Validation du Domaine `18eithing.bj`

Ce guide explique pas à pas les démarches à suivre une fois le nom de domaine **18eithing.bj** validé auprès de votre registraire / hébergeur béninois.

---

## 1. Informations du Domaine
- **Nom de domaine principal** : `18eithing.bj`
- **Sous-domaine www** : `www.18eithing.bj`
- **Email officiel de contact** : `contact@18eithing.bj`

---

## 2. Configuration des Enregistrements DNS (Domain Name System)

Rendez-vous dans la console d'administration DNS de votre hébergeur / registraire au Bénin (Zone DNS / Gestion des enregistrements).

### A. Si votre site est hébergé sur Netlify (comme `preeminent-longma-8cd4a6.netlify.app`)

1. **Ajouter le domaine dans Netlify** :
   - Allez sur votre tableau de bord Netlify.
   - Sélectionnez votre site -> **Domain management** -> **Add custom domain**.
   - Entrez `18eithing.bj`.

2. **Configurer la Zone DNS chez votre registraire béninois** :

| Type  | Nom / Hôte | Valeur / Cible | TTL | Description |
|-------|------------|----------------|-----|-------------|
| **A** | `@` (ou vide) | `75.2.60.5` | 3600 | Pointe le domaine principal vers l'IP de Netlify Load Balancer |
| **CNAME** | `www` | `preeminent-longma-8cd4a6.netlify.app.` | 3600 | Pointe `www.18eithing.bj` vers votre site Netlify |

*(Remarque : Si vous utilisez Netlify DNS, vous pouvez aussi simplement remplacer les Serveurs de Noms / Nameservers chez votre registraire par ceux fournis par Netlify, ex: `dns1.p01.nsone.net`)*.

---

### B. Si votre site est hébergé sur GitHub Pages

1. **Fichier CNAME dans le projet** :
   - Le fichier `CNAME` contenant `18eithing.bj` est déjà présent à la racine du dépôt.

2. **Enregistrements DNS chez le registraire béninois** :

| Type  | Nom / Hôte | Valeur / Cible | TTL |
|-------|------------|----------------|-----|
| **A** | `@` | `185.199.108.153` | 3600 |
| **A** | `@` | `185.199.109.153` | 3600 |
| **A** | `@` | `185.199.110.153` | 3600 |
| **A** | `@` | `185.199.111.153` | 3600 |
| **CNAME** | `www` | `<votre-username-github>.github.io.` | 3600 |

---

## 3. Configuration des Messageries Web / Email (`contact@18eithing.bj`)

Pour recevoir et envoyer des emails avec l'adresse `contact@18eithing.bj` :

1. Dans votre espace d'hébergement béninois ou webmail :
   - Créez un compte email ou une redirection email pour `contact@18eithing.bj`.
2. Configurez les enregistrements MX (Mail Exchange) fournis par votre service email (ex: cPanel, Google Workspace, Titan, etc.).
3. Ajoutez les enregistrements SPF et DKIM recommandés par votre fournisseur pour éviter que les e-mails ne finissent en SPAM.

---

## 4. Activation du Certificat SSL / HTTPS (Sécurité)

- Sur Netlify ou GitHub Pages, l'activation du certificat SSL Let's Encrypt se fait **automatiquement** dès que la propagation DNS est effective (compter entre 1h et 24h).
- Assurez-vous d'activer l'option **"HTTPS obligatoire"** (Force HTTPS) dans les paramètres du domaine.

---

## 5. Vérification & Validation

Une fois la configuration terminée :
1. Testez le site dans votre navigateur : `https://18eithing.bj` et `https://www.18eithing.bj`.
2. Testez l'envoi d'un message à `contact@18eithing.bj`.
3. Cliquez sur le bouton WhatsApp du site pour vérifier le bon fonctionnement du lien interactif.
