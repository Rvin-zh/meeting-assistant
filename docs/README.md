# مستندات پروژه — دستیار جلسه

## فهرست

سه سند اصلی به **فارسی** (مناسب ارائه/فارغ‌التحصیلی) — هر کدام یک PDF متناظر در `pdf/`:

| فایل | محتوا |
|------|--------|
| [01-project-overview.html](01-project-overview.html) | **شرح پروژه و چشم‌انداز** — مسئله، محصول، معماری، چارچوب AI-native، معیار موفقیت |
| [02-implementation.html](02-implementation.html) | **پیاده‌سازی فنی** — جریان داده، RAG، عامل‌ها، SQLite/Chroma، API، UI، تست‌ها، مدیریت خطا |
| [03-roadmap-and-future-work.html](03-roadmap-and-future-work.html) | **نقشه راه و کارهای آینده** — اسپرینت ۲–۶+، راهنمای برگزارکننده، SOW/قرارداد، sentiment، MLOps، ایده‌های پژوهشی |

منابع تکمیلی:

| فایل | محتوا |
|------|--------|
| [CHANGELOG.md](CHANGELOG.md) | **تاریخچه تغییرات** — با هر feature به‌روز شود |
| [screenshots/](screenshots/) | **اسکرین‌شات UI/UX** — خانه، جلسه، تسک‌ها، تنظیمات |
| [superpowers/specs/2026-05-26-meeting-assistant-design.md](superpowers/specs/2026-05-26-meeting-assistant-design.md) | Spec طراحی |
| [superpowers/specs/future-sprints-roadmap.md](superpowers/specs/future-sprints-roadmap.md) | نقشه اسپرینت (Markdown) |

## مشاهده HTML

فایل‌های `.html` را در مرورگر باز کنید (RTL، نمودار Mermaid).

## PDF و SVG (خروجی خودکار)

```bash
chmod +x scripts/export-docs.sh
./scripts/export-docs.sh
```

| خروجی | مسیر |
|--------|------|
| **PDF** (فارسی RTL، فونت Vazirmatn) | [docs/pdf/](pdf/) |
| **SVG** (نمودارهای Mermaid) | [docs/diagrams/](diagrams/) |
| **UI screenshots** (Playwright) | [docs/screenshots/](screenshots/) |

برای به‌روزرسانی اسکرین‌شات‌ها (backend + frontend باید روشن باشند):

```bash
chmod +x scripts/capture-ui-screenshots.sh
./scripts/capture-ui-screenshots.sh
```

نیازمندی‌ها: Node.js 20+، اینترنت (اولین بار برای npm و فونت).

## مخزن کد

https://github.com/Rvin-zh/meeting-assistant
