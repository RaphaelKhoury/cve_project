# CVE Project - NVD Vulnerabilities

This project provides a solution for managing and analyzing **CVE** vulnerabilities from the **NVD**.  
It allows you to:  

- **Download** CVE files from the NVD (JSON.gz)  
- **Extract** all important data (description, CVSS, CWE, CPE, etc.)  
- **Insert** this data into a PostgreSQL database  
- **Track** historical changes of CVEs via the NVD API (`/cvehistory/2.0`)  

The change history is stored in PostgreSQL in the **`importer_change_history`** table.  

---

## 📂 Project Structure

```
CVE_PROJECT/
├── src/
│   ├── downloader.py              # Download JSON.gz files
│   ├── extractor.py               # Extract CVE data
│   ├── importer_cve.py            # Insert CVEs into PostgreSQL
│   ├── importer_change_history.py # Retrieve change history of a CVE list (API)
│   ├── import_allchangement.py    # Insert change history for multiple CVEs
│   ├── config.py                  # General settings (API key, DB)
│   └── db.py                      # PostgreSQL connection
├── data/                          # Extracted JSON data and history
├── .env                           # NVD API key and DB configuration
├── .gitignore
├── README.md
└── requirements.txt
```

---

## 🛠 Prerequisites

- **Python 3.10+**
- **PostgreSQL 14+** (or compatible version)
- **NVD API Key**  

---

## 📥 Installation

### 1- Clone the project

```bash
git clone https://github.com/fatoumata256/cve_project.git
cd cve_project
```

---

### 2- Install PostgreSQL

1. **Download and install PostgreSQL**  
   - Windows: https://www.postgresql.org/download/windows/

2. **Create the database**  
   ```bash
   psql -U postgres -c "CREATE DATABASE cve_db;"
   ```

---

### 3- Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/Mac
.venv\Scripts\activate         # Windows
```

---

### 4- Install Python dependencies

```bash
pip install -r requirements.txt
```

---

### 5- Configure the `.env` file

Create a `.env` file at the project root with your settings:

```
DB_HOST=localhost
DB_PORT=5432
DB_NAME=cve_db
DB_USER=postgres
DB_PASSWORD=admin12

NVD_API_KEY=4a35f378-39a5-418b-9ac1-50d3cd077174
```

---

## 🗃️ Database Setup
Option A — Use the provided schema.sql

    Download schema.sql from the repo (located in the src/ folder).

    Run: psql -U postgres -d cve_db -f src/schema.sql

Option B — Inline SQL (copy/paste)

    Copy the SQL block from schema.sql (same content). 


## 🚀 Using the scripts

**Download CVE files (JSON.gz)**  
```bash
python src/downloader.py
```

**Extract CVE data from JSON files**  
```bash
python src/extractor.py
```

**Insert CVEs into PostgreSQL**  
Modify importer_cve.py so to have the correct password for your DB.
```bash
python src/importer_cve.py
```

****optional, include changes to CVEs in the DB****

**Retrieve the history of a CVE via the API**  
(The CVE number is the one for which you want the changse)
```bash
python src/importer_change_history.py CVE-2021-44228
```

**Retrieve and insert history for multiple CVEs**  
```bash
python src/import_allchangement.py
```

Connect to db with : 
psql -U postgres -d cve_db

---
Sample requests


1.Check if a CVE is in the DB
SELECT * FROM cve WHERE cve_id = 'CVE-2024-25694';

2.Description for a given CVE
SELECT lang, description FROM cve_description WHERE cve_id = 'CVE-2024-25694'; 
3. List references for a CVE.
 SELECT r.url, r.source, r.tags FROM cve_reference cr JOIN reference r ON cr.reference_id = r.id WHERE cr.cve_id = 'CVE-2024-25694';

4. Show CVSS scrores for a CVE 
SELECT cve_id,version, base_score, base_severity, vector_string, attack_vector, attack_complexity, privileges_required, user_interaction, scope, confidentiality_impact, integrity_impact, availability_impact FROM cvss WHERE cve_id = 'CVE-2024-25694';
5. Show  CWE for a CVE 
SELECT cc.cve_id, cc.cwe_id FROM cve_cwe cc WHERE cc.cve_id = 'CVE-2024-25694';

6. Show CPE for a CVE
 SELECT c. vendor, c. product, c.version, c.criteria, c.vulnerable FROM cve_cpe_match cm JOIN cpe_match c ON cm.cpe_match_id = c.id WHERE cm.cve_id = 'CVE-2024-25694';
7. Show all changes (if the scripts for changes have been run )
SELECT cve_id, published, last_modified FROM cve ORDER BY last_modified DESC LIMIT 20;

8. List a CVE with its vendors 
 SELECT cm.cve_id, c.vendor, c.product FROM cve_cpe_match cm JOIN cpe_match c ON cm.cpe_match_id = c.id WHERE cm.cve_id = 'CVE-2021-44228' ORDER BY c.vendor, c.product;

9. List all changes for a CVE. 
 SELECT * FROM cve_change_history WHERE cve_id = 'CVE-2021-44228' ORDER BY change_date DESC;
10. Find all CVEs modified during a given time period
 SELECT DISTINCT cve_id FROM cve_change_history WHERE change_date BETWEEN '2025-01- 01' AND '2025-01-31';

11. Status of a CVE from 2010 with the organisation that submitted it. 
 SELECT cve_id, source_identifier, vuln_status FROM cve WHERE cve_id LIKE 'CVE-2010-%' AND vuln_status IS NOT NULL ORDER BY cve_id LIMIT 20;
12. Count the number of changs by type 
 SELECT action, COUNT (*) FROM cve_change_history GROUP BY action.

---

## 📦 Main dependencies

- `requests` — API calls to NVD  
- `psycopg2` — PostgreSQL connection  
- `python-dotenv` — Load environment variables  
- `tqdm` — Progress bar  

---

## 📜 License

This project is an academic work. Free to use for educational purposes.

---

## 📬 Contact

**Developed by:** Fatoumata Diallo  
**GitHub:** https://github.com/fatoumata256
