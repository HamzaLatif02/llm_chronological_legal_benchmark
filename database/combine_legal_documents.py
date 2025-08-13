import json

# File paths
gdpr_path = '/Users/apple/Desktop/uni/kings/project/database/gdpr_articles.json'
primary_path = '/Users/apple/Desktop/uni/kings/project/database/uk_primary_legislation.json'
secondary_path = '/Users/apple/Desktop/uni/kings/project/database/uk_secondary_legislation.json'
output_path = '/Users/apple/Desktop/uni/kings/project/database/combined_legal_documents.json'

combined_data = []

# Load GDPR file
with open(gdpr_path, 'r', encoding='utf-8') as f:
    gdpr_json = json.load(f)

# Convert GDPR file to list and add category 'GDPR'
if isinstance(gdpr_json, dict):
    for key, value in gdpr_json.items():
        if isinstance(value, dict):
            value['category'] = 'gdpr'
            combined_data.append(value)
else:
    for item in gdpr_json:
        item['category'] = 'gdpr'
        combined_data.append(item)

# Load primary legislations
try:
    with open(primary_path, 'r', encoding='utf-8') as f:
        primary_json = json.load(f)
        if isinstance(primary_json, dict):
            primary_json['category'] = 'primary legislation'
            combined_data.append(primary_json)
        elif isinstance(primary_json, list):
            for item in primary_json:
                item['category'] = 'primary legislation'
                combined_data.append(item)
except FileNotFoundError:
    print("Primary legislation file not found.")

# Load secondary legislations
with open(secondary_path, 'r', encoding='utf-8') as f:
    secondary_json = json.load(f)
    for item in secondary_json:
        item['category'] = 'secondary legislation'
        combined_data.append(item)

# Save combined legislations file
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(combined_data, f, indent=4, ensure_ascii=False)

print(f"Saved {len(combined_data)} combined documents to '{output_path}'.")
