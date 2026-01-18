# Mock Server

> **Simulate LLM APIs for fast, free, and deterministic testing.**

---

## 🧠 Mental Model

### The Problem
Running `pytest` against GPT-4 is:
1.  **Expensive**: $$$ for every test run.
2.  **Slow**: 1-5 seconds per test.
3.  **Flaky**: Network errors or varied outputs break assertions.

### The Solution
**Local Mock Server**.
A lightweight HTTP server that:
1.  Listens on `localhost:8000`.
2.  Accepts `/v1/chat/completions` (OpenAI format).
3.  Returns hardcoded JSON responses depending on the input prompt.

### When to use this
*   [x] CI/CD pipelines.
*   [x] Offline development.

---

## 🏗️ Architecture

```mermaid
graph LR
    Agent -->|POST /v1/chat| Localhost[Mock Server]
    Localhost -->|Match Rules| Response[JSON]
    Response --> Agent
```

## ⚠️ Risks & Ethics

See [ETHICS.md](ETHICS.md).
- **Drift**: If OpenAI changes their API schema, your mock might become outdated.
- **Overconfidence**: Tests pass on mock, but fail on real model (e.g., real model refuses prompt).
