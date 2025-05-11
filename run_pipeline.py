from ingestion.fetch_feeds import fetch_nist_feed
from nlp.extract_threats import process_nist_cve
from ml.cluster_threats import cluster_threats
from db.save_to_db import save_to_db

if __name__ == "__main__":
    fetch_nist_feed()
    process_nist_cve()
    cluster_threats()
    save_to_db()
    print("[✓] End-to-end pipeline completed.")