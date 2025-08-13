import json
import re

# Load Qwen answers file
with open("/Users/apple/Desktop/uni/kings/project/test/qwen_answers.json", "r", encoding="utf-8") as f:
    qwen_answers = json.load(f)

# Load ground truth file
with open("/Users/apple/Desktop/uni/kings/project/tasks/semantic_tasks/ordering_tasks_with_answers.json", "r", encoding="utf-8") as f:
    ground_truth = json.load(f)

# Filter tasks where taskID starts with 'OR'
qwen_answers = [ans for ans in qwen_answers if ans.get("task_id", "").startswith("OR")]
ground_truth = {task["task_id"]: task for task in ground_truth if task.get("task_id", "").startswith("OR")}

# Normalise text by converting to lowercase and 
# removing characters that are not lowercase letters and digits
def normalise(text):
    return re.sub(r"[^a-z0-9]+", "", text.lower())

# Extract ordered titles from Qwen answer
def extract_titles_from_qwen(text, known_titles):
    norm_text = normalise(text)
    matched = []
    for title in known_titles:
        if normalise(title) in norm_text:
            matched.append(title)
    return matched

# Evaluation logic for each field
def evaluate_field(qwen_text, correct_order):
    extracted_order = extract_titles_from_qwen(qwen_text, correct_order)
    is_correct = extracted_order == correct_order
    return {
        "is_correct": is_correct,
        "qwen_order": extracted_order,
        "qwen_text_snippet": qwen_text[:300]
    }

results = []

# Iterate through all tasks
for ans in qwen_answers:
    task_id = ans["task_id"]
    if task_id not in ground_truth:
        continue

    correct_order = ground_truth[task_id]["answer"]
    qwen_main = ans.get("answer", "")
    qwen_dates = ans.get("answer_with_dates", "")

    main_result = evaluate_field(qwen_main, correct_order)
    dates_result = evaluate_field(qwen_dates, correct_order)

    results.append({
        "task_id": task_id,
        "expected_order": correct_order,
        "answer": main_result,
        "answer_with_dates": dates_result
    })

# Calculate accuracy scores
main_correct = sum(1 for r in results if r["answer"]["is_correct"])
dates_correct = sum(1 for r in results if r["answer_with_dates"]["is_correct"])
total = len(results)

# Print results
print(f"Qwen 'answer' correct: {main_correct} / {total}")
print(f"Qwen 'answer_with_dates' correct: {dates_correct} / {total}")
print("Results saved to 'qwen_or_responses.json'")

# Save results in JSON format
with open("qwen_or_responses.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
