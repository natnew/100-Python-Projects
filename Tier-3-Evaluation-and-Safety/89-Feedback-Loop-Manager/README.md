# Feedback Loop Manager Agent

> **"Feedback is the breakfast of champions."**

---

## 🧠 Mental Model

### The Problem
You deploy an agent. It fails 10% of the time.
But you don't know *which* 10% unless users tell you.
Without a feedback loop, improvement is blind.

### The Solution
A **Feedback Collector**.
*   **Explicit**: User clicks "👍" or "👎".
*   **Implicit**: User re-rolls or stops using the tool.
*   **Metrics**: CSAT (Customer Satisfaction) / NPS (Net Promoter Score).

### Architecture
1.  **Interaction**: Agent generates response.
2.  **Collection**: User submits rating (1-5).
3.  **Aggregation**: Calculate scores.
4.  **Action**: Flag low-scoring prompts for review (Human-in-the-Loop).

## 🛠️ Tech Stack
*   `statistics` (Mean/Median).
*   `sqlite3` (Optional - simulated here with In-Memory list).
