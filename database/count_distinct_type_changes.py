# Prints most common 'change' types
# Used to find 'type' terms that affect end dates of legislations, used to build legislations timeline

import json
from collections import Counter

# Load legislation changes file
with open("/Users/apple/Desktop/uni/kings/project/database/legislation_changes_1700_2025_updated.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Count frequency of each 'type'
type_counts = Counter(entry.get("type") for entry in data if entry.get("type"))

# Sort by descending frequency
sorted_type_counts = dict(sorted(type_counts.items(), key=lambda x: x[1], reverse=True))

print(f"\n Total distinct types: {len(sorted_type_counts)}")

# Save all 'types' and respective counts in JSON file
with open("changes_distinct_types_with_counts.json", "w", encoding="utf-8") as out_file:
    json.dump(sorted_type_counts, out_file, indent=2)

print("Saved to 'changes_distinct_types_with_counts.json'")
