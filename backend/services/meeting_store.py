import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from backend.config import MEETINGS_DIR, SYNTHETIC_DIR
from backend.models.schemas import MeetingRecord


class MeetingStore:
    def __init__(self, meetings_dir: Path = MEETINGS_DIR) -> None:
        self.meetings_dir = meetings_dir

    def _path(self, meeting_id: str) -> Path:
        return self.meetings_dir / f"{meeting_id}.json"

    def save(self, record: MeetingRecord) -> MeetingRecord:
        self._path(record.id).write_text(
            record.model_dump_json(indent=2),
            encoding="utf-8",
        )
        return record

    def get(self, meeting_id: str) -> MeetingRecord | None:
        path = self._path(meeting_id)
        if not path.exists():
            return None
        return MeetingRecord.model_validate_json(path.read_text(encoding="utf-8"))

    def list_all(self) -> list[MeetingRecord]:
        records: list[MeetingRecord] = []
        for path in sorted(self.meetings_dir.glob("*.json")):
            records.append(
                MeetingRecord.model_validate_json(path.read_text(encoding="utf-8"))
            )
        records.sort(key=lambda r: r.created_at, reverse=True)
        return records

    def list_synthetic(self) -> list[dict[str, str]]:
        files = []
        for path in sorted(SYNTHETIC_DIR.glob("*.txt")):
            files.append({"id": path.stem, "filename": path.name, "title": path.stem})
        return files

    def load_synthetic(self, file_id: str) -> str:
        path = SYNTHETIC_DIR / f"{file_id}.txt"
        if not path.exists():
            path = SYNTHETIC_DIR / file_id
        if not path.exists():
            raise FileNotFoundError(f"Synthetic meeting not found: {file_id}")
        return path.read_text(encoding="utf-8")

    @staticmethod
    def new_id() -> str:
        return uuid4().hex[:12]

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()
