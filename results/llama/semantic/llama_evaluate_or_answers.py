import json
import re

# Load Llama answers file
with open("/Users/apple/Desktop/uni/kings/project/test/llama_answers.json", "r", encoding="utf-8") as f:
    llama_answers = json.load(f)

# Load ground truth file
with open("/Users/apple/Desktop/uni/kings/project/tasks/semantic_tasks/ordering_tasks_with_answers.json", "r", encoding="utf-8") as f:
    ground_truth = json.load(f)

# Filter tasks where taskID starts with 'OR'
llama_answers = [ans for ans in llama_answers if ans.get("task_id", "").startswith("OR")]
ground_truth = {task["task_id"]: task for task in ground_truth if task.get("task_id", "").startswith("OR")}

# Normalise text by converting to lowercase and 
# removing characters that are not lowercase letters and digits
def normalise(text):
    return re.sub(r"[^a-z0-9]+", "", text.lower())

# Extract ordered titles from Llama answer
def extract_titles_from_llama(text, known_titles):
    norm_text = normalise(text)
    matched = []
    for title in known_titles:
        if normalise(title) in norm_text:
            matched.append(title)
    return matched

# Evaluation logic for each field
def evaluate_field(llama_text, correct_order):
    extracted_order = extract_titles_from_llama(llama_text, correct_order)
    is_correct = extracted_order == correct_order
    return {
        "is_correct": is_correct,
        "llama_order": extracted_order,
        "llama_text_snippet": llama_text[:300]
    }

results = []

# Iterate through all tasks
for ans in llama_answers:
    task_id = ans["task_id"]
    if task_id not in ground_truth:
        continue

    correct_order = ground_truth[task_id]["answer"]
    llama_main = ans.get("answer", "")
    llama_dates = ans.get("answer_with_dates", "")

    main_result = evaluate_field(llama_main, correct_order)
    dates_result = evaluate_field(llama_dates, correct_order)

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
print(f"Llama 'answer' correct: {main_correct} / {total}")
print(f"Llama 'answer_with_dates' correct: {dates_correct} / {total}")
print("Results saved to 'llama_or_responses.json'")

# Save results in JSON format
with open("llama_or_responses.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
