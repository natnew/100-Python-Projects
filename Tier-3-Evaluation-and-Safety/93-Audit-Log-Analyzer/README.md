# Audit Log Analyzer Agent

> **"Who watches the watchers?"**

---

## 🧠 Mental Model

### The Problem
An agent deleted a file.
Was it a bug? A hack? Or a legitimate user action?
Without logs, you are guessing.

### The Solution
A **Forensic Analyzer**.
It parses structured logs (`JSON`) to reconstruct a timeline of events.
It flags "Suspicious Sequences" (e.g., 50 logins in 1 minute).

### Architecture
1.  **Ingest**: Read log file.
2.  **Parse**: Extract `timestamp`, `actor`, `action`, `resource`.
3.  **Detect**: Run rules (e.g., Velocity Checks).

## 🛠️ Tech Stack
*   `json` (Structured Logs).
*   `dateutil` (Time delta calculations).
