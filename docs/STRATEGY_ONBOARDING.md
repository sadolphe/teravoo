# STRATÉGIE D'ONBOARDING TERAVOO

**Version**: 1.0
**Date**: 2025-01-10
**Author**: Product Architect & Trust Compliance Lead

---

## PARTIE 1 – Principes d’onboarding TeraVoo

### Pourquoi un onboarding unique serait un échec
TeraVoo connecte deux mondes aux contraintes radicalement opposées : le **terrain malgache** (faible connectivité, culture orale, informalité) et le **marché international B2B** (exigence de conformité, digital-first, aversion au risque).
Tenter d'appliquer un flux d'inscription standard (Email > MdP > Profil) échouerait car :
1.  Les producteurs n'ont pas d'email ou d'usage numérique autonome.
2.  Les facilitateurs ont besoin d'outils opérationnels immédiats, pas de lourdeur administrative.
3.  Les acheteurs ont besoin de preuves de confiance avant de s'engager, pas d'un formulaire vide.

### Principes Directeurs
1.  **Onboarding Progressif** : Ne demander une information que lorsqu'elle devient nécessaire à l'opération suivante.
2.  **Onboarding Contextuel** : L'inscription n'est pas une étape isolée, elle est intégrée à l'action (ex: s'inscrire en scannant une vanille).
3.  **Onboarding par la Preuve** : La confiance ne se décrète pas par un badge "Vérifié", elle se construit par l'accumulation de données (historique, scans, transactions).
4.  **Friction Volontaire** : Introduire des étapes de validation humaine ou technique là où la fraude pourrait détruire la valeur de la plateforme (KYC Acheteur, Validation Facilitateur).

---

## PARTIE 2 – Onboarding Producteur (Assisté / Indirect)

### 1. Positionnement
Le producteur de vanille (fermier) n'est **pas** un utilisateur direct de l'application au sens classique. Il est **représenté**.
Son "compte" est une identité numérique gérée et garantie par un tiers de confiance : le **Facilitateur** (ou Coopérative).

### 2. Déclencheur d’onboarding
Le producteur n'entre pas dans le système en cliquant sur "S'inscrire". Il entre quand **son produit entre**.
*   **Moment clé** : Lors de la **première collecte** ou du **premier audit terrain** par un Facilitateur.
*   **Action** : Le Facilitateur scanne un lot de vanille ou enregistre une parcelle. Si le producteur n'existe pas, il est créé à la volée.

### 3. Données collectées (MVP)

#### Obligatoire (Bloquant)
*   **Nom / Prénom ou Surnom local** : Pour l'identification humaine.
*   **Lieu de production (Fokontany / Village)** : Pour la traçabilité géographique de base.
*   **Lien avec le Facilitateur** : Qui est responsable de ce profil (ID Facilitateur).

#### Facultatif (Enrichissement)
*   **Photo du Producteur** : Humanisation du profil pour l'acheteur.
*   **Années d'expérience** : Storytelling.
*   **Superficie estimée** : Capacité de production.

#### Enrichissement ultérieur (Pas à l'inscription)
*   **Coordonnées mobiles** : Si paiement mobile envisagé plus tard.
*   **Carte d'identité nationale** : Uniquement si formalisation légale requise.

### 4. Parcours réel
1.  **Terrain** : Le Facilitateur rencontre le Producteur dans son champ ou au point de collecte.
2.  **App Mobile (Facilitateur)** : "Nouveau Lot" > "Sélectionner Producteur" > "Créer Nouveau".
3.  **Saisie** : Le Facilitateur entre le nom et le village. Il prend une photo du producteur (avec son accord).
4.  **Validation** : Le profil est créé en mode "Non Vérifié" (trust score bas).
5.  **Consolidation** : C'est la répétition des transactions avec ce profil qui le validera définitivement.

### 5. Limites volontaires
*   **Pas d'accès direct ("Login")** : Le producteur ne se connecte pas. Il n'a pas de mot de passe. Il reçoit (éventuellement) des SMS de confirmation.
*   **Pas de négociation prix** : Le prix est fixé avec le Facilitateur, pas négocié en direct sur l'app avec un acheteur à New York (protection contre la volatilité et complexité).
*   **Pas de gestion logistique** : C'est le rôle du Facilitateur.

---

## PARTIE 3 – Onboarding Facilitateur (Utilisateur Clé)

### 1. Rôle produit
Le Facilitateur est la **clé de voûte**. C'est lui qui injecte la donnée (la vérité terrain). Si son onboarding est raté, la donnée est fausse, et la plateforme perd toute valeur. Il est l'utilisateur "Power User" de l'App Mobile.

### 2. Parcours d’inscription
1.  **Création de compte (App Mobile)** : Numéro de téléphone + OTP (SMS). Pas d'email requis initialement pour réduire la friction.
2.  **Vérification Identité** : Upload photo CIN (Carte Identité Nationale) + Selfie.
3.  **Rattachement** :
    *   Si indépendant : Doit fournir une preuve d'agrément ou être validé par un Ops TeraVoo.
    *   Si employé de Coopérative : Entre un Code Coopérative fournit par son manager.
