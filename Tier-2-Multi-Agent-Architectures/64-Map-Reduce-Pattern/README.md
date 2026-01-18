# Map-Reduce Pattern

> **Process big data by splitting it up.**

---

## 🧠 Mental Model

### The Problem
You have 10,000 text files. You want to count every word.
A single loop is too slow.
Loading everything into RAM crashes.

### The Solution
**Map-Reduce**.
1.  **Split**: Divide files into chunks.
2.  **Map**: Agents process chunks in parallel -> `(word, 1)`.
3.  **Shuffle**: Group by key -> `word: [1, 1, 1]`.
4.  **Reduce**: Sum up values -> `(word, 3)`.

### When to use this
*   [x] Log Analysis (Count error types).
*   [x] Search Indexing (Inverted Index).
*   [x] Distributing standard LLM tasks (Summarize 50 chapters, then summarize the summaries).

---

## 🏗️ Architecture

```mermaid
graph TD
    Input -->|Split| Chunk1
    Input -->|Split| Chunk2
    
    Chunk1 -->|Map| K1[(cat, 1)] & K2[(dog, 1)]
    Chunk2 -->|Map| K2_2[(dog, 1)] & K3[(bat, 1)]
    
    K1 -->|Shuffle| Reducer1
    K2 & K2_2 -->|Shuffle| Reducer2
    K3 -->|Shuffle| Reducer3
    
    Reducer1 -->|Sum| Out1[cat: 1]
    Reducer2 -->|Sum| Out2[dog: 2]
    Reducer3 -->|Sum| Out3[bat: 1]
```

## ⚠️ Risks & Ethics

See [ETHICS.md](ETHICS.md).
- **Stragglers**: If one Mapper is slow, the whole job waits.
- **Skew**: If "the" appears 1M times and "antigravity" 1 time, the Reducer for "the" will crash.
