# Collaborative Canvas Agent

> **"Together we go far."**

---

## 🧠 Mental Model

### The Problem
Agent A writes code. Agent B writes tests.
If they overwrite each other's files, chaos ensues.
They need a **Shared State** that handles concurrent updates.

### The Solution
**Operational Transformation (OT)** / **CRDT** (simplified).
Instead of storing the *Text*, we store the *Operations* (Insert, Delete).
The "Canvas" applies these operations in order (or merges them).

### Architecture
1.  **State**: The current document text.
2.  **Operation**: `Insert(index, char)` or `Delete(index)`.
3.  **SyncEngine**: Receives Ops and applies them to State.

## 🛠️ Tech Stack
*   `threading` (Simulation of users).
*   `list` (Mutable sequence).
