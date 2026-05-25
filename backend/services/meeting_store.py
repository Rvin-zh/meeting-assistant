"""Persist meetings and summaries in SQLite."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from backend.config import MEETINGS_DIR, SQLITE_PATH, SYNTHETIC_DIR
from backend.models.schemas import MeetingAnalysis, MeetingRecord, MeetingTask
from backend.services.database import connect, get_meta, init_db, set_meta


class MeetingStore:
    def __init__(
        self,
        db_path: Path = SQLITE_PATH,
        *,
        legacy_json_dir: Path | None = MEETINGS_DIR,
    ) -> None:
        self.db_path = db_path
        self.legacy_json_dir = legacy_json_dir
        init_db(self.db_path)
        self._migrate_legacy_json()

    def save(self, record: MeetingRecord) -> MeetingRecord:
        analysis = record.analysis
        with connect(self.db_path) as conn:
            conn.execute(
                """
                INSERT INTO meetings (
                    id, title, transcript, summary, title_en,
                    key_points_json, decisions_json, tasks_json,
                    created_at, source
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    title = excluded.title,
                    transcript = excluded.transcript,
                    summary = excluded.summary,
                    title_en = excluded.title_en,
                    key_points_json = excluded.key_points_json,
                    decisions_json = excluded.decisions_json,
                    tasks_json = excluded.tasks_json,
                    created_at = excluded.created_at,
                    source = excluded.source
                """,
                (
                    record.id,
                    record.title,
                    record.transcript,
                    analysis.summary,
                    analysis.title_en,
                    json.dumps(analysis.key_points, ensure_ascii=False),
                    json.dumps(analysis.decisions, ensure_ascii=False),
                    json.dumps(
                        [t.model_dump() for t in analysis.tasks],
                        ensure_ascii=False,
                    ),
                    record.created_at,
                    record.source,
                ),
            )
            conn.commit()
        return record

    def get(self, meeting_id: str) -> MeetingRecord | None:
        with connect(self.db_path) as conn:
            row = conn.execute(
                "SELECT * FROM meetings WHERE id = ?", (meeting_id,)
            ).fetchone()
        if not row:
            return None
        return self._row_to_record(row)

    def list_all(self) -> list[MeetingRecord]:
        with connect(self.db_path) as conn:
            rows = conn.execute(
                "SELECT * FROM meetings ORDER BY created_at DESC"
            ).fetchall()
        return [self._row_to_record(row) for row in rows]

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

    def _migrate_legacy_json(self) -> None:
        if not self.legacy_json_dir or not self.legacy_json_dir.is_dir():
            return
        json_files = list(self.legacy_json_dir.glob("*.json"))
        if not json_files:
            return

        with connect(self.db_path) as conn:
            if get_meta(conn, "legacy_json_migrated") == "1":
                return
            for path in json_files:
                try:
                    record = MeetingRecord.model_validate_json(
                        path.read_text(encoding="utf-8")
                    )
                except Exception:
                    continue
                self.save(record)
            set_meta(conn, "legacy_json_migrated", "1")
            conn.commit()

    @staticmethod
    def _row_to_record(row: object) -> MeetingRecord:
        tasks_raw = json.loads(row["tasks_json"])
        tasks = [MeetingTask.model_validate(t) for t in tasks_raw]
        analysis = MeetingAnalysis(
            title=row["title"],
            title_en=row["title_en"] or "",
            summary=row["summary"],
            key_points=json.loads(row["key_points_json"]),
            decisions=json.loads(row["decisions_json"]),
            tasks=tasks,
        )
        return MeetingRecord(
            id=row["id"],
            title=row["title"],
            transcript=row["transcript"],
            analysis=analysis,
            created_at=row["created_at"],
            source=row["source"],
        )

    @staticmethod
    def new_id() -> str:
        return uuid4().hex[:12]

    @staticmethod
    def now_iso() -> str:
        return datetime.now(timezone.utc).isoformat()
