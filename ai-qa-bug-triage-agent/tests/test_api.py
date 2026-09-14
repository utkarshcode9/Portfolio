
def sample_bug(title="UPI payment succeeds but order remains pending"):
    return {
        "title": title,
        "description": "Money is deducted but checkout remains pending after successful UPI payment.",
        "steps_to_reproduce": "Login -> checkout -> UPI -> pay",
        "expected_result": "Order confirmed",
        "actual_result": "Order pending",
        "environment": "QA / Chrome",
        "reporter": "qa.engineer",
        "customer_impact": "Money deducted; cannot checkout",
    }


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_triage_creates_structured_bug(client):
    r = client.post("/api/v1/triage", json=sample_bug())
    assert r.status_code == 201
    body = r.json()
    assert body["category"] == "payments"
    assert body["severity"] == "critical"
    assert body["priority"] == "P0"
    assert body["requires_human_review"] is True
    assert len(body["test_cases"]) >= 5


def test_duplicate_detection(client):
    first = client.post("/api/v1/triage", json=sample_bug()).json()
    second = client.post("/api/v1/triage", json=sample_bug("UPI payment successful but order still pending")).json()
    assert second["duplicate_of"] == first["id"]
    assert second["duplicate_score"] >= 82


def test_human_approval(client):
    bug = client.post("/api/v1/triage", json=sample_bug()).json()
    r = client.post(f"/api/v1/bugs/{bug['id']}/approve", json={"approved_by":"QA Lead","create_jira":False})
    assert r.status_code == 200
    assert r.json()["status"] == "approved"
    assert r.json()["requires_human_review"] is False


def test_metrics(client):
    client.post("/api/v1/triage", json=sample_bug())
    m = client.get("/api/v1/metrics").json()
    assert m["total_bugs"] == 1
    assert m["critical_bugs"] == 1
