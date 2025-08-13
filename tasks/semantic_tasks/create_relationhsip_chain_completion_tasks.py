import json
from collections import defaultdict

# Load legislation changes file
with open("/Users/apple/Desktop/uni/kings/project/database/legislation_changes_1700_2025_complete.json", "r", encoding="utf-8") as f:
    changes = json.load(f)

# Group affecting acts by affected act
chain_map = defaultdict(list)
for entry in changes:
    affected = entry.get("affected_title")
    affecting = entry.get("affecting_title")
    if affected and affecting:
        chain_map[affected].append(affecting)

# Create tasks
tasks = []
task_id = 1
for affected_title, affecting_titles in chain_map.items():
    unique_affecting = sorted(set(affecting_titles))
    if len(unique_affecting) > 1:
        task = {
            "task_id": f"RC{task_id:03}",
            "task_type": "relationship_chain_completion",
            "prompt": f"Which acts have affected the {affected_title}?",
            "answer": unique_affecting
        }
        tasks.append(task)
        task_id += 1
        if len(tasks) >= 100: # Create 100 tasks, change for a different number of tasks
            break

# Save tasks with answers in a JSON file
with open("relationship_chain_tasks_with_answers.json", "w", encoding="utf-8") as f:
    json.dump(tasks, f, indent=2, ensure_ascii=False)

# Save tasks without answers (test set) in a JSON file
test_tasks = [{k: v for k, v in task.items() if k != "answer"} for task in tasks]
with open("relationship_chain_tasks_without_answers.json", "w", encoding="utf-8") as f:
    json.dump(test_tasks, f, indent=2, ensure_ascii=False)

print(f"Generated {len(tasks)} relationship chain tasks.")
