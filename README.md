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

## اسناد (سه سند اصلی فارسی)

سه سند اصلی پروژه به فارسی (مناسب ارائه دانشگاهی) در `docs/` — هر کدام یک PDF متناظر در `docs/pdf/`:

- `docs/01-project-overview.html` — **شرح پروژه و چشم‌انداز** (مسئله، محصول، معماری، چارچوب AI-native، معیار موفقیت)
- `docs/02-implementation.html` — **پیاده‌سازی فنی** (جریان داده، RAG، عامل‌ها، API، UI، تست‌ها، مدیریت خطا)
- `docs/03-roadmap-and-future-work.html` — **نقشه راه و کارهای آینده** (اسپرینت ۲–۶+، راهنمای برگزارکننده، هم‌راستایی SOW، sentiment، MLOps، ایده‌های پژوهشی)

سایر منابع:

- `docs/README.md` — فهرست مستندات
- `docs/CHANGELOG.md` — **تاریخچه تغییرات** (با هر feature به‌روز شود)
- Spec: `docs/superpowers/specs/2026-05-26-meeting-assistant-design.md`
- **Voice:** آپلود/ضبط صوت → Gemini رونویسی → همان pipeline تحلیل (`POST /api/transcribe`)
- PDF export: `./scripts/export-docs.sh` → `docs/pdf/` (سه PDF متناظر سه سند بالا)
