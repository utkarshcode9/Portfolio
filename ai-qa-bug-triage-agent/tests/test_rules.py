from app.services.rules import classify_category, classify_severity, priority_from_severity


def test_payment_category():
    assert classify_category("upi payment deducted but order pending") == "payments"


def test_critical_money_deducted():
    assert classify_severity("payment deducted but order not created") == "critical"


def test_low_cosmetic_bug():
    assert classify_severity("minor ui alignment issue") == "low"


def test_priority_mapping():
    assert priority_from_severity("critical", "") == "P0"
    assert priority_from_severity("high", "") == "P1"
    assert priority_from_severity("low", "") == "P3"
