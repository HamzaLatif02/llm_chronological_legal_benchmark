import json

# Load GPT answers file
with open("/Users/apple/Desktop/uni/kings/project/test/gpt_answers.json", "r", encoding="utf-8") as f:
    gpt_answers = json.load(f)

# Load ground truth file
with open("/Users/apple/Desktop/uni/kings/project/tasks/timeline_tasks/contains_tasks_with_answers.json", "r", encoding="utf-8") as f:
    ground_truth = json.load(f)

# Filter tasks where taskID starts with 'CN'
gpt_answers = [ans for ans in gpt_answers if ans.get("task_id", "").startswith("CN")]
ground_truth = {task["task_id"]: task for task in ground_truth if task.get("task_id", "").startswith("CN")}

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
for gpt in gpt_answers:
    task_id = gpt["task_id"]
    if task_id not in ground_truth:
        continue

    expected = ground_truth[task_id]["answer"]["contains"].strip().lower()
    gpt_main = find_yes_no(gpt.get("answer", ""))
    gpt_dates = find_yes_no(gpt.get("answer_with_dates", ""))

    main_correct = gpt_main == expected
    dates_correct = gpt_dates == expected

    results.append({
        "task_id": task_id,
        "expected": expected,
        "found_in_answer": gpt_main,
        "found_in_answer_with_dates": gpt_dates,
        "correct_main": main_correct,
        "correct_with_dates": dates_correct,
        "gpt_text_snippet": gpt.get("answer", "")[:150]
    })

# Calculate accuracy scores
correct_main = sum(1 for r in results if r["correct_main"])
correct_dates = sum(1 for r in results if r["correct_with_dates"])
total = len(results)

# Print results
print(f"Correct in 'answer': {correct_main} / {total}")
print(f"Correct in 'answer_with_dates': {correct_dates} / {total}")
print("Results saved to 'gpt_cn_responses.json'")

# Save results in JSON format
with open("gpt_cn_responses.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
