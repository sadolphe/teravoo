# Spécifications Fonctionnelles : Module Request Sourcing (RFP)

**Document de Design Produit**
**Date :** 10 Janvier 2026
**Auteur :** Antigravity (Product Architect)
**Source de vérité :** `TERAVOO_FULL_PROJECT_FRAMING.md`, `TERAVOO_MVP_PLAN.md`

---

## 1. Définition Fonctionnelle du Request Sourcing

### Concept
La "Request Sourcing" est une **Demande d'Approvisionnement Structurée**. Contrairement à une recherche classique où l'acheteur navigue dans le catalogue ("Picking"), ici l'acheteur exprime un besoin précis et laisse le "Smart Match™" (IA) et le réseau de Facilitateurs venir à lui.

C'est l'équivalent d'un **Appel d'Offres Privé ou Public** au sein de l'écosystème TeraVoo.

### Cas d'usage (Why & When)
*   **Quand l'utiliser ?**
    *   Volume important dépassant le stock visible d'un seul vendeur.
    *   Besoin spécifique non présent au catalogue (ex: "Vanille certifiée Bio équitable spécifique").
    *   Planification à l'avance (récolte future).
*   **Différence vs Recherche** :
    *   *Recherche* = "Je veux acheter ce que je vois maintenant" (Stock Spot).
    *   *Request* = "Je veux trouver qui peut me fournir ceci pour le mois prochain" (Sourcing stratégique).

