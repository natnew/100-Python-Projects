# Intent Classification Agent

> **"The Traffic Cop of AI."**

---

## 🧠 Mental Model

### The Problem
You have 10 specialized agents (Math, Code, Medical).
User asks: "My stomach hurts."
You don't want the Math agent to answer.
You need a router.

### The Solution
A **Classifier**.
It analyzes the user's prompt and selects the best tool/agent.
*   "Solve 2+2" -> `MathAgent`.
*   "Write Python" -> `CodeAgent`.

### Architecture
1.  **Registry**: List of agents + Keywords/Embeddings.
2.  **Router**: `match(prompt) -> Agent`.
3.  **Dispatcher**: Invokes the selected agent.

## 🛠️ Tech Stack
*   `difflib` (Similarity matching for demo).
*   cosine similarity (if using embeddings).
