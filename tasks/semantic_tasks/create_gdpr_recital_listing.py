import json
import re

# Load GDPR articles file
with open("/Users/apple/Desktop/uni/kings/project/database/gdpr_articles.json", "r", encoding="utf-8") as f:
    gdpr_articles = json.load(f)

# Create tasks
tasks = []
task_id = 1

for article_key, article_data in gdpr_articles.items():
    title = article_data.get("title", article_key)
    raw_text = article_data.get("text", "")

    # Clean article text and remove everything after the first '←' or 'GDPR Table of contents'
    cleaned_text = re.sub(r'\s+', ' ', raw_text.strip())

    cut_markers = ['←', 'Art. 2 GDPR → GDPR Table of contents']
    for marker in cut_markers:
        if marker in cleaned_text:
            cleaned_text = cleaned_text.split(marker)[0].strip()
            break  # Stop at first match


    recitals = []

    # Search for "Suitable Recitals" inside text
    match = re.search(r"Suitable Recitals\s*(.*)", cleaned_text, re.IGNORECASE)
    if match:
        recitals_block = match.group(1)

        # Extract (1) Text (2) Text (structure of how recitals are presented in the text)
        recital_matches = re.findall(r"\(\s*(\d+)\s*\)\s*([^(]+?)(?=\(\s*\d+\s*\)|$)", recitals_block)

        for num, text in recital_matches:
            recitals.append({"number": num, "text": text.strip()})

    # Create a task, even if no recitals were found
    task = {
        "task_id": f"RE{task_id:03}",
        "task_type": "gdpr_recital",
        "prompt": f"List the corresponding recital(s) for the following GDPR article: {title}",
        "answer": {title: recitals}
    }
    tasks.append(task)
    task_id += 1

# Save tasks with answers in a JSON file
with open("recital_to_article_tasks_with_answers.json", "w", encoding="utf-8") as f:
    json.dump(tasks, f, indent=2, ensure_ascii=False)

# Save tasks without answers (test set) in a JSON file
test_only_tasks = [{k: v for k, v in task.items() if k != "answer"} for task in tasks]
with open("recital_to_article_tasks_without_answers.json", "w", encoding="utf-8") as f:
    json.dump(test_only_tasks, f, indent=2, ensure_ascii=False)

print(f"Created {len(tasks)} GDPR recitals tasks.")
