from pathlib import Path
from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from app.config import get_settings
from app.db import Base, engine, get_db
from app.schemas import ApprovalRequest, BugCreate, BugResponse, MetricsResponse
from app.services.triage_service import approve_bug, list_bugs, metrics, triage_bug

settings = get_settings()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="AI-assisted QA defect triage with duplicate detection, test-case generation, human review and Jira integration.",
)

static_dir = Path(__file__).parent / "static"
app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", include_in_schema=False)
def dashboard():
    return FileResponse(static_dir / "index.html")


@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.app_name,
        "openai_enabled": bool(settings.use_openai and settings.openai_api_key),
        "jira_enabled": settings.jira_enabled,
    }


@app.post("/api/v1/triage", response_model=BugResponse, status_code=201)
def triage(payload: BugCreate, db: Session = Depends(get_db)):
    return triage_bug(db, payload)


@app.get("/api/v1/bugs", response_model=list[BugResponse])
def bugs(
    status: str | None = Query(default=None),
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
):
    return list_bugs(db, status=status, limit=limit)


@app.get("/api/v1/review-queue", response_model=list[BugResponse])
def review_queue(db: Session = Depends(get_db)):
    return list_bugs(db, status="pending_review", limit=200)


@app.post("/api/v1/bugs/{bug_id}/approve", response_model=BugResponse)
def approve(bug_id: int, payload: ApprovalRequest, db: Session = Depends(get_db)):
    try:
        return approve_bug(db, bug_id, payload)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Approval/Jira action failed: {exc}") from exc


@app.get("/api/v1/metrics", response_model=MetricsResponse)
def get_metrics(db: Session = Depends(get_db)):
    return metrics(db)