4.  **Activation** : Le compte est créé mais **bridé** (peut scanner en mode "brouillon" mais ne peut pas publier sur la Marketplace) tant que l'identité n'est pas validée.

### 3. Frictions volontaires
*   **Validation des droits de publication** : Un facilitateur ne peut pas rendre public des tonnes de vanille sans avoir été "Vérifié" par TeraVoo (appel téléphonique ou rencontre Ops).
    *   *Pourquoi ?* Éviter le spam de fausses offres qui décevraient les acheteurs.
*   **Formation forcée** : Lors du premier scan, un mini-tutoriel obligatoire (3 écrans) sur "Comment prendre une bonne photo" et "Comment utiliser le spectromètre (si applicable)".

---

## PARTIE 4 – Onboarding Acheteur B2B (Direct & Progressif)

### 1. Objectif
Rassurer, séduire, puis convertir. L'acheteur doit sentir qu'il entre dans un "cercle de confiance" et non sur un site e-commerce grand public.

### 2. Étapes d’onboarding

#### Niveau 1 : Exploration (Visiteur)
*   **Accès** : Libre (Landing page, Marketplace "floutée" ou partielle).
*   **Action** : Peut voir les prix moyens, des exemples de producteurs, la technologie.
*   **Restriction** : Ne peut pas voir les détails contractuels ni contacter.

#### Niveau 2 : Intention (Prospect)
*   **Déclencheur** : Clique sur "Voir les détails d'un lot" ou "Télécharger une fiche qualité".
*   **Données** : Email professionnel + Nom Entreprise.
*   **Action** : Accès aux fiches produits complètes.
*   **Validation** : Email vérifié.

#### Niveau 3 : Transaction (Client)
*   **Déclencheur** : Clique sur "Faire une offre" ou "Demande d'échantillon".
*   **Données (KYB)** : Kbis/Registration Doc, Adresse de facturation, Représentant légal.
*   **Friction** : L'accès aux fonctions de paiement/escrow est bloqué tant que la compliance (Lutte anti-blanchiment) n'est pas validée (automatique ou manuelle).

### 3. Données demandées par étape
*   **Tôt** : Intérêts (Quel volume cherchez-vous ? Quel grade ?). *Pourquoi ?* Pour personnaliser le dashboard immédiatement.
*   **Tard** : Documents légaux. *Pourquoi ?* Car c'est pénible. On ne le demande que quand l'acheteur est convaincu et prêt à payer.

### 4. UX & Messages
*   **Valeur de la friction** : "Pour garantir la sécurité de vos fonds sur l'Escrow, nous devons valider votre société conformément aux régulations bancaires." (C'est une feature de sécurité, pas une contrainte administrative).
*   **Rassurance** : Afficher les logos des partenaires de compliance (ex: Stripe Identity, Partenaires bancaires) dès le formulaire.

---

## PARTIE 5 – Onboarding Admin / Ops (Gardiens du Temple)

### Rôle
Les Ops TeraVoo ne s'onboardent pas eux-mêmes, ils sont créés par le CTO/SuperAdmin.

### Contrôle et Validation
L'Admin agit comme **Tiers de Confiance Humain** dans la boucle digitale :
1.  **Validation Facilitateurs** : Reçoit les alertes "Nouveau Facilitateur". Vérifie la cohérence des infos. Active le bouton "Droit de Publication".
2.  **Surveillance Compliance** : Reçoit les alertes de documents KYB invalides côté Acheteurs.
3.  **Gestion des Conflits** : A la main pour bloquer un compte (Producteur ou Acheteur) en cas de signalement de fraude.

---

## PARTIE 6 – Liens avec Our Producers & Traceability

### Trust Score (Score de Confiance)
L'onboarding est le **point zéro** du Trust Score.
*   Un profil complété à 100% = Bonus initial.
*   Un profil (Producteur) avec photo et géolocalisation précise = Indicateur de transparence.
*   Le Trust Score évolue ensuite dynamiquement avec l'activité (scans conformes, livraisons réussies).

### Visibilité
*   Un producteur mal onboardé (infos manquantes) sera invisible ou classé en bas de liste ("Profil incomplet").
*   Un acheteur non vérifié ne verra pas les "Offres Premium" réservées aux partenaires fiables.

### Traçabilité
L'onboarding du Facilitateur conditionne la **valeur de la preuve** de traçabilité.
*   Si le Facilitateur est "Certifié TeraVoo" (onboarding complet + formation), ses scans ont une valeur de "Preuve Forte" sur la blockchain.
*   S'il est nouveau, ses scans sont "À vérifier".

---
*Document confidentiel - Usage interne TeraVoo Tech & Product*
