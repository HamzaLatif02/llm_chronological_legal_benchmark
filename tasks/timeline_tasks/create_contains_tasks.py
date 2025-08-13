import json
from datetime import datetime
import random

# Load legislation timeline file
with open("/Users/apple/Desktop/uni/kings/project/database/legislation_timeline.json", "r", encoding="utf-8") as f:
    timeline = json.load(f)

# Parse date strings into datetime object
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return None

# Generate random unique pairs
valid_pairs = []
for i in range(len(timeline)):
    for j in range(len(timeline)):
        if i == j:
            continue

        lawA = timeline[i]
        lawB = timeline[j]

        startA = parse_date(lawA["start_date"])
        endA = parse_date(lawA["end_date"])
        startB = parse_date(lawB["start_date"])
        endB = parse_date(lawB["end_date"])

        if all([startA, endA, startB, endB]):
            valid_pairs.append((lawA, lawB))

# Sample 100 valid pairs
random.seed(42)
sampled_pairs = random.sample(valid_pairs, min(100, len(valid_pairs)))

# Create tasks
tasks_with_answers = []
tasks_without_answers = []

for task_id, (lawA, lawB) in enumerate(sampled_pairs, start=1):
    titleA = lawA["title"]
    titleB = lawB["title"]
    startA_raw, endA_raw = lawA["start_date"], lawA["end_date"]
    startB_raw, endB_raw = lawB["start_date"], lawB["end_date"]

    startA = parse_date(startA_raw)
    endA = parse_date(endA_raw)
    startB = parse_date(startB_raw)
    endB = parse_date(endB_raw)

    # Ground truth condition: A starts before B and ends after B
    contains = startA < startB and endA > endB
    contains_text = "yes" if contains else "no"

    task = {
        "task_id": f"CN{task_id:03}",
        "task_type": "contains_task",
        "prompt": f"Does '{titleA}' contain '{titleB}'?",
        "prompt_with_dates": (
            f"Does '{titleA}' (from {startA_raw} to {endA_raw}) contain "
            f"'{titleB}' (from {startB_raw} to {endB_raw})?"
        ),
        "answer": {
            "contains": contains_text,
            "legislation_1": {
                "title": titleA,
                "start_date": startA_raw,
                "end_date": endA_raw
            },
            "legislation_2": {
                "title": titleB,
                "start_date": startB_raw,
                "end_date": endB_raw
            }
        }
    }

    tasks_with_answers.append(task)
    tasks_without_answers.append({k: v for k, v in task.items() if k != "answer"})

# Save tasks with answers in a JSON file
with open("contains_tasks_with_answers.json", "w", encoding="utf-8") as f:
    json.dump(tasks_with_answers, f, indent=2, ensure_ascii=False)

# Save tasks without answers (test set) in a JSON file
with open("contains_tasks_without_answers.json", "w", encoding="utf-8") as f:
    json.dump(tasks_without_answers, f, indent=2, ensure_ascii=False)

print(f"Generated {len(tasks_with_answers)} 'contains' tasks with and without date prompts.")
