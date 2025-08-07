#  CVE Project - NVD Vulnerabilities 

Ce projet permet de :

1. Télécharger les fichiers CVE depuis le NVD (JSON)
2. Extraire toutes les données (description, CVSS, CWE, CPE, etc.)
3. Insérer les données dans la base PostgreSQL
4. Suivre les changements historiques des CVE via l’API NVD (/cvehistory/2.0)

Nous utilisons l'API Officielle de la NVD pour récupérer l'historique des changements d'une CVE. Les données sont insérées dans la Base de données PostGreSql "importer_change_history"

##  Structure

CVE_PROJECT/
├── src/
│ ├── downloader.py # Téléchargement des fichiers JSON.gz
│ ├── extractor.py # Extraction des données CVE depuis les fichiers
│ ├── importer_cve.py # Insertion des CVE dans PostgreSQL
│ ├── importer_change_history.py # Récupération de l’historique d’Une liste de CVE (API)
│ ├── import_allchangement.py # Insertion de l’historique de changements plusieurs CVEs
│ ├── config.py # Paramètres généraux (clé API, DB)
│ └── db.py # Connexion à la base PostgreSQL
├── data/ # Données JSON extraites et historiques
├── .env # Clé API NVD et config DB
├── .gitignore
├── README.md
└── requirements.txt



##  Installation

# 1. Cloner le projet

```bash
git clone https://github.com/fatoumata256/cve_project.git
cd cve_project

# 2. Créer un environnement virtuel

```bash
python -m venv .venv
source .venv/bin/activate  # ou .venv\Scripts\activate sur Windows
```

# 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

---

# Configuration – fichier `.env`

Crée un fichier `.env` à la racine du projet pour y stocker ta configuration locale :

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cve_db
DB_USER=postgres
DB_PASSWORD=admin12

NVD_API_KEY=*
```

Ce fichier est ignoré par Git 

---

# Utilisation des scripts

# Télécharger les fichiers CVE (JSON.gz)

```bash
python src/downloader.py
```

# Extraire les données CVE depuis les fichiers JSON

```bash
python src/extractor.py
```

# Insérer les CVE dans PostgreSQL

```bash
python src/importer_cve.py
```

# Récupérer l’historique d’une CVE via l’API

```bash
python src/importer_change_history.py CVE-2021-44228
```

# Récupérer et insérer l’historique de plusieurs CVE

```bash
python src/import_allchangement.py


---

#  Dépendances principales

- 'requests' — pour les appels à l’API NVD
- 'psycopg2' — pour la connexion PostgreSQL
- 'python-dotenv' — pour charger le fichier '.env'
- 'tqdm' — pour l’affichage de la progression

---

#  Licence

Projet académique  
Utilisation libre à des fins pédagogiques.

---

# Contact

Développé par *Fatoumata Diallo*  
GitHub : [https://github.com/fatoumata256](https://github.com/fatoumata256)

