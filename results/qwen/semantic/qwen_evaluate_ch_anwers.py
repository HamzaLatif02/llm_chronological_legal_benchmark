import json
import re

# Load Qwen answers file
with open("/Users/apple/Desktop/uni/kings/project/test/qwen_answers.json", "r", encoding="utf-8") as f:
    qwen_answers = json.load(f)

# Load ground truth file
with open("/Users/apple/Desktop/uni/kings/project/tasks/semantic_tasks/change_update_ordering_tasks_with_answers.json", "r", encoding="utf-8") as f:
    ground_truth = json.load(f)

# Filter tasks where taskID starts with 'CH'
qwen_answers = [ans for ans in qwen_answers if ans.get("task_id", "").startswith("CH")]
ground_truth = {task["task_id"]: task for task in ground_truth if task.get("task_id", "").startswith("CH")}

# Normalise text by converting to lowercase and 
# removing characters that are not lowercase letters and digits
def normalise(text):
    return re.sub(r"[^a-z0-9]+", "", text.lower())

# Check if all legislation titles are mentioned in the correct order in Qwen answer
def evaluate_qwen_text(qwen_text, gt_titles):
    short_titles = [title.split(" of")[0] for title in gt_titles]
    norm_short_titles = [normalise(title) for title in short_titles]
    qwen_text_norm = normalise(qwen_text)

    qwen_order = []
    for idx, short_title in enumerate(norm_short_titles):
        match = re.search(short_title, qwen_text_norm)
        if match:
            qwen_order.append((idx, match.start()))
        else:
            qwen_order.append((idx, float("inf")))

    order_in_qwen = [idx for idx, _ in sorted(qwen_order, key=lambda x: x[1])]
    correct_order = order_in_qwen == list(range(len(gt_titles)))
    found_all = all(x[1] != float("inf") for x in qwen_order)

    return {
        "correct_titles_found": found_all,
        "correct_order": correct_order,
        "overall_correct": found_all and correct_order,
        "order_in_qwen": order_in_qwen,
        "qwen_text_snippet": qwen_text[:300]
    }

results = []

# Iterate through all tasks
for ans in qwen_answers:
    task_id = ans["task_id"]
    qwen_main = ans.get("answer", "")
    qwen_dates = ans.get("answer_with_dates", "")

    if task_id not in ground_truth:
        continue

    gt_titles = [entry["title"] for entry in ground_truth[task_id]["answer"]]

    main_result = evaluate_qwen_text(qwen_main, gt_titles)
    dates_result = evaluate_qwen_text(qwen_dates, gt_titles)

    results.append({
        "task_id": task_id,
        "expected_titles": gt_titles,
        "main_answer": main_result,
        "answer_with_dates": dates_result
    })

# Calculate accuracy scores
correct_main = sum(1 for r in results if r["main_answer"]["overall_correct"])
correct_dates = sum(1 for r in results if r["answer_with_dates"]["overall_correct"])
total = len(results)

# Print results
print(f"Qwen 'answer' correct: {correct_main} / {total}")
print(f"Qwen 'answer_with_dates' correct: {correct_dates} / {total}")
print("Results saved to qwen_ch_responses.json")

# Save results in JSON format
with open("qwen_ch_responses.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
