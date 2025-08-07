import json
import os
from pathlib import Path

# Répertoire contenant les fichiers JSON 2.0
INPUT_DIR = "data"
OUTPUT_FILE = "data/cve_extracted.json"


def extract_cve_data(raw):
    """
    Extraction des données CVE depuis un fichier JSON 2.0 du NVD.
    """
    results = []

    for entry in raw.get("vulnerabilities", []):
        item = entry.get("cve", {})

        cve_id = item.get("id")
        assigner = item.get("sourceIdentifier")
        published = item.get("published")
        last_modified = item.get("lastModified")
        vuln_status = item.get("vulnStatus")
        cve_tags = item.get("cveMetadata", {}).get("tags", [])

        # Descriptions
        descriptions = item.get("descriptions", [])

        # Références
        references = []
        for ref in item.get("references", []):
            references.append({
                "url": ref.get("url"),
                "source": ref.get("source"),
                "tags": ref.get("tags", [])
            })

        # Weaknesses (CWE)
        cwe_list = []
        weaknesses = item.get("weaknesses", [])
        for weakness in weaknesses:
            for desc in weakness.get("description", []):
                val = desc.get("value")
                if val and "CWE" in val:
                    cwe_list.append(val)

        # Configurations (CPE)
        cpe_matches = []
        for config in item.get("configurations", []):
            for node in config.get("nodes", []):
                for match in node.get("cpeMatch", []):
                    cpe_uri = match.get("criteria")
                    if not cpe_uri:
                        continue
                    parts = cpe_uri.split(":")
                    vendor = parts[3] if len(parts) > 3 else None
                    product = parts[4] if len(parts) > 4 else None
                    version = parts[5] if len(parts) > 5 else None

                    cpe_matches.append({
                        "criteria": cpe_uri,
                        "vulnerable": match.get("vulnerable", False),
                        "vendor": vendor,
                        "product": product,
                        "version": version
                    })

        # CVSS metrics
        cvss_metrics = []
        for metric_version in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
            for metric in item.get("metrics", {}).get(metric_version, []):
                data = metric.get("cvssData", {})
                cvss_entry = {
                    "version": data.get("version"),
                    "vectorString": data.get("vectorString"),
                    "baseScore": data.get("baseScore"),
                    "baseSeverity": data.get("baseSeverity"),
                    "exploitabilityScore": metric.get("exploitabilityScore"),
                    "impactScore": metric.get("impactScore"),
                }
                # Ajout des champs selon les versions

                if "attackVector" in data:
                    cvss_entry.update({
                        "attackVector": data.get("attackVector"),
                        "attackComplexity": data.get("attackComplexity"),
                        "privilegesRequired": data.get("privilegesRequired"),
                        "userInteraction": data.get("userInteraction"),
                        "scope": data.get("scope"),
                        "confidentialityImpact": data.get("confidentialityImpact"),
                        "integrityImpact": data.get("integrityImpact"),
                        "availabilityImpact": data.get("availabilityImpact"),
                    })
                elif "accessVector" in data:
                    cvss_entry.update({
                        "accessVector": data.get("accessVector"),
                        "accessComplexity": data.get("accessComplexity"),
                        "authentication": data.get("authentication"),
                        "confidentialityImpact": data.get("confidentialityImpact"),
                        "integrityImpact": data.get("integrityImpact"),
                        "availabilityImpact": data.get("availabilityImpact"),
                    })

                cvss_metrics.append(cvss_entry)

        results.append({
            "cve_id": cve_id,
            "source_identifier": assigner,
            "published": published,
            "last_modified": last_modified,
            "vuln_status": vuln_status,
            "cve_tags": cve_tags,
            "descriptions": descriptions,
            "references": references,
            "weaknesses": weaknesses,
            "cwe": cwe_list,
            "cpe_matches": cpe_matches,
            "cvss_metrics": cvss_metrics
        })

    return results


def main():
    # Recherche tous les fichiers JSON 2.0
    input_files = list(Path(INPUT_DIR).glob("nvdcve-2.0-*.json"))

    if not input_files:
        print(f" Aucun fichier JSON 2.0 trouvé dans le répertoire : {INPUT_DIR}")
        return

    all_extracted_cves = []

    for file_path in input_files:
        print(f" Traitement du fichier : {file_path}")
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            extracted = extract_cve_data(data)
            all_extracted_cves.extend(extracted)
        except Exception as e:
            print(f" Erreur lors du traitement du fichier {file_path} : {e}")
            continue

    if not all_extracted_cves:
        print(" Aucune donnée CVE n'a été extraite.")
        return

    Path(OUTPUT_FILE).parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_extracted_cves, f, indent=2)

    print(f"\n Extraction terminée : {len(all_extracted_cves)} CVEs extraites et sauvegardées dans {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
