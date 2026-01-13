# TeraVoo : Plan de Delivery MVP (Mission Commando)
*Source de vérité stricte : TERAVOO_FULL_PROJECT_FRAMING.md*

Ce document cadre l'exécution du MVP ("Horizon 1: Trust Foundation") pour une mise en production en **10 semaines maximum**.

---

## 1. Relecture & Extraction MVP

### 1.1. Proposition de Valeur Centrale (MVP)
*   **Pour le Producteur/Facilitateur** : Vendre de la vanille Grade A vérifiée à un prix juste (+30%).
*   **Pour l'Acheteur** : Sourcer sans risque (qualité prouvée par photo, fonds sécurisés).

### 1.2. Cibles MVP (Stricte)
*   **Persona B (Faly - Facilitateur)** : Utilisateur principal de l'App. C'est lui qui a le smartphone.
*   **Persona C (Sarah - Acheteuse)** : Utilisatrice du Dashboard Web pour acheter.
*   *Exclus du MVP* : Le producteur "Hantona" en autonomie (US 1.2 précise que c'est le Facilitateur qui agit pour lui via "Sous-compte").

### 1.3. Périmètre Core vs Post-MVP

| Feature | Core MVP (Horizon 1) | Post-MVP (Exclu) |
| :--- | :--- | :--- |
| **Accès** | Inscription Mobile (Tel) | Login Social, SSO Enterprise |
| **Catalogue** | Création produit, **Photo Booster (API Replicate)** | Vidéo, 3D, Réalité Augmentée |
| **Langue** | Traduction Chat (API GPT-4) | Doublage vocal temps réel |
| **Paiement** | **Manuel (Preuve virement import)** | Mobile Money Automatique, Crypto |
| **Logistique** | Incoterm **FOB** (Vendeur livre au port) | CIF, Door-to-Door, Tracking GPS camion |
| **Blockchain** | **AUCUNE** | Traçabilité Blockchain, Tokenisation |
| **Finance** | Escrow (Séquestre Manuel/Stripe) | Micro-crédit, Avance trésorerie |

---

## 2. Définition du MVP Final (Gel de Périmètre)

### Fonctionnalité 1 : Onboarding "Terrain" & KYC Light
*   **Objectif** : Enrôler des facilitateurs valides.
*   **Critères** :
    *   Upload photo ID.
    *   Validation manuelle par Admin (No KYC No Sale).
    *   Création de sous-profils producteurs (Nom + Photo).

### Fonctionnalité 2 : Catalogue Assisté IA (Photo Booster)
*   **Objectif** : Transformer une photo sombre en actif "vendable".
*   **Critères** :
    *   Input: Photo prise in-app.
    *   Processing: Détourage + Upscaling (API externe).
    *   Output: Visuel "Pro" sur fond neutre.
*   *Dépendance* : API Replicate/Flux.

### Fonctionnalité 3 : Chat & Négociation Multilingue
*   **Objectif** : Accorder sur le prix.
*   **Critères** :
    *   Chat texte simple.
    *   Bouton "Traduire" à la demande.
    *   Génération automatique Contrat PDF (Template fixe) une fois prix accordé.

### Fonctionnalité 4 : Paiement Séquestre (Escrow)
*   **Objectif** : Garantir la transaction.
*   **Critères** :
    *   Acheteur vire fonds sur compte cantonnement.
    *   Admin marque order "Fonds Reçus".
    *   Vendeur notifié "Go pour expédition".

---

## 3. Parcours Utilisateur MVP

### Flow "Vente Assistée" (Happy Path)
1.  **Onboarding** : Faly télécharge l'app (APK sideload ou Play Store), entre son tel, reçoit OTP.
2.  **Creation Profil** : Faly crée le profil de son oncle Hantona (Photo simple).
3.  **Qualité (Moment de Vérité)** : Faly prend photo de la vanille. Feedback visuel immédiat (IA : "Rejeté, trop flou" ou "Validé").
4.  **Mise en Vente** : Faly entre quantité (10kg) et prix FOB suggéré (250$).
5.  **Matching** : Sarah (Web) voit le produit. Envoie message "Ok pour 240$ ?".
6.  **Deal** : Faly voit message traduit "Accept 240$?". Il clique "Accepter".
7.  **Contrat** : PDF généré.
8.  **Escrow** : Sarah fait virement. Admin valide. Faly reçoit notif.
9.  **Expédition** : Faly livre au port. Upload BL (Bill of Lading).

### Cas d'Erreur (Bloquant MVP)
*   **Pas de Réseau** : Faly peut créer fiche et prendre photo. App stocke en local (SQLite). Sync auto dès retour réseau. (Indicateur jaune requis).

---

## 4. Spécification Fonctionnelle MVP

### User Stories Critiques
*   `US-AUTH-01` : En tant que Facilitateur, je me connecte par OTP SMS.
*   `US-PROD-01` : En tant que Facilitateur, je prends une photo et reçois une version "Studio" en <5s.
*   `US-CHAT-01` : En tant que Vendeur, je lis les messages Anglais en Malgache.
*   `US-ORDER-01` : En tant qu'Admin, je débloque les fonds manuellement après vérification BL.

### Ce qui est ABSENT (Hors Scope)
*   Pas de gestion de wallet en monnaie locale dans l'app (virements se font hors app pour le MVP, l'app ne fait que le tracking).
*   Pas de notation "Trust Score" algorithmique complexe (Score = Nombre de ventes réussies simple).
*   Pas de gestion logistique (juste upload document preuve).