### Périmètre Produits & Volumes
*   **Produits** : Focus MVP sur Vanille, Girofle, Litchi (Phases 1 & 2).
*   **Volumes** : Gros et Demi-Gros (B2B).
*   **Récurrence** : Non explicite dans les documents sources. *(Note : Les docs mentionnent "Commandes", "Contrats" et "Prédictif Stock", mais pas de moteur d'abonnement/livraison cadencée automatique dans le MVP).*

---

## 2. Création de la Request (Côté Acheteur)

### Formulaire & Logique Métier
L'interface est un "Wizard" (Assistant) guidé par étape pour éviter les demandes incomplètes.

1.  **Produit & Qualité** :
    *   Sélection Produit (ex: Vanille).
    *   Input : Grade attendu (A, B, C, Vrac). *Basé sur la classification IA Doc 1-3.2*.
    *   Input : Critères spécifiques (Taux humidité, Taux vanilline).
2.  **Quantité** :
    *   Target (ex: 1000 kg).
    *   **Tolérance** : Switch "Accepter livraisons partielles ?" (Oui/Non). Si Oui, minimum par lot (ex: 50kg).
3.  **Prix** :
    *   Choix : "Prix Fixe" ou "Fourchette de discussion".
    *   *Soutien IA* : Le "Pricing Advisor" (Doc 1-2.1) affiche le prix marché actuel et alerte si le prix cible est déconnecté ("Votre prix est 30% sous le marché, risque de 0 réponse").
4.  **Logistique** :
    *   **Incoterm** : **FOB (Free On Board) UNIQUEMENT** (*Contrainte stricte Doc 1 - Arbitrage Logistique*). L'acheteur doit savoir qu'il prend la main au port.
    *   Date limite d'expédition ("Ready to Ship by").
5.  **Géographie** :
    *   Origine souhaitée (ex: Madagascar / Sava).

### Contraintes Bloquantes (Validation)
*   Si le formulaire est incomplet sur le critère Grade (car l'IA ne pourra pas matcher).
*   Si la date de livraison est < Délai logistique incompressible calculé par l'IA.
*   Si l'acheteur n'est pas KYB validé (Business Verified).

---

## 3. Barre de Progression de la Demande

*Ceci est une conception UI basée sur la logique d'agrégation "Coopératives/Facilitateurs".*

### Design VIsuel
Une "Jauge de Remplissage" circulaire ou linéaire visible sur le Dashboard Acheteur.

*   **Affichage** : `[||||||....] 600kg / 1000kg sécurisés (60%)`.
*   **Détail** :
    *   Segments de couleurs différents par Vendeur/Facilitateur engagé.
    *   Indicateur de statut : "En négociation", "Validé", "En attente preuve".

### Comportement
*   **Sous-couverture** : Tant que < 100%, la Request reste "Ouverte" au marché (Smart Match continue de chercher).
*   **Sur-couverture** : Si les propositions cumulent > 100%, l'acheteur reçoit une alerte "Offres excédentaires, sélectionnez les meilleures".
*   **Visibilité Producteur** : Le producteur voit "Recherche 1000kg, reste 400kg à combler". Cela crée un sentiment d'urgence (FOMO).

---

## 4. Appel d'Offre & Réponses Producteurs

### Orchestration par "Smart Match"
1.  **Diffusion Ciblée** : L'IA ne spamme pas tout le monde. Elle notifie les Facilitateurs ayant :
    *   Stock déclaré compatible (Type/Grade).
    *   Historique de fiabilité (Trust Score > X).
    *   Géolocalisation pertinente.
2.  **Notification** : Message Push/WhatsApp au Facilitateur : *"Opportunité : Acheteur cherche 500kg Vanille A. Tu as 50kg en stock. Proposer ?"*

### Types de Réponses Producteurs
*   **Réponse Totale** : "Je prends tout le lot" (Rare pour les gros volumes).
*   **Réponse Partielle** : "Je peux fournir 50kg sur les 1000kg demandes".
*   **Contre-Proposition** : "Je peux fournir, mais à 260$ (vs 250$ cible)".

### Gestion Multi-Producteurs
Le système "Bucket" de TeraVoo agrège les lignes.
*   L'acheteur voit une seule Request, mais à l'intérieur, une liste de "Sous-lots" candidats.
*   Il doit valider chaque sous-lot individuellement ou faire une "Validation en masse" si les critères IA sont tous verts.

---

## 5. Négociation Assistée par IA

### Rôle de Copilote (Doc 1 - 1.1 Assistant)
L'IA ne décide pas, elle fluidifie.
*   **Traduction** : Chat temps réel Malgache <-> Anglais/Français.
*   **Contextualisation** :
    *   Si le vendeur propose un prix élevé, l'IA affiche à l'acheteur : *"Ce vendeur a un Trust Score de 4.9/5 et livre généralement en 2 jours. Le premium peut se justifier."*
    *   Si l'acheteur casse le prix, l'IA suggère au vendeur : *"Ce prix est bas, mais l'acheteur prend 1 tonne et paie comptant. Accepter sécurise votre saison."*

### Cadrage de la Conversation
*   L'IA détecte les impasses (boucle de refus). Elle propose : *"Voulez-vous couper la poire en deux à 245$ ?"*
*   Elle empêche de sortir du cadre sécurisé (bloque l'échange de numéros de téléphone perso / emails pour éviter le contournement "Desintermediation").

---

## 6. Conseils d'Achat & Vente

### Côté Acheteur (Arbitrage)
*   **Risk Score** : Pour chaque offre reçue, affichage d'un feu tricolore basé sur le "Producer Trust Score" (Doc 1-2.2).
*   **Market Insight** : "Le prix de la Vanille est en hausse (+5% cette semaine). Il est conseillé de clore le deal maintenant."

### Côté Vendeur (Opportunité)
*   **Pricing Guidance** : "Ton prix est 10$ au-dessus de la moyenne des offres reçues par cet acheteur. Baisse à 240$ pour gagner le marché."
*   **Alerting** : "Attention, cet acheteur demande un grade A strict. Ta photo a été notée 'B' par l'IA. Risque de litige élevé."

---

## 7. Certifications & Conformité

### Digitalisation des Preuves
*   La Request spécifie les certificats requis (Bio, Fairtrade, Phytosanitaire).
*   **Vérification** :
    *   Pour les labels (Bio) : Le Facilitateur upload le document une seule fois sur son profil. La Request vérifie la validité (Date exp).
    *   **Contrôle Documentaire IA** : L'IA scanne le PDF/Photo du certificat. Si illisible ou expiré, l'offre est "Flagged" (Impossible de rejoindre la Request avec le statut 'Certifié').
*   *Limitation* : En MVP, vérification visuelle (OCR). Pas de connexion API directe aux organismes certificateurs * (Non mentionné dans les docs)*.

---

## 8. Supply Chain & Promesse

### Statuts de la Request (Post-Deal)
Une fois les offres acceptées (consolidées), la Request passe en mode "Exécution".
1.  **Waiting for Escrow** : L'acheteur doit financer le montant total consolidé.
2.  **Ready to Ship** : Tous les producteurs sont notifiés.
3.  **Partial Shipping** : Comme c'est multi-vendeurs, la barre de livraison progresse lot par lot.
    *   *Producteur A a livré au port (BL validé) -> 10% livré.*
    *   *Producteur B a livré au port -> 30% livré.*
4.  **Completed** : 100% FOB (Marchandise à bord). La responsabilité TeraVoo/Vendeur s'arrête là (Incoterm FOB).

### Responsabilité
*   Chaque vendeur est responsable de *son* sous-lot jusqu'au port.
*   Le "Facilitateur" est le garant logistique local (c'est lui qui gère le transport vers le port pour ses producteurs).

---

## 9. Feature "Airbnb-like" : Producteurs Recommandés

### Algorithme de Ranking (Trust Score - Doc 1 2.2)
Les producteurs/facilitateurs s'affichent en tête de liste ("Best Match") selon :
1.  **Fiabilité Historique** : Taux d'annulations (Doit être bas).
2.  **Conformité Visuelle** : L'IA a-t-elle souvent confirmé leur grade annoncé ? (Pas de sur-promesse).
3.  **Réactivité** : Temps de réponse moyen au Chat.

### Mécanisme Anti-Favoritisme
*   Rotation des "Top Sellers" pour éviter que ce soient toujours les mêmes 3 gros qui prennent tout.
*   Label "New Rising Star" pour les nouveaux facilitateurs ayant réussi leurs 5 premières ventes parfaitement.

---

## 10. Contrat & Récapitulatif Final

### Génération "Smart Contract" (PDF)
Le système génère un **Contrat Cadre d'Achat** unique pour la Request, avec des annexes par Vendeur.
*   **Header** : Acheteur X s'engage à acheter 1T de Vanille.
*   **Split** :
    *   Lot 1 : 500kg auprès de Vendeur A (Prix X, Date Y).
    *   Lot 2 : 200kg auprès de Vendeur B.
    *   ...
*   **Clauses** : Standardisées TeraVoo (Qualité, Litige, FOB).

### Signature
*   **Acheteur** : Signe une fois pour la Request globale.
*   **Vendeurs** : Chaque Facilitateur signe (digitalement sur mobile) son Ordre de Vente (PO) spécifique.

### Valeur Juridique
Ce document, associé à la preuve de virement (Escrow) et au Bill of Lading (Preuve transport), constitue le "Dossier Litige" complet accessible aux arbitres TeraVoo en cas de problème.
