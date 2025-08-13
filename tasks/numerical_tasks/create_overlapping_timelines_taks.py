import json
import random
from datetime import datetime
import re
from collections import defaultdict

# Parse enactment dates by removing ordinal suffix (example: 8th -> 8)
def parse_date(date_str):
    date_str = re.sub(r'(\d{1,2})(st|nd|rd|th)', r'\1', date_str)
    return datetime.strptime(date_str.strip(), '%d %B %Y')

# Format dates into: "YYYY-MM-DD"
def format_date_ymd(date_obj):
    return date_obj.strftime('%Y-%m-%d')

# Load combined_legal_documents file
with open("/Users/apple/Desktop/uni/kings/project/database/combined_legal_documents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Filter primary/secondary legislation with valid enactment date
acts = []
for item in data:
    if item.get("category") in ["primary legislation", "secondary legislation"] and "enactment_date" in item:
        try:
            date = parse_date(item["enactment_date"])
            item["parsed_date"] = date
            item["formatted_date"] = format_date_ymd(date)
            acts.append(item)
        except:
            continue

# Randomly sample 100 legislations
random.seed(42)
sampled_acts = random.sample(acts, min(100, len(acts)))

# Group legislations by year
by_year = defaultdict(list)
for act in sampled_acts:
    by_year[act["parsed_date"].year].append(act)

# Generate overlapping timelines tasks
tasks = []
task_id = 1

for year, group in by_year.items():
    if len(group) < 2:
        continue

    sampled_pairs = random.sample(
        [(a, b) for i, a in enumerate(group) for b in group[i + 1:]],
        min(5, len(group) * (len(group) - 1) // 2)
    )
    
    # Check if legislations were enacted on the same day
    for a, b in sampled_pairs:
        simultaneous = a["parsed_date"] == b["parsed_date"]
        answer_text = "Yes" if simultaneous else "No"

        task = {
            "task_id": f"OV{task_id:03}",
            "task_type": "overlapping_enactment_check",
            "prompt": f"Were the '{a['title']}' and the '{b['title']}' enacted on the same day in {year}?",
            "prompt_with_dates": f"'{a['title']}' was enacted on {a['formatted_date']}, and '{b['title']}' was enacted on {b['formatted_date']}. Were they enacted on the same day?",
            "answer": {
                "answer": answer_text,
                "a_title": a["title"],
                "a_date": a["formatted_date"],
                "b_title": b["title"],
                "b_date": b["formatted_date"]
            }
        }
        tasks.append(task)
        task_id += 1

# Save tasks with answers in a JSON file
with open("overlapping_tasks_with_answers.json", "w", encoding="utf-8") as f:
    json.dump(tasks, f, indent=2, ensure_ascii=False)

# Save tasks without answers (test set) in a JSON file
test_only = [{k: v for k, v in task.items() if k != "answer"} for task in tasks]
with open("overlapping_tasks_without_answers.json", "w", encoding="utf-8") as f:
    json.dump(test_only, f, indent=2, ensure_ascii=False)

print(f"Created {len(tasks)} overlapping enactment tasks with and without enactment date prompts.")
