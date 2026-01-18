# Load Balancer Pattern

> **Distribute traffic to the best available server.**

---

## 🧠 Mental Model

### The Problem
Server A is powerful (8 cores).
Server B is weak (1 core).
If we send 50% of traffic to each, Server B dies.
Also, if Server A crashes, we must stop sending requests there.

### The Solution
**Load Balancer**.
1.  **Health Checks**: Ping servers every 5s. Mark dead ones as "Down".
2.  **Strategy**:
    *   *Round Robin*: A, B, A, B.
    *   *Weighted*: A, A, A, B (3:1 ratio).
    *   *Least Connections*: Send to the one with fewest active requests.

### When to use this
*   [x] Scaling Web Services.
*   [x] LLM Inference (Route to Azure/AWS based on availability).
*   [x] Reliability (Failover).

---

## 🏗️ Architecture

```mermaid
graph LR
    User -->|Req| LB[Load Balancer]
    LB -->|Req| S1[Server A (Healthy)]
    LB -.->|Req| S2[Server B (Dead)]
    LB -->|Req| S3[Server C (Healthy)]
```

## ⚠️ Risks & Ethics

See [ETHICS.md](ETHICS.md).
- **SPOF**: The Load Balancer itself is a Single Point of Failure (Solution: DNS failover).
- **Session Stickiness**: If a user logs into Server A, but the next request goes to Server B, they might be logged out (Need shared session store, see Project 46).
