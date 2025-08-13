import os
import json
import time
from dotenv import load_dotenv
from together import Together

# Load environment variables (API key)
# API key should be stored and declared in a separate file called '.env'
load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")

# Initialise Together client
client = Together(api_key=api_key)

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
# Define Llama model name
model_name = "meta-llama/Llama-3.3-70B-Instruct-Turbo-Free"

# Iterate over all task files
for file_path in file_paths:
    print(f"Processing file: {file_path}")
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            tasks = json.load(f)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        continue

    for task in tasks:
        task_id = task.get("task_id")
        prompt_1 = task.get("prompt")
        prompt_2 = task.get("prompt_with_dates")
        result = {"task_id": task_id}

        try:
            # Prompt 1 (without dates)
            if prompt_1:
                res_1 = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt_1}],
                    temperature=0.0,
                    max_tokens=512,
                )
                result["answer"] = res_1.choices[0].message.content.strip()
                time.sleep(1)

            # Prompt 2 (if available) (with dates)
            if prompt_2:
                res_2 = client.chat.completions.create(
                    model=model_name,
                    messages=[{"role": "user", "content": prompt_2}],
                    temperature=0.0,
                    max_tokens=512,
                )
                result["answer_with_dates"] = res_2.choices[0].message.content.strip()
                time.sleep(1)

            results.append(result)

        except Exception as e:
            print(f"Error with task {task_id}: {e}")
            continue

# Save Llama results answers in a JSON file
with open("llama_answers.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print(f"\n Completed {len(results)} total Llama prompt responses.")

