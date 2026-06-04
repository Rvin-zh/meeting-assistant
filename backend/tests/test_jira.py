import base64
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from backend.models.schemas import MeetingTask
from backend.services.jira import (
    PRIORITY_MAP,
    _auth_header,
    build_issue_payload,
    create_issues,
    preview_issues,
)


class TestBuildIssuePayload:
    def test_uses_english_fields_for_jira(self):
        task = MeetingTask(
            title="رفع باگ",
            title_en="Fix refresh token bug",
            assignee="Sara",
            deadline="tomorrow",
            priority="high",
            context="باگ refresh token",
            context_en="Fix refresh token bug before smoke tests",
        )
        issue = build_issue_payload(task, "استنداپ", "Sprint standup")
        assert issue.summary == "Fix refresh token bug"
        assert "*Meeting:* Sprint standup" in issue.description
        assert (
            "*Context:* Fix refresh token bug before smoke tests" in issue.description
        )
        assert "*Suggested assignee:* Sara" in issue.description
        assert "*Deadline:* tomorrow" in issue.description
        assert issue.priority == "High"

    def test_falls_back_to_persian_when_en_missing(self):
        task = MeetingTask(title="Fix bug", context="token issue")
        issue = build_issue_payload(task, "Meeting")
        assert issue.summary == "Fix bug"
        assert "*Context:* token issue" in issue.description

    def test_missing_optional_fields_use_dash(self):
        task = MeetingTask(title="T", title_en="Task T", context="")
        issue = build_issue_payload(task, "Meeting", "Dev sync")
        assert "*Context:* —" in issue.description
        assert "Suggested assignee" not in issue.description

    def test_unknown_priority_maps_to_medium(self):
        task = MeetingTask(title="T", title_en="T", priority="medium", context="c")
        assert build_issue_payload(task, "x").priority == PRIORITY_MAP["medium"]


class TestPreviewIssues:
    def test_assigns_task_index(self):
        tasks = [
            MeetingTask(title="A", title_en="Task A", context="a", context_en="ctx a"),
            MeetingTask(title="B", title_en="Task B", context="b", context_en="ctx b"),
        ]
        issues = preview_issues(tasks, "جلسه", "Team meeting")
        assert [i.task_index for i in issues] == [0, 1]
        assert issues[0].summary == "Task A"

    def test_empty_tasks(self):
        assert preview_issues([], "Meeting") == []


class TestAuthHeader:
    def test_basic_auth_encoding(self):
        with (
            patch("backend.services.jira.JIRA_EMAIL", "user@test.com"),
            patch("backend.services.jira.JIRA_API_TOKEN", "secret-token"),
        ):
            headers = _auth_header()
            encoded = headers["Authorization"].split(" ", 1)[1]
            decoded = base64.b64decode(encoded).decode()
            assert decoded == "user@test.com:secret-token"


class TestCreateIssues:
    @pytest.mark.asyncio
    async def test_raises_without_credentials(self):
        from backend.models.schemas import JiraPreviewIssue

        issue = JiraPreviewIssue(
            summary="S", description="D", priority="Medium", task_index=0
        )
        with patch("backend.services.jira.JIRA_EMAIL", ""):
            with pytest.raises(ValueError, match="credentials"):
                await create_issues([issue])

    @pytest.mark.asyncio
    async def test_successful_create(self):
        from backend.models.schemas import JiraPreviewIssue

        issue = JiraPreviewIssue(
            summary="Task", description="Desc", priority="High", task_index=0
        )
        mock_response = MagicMock()
        mock_response.status_code = 201
        mock_response.json.return_value = {"key": "KAN-99"}

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        with (
            patch("backend.services.jira.JIRA_EMAIL", "u@t.com"),
            patch("backend.services.jira.JIRA_API_TOKEN", "tok"),
            patch("backend.services.jira.httpx.AsyncClient", return_value=mock_client),
        ):
            created = await create_issues([issue])

        assert created == [{"key": "KAN-99", "summary": "Task", "task_index": 0}]
        mock_client.post.assert_called_once()

    @pytest.mark.asyncio
    async def test_jira_error_raises_value_error(self):
        from backend.models.schemas import JiraPreviewIssue

        issue = JiraPreviewIssue(
            summary="T", description="D", priority="Low", task_index=0
        )
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Bad request"

        mock_client = AsyncMock()
        mock_client.post.return_value = mock_response
        mock_client.__aenter__.return_value = mock_client
        mock_client.__aexit__.return_value = None

        with (
            patch("backend.services.jira.JIRA_EMAIL", "u@t.com"),
            patch("backend.services.jira.JIRA_API_TOKEN", "tok"),
            patch("backend.services.jira.httpx.AsyncClient", return_value=mock_client),
        ):
            with pytest.raises(ValueError, match="Jira error \\(400\\)"):
                await create_issues([issue])
