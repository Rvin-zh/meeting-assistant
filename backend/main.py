from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.agents.rag import ask_meeting
from backend.config import (
    GOOGLE_API_KEY,
    JIRA_API_TOKEN,
    JIRA_EMAIL,
    JIRA_SITE_URL,
    CHROMA_DIR,
    SQLITE_PATH,
)
from backend.models.schemas import (
    AskRequest,
    CreateMeetingRequest,
    JiraCreateRequest,
    MeetingRecord,
)
from backend.services.ingest import ingest_meeting
from backend.services.jira import create_issues, preview_issues
from backend.services.meeting_store import MeetingStore
from backend.services.vector_store import VectorStore

app = FastAPI(title="دستیار جلسه", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4321", "http://127.0.0.1:4321"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

meeting_store = MeetingStore(SQLITE_PATH)
vector_store = VectorStore(CHROMA_DIR)


@app.get("/api/health")
async def health() -> dict:
    return {
        "status": "ok",
        "google_api": bool(GOOGLE_API_KEY),
        "jira_configured": bool(JIRA_EMAIL and JIRA_API_TOKEN),
        "jira_site": JIRA_SITE_URL,
        "database": str(SQLITE_PATH),
    }


@app.get("/api/meetings")
async def list_meetings() -> list[MeetingRecord]:
    return meeting_store.list_all()


@app.get("/api/meetings/synthetic")
async def list_synthetic() -> list[dict[str, str]]:
    return meeting_store.list_synthetic()


@app.post("/api/meetings/synthetic/{file_id}", response_model=MeetingRecord)
async def create_from_synthetic(file_id: str) -> MeetingRecord:
    try:
        transcript = meeting_store.load_synthetic(file_id)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    try:
        return await ingest_meeting(
            transcript,
            source=f"synthetic:{file_id}",
            store=meeting_store,
            vector_store=vector_store,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"خطا در پردازش: {exc}") from exc


@app.post("/api/meetings", response_model=MeetingRecord)
async def create_meeting(body: CreateMeetingRequest) -> MeetingRecord:
    if not body.transcript.strip():
        raise HTTPException(status_code=400, detail="transcript الزامی است")
    try:
        return await ingest_meeting(
            body.transcript,
            title=body.title,
            store=meeting_store,
            vector_store=vector_store,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"خطا در پردازش: {exc}") from exc


@app.get("/api/meetings/{meeting_id}", response_model=MeetingRecord)
async def get_meeting(meeting_id: str) -> MeetingRecord:
    record = meeting_store.get(meeting_id)
    if not record:
        raise HTTPException(status_code=404, detail="جلسه یافت نشد")
    return record


@app.post("/api/meetings/{meeting_id}/ask")
async def ask_question(meeting_id: str, body: AskRequest):
    record = meeting_store.get(meeting_id)
    if not record:
        raise HTTPException(status_code=404, detail="جلسه یافت نشد")
    if not body.question.strip():
        raise HTTPException(status_code=400, detail="سوال الزامی است")
    try:
        answer = await ask_meeting(meeting_id, body.question, vector_store)
        return answer
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"خطا در RAG: {exc}") from exc


@app.post("/api/meetings/{meeting_id}/jira/preview")
async def jira_preview(meeting_id: str):
    record = meeting_store.get(meeting_id)
    if not record:
        raise HTTPException(status_code=404, detail="جلسه یافت نشد")
    issues = preview_issues(
        record.analysis.tasks,
        record.title,
        record.analysis.title_en,
    )
    return {"issues": issues}


@app.post("/api/meetings/{meeting_id}/jira/create")
async def jira_create(meeting_id: str, body: JiraCreateRequest | None = None):
    record = meeting_store.get(meeting_id)
    if not record:
        raise HTTPException(status_code=404, detail="جلسه یافت نشد")

    issues = preview_issues(
        record.analysis.tasks,
        record.title,
        record.analysis.title_en,
    )
    if body and body.task_indices is not None:
        selected = [issues[i] for i in body.task_indices if 0 <= i < len(issues)]
    else:
        selected = issues

    if not selected:
        raise HTTPException(status_code=400, detail="تسکی برای ارسال نیست")

    try:
        created = await create_issues(selected)
        return {"created": created}
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"خطا در Jira: {exc}") from exc
