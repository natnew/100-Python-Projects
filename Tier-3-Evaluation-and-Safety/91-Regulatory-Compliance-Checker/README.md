# Regulatory Compliance Checker Agent

> **"Compliance is not optional."**

---

## 🧠 Mental Model

### The Problem
GDPR, CCPA, EU AI Act.
These are massive legal frameworks.
Does your agent support "Right to be Forgotten" (Article 17)?
Does it have "Human Oversight" (Article 14)?

### The Solution
A **Capability Scanner**.
It checks the agent's codebase or configuration for required hooks.
*   *Requirement*: `delete_user_data()` must exist.
*   *Requirement*: `human_override` must be enabled.

### Architecture
1.  **Registry**: List of Regulations (GDPR, etc.).
2.  **Scanner**: Inspects agent Interface/API.
3.  **Report**: Pass/Fail for each clause.

## 🛠️ Tech Stack
*   `inspect` (Reflection on code).
*   `dataclasses`.
