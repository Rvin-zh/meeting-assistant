from backend.agents.analysis import analyze_transcript
from backend.config import CHROMA_DIR, SQLITE_PATH
from backend.models.schemas import CreateMeetingRequest, MeetingAnalysis, MeetingRecord
from backend.services.meeting_store import MeetingStore
from backend.services.transcript import (
    chunk_transcript,
    format_transcript,
    parse_transcript,
)
from backend.services.vector_store import VectorStore


async def ingest_meeting(
    transcript: str,
    *,
    title: str | None = None,
    source: str = "upload",
    store: MeetingStore | None = None,
    vector_store: VectorStore | None = None,
) -> MeetingRecord:
    meeting_store = store or MeetingStore(SQLITE_PATH)
    vectors = vector_store or VectorStore(CHROMA_DIR)

    turns = parse_transcript(transcript)
    if not turns:
        raise ValueError("transcript خالی یا نامعتبر است")

    formatted = format_transcript(turns)
    analysis: MeetingAnalysis = await analyze_transcript(formatted)
    if title:
        analysis.title = title

    meeting_id = MeetingStore.new_id()
    chunks = chunk_transcript(turns)
    await vectors.index_meeting(meeting_id, chunks)

    record = MeetingRecord(
        id=meeting_id,
        title=analysis.title,
        transcript=formatted,
        analysis=analysis,
        created_at=MeetingStore.now_iso(),
        source=source,
    )
    meeting_store.save(record)
    return record
