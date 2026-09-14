from app.schemas import TestCase


def generate_test_cases(category: str, title: str) -> list[TestCase]:
    common = [
        TestCase(
            id="TC-01",
            title=f"Reproduce reported defect: {title[:80]}",
            preconditions="Test environment matches the reported environment and required test data is available.",
            steps=["Open the affected workflow", "Follow the reported steps", "Observe system behavior and logs"],
            expected_result="Application completes the workflow without the reported defect.",
            type="regression",
        ),
        TestCase(
            id="TC-02",
            title="Validate expected happy path",
            preconditions="Valid user and valid data are available.",
            steps=["Start the workflow with valid inputs", "Complete all required actions", "Verify final state"],
            expected_result="Happy path completes successfully with correct data and UI state.",
            type="positive",
        ),
        TestCase(
            id="TC-03",
            title="Validate invalid or missing input handling",
            preconditions="User can access the affected workflow.",
            steps=["Submit invalid or incomplete input", "Observe validation", "Retry with corrected input"],
            expected_result="Clear validation is shown and the system remains stable.",
            type="negative",
        ),
        TestCase(
            id="TC-04",
            title="Validate retry and duplicate-action behavior",
            preconditions="Workflow is available and test data can be repeated.",
            steps=["Perform the action", "Repeat or retry the same action quickly", "Verify final state and records"],
            expected_result="Repeated actions do not create inconsistent or duplicate results.",
            type="edge",
        ),
    ]

    specialized = {
        "payments": TestCase(
            id="TC-05", title="Payment callback and reconciliation validation",
            preconditions="Payment sandbox/test method is configured.",
            steps=["Start payment", "Complete payment successfully", "Delay/replay callback", "Verify order and payment state"],
            expected_result="Payment and order states remain consistent and duplicate callbacks are handled safely.", type="integration"
        ),
        "authentication": TestCase(
            id="TC-05", title="Session and authentication boundary validation",
            preconditions="Valid and invalid credentials/test sessions are available.",
            steps=["Login successfully", "Expire or invalidate session", "Retry protected action", "Re-authenticate"],
            expected_result="Session rules are enforced and valid users can recover cleanly.", type="integration"
        ),
        "api": TestCase(
            id="TC-05", title="API dependency failure and recovery validation",
            preconditions="API endpoint can be tested with controlled responses.",
            steps=["Send valid request", "Simulate 5xx/timeout", "Retry request", "Validate logs and final response"],
            expected_result="Errors are handled gracefully and retry behavior does not corrupt state.", type="integration"
        ),
        "performance": TestCase(
            id="TC-05", title="Performance threshold validation",
            preconditions="Representative test data and timing tools are available.",
            steps=["Measure baseline", "Repeat workflow under increased load", "Capture latency", "Compare with target"],
            expected_result="Response time remains within agreed performance threshold.", type="integration"
        ),
        "ui": TestCase(
            id="TC-05", title="Cross-browser and responsive UI validation",
            preconditions="Chromium, Firefox and WebKit/mobile viewport are available.",
            steps=["Open affected page in each browser", "Check desktop and mobile widths", "Validate interaction and layout"],
            expected_result="UI remains usable, aligned and consistent across supported browsers/viewports.", type="regression"
        ),
    }
    common.append(specialized.get(category, TestCase(
        id="TC-05", title="Adjacent workflow regression validation",
        preconditions="Related features and representative data are available.",
        steps=["Complete the affected workflow", "Navigate to related workflow", "Verify saved state and downstream behavior"],
        expected_result="Fix does not introduce regression in adjacent functionality.", type="regression"
    )))
    return common
