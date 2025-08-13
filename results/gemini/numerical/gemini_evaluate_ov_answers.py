import json

# Load Gemini answers file
with open("/Users/apple/Desktop/uni/kings/project/test/gemini_answers.json", "r", encoding="utf-8") as f:
    gemini_answers = json.load(f)

# Load ground truth file
with open("/Users/apple/Desktop/uni/kings/project/tasks/numerical_tasks/overlapping_tasks_with_answers.json", "r", encoding="utf-8") as f:
    ground_truth = json.load(f)

# Filter tasks where taskID starts with 'OV'
gemini_answers = [ans for ans in gemini_answers if ans.get("task_id", "").startswith("OV")]
ground_truth = {task["task_id"]: task for task in ground_truth if task.get("task_id", "").startswith("OV")}

# Extract first 'Yes'/'No' word from answer 
def find_yes_no(text):
    text = text.strip().lower()
    if "yes," in text:
        return "Yes"
    elif "no," in text:
        return "No"
    return None

results = []

# Iterate through all tasks
for gemini in gemini_answers:
    task_id = gemini["task_id"]
    if task_id not in ground_truth:
        continue

    gt_answer = ground_truth[task_id]["answer"]["answer"]

    gemini_main = gemini.get("answer", "")
    gemini_dates = gemini.get("answer_with_dates", "")

    main_first = find_yes_no(gemini_main)
    dates_first = find_yes_no(gemini_dates)

    # Check if answers are correct
    main_correct = main_first == gt_answer
    dates_correct = dates_first == gt_answer

    results.append({
        "task_id": task_id,
        "expected_answer": gt_answer,
        "gemini_main_first_word": main_first,
        "gemini_with_dates_first_word": dates_first,
        "answer_correct": main_correct,
        "answer_with_dates_correct": dates_correct,
        "gemini_answer_snippet": gemini_main[:200],
        "gemini_answer_with_dates_snippet": gemini_dates[:200]
    })

# Calculate accuracy scores
main_correct_total = sum(1 for r in results if r["answer_correct"])
dates_correct_total = sum(1 for r in results if r["answer_with_dates_correct"])
total = len(results)

# Print results
print(f"Correct 'answer': {main_correct_total} / {total}")
print(f"Correct 'answer_with_dates': {dates_correct_total} / {total}")
print("Results saved to 'gemini_ov_responses.json'")

# Save results in JSON format
with open("gemini_ov_responses.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
