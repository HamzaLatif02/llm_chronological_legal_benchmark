import json

# Load Gemini answers file
with open("/Users/apple/Desktop/uni/kings/project/test/gemini_answers.json", "r", encoding="utf-8") as f:
    gemini_answers = json.load(f)

# Load ground truth file
with open("/Users/apple/Desktop/uni/kings/project/tasks/timeline_tasks/during_tasks_with_answers.json", "r", encoding="utf-8") as f:
    ground_truth = json.load(f)

# Filter tasks where taskID starts with 'DU'
gemini_answers = [ans for ans in gemini_answers if ans.get("task_id", "").startswith("DU")]
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
for ans in gemini_answers:
    task_id = ans["task_id"]
    if task_id not in ground_truth:
        continue

    expected = ground_truth[task_id]["answer"]["during"].strip().lower()
    gemini_main = find_yes_no(ans.get("answer", ""))
    gemini_dates = find_yes_no(ans.get("answer_with_dates", ""))

    result = {
        "task_id": task_id,
        "expected": expected,
        "gemini_main_answer": gemini_main,
        "gemini_with_dates_answer": gemini_dates,
        "correct_main": gemini_main == expected,
        "correct_with_dates": gemini_dates == expected,
        "gemini_main_snippet": ans.get("answer", "")[:200],
        "gemini_with_dates_snippet": ans.get("answer_with_dates", "")[:200]
    }

    results.append(result)

# Calculate accuracy scores
correct_main = sum(1 for r in results if r["correct_main"])
correct_dates = sum(1 for r in results if r["correct_with_dates"])
total = len(results)

# Print results
print(f"Correct in 'answer': {correct_main} / {total}")
print(f"Correct in 'answer_with_dates': {correct_dates} / {total}")
print("Results saved to 'gemini_du_responses.json'")

# Save results in JSON format
with open("gemini_du_responses.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
