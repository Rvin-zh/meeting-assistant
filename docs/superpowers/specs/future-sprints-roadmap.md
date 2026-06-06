# Future Sprints Roadmap — Meeting Assistant

**Updated:** 2026-06-04  
**Advanced features (planned):** [2026-advanced-meeting-features.md](2026-advanced-meeting-features.md) · [قابلیت‌های-پیشرفته-آینده.html](../../قابلیت‌های-پیشرفته-آینده.html)
**Out of scope (for now):** Live streaming STT during meetings, professional speaker diarization, separate Cloud Speech-to-Text pipeline. **In MVP:** upload/record audio → Gemini transcription via `POST /api/transcribe` (same `GOOGLE_API_KEY`).

Sprint 1 (MVP) is complete. See [نقشه-اسپرینت‌ها.html](../../نقشه-اسپرینت‌ها.html) for the full Persian HTML version with diagrams.

---

## Sprint 2 — Archive & cross-meeting RAG

| Feature | Notes |
|---------|--------|
| Multi-meeting RAG | Filter by `org_id`, `project`, date range; Chroma metadata |
| Archive UI | List/search meetings; SQLite FTS5 on title + summary |
| Tags & project | `tags`, `project_key` columns |
| Export | Markdown/PDF summary from `MeetingAnalysis` |
| Compare agent | Cross-meeting decisions diff (`compare_agent`) |

**Acceptance:** One question spanning ≥2 meetings with citations; archive search &lt;500ms at ~100 meetings.

---

## Sprint 3 — Jira workflow

| Feature | Notes |
|---------|--------|
| Assignee mapping | Persian speaker name → Jira `accountId` table |
| `jira_agent` | Tools: search duplicates, preview, suggest epic |
| OAuth | Team Atlassian OAuth instead of personal API token |
| Human-in-the-loop | Edit tasks in UI before bulk create |
| Issue sync | Store `jira_keys_json` on tasks; link back in UI |
| Custom fields | Project-specific field map via config |

---

## Sprint 4 — Users, orgs, integrations

| Feature | Notes |
|---------|--------|
| Auth | JWT or OIDC (SSO) |
| Workspaces | `org_id` tenancy on all data |
| RBAC | admin / editor / viewer |
| Calendar metadata | Google Calendar read-only → prefill meeting form (transcript from text or voice upload) |
| Email digest | RTL HTML summary to attendees |
| Slack/Teams | Webhook notification after analysis |

---

## Sprint 5 — Scale & production

| Feature | Notes |
|---------|--------|
| PostgreSQL | Migrate from SQLite; Alembic |
| Vector scale | pgvector or Chroma Cloud |
| Background ingest | Queue + job status UI |
| Observability | OpenTelemetry, structured logs |
| Deploy | Docker Compose; optional Cloud Run |
| Eval harness | Golden transcripts; regression on summaries |
| Rate limits | Per-org quotas; embedding cache |

---

## Sprint 6+ — Product differentiation

- **Agents:** `review_agent`, `risk_agent`, `orchestrator`
- **`facilitation_agent`:** Post-meeting guide for organizers — efficient meetings, timeboxing, next agenda (see [advanced features spec](2026-advanced-meeting-features.md))
- **`alignment_agent`:** Upload SOW/contracts; compare meeting decisions vs scope — aligned / out-of-scope / unclear
- **`sentiment_agent`:** Per-speaker text tone analysis; concern flags; ethics/RBAC required
- **Decision tracking** across meetings
- **Action-item dashboard** (all open tasks)
- **Meeting templates** (standup, retro, planning prompts)
- **Speaker participation** analytics
- **Conflict detection** vs prior decisions
- **Follow-up agenda** generation
- **Confluence/Notion** publish
- **Analysis versioning** (human edits, partial re-run)
- **Privacy:** PII mask, retention, GDPR export
- **On-prem** optional deployment

---

## Priority matrix

| Priority | Item |
|----------|------|
| P0 | Multi-meeting RAG + archive FTS |
| P0 | Jira assignee mapping |
| P1 | Auth + workspace |
| P1 | Pre-create task editing |
| P1 | Facilitation guide (`facilitation_agent`) |
| P1 | SOW/contract upload + alignment report |
| P2 | PostgreSQL + job queue |
| P2 | Calendar metadata + email summary |
| P2 | Text sentiment per speaker (ethics opt-in) |
| P3 | Multi-agent, wiki export |

---

## Dependency chain

```
Sprint 1 (SQLite + Chroma)
  → Sprint 2 (multi-RAG)
  → Sprint 3 (Jira) — parallel with 2
  → Sprint 4 (auth/org) — needs 2+3 for real teams
  → Sprint 5 (Postgres/deploy)
  → Sprint 6+ (orchestration)
```
