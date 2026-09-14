from __future__ import annotations

CATEGORY_KEYWORDS = {
    "payments": ["payment", "upi", "card", "refund", "transaction", "charged", "billing", "invoice"],
    "authentication": ["login", "sign in", "signin", "password", "otp", "authentication", "session", "mfa"],
    "api": ["api", "endpoint", "500", "502", "503", "response code", "payload", "callback", "webhook"],
    "performance": ["slow", "latency", "timeout", "hang", "freeze", "performance", "loading"],
    "ui": ["button", "alignment", "color", "font", "layout", "overlap", "responsive", "ui", "typo"],
    "data": ["data", "missing record", "duplicate record", "duplicate", "two records", "creates two", "wrong value", "corrupt", "database"],
    "network": ["network", "vpn", "connection", "offline", "dns"],
}

CRITICAL_TERMS = [
    "data loss", "security breach", "production down", "service down", "all users", "money deducted",
    "charged twice", "payment deducted", "cannot checkout", "crash on launch", "system unavailable"
]
LOW_TERMS = ["typo", "spacing", "alignment", "minor ui", "cosmetic", "wrong color", "font size"]
HIGH_TERMS = ["login failed", "login fails", "cannot login", "checkout", "payment failed", "500 error", "returns 500", "http 500", "blocking", "crash"]


def normalize_text(*parts: str) -> str:
    return " ".join(p or "" for p in parts).lower()


def classify_category(text: str) -> str:
    scores = {category: sum(1 for word in words if word in text) for category, words in CATEGORY_KEYWORDS.items()}
    best = max(scores, key=scores.get)
    return best if scores[best] > 0 else "other"


def classify_severity(text: str, customer_impact: str = "") -> str:
    joined = f"{text} {customer_impact.lower()}"
    if any(term in joined for term in CRITICAL_TERMS):
        return "critical"
    if any(term in joined for term in LOW_TERMS):
        return "low"
    if any(term in joined for term in HIGH_TERMS):
        return "high"
    if any(term in joined for term in ["multiple users", "production", "major feature", "unable to proceed"]):
        return "high"
    return "medium"


def priority_from_severity(severity: str, text: str) -> str:
    if severity == "critical":
        return "P0"
    if severity == "high":
        return "P1"
    if severity == "low":
        return "P3"
    if "production" in text or "customer" in text:
        return "P1"
    return "P2"


def root_cause_hint(category: str, text: str) -> str:
    hints = {
        "payments": "Check payment-provider callback/webhook handling, transaction state reconciliation and idempotency.",
        "authentication": "Check identity provider response, token/session expiry, OTP/MFA validation and authorization logs.",
        "api": "Check API logs, request payload validation, dependency health and recent backend deployments.",
        "performance": "Check latency traces, slow queries, downstream timeouts, resource saturation and caching.",
        "ui": "Check DOM/CSS regression, responsive breakpoints, browser-specific rendering and recent UI changes.",
        "data": "Check database constraints, transformation logic, race conditions and data synchronization jobs.",
        "network": "Check service reachability, DNS/VPN configuration, proxy rules and network error logs.",
        "other": "Compare failing and working paths, inspect logs and recent changes, then tighten reproduction steps.",
    }
    return hints.get(category, hints["other"])
