# Coding Agent

> **An agent that writes, tests, and fixes code iteratively.**

---

## 🧠 Mental Model

### The Problem
LLMs write buggy code.
"Copy-paste this into your terminal" is bad UX.
We need an agent that *owns* the code lifecycle.

### The Solution
**The Coder Loop**.
1.  **Write**: Generates Python code.
2.  **Lint**: Checks for syntax errors (simulated `pylint`).
3.  **Execute**: Runs the code in a sandbox (mocked).
4.  **Fix**: If stderr is not empty, feed the error back to the LLM and retry.

### When to use this
*   [x] Automated scripts (e.g., "Rename all .jpg files").
*   [x] Data Analysis/Notebooks.
*   [x] Fixing simple bugs in a repo.

---

## 🏗️ Architecture

```mermaid
graph TD
    User -->|Req: Factorial(5)| Coder
    Coder -->|Draft v1| Sandbox[Execution Env]
    Sandbox -->|Error: Indentation| Coder
    Coder -->|Draft v2| Sandbox
    Sandbox -->|Success: 120| Coder
    Coder -->|Final Result| User
```

## ⚠️ Risks & Ethics

See [ETHICS.md](ETHICS.md).
- **Infinite Loops**: The agent might keep retrying the same fix forever.
- **Security**: Running arbitrary LLM code is dangerous. **ALWAYS** use a container/sandbox in production.
