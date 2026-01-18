# Model Card Generator Agent

> **"Read the label."**

---

## 🧠 Mental Model

### The Problem
Who built this model? What data was it trained on? What are its limitations?
If you can't answer these, you shouldn't ship it.

### The Solution
**Model Cards** (Google) / **System Cards** (Meta).
A standardized document describing the model's provenance, usage, and risks.
This agent automates the generation of these markdown files from configuration.

### Architecture
1.  **Metadata Input**: JSON spec (Author, License, Metrics).
2.  **Template Engine**: Jinja2 (or f-strings) to render `MODEL_CARD.md`.
3.  **Publisher**: Save to repo.

## 🛠️ Tech Stack
*   `json`
*   `dataclasses`
