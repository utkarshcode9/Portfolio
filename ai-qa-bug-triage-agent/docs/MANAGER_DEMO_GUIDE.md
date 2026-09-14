# Manager Demo Guide

## 5-minute demo story
1. Open `http://localhost:8000` and show health/metrics.
2. Submit the pre-filled UPI payment defect.
3. Highlight automatic category, `critical` severity, `P0` priority and generated test cases.
4. Explain why it is routed to **human review**: the system does not let high-impact AI decisions silently create external tickets.
5. Submit a similar payment defect and show duplicate detection.
6. Approve the defect from the review queue.
7. Open `/docs` to show the REST API and mention n8n/Jira integration.
8. Show `n8n/ai_bug_triage_workflow.json` and explain webhook → triage → review decision → response.

## Business value
- Standardizes defect triage quality.
- Reduces repetitive manual classification.
- Surfaces possible duplicates before engineers spend time investigating them.
- Generates a first-pass regression test set.
- Keeps humans in the loop for critical/high-risk defects.
- Provides an audit-friendly API/database record for every triage result.

## Important positioning
This is an **AI-assisted QA workflow**, not an autonomous replacement for QA leads. Severity, priority and suspected root-cause output are recommendations; high-impact issues are deliberately routed to a human reviewer.
