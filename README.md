# Legal Benchmark for Chronological Understanding in Large Language Models

This repository contains the **first benchmark** dedicated to evaluating Large Language Models’ (LLMs) ability to understand and reason about **temporal information** in **legal texts**.  
The benchmark focuses on **UK primary/secondary legislation** and the **General Data Protection Regulation (GDPR)**.

---

## Overview

LLMs excel at many NLP tasks, but their ability to handle **time-based reasoning** in legal contexts is largely unexplored.  
Temporal reasoning is essential in law: determining *what law applied at a given time*, *how it changed*, and *why*.  
Errors in this reasoning can lead to **serious legal misinterpretations**.

This benchmark evaluates 6 popular LLMs on 12 temporal reasoning tasks spanning:
- **Semantic reasoning**
- **Numerical date reasoning**
- **Timeline reasoning**

---

## Features

- **Custom Legal Dataset**  
  - UK legislation changes from **1700–2025**  
  - GDPR articles and recitals  
  - Temporal links (amends, repeals, updates)  
  - Manually validated amendment chains

- **12 Temporal Reasoning Tasks**  
  - **Semantic:** chronological order, GDPR recitals, relationship chain, linking terms  
  - **Numerical:** date comparison, same date enactment, duration between laws  
  - **Timeline:** contains, during, overlap, overlapped-by

- **1,900+ Examples**  
  - Prompts **with** and **without explicit dates** for controlled evaluation  
  - JSON schema for flexible processing

- **Evaluation Pipeline**  
  - Benchmarks **GPT-4, Claude, Gemini, Mistral, Llama, Qwen**  
  - Visual analysis scripts and baseline results


