# Watermarking Agent

> **"Sign your work, invisibly."**

---

## 🧠 Mental Model

### The Problem
AI-generated text is flooding the web.
We need a way to prove that "Model X" wrote this text.
Visible signatures ("Written by AI") are easily removed.

### The Solution
**Text Steganography (Watermarking)**.
We inject invisible characters (Zero-width spaces) or use a statistical pattern (e.g., Red/Green list of words) to "stamp" the text.

### Architecture
1.  **Encode**: Message + Secret -> Watermarked Message.
2.  **Decode**: Watermarked Message -> Provenance Verified.
3.  **Attack**: Can we remove it?

## 🛠️ Tech Stack
*   `Unicode` (Zero-width characters: `\u200b`, `\u200c`).
*   String manipulation.
