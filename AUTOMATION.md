# Automation and Webhook Integration

## Overview

Post-upload automation runs summary and risk analysis asynchronously using FastAPI BackgroundTasks. Results are persisted in `automation_runs` table with status tracking. A webhook compatible with n8n emits `analysis.completed` events.

## Architecture

```
Document Upload -> BackgroundTasks -> Automation Service -> Summary + Risk Analysis -> Webhook -> n8n
```

### Key Components

- **`app/models.py`**: `AutomationRun` model with status, progress, results, webhook status
- **`app/automation_service.py`**: Creates runs, executes steps, updates status
- **`app/webhook_service.py`**: Sends `analysis.completed` webhook with retry, timeout, idempotency
- **`app/main.py`**: Upload endpoint triggers automation; automation endpoints for listing/retry
- **`n8n/analysis-completed-workflow.json`**: Example n8n workflow

## AutomationRun Model

| Field | Type | Description |
|-------|------|-------------|
| id | String (UUID) | Primary key |
| document_id | String FK | Related document |
| user_id | String FK | Owning user |
| automation_type | String | Default: `post_upload` |
| status | String | PENDING, RUNNING, COMPLETED, FAILED, PARTIAL_SUCCESS |
| current_step | String | DOCUMENT_PROCESSING, SUMMARY, RISK_ANALYSIS, WEBHOOK, COMPLETED |
| progress_percent | Integer | 0-100 |
| started_at | DateTime | When execution started |
| completed_at | DateTime | When execution completed |
| error_message | Text | Error details if failed |
| summary_result | JSON | Summary tool output |
| risk_result | JSON | Risk analysis output |
| webhook_status | String | pending, sent, failed |
| webhook_error | Text | Webhook error details |
| created_at | DateTime | Record creation |
| updated_at | DateTime | Last update |

## Automation Steps

1. **DOCUMENT_PROCESSING** (10%): Verify document exists
2. **SUMMARY** (30-50%): Run `summarize_document` tool
3. **RISK_ANALYSIS** (70-85%): Run `RiskAnalyzer.analyze()`
4. **WEBHOOK** (90%): Send `analysis.completed` event
5. **COMPLETED** (100%): Finalize status

## Status Values

- **PENDING**: Created, not yet started
- **RUNNING**: Currently executing
- **COMPLETED**: All steps succeeded, webhook sent
- **PARTIAL_SUCCESS**: Some steps had errors or webhook failed, but results persisted
- **FAILED**: Critical error, no results

## API Endpoints

### List Automation Runs
```
GET /automations/runs?document_id={id}&status={status}&skip=0&limit=20
```
Users see only their own runs. ADMIN sees all.

### Get Automation Run
```
GET /automations/runs/{run_id}
```

### Retry Failed Run
```
POST /automations/runs/{run_id}/retry
```
Only FAILED or PARTIAL_SUCCESS runs can be retried.

### System Status (ADMIN only)
```
GET /admin/system-status
```
Returns aggregated metrics: runs by status, total documents, total risk analyses, recent failures, avg duration, failed webhooks.

## Webhook Configuration

Environment variables in `.env`:

```
AUTOMATION_WEBHOOK_URL=https://n8n.example.com/webhook/legal-ai
AUTOMATION_WEBHOOK_TIMEOUT_SECONDS=10
AUTOMATION_WEBHOOK_MAX_RETRIES=3
AUTOMATION_WEBHOOK_ENABLED=true
```

## Webhook Payload

```json
{
  "event": "analysis.completed",
  "event_id": "uuid-v4",
  "timestamp": "ISO-8601",
  "document": {
    "id": "doc-uuid",
    "title": "Contract Title"
  },
  "automation": {
    "run_id": "run-uuid",
    "status": "COMPLETED"
  },
  "analysis": {
    "summary_available": true,
    "risk_analysis_available": true,
    "overall_risk": "high",
    "confidence_score": 85
  }
}
```

### Webhook Features

- **Idempotency key**: `X-Idempotency-Key` header with event UUID
- **Retry**: Up to `AUTOMATION_WEBHOOK_MAX_RETRIES` attempts
- **Timeout**: `AUTOMATION_WEBHOOK_TIMEOUT_SECONDS` per attempt
- **No sensitive data**: Payload contains no prompts, API keys, or user credentials

## n8n Workflow

Import `n8n/analysis-completed-workflow.json` into n8n. The workflow:
1. Receives webhook POST
2. Validates event type is `analysis.completed`
3. Checks if risk is high or critical
4. Sends email/Slack notification (disabled by default)
5. Responds OK

## Alembic Migration

```bash
# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

Migration file: `alembic/versions/4f38586d77d6_add_automation_runs_table.py`

## Frontend

The **Automations** page (`/automations`) displays:
- List of automation runs with status badges
- Progress bars for each run
- Filter by status
- Retry button for failed/partial runs
- Links to document and risk analysis
- Webhook status indicator

## Testing

Tests in `tests/test_automation.py` cover:
- AutomationRun model CRUD
- Endpoint access control (user vs admin)
- Background execution with mocked tools
- Webhook failure does not destroy results
- Webhook payload structure and no sensitive data
- Webhook retry, timeout, idempotency key
- System status endpoint (admin only)
