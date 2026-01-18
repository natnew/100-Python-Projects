# Carbon Footprint Tracker Agent

> **"There is no Planet B."**

---

## 🧠 Mental Model

### The Problem
Training GPT-3 consumed 1,287 MWh (same as 120 US homes for a year).
Inference also burns energy.
Developers need visibility into the environmental impact of their agents.

### The Solution
A **Sustainability Monitor**.
It tracks compute usage (GPU/CPU time) and converts it to $CO_2e$ (Carbon Dioxide Equivalent).
Formula: $Energy (kWh) \times Carbon Intensity (g/kWh) = CO_2e$.

### Architecture
1.  **Monitor**: Track process runtime and hardware power draw (TDP).
2.  **Calculator**: Apply regional carbon intensity factors (e.g., Virginia (high coal) vs Montreal (hydro)).
3.  **Report**: Emit "Green Metrics".

## 🛠️ Tech Stack
*   `Math` (Conversion logic).
*   `dataclasses` (Hardware specs).
