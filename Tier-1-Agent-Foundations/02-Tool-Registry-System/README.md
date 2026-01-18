# Tool Registry System

> **A dynamic registry that manages tool lifecycles, permissions, and schema generation.**

---

## 🧠 Mental Model

### The Problem
Agents need to know what tools are available, how to call them, and whether they are allowed to use them. Hardcoding tool lists is brittle.
LLMs also need schemas (JSON Schema) to understand tools, which are tedious to write manually.

### The Solution
A central `ToolRegistry` that:
1.  **Registers** Python functions using a simple decorator.
2.  **Introspects** type hints and docstrings to auto-generate OpenAI-compatible schemas.
3.  **Executes** validated tool calls.
4.  **Manages** lifecycle (experimental, deprecated) and permissions.

### When to use this
*   [x] Building a generic agent that can hold many tools.
*   [x] Exposing a dynamic set of plugins to an LLM.

---

## 🏗️ Architecture

```mermaid
graph TD
    Func[Python Function] -->|@register| Registry
    Registry -->|to_openai_tools()| LLM[LLM System Prompt]
    LLM -->|Tool Call| Router
    Router -->|execute()| Registry
    Registry -->|Return Value| LLM
```

## ⚠️ Risks & Ethics

See [ETHICS.md](ETHICS.md).
- **Execution Sandbox**: This registry executes code. Ensure tools are safe.
- **Permission Escalation**: Can an agent confuse the registry to execute a restricted tool?
