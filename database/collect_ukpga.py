import os
import time
import json
import requests
import xml.etree.ElementTree as ET

# Define XML namespaces for Atom feeds and legislations
ns_atom = {'atom': 'http://www.w3.org/2005/Atom'}
ns_leg = {'leg': 'http://www.legislation.gov.uk/namespaces/legislation'}

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

# Master feed for all UKPGA years
master_feed_url = "https://www.legislation.gov.uk/ukpga/data.feed"
master_response = requests.get(master_feed_url)
master_root = ET.fromstring(master_response.content)

# Get 'year' from 'leg:facetYear' elements
year_elements = master_root.findall('.//leg:facetYear', ns_leg)
year_links = [(el.attrib['year'], el.attrib['href']) for el in year_elements]

all_acts = []

# Loop through each year in facetYear
for year, year_feed_url in year_links:
    print(f"\n Processing year: {year}")

    try:
        year_response = requests.get(year_feed_url)
        if year_response.status_code != 200:
            print(f"   Failed to fetch year feed: {year}")
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
                    "uri": uri,
                    "year": year,
                    "title": title_el.text.strip() if title_el is not None else f"Act ({year})",
                    "long_title": long_title_el.text.strip() if long_title_el is not None else "",
                    "enactment_date": date_el.text.strip('[]') if date_el is not None else None,
                    "full_text": extract_text_recursive(body_el) if body_el is not None else ""
                }

                all_acts.append(act_data)
                time.sleep(0.5)

            except Exception as e:
                print(f"     Error processing {enacted_uri}: {e}")
                continue

        time.sleep(1.0)

    except Exception as year_err:
        print(f"   Error processing year {year}: {year_err}")
        continue

# Save all 'UUKPGA' legislations in a JSON file
output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "all_ukpga_legislation.json")
with open(output_path, 'w', encoding='utf-8') as f:
    json.dump(all_acts, f, indent=2, ensure_ascii=False)

print(f"\n Saved all legislation to {output_path}")
