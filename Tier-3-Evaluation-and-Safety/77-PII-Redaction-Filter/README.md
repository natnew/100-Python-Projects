# PII Redaction Filter Agent

> **"Data is a distinct liability."**

---

## 🧠 Mental Model

### The Problem
Users paste emails, phone numbers, and API keys into Chatbots.
This data gets sent to the LLM provider.
It gets logged in your database.
It leaks.

### The Solution
A **Privacy Preserving Proxy**.
Before the prompt reaches the LLM, we scan it for PII (Personally Identifiable Information).
We replace it with `[EMAIL_REDACTED]`.

### Regex Patterns
*   **Email**: `\b[\w\.-]+@[\w\.-]+\.\w+\b`
*   **Phone**: `\b\d{3}[-.]?\d{3}[-.]?\d{4}\b` (US Simple)
*   **SSN/Credit Card**: (Similar patterns)

## 🛠️ Tech Stack
*   `re` (Regular Expressions) - Fast and effective for structured PII.
*   `presidio` (Microsoft's library - optional advanced step, here we use `re`).
