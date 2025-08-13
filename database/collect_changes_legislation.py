# The code below only collects the first 50 entries per year, as the url format used is incorrect.
# Use the updated code, named 'colelct_changes_legislation_updated.py', for all entries.

import requests
import xml.etree.ElementTree as ET
import json
import time

# Define XML namespaces for Atom feeds and legislation changes
ns = {
    'atom': 'http://www.w3.org/2005/Atom',
    'ukm': 'http://www.legislation.gov.uk/namespaces/metadata'
}

# Parse entries for a single year's feed
def extract_entries_from_feed(xml_content):
    root = ET.fromstring(xml_content)
    entries = []
    for entry in root.findall('atom:entry', ns):
        content = entry.find('atom:content', ns)
        if content is None:
            continue

        effect = content.find('ukm:Effect', ns)
        if effect is None:
            continue

        entries.append({
            "effect_id": effect.attrib.get("EffectId"),
            "type": effect.attrib.get("Type"),
            "modified": effect.attrib.get("Modified"),
            "affected_uri": effect.attrib.get("AffectedURI"),
            "affecting_uri": effect.attrib.get("AffectingURI"),
            "affected_number": effect.attrib.get("AffectedNumber"),
            "affecting_number": effect.attrib.get("AffectingNumber"),
            "affected_year": effect.attrib.get("AffectedYear"),
            "affecting_year": effect.attrib.get("AffectingYear"),
            "affected_class": effect.attrib.get("AffectedClass"),
            "affecting_class": effect.attrib.get("AffectingClass"),
            "affected_title": effect.findtext("ukm:AffectedTitle", default="", namespaces=ns),
            "affecting_title": effect.findtext("ukm:AffectingTitle", default="", namespaces=ns),
            "entry_title": entry.findtext("atom:title", default="", namespaces=ns),
            "entry_updated": entry.findtext("atom:updated", default="", namespaces=ns),
            "entry_id": entry.findtext("atom:id", default="", namespaces=ns)
        })

    return entries

# Main loop through all years (1700 to 2025)
# Only works for first page of feed per year, so maximum 50 entries per year are collected, because the url below is incorrect.
all_entries = []
for year in range(1700, 2026):
    url = f"https://www.legislation.gov.uk/changes/affected/all/{year}/data.feed"
    try:
        print(f"Fetching year {year}...")
        response = requests.get(url, timeout=20)
        if response.status_code == 200:
            entries = extract_entries_from_feed(response.content)
            print(f"Year {year}: {len(entries)} entries")
            all_entries.extend(entries)
        else:
            print(f"Year {year}: HTTP {response.status_code}")
    except Exception as e:
        print(f"Year {year} failed: {e}")
    time.sleep(1)

# Save legislation changes in a JSON file
with open("legislation_changes_1700_2025.json", "w", encoding="utf-8") as f:
    json.dump(all_entries, f, indent=2, ensure_ascii=False)

print(f"\n Done! Saved {len(all_entries)} entries to 'legislation_changes_1700_2025.json'")
