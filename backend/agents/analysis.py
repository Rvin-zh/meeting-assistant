import os

from pydantic_ai import Agent

from backend.config import GEMINI_MODEL, GOOGLE_API_KEY
from backend.models.schemas import MeetingAnalysis

if GOOGLE_API_KEY:
    os.environ.setdefault("GOOGLE_API_KEY", GOOGLE_API_KEY)

analysis_agent = Agent(
    GEMINI_MODEL,
    output_type=MeetingAnalysis,
    system_prompt=(
        "You analyze Persian meeting transcripts. "
        "Output UI fields in Persian: title, summary, key_points, decisions, and each task's title and context. "
        "Also output English fields for Jira (LTR): title_en (meeting), and per task title_en (issue summary) "
        "and context_en (issue description context). Keep title_en/context_en concise and professional in English. "
        "Tasks must be actionable. Priority: high, medium, or low."
    ),
)


async def analyze_transcript(transcript: str) -> MeetingAnalysis:
    prompt = f"این transcript جلسه را تحلیل کن:\n\n{transcript}"
    result = await analysis_agent.run(prompt)
    return result.output
