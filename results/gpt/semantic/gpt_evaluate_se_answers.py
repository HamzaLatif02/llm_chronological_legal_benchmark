import json
import re

# Load GPT answers file
with open("/Users/apple/Desktop/uni/kings/project/test/gpt_answers.json", "r", encoding="utf-8") as f:
    gpt_data = json.load(f)

# Load ground truth file
with open("/Users/apple/Desktop/uni/kings/project/tasks/semantic_tasks/semantic_linking_tasks_with_answers.json", "r", encoding="utf-8") as f:
    ground_truth_data = json.load(f)

# Filter tasks where taskID starts with 'SE'
gpt_data = [x for x in gpt_data if x.get("task_id", "").startswith("SE")]
ground_truth = {x["task_id"]: x for x in ground_truth_data if x.get("task_id", "").startswith("SE")}

# Normalise text by converting to lowercase and 
# removing characters that are not lowercase letters and digits
def normalize(text):
    return re.sub(r"[^a-z0-9]+", "", text.lower())

results = []

# Iterate through all tasks
for item in gpt_data:
    task_id = item["task_id"]
    gpt_text = item.get("answer", "")
    gpt_norm = normalize(gpt_text)

    if task_id not in ground_truth:
        continue

    expected_titles = ground_truth[task_id]["answer"]
    found = []
    missing = []
    
    # Check if legislation title is found in answer
    for title in expected_titles:
        if normalize(title) in gpt_norm:
            found.append(title)
        else:
            missing.append(title)

    correct = len(missing) == 0

    results.append({
        "task_id": task_id,
        "correct": correct,
        "found": found,
        "missing": missing,
        "gpt_text_snippet": gpt_text[:300]
    })

# Calculate accuracy scores
correct_count = sum(1 for r in results if r["correct"])

# Print results
print(f"Correct semantic links: {correct_count} / {len(results)}")
print("Results saved to 'gpt_se_responses.json'")

# Save results in JSON format
with open("gpt_se_responses.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

