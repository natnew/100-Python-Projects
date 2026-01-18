# Standardized Agent Protocol (ACL)

> **A common language for agents to communicate intent, not just data.**

---

## 🧠 Mental Model

### The Problem
If Agent A sends `{"cmd": "delete"}` and Agent B expects `{"action": "delete"}`, they can't talk.
Ad-hoc JSON schemas lead to a "Tower of Babel."
We need a standard *envelope* that describes **Intent** (Performative) separate from **Content**.

### The Solution
**FIPA-ACL (Simplified)**.
An industry standard for agent communication.
1.  **Performative**: What is this message doing?
    *   `REQUEST`: "Please do X."
    *   `INFORM`: "The answer is X."
    *   `REFUSE`: "I won't do X."
    *   `NOT_UNDERSTOOD`: "What is X?"
2.  **Content**: The actual data.
3.  **Ontology**: The glossary used in the content.

### When to use this
*   [x] Large ecosystems of heterogeneous agents.
*   [x] Negotiation protocols (Contract Net).

---

## 🏗️ Architecture

```mermaid
graph TD
    Sender -->|Envelope| Receiver
    
    subgraph Envelope
    Performative: REQUEST
    Language: JSON
    Ontology: Banking
    Content: {account: 123}
    end
```

## ⚠️ Risks & Ethics

See [ETHICS.md](ETHICS.md).
- **Overhead**: The envelope is verbose.
- **Strictness**: Strict adherence to standards slows down rapid prototyping.
