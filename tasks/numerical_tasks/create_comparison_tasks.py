import json
import random
from datetime import datetime
import re

# Parse enactment dates by removing ordinal suffix (example: 8th -> 8)
def parse_date(date_str):
    date_str = re.sub(r'(\d{1,2})(st|nd|rd|th)', r'\1', date_str)
    return datetime.strptime(date_str.strip(), '%d %B %Y')

# Load combined_legal_documents file
with open("/Users/apple/Desktop/uni/kings/project/database/combined_legal_documents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Filter primary/secondary legislations with valid enactment dates
acts = []
for item in data:
    if item.get("category") in ["primary legislation", "secondary legislation"] and "enactment_date" in item:
        try:
            item["parsed_date"] = parse_date(item["enactment_date"])
            acts.append(item)
        except Exception:
            continue

# Generate tasks comparing two legislations
tasks = []
task_id = 1

for _ in range(100):  # 100 = number of tasks, can be changed to generate more tasks
    a, b = random.sample(acts, 2)
    date_a = a["parsed_date"]
    date_b = b["parsed_date"]

    # Determine older/newer legislation
    if date_a < date_b:
        older, newer = a, b
    else:
        older, newer = b, a

    # Create task with two prompts, one with dates and one without
    task = {
        "task_id": f"CO{task_id:03}",
        "task_type": "comparison_older_newer",
        "prompt": f"Between '{a['title']}' and '{b['title']}', which legislation is older and which is newer?",
        "prompt_with_dates": f"'{a['title']}' was enacted on {a['enactment_date']} and '{b['title']}' was enacted on {b['enactment_date']}. Which one is older and which one is newer?",
        "answer": {
            "older": older["title"],
            "older_enacted": older["enactment_date"],
            "newer": newer["title"],
            "newer_enacted": newer["enactment_date"]
        }
    }
    tasks.append(task)
    task_id += 1

# Save tasks with answers in a JSON file
with open("comparison_tasks_with_answers.json", "w", encoding="utf-8") as f:
    json.dump(tasks, f, indent=2, ensure_ascii=False)

# Save tasks without answers (test set) in a JSON file
test_only = [{k: v for k, v in t.items() if k != "answer"} for t in tasks]
with open("comparison_tasks_without_answers.json", "w", encoding="utf-8") as f:
    json.dump(test_only, f, indent=2, ensure_ascii=False)

print(f"Generated {len(tasks)} comparison tasks with and without enactment date prompts.")
