# 🧑‍💻 Guide de Test Local (TeraVoo MVP)

Ce guide vous permet de lancer l'application complète (Base de données, Backend API, Frontend Web) sur votre machine locale pour tester le module "Request Sourcing".

## Pré-requis
*   Docker (pour la base de données)
*   Python 3.10+ (pour le backend)
*   Node.js 18+ (pour le frontend)

---

## Etape 1 : Démarrer l'infrastructure et le Backend

J'ai créé un script unique pour tout lancer facilement.

1.  Ouvrez votre terminal à la racine `Teravoo/`.
2.  Lancez le script de démarrage :
    ```bash
    sh start_dev.sh
    ```
    *Ce script va lancer Docker, installer les dépendances Python, et démarrer le serveur API sur le port 8000.*

**Alternative manuelle (si le script ne fonctionne pas) :**
```bash
# 1. DB
docker-compose up -d db

# 2. Backend
cd backend
source venv/bin/activate  # (ou python3 -m venv venv && source venv/bin/activate)
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## Etape 2 : Démarrer le Frontend

Dans un **second terminal** (laissez le premier tourner) :

1.  Allez dans le dossier web :
    ```bash
    cd web
    ```
2.  Installez les dépendances (si ce n'est pas fait) :
    ```bash
    npm install
    ```
3.  Lancez le serveur de développement :
    ```bash
    npm run dev
    ```

Le frontend sera accessible sur : **http://localhost:3000**

---

## Etape 3 : Scénario de Test Conseillé

Une fois l'app lancée, suivez ce parcours pour tout tester :

1.  **Dashboard** : Allez sur `http://localhost:3000/dashboard/requests`. (Vide au début).
2.  **Création** : Cliquez sur **"+ New Request"**.
    *   Remplissez le Wizard (Produit: Vanilla, Grade: A, Certs: Organic...).
    *   Validez la création.
3.  **Simulation Offre (Backend)** :
    *   L'interface web ne permet pas encore aux producteurs de répondre (c'est une app mobile séparée).
    *   Pour simuler une réponse, ouvrez un 3ème terminal et lancez mon script de test qui va injecter une offre :
        ```bash
        python3 test_advanced_flow.py
        ```
        *(Cela va créer une offre, générer un contrat, etc. sur la request ID 2 normalement)*
4.  **Retour Dashboard** : Rafraîchissez la page Web.
    *   Cliquez sur la demande.
    *   Constatez la **Mega-Bar** de progression, le **Trust Score**, le statut **Logistique**.
    *   Cliquez sur **"Generate Contract"** pour tester le téléchargement.

Bon test ! 🚀
