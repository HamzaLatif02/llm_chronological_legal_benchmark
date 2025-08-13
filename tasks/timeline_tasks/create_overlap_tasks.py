import json
import random
from datetime import datetime

# Load legislation timeline file
with open("/Users/apple/Desktop/uni/kings/project/database/legislation_timeline.json", "r", encoding="utf-8") as f:
    timeline = json.load(f)

# Parse date strings into datetime object
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except:
        return None

# Build valid law pairs and store 'overlap' status
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

        if not all([startA, endA, startB, endB]):
            continue  # Skip if any required date is missing

        # Ground truth condition: A starts before B, ends during B
        if startA < startB and startB <= endA <= endB:
            overlap = "yes"
        else:
            overlap = "no"

        valid_pairs.append({
            "lawA": lawA,
            "lawB": lawB,
            "overlap": overlap
        })

# Sample 100 valid pairs
random.seed(42)
sampled_pairs = random.sample(valid_pairs, min(100, len(valid_pairs)))

# Create tasks
tasks_with_answers = []
tasks_without_answers = []

for task_id, pair in enumerate(sampled_pairs, start=1):
    lawA = pair["lawA"]
    lawB = pair["lawB"]
    overlap = pair["overlap"]

    task = {
        "task_id": f"OL{task_id:03}",
        "task_type": "overlap_task",
        "prompt": f"Does '{lawA['title']}' overlap '{lawB['title']}'?",
        "prompt_with_dates": (
            f"Does '{lawA['title']}' (from {lawA['start_date']} to {lawA['end_date']}) "
            f"overlap '{lawB['title']}' (from {lawB['start_date']} to {lawB['end_date']})?"
        ),
        "answer": {
            "overlap": overlap,
            "legislation_1": {
                "title": lawA["title"],
                "start_date": lawA["start_date"],
                "end_date": lawA["end_date"]
            },
            "legislation_2": {
                "title": lawB["title"],
                "start_date": lawB["start_date"],
                "end_date": lawB["end_date"]
            }
        }
    }

    tasks_with_answers.append(task)
    tasks_without_answers.append({k: v for k, v in task.items() if k != "answer"})

# Save tasks with answers in a JSON file
with open("overlap_tasks_with_answers.json", "w", encoding="utf-8") as f:
    json.dump(tasks_with_answers, f, indent=2, ensure_ascii=False)

# Save tasks without answers (test set) in a JSON file
with open("overlap_tasks_without_answers.json", "w", encoding="utf-8") as f:
    json.dump(tasks_without_answers, f, indent=2, ensure_ascii=False)

print(f"Generated {len(tasks_with_answers)} 'overlap' tasks with and without date prompts.")
