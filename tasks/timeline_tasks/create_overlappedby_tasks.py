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

# Build valid 'overlapped-by' pairs
valid_pairs = []

for i in range(len(timeline)):
    for j in range(len(timeline)):
        if i == j:
            continue

        lawA = timeline[i]
        lawB = timeline[j]

        titleA = lawA["title"]
        titleB = lawB["title"]
        startA_raw, endA_raw = lawA["start_date"], lawA["end_date"]
        startB_raw, endB_raw = lawB["start_date"], lawB["end_date"]

        startA = parse_date(startA_raw)
        endA = parse_date(endA_raw)
        startB = parse_date(startB_raw)
        endB = parse_date(endB_raw)

        if not all([startA, endA, startB, endB]):
            continue

        # Ground truth condition: A starts during B, ends after B
        if startB < startA < endB < endA:
            valid_pairs.append((lawA, lawB, "yes"))
        else:
            valid_pairs.append((lawA, lawB, "no"))

# Sample 100 random valid pairs
random.seed(42)
sampled_pairs = random.sample(valid_pairs, min(100, len(valid_pairs)))

# Create tasks
tasks_with_answers = []
tasks_without_answers = []

for task_id, (lawA, lawB, overlap_text) in enumerate(sampled_pairs, start=1):
    titleA = lawA["title"]
    titleB = lawB["title"]
    startA_raw = lawA["start_date"]
    endA_raw = lawA["end_date"]
    startB_raw = lawB["start_date"]
    endB_raw = lawB["end_date"]

    task = {
        "task_id": f"OB{task_id:03}",
        "task_type": "overlapped_by_task",
        "prompt": f"Is '{titleA}' overlapped by '{titleB}'?",
        "prompt_with_dates": (
            f"Is '{titleA}' (from {startA_raw} to {endA_raw}) overlapped by "
            f"'{titleB}' (from {startB_raw} to {endB_raw})?"
        ),
        "answer": {
            "overlapped_by": overlap_text,
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
with open("overlapped_by_tasks_with_answers.json", "w", encoding="utf-8") as f:
    json.dump(tasks_with_answers, f, indent=2, ensure_ascii=False)

# Save tasks without answers (test set) in a JSON file
with open("overlapped_by_tasks_without_answers.json", "w", encoding="utf-8") as f:
    json.dump(tasks_without_answers, f, indent=2, ensure_ascii=False)

print(f"Generated {len(tasks_with_answers)} 'overlapped-by' tasks with and without date prompts.")
