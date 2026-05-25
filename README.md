# دستیار جلسه سازمانی — MVP

اپ دمو برای تحلیل transcript جلسات فارسی: خلاصه، تسک، RAG، Jira.

## پیش‌نیاز

- Python 3.11+
- Node.js 20+
- فایل `.env` در ریشه پروژه (از `.env.example` کپی کنید)

## تست backend

```bash
chmod +x scripts/run-tests.sh
./scripts/run-tests.sh
```

**79 unit tests** (+ **8 live tests** with real API keys) — unit: `./scripts/run-tests.sh` · live: `./scripts/run-live-tests.sh`

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

- `docs/پروژه-اصلی.html`
- `docs/پیاده-سازی.html`
- `docs/شرح-پروژه-دستیار-جلسه.html`
- Spec: `docs/superpowers/specs/2026-05-26-meeting-assistant-design.md`
