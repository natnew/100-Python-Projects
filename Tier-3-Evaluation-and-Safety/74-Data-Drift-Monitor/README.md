# Data Drift Monitor Agent

> **"The only constant is change, and change breaks models."**

---

## 🧠 Mental Model

### The Problem
You trained your AI on data from 2023.
It's now 2026. The world has changed.
The inputs are different (Drift). The outputs are wrong (Degradation).

### The Solution
A **Drift Monitor**.
It compares the *Reference Distribution* (Training Data) with the *Current Distribution* (Production Data).
If they diverge statistically, it raises an alarm.

### Techniques
1.  **Z-Score** (Simple): Has the mean shifted?
2.  **KS Test**: Has the shape of the distribution changed?
3.  **PSI (Population Stability Index)**: Industry standard for credit scoring drift.

## 🛠️ Tech Stack
*   `math` (Statistics).
*   `random` (Simulation).
