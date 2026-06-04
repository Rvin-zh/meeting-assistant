"""Export meeting analysis as Markdown."""

from backend.models.schemas import MeetingRecord

PRIORITY_FA = {"high": "بالا", "medium": "متوسط", "low": "پایین"}


def meeting_to_markdown(record: MeetingRecord) -> str:
    a = record.analysis
    lines = [
        f"# {record.title}",
        "",
        f"- **شناسه:** `{record.id}`",
        f"- **تاریخ:** {record.created_at}",
        f"- **منبع:** {record.source}",
        "",
        "## خلاصه",
        "",
        a.summary,
        "",
    ]
    if a.key_points:
        lines.extend(["## نکات کلیدی", ""])
        lines.extend(f"- {p}" for p in a.key_points)
        lines.append("")
    if a.decisions:
        lines.extend(["## تصمیمات", ""])
        lines.extend(f"- {d}" for d in a.decisions)
        lines.append("")
    if a.tasks:
        lines.extend(["## تسک‌ها", ""])
        for i, t in enumerate(a.tasks, 1):
            pr = PRIORITY_FA.get(t.priority, t.priority)
            lines.append(f"### {i}. {t.title}")
            if t.title_en:
                lines.append(f"- **Jira (EN):** {t.title_en}")
            if t.assignee:
                lines.append(f"- **مسئول:** {t.assignee}")
            if t.deadline:
                lines.append(f"- **مهلت:** {t.deadline}")
            lines.append(f"- **اولویت:** {pr}")
            if t.context:
                lines.append(f"- **زمینه:** {t.context}")
            lines.append("")
    return "\n".join(lines).strip() + "\n"
