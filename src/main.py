import os
import gzip
import shutil
from subprocess import run
from extractor import main as extract_cve_data
from importer_cve import main as import_cve_data
from importer_change_history import main as import_change_history

def download_all():
    print(" Téléchargement des fichiers JSON.gz depuis NVD (format 2.0)...")
    run(["python", "downloader.py"])

def decompress_all():
    print(" Décompression des fichiers .gz...")
    for file in os.listdir("data"):
        if file.endswith(".gz"):
            gz_path = os.path.join("data", file)
            json_path = gz_path[:-3]  # supprime le .gz
            print(f"➤ Décompression : {gz_path}")
            with gzip.open(gz_path, 'rb') as f_in:
                with open(json_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

def main():
    print(" Démarrage de l'extraction de CVE complète (support JSON 2.0)...\n")

    # 1. Téléchargement des fichiers JSON compressés depuis NVD
    download_all()

    # 2. Décompression des fichiers .gz
    decompress_all()

    # 3. Extraction des données depuis les fichiers JSON 2.0 vers cve_extracted.json
    print("\n Extraction des données CVE...")
    extract_cve_data()

    # 4. Import des données dans la base de données PostgreSQL
    print("\n Importation des données CVE dans la base PostgreSQL...")
    import_cve_data()

    # 5. Import de l'historique des changements via l'API
    print("\n Importation de l'historique des changements (via API)...")
    import_change_history()

    print("\n Terminée avec succès.")

if __name__ == "__main__":
    main()
