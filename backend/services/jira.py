import base64
from typing import Any

import httpx

from backend.config import JIRA_API_TOKEN, JIRA_EMAIL, JIRA_PROJECT_KEY, JIRA_SITE_URL
from backend.models.schemas import JiraPreviewIssue, MeetingTask

PRIORITY_MAP = {
    "high": "High",
    "medium": "Medium",
    "low": "Low",
}


def _auth_header() -> dict[str, str]:
    token = base64.b64encode(f"{JIRA_EMAIL}:{JIRA_API_TOKEN}".encode()).decode()
    return {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def build_issue_payload(
    task: MeetingTask, meeting_title: str, meeting_title_en: str = ""
) -> JiraPreviewIssue:
    """Build Jira issue fields in English for readable LTR display in Jira."""
    summary = (task.title_en or task.title).strip()
    meeting_label = (meeting_title_en or meeting_title).strip()
    context = (task.context_en or task.context or "—").strip()

    description_parts = [
        f"*Meeting:* {meeting_label}",
        f"*Context:* {context}",
    ]
    if task.assignee:
        description_parts.append(f"*Suggested assignee:* {task.assignee}")
    if task.deadline:
        description_parts.append(f"*Deadline:* {task.deadline}")

    return JiraPreviewIssue(
        summary=summary,
        description="\n".join(description_parts),
        priority=PRIORITY_MAP.get(task.priority, "Medium"),
        task_index=-1,
    )


def preview_issues(
    tasks: list[MeetingTask],
    meeting_title: str,
    meeting_title_en: str = "",
) -> list[JiraPreviewIssue]:
    issues = []
    for index, task in enumerate(tasks):
        issue = build_issue_payload(task, meeting_title, meeting_title_en)
        issue.task_index = index
        issues.append(issue)
    return issues


async def create_issues(
    issues: list[JiraPreviewIssue],
    assignee_account_ids: list[str | None] | None = None,
) -> list[dict[str, Any]]:
    if not JIRA_EMAIL or not JIRA_API_TOKEN:
        raise ValueError("Jira credentials are not configured")

    created: list[dict[str, Any]] = []
    async with httpx.AsyncClient(timeout=30.0) as client:
        for i, issue in enumerate(issues):
            fields: dict[str, Any] = {
                "project": {"key": JIRA_PROJECT_KEY},
                "summary": issue.summary,
                "description": {
                    "type": "doc",
                    "version": 1,
                    "content": [
                        {
                            "type": "paragraph",
                            "content": [{"type": "text", "text": issue.description}],
                        }
                    ],
                },
                "issuetype": {"name": "Task"},
                "priority": {"name": issue.priority},
            }
            if assignee_account_ids and i < len(assignee_account_ids):
                account_id = assignee_account_ids[i]
                if account_id:
                    fields["assignee"] = {"accountId": account_id}
            payload = {"fields": fields}
            response = await client.post(
                f"{JIRA_SITE_URL.rstrip('/')}/rest/api/3/issue",
                headers=_auth_header(),
                json=payload,
            )
            if response.status_code >= 400:
                detail = response.text
                raise ValueError(f"Jira error ({response.status_code}): {detail}")
            data = response.json()
            created.append(
                {
                    "key": data.get("key"),
                    "summary": issue.summary,
                    "task_index": issue.task_index,
                }
            )
    return created
