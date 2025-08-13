import json

# Load JSON file with linking terms and contexts
with open("legislation_with_linking_terms.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

# Collect valid titles in document
all_titles = [doc["title"] for doc in documents if doc.get("title") and isinstance(doc["title"], str)]

matches = []

# Iterate through document to match linking terms to titles
for doc in documents:
    if doc.get("category") not in ["primary legislation", "secondary legislation"]:
        continue

    source_title = doc.get("title", "Untitled Document")
    linking_terms = doc.get("linking_terms_found", [])

    for entry in linking_terms:
        context = entry.get("context", "")
        phrase = entry.get("phrase", "")

        for other_title in all_titles:
            if other_title and other_title != source_title and other_title in context:
                matches.append({
                    "source_title": source_title,
                    "linking_term": phrase,
                    "matched_title": other_title,
                    "context": context
                })

# Save in a JSON file
with open("matched_contexts.json", "w", encoding="utf-8") as f:
    json.dump(matches, f, indent=4, ensure_ascii=False)

print(f"Saved {len(matches)} matched contexts to 'matched_contexts.json'")
