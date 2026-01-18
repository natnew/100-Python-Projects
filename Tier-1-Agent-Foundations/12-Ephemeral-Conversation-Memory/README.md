# Ephemeral Conversation Memory

> **A standard interface for managing session-based conversation history.**

---

## 🧠 Mental Model

### The Problem
Raw Python lists (`[]`) are messy for chat history.
*   No standard way to add `User` vs `AI` messages.
*   No easy way to serialize to JSON or dictionaries for API calls.
*   Hard to attach metadata (timestamps, token counts).

### The Solution
A clean `ChatMessageHistory` class.
1.  **Typed Methods**: `add_user_message()`, `add_ai_message()`.
2.  **Serialization**: `to_dict()` for API payloads.
3.  **In-Memory**: Fast, transient storage for the lifetime of the process.

### When to use this
*   [x] Short-lived sessions (Customer support chat).
*   [x] The "Active Memory" component of a larger system.

---

## 🏗️ Architecture

```mermaid
graph TD
    User -->|Message| History
    Agent -->|Response| History
    History -->|Format| List[List[Dict]]
    List --> LLM
```

## ⚠️ Risks & Ethics

See [ETHICS.md](ETHICS.md).
- **Data Loss**: Stored in RAM. Lost on restart.
- **Privacy**: Be careful when logging the entire history object to disk/console.
