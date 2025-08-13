import json
import re

# Load Llama answers file
with open("/Users/apple/Desktop/uni/kings/project/test/llama_answers.json", "r", encoding="utf-8") as f:
    llama_answers = json.load(f)

# Load ground truth file
with open("/Users/apple/Desktop/uni/kings/project/tasks/numerical_tasks/duration_between_tasks_with_answers.json", "r", encoding="utf-8") as f:
    ground_truth = json.load(f)

# Filter tasks where taskID starts with 'DB'
llama_answers = [ans for ans in llama_answers if ans.get("task_id", "").startswith("DB")]
ground_truth = {task["task_id"]: task for task in ground_truth if task.get("task_id", "").startswith("DB")}

# Normalise text by converting to lowercase and 
# replacing 'and' with space, removing punctuation, and collapsing whitespaces
def normalise(text):
    text = text.lower()
    text = text.replace(" and ", " ")
    text = re.sub(r"[^\w\s]", "", text)
    return re.sub(r"\s+", " ", text).strip()

results = []

# Iterate through all tasks
for llama in llama_answers:
    task_id = llama["task_id"]
    if task_id not in ground_truth:
        continue

    gt_duration = normalise(ground_truth[task_id]["answer"])
    llama_main = normalise(llama.get("answer", ""))
    llama_dates = normalise(llama.get("answer_with_dates", ""))

    # Check if duration is found in LLama answer
    found_in_main = gt_duration in llama_main
    found_in_dates = gt_duration in llama_dates

    results.append({
        "task_id": task_id,
        "expected_duration": ground_truth[task_id]["answer"],
        "answer_correct": found_in_main,
        "answer_with_dates_correct": found_in_dates,
        "llama_answer_snippet": llama.get("answer", "")[:200],
        "llama_answer_with_dates_snippet": llama.get("answer_with_dates", "")[:200]
    })

# Calculate accuracy scores
main_correct = sum(1 for r in results if r["answer_correct"])
dates_correct = sum(1 for r in results if r["answer_with_dates_correct"])
total = len(results)

# Print results
print(f"Duration found in 'answer': {main_correct} / {total}")
print(f"Duration found in 'answer_with_dates': {dates_correct} / {total}")
print("Results saved to 'llama_db_responses.json'")

# Save results in JSON format
with open("llama_db_responses.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)
