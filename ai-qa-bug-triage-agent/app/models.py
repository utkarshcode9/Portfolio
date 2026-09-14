from datetime import datetime, timezone
from sqlalchemy import Boolean, DateTime, Float, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column
from app.db import Base


class Bug(Base):
    __tablename__ = "bugs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String(255), index=True)
    description: Mapped[str] = mapped_column(Text)
    steps_to_reproduce: Mapped[str] = mapped_column(Text, default="")
    expected_result: Mapped[str] = mapped_column(Text, default="")
    actual_result: Mapped[str] = mapped_column(Text, default="")
    environment: Mapped[str] = mapped_column(String(255), default="")
    reporter: Mapped[str] = mapped_column(String(120), default="anonymous")

    category: Mapped[str] = mapped_column(String(50), default="other")
    severity: Mapped[str] = mapped_column(String(20), default="medium")
    priority: Mapped[str] = mapped_column(String(20), default="P2")
    confidence: Mapped[float] = mapped_column(Float, default=0.0)
    ai_summary: Mapped[str] = mapped_column(Text, default="")
    root_cause_hint: Mapped[str] = mapped_column(Text, default="")
    test_cases_json: Mapped[str] = mapped_column(Text, default="[]")

    duplicate_of: Mapped[int | None] = mapped_column(Integer, nullable=True)
    duplicate_score: Mapped[float] = mapped_column(Float, default=0.0)
    requires_human_review: Mapped[bool] = mapped_column(Boolean, default=False)
    status: Mapped[str] = mapped_column(String(30), default="triaged")
    jira_issue_key: Mapped[str] = mapped_column(String(50), default="")

    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    approved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
