import os
import requests
import gzip
import shutil
from datetime import datetime

def download_file(url, output_path):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        print(f" Fichier téléchargé : {output_path}")
    except Exception as e:
        print(f" Échec du téléchargement : {url} → {e}")

def decompress_file(gz_path):
    json_path = gz_path[:-3]  # Supprime .gz
    if os.path.exists(json_path):
        print(f" Déjà décompressé : {json_path}")
        return
    try:
        with gzip.open(gz_path, 'rb') as f_in:
            with open(json_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        print(f" Décompressé : {json_path}")
    except Exception as e:
        print(f" Erreur de décompression {gz_path} → {e}")

def main():
    print(" Début de l'exécution :", datetime.now())

    # Base URL pour JSON 2.0
    base_url = "https://nvd.nist.gov/feeds/json/cve/2.0/"
    current_year = datetime.now().year

    # Fichiers à télécharger : années + recent + modified
    filenames = [f"nvdcve-2.0-{year}.json.gz" for year in range(2010, current_year + 1)]
    filenames += ["nvdcve-2.0-recent.json.gz", "nvdcve-2.0-modified.json.gz"]

    os.makedirs("data", exist_ok=True)

    for fname in filenames:
        url = base_url + fname
        gz_path = os.path.join("data", fname)
        print(f" Téléchargement de {url} ...")
        download_file(url, gz_path)
        decompress_file(gz_path)

    print(" Terminé à :", datetime.now())

if __name__ == "__main__":
    main()
