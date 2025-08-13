import json
from datetime import datetime
import re

# Load combined legal documents (gdpr + primary + secondary legislation) file
with open("combined_legal_documents.json", "r", encoding="utf-8") as f:
    all_documents = json.load(f)

# Filter only primary and secondary legislations, since GDPR do not have an enactment date
legislations = [
    doc for doc in all_documents
    if doc.get("category") in ["primary legislation", "secondary legislation"]
]

edges = []

# Parse date by removing the ordinal suffix (example: 3rd -> 3)
def parse_date(date_str):
    if not date_str:
        return None
    cleaned = re.sub(r'(\d{1,2})(st|nd|rd|th)', r'\1', date_str)
    try:
        return datetime.strptime(cleaned.strip(), "%d %B %Y")
    except ValueError:
        return None

# Create 'procedes'/'follows' relationships by comparing enactment dates
for i, doc1 in enumerate(legislations):
    date1 = parse_date(doc1.get("enactment_date", ""))
    if not date1:
        continue

    title1 = doc1.get("title", f"Unknown-{i}")
    date1_str = date1.strftime("%Y-%m-%d")

    for j, doc2 in enumerate(legislations):
        if i == j:
            continue

        date2 = parse_date(doc2.get("enactment_date", ""))
        if not date2:
            continue

        title2 = doc2.get("title", f"Unknown-{j}")
        date2_str = date2.strftime("%Y-%m-%d")

        edge_type = "precedes" if date1 < date2 else "follows"

        edges.append({
            "source": title1,
            "target": title2,
            "type": edge_type,
            "source_date": date1_str,
            "target_date": date2_str
        })

# Save all relationships in a JSON file
with open("temporal_relationships.json", "w", encoding="utf-8") as f:
    json.dump(edges, f, indent=4, ensure_ascii=False)

print(f"Saved {len(edges)} relationships to 'temporal_relationships.json'")
