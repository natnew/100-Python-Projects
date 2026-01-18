# Performance Profiler Agent

> **"Premature optimization is the root of all evil (but ignoring latency is worse)."**

---

## 🧠 Mental Model

### The Problem
Your agent is slow. Why?
Is it the LLM call? The database query? Or a terribly inefficient loop in your Python code?
Guessing is dangerous. Measuring is engineering.

### The Solution
A **Profiler Agent**.
It wraps your code execution and reports exactly where time is spent.
It uses Python's built-in `cProfile` to inspect function call cost.

### Key Metrics
1.  **ncalls**: Number of times a function was called.
2.  **tottime**: Total time spent *in* the function (excluding sub-calls).
3.  **cumtime**: Cumulative time (including sub-calls).

## 🛠️ Tech Stack
*   `cProfile`: C-extension for profiling.
*   `pstats`: Helper to format stats.
*   `functools`: For decorators.
