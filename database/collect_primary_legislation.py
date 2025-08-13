import os
import time
import json
import requests
import xml.etree.ElementTree as ET

# Define XML namespaces for Atom feeds and legislations
ns_atom = {'atom': 'http://www.w3.org/2005/Atom'}
ns_leg = {'leg': 'http://www.legislation.gov.uk/namespaces/legislation'}

# List of all UK primary legislation types, except 'ukpga' as it was exctracted separately
legislation_types = [
    "ukla", "ukppa", "asp", "asc", "anaw", "mwa",
    "ukcm", "nia", "aosp", "aep", "aip", "apgb",
    "gbla", "nisi", "mnia", "apni"
]

# Recursive text extractor
def extract_text_recursive(elem):
    texts = []
    if elem.text:
        texts.append(elem.text.strip())
    for child in elem:
        texts.append(extract_text_recursive(child))
        if child.tail:
            texts.append(child.tail.strip())
    return ' '.join(filter(None, texts))

all_acts = []

# Loop through all legislation types
for leg_type in legislation_types:
    print(f"\n Checking legislation type: {leg_type}")
    master_feed_url = f"https://www.legislation.gov.uk/{leg_type}/data.feed"
    
    try:
        master_response = requests.get(master_feed_url)
        if master_response.status_code != 200:
            print(f"   Failed to fetch master feed for {leg_type}")
            continue

        master_root = ET.fromstring(master_response.content)
        year_elements = master_root.findall('.//leg:facetYear', ns_leg)
        year_links = [(el.attrib['year'], el.attrib['href']) for el in year_elements]

        for year, year_feed_url in year_links:
            print(f" Processing {leg_type.upper()} year {year}")

            try:
                year_response = requests.get(year_feed_url)
                if year_response.status_code != 200:
                    print(f"   Failed year feed: {year_feed_url}")
                    continue

                year_root = ET.fromstring(year_response.content)

                for act_entry in year_root.findall('atom:entry', ns_atom):
                    uri = act_entry.find('atom:id', ns_atom).text.strip()
                    enacted_uri = uri.replace("/id", "") + "/enacted/data.xml"
                    print(f"   Fetching Act: {enacted_uri}")

                    try:
                        act_response = requests.get(enacted_uri)
                        if act_response.status_code != 200:
                            print(f"     Not found: {enacted_uri}")
                            continue

                        act_root = ET.fromstring(act_response.content)

                        title_el = act_root.find('.//leg:Title', ns_leg)
                        long_title_el = act_root.find('.//leg:LongTitle', ns_leg)
                        date_el = act_root.find('.//leg:DateOfEnactment/leg:DateText', ns_leg)
                        body_el = act_root.find('.//leg:Body', ns_leg)

                        act_data = {
                            "type": leg_type,
                            "uri": uri,
                            "year": year,
                            "title": title_el.text.strip() if title_el is not None else f"Act ({year})",
                            "long_title": long_title_el.text.strip() if long_title_el is not None else "",
                            "enactment_date": date_el.text.strip("[]") if date_el is not None else None,
                            "full_text": extract_text_recursive(body_el) if body_el is not None else ""
                        }

                        all_acts.append(act_data)
                        time.sleep(0.5)

                    except Exception as e:
                        print(f"     Error parsing {enacted_uri}: {e}")
                        continue

                time.sleep(1.0)

            except Exception as year_err:
                print(f"   Year error for {year}: {year_err}")
                continue

    except Exception as type_err:
        print(f" Type error for {leg_type}: {type_err}")
        continue

# Save all legislations in a JSON file
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_uk_primary_legislation.json")
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(all_acts, f, indent=2, ensure_ascii=False)

print(f"\n Saved all legislations to {output_path}")
