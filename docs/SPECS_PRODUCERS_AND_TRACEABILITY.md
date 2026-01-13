# Spécifications : "Our Producers" & "Traceability"

Ce document détaille la conception produit et technique des piliers **Producteurs** et **Traçabilité** de TeraVoo, basé sur le cadrage du projet.

---

# PARTIE 1 – "Our Producers"

## 1. Rôle de la section "Our Producers"

### À quoi sert cette section ?
Dans le parcours acheteur, la section "Our Producers" transforme une marketplace de commodités anonymes en une plateforme de **partenariat de confiance**. Elle permet à l'acheteur d'identifier **qui** produit la vanille (ou autre épice), validant ainsi la promesse "Direct Trade".

> **Cadrage Produit** : Cette section n'est pas une vitrine publique type "LinkedIn" (profile vanity), mais un **outil de décision B2B** orienté fiabilité et capacité industrielle.

### Pourquoi est-elle critique ?
*   **Confiance (Trust)** : L'acheteur international a besoin de savoir que derrière l'offre, il y a une réalité physique auditée, pas un trader opportuniste.
*   **Compliance** : Elle fournit les preuves nécessaires (CSR, équité) que l'acheteur doit souvent justifier à ses propres clients finaux.
*   **Différenciation** : Contrairement aux plateformes B2B classiques (Alibaba), TeraVoo ne vend pas un "stock" mais une capacité de production vérifiée.

### Articulation Facilitateur / Producteur
Le modèle TeraVoo repose sur le **Facilitateur**. La section "Our Producers" met en avant ce Facilitateur comme **point d'entrée fiable**, tout en donnant de la visibilité aux petits producteurs qu'il agrège. C'est le Facilitateur qui porte le "Trust Score", car c'est lui qui s'engage contractuellement.

---

## 2. Typologie des profils producteurs

Trois types de profils coexistent, mais leur visibilité diffère :

1.  **Le Facilitateur (Prioritaire & Visible)**
    *   **Définition** : Entrepreneur local, collecteur digitalisé ou leader de communauté. Il agrège l'offre de plusieurs fermes.
    *   **Rôle** : Interlocuteur commercial unique, responsable de la logistique FOB et de la qualité déclarée.
    *   **Visibilité** : Profil public complet. C'est lui que l'acheteur "choisit".

2.  **La Coopérative (Visible)**
    *   **Définition** : Structure formelle regroupant des producteurs.
    *   **Rôle** : Similaire au facilitateur, mais avec une gouvernance collective. Souvent associée à des labels (Fairtrade).
    *   **Visibilité** : Profil public complet.

3.  **Le Producteur Individuel (Masqué / "Nested")**
    *   **Définition** : Le fermier qui cultive réellement.
    *   **Rôle** : Fournit la matière première au Facilitateur.
    *   **Visibilité** : **Masquée par défaut** sur la marketplace pour éviter le contournement et simplifier la lecture.
    *   **Exception** : Ses données (Nom, Localisation précise) apparaissent dans la **Traceabilité** d'un lot spécifique, une fois l'offre émise.

---

## 3. Structure d'un profil "Producer" (Fiche Facilitateur)

### Informations Visibles (Confiance & Business)
*   **Identité** : Nom de la structure (ex: "Sava Gold Collectors"), Photo du responsable, Année de création.
*   **Localisation** : Région (ex: "Sava, Madagascar"), District. Carte approximative (rayon de 10km) pour protéger la sécurité.
*   **Produit & Volume** : Spécialités (Vanille Bourbon, Girofle), Capacité annuelle estimée (ex: "5 - 10 Tonnes").
*   **Certifications** : Badges vérifiés (Bio, Fairtrade) avec dates de validité.
*   **Performance (Track Record)** : "Membre depuis 2024", "12 Transactions réussies", "Dernière livraison : Paris, France".
*   **Trust Score** : Note globale (ex: 4.8/5) détaillée.

