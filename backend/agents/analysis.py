import os

from pydantic_ai import Agent

from backend.config import GEMINI_MODEL, GOOGLE_API_KEY
from backend.models.schemas import MeetingAnalysis, MeetingType

if GOOGLE_API_KEY:
    os.environ.setdefault("GOOGLE_API_KEY", GOOGLE_API_KEY)

BASE_PROMPT = (
    "You analyze Persian meeting transcripts. "
    "Output UI fields in Persian: title, summary, key_points, decisions, and each task's title and context. "
    "Also output English fields for Jira (LTR): title_en (meeting), and per task title_en (issue summary) "
    "and context_en (issue description context). Keep title_en/context_en concise and professional in English. "
    "Tasks must be actionable. Priority: high, medium, or low."
)

MEETING_TYPE_HINTS: dict[MeetingType, str] = {
    "standup": (
        "This is a daily standup. Focus on: what each person did, blockers, "
        "today's plan. Keep summary short. Tasks = concrete next steps with owners."
    ),
    "planning": (
        "This is a sprint/quarter planning session. Focus on: scope, milestones, "
        "deadlines, dependencies, and explicit decisions. Tasks should map to deliverables."
    ),
    "review": (
        "This is a review/retro/demo session. Focus on: outcomes, feedback, "
        "lessons learned, and follow-up actions. Capture decisions clearly."
    ),
    "general": "",
}

analysis_agent = Agent(
    GEMINI_MODEL,
    output_type=MeetingAnalysis,
    system_prompt=BASE_PROMPT,
)


async def analyze_transcript(
    transcript: str, meeting_type: MeetingType = "general"
) -> MeetingAnalysis:
    hint = MEETING_TYPE_HINTS.get(meeting_type, "")
    prompt = f"نوع جلسه: {meeting_type}\n\nاین transcript را تحلیل کن:\n\n{transcript}"
    if hint:
        prompt += f"\n\nراهنما: {hint}"
    result = await analysis_agent.run(prompt)
    return result.output
