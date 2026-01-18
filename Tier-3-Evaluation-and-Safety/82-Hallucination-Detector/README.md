# Hallucination Detector Agent

> **"Trust, but verify."**

---

## 🧠 Mental Model

### The Problem
LLMs make things up.
"Who is the CEO of Google?" -> "Sundar Pichai" (Correct).
"Who is the CEO of some_fake_company?" -> "John Doe" (Hallucination).

### The Solution
**Self-Consistency Evaluation**.
If you ask the same question 5 times with high temperature:
*   If the model is confident (Fact), it answers mostly the same way.
*   If the model is hallucinating, the answers will diverge violently.

### Architecture
1.  **Sampler**: Generate $N$ samples ($T=0.7$).
2.  **Cluster**: Group similar answers.
3.  **Entropy Check**: Calculate consistency score.

## 🛠️ Tech Stack
*   `SequenceMatcher` (difflib) for string similarity.
*   Mock LLM.
