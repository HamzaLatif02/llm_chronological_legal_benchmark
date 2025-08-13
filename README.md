# Legal Benchmark for Chronological Understanding in Large Language Models

This repository contains the code, datasets, and evaluation framework for my MSc Data Science final project **"Legal Benchmark for Chronological Understanding in Large Language Models"**.

The project introduces a **12-task benchmark** designed to evaluate the temporal reasoning capabilities of large language models (LLMs) using UK legislation and the GDPR.  
The benchmark tests **semantic, numerical, and timeline-based reasoning**, with and without explicit date information.

---

## Project Overview

### Objectives
- Build a **custom legal database** from UK and GDPR legislation.
- Create **12 diverse task types** to assess temporal reasoning.
- Benchmark **6 LLMs**: GPT-4, Claude, Gemini, Mistral, Llama, and Qwen.
- Analyse results with **custom evaluation scripts** and **Tableau visualisations**.

### Data Sources
- **GDPR** – Extracted from [gdpr-info.eu](https://gdpr-info.eu)
- **UK Public General Acts (UKPGA)** – From [Legislation.gov.uk](https://www.legislation.gov.uk)
- **Primary & Secondary Legislation** – From [Legislation.gov.uk](https://www.legislation.gov.uk)
- **Legislation Changes** – From [Legislation.gov.uk/Changes](https://www.legislation.gov.uk/changes)

---

## Dataset
The dataset, in JSON format, is publicly available on [Kaggle](https://www.kaggle.com/datasets/hamza49/uk-legislations/data)

---

## Folder Structure
project_root/

1. database/ # Python scripts for building the legal database
  - temporal_relationships/ # Scripts for linking laws and creating timelines
  - *.py,

2. tasks/ # Scripts to generate 12 task types + generated task files
  - semantic_tasks/
  - numerical_tasks/
  - timeline_tasks/

3. test/ # Scripts to generate LLM answers + response JSONs

4. results/ # Evaluation scripts & visualisations
  - visualisation/ # Tableau project + visualisation images
  - compare_all_results.py

5. README.md

---

## Execution Order

### **Database Creation**
Run the following scripts in `database/`:
1. `Collect_gdpr.py`
2. `Collect_ukpga.py`
3. `Collect_primary_legislation.py`
4. `Join_primary_legislations.py`
5. `Collect_secondary_legislation.py`
6. `Combine_legal_documents.py`
7. `temporal_relationships/create_temporal_relationships.py`
8. `temporal_relationships/create_linking_terms.py`
9. `temporal_relationships/find_titles_in_links.py`
10. Manually update `matched_contexts_with_title.json`
11. `collect_changes_legislation.py`
12. `colelct_changes_legislation_updated.py`
13. `count_distinct_type_changes.py`
14. `create_legislation_timeline.py`

---

### **Task Generation**
Inside `tasks/`:
- **Semantic tasks** – 5 scripts
- **Numerical tasks** – 3 scripts
- **Timeline tasks** – 4 scripts  
Each task is stored in:
- `*_no_answers.json` (for model testing)
- `*_with_answers.json` (for evaluation)

Scripts can be run in any order.

---

### **Model Testing**
Inside `test/`:
- 6 scripts (one per LLM) to generate answers.
- Requires API keys for:
  - OpenAI (`OPENAI_API_KEY`)
  - Anthropic (`ANTHROPIC_API_KEY`)
  - Google Gemini (`GEMINI_API_KEY`)
  - Together.ai (`TOGETHER_API_KEY`)

Create a `.env` file in the root directory:
- OPENAI_API_KEY=your_key_here
- ANTHROPIC_API_KEY=your_key_here
- GEMINI_API_KEY=your_key_here
- TOGETHER_API_KEY=your_key_here

---

### **Evaluation**
Inside `results/`:
- Run evaluation scripts for each LLM and category.
- `compare_all_results.py` to generate a consolidated Excel table.
- Visualisations available in `results/visualisation/` (Tableau project & images).

---

## Visualisations
The results are presented in **6 key charts**, one for each research question, covering:
1. Effect of date inclusion on performance.
2. Category-wise performance comparison.
3. Chronological ordering accuracy.
4. Semantic reasoning performance.
5. Numerical reasoning accuracy.
6. Timeline reasoning performance.

---

## Key Findings
- GPT-4 was the most consistent but still struggled with complex legal timelines.
- Prompt wording significantly affected results.
- No LLM was perfect across all 12 tasks.
- Timeline-based reasoning remains the hardest challenge.

---

## Future Work
- Extend benchmark to EU and US legislation.
- Investigate **domain-specific fine-tuning** and **retrieval-augmented generation**.
- Explore the effect of **prompt structure** on performance.

---

## License
All code is released under the **MIT License**.  
Data from legislation sources is covered by the **Open Government Licence (OGL)**.

---

## Author
**Hamza Latif**  
MSc Data Science, King’s College London  
Supervised by Dr. Albert Merono-Peñuela
