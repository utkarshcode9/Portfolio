from pathlib import Path
import csv
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.schemas import BugCreate
from app.services.ai_service import deterministic_analysis


def main():
    source = Path(__file__).resolve().parents[1] / "sample_data" / "bugs.csv"
    rows = list(csv.DictReader(source.open(encoding="utf-8")))
    severity_correct = 0
    category_correct = 0
    print("ID | Expected severity/category | Predicted severity/category")
    print("-" * 78)
    for i, row in enumerate(rows, start=1):
        result = deterministic_analysis(BugCreate(title=row["title"], description=row["description"]))
        severity_correct += result.severity == row["expected_severity"]
        category_correct += result.category == row["expected_category"]
        print(f"{i:02d} | {row['expected_severity']}/{row['expected_category']} | {result.severity}/{result.category}")
    total = len(rows)
    print("-" * 78)
    print(f"Severity accuracy: {severity_correct}/{total} = {severity_correct/total:.1%}")
    print(f"Category accuracy: {category_correct}/{total} = {category_correct/total:.1%}")
    print("Note: This starter set is intentionally small. Expand it before quoting metrics on a resume.")


if __name__ == "__main__":
    main()
