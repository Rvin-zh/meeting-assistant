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

ترمینال ۱ — backend:

```bash
chmod +x scripts/run-backend.sh
./scripts/run-backend.sh
```

ترمینال ۲ — frontend:

```bash
chmod +x scripts/run-frontend.sh
./scripts/run-frontend.sh
```

باز کنید: http://localhost:4321

## اسناد

- `docs/README.md` — فهرست مستندات
- `docs/CHANGELOG.md` — **تاریخچه تغییرات** (با هر feature به‌روز شود)
- `docs/پروژه-اصلی.html` · `docs/پیاده-سازی.html` · `docs/شرح-پروژه-دستیار-جلسه.html`
- **Planned (Sprint 6+):** `docs/قابلیت‌های-پیشرفته-آینده.html` — facilitator guide, SOW alignment, sentiment
- Spec: `docs/superpowers/specs/2026-05-26-meeting-assistant-design.md`
- Roadmap: `docs/نقشه-اسپرینت‌ها.html` (Sprints 2–6+)
- **Voice:** آپلود/ضبط صوت → Gemini رونویسی → همان pipeline تحلیل (`POST /api/transcribe`)
- PDF export: `./scripts/export-docs.sh` → `docs/pdf/`
