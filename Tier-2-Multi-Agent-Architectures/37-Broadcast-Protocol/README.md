# Broadcast Protocol

> **Send a message to everyone and track who received it.**

---

## 🧠 Mental Model

### The Problem
Simple Pub/Sub (Project 36) is "Fire and Forget."
Sometimes you need to ensure **Total Coverage**.
"Emergency Stop": All agents must stop immediately.
"Roll Call": All agents must report their status.

### The Solution
**Broadcast with ACKs**.
1.  **Broadcast**: Send to a special `*` channel or iterate all known agents.
2.  **Ack Request**: Message includes `reply_required=True` and a `correlation_id`.
3.  **Tracker**: The sender waits for N acknowledgments within T seconds.

### When to use this
*   [x] System shutdown triggers.
*   [x] Leader election (Who is alive?).
*   [x] Configuration updates (Update API Key for everyone).

---

## 🏗️ Architecture

```mermaid
sequenceDiagram
    Controller->>+All: BROADCAST: "Pause Work" (ID: 101)
    AgentA-->>-Controller: ACK (ID: 101)
    AgentB-->>-Controller: ACK (ID: 101)
    Controller->>Controller: Count ACKs (2/2)
    Note right of Controller: Broadcast Complete
```

## ⚠️ Risks & Ethics

See [ETHICS.md](ETHICS.md).
- **Storms**: If 1,000 agents ACK at once, the controller gets flooded (Thundering Herd).
- **Timeouts**: What if Agent C is sleeping? The broadcast hangs? (Need timeouts).
