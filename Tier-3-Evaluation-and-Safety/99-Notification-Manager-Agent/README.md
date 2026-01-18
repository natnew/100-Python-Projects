# Notification Manager Agent

> **"Don't spam me."**

---

## 🧠 Mental Model

### The Problem
If 5 agents all decide to alert the user at the same time, it's annoying.
You need a central notification hub.
It handles **Queuing**, **Debouncing** (throttling), and **Channel Selection**.

### The Solution
A **Notification Queue**.
*   **Channels**: Email, Slack, SMS, Push.
*   **Priority**: High (wake me up) vs. Low (digest).
*   **Logic**: "If I sent an email 5 mins ago, wait."

### Architecture
1.  **Inbox**: Agents push `Message` to queue.
2.  **Worker**: Reads queue, applies logic.
3.  **Adapter**: Mock interface for `SendGrid` or `Slack`.

## 🛠️ Tech Stack
*   `queue` (Thread-safe FIFO).
*   `time` (Debouncing).
