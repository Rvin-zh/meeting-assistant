"""
Live HTTP API tests — real FastAPI routes + real Google/Jira credentials.

Run: ./scripts/run-live-tests.sh
"""

from __future__ import annotations

from pathlib import Path
from unittest.mock import AsyncMock, patch

import httpx
import pytest
from httpx import ASGITransport, AsyncClient

from backend.main import app
from backend.models.schemas import MeetingAnalysis, MeetingRecord
from backend.services.meeting_store import MeetingStore
from backend.services.vector_store import VectorStore
from backend.tests.conftest import SAMPLE_TRANSCRIPT
from backend.tests.test_live_integration import LIVE_TRANSCRIPT

pytestmark = pytest.mark.live


@pytest.fixture
async def live_api_client(
    tmp_path: Path,
    google_configured: None,
    monkeypatch: pytest.MonkeyPatch,
):
    db = tmp_path / "live-api.db"
    chroma = tmp_path / "live-api-chroma"
    monkeypatch.setattr(
        "backend.main.meeting_store",
        MeetingStore(db, legacy_json_dir=None),
    )
    monkeypatch.setattr("backend.main.vector_store", VectorStore(chroma))
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url="http://test",
        timeout=120.0,
    ) as client:
        yield client


@pytest.mark.asyncio
async def test_live_api_health(live_api_client: AsyncClient):
    response = await live_api_client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["google_api"] is True
    assert "database" in data


@pytest.mark.asyncio
async def test_live_api_create_meeting_real_gemini(live_api_client: AsyncClient):
    response = await live_api_client.post(
        "/api/meetings",
        json={"transcript": LIVE_TRANSCRIPT, "title": "Live API Test"},
    )
    assert response.status_code == 200, response.text
    body = response.json()
    assert body["id"]
    assert body["analysis"]["summary"]
    assert len(body["analysis"]["summary"]) > 10


@pytest.mark.asyncio
async def test_live_api_get_meeting_after_create(live_api_client: AsyncClient):
    created = await live_api_client.post(
        "/api/meetings",
        json={"transcript": LIVE_TRANSCRIPT},
    )
    assert created.status_code == 200
    meeting_id = created.json()["id"]

    fetched = await live_api_client.get(f"/api/meetings/{meeting_id}")
    assert fetched.status_code == 200
    assert fetched.json()["analysis"]["summary"] == created.json()["analysis"]["summary"]


@pytest.mark.asyncio
async def test_live_api_ask_rag(live_api_client: AsyncClient):
    created = await live_api_client.post(
        "/api/meetings",
        json={"transcript": LIVE_TRANSCRIPT},
    )
    meeting_id = created.json()["id"]

    response = await live_api_client.post(
        f"/api/meetings/{meeting_id}/ask",
        json={"question": "deadline دمو چه روزی است؟"},
    )
    assert response.status_code == 200, response.text
    answer = response.json()["answer"]
    assert len(answer) > 5


@pytest.mark.asyncio
async def test_live_api_ask_hello_no_context(live_api_client: AsyncClient):
    created = await live_api_client.post(
        "/api/meetings",
        json={"transcript": LIVE_TRANSCRIPT},
    )
    meeting_id = created.json()["id"]

    response = await live_api_client.post(
        f"/api/meetings/{meeting_id}/ask",
        json={"question": "hello"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data.get("used_meeting_context") is False
    assert data["sources"] == []


@pytest.mark.asyncio
async def test_live_api_jira_preview(jira_configured: None, live_api_client: AsyncClient):
    mock_record = MeetingRecord(
        id="jira-preview-live",
        title="تست",
        transcript=SAMPLE_TRANSCRIPT,
        analysis=MeetingAnalysis(
            title="تست",
            title_en="Live preview test",
            summary="summary",
            tasks=[],
        ),
        created_at="2026-05-26T00:00:00+00:00",
    )
    with patch(
        "backend.main.ingest_meeting", new=AsyncMock(return_value=mock_record)
    ):
        created = await live_api_client.post(
            "/api/meetings",
            json={"transcript": SAMPLE_TRANSCRIPT},
        )
    meeting_id = created.json()["id"]

    preview = await live_api_client.post(f"/api/meetings/{meeting_id}/jira/preview")
    assert preview.status_code == 200


@pytest.mark.asyncio
async def test_live_api_list_meetings(live_api_client: AsyncClient):
    await live_api_client.post(
        "/api/meetings",
        json={"transcript": LIVE_TRANSCRIPT},
    )
    listed = await live_api_client.get("/api/meetings")
    assert listed.status_code == 200
    assert len(listed.json()) >= 1