---

## 5. Implémentation Technique MVP

### Architecture Minimale
*   **Mobile (Facilitateur)** : **Flutter**.
    *   *Justification* : Offline-first, Android Low-end.
    *   *Build* : APK direct pour test terrain.
*   **Web (Acheteur/Admin)** : **Next.js**.
    *   *Justification* : SEO, Vitesse, Dashboard React simple.
*   **Backend** : **Python FastAPI**.
    *   *Justification* : Facilité intégration IA, Perf.
*   **Database** : **PostgreSQL** (Hébergé Supabase ou AWS RDS).
    *   *Justification* : Relationnel robuste pour Orders/Users.
*   **Storage** : **AWS S3** (Buckets privés pour IDs, Publics pour Produits).

### Modèle de Données (MVP Critical)
*   `users` (id, phone, role, kyc_status)
*   `products` (id, seller_id, quality_grade, price_fob, status, photo_url_raw, photo_url_ai)
*   `orders` (id, buyer_id, product_id, amount, escrow_status={P_PENDING, P_SECURED, P_RELEASED})
*   `messages` (id, order_id, content_origin, content_translated)

### APIs Essentielles
*   `POST /auth/login` (OTP)
*   `POST /products/upload` (Image -> AI Service -> S3)
*   `GET /market/feed` (Liste publique)
*   `POST /orders/{id}/EscrowConfirm` (Admin only)

---

## 6. Plan de Delivery (Sprints 2 semaines)

### Sprint 1 : "Hello World & DB"
*   **Livrable** : Repo, DB Schema déployé, Auth OTP fonctionnelle.
*   **Risque** : Délai validation compte SMS (Twilio/local).

### Sprint 2 : "Catalogue & Vision"
*   **Livrable** : App Mobile permet upload photo + appel API IA (Replicate). Affichage galerie.
*   **Done** : Une photo moche devient belle dans l'app.

### Sprint 3 : "Marketplace & Chat"
*   **Livrable** : Web Acheteur (Liste), Chat simple Mobile<->Web.
*   **Done** : Envoi message "Test" reçu traduit.

### Sprint 4 : "Transaction Flow"
*   **Livrable** : Cycle de vie commande (Création -> Escrow -> Expé). PDF Gen.
*   **Done** : Flow complet simulé avec faux paiement.

### Sprint 5 : "Hardening & Deploy"
*   **Livrable** : Tests Terrain (Mode Offline), Security Audit light. Mise en Prod.

---

## 7. Mise en Production MVP

### Checklist Go-Live
1.  **Infra** : Serveur Back (Render/Railway/AWS), DB Prod.
2.  **Sécurité** : HTTPS partout, Bucket S3 privé par défaut, CORS strict.
3.  **Monitoring** : Sentry (Crash reporting App Mobile).
4.  **Admin** : Un compte "SuperAdmin" créé pour gérer KYC et Escrow manuellement.

### Acceptable en MVP
*   Validation KYC prend 24h (Humain).
*   Virement bancaire prend 3 jours.
*   Pas de push notification native (Polling ou SMS fallback).

### Non Négociable
*   **Perte de données offline**. (L'app DOIT sync).
*   **Sécurité des données bancaires** (Pas de stockage RIB en clair, utiliser Tokenisation Stripe ou simplement IBAN affiché statique pour virement).

---

## 8. Mesure & Apprentissage

### North Star Metric (MVP)
*   **1** : Nombre deTransactions "Terminées" (Fonds libérés au producteur). (Objectif: 5).

### KPIs Secondaires
*   **Taux d'activation Facilitateur** : % Inscrits qui postent 1 produit valide.
*   **Taux de succès IA** : % Photos acceptées du 1er coup par le système.

---

## 9. Décision Post-MVP

*   **Critère Go (V1)** : 5 Transactions réelles sans intervention technique (bugfix).
*   **Critère Pivot** : Si les facilitateurs refusent d'utiliser l'App ("Trop compliqué") -> Pivoter sur une App SMS/WhatsApp bot.
*   **Critère Itération** : Si l'IA rejette trop de photos ("Faux négatifs") -> Remplacer modèle ou autoriser "Override" manuel.

**Ce que le MVP doit prouver** : Qu'un facilitateur avec un smartphone à 50$ PEUT initier une vente internationale fiable.
