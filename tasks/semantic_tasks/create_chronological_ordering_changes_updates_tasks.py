import json
import random
from datetime import datetime, timezone

# Load legislation changes file
with open("/Users/apple/Desktop/uni/kings/project/database/legislation_changes_1700_2025_complete.json", "r", encoding="utf-8") as f:
    changes = json.load(f)

title_date_pairs = []
title_to_updated_date = {}

# Identify the most recent update of a legislation
for entry in changes:
    title = entry.get("affecting_title")
    modified = entry.get("modified")
    updated = entry.get("entry_updated")
    if title and modified and updated:
        try:
            mod_date = datetime.fromisoformat(modified.replace("Z", "+00:00")).astimezone(timezone.utc)
            updated_date = datetime.fromisoformat(updated.replace("Z", "+00:00")).astimezone(timezone.utc)
            title_date_pairs.append((title, mod_date))
            if title not in title_to_updated_date or updated_date > title_to_updated_date[title]:
                title_to_updated_date[title] = updated
        except:
            continue

# Deduplicate by title, keeping the earliest change date
title_to_earliest_date = {}
for title, date in title_date_pairs:
    if title not in title_to_earliest_date or date < title_to_earliest_date[title]:
        title_to_earliest_date[title] = date

# Build final sorted list of titles with dates
sorted_title_dates = list(title_to_earliest_date.items())

# Create tasks
tasks = []
task_id = 1
random.seed(42)

for _ in range(100):  # 100 = number of tasks, can be changed to generate more tasks
    sample = random.sample(sorted_title_dates, k=3)  # Change value of k to change number of legislations in task
    titles = [title for title, _ in sample]
    sorted_titles = [title for title, _ in sorted(sample, key=lambda x: x[1])]
    answer = [{"title": title, "entry_updated": title_to_updated_date.get(title, "")} for title in sorted_titles]

    task = {
        "task_id": f"CH{task_id:03}",
        "task_type": "change_ordering",
        "prompt": f"Arrange the following legislative changes in chronological order of when they were last updated: " + ", ".join(titles),
        "prompt_with_dates": (
            "Arrange these legislative changes in chronological order based on the following update dates: " +
            "; ".join([f"{title} ({title_to_updated_date.get(title, 'unknown')})" for title in titles])
        ),
        "answer": answer
    }
    tasks.append(task)
    task_id += 1

# Save tasks with answers in a JSON file
with open("change_update_ordering_tasks_with_answers.json", "w", encoding="utf-8") as f:
    json.dump(tasks, f, indent=2, ensure_ascii=False)

# Save tasks without answers (test set) in a JSON file
test_tasks = [{k: v for k, v in task.items() if k != "answer"} for task in tasks]
with open("change_update_ordering_tasks_without_answers.json", "w", encoding="utf-8") as f:
    json.dump(test_tasks, f, indent=2, ensure_ascii=False)

print(f"Created {len(tasks)} chronological change ordering tasks with and without enactment date prompts.")
