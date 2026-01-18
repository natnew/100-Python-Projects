# Priority Queue Pattern

> **VIPs go first.**

---

## 🧠 Mental Model

### The Problem
Task A ("Reset Password") takes 1 second.
Task B ("Generate Monthly Report") takes 1 hour.
If B is ahead of A in the queue, the user waits 1 hour to reset their password.
Round-Robin helps, but sometimes urgency matters more than fairness.

### The Solution
**Priority Queue**.
1.  **Tag**: Every task gets a priority (High, Medium, Low).
2.  **Heap**: The queue respects the priority order, not insertion order.
3.  **Pop**: Always return the highest priority item.

### When to use this
*   [x] Customer Support (Premium vs Free users).
*   [x] Emergency Alerts (Fire alarm overrides background music).
*   [x] Interactive vs Batch workloads.

---

## 🏗️ Architecture

```mermaid
graph TD
    Incoming -->|Critical| Heap
    Incoming -->|Low| Heap
    Heap -->|Pop Max| Agent
    
    subgraph Heap
    1: Critical
    2: Critical
    3: High
    4: Low
    end
```

## ⚠️ Risks & Ethics

See [ETHICS.md](ETHICS.md).
- **Starvation**: If high-priority tasks keep arriving, low-priority tasks never run. (Solution: Priority Aging).
