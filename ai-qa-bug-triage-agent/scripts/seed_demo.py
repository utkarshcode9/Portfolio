from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.db import Base, SessionLocal, engine
from app.schemas import BugCreate
from app.services.triage_service import triage_bug

Base.metadata.create_all(bind=engine)

samples = [
    BugCreate(title="UPI payment succeeds but order remains pending", description="Money is deducted after successful UPI payment but the order is not confirmed.", steps_to_reproduce="Checkout -> UPI -> pay -> return", actual_result="Pending order", expected_result="Confirmed order", environment="Chrome / Android", customer_impact="Money deducted; cannot checkout"),
    BugCreate(title="Login button overlaps password field on mobile", description="On 320px viewport the login button overlaps the password field.", environment="Chrome mobile 320px"),
    BugCreate(title="Search API returns 500 for special characters", description="GET /search returns HTTP 500 when query contains % or & symbols.", environment="QA API"),
    BugCreate(title="Dashboard takes 18 seconds to load", description="Dashboard loading is slow for accounts with more than 20k records.", environment="QA"),
]

db = SessionLocal()
try:
    for item in samples:
        result = triage_bug(db, item)
        print(f"Seeded #{result.id}: {result.title} -> {result.severity}/{result.priority}")
finally:
    db.close()
