# Mockups & Wireframes : Module Request Sourcing

**Document de Visualisation UI/UX**
**Objectif :** Concrétiser les spécifications fonctionnelles par des écrans clés.
**Format :** Wireframes Textuels (haute fidélité fonctionnelle).

---

## 🏗️ FLUX 1 : L'ACHETEUR CRÉE SA DEMANDE (WEB)
*L'acheteur est sur son Dashboard Desktop. Il veut sourcer 2 Tonnes de Vanille.*

### Écran 1.1 : Le "Wizard" - Étape Spécifications
```text
+-----------------------------------------------------------------------+
|  TERAVOO | Dashboard > Nouvelle Request Sourcing           [Step 1/4] |
+-----------------------------------------------------------------------+
|                                                                       |
|  1. QUEL PRODUIT CHERCHEZ-VOUS ?                                      |
|  [ Vanille (Gousses) v ]                                              |
|                                                                       |
|  2. CRITÈRES DE QUALITÉ (L'IA filtre pour vous)                       |
|  Grade Visé :                                                         |
|  ( ) GRADE A (Gourmet/Black) - Humidité > 30%                         |
|  (o) GRADE B (Red/Europe)    - Humidité 20-30%  <-- SÉLECTIONNÉ       |
|  ( ) GRADE C (Cuts/Vrac)                                              |
|                                                                       |
|  Critères Spécifiques :                                               |
|  [x] Taux Vanilline > 1.4% (Requis)                                   |
|  [ ] Taille > 16cm                                                    |
|                                                                       |
|  ---------------------------------------------------                  |
|  💡 AI INSIGHT :                                                      |
|  "Pour du Grade B à Madagascar actuellement, la                       |
|   taille moyenne est de 14-15cm. Exiger >16cm                         |
|   réduira vos résultats de 80%."                                      |
|  ---------------------------------------------------                  |
|                                                                       |
|                                         [ Suivant > ]                 |
+-----------------------------------------------------------------------+
```

### Écran 1.2 : Volume & Target (Barre de Progression Future)
```text
+-----------------------------------------------------------------------+
|  TERAVOO | Dashboard > Nouvelle Request Sourcing           [Step 2/4] |
+-----------------------------------------------------------------------+
|                                                                       |
|  3. VOLUME CIBLE                                                      |
|  Quantité Totale Désirée : [ 2000 ] [ kg ]                            |
|                                                                       |
|  Logique d'Acceptation :                                              |
|  [x] MULTI-VENDEURS (Acceptation partielle)                           |
|      "Je suis prêt à construire ce volume avec plusieurs lots."       |
|      Minimum par lot : [ 100 ] kg                                     |
|                                                                       |
|  [ ] LOT UNIQUE (Un seul vendeur doit tout fournir)                   |
|                                                                       |
|  ---------------------------------------------------                  |
|  📊 VOTRE REQUEST BAR (Aperçu) :                                      |
|  [..................................................] 0 / 2000 kg     |
|  Une fois publiée, vous verrez cette barre se remplir                 |
|  au fur et à mesure des offres acceptées.                             |
|  ---------------------------------------------------                  |
|                                                                       |
|  [ < Retour ]                           [ Suivant > ]                 |
+-----------------------------------------------------------------------+
```

### Écran 1.3 : Prix & Budget (Pricing Advisor)
```text
+-----------------------------------------------------------------------+
|  TERAVOO | Dashboard > Nouvelle Request Sourcing           [Step 3/4] |
+-----------------------------------------------------------------------+
|                                                                       |
|  4. PRIX CIBLE (Incoterm FOB - Départ Port)                           |
|                                                                       |
|  Prix du Marché (Sava, Mada) : ~210 - 230 USD / kg                    |
|                                                                       |
|  Votre offre :                                                        |
|  [ 200 ] USD / kg                                                     |
|                                                                       |
|  ---------------------------------------------------                  |
|  ⚠️ AI WARNING :                                                      |
|  "Votre prix est 5% sous le marché bas.                               |
|   Risque de réponse faible.                                           |
|   Conseil : Montez à 215$ pour maximiser les offres."                 |
|   [ Appliquer 215$ ]                                                  |
|  ---------------------------------------------------                  |
|                                                                       |
|  [ < Retour ]                           [ Publier Request > ]         |
+-----------------------------------------------------------------------+
```

---

## 📱 FLUX 2 : LE FACILITATEUR RÉPOND (MOBILE)
*Faly, facilitateur à Sambava, reçoit une notif. Il n'a que 400kg.*

### Écran 2.1 : Notification & Détail (FOMO)
```text
+-----------------------------------+
|  TERAVOO                   🔔 2m  |
+-----------------------------------+
|  OPPORTUNITÉ SOURCING             |
|  Acheteur "Hambourg Spice"        |
|  Cherche : 2000kg Vanille Grade B |
|  Prix : 215$ / kg                 |
|                                   |
|  ÉTAT DE LA DEMANDE :             |
|  [████▒▒▒▒▒▒] 40% Comblé          |
|  Reste 1200kg à prendre !         |
|                                   |
|  VOTRE STOCK COMPATIBLE :         |
|  ✅ Lot #402 (Hantona) : 150kg    |
|  ✅ Lot #405 (Coop B)  : 250kg    |
|  TOTAL DISPO : 400kg              |
|                                   |
|  [ IGNORER ]   [ PROPOSER STOCK ] |
+-----------------------------------+
```

