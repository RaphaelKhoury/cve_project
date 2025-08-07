import requests
import psycopg2
import os
from datetime import datetime
from tqdm import tqdm

#  1. Configuration 

DB_CONFIG = {
    "dbname": "cve_db",
    "user": "postgres",
    "password": "admin12",
    "host": "localhost",
    "port": "5432"
}

#  CLE API ET URL
NVD_API_KEY = os.getenv("NVD_API_KEY", "4a35f378-39a5-418b-9ac1-50d3cd077174")
NVD_HISTORY_API_URL = "https://services.nvd.nist.gov/rest/json/cvehistory/2.0"

#  2. Connexion Base de Données 

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f" Erreur connexion DB : {e}")
        return None

# 3. Fonction principale de récupération d'historique 

def get_cve_history(cve_id):
    headers = {"apiKey": NVD_API_KEY}
    params = {"cveId": cve_id}
    try:
        response = requests.get(NVD_HISTORY_API_URL, headers=headers, params=params, timeout=60)
        response.raise_for_status()
        data = response.json()
        return data.get("cveChanges", [])
    except requests.RequestException as e:
        print(f" API erreur pour {cve_id} : {e}")
        return []

# 4. Insertion des changements dans PostgreSQL 

def insert_change_history(cursor, cve_id, event_name, change_id, created, source_identifier, action, type_, old_value, new_value):
    sql = """
    INSERT INTO cve_change_history (
        cve_id, event_name, change_id, change_date, source_identifier,
        action, type, old_value, new_value
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
    """
    cursor.execute(sql, (cve_id, event_name, change_id, created, source_identifier, action, type_, old_value, new_value))

# 5. Traitement complet d'une CVE 

def process_cve_history(cursor, cve_id):
    print(f"\n CVE : {cve_id}")
    changes = get_cve_history(cve_id)
    print(f" {len(changes)} changements récupérés")
    
    for change in changes:
        chg = change.get("change", {})
        event_name = chg.get("eventName")
        change_id = chg.get("cveChangeId")
        created = chg.get("created")
        source_identifier = chg.get("sourceIdentifier")
        details = chg.get("details", [])

        for detail in details:
            action = detail.get("action")
            type_ = detail.get("type")
            old_value = detail.get("oldValue")
            new_value = detail.get("newValue")

            insert_change_history(cursor, cve_id, event_name, change_id, created, source_identifier, action, type_, old_value, new_value)

# 6. Exécution principale 

def main():
    conn = get_db_connection()
    if not conn:
        return
    
    # 6. liste des CVE (à adapter en fonction des changements des CVE qu'on veut voir dans la BD)
    
    cve_list = [
        "CVE-2015-7547",
        "CVE-2011-2477",
        "CVE-2017-0144",
        "CVE-2020-18123",
        "CVE-2022-22965",
        "CVE-2021-44228",
        "CVE-2019-0708",
        "CVE-2023-23397",
        "CVE-2025-8433",
        "CVE-2018-0171"
    ]

    try:
        with conn.cursor() as cursor:
            for cve_id in tqdm(cve_list, desc=" CVEs en cours"):
                process_cve_history(cursor, cve_id)
            conn.commit()
            print("\n Tous les changements enregistrés en base")
    except Exception as e:
        print(f" Erreur générale : {e}")
        conn.rollback()
    finally:
        conn.close()
        print("[*] Connexion fermée")

if __name__ == "__main__":
    main()