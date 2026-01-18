# Cloud Cost Estimator Agent

> **"The cloud is just someone else's computer, and they charge rent."**

---

## 🧠 Mental Model

### The Problem
AI calls are cheap individually ($0.03).
But 10,000 calls a day adds up ($300).
A runaway loop can bankrupt a startup in hours.

### The Solution
A **Cost Estimator & Budget Enforcer**.
It tracks "Token Usage" (Prompt + Completion).
It applies unit prices (Model Cards).
It enforces budgets ("Stop if daily > $50").

### Key Concepts
1.  **Token Counting**: 1000 tokens ~= 750 words.
2.  **Pricing Models**: Input tokens are usually cheaper than output tokens.
3.  **Accumulators**: Rolling daily/monthly totals.

## 🛠️ Tech Stack
*   `dataclasses` (Configuration).
*   `decimal` (Handling currency floating point errors).
