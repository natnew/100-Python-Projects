# Data Lineage Tracker Agent

> **"Follow the crumb trail."**

---

## 🧠 Mental Model

### The Problem
"Why did the model say X?"
Maybe it was trained on "Dataset Y", which included "File Z".
Without lineage, you can't trace errors back to the source.

### The Solution
A **Provenance Graph**.
Every time data is transformed, we record a "Lineage Event".
*   `Source` -> `Transformation` -> `Output`.

### Architecture
1.  **Tracker**: Captures events (Inputs, Process, Outputs).
2.  **GraphBuilder**: Constructs a Directed Acyclic Graph (DAG).
3.  **Visualizer**: Exports to DOT/Mermaid.

## 🛠️ Tech Stack
*   `networkx` (Graph data structure).
*   `uuid` (Unique IDs for artifacts).