### Informations Masquées (Protection)
*   **Coordonnées directes** : Email, Téléphone, WhatsApp. (Le chat passe par TeraVoo tant que le contrat n'est pas signé).
*   **Liste exacte des fermiers** : Pour éviter que des concurrents ne démarch directement sa base de sourcing.
*   **Coordonnées GPS exactes de stockage** : Pour la sécurité physique contre le vol de vanille.

---

## 4. KPI & Confiance ("Airbnb-like")

Le **Trust Score** est l'actif principal du Facilitateur. Il est calculé algorithmiquement (MVP : Moyenne pondérée).

### KPI Affichés et Calcul (MVP)
1.  **Qualité Livrée vs Annoncée (Poids : 40%)** : Écart moyen entre le grade annoncé (AI Sourcing) et le grade validé à la réception.
2.  **Fiabilité Logistique (Poids : 30%)** : Respect des délais d'expédition (Date promise vs Date réelle FOB).
3.  **Taux de Réponse (Poids : 15%)** : % de Sourcing Requests auxquelles il répond et temps de réponse moyen.
4.  **Conformité Documentaire (Poids : 15%)** : Validité des documents KYC et Certifications uploadés.

### 4.1. Gestion des Conflits & Sanctions

Que se passe-t-il en cas de manquement ? Le système impose des pénalités automatiques pour rassurer les acheteurs institutionnels.

| Manquement | Conséquence Immédiate | Conséquence Long Terme |
| :--- | :--- | :--- |
| **Qualité non conforme** | Baisse du Trust Score (Composante Qualité) | Perte du badge "Premium" |
| **Retard Logistique** | Baisse du Trust Score (Composante Délai) | Exclusion des "Urgent Requests" |
| **Certificat Expiré** | Le badge devient "Inactif" (Grisé) | Suspension temporaire des ventes |
| **Fraude avérée** | Suspension immédiate du compte | Bannissement définitif (Blacklist) |

---

## 5. UX & Parcours Utilisateur

### Découverte
*   **Via "Our Producers"** : Carte interactive/Grille filtrable.
*   **Via Fiche Produit** : Lien contextuel "Sold by...".
*   **Via Request** : Lien depuis l'offre reçue.

### Actions
*   **Consulter** : Historique et avis (anonymisés).
*   **Favoris** : Ajouter aux fournisseurs privilégiés.
*   **Initier Request** : "Ask for Quotation" contextuel.

---

# PARTIE 2 – "Traceability"

## 6. Définition Produit de la Traçabilité TeraVoo

### Concept
Chez TeraVoo, la traçabilité n'est pas juste "d'où ça vient", mais **"la preuve que ce que j'ai acheté est ce qui a été expédié"**.
*   **Scope** : Du **Lot Initial** jusqu'à la **Livraison FOB**.
*   **Philosophie technique** : La traçabilité TeraVoo est conçue comme une **API interne**, afin de pouvoir être exportée vers des clients Enterprise (ERP) ou auditée par des tiers à l'avenir.

---

## 7. Objets Traçables (Modèle Conceptuel)

*   **Lot (Batch)** : Stock initial (avec QR Code interne).
*   **Sourcing Request** : Besoin acheteur.
*   **Sourcing Offer** : Proposition commerciale.
*   **Smart Contract** : Objet juridique figé.
*   **Shipment** : Objet logistique physique.

---

## 8. Timeline de Traçabilité (Cœur de la Feature)

Cette timeline est visible par l'acheteur pour chaque commande active.

### 8.1. Intégrité & Versioning (Append-Only)
*   **Append-Only** : La timeline fonctionne en "ajout seul". Aucune étape validée ne peut être supprimée.
*   **Correction** : Si une erreur survient (ex: mauvais poids déclaré), on ajoute un événement "Correction" qui annule et remplace la valeur précédente, mais l'erreur reste visible dans l'historique d'audit (transparence totale).
*   **Gouvernance** : Cela prouve à l'acheteur que la donnée est **gouvernée**, et non "bricolée" en base de données pour cacher des problèmes.

### 8.2. Qui voit quoi ? (Matrice RBAC)

| Rôle | Voir Traceability | Modifier / Ajouter | Télécharger Documents |
| :--- | :---: | :---: | :---: |
| **Acheteur** | ✅ (Vue complète) | ❌ | ✅ (Preuves) |
| **Facilitateur** | ✅ (Ses lots) | ✅ (Ses étapes : Origine, Transit) | ❌ (Sauf les siens) |
| **Transitaire** | ❌ (Vue partielle) | ✅ (Logistique : Douane, FOB) | ❌ |
| **Produit (Admin)** | ✅ | ✅ (Arbitrage / Override) | ✅ |

### 8.3. Étapes Clés

| Étape | Donnée | Source | Validé par |
| :--- | :--- | :--- | :--- |
| **1. Origine** | Déclaration récolte, GPS | App Mobile | Facilitateur |
| **2. Qualité** | Analyse Photo/Humidité | **IA Scan** | **Système (Automatique)** |
| **3. Deal** | Prix, Volume, Incoterm | Contrat | Système (Figé) |
| **4. Préparation** | Mise en cartons, Poids final | App Mobile | Facilitateur |
| **5. Transit** | Départ Entrepôt | App Mobile (GPS) | Facilitateur |
| **6. Port (FOB)** | Certificat Phyto, Douane | Upload | Transitaire |
| **7. Final** | Bill of Landing (BL) | Upload | Transitaire |

---

## 9. Rôle de l'IA dans la Traçabilité

L'IA agit comme un **Auditeur Permanent** (Tierce Partie de Confiance virtuelle).
*   **Cohérence Visuelle** : Compare Lot Origine vs Lot Export.
*   **Cohérence Documents** : Cross-check Poids Phyto vs Poids Contrat.
*   **Géolocalisation** : Anti-fraude origine via GPS metadata.

---

## 10. Traçabilité & Conformité Export

*   **Passeport Produit** : Génération auto des preuves pour l'importateur.
*   **RDUE (Déforestation)** : Fourniture des points GPS anonymisés pour prouver la non-déforestation.
*   **Audit** : "Evidence Vault" accessible en un clic pour les contrôleurs.

---

## 11. UX "Traceability" Coté Acheteur

### Accès
*   Bouton "Track Order" (Dashboard/Email).
*   QR Code sur le contrat PDF.

### Présentation (UI)
*   Timeline Verticale (Vert = Validé, Orange = Alerte).
*   Onglet "Evidence Vault" latéral pour les documents.

---

## 12. Évolution Future (Post-MVP)

*   **Blockchain** : Ancrage des hashs d'étapes sur Polygon (Preuve immuable).
*   **NFT Batch** : Tokenisation du lot pour le trading secondaire.
*   **Audit Tiers** : Accès "Auditeur" (Read-Only) pour Ecocert/Douanes.
