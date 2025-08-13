import json
import re

# Load Claude answers file
with open("/Users/apple/Desktop/uni/kings/project/test/claude_answers.json", "r", encoding="utf-8") as f:
    claude_answers = json.load(f)

# Load ground truth file
with open("/Users/apple/Desktop/uni/kings/project/tasks/semantic_tasks/change_update_ordering_tasks_with_answers.json", "r", encoding="utf-8") as f:
    ground_truth = json.load(f)

# Filter tasks where taskID starts with 'CH'
claude_answers = [ans for ans in claude_answers if ans.get("task_id", "").startswith("CH")]
ground_truth = {task["task_id"]: task for task in ground_truth if task.get("task_id", "").startswith("CH")}

# Normalise text by converting to lowercase and 
# removing characters that are not lowercase letters and digits
def normalise(text):
    return re.sub(r"[^a-z0-9]+", "", text.lower())

# Check if all legislation titles are mentioned in the correct order in Claude answer
def evaluate_claude_text(claude_text, gt_titles):
    short_titles = [title.split(" of")[0] for title in gt_titles]
    norm_short_titles = [normalise(title) for title in short_titles]
    claude_text_norm = normalise(claude_text)

    claude_order = []
    for idx, short_title in enumerate(norm_short_titles):
        match = re.search(short_title, claude_text_norm)
        if match:
            claude_order.append((idx, match.start()))
        else:
            claude_order.append((idx, float("inf")))

    order_in_claude = [idx for idx, _ in sorted(claude_order, key=lambda x: x[1])]
    correct_order = order_in_claude == list(range(len(gt_titles)))
    found_all = all(x[1] != float("inf") for x in claude_order)

    return {
        "correct_titles_found": found_all,
        "correct_order": correct_order,
        "overall_correct": found_all and correct_order,
        "order_in_claude": order_in_claude,
        "claude_text_snippet": claude_text[:300]
    }

results = []

# Iterate through all tasks
for ans in claude_answers:
    task_id = ans["task_id"]
    claude_main = ans.get("answer", "")
    claude_dates = ans.get("answer_with_dates", "")

    if task_id not in ground_truth:
        continue

    gt_titles = [entry["title"] for entry in ground_truth[task_id]["answer"]]

    main_result = evaluate_claude_text(claude_main, gt_titles)
    dates_result = evaluate_claude_text(claude_dates, gt_titles)

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
print(f"Claude 'answer' correct: {correct_main} / {total}")
print(f"Claude 'answer_with_dates' correct: {correct_dates} / {total}")
print("Results saved to claude_ch_responses.json")

# Save results in JSON format
with open("claude_ch_responses.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
