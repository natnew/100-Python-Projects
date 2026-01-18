# License Compliance Checker Agent

> **"Don't get sued."**

---

## 🧠 Mental Model

### The Problem
You used a library licensed under **GPL v3**.
Now your entire proprietary codebase must be open sourced.
This is "copyleft viral infection."

### The Solution
A **Dependency Scanner**.
It checks your list of packages (e.g., `requirements.txt`).
It looks up their licenses.
It flags "High Risk" licenses (GPL, AGPL) vs "Permissive" (MIT, Apache).

### Architecture
1.  **Scanner**: Parse `requirements.txt`.
2.  **Lookup**: Check a Database (JSON) of package metadata.
3.  **Policy**: Allow/Deny based on `AllowList` = [MIT, Apache, BSD].

## 🛠️ Tech Stack
*   `pkg_resources` (Reading installed packages).
*   `json` (Mock registry).
