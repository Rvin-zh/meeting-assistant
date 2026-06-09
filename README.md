# دستیار جلسه سازمانی — MVP

اپ دمو برای تحلیل جلسات فارسی: **متن یا صوت** → transcript → خلاصه، تسک، RAG، Jira.

**Meetings DB:** SQLite (`data/meetings.db`) — transcripts, summaries, tasks. Legacy JSON in `data/meetings/` migrates on first start.

**Vector DB:** [ChromaDB](https://www.trychroma.com/) (embedded, local — `data/chroma/`).

## پیش‌نیاز

- Python 3.11+
- Node.js 20+
- فایل `.env` در ریشه پروژه (از `.env.example` کپی کنید)

## تست backend

```bash
chmod +x scripts/run-tests.sh
./scripts/run-tests.sh
```

**141 unit tests** (+ **12 live tests** with real APIs) — unit: `./scripts/run-tests.sh` · live: `./scripts/run-live-tests.sh` · both: `./scripts/run-all-tests.sh`

## اجرا

یک ترمینال — backend + frontend:

```bash
chmod +x scripts/run-dev.sh
./scripts/run-dev.sh
```

یا دو ترمینال جدا:

```bash
chmod +x scripts/run-backend.sh
./scripts/run-backend.sh
```

```bash
chmod +x scripts/run-frontend.sh
./scripts/run-frontend.sh
```

باز کنید: http://localhost:4321

## اسناد (English — graduation set)

سه سند اصلی پروژه به انگلیسی (مناسب ارائه دانشگاهی) در `docs/`:

- `docs/01-project-overview.html` — Project Overview & Vision (problem, product, architecture, AI-native framing)
- `docs/02-implementation.html` — Technical Implementation (data flow, RAG, agents, API, UI, tests)
- `docs/03-roadmap-and-future-work.html` — Roadmap & Future Work (Sprints 2–6+, facilitator guide, SOW alignment, sentiment, MLOps)

سایر منابع:

- `docs/README.md` — فهرست مستندات
- `docs/CHANGELOG.md` — **تاریخچه تغییرات** (با هر feature به‌روز شود)
- Spec: `docs/superpowers/specs/2026-05-26-meeting-assistant-design.md`
- **Voice:** آپلود/ضبط صوت → Gemini رونویسی → همان pipeline تحلیل (`POST /api/transcribe`)
- PDF export: `./scripts/export-docs.sh` → `docs/pdf/` (سه PDF متناظر سه سند بالا)
