import os
import json
import time
from dotenv import load_dotenv
import anthropic

# Load environment variables (API key)
# API key should be stored and declared in a separate file called '.env'
load_dotenv()
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# List of file paths of all 12 tasks without answers
file_paths = [
    "/Users/apple/Desktop/uni/kings/project/tasks/semantic_tasks/change_update_ordering_tasks_without_answers.json",
    "/Users/apple/Desktop/uni/kings/project/tasks/semantic_tasks/ordering_tasks_without_answers.json",
    "/Users/apple/Desktop/uni/kings/project/tasks/semantic_tasks/recital_to_article_tasks_without_answers.json",
    "/Users/apple/Desktop/uni/kings/project/tasks/semantic_tasks/semantic_linking_tasks_without_answers.json",
    "/Users/apple/Desktop/uni/kings/project/tasks/semantic_tasks/relationship_chain_tasks_without_answers.json",
    "/Users/apple/Desktop/uni/kings/project/tasks/numerical_tasks/comparison_tasks_without_answers.json",
    "/Users/apple/Desktop/uni/kings/project/tasks/numerical_tasks/overlapping_tasks_without_answers.json",
    "/Users/apple/Desktop/uni/kings/project/tasks/numerical_tasks/duration_between_tasks_without_answers.json",
    "/Users/apple/Desktop/uni/kings/project/tasks/timeline_tasks/contains_tasks_without_answers.json",
    "/Users/apple/Desktop/uni/kings/project/tasks/timeline_tasks/during_tasks_without_answers.json",
    "/Users/apple/Desktop/uni/kings/project/tasks/timeline_tasks/overlap_tasks_without_answers.json",
    "/Users/apple/Desktop/uni/kings/project/tasks/timeline_tasks/overlapped_by_tasks_without_answers.json"
]

results = []

# Iterate over all task files
for file_path in file_paths:
    print(f"Processing file: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tasks = json.load(f)
    except Exception as e:
        print(f"Could not read {file_path}: {e}")
        continue

    for task in tasks:
        task_id = task.get("task_id")
        prompt_1 = task.get("prompt")
        prompt_2 = task.get("prompt_with_dates")

        response_record = {"task_id": task_id}

        try:
            # Prompt 1 (without dates)
            if prompt_1:
                response_1 = client.messages.create(
                    model="claude-3-5-haiku-20241022", # Define Claude model name
                    max_tokens=500,
                    temperature=0,
                    messages=[{"role": "user", "content": prompt_1}]
                )
                response_record["answer"] = response_1.content[0].text
                time.sleep(1)

            # Prompt 2 (if available) (with dates)
            if prompt_2:
                response_2 = client.messages.create(
                    model="claude-3-5-haiku-20241022", # Define same Claude model name
                    max_tokens=500,
                    temperature=0,
                    messages=[{"role": "user", "content": prompt_2}]
                )
                response_record["answer_with_dates"] = response_2.content[0].text
                time.sleep(1)

            results.append(response_record)

        except Exception as e:
            print(f"Error with task {task_id}: {e}")
            continue

# Save Claude results answers in a JSON file
with open("claude_answers.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n Completed {len(results)} total Claude prompt responses.")
