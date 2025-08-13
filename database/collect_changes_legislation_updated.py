import requests
import xml.etree.ElementTree as ET
import json
import time

# Define XML namespaces for Atom feeds and legislation changes
ns = {
    'atom': 'http://www.w3.org/2005/Atom',
    'ukm': 'http://www.legislation.gov.uk/namespaces/metadata'
}

# Parse a single page of results
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

all_entries = []

# Fetch data from all years and pages
# Each page has 50 entries, this value can be chnaged by chnaging the value 50 in 'results-count=50&sort' in the url below, although it does not affect performance
for year in range(1700, 2026):
    print(f"\n Year {year}")
    page = 1
    while True:
        url = f"https://www.legislation.gov.uk/changes/affected/all/{year}/data.feed?results-count=50&sort=affected-year-number&page={page}"
        try:
            print(f"   Fetching page {page}...", end='')
            response = requests.get(url, timeout=20)
            if response.status_code != 200:
                print(f"  HTTP {response.status_code}")
                break

            entries = extract_entries_from_feed(response.content)
            if not entries:
                print("  No entries.")
                break

            print(f"  {len(entries)} entries")
            all_entries.extend(entries)
            page += 1
            time.sleep(1)

        except Exception as e:
            print(f"  Error on page {page}: {e}")
            break

# Save legislation changes in a JSON file
output_file = "legislation_changes_1700_2025_complete.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(all_entries, f, indent=2, ensure_ascii=False)

print(f"\n Done! Saved {len(all_entries)} entries to '{output_file}'")
