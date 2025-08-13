import requests
from bs4 import BeautifulSoup
import json
import os

# Base URL fromat used by each GDPR article
base_url = "https://gdpr-info.eu/art-{}-gdpr/"
articles = {}


# Scrape all 99 GDPR articles
for i in range(1, 100):
    url = base_url.format(i)
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        title = soup.find('h1').text.strip()
        content = soup.find('div', class_='entry-content')
        text = content.get_text(separator='\n').strip()

        articles[f"Article {i}"] = {
            "title": title,
            "url": url,
            "text": text
        }
    else:
        print(f"Article {i} not found or failed to load.")
        continue

# Get current dicrectory
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'gdpr_articles.json')

# Save all articles in a JSON file
with open(file_path, 'w', encoding='utf-8') as f:
    json.dump(articles, f, ensure_ascii=False, indent=4)

print(f"GDPR articles saved to: {file_path}")
