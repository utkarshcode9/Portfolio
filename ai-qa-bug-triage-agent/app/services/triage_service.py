import json
from datetime import datetime, timezone
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from app.config import get_settings
from app.models import Bug
from app.schemas import ApprovalRequest, BugCreate, BugResponse, MetricsResponse, TestCase
from app.services.ai_service import analyze_bug
from app.services.duplicate_service import find_duplicate
from app.services.jira_service import create_jira_issue

settings = get_settings()


def bug_to_response(bug: Bug) -> BugResponse:
    test_cases = [TestCase(**item) for item in json.loads(bug.test_cases_json or "[]")]
    return BugResponse(
        id=bug.id,
        title=bug.title,
        description=bug.description,
        category=bug.category,
        severity=bug.severity,
        priority=bug.priority,
        confidence=bug.confidence,
        ai_summary=bug.ai_summary,
        root_cause_hint=bug.root_cause_hint,
        test_cases=test_cases,
        duplicate_of=bug.duplicate_of,
        duplicate_score=bug.duplicate_score,
        requires_human_review=bug.requires_human_review,
        status=bug.status,
        jira_issue_key=bug.jira_issue_key,
        created_at=bug.created_at,
    )


def triage_bug(db: Session, incoming: BugCreate) -> BugResponse:
    analysis = analyze_bug(incoming)
    duplicate_of, duplicate_score = find_duplicate(
        db, incoming.title, incoming.description, settings.duplicate_threshold
    )
    requires_review = (
        analysis.severity in settings.review_severities
        or analysis.confidence < 0.75
        or duplicate_of is not None
    )
    status = "pending_review" if requires_review else "approved"
    bug = Bug(
        **incoming.model_dump(exclude={"customer_impact"}),
        category=analysis.category,
        severity=analysis.severity,
        priority=analysis.priority,
        confidence=analysis.confidence,
        ai_summary=analysis.summary,
        root_cause_hint=analysis.root_cause_hint,
        test_cases_json=json.dumps([tc.model_dump() for tc in analysis.test_cases]),
        duplicate_of=duplicate_of,
        duplicate_score=duplicate_score,
        requires_human_review=requires_review,
        status=status,
        approved_at=None if requires_review else datetime.now(timezone.utc),
    )
    db.add(bug)
    db.commit()
    db.refresh(bug)
    return bug_to_response(bug)


def approve_bug(db: Session, bug_id: int, approval: ApprovalRequest) -> BugResponse:
    bug = db.get(Bug, bug_id)
    if not bug:
        raise KeyError("Bug not found")
    bug.status = "approved"
    bug.requires_human_review = False
    bug.approved_at = datetime.now(timezone.utc)
    if approval.create_jira:
        bug.jira_issue_key = create_jira_issue(bug)
    db.commit()
    db.refresh(bug)
    return bug_to_response(bug)


def list_bugs(db: Session, status: str | None = None, limit: int = 100) -> list[BugResponse]:
    stmt = select(Bug).order_by(Bug.created_at.desc()).limit(limit)
    if status:
        stmt = stmt.where(Bug.status == status)
    return [bug_to_response(b) for b in db.scalars(stmt).all()]


def metrics(db: Session) -> MetricsResponse:
    def count_where(*conditions) -> int:
        stmt = select(func.count()).select_from(Bug)
        for condition in conditions:
            stmt = stmt.where(condition)
        return int(db.scalar(stmt) or 0)

    return MetricsResponse(
        total_bugs=count_where(),
        pending_review=count_where(Bug.status == "pending_review"),
        critical_bugs=count_where(Bug.severity == "critical"),
        high_bugs=count_where(Bug.severity == "high"),
        duplicates_detected=count_where(Bug.duplicate_of.is_not(None)),
        approved=count_where(Bug.status == "approved"),
        jira_created=count_where(Bug.jira_issue_key != ""),
    )
