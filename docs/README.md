# مستندات پروژه — دستیار جلسه

## فهرست

| فایل | محتوا |
|------|--------|
| [پروژه-اصلی.html](پروژه-اصلی.html) | چشم‌انداز محصول، معماری، sprintها |
| [پیاده-سازی.html](پیاده-سازی.html) | پیاده‌سازی فنی: API، ChromaDB، RAG، Jira، UI |
| [شرح-پروژه-دستیار-جلسه.html](شرح-پروژه-دستیار-جلسه.html) | شرح دوره، RAG، MLOps آینده |
| [قابلیت‌های-پیشرفته-آینده.html](قابلیت‌های-پیشرفته-آینده.html) | **Sprint 6+** — راهنمای برگزارکننده · SOW/قرارداد · sentiment |
| [نقشه-اسپرینت‌ها.html](نقشه-اسپرینت‌ها.html) | **اسپرینت ۲–۶+** — ایده‌ها و اولویت |
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
