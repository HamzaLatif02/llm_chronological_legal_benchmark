import os
import json
import pandas as pd

# Define settings 
llm_names = ["gpt", "claude", "gemini", "llama", "mistral", "qwen"]
categories = {
    "numerical": ["co", "db", "ov"],
    "semantic": ["ch", "or", "rc", "re", "se"],
    "timeline": ["cn", "du", "ob", "ol"]
}
base_dir = "/Users/apple/Desktop/uni/kings/project/results"

# Custom parsing depending on task type 
def parse_file(file_path, category, prefix):
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        if not isinstance(data, list):
            return None

        main_correct = 0
        with_dates_correct = 0
        total = len(data)
        with_dates_exists = False

        for d in data:
            if category == "numerical":
                if "answer_correct" in d:
                    main_correct += bool(d["answer_correct"])
                if "answer_with_dates_correct" in d:
                    with_dates_exists = True
                    with_dates_correct += bool(d["answer_with_dates_correct"])

            elif category == "semantic":
                if prefix == "ch":
                    if "main_answer" in d and "overall_correct" in d["main_answer"]:
                        main_correct += bool(d["main_answer"]["overall_correct"])
                    if "answer_with_dates" in d and "overall_correct" in d["answer_with_dates"]:
                        with_dates_exists = True
                        with_dates_correct += bool(d["answer_with_dates"]["overall_correct"])
                elif prefix == "or":
                    if "answer" in d and "is_correct" in d["answer"]:
                        main_correct += bool(d["answer"]["is_correct"])
                    if "answer_with_dates" in d and "is_correct" in d["answer_with_dates"]:
                        with_dates_exists = True
                        with_dates_correct += bool(d["answer_with_dates"]["is_correct"])
                else:
                    if "correct" in d:
                        main_correct += bool(d["correct"])

            elif category == "timeline":
                if "correct_main" in d:
                    main_correct += bool(d["correct_main"])
                if "correct_with_dates" in d:
                    with_dates_exists = True
                    with_dates_correct += bool(d["correct_with_dates"])

        result = {
            "main_correct": main_correct,
            "with_dates_correct": with_dates_correct if with_dates_exists else None,
            "main_total": total,
            "with_dates_total": total if with_dates_exists else None
        }
        return result
    except Exception as e:
        return None

# Collect results 
records = []

for llm in llm_names:
    for category, prefixes in categories.items():
        for prefix in prefixes:
            file_name = f"{llm}_{prefix}_responses.json"
            file_path = os.path.join(base_dir, llm, category, file_name)

            parsed = parse_file(file_path, category, prefix)
            if parsed:
                # Compute accuracies, main and without dates 
                main_total = parsed["main_total"]
                with_dates_total = parsed["with_dates_total"]
                main_acc = (parsed["main_correct"] / main_total * 100) if main_total else None
                with_dates_acc = (parsed["with_dates_correct"] / with_dates_total * 100) if with_dates_total else None

                # Compute overall accuracy
                correct_vals = [v for v in [parsed["main_correct"], parsed["with_dates_correct"]] if v is not None]
                total_vals = [v for v in [main_total, with_dates_total] if v is not None]
                overall_correct = sum(correct_vals)
                overall_total = sum(total_vals)
                overall_acc = (overall_correct / overall_total * 100) if overall_total else None

                records.append({
                    "LLM": llm,
                    "Category": category,
                    "Task": prefix.upper(),
                    "Main Correct": parsed["main_correct"],
                    "Main Total": main_total,
                    "Main Accuracy (%)": round(main_acc, 2) if main_acc is not None else None,
                    "With Dates Correct": parsed["with_dates_correct"],
                    "With Dates Total": with_dates_total,
                    "With Dates Accuracy (%)": round(with_dates_acc, 2) if with_dates_acc is not None else None,
                    "Overall Correct": overall_correct,
                    "Overall Total": overall_total,
                    "Overall Accuracy (%)": round(overall_acc, 2) if overall_acc is not None else None
                })

# Save to Excel 
df = pd.DataFrame(records)
output_path = "/Users/apple/Desktop/uni/kings/project/results/llm_accuracy_summary_full.xlsx"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
df.to_excel(output_path, index=False)

print(f"Excel saved to: {output_path}")
