# Constitutional AI Agent

> **"Critique thyself."**

---

## 🧠 Mental Model

### The Problem
RLHF (training on human preferences) is expensive and hard to scale.
Sometimes the model knows *what* is right, but needs a nudge.

### The Solution
**Constitutional AI (CAI)**.
Instead of human feedback, use **AI feedback**.
1.  **Generate**: Model produces a response (maybe bad).
2.  **Critique**: Model critiques its own response against a set of rules (The Constitution).
3.  **Refine**: Model rewrites the response.

### The Constitution (Principles)
*   *Please choose the response that is most helpful, honest, and harmless.*
*   *Please ensure the response effectively fosters a sense of safety.*

## 🛠️ Tech Stack
*   Process chaining (Generate -> Critique -> Revise).
*   Mock LLM (Simulating the refinement process).
