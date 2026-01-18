# Audio Transcription Service

> **Convert voice input into text for the agent to understand.**

---

## 🧠 Mental Model

### The Problem
Agents assume text input. But users want to speak (Siri/Alexa style).
Audio files are large binaries (WAV/MP3).
Transcription APIs (Whisper, Google STT) are slow/async.

### The Solution
A **Worker Service**.
1.  **Receive**: Client uploads audio buffer.
2.  **Transcode**: Convert to 16khz/Mono (Wait for ffmpeg).
3.  **Transcribe**: Send to OpenAI Whisper or run local model.
4.  **Callback**: Return text to the main agent loop.

### When to use this
*   [x] Voice Bots.
*   [x] Meeting summarizers.

---

## 🏗️ Architecture

```mermaid
graph LR
    Mic[Microphone] -->|WAV| Server
    Server -->|Job| Queue
    Queue --> Worker
    Worker -->|WAV| Whisper[Whisper Model]
    Whisper -->|Text| Agent
```

## ⚠️ Risks & Ethics

See [ETHICS.md](ETHICS.md).
- **Consent**: Never record without permission.
- **Accuracy**: Accents and background noise cause hallucinations ("Ice cream" vs "I scream").
