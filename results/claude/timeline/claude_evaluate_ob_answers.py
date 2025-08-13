import json
import re

# Load Claude answers file
with open("/Users/apple/Desktop/uni/kings/project/test/claude_answers.json", "r", encoding="utf-8") as f:
    claude_answers = json.load(f)

# Load ground truth file
with open("/Users/apple/Desktop/uni/kings/project/tasks/timeline_tasks/overlapped_by_tasks_with_answers.json", "r", encoding="utf-8") as f:
    ground_truth = json.load(f)

# Filter tasks where taskID starts with 'OB'
claude_answers = [ans for ans in claude_answers if ans.get("task_id", "").startswith("OB")]
ground_truth = {task["task_id"]: task for task in ground_truth if task.get("task_id", "").startswith("OB")}

# Find 'overlap' direction of answer
def infer_overlap_answer(text):
    text = text.lower()
    
    # Normalise common overlapping phrases
    text = text.replace("do not overlap", "don't overlap")
    text = text.replace("does not overlap", "doesn't overlap")
    text = text.replace("did not overlap", "didn't overlap")

    if re.search(r"\bno,\b", text) or "not overlapped" in text or "doesn't overlap" in text or "don't overlap" in text or "didn't overlap" in text or "no overlap" in text:
        return "no"
    if re.search(r"\byes,\b", text) or "overlapped" in text or "do overlap" in text or "overlap" in text:
        return "yes"
    
    return None

results = []

# Iterate through all tasks
for ans in claude_answers:
    task_id = ans["task_id"]
    if task_id not in ground_truth:
        continue

    expected = ground_truth[task_id]["answer"]["overlapped_by"].strip().lower()
    
    claude_main_raw = ans.get("answer", "")
    claude_dates_raw = ans.get("answer_with_dates", "")

    claude_main = infer_overlap_answer(claude_main_raw)
    claude_dates = infer_overlap_answer(claude_dates_raw)

    result = {
        "task_id": task_id,
        "expected_overlapped_by": expected,
        "claude_answer_inferred": claude_main,
        "claude_with_dates_inferred": claude_dates,
        "correct_main": claude_main == expected,
        "correct_with_dates": claude_dates == expected,
        "claude_main_snippet": claude_main_raw[:300],
        "claude_with_dates_snippet": claude_dates_raw[:300]
    }

    results.append(result)

# Calculate accuracy scores
correct_main = sum(1 for r in results if r["correct_main"])
correct_dates = sum(1 for r in results if r["correct_with_dates"])
total = len(results)

# Print results
print(f"Correct in 'answer': {correct_main} / {total}")
print(f"Correct in 'answer_with_dates': {correct_dates} / {total}")
print("Results saved to 'claude_ob_responses.json'")

# Save results in JSON format
with open("claude_ob_responses.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
