# API Examples

## Health
```bash
curl http://localhost:8000/health
```

## Triage a defect
```bash
curl -X POST http://localhost:8000/api/v1/triage \
  -H "Content-Type: application/json" \
  -d '{
    "title": "UPI payment succeeds but order remains pending",
    "description": "Money is deducted but order is not confirmed.",
    "steps_to_reproduce": "Login -> cart -> checkout -> UPI -> pay",
    "expected_result": "Order confirmed",
    "actual_result": "Order pending",
    "environment": "QA / Chrome",
    "reporter": "qa.engineer",
    "customer_impact": "Money deducted; cannot checkout"
  }'
```

## Review queue
```bash
curl http://localhost:8000/api/v1/review-queue
```

## Approve a defect without Jira
```bash
curl -X POST http://localhost:8000/api/v1/bugs/1/approve \
  -H "Content-Type: application/json" \
  -d '{"approved_by":"QA Lead","create_jira":false,"comment":"Reviewed"}'
```

## Metrics
```bash
curl http://localhost:8000/api/v1/metrics
```
