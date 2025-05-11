import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
import pandas as pd

def cluster_threats():
    with open("data/processed/parsed_threats.json") as f:
        threats = json.load(f)

    descriptions = [item["description"] for item in threats]
    vectorizer = TfidfVectorizer(max_features=1000)
    X = vectorizer.fit_transform(descriptions)
    kmeans = KMeans(n_clusters=5, random_state=0).fit(X)

    for i, item in enumerate(threats):
        item["cluster"] = int(kmeans.labels_[i])

    with open("data/processed/clustered_threats.json", "w") as f:
        json.dump(threats, f)

    print("[+] Clustered threats using KMeans.")

if __name__ == "__main__":
    cluster_threats()