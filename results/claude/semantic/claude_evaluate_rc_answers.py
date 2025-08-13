import json
import re

# Load Claude answers file
with open("/Users/apple/Desktop/uni/kings/project/test/claude_answers.json", "r", encoding="utf-8") as f:
    claude_data = json.load(f)

# Load ground truth file
with open("/Users/apple/Desktop/uni/kings/project/tasks/semantic_tasks/relationship_chain_tasks_with_answers.json", "r", encoding="utf-8") as f:
    ground_truth_data = json.load(f)

# Filter tasks where taskID starts with 'RC'
claude_data = [x for x in claude_data if x.get("task_id", "").startswith("RC")]
ground_truth = {x["task_id"]: x for x in ground_truth_data if x.get("task_id", "").startswith("RC")}

# Normalise text by converting to lowercase and 
# removing characters that are not lowercase letters and digits
def normalise(text):
    return re.sub(r"[^a-z0-9]+", "", text.lower())

results = []

# Iterate through all tasks
for item in claude_data:
    task_id = item["task_id"]
    claude_text = item.get("answer", "")
    claude_norm = normalise(claude_text)

    if task_id not in ground_truth:
        continue

    expected_titles = ground_truth[task_id]["answer"]
    found = []
    missing = []

    # Check if legislation title is found in answer
    for title in expected_titles:
        if normalise(title) in claude_norm:
            found.append(title)
        else:
            missing.append(title)

    correct = len(missing) == 0

    results.append({
        "task_id": task_id,
        "correct": correct,
        "found": found,
        "missing": missing,
        "claude_text_snippet": claude_text[:300]
    })

# Calculate accuracy scores
correct_count = sum(1 for r in results if r["correct"])
total = len(results)

# Print results
print(f"Correct relationship chain answers: {correct_count} / {total}")
print("Results saved to 'claude_rc_responses.json'")

# Save results in JSON format
with open("claude_rc_responses.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
