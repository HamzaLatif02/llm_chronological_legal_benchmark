import json

# Define all linking terms
LINKING_TERMS = {
    "amends": ["amends", "modifies", "alters", "updates"],
    "repeals": ["repeals", "revokes", "nullifies", "removes"],
    "references": [
        "subject to", "in accordance with", "pursuant to",
        "under the provisions of", "as defined in", "within the meaning of",
        "by virtue of", "as amended by"
    ],
    "replaces": ["replaces", "substitutes", "supersedes"]
}

# Flatten list
ALL_TERMS = [(cat, phrase) for cat, phrases in LINKING_TERMS.items() for phrase in phrases]

# Load combined_legal_documents file
with open("combined_legal_documents.json", "r", encoding="utf-8") as f:
    documents = json.load(f)

# Extract context window around the linking term found, 10 words before and 9 words after the linking term (total of 20 words)
def extract_context(text, phrase, window=20):
    words = text.split()
    contexts = []
    phrase_lower = phrase.lower()

    for i, word in enumerate(words):
        if phrase_lower in word:
            start = max(i - window, 0)
            end = min(i + window + 1, len(words))
            context = ' '.join(words[start:end])
            contexts.append(context)
    return contexts

# Find linking terms for each legislation
for doc in documents:
    if doc.get("category") not in ["primary legislation", "secondary legislation"]:
        continue

    full_text = doc.get("full_text", "").lower()
    found_terms = []

    for category, phrase in ALL_TERMS:
        if phrase in full_text:
            contexts = extract_context(full_text, phrase)
            for context in contexts:
                found_terms.append({
                    "category": category,
                    "phrase": phrase,
                    "context": context
                })

    if found_terms:
        doc["linking_terms_found"] = found_terms

# Save all legislation with linking terms in a JSON file
with open("legislation_with_linking_terms.json", "w", encoding="utf-8") as f:
    json.dump(documents, f, indent=4, ensure_ascii=False)

print("Linking terms and context extracted successfully.")
