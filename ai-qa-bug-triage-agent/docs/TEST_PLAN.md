# Test Plan — AI QA / Bug Triage Automation Agent

## Objective
Validate classification, severity/priority assignment, duplicate detection, test-case generation, human-review routing, API behavior and optional Jira handoff.

## Functional test cases
| ID | Scenario | Expected result |
|---|---|---|
| QA-001 | Payment deducted but order not confirmed | Category `payments`, severity `critical`, priority `P0`, human review required |
| QA-002 | Valid OTP but login blocked | Category `authentication`, high/P1 |
| QA-003 | UI alignment issue | Category `ui`, low/P3 |
| QA-004 | API returns 500 | Category `api`, high/P1 |
| QA-005 | Slow dashboard | Category `performance`, test cases include performance validation |
| QA-006 | Submit same defect twice | Second defect contains `duplicate_of` and similarity >= configured threshold |
| QA-007 | Critical defect created | Status is `pending_review` |
| QA-008 | Approve pending defect | Status becomes `approved` and human review flag is cleared |
| QA-009 | Invalid bug title/description | API returns 422 validation error |
| QA-010 | Jira disabled and approve without Jira | Approval succeeds locally |
| QA-011 | Metrics after defects | Dashboard counts match stored data |
| QA-012 | OpenAI disabled | Deterministic fallback still generates complete triage output |

## Non-functional checks
- API health endpoint responds successfully.
- No credentials are committed to Git.
- Application starts in Docker and local Python environments.
- High-impact defects cannot bypass the configured human-review policy.
- AI failure falls back to deterministic logic instead of breaking intake.
