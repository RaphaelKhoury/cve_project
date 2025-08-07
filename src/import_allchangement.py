import requests
import psycopg2
import os
from datetime import datetime
from tqdm import tqdm

# Ce fichier concerne l'import sur les changements des CVE Depuis 2010 

# 1. Configuration 
DB_CONFIG = {
    "dbname": "cve_db",
    "user": "postgres",
    "password": "admin12",
    "host": "localhost",
    "port": "5432"
}

NVD_API_KEY = os.getenv("NVD_API_KEY", "4a35f378-39a5-418b-9ac1-50d3cd077174")
NVD_HISTORY_API_URL = "https://services.nvd.nist.gov/rest/json/cvehistory/2.0"

# 2. Connexion Base de Données 

def get_db_connection():
    try:
        return psycopg2.connect(**DB_CONFIG)
    except Exception as e:
        print(f" Erreur connexion DB : {e}")
        return None

# 3. Récupération de toutes les CVE à partir de 2010

def get_cve_list_from_2010(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT cve_id FROM cve
            WHERE cve_id >= 'CVE-2010-0001'
            ORDER BY cve_id;
        """)
        return [row[0] for row in cursor.fetchall()]

# 4. Récupération de l’historique d’une CVE via API 

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

# 5. Insertion dans la base 

def insert_change_history(cursor, cve_id, event_name, change_id, created, source_identifier, action, type_, old_value, new_value):
    sql = """
    INSERT INTO cve_change_history (
        cve_id, event_name, change_id, change_date, source_identifier,
        action, type, old_value, new_value
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT DO NOTHING;
    """
    cursor.execute(sql, (cve_id, event_name, change_id, created, source_identifier, action, type_, old_value, new_value))

#  6. Traitement d'une CVE 

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

#  7. Main 
def main():
    conn = get_db_connection()
    if not conn:
        return

    try:
        cve_list = get_cve_list_from_2010(conn)
        print(f"\n {len(cve_list)} CVEs à traiter depuis 2020...")

        with conn.cursor() as cursor:
            for cve_id in tqdm(cve_list, desc=" Traitement des CVEs"):
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
