# Vector Database (RAG)

> **Store concepts, not keywords.**

---

## 🧠 Mental Model

### The Problem
SQL databases search for exact matches (`WHERE name = 'cat'`).
Humans search for meaning (`"furry pet"`).
We need to store data as **vectors** (lists of floats, e.g., `[0.1, 0.9, -0.2]`).

### The Solution
**Vector Store**.
1.  **Embed**: Convert text to vector using a model (e.g., Ada-002).
2.  **Store**: Save `{"id": 1, "vector": [...], "text": "Cat is a pet"}`.
3.  **Query**: Find vectors closest to the query vector using **Cosine Similarity**.

### When to use this
*   [x] Semantic Search (RAG).
*   [x] Recommendation Systems.
*   [x] Long-term Memory for agents.

---

## 🏗️ Architecture

```mermaid
graph LR
    User -->|Query: 'Pet'| EmbeddingModel
    EmbeddingModel -->|Vector: [0.2, 0.8]| DB
    DB -->|Similarity Search| Result['Cat']
```

## ⚠️ Risks & Ethics

See [ETHICS.md](ETHICS.md).
- **Hallucinations**: RAG reduces but doesn't eliminate hallucinations.
- **Privacy**: Be careful when storing sensitive data in embeddings (inversion attacks are rare capable).
