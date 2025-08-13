import json

# Load Mistral answers file
with open("/Users/apple/Desktop/uni/kings/project/test/mistral_answers.json", "r", encoding="utf-8") as f:
    mistral_answers = json.load(f)

# Load ground truth file
with open("/Users/apple/Desktop/uni/kings/project/tasks/timeline_tasks/during_tasks_with_answers.json", "r", encoding="utf-8") as f:
    ground_truth = json.load(f)

# Filter tasks where taskID starts with 'DU'
mistral_answers = [ans for ans in mistral_answers if ans.get("task_id", "").startswith("DU")]
ground_truth = {task["task_id"]: task for task in ground_truth if task.get("task_id", "").startswith("DU")}

# Extract first 'Yes'/'No' word from answer
def find_yes_no(text):
    text = text.strip().lower()
    if "yes," in text:
        return "yes"
    elif "no," in text:
        return "no"
    return None

results = []

# Iterate through all tasks
for ans in mistral_answers:
    task_id = ans["task_id"]
    if task_id not in ground_truth:
        continue

    expected = ground_truth[task_id]["answer"]["during"].strip().lower()
    mistral_main = find_yes_no(ans.get("answer", ""))
    mistral_dates = find_yes_no(ans.get("answer_with_dates", ""))

    result = {
        "task_id": task_id,
        "expected": expected,
        "mistral_main_answer": mistral_main,
        "mistral_with_dates_answer": mistral_dates,
        "correct_main": mistral_main == expected,
        "correct_with_dates": mistral_dates == expected,
        "mistral_main_snippet": ans.get("answer", "")[:200],
        "mistral_with_dates_snippet": ans.get("answer_with_dates", "")[:200]
    }

    results.append(result)

# Calculate accuracy scores
correct_main = sum(1 for r in results if r["correct_main"])
correct_dates = sum(1 for r in results if r["correct_with_dates"])
total = len(results)

# Print results
print(f"Correct in 'answer': {correct_main} / {total}")
print(f"Correct in 'answer_with_dates': {correct_dates} / {total}")
print("Results saved to 'mistral_du_responses.json'")

# Save results in JSON format
with open("mistral_du_responses.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
