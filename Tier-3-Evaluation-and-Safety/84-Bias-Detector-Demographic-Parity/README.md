# Bias Detector Agent

> **"Equality means treating equal things equally."**

---

## 🧠 Mental Model

### The Problem
AI models contain biases from their training data.
They might associate "Doctor" with men and "Nurse" with women.
They might give lower credit scores to certain zip codes.

### The Solution
**Demographic Parity Testing**.
We replace sensitive attributes (names, pronouns) in the prompt and check if the output changes.
*   Prompt A: "John is a doctor..."
*   Prompt B: "Mary is a doctor..."
If the sentiment or classification flips, we have bias.

### Architecture
1.  **Template**: " [NAME] is a [PROFESSION]. They are... "
2.  **Permuter**: Insert ["John", "Mary", "Jamal", "Wei"].
3.  **Analyzer**: Compare outputs.

## 🛠️ Tech Stack
*   `textblob` (Sentiment Analysis) - or simple positive/negative words.
*   `itertools` (Permutations).
