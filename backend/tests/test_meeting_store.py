from pathlib import Path

import pytest

from backend.models.schemas import MeetingRecord
from backend.services.meeting_store import MeetingStore
from backend.tests.conftest import SAMPLE_ANALYSIS, SAMPLE_TRANSCRIPT


class TestMeetingStoreCRUD:
    def test_save_and_get(self, meeting_store: MeetingStore):
        record = MeetingRecord(
            id="abc123",
            title="t",
            transcript=SAMPLE_TRANSCRIPT,
            analysis=SAMPLE_ANALYSIS,
            created_at="2026-01-01T00:00:00+00:00",
        )
        meeting_store.save(record)
        loaded = meeting_store.get("abc123")
        assert loaded is not None
        assert loaded.title == "t"

    def test_get_missing_returns_none(self, meeting_store: MeetingStore):
        assert meeting_store.get("missing") is None

    def test_list_all_sorted_newest_first(self, meeting_store: MeetingStore):
        r1 = MeetingRecord(
            id="1",
            title="old",
            transcript="t",
            analysis=SAMPLE_ANALYSIS,
            created_at="2026-01-01T00:00:00+00:00",
        )
        r2 = MeetingRecord(
            id="2",
            title="new",
            transcript="t",
            analysis=SAMPLE_ANALYSIS,
            created_at="2026-02-01T00:00:00+00:00",
        )
        meeting_store.save(r1)
        meeting_store.save(r2)
        titles = [r.title for r in meeting_store.list_all()]
        assert titles == ["new", "old"]


class TestSyntheticFiles:
    def test_list_synthetic(
        self, tmp_data_dirs: dict[str, Path], monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.setattr(
            "backend.services.meeting_store.SYNTHETIC_DIR",
            tmp_data_dirs["synthetic"],
        )
        store = MeetingStore(tmp_data_dirs["meetings"])
        items = store.list_synthetic()
        assert len(items) == 1
        assert items[0]["id"] == "demo-meeting"

    def test_load_synthetic(
        self, tmp_data_dirs: dict[str, Path], monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.setattr(
            "backend.services.meeting_store.SYNTHETIC_DIR",
            tmp_data_dirs["synthetic"],
        )
        store = MeetingStore(tmp_data_dirs["meetings"])
        text = store.load_synthetic("demo-meeting")
        assert "علی" in text

    def test_load_synthetic_not_found(
        self, tmp_data_dirs: dict[str, Path], monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.setattr(
            "backend.services.meeting_store.SYNTHETIC_DIR",
            tmp_data_dirs["synthetic"],
        )
        store = MeetingStore(tmp_data_dirs["meetings"])
        with pytest.raises(FileNotFoundError):
            store.load_synthetic("no-such-file")


class TestMeetingStoreHelpers:
    def test_new_id_length(self):
        assert len(MeetingStore.new_id()) == 12

    def test_now_iso_contains_t(self):
        assert "T" in MeetingStore.now_iso()
