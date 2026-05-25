const API_BASE = import.meta.env.PUBLIC_API_URL ?? '';

export interface MeetingTask {
  title: string;
  assignee?: string | null;
  deadline?: string | null;
  priority: 'high' | 'medium' | 'low';
  context: string;
}

export interface MeetingAnalysis {
  title: string;
  summary: string;
  key_points: string[];
  decisions: string[];
  tasks: MeetingTask[];
}

export interface MeetingRecord {
  id: string;
  title: string;
  transcript: string;
  analysis: MeetingAnalysis;
  created_at: string;
  source: string;
}

export interface RagAnswer {
  answer: string;
  sources: { speaker: string; chunk_id: string; excerpt?: string; text?: string }[];
  used_meeting_context?: boolean;
}

export interface JiraPreviewIssue {
  summary: string;
  description: string;
  priority: string;
  task_index: number;
}

async function request<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${API_BASE}${path}`, {
    headers: { 'Content-Type': 'application/json', ...(init?.headers ?? {}) },
    ...init,
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: res.statusText }));
    throw new Error(err.detail ?? 'خطای سرور');
  }
  return res.json();
}

export const api = {
  health: () => request<{ status: string; google_api: boolean; jira_configured: boolean }>('/api/health'),
  listMeetings: () => request<MeetingRecord[]>('/api/meetings'),
  listSynthetic: () => request<{ id: string; filename: string; title: string }[]>('/api/meetings/synthetic'),
  createFromSynthetic: (id: string) =>
    request<MeetingRecord>(`/api/meetings/synthetic/${id}`, { method: 'POST' }),
  createMeeting: (transcript: string, title?: string) =>
    request<MeetingRecord>('/api/meetings', {
      method: 'POST',
      body: JSON.stringify({ transcript, title }),
    }),
  getMeeting: (id: string) => request<MeetingRecord>(`/api/meetings/${id}`),
  ask: (id: string, question: string) =>
    request<RagAnswer>(`/api/meetings/${id}/ask`, {
      method: 'POST',
      body: JSON.stringify({ question }),
    }),
  jiraPreview: (id: string) =>
    request<{ issues: JiraPreviewIssue[] }>(`/api/meetings/${id}/jira/preview`, { method: 'POST' }),
  jiraCreate: (id: string, task_indices?: number[]) =>
    request<{ created: { key: string; summary: string }[] }>(`/api/meetings/${id}/jira/create`, {
      method: 'POST',
      body: JSON.stringify({ task_indices }),
    }),
};
