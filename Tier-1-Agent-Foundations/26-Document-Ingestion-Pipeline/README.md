# Document Ingestion Pipeline

> **Standardize raw files into clean, chunked text for AI processing.**

---

## 🧠 Mental Model

### The Problem
AI models accept text strings, not binary PDFs or Word docs.
"Chat with your Data" requires extracting text, stripping garbage (headers/footers), and chunking it into manageable pieces (e.g., 500 tokens).

### The Solution
**Ingestion Pipeline**.
1.  **Loader**: Reads file from disk/URL -> `RawText`.
2.  **Cleaner**: Removes regex noise (e.g., `Page 1 of 10`).
3.  **Splitter**: RecursiveCharacterSplitter (splits on paragraphs first, then sentences).
4.  **Document Object**: Output standard `Document(page_content="...", metadata={...})`.

### When to use this
*   [x] RAG applications.
*   [x] Analyzing long financial reports.

---

## 🏗️ Architecture

```mermaid
graph LR
    PDF[File.pdf] --> Loader
    Loader -->|Raw Text| Cleaner
    Cleaner -->|Clean Text| Splitter
    Splitter -->|Chunks| Docs[List[Document]]
    Docs --> DB[(Vector Store)]
```

## ⚠️ Risks & Ethics

See [ETHICS.md](ETHICS.md).
- **Data Privacy**: Be careful not to ingest PII (SSNs, passwords) from dumps.
- **OCR Errors**: "RN" might look like "M". Bad input = Bad output.
