import json
import re

# Load Mistral answers file
with open("/Users/apple/Desktop/uni/kings/project/test/mistral_answers.json", "r", encoding="utf-8") as f:
    mistral_data = json.load(f)

# Load ground truth file
with open("/Users/apple/Desktop/uni/kings/project/tasks/semantic_tasks/relationship_chain_tasks_with_answers.json", "r", encoding="utf-8") as f:
    ground_truth_data = json.load(f)

# Filter tasks where taskID starts with 'RC'
mistral_data = [x for x in mistral_data if x.get("task_id", "").startswith("RC")]
ground_truth = {x["task_id"]: x for x in ground_truth_data if x.get("task_id", "").startswith("RC")}

# Normalise text by converting to lowercase and 
# removing characters that are not lowercase letters and digits
def normalise(text):
    return re.sub(r"[^a-z0-9]+", "", text.lower())

results = []

# Iterate through all tasks
for item in mistral_data:
    task_id = item["task_id"]
    mistral_text = item.get("answer", "")
    mistral_norm = normalise(mistral_text)

    if task_id not in ground_truth:
        continue

    expected_titles = ground_truth[task_id]["answer"]
    found = []
    missing = []

    # Check if legislation title is found in answer
    for title in expected_titles:
        if normalise(title) in mistral_norm:
            found.append(title)
        else:
            missing.append(title)

    correct = len(missing) == 0

    results.append({
        "task_id": task_id,
        "correct": correct,
        "found": found,
        "missing": missing,
        "mistral_text_snippet": mistral_text[:300]
    })

# Calculate accuracy scores
correct_count = sum(1 for r in results if r["correct"])
total = len(results)

# Print results
print(f"Correct relationship chain answers: {correct_count} / {total}")
print("Results saved to 'mistral_rc_responses.json'")

# Save results in JSON format
with open("mistral_rc_responses.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
