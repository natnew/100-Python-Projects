# Access Control (RBAC) Agent

> **"With great power comes great need for a permission system."**

---

## 🧠 Mental Model

### The Problem
If every agent can delete the database, your database will be deleted.
"Alice" is an intern. She should not deploy to prod.
"Bob" is a senior engineer. He can.

### The Solution
A **Gatekeeper (Authorizer)**.
It checks every request against a policy.
*   **Subject**: Who? (Alice)
*   **Role**: What group? (Intern)
*   **Resource**: What object? (ProductionDB)
*   **Action**: What verb? (Delete)

### Architecture
1.  **Users** are assigned **Roles**.
2.  **Roles** have **Permissions**.
3.  **Gatekeeper** checks: `User -> Role -> Permission`.

## 🛠️ Tech Stack
*   `dataclasses` (Structs).
*   `typing` (Enums).
