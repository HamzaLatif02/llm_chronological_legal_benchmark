import json
from datetime import datetime
from dateutil import parser

# Load combined_legal_documents and legislation_changes files
with open("/Users/apple/Desktop/uni/kings/project/database/combined_legal_documents.json", "r", encoding="utf-8") as f:
    combined_documents = json.load(f)

with open("/Users/apple/Desktop/uni/kings/project/database/legislation_changes_1700_2025_updated.json", "r", encoding="utf-8") as f:
    legislation_changes = json.load(f)

# Define end-date affecting 'type' terms
end_date_types = {
    "repealed", "revoked", "expired", "ceased to have effect", "excluded",
    "omitted", "deleted", "replaced", "disapplied", "substituted"
}

# Build a lookup from affected_title to list of entry_updated dates
title_to_updated_dates = {}
for change in legislation_changes:
    change_type = change.get("type", "").strip().lower()
    if change_type not in end_date_types:
        continue

    title = change.get("affected_title", "").strip()
    updated = change.get("entry_updated")
    if title and updated:
        title_to_updated_dates.setdefault(title, []).append(updated)

# Convert enactment date to ISO format, to ensure all dates are in same format
def parse_enactment_date(text):
    try:
        return parser.parse(text).date().isoformat()
    except:
        return None

# Build timeline entries
today_str = datetime.today().date().isoformat()
timeline = []
for doc in combined_documents:
    category = doc.get("category", "").lower()
    if category not in {"primary legislation", "secondary legislation"}:
        continue

    # Skip if enactment_date is missing or invalid
    start_date_raw = doc.get("enactment_date", "")
    start_date = parse_enactment_date(start_date_raw)
    if not start_date:
        continue

    title = doc.get("title")
    updated_dates = title_to_updated_dates.get(title, [])
    if updated_dates:
        end_date_iso = max(updated_dates)
        end_date = parser.parse(end_date_iso).date().isoformat()
    else:
        end_date = today_str  # Use today's date in case no end date is found, meaning legislation is ongoing

    timeline.append({
        "title": title,
        "start_date": start_date,
        "end_date": end_date
    })

# Save legislations timeline to a JSON file
with open("legislation_timeline.json", "w", encoding="utf-8") as f:
    json.dump(timeline, f, indent=2, ensure_ascii=False)

print(f"Created timeline for {len(timeline)} primary/secondary legislations.")
