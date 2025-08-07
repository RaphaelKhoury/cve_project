import json
import psycopg2
from psycopg2.extras import execute_values

DATA_FILE = "data/cve_extracted.json"

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        database="cve_db",
        user="postgres",
        password="admin12"
    )

def load_data(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def insert_cve(conn, cve):
    with conn.cursor() as cur:
        cur.execute("""
            INSERT INTO cve (cve_id, source_identifier, published, last_modified, vuln_status, cve_tags)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (cve_id) DO NOTHING;
        """, (
            cve["cve_id"],
            cve.get("source_identifier"),
            cve.get("published"),
            cve.get("last_modified"),
            cve.get("vuln_status"),
            cve.get("cve_tags", [])
        ))

def insert_descriptions(conn, cve_id, descriptions):
    with conn.cursor() as cur:
        execute_values(cur, """
            INSERT INTO cve_description (cve_id, lang, description)
            VALUES %s
            ON CONFLICT DO NOTHING;
        """, [(cve_id, d.get("lang"), d.get("value")) for d in descriptions])

def insert_references(conn, cve_id, references):
    with conn.cursor() as cur:
        for ref in references:
            cur.execute("""
                INSERT INTO reference (url, source, tags)
                VALUES (%s, %s, %s)
                ON CONFLICT (url) DO UPDATE SET tags = EXCLUDED.tags RETURNING id;
            """, (
                ref.get("url"),
                ref.get("source"),
                ref.get("tags", [])
            ))
            reference_id = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO cve_reference (cve_id, reference_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
            """, (cve_id, reference_id))

def insert_cvss(conn, cve_id, cvss_list):
    with conn.cursor() as cur:
        for cvss in cvss_list:
            version = cvss.get("version")
            if not version:
                continue

            cur.execute("DELETE FROM cvss WHERE cve_id = %s AND version = %s;", (cve_id, version))

            cur.execute("""
                INSERT INTO cvss (
                    cve_id, version, base_score, base_severity, vector_string,
                    exploitability_score, impact_score, attack_vector,
                    attack_complexity, privileges_required, user_interaction,
                    scope, confidentiality_impact, integrity_impact,
                    availability_impact, access_vector, access_complexity, authentication
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                cve_id,
                version,
                cvss.get("baseScore"),
                cvss.get("baseSeverity"),
                cvss.get("vectorString"),
                cvss.get("exploitabilityScore"),
                cvss.get("impactScore"),
                cvss.get("attackVector"),
                cvss.get("attackComplexity"),
                cvss.get("privilegesRequired"),
                cvss.get("userInteraction"),
                cvss.get("scope"),
                cvss.get("confidentialityImpact"),
                cvss.get("integrityImpact"),
                cvss.get("availabilityImpact"),
                cvss.get("accessVector"),
                cvss.get("accessComplexity"),
                cvss.get("authentication")
            ))

def insert_weaknesses(conn, cve_id, weaknesses):
    with conn.cursor() as cur:
        for w in weaknesses:
            for desc in w.get("description", []):
                cur.execute("""
                    INSERT INTO cve_weakness (cve_id, source, type, description)
                    VALUES (%s, %s, %s, %s)
                    ON CONFLICT DO NOTHING;
                """, (
                    cve_id,
                    w.get("source"),
                    w.get("type"),
                    desc.get("value")
                ))

def insert_cwe(conn, cve_id, cwe_list):
    with conn.cursor() as cur:
        for cwe in cwe_list:
            cur.execute("""
                INSERT INTO cwe (cwe_id) VALUES (%s)
                ON CONFLICT (cwe_id) DO NOTHING;
            """, (cwe,))
            cur.execute("""
                INSERT INTO cve_cwe (cve_id, cwe_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
            """, (cve_id, cwe))

def insert_cpe_match(conn, cve_id, cpe_matches):
    with conn.cursor() as cur:
        for cpe in cpe_matches:
            cur.execute("""
                INSERT INTO cpe_match (criteria, match_criteria_id, vulnerable, vendor, product, version)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING id;
            """, (
                cpe.get("criteria"),
                cpe.get("matchCriteriaId"),
                cpe.get("vulnerable"),
                cpe.get("vendor"),
                cpe.get("product"),
                cpe.get("version")
            ))
            cpe_id = cur.fetchone()[0]
            cur.execute("""
                INSERT INTO cve_cpe_match (cve_id, cpe_match_id)
                VALUES (%s, %s)
                ON CONFLICT DO NOTHING;
            """, (cve_id, cpe_id))

def main():
    print(" Début de l'importation...")
    cves = load_data(DATA_FILE)
    conn = get_connection()
    conn.autocommit = True

    for cve in cves:
        try:
            insert_cve(conn, cve)
            insert_descriptions(conn, cve["cve_id"], cve.get("descriptions", []))
            insert_references(conn, cve["cve_id"], cve.get("references", []))
            insert_cvss(conn, cve["cve_id"], cve.get("cvss_metrics", []))
            insert_weaknesses(conn, cve["cve_id"], cve.get("weaknesses", []))
            insert_cwe(conn, cve["cve_id"], cve.get("cwe", []))
            insert_cpe_match(conn, cve["cve_id"], cve.get("cpe_matches", []))
            print(f" {cve['cve_id']} inséré.")
        except Exception as e:
            print(f" Erreur pour {cve['cve_id']} → {e}")

    conn.close()
    print("✅ Importation terminée.")

if __name__ == "__main__":
    main()
