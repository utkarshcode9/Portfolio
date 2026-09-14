from rapidfuzz import fuzz
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Bug


def find_duplicate(db: Session, title: str, description: str, threshold: int) -> tuple[int | None, float]:
    candidates = db.scalars(select(Bug).order_by(Bug.created_at.desc()).limit(200)).all()
    incoming = f"{title} {description}".strip().lower()
    best_id = None
    best_score = 0.0
    for bug in candidates:
        existing = f"{bug.title} {bug.description}".strip().lower()
        score = float(fuzz.token_set_ratio(incoming, existing))
        if score > best_score:
            best_score = score
            best_id = bug.id
    if best_score >= threshold:
        return best_id, round(best_score, 2)
    return None, round(best_score, 2)
