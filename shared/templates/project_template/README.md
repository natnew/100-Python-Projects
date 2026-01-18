# [Project Name]

> **One-sentence summary of the pattern.** e.g., "A structured validation layer that coerces LLM outputs into Pydantic models."

---

## 🧠 Mental Model

### The Problem
Describe the specific challenge this pattern addresses.
*Example: LLMs are nondeterministic text generators, but software systems need structured data. Regex parsing is brittle.*

### The Solution
Explain the architectural approach.
*Example: We use a multi-stage parser that attempts zero-shot validation first, then falls back to a "repair" prompt if schema validation fails.*

### When to use this
*   [ ] Condition A
*   [ ] Condition B

---

## 🏗️ Architecture

See [DESIGN.md](DESIGN.md) for detailed tradeoffs and diagrams.

## ⚠️ Risks & Ethics

See [ETHICS.md](ETHICS.md) for failure modes and safety considerations.

---

## 🚀 Quick Start

### Installation

```bash
poetry install
```

### Usage

```python
from src.main import run_pattern

result = run_pattern(input_data="...")
print(result)
```

### Running Evals

```bash
python evals/eval_basic.py
```
