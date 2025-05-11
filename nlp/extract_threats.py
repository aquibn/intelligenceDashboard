import json
import spacy
from pathlib import Path

nlp = spacy.load("en_core_web_sm")

def extract_entities(description):
    doc = nlp(description)
    return [ent.text for ent in doc.ents if ent.label_ in ("ORG", "GPE", "PRODUCT", "DATE")]

def process_nist_cve():
    with open("data/processed/nist_cve.json") as f:
        cve_data = json.load(f)["CVE_Items"]
    processed = []
    for item in cve_data:
        desc = item["cve"]["description"]["description_data"][0]["value"]
        entities = extract_entities(desc)
        processed.append({
            "cve_id": item["cve"]["CVE_data_meta"]["ID"],
            "published": item["publishedDate"],
            "entities": entities,
            "description": desc
        })
    Path("data/processed").mkdir(parents=True, exist_ok=True)
    with open("data/processed/parsed_threats.json", "w") as f:
        json.dump(processed, f)
    print("[+] Extracted entities from CVE descriptions.")

if __name__ == "__main__":
    process_nist_cve()