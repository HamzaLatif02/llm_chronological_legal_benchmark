import json
import re

# Load Gemini answers file
with open("/Users/apple/Desktop/uni/kings/project/test/gemini_answers.json", "r", encoding="utf-8") as f:
    gemini_data = json.load(f)

# Load ground truth file
with open("/Users/apple/Desktop/uni/kings/project/tasks/semantic_tasks/relationship_chain_tasks_with_answers.json", "r", encoding="utf-8") as f:
    ground_truth_data = json.load(f)

# Filter tasks where taskID starts with 'RC'
gemini_data = [x for x in gemini_data if x.get("task_id", "").startswith("RC")]
ground_truth = {x["task_id"]: x for x in ground_truth_data if x.get("task_id", "").startswith("RC")}

# Normalise text by converting to lowercase and 
# removing characters that are not lowercase letters and digits
def normalise(text):
    return re.sub(r"[^a-z0-9]+", "", text.lower())

results = []

# Iterate through all tasks
for item in gemini_data:
    task_id = item["task_id"]
    gemini_text = item.get("answer", "")
    gemini_norm = normalise(gemini_text)

    if task_id not in ground_truth:
        continue

    expected_titles = ground_truth[task_id]["answer"]
    found = []
    missing = []

    # Check if legislation title is found in answer
    for title in expected_titles:
        if normalise(title) in gemini_norm:
            found.append(title)
        else:
            missing.append(title)

    correct = len(missing) == 0

    results.append({
        "task_id": task_id,
        "correct": correct,
        "found": found,
        "missing": missing,
        "gemini_text_snippet": gemini_text[:300]
    })

# Calculate accuracy scores
correct_count = sum(1 for r in results if r["correct"])
total = len(results)

# Print results
print(f"Correct relationship chain answers: {correct_count} / {total}")
print("Results saved to 'gemini_rc_responses.json'")

# Save results in JSON format
with open("gemini_rc_responses.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
