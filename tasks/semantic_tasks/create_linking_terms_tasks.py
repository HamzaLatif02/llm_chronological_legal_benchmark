import json
from collections import defaultdict

# Load matched contexts with titles file
with open("/Users/apple/Desktop/uni/kings/project/database/matched_contexts_with_title.json", "r", encoding="utf-8") as f:
    links = json.load(f)

# Dictionary to group by (source_title, linking_term)
task_dict = defaultdict(list)

for entry in links:
    source = entry.get("source_title")
    link = entry.get("linking_term")
    target = entry.get("matched_title")

    # Reformat linking terms by removing trailing 's' (example: repeals -> repeal)
    if link and link.endswith('s'):
        link = link[:-1]

    if source and link and target:
        key = (source, link)
        task_dict[key].append(target)

# Create tasks
tasks = []
for i, ((source, link), targets) in enumerate(task_dict.items(), start=1):
    task = {
        "task_id": f"SE{i:03}",
        "task_type": "legislation_linking",
        "prompt": f"Which legislation(s) does {source} {link}?",
        "answer": list(set(targets))  # Remove any duplicates
    }
    tasks.append(task)

# Save tasks with answers in a JSON file
with open("semantic_linking_tasks_with_answers.json", "w", encoding="utf-8") as f:
    json.dump(tasks, f, indent=2, ensure_ascii=False)

# Save tasks without answers (test set) in a JSON file
test_only = [{k: v for k, v in task.items() if k != "answer"} for task in tasks]
with open("semantic_linking_tasks_without_answers.json", "w", encoding="utf-8") as f:
    json.dump(test_only, f, indent=2, ensure_ascii=False)

print(f"Created {len(tasks)} semantic linking tasks.")
