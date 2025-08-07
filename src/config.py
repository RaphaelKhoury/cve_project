# URL fichiers .json.gz du NVD (format 2.0)
NVD_FEED_BASE_URL = "https://nvd.nist.gov/feeds/json/cve/2.0/"

# PostgreSQL config
DB_CONFIG = {
    "host": "localhost",
    "database": "cve_db",
    "user": "cv_user",
    "password": "admin12",
    "port": 5432  
}

# Dossier local pour stocker les fichiers JSON.gz et les extraits JSON
DOWNLOAD_DIR = "./data"

#  CLE API 
NVD_API_KEY ="4a35f378-39a5-418b-9ac1-50d3cd077174"

