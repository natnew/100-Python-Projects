# Agent Worker Pool

> **Reuse agents to save startup costs.**

---

## 🧠 Mental Model

### The Problem
Initializing an agent might be expensive (loading large prompts, connecting to DBs).
Creating `new Agent()` for every single task is inefficient.
If 1000 tasks arrive, spawning 1000 agents crashes the system.

### The Solution
**Object Pool Pattern**.
1.  **Initialize**: Start a fixed number of agents (e.g., 5) at boot.
2.  **Acquire**: Client asks "Give me an agent."
3.  **Use**: Client uses the agent.
4.  **Release**: Client puts the agent back in the pool.

### When to use this
*   [x] High-throughput API backends.
*   [x] Limiting concurrency (Rate Limit handling).
*   [x] Managing heavy resources (Browser instances).

---

## 🏗️ Architecture

```mermaid
graph LR
    Client -->|Acquire| Pool
    Pool -->|Agent A| Client
    Client -->|Release| Pool
    
    subgraph PoolState
    Available: [B, C, D]
    Busy: [A]
    end
```

## ⚠️ Risks & Ethics

See [ETHICS.md](ETHICS.md).
- **State Leaks**: If Agent A remembers the previous user's credit card, and is given to the next user -> Privacy Disaster. **Always sanitize agents on release.**
- **Deadlocks**: If all agents are busy and the running agents need *another* agent to finish -> Gridlock.
