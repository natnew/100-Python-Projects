# Man-in-the-Middle (MITM) Simulation

> **"Dance like no one is watching, encrypt like everyone is."**

---

## 🧠 Mental Model

### The Problem
Agents communicate over a network.
If the network is untrusted (e.g., HTTP), an attacker can sit in the middle.
They can read your messages (Confidentiality breach).
They can change your messages (Integrity breach).

### The Solution
**Encryption (TLS)**.
But to understand the cure, we must demonstrate the disease.
This project simulates an unencrypted channel where a middleman (Mallory) alters a banking transaction.

### Architecture
```mermaid
graph LR
    Alice[Alice] -->|Send $100| Mallory[Mallory (MITM)]
    Mallory -->|Send $1000| Bob[Bob (Bank)]
```

## 🛠️ Tech Stack
*   `queue` (To simulate the network wire).
*   `base64` (To simulate weak encoding vs encryption).
