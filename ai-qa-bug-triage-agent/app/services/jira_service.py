from __future__ import annotations
import httpx
from app.config import get_settings
from app.models import Bug

settings = get_settings()


def build_jira_payload(bug: Bug) -> dict:
    description = (
        f"AI Triage Summary:\n{bug.ai_summary}\n\n"
        f"Severity: {bug.severity}\nPriority: {bug.priority}\nCategory: {bug.category}\n"
        f"Confidence: {bug.confidence:.0%}\n\n"
        f"Reported Description:\n{bug.description}\n\n"
        f"Steps to Reproduce:\n{bug.steps_to_reproduce or 'Not provided'}\n\n"
        f"Expected Result:\n{bug.expected_result or 'Not provided'}\n\n"
        f"Actual Result:\n{bug.actual_result or 'Not provided'}\n\n"
        f"Environment:\n{bug.environment or 'Not provided'}\n\n"
        f"Investigation Hint:\n{bug.root_cause_hint}"
    )
    return {
        "fields": {
            "project": {"key": settings.jira_project_key},
            "summary": f"[{bug.severity.upper()}] {bug.title}",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [{"type": "paragraph", "content": [{"type": "text", "text": description}]}],
            },
            "issuetype": {"name": settings.jira_issue_type},
            "labels": ["ai-triage", f"severity-{bug.severity}", bug.category],
        }
    }


def create_jira_issue(bug: Bug) -> str:
    if not settings.jira_enabled:
        return "DEMO-NOT-CREATED"
    required = [settings.jira_base_url, settings.jira_email, settings.jira_api_token, settings.jira_project_key]
    if not all(required):
        raise RuntimeError("Jira is enabled but Jira configuration is incomplete.")
    url = f"{settings.jira_base_url.rstrip('/')}/rest/api/3/issue"
    with httpx.Client(timeout=20) as client:
        response = client.post(
            url,
            json=build_jira_payload(bug),
            auth=(settings.jira_email, settings.jira_api_token),
            headers={"Accept": "application/json", "Content-Type": "application/json"},
        )
        response.raise_for_status()
        return response.json().get("key", "")
