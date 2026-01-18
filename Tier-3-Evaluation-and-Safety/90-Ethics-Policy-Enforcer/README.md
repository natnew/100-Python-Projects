# Ethics Policy Enforcer Agent

> **"Code is law, but ethics is the spirit."**

---

## 🧠 Mental Model

### The Problem
Some actions are legal (`rm -rf /`) but unethical or against company policy.
LLMs don't have innate ethics; they have training probabilities.
You need a **Policy Engine**.

### The Solution
A **Rule-Based Enforcer** (Deterministic).
Unlike Constitutional AI (which uses LLM for critique), this uses hard logic for critical corporate policies.
*   *Policy*: "No financial advice."
*   *Policy*: "No medical diagnosis."
*   *Policy*: "No political endorsement."

### Architecture
1.  **Input**: Agent Intent.
2.  **Policy Store**: JSON/YAML rules.
3.  **Engine**: Match(Intent, Rules).
4.  **Verdict**: Allow/Deny + Explanation.

## 🛠️ Tech Stack
*   `json` (Policies).
*   `re` (Keyword matching).
