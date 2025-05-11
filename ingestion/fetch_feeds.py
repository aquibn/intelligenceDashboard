import os, gzip, json, requests
from config import NIST_FEED_URL, DATA_DIR

def fetch_nist_feed():
    os.makedirs(f"{DATA_DIR}/raw", exist_ok=True)
    os.makedirs(f"{DATA_DIR}/processed", exist_ok=True) 
    filename = f"{DATA_DIR}/raw/nist_cve.json.gz"
    r = requests.get(NIST_FEED_URL)
    with open(filename, 'wb') as f:
        f.write(r.content)
    with gzip.open(filename, 'rt', encoding='utf-8') as gz:
        data = json.load(gz)
    with open(f"{DATA_DIR}/processed/nist_cve.json", "w") as f:
        json.dump(data, f)
    print("[+] Fetched and extracted NIST feed.")

if __name__ == "__main__":
    fetch_nist_feed()