### Écran 2.2 : Réponse Partielle & Conditions
```text
+-----------------------------------+
|  < Retour    RÉPONDRE             |
+-----------------------------------+
|  Votre Proposition :              |
|                                   |
|  VOLUME :                         |
|  [ 400 ] kg                       |
|  (Vous ne comblez que 20% de la   |
|   demande totale).                |
|                                   |
|  PRIX PROPOSÉ :                   |
|  [ 215 ] $ / kg  (Prix demandé)   |
|                                   |
|  DISPONIBILITÉ :                  |
|  [x] Immédiate (En stock)         |
|  [ ] Récolte à venir              |
|                                   |
|  PHOTOS DE PREUVE :               |
|  [IMG_Lot402.jpg] [IMG_Lot405.jpg]|
|  ✅ Validé Grade B par IA         |
|                                   |
|       [ ENVOYER L'OFFRE ]         |
+-----------------------------------+
```

---

## 🏗️ FLUX 3 : LE DASHBOARD D'ORCHESTRATION (COMPLEXE)
*L'acheteur revient 2h plus tard. Plusieurs offres sont arrivées.*

### Écran 3.1 : La "Mega-Bar" de Progression
```text
+---------------------------------------------------------------------------+
|  REQUEST #REQ-2026-88 | Status : OPEN                                     |
|  Objet : 2000kg Vanille Grade B @ 215$                                    |
+---------------------------------------------------------------------------+
|                                                                           |
|  PROGRESSION DU SOURCING :                                                |
|                                                                           |
|  [██████████ (A) ][█████ (B) ][▒▒▒▒ (C) ][....................]           |
|  0kg            800kg       1200kg     1600kg               2000kg        |
|                                                                           |
|  Légende :                                                                |
|  [██] VERT : Offres Validées (800kg)                                      |
|  [▒▒] JAUNE : En Négociation (400kg)                                      |
|  [..] GRIS : Reste à trouver (800kg)                                      |
|                                                                           |
|  -----------------------------------------------------------------------  |
|                                                                           |
|  LISTE DES OFFRES REÇUES (Inbox) :                                        |
|                                                                           |
|  | Vendeur    | Vol.  | Prix   | Trust Score | Action                     |
|  |------------|-------|--------|-------------|----------------------------|
|  | Coop SAVA  | 800kg | 215$   | 🟢 4.8/5    | ✅ VALIDÉ (Ajouté au panier)|
|  | Faly Facil.| 400kg | 220$   | 🟢 4.5/5    | 💬 NÉGOCIER (Prix +haut)   |
|  | New Vended | 900kg | 205$   | 🔴 2.1/5    | ⚠️ REJETÉ (Risque Qualité) |
|                                                                           |
+---------------------------------------------------------------------------+
```

---

## 💬 FLUX 4 : NÉGOCIATION & CONTRAT
*L'acheteur clique sur "Négocier" avec Faly.*

### Écran 4.1 : Chat Contextuel (Acheteur View)
```text
+-----------------------------------------------------------------------+
|  CHAT AVEC FALY (Facilitateur) | Offre : 400kg @ 220$ (Cible 215$)    |
+-----------------------------------------------------------------------+
|  [ SYSTEM ] : Faly propose 220$ (+2.3% vs Target).                    |
|                                                                       |
|  [ ACHETEUR ](FR) :                                                   |
|  "Bonjour Faly. Je prends ton lot entier si tu t'alignes à 215$."     |
|                                                                       |
|       (Traduction auto -> MG : "Miarahaba Faly...")                   |
|                                                                       |
|  [ FALY ](MG -> FR) :                                                 |
|  "Bonjour. Mes producteurs ont une qualité extra sèche (22%).          |
|   218$ est mon dernier prix."                                         |
|                                                                       |
|  ---------------------------------------------------                  |
|  🤖 AI COPILOTE :                                                     |
|  "Faly a un excellent historique sur l'humidité.                      |
|   Accepter 218$ (+3$ total = +1200$) sécurise 400kg                   |
|   de très bonne qualité. Conseil : ACCEPTER."                         |
|  ---------------------------------------------------                  |
|                                                                       |
|  [ Refuser ]      [ Proposer 216$ ]      [ ✅ ACCEPTER À 218$ ]       |
+-----------------------------------------------------------------------+
```

### Écran 4.2 : Le Contrat Consolidé (Checkout)
*Une fois Faly accepté, la barre est à 1200/2000kg. L'acheteur décide de clore la Request et d'acheter les 1200kg trouvés.*

```text
+-----------------------------------------------------------------------+
|  VALIDATION FINALE DE LA REQUEST                                      |
+-----------------------------------------------------------------------+
|                                                                       |
|  RÉCAPITULATIF COMMANDE GROUPÉE :                                     |
|                                                                       |
|  1. Lot A (Coop SAVA)   : 800 kg @ 215$ = 172,000 $                   |
|  2. Lot B (Faly)        : 400 kg @ 218$ =  87,200 $                   |
|                             -------------------------                 |
|  TOTAL VOLUME           : 1 200 kg                                    |
|  TOTAL PRIX (FOB)       : 259 200 $                                   |
|                                                                       |
|  DOCUMENTATION GÉNÉRÉE :                                              |
|  [📄 Contrat_Cadre_REQ88.pdf] (Inclut Annexe A et B)                  |
|  [📄 Proforma_Invoice_Global.pdf]                                     |
|                                                                       |
|  ACTION REQUISE :                                                     |
|  Pour valider ces lots et bloquer le stock chez les vendeurs :        |
|                                                                       |
|      [ SIGNER & PASSER AU PAIEMENT (ESCROW) ]                         |
|                                                                       |
+-----------------------------------------------------------------------+
```
