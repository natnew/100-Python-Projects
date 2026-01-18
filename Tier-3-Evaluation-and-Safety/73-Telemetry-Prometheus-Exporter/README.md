# Telemetry Agent (Prometheus Exporter)

> **"If a tree falls in a forest and no one scrapes the metrics, did it happen?"**

---

## 🧠 Mental Model

### The Problem
Logs are great for stories.
Metrics are great for trends.
"The server is slow" is a log.
"Latency is 500ms (up from 100ms)" is a metric.

### The Solution
A **Telemetry Exporter**.
Instead of pushing data to a database, we **expose** it.
Systems like Prometheus "scrape" this data every 15s.

### The Protocol (OpenMetrics)
It's text based:
```text
# HELP agent_tasks_completed Total tasks finished
# TYPE agent_tasks_completed counter
agent_tasks_completed 42
```

## 🛠️ Tech Stack
*   `http.server` (Python Stdlib) - to serve the `/metrics` page.
*   `requests` (Optional, for simulation).
*   `threading` (to run server in background).
