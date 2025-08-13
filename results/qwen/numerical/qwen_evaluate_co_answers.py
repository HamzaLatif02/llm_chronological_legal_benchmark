import json
import re

# Load Qwen answers file
with open("/Users/apple/Desktop/uni/kings/project/test/qwen_answers.json", "r", encoding="utf-8") as f:
    qwen_answers = json.load(f)

# Load ground truth file
with open("/Users/apple/Desktop/uni/kings/project/tasks/numerical_tasks/comparison_tasks_with_answers.json", "r", encoding="utf-8") as f:
    ground_truth = json.load(f)

# Filter tasks where taskID starts with 'CO'
qwen_answers = [ans for ans in qwen_answers if ans.get("task_id", "").startswith("CO")]
ground_truth = {task["task_id"]: task for task in ground_truth if task.get("task_id", "").startswith("CO")}

# Normalise text by converting to lowercase and 
# removing characters that are not lowercase letters and digits
def normalise(text):
    return re.sub(r"[^a-z0-9]+", "", text.lower())

# Check if older and newer assignments are correct in Qwen answer
def check_comparison(text, older, newer):
    text_norm = normalise(text)
    older_correct = normalise(older) in text_norm
    newer_correct = normalise(newer) in text_norm
    return older_correct and newer_correct

results = []

# Iterate through all tasks
for ans in qwen_answers:
    task_id = ans["task_id"]
    if task_id not in ground_truth:
        continue

    gt = ground_truth[task_id]["answer"]
    older = gt["older"]
    newer = gt["newer"]

    qwen_main = ans.get("answer", "")
    qwen_dates = ans.get("answer_with_dates", "")

    main_correct = check_comparison(qwen_main, older, newer)
    dates_correct = check_comparison(qwen_dates, older, newer)

    results.append({
        "task_id": task_id,
        "expected_older": older,
        "expected_newer": newer,
        "answer_correct": main_correct,
        "answer_with_dates_correct": dates_correct,
        "qwen_main_snippet": qwen_main[:300],
        "qwen_with_dates_snippet": qwen_dates[:300]
    })

# Calculate accuracy scores
main_score = sum(1 for r in results if r["answer_correct"])
dates_score = sum(1 for r in results if r["answer_with_dates_correct"])
total = len(results)

# Print results
print(f"'answer' field correct: {main_score}/{total}")
print(f"'answer_with_dates' field correct: {dates_score}/{total}")
print("Results saved to 'qwen_co_responses.json'")

# Save results in JSON format
with open("qwen_co_responses.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
