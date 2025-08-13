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

**Retrieve the history of a CVE via the API**  
(The CVE number is the one for which you want the changse)
```bash
python src/importer_change_history.py CVE-2021-44228
```

**Retrieve and insert history for multiple CVEs**  
```bash
python src/import_allchangement.py
```

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
