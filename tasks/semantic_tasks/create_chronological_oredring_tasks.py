import json
import uuid
from collections import defaultdict
from datetime import datetime
import random

# Load temporal relationships file
with open("/Users/apple/Desktop/uni/kings/project/database/temporal_relationships/temporal_relationships.json", "r", encoding="utf-8") as f:
    temporal_relationships = json.load(f)

# Group by source, collect source and target titles with dates
grouped = defaultdict(list)
for rel in temporal_relationships:
    grouped[rel["source"]].append({
        "title": rel["source"],
        "date": rel["source_date"]
    })
    grouped[rel["source"]].append({
        "title": rel["target"],
        "date": rel["target_date"]
    })

# Parse ISO date strings
def parse_date(date_str):
    return datetime.strptime(date_str, "%Y-%m-%d")

# Create tasks
tasks = []
seen_groups = set()

for source, entries in grouped.items():
    # Deduplicate by title
    unique_titles = {}
    for entry in entries:
        if entry["title"] not in unique_titles:
            unique_titles[entry["title"]] = entry["date"]

    if len(unique_titles) < 3:
        continue

    sample_size = min(len(unique_titles), random.choice([3, 4, 5]))
    selected = random.sample(list(unique_titles.items()), sample_size)
    titles_with_dates = [{"title": t, "date": parse_date(d)} for t, d in selected]

    correct_order = sorted(titles_with_dates, key=lambda x: x["date"])
    correct_titles = [x["title"] for x in correct_order]

    # Shuffle for prompt variety
    shuffled_titles = random.sample(correct_titles, len(correct_titles))

    group_key = tuple(sorted(correct_titles))
    if group_key in seen_groups:
        continue
    seen_groups.add(group_key)

    # Build string with dates for prompt with dates
    titles_with_dates_str = ", ".join(
        [f"{t['title']} ({t['date'].strftime('%Y-%m-%d')})" for t in titles_with_dates]
    )

    task = {
        "task_id": f"OR{len(tasks) + 1:03}",
        "task_type": "chronological_ordering",
        "prompt": f"Arrange the following legal acts in order of enactment: {', '.join(shuffled_titles)}",
        "prompt_with_dates": f"Arrange the following legal acts in order of enactment: {titles_with_dates_str}",
        "answer": correct_titles
    }
    tasks.append(task)

    if len(tasks) >= 100: # Create 100 tasks, change for a different number of tasks
        break

# Save tasks with answers in a JSON file
with open("ordering_tasks_with_answers.json", "w", encoding="utf-8") as f:
    json.dump(tasks, f, indent=2, ensure_ascii=False)

# Save tasks without answers (test set) in a JSON file
test_tasks = [{k: v for k, v in task.items() if k != "answer"} for task in tasks]
with open("ordering_tasks_without_answers.json", "w", encoding="utf-8") as f:
    json.dump(test_tasks, f, indent=2, ensure_ascii=False)

print(f"Saved {len(tasks)} tasks to chronological enactment ordering tasks with and without enactment date prompts.")
