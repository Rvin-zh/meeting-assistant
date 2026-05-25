"""Shared Pydantic schemas."""

from typing import Literal

from pydantic import BaseModel, Field


class MeetingTask(BaseModel):
    title: str
    title_en: str = ""
    assignee: str | None = None
    deadline: str | None = None
    priority: Literal["high", "medium", "low"] = "medium"
    context: str = ""
    context_en: str = ""


class MeetingAnalysis(BaseModel):
    title: str
    title_en: str = ""
    summary: str
    key_points: list[str] = Field(default_factory=list)
    decisions: list[str] = Field(default_factory=list)
    tasks: list[MeetingTask] = Field(default_factory=list)


class ChunkCitation(BaseModel):
    chunk_id: str
    speaker: str
    excerpt: str = ""
    text: str = ""  # alias for excerpt (backward compat)


class RagAnswer(BaseModel):
    answer: str
    sources: list[ChunkCitation] = Field(default_factory=list)
    used_meeting_context: bool = False


class TranscriptTurn(BaseModel):
    timestamp: str
    speaker: str
    text: str


class TranscriptChunk(BaseModel):
    chunk_id: str
    speaker: str
    text: str
    turn_indices: list[int]


class MeetingRecord(BaseModel):
    id: str
    title: str
    transcript: str
    analysis: MeetingAnalysis
    created_at: str
    source: str = "upload"


class CreateMeetingRequest(BaseModel):
    transcript: str
    title: str | None = None


class AskRequest(BaseModel):
    question: str


class JiraPreviewIssue(BaseModel):
    summary: str
    description: str
    priority: str
    task_index: int


class JiraCreateRequest(BaseModel):
    task_indices: list[int] | None = None
