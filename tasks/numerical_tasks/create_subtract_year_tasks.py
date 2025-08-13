import json
import random
from datetime import datetime
from dateutil.relativedelta import relativedelta

import re

# Parse enactment dates by removing ordinal suffix (example: 8th -> 8)
def parse_date(date_str):
    date_str = re.sub(r'(\d{1,2})(st|nd|rd|th)', r'\1', date_str)
    return datetime.strptime(date_str.strip(), '%d %B %Y')

# Format duration as "X years Y months Z days"
def format_duration(delta):
    return f"{delta.years} years {delta.months} months {delta.days} days"

# Load combined_legal_documents file
with open("/Users/apple/Desktop/uni/kings/project/database/combined_legal_documents.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Filter for primary and secondary legislation with valid enactement dates
filtered = [
    item for item in data
    if item.get("category") in ["primary legislation", "secondary legislation"]
    and "enactment_date" in item and item["enactment_date"]
]

# Sort by parsed date
for item in filtered:
    try:
        item["parsed_date"] = parse_date(item["enactment_date"])
    except Exception:
        item["parsed_date"] = None

filtered = [item for item in filtered if item["parsed_date"] is not None]
filtered.sort(key=lambda x: x["parsed_date"])

# Generate duration tasks
tasks = []
task_id = 1

for _ in range(100):  # 100 = number of tasks, can be changed to generate more tasks
    a, b = random.sample(filtered, 2)
    if a["parsed_date"] > b["parsed_date"]:
        a, b = b, a  # Ensure 'legislation a' is earlier

    delta = relativedelta(b["parsed_date"], a["parsed_date"])
    task = {
        "task_id": f"DB{task_id:03}",
        "task_type": "duration_between_laws",
        "prompt": f"How long after '{a['title']}' was '{b['title']}' enacted?",
        "prompt_with_dates": f"'{a['title']}' was enacted on {a['parsed_date'].date().isoformat()}, and {b['title']}' was enacted on {b['parsed_date'].date().isoformat()}. How long after the first was the second enacted?",
        "answer": format_duration(delta)
    }
    tasks.append(task)
    task_id += 1

# Save tasks with answers in a JSON file
with open("duration_between_tasks_with_answers.json", "w", encoding="utf-8") as f:
    json.dump(tasks, f, indent=2, ensure_ascii=False)

# Save tasks without answers (test set) in a JSON file
test_tasks = [{k: v for k, v in task.items() if k != "answer"} for task in tasks]
with open("duration_between_tasks_without_answers.json", "w", encoding="utf-8") as f:
    json.dump(test_tasks, f, indent=2, ensure_ascii=False)

print(f"Created {len(tasks)} duration tasks with and without enactment date prompts.")
