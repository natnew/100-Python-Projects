# Adversarial Example Generator Agent

> **"A chain is only as strong as its weakest link."**

---

## 🧠 Mental Model

### The Problem
AI models are fragile.
Changing one pixel in an image can turn a "Panda" into a "Gibbon".
In NLP, adding invisible characters or swapping letters can bypass filters.

### The Solution
An **Adversarial Generator**.
It takes a valid input and applies perturbations to create an "Adversarial Example".
We test if the model (classifier/agent) is fooled.

### Techniques
1.  **Homoglyphs**: `password` -> `p@ssword` or `massacre` -> `mаssacre` (Cyrillic 'a').
2.  **Noise Injection**: Adding random chars.
3.  **Typos**: Swapping adjacent chars.

## 🛠️ Tech Stack
*   `random` (Simulation).
*   String manipulation.
