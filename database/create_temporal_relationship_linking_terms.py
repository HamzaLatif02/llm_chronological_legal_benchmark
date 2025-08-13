import json
import re

# Load input JSON file
with open("matched_contexts_with_title.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Function to extract a 4-digit year from a title
def extract_year(title):
    match = re.search(r"\b(18|19|20)\d{2}\b", title)
    return int(match.group()) if match else None

# Prepare relationship entries
relationships = []
for item in data:
    source_title = item.get("source_title")
    target_title = item.get("matched_title")
    linking_term = item.get("linking_term")

    if source_title and target_title and linking_term:
        relationship_entry = {
            "source": source_title,
            "target": target_title,
            "relationship": linking_term,
            "source_year": extract_year(source_title),
            "target_year": extract_year(target_title),
        }
        relationships.append(relationship_entry)

# Save output to JSON
with open("temporal_relationships_linking_terms.json", "w", encoding="utf-8") as f:
    json.dump(relationships, f, indent=2)

print(f"Created {len(relationships)} temporal relationships.")
