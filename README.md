# CVE Project - NVD Vulnerabilities

Ce projet est une solution complète pour la gestion et l'analyse des vulnérabilités CVE issues de la NVD. Il permet de :

- **Télécharger** les fichiers CVE depuis le NVD (JSON).
- **Extraire** toutes les données importantes (description, CVSS, CWE, CPE, etc.).
- **Insérer** ces données dans une base de données PostgreSQL.
- **Suivre** les changements historiques des CVE via l'API NVD (`/cvehistory/2.0`).

L'historique des changements est stocké dans la base de données PostgreSQL sous la table `importer_change_history`.

---

## Structure du projet

CVE_PROJECT/
├── src/
│   ├── downloader.py             # Téléchargement des fichiers JSON.gz
│   ├── extractor.py              # Extraction des données CVE depuis les fichiers
│   ├── importer_cve.py           # Insertion des CVE dans PostgreSQL
│   ├── importer_change_history.py # Récupération de l’historique d’une liste de CVE (API)
│   ├── import_allchangement.py   # Insertion de l’historique de changements pour plusieurs CVE
│   ├── config.py                 # Paramètres généraux (clé API, DB)
│   └── db.py                     # Connexion à la base PostgreSQL
├── data/                       # Données JSON extraites et historiques
├── .env                        # Clé API NVD et configuration DB
├── .gitignore
├── README.md
└── requirements.txt


---

## Installation

### 1. Cloner le projet

```bash
git clone [https://github.com/fatoumata256/cve_project.git](https://github.com/fatoumata256/cve_project.git)
cd cve_project

2. Créer un environnement virtuel

Bash

python -m venv .venv
source .venv/bin/activate    # Ou `.venv\Scripts\activate` sur Windows

3. Installer les dépendances

Bash

pip install -r requirements.txt

Configuration – Fichier .env

Créez un fichier .env à la racine du projet pour stocker vos informations de configuration locales. Ce fichier est ignoré par Git.

DB_HOST=localhost
DB_PORT=5432
DB_NAME=cve_db
DB_USER=postgres
DB_PASSWORD=admin12

NVD_API_KEY=4a35f378-39a5-418b-9ac1-50d3cd077174

Utilisation des scripts

Pour utiliser les différentes fonctionnalités du projet, exécutez les scripts suivants depuis le répertoire CVE_PROJECT/.

    Télécharger les fichiers CVE (JSON.gz)
    Bash

python src/downloader.py

Extraire les données CVE depuis les fichiers JSON
Bash

python src/extractor.py

Insérer les CVE dans PostgreSQL
Bash

python src/importer_cve.py

Récupérer l’historique d’une CVE via l’API
Bash

python src/importer_change_history.py CVE-2021-44228

Récupérer et insérer l’historique de plusieurs CVE
Bash

    python src/import_allchangement.py

Dépendances principales

    requests — Pour les appels à l’API NVD

    psycopg2 — Pour la connexion à PostgreSQL

    python-dotenv — Pour charger le fichier .env

    tqdm — Pour l’affichage de la progression

Licence

Ce projet est un travail académique. Son utilisation est libre à des fins pédagogiques.

Contact

Développé par Fatoumata Diallo GitHub : https://github.com/fatoumata256

