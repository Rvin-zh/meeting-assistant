# Enterprise Meeting Assistant — MVP

AI-powered meeting intelligence system for Persian enterprise meetings: **Audio or Text** → Transcript → Executive Summary, Action Items, Vector RAG Search & Jira Task Generation.

[[ فارسی (Persian) ]](README.md) · **[ English ]**

---

## Architecture Overview

```
                      ┌────────────────────────────────────────┐
                      │          Astro Frontend (RTL)          │
                      │  Meeting Dashboard • Audio Recorder    │
                      └──────────────────┬─────────────────────┘
                                         │ REST API
                                         ▼
                      ┌────────────────────────────────────────┐
                      │          FastAPI Backend Engine        │
                      ├──────────────────┬─────────────────────┤
                      │ • Gemini Audio   │ • Pydantic AI Agent │
                      │   Transcriber    │ • Task Extractor    │
                      │ • Sentiment/Tone │ • Jira Dispatcher   │
                      └─────────┬────────┴──────────┬──────────┘
                                │                   │
                                ▼                   ▼
                      ┌──────────────────┐ ┌──────────────────┐
                      │  SQLite Database │ │  ChromaDB (Local)│
                      │   (Structured)   │ │  (Vector Embed)  │
                      └──────────────────┘ └──────────────────┘
```

- **Meetings Database:** Embedded SQLite (`data/meetings.db`) storing meeting metadata, transcripts, structured summaries, and action items.
- **Vector Database:** Local embedded [ChromaDB](https://www.trychroma.com/) (`data/chroma/`) indexing multi-turn semantic embeddings for cross-meeting question answering and search.

---

## Key Features

- **Voice Ingestion & Audio Transcription:** Native voice recording or audio upload via `POST /api/transcribe`, using Google Gemini with structured Persian phonetic adaptation.
- **Pydantic AI Agent Pipeline:** Automated meeting facilitation and structured extraction:
  - Concise executive summaries.
  - Granular action items with owner detection and deadlines.
  - Semantic question-answering with citation grounding over past meetings.
- **Project Tracking & Jira Sync:** Direct mapping of meeting tasks to Jira tickets with priority, issue type, and assignee assignment.
- **Multi-Layer Testing Suite:** 141 comprehensive unit tests and 12 live end-to-end API verification tests.

---

## Quickstart & Prerequisites

### Requirements
- **Python:** 3.11+
- **Node.js:** 20+
- **API Keys:** Google Gemini API Key (copy from `.env.example` to `.env`)

### Setup Environment
```bash
cp .env.example .env
# Edit .env and insert your GOOGLE_API_KEY
```

### Running Backend & Frontend Together
```bash
chmod +x scripts/run-dev.sh
./scripts/run-dev.sh
```

### Running Components Individually
```bash
# Terminal 1 - FastAPI Backend
chmod +x scripts/run-backend.sh
./scripts/run-backend.sh

# Terminal 2 - Astro Frontend
chmod +x scripts/run-frontend.sh
./scripts/run-frontend.sh
```

Once running, access the application at: **http://localhost:4321**

---

## Test Automation

Run tests using the project scripts:

```bash
# Run 141 unit tests
./scripts/run-tests.sh

# Run 12 live integration tests (requires real API key)
./scripts/run-live-tests.sh

# Run all test suites
./scripts/run-all-tests.sh
```

---

## Comprehensive Project Documentation

Detailed academic and technical documentation is maintained under `docs/` with matching printable PDFs in `docs/pdf/`:

1. **Project Overview & Vision** (`docs/01-project-overview.html`)
   - Problem statement, product architecture, AI-native design principles, and KPIs.
2. **Technical Implementation** (`docs/02-implementation.html`)
   - Dataflow pipelines, RAG architecture, agent orchestration, REST API schemas, and error recovery.
3. **Roadmap & Future Extensions** (`docs/03-roadmap-and-future-work.html`)
   - Sprints 2–6, real-time meeting coaching, Jira enterprise webhooks, MLOps, and research proposals.

---

## License & Author
- **Author:** [Rvin-zh](https://github.com/Rvin-zh)
- **Repository:** [https://github.com/Rvin-zh/meeting-assistant](https://github.com/Rvin-zh/meeting-assistant)
