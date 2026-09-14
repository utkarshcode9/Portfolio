import json
from app.config import get_settings
from app.schemas import BugCreate, TriageAnalysis
from app.services.rules import classify_category, classify_severity, normalize_text, priority_from_severity, root_cause_hint
from app.services.case_generator import generate_test_cases

settings = get_settings()


def deterministic_analysis(bug: BugCreate) -> TriageAnalysis:
    text = normalize_text(
        bug.title, bug.description, bug.steps_to_reproduce,
        bug.expected_result, bug.actual_result, bug.environment
    )
    category = classify_category(text)
    severity = classify_severity(text, bug.customer_impact)
    priority = priority_from_severity(severity, text)
    confidence = 0.82 if category != "other" else 0.72
    return TriageAnalysis(
        category=category,
        severity=severity,
        priority=priority,
        confidence=confidence,
        summary=f"{bug.title}. Classified as {category} with {severity} severity and {priority} priority.",
        root_cause_hint=root_cause_hint(category, text),
        test_cases=generate_test_cases(category, bug.title),
    )


def analyze_bug(bug: BugCreate) -> TriageAnalysis:
    fallback = deterministic_analysis(bug)
    if not (settings.use_openai and settings.openai_api_key):
        return fallback

    try:
        from openai import OpenAI
    except ImportError:
        return fallback
    client = OpenAI(api_key=settings.openai_api_key)
    prompt = f"""
You are a senior QA defect triage assistant. Return ONLY valid JSON, no markdown.
Use these allowed severity values: critical, high, medium, low.
Use these allowed priority values: P0, P1, P2, P3.
Do not invent evidence. Keep confidence between 0 and 1.

Bug title: {bug.title}
Description: {bug.description}
Steps: {bug.steps_to_reproduce}
Expected: {bug.expected_result}
Actual: {bug.actual_result}
Environment: {bug.environment}
Customer impact: {bug.customer_impact}

Return this exact JSON shape:
{{
  "category": "payments|authentication|api|performance|ui|data|network|other",
  "severity": "critical|high|medium|low",
  "priority": "P0|P1|P2|P3",
  "confidence": 0.0,
  "summary": "concise triage summary",
  "root_cause_hint": "investigation hint, not a claimed root cause"
}}
"""
    try:
        response = client.responses.create(model=settings.openai_model, input=prompt)
        data = json.loads(response.output_text)
        ai_core = {
            "category": data.get("category", fallback.category),
            "severity": data.get("severity", fallback.severity),
            "priority": data.get("priority", fallback.priority),
            "confidence": float(data.get("confidence", fallback.confidence)),
            "summary": data.get("summary", fallback.summary),
            "root_cause_hint": data.get("root_cause_hint", fallback.root_cause_hint),
            "test_cases": generate_test_cases(data.get("category", fallback.category), bug.title),
        }
        return TriageAnalysis(**ai_core)
    except Exception:
        return fallback
