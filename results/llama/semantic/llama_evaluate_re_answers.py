import json
import re

# Load Llama answers file
with open("/Users/apple/Desktop/uni/kings/project/test/llama_answers.json", "r", encoding="utf-8") as f:
    llama_data = json.load(f)

# Load ground truth file
with open("/Users/apple/Desktop/uni/kings/project/tasks/semantic_tasks/recital_to_article_tasks_with_answers.json", "r", encoding="utf-8") as f:
    ground_truth_data = json.load(f)

# Filter tasks where taskID starts with 'RE'
llama_data = [x for x in llama_data if x.get("task_id", "").startswith("RE")]
ground_truth = {x["task_id"]: x for x in ground_truth_data if x.get("task_id", "").startswith("RE")}

# Extract recitals mentioned in answer
def extract_recital_numbers(text):
    matches = re.findall(r"(?:Recital|recital)?\s*(\d{1,3})", text)
    return sorted(set(matches))

results = []

# Iterate through all tasks
for item in llama_data:
    task_id = item["task_id"]
    llama_text = item.get("answer", "")

    if task_id not in ground_truth:
        continue

    # Extract expected recital numbers
    gt_entry = ground_truth[task_id]["answer"]
    article_key = list(gt_entry.keys())[0]
    gt_recitals = [r["number"] for r in gt_entry[article_key]]

    llama_recitals = extract_recital_numbers(llama_text)

    # Check for correctness
    correct = sorted(gt_recitals) == sorted(llama_recitals)
    missing = sorted(set(gt_recitals) - set(llama_recitals))
    extra = sorted(set(llama_recitals) - set(gt_recitals))

    results.append({
        "task_id": task_id,
        "correct": correct,
        "llama_recitals": llama_recitals,
        "ground_truth_recitals": gt_recitals,
        "missing_recitals": missing,
        "extra_recitals": extra,
        "llama_text_snippet": llama_text[:300]
    })

# Calculate accuracy scores
correct_count = sum(1 for r in results if r["correct"])

# Print results
print(f"Correct answers: {correct_count} / {len(results)}")
print("Results saved to 'llama_re_responses.json'")

# Save results in JSON format
with open("llama_re_responses.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

