# Guide de Déploiement TeraVoo (2026)

Ce document récapitule la procédure pour déployer l'application sur **Render** (Backend) et **Vercel** (Frontend).

---

## 1. Architecture

*   **Repository** : `https://github.com/sadolphe/teravoo` (Monorepo pour Backend et Frontend).
*   **Backend** : Python (FastAPI) + PostgreSQL. Déployé sur **Render**.
*   **Frontend** : Next.js (TypeScript). Déployé sur **Vercel**.

---

## 2. Déploiement Backend (Render)

### Configuration du Service
*   **Type** : Web Service
*   **Repo** : `teravoo`
*   **Environment** : `Docker`
*   **Root Directory** : `web` (Attention : Render peut parfois avoir besoin de la racine, mais notre Dockerfile est dans `web`. Si vous déployez le backend Python, utilisez l'environnement **Python** standard, pas Docker).

> **Correction Importante** : Pour le BACKEND Python, nous utilisons l'environnement natif **Python 3** de Render, pas Docker. Docker est utilisé ici pour le Frontend si besoin ou pour des conteneurs isolés.

**Configuration Recommandée (Python Native) :**
*   **Build Command** : `pip install -r backend/requirements.txt`
*   **Start Command** : `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`

### Variables d'Environnement (Environment Variables)
À saisir dans le dashboard Render :

| Clé | Valeur | Description |
| :--- | :--- | :--- |
| `PYTHON_VERSION` | `3.11.0` | Version Python |
| `DATABASE_URL` | *Fourni par Render* | Lien vers la DB PostgreSQL (Internal connection string) |
| `BACKEND_CORS_ORIGINS_STR` | `https://votre-frontend.vercel.app` | Autorise le frontend à appeler l'API. (Mettre `*` pour tester au début) |

### Initialisation de la Base de Données
Une fois déployé, la base est vide. Pour la remplir avec les données de démo :
1.  Aller dans l'onglet **Shell** sur Render.
2.  Exécuter : `python backend/seed_producers_api.py`

---

## 3. Déploiement Frontend (Vercel)

### Configuration du Projet
*   **Framework Preset** : Next.js
*   **Root Directory** : `web` (Indispensable car le code Next.js n'est pas à la racine).

### Variables d'Environnement
À saisir sur Vercel :

| Clé | Valeur | Description |
| :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | `https://votre-backend.onrender.com/api/v1` | URL publique de votre API Backend. **Important** : Ajouter `/api/v1` à la fin. |

---

## 4. Dépannage Courant

### Erreur "404 Not Found" sur le Frontend
*   Vérifiez que le build Vercel est vert.
*   Vérifiez la variable `NEXT_PUBLIC_API_URL`.

### Erreur "500 Internal Server Error" sur l'API
*   Vérifiez les logs sur Render.
*   Souvent dû à la base de données vide -> Lancez le script de *seed*.
*   Ou problème CORS -> Vérifiez `BACKEND_CORS_ORIGINS_STR`.

### Erreur "Docker" sur Render
*   Si vous déployez le backend Python, n'utilisez **PAS** Docker. Choisissez "Environment: Python". Docker est réservé aux usages avancés ou au frontend hors-Vercel.
