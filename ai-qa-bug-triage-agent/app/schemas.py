from datetime import datetime
from typing import Literal
from pydantic import BaseModel, Field

Severity = Literal["critical", "high", "medium", "low"]
Priority = Literal["P0", "P1", "P2", "P3"]


class BugCreate(BaseModel):
    title: str = Field(min_length=5, max_length=255)
    description: str = Field(min_length=10)
    steps_to_reproduce: str = ""
    expected_result: str = ""
    actual_result: str = ""
    environment: str = ""
    reporter: str = "anonymous"
    customer_impact: str = ""


class TestCase(BaseModel):
    id: str
    title: str
    preconditions: str
    steps: list[str]
    expected_result: str
    type: Literal["positive", "negative", "edge", "regression", "integration"]


class TriageAnalysis(BaseModel):
    category: str
    severity: Severity
    priority: Priority
    confidence: float = Field(ge=0, le=1)
    summary: str
    root_cause_hint: str
    test_cases: list[TestCase]


class BugResponse(BaseModel):
    id: int
    title: str
    description: str
    category: str
    severity: str
    priority: str
    confidence: float
    ai_summary: str
    root_cause_hint: str
    test_cases: list[TestCase]
    duplicate_of: int | None
    duplicate_score: float
    requires_human_review: bool
    status: str
    jira_issue_key: str
    created_at: datetime


class ApprovalRequest(BaseModel):
    approved_by: str = Field(min_length=2)
    create_jira: bool = False
    comment: str = ""


class MetricsResponse(BaseModel):
    total_bugs: int
    pending_review: int
    critical_bugs: int
    high_bugs: int
    duplicates_detected: int
    approved: int
    jira_created: int
