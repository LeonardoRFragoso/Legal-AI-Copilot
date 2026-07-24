# Human Review Workflow

## Overview

The Legal AI Copilot implements a human-in-the-loop review workflow for AI-generated analyses. Every analysis produced by the system — whether via chat, direct API, or automation — is persisted as an `AnalysisRecord` that can be reviewed, approved, rejected, or sent back for corrections.

## Architecture

### Models

**AnalysisRecord** (`analysis_records` table):
- `id`: UUID primary key
- `document_id`, `user_id`: ownership and document reference
- `automation_run_id`, `conversation_id`, `message_id`: optional source links
- `analysis_type`: SUMMARY, EXTRACTION, COMPARISON, QUESTION_ANSWERING, RISK_ANALYSIS
- `status`: GENERATED → PENDING_REVIEW → APPROVED/REJECTED/NEEDS_CHANGES
- `content_summary`: truncated text preview (500 chars)
- `structured_result`: full JSON result (risks, parties, etc.)
- `confidence_score`, `confidence_level`, `overall_risk`: quality indicators
- `citations`, `disclaimer`: provenance and legal disclaimer
- `model_name`, `prompt_version`: traceability
- `blocked`: flag for guardrail-blocked analyses
- `estimated_manual_minutes`, `estimated_time_saved_minutes`: productivity metrics
- `version`, `parent_analysis_id`: versioning support
- Timestamps: `created_at`, `updated_at`

**AnalysisReview** (`analysis_reviews` table):
- `id`: UUID primary key
- `analysis_record_id`: FK to AnalysisRecord
- `reviewer_user_id`: FK to User
- `previous_status`, `new_status`: transition record
- `decision`: APPROVE, REJECT, REQUEST_CHANGES
- `comment`: reviewer comment (required for REJECT and REQUEST_CHANGES)
- `created_at`: timestamp
- **Append-only**: reviews are never modified or deleted

### State Machine

```
GENERATED → PENDING_REVIEW → APPROVED (terminal)
                          → REJECTED → PENDING_REVIEW (re-review)
                          → NEEDS_CHANGES → PENDING_REVIEW (re-review)
                                        → APPROVED
                                        → REJECTED
```

Valid transitions are enforced by `validate_transition()` in `analysis_record_service.py`.

### RBAC

- **ADMIN**: Can view and review all analyses
- **LAWYER**: Can view and review own analyses (and analyses on documents they own)
- **ASSISTANT**: Can view own analyses, cannot review
- **CLIENT/VIEWER**: Can view own analyses, cannot review

## API Endpoints

| Method | Path | Description | Auth |
|--------|------|-------------|------|
| GET | `/analyses` | List analyses with filters | Any authenticated user |
| GET | `/analyses/{id}` | Get analysis detail with review history | Owner or ADMIN |
| POST | `/analyses/{id}/reviews` | Submit review decision | LAWYER or ADMIN |
| GET | `/analyses/{id}/reviews` | Get review history (chronological) | Owner or ADMIN |

### Filters (GET /analyses)
- `document_id`, `analysis_type`, `status`, `confidence_level`, `overall_risk`
- `created_from`, `created_to` (date range)
- `skip`, `limit` (pagination)

### Review Request
```json
{
  "decision": "APPROVE | REJECT | REQUEST_CHANGES",
  "comment": "Optional for APPROVE, required for REJECT and REQUEST_CHANGES"
}
```

## Frontend

The **Reviews** page (`/reviews`) provides:
- Filterable list of analyses (by type and status)
- Detail view with structured data, risks, citations, disclaimer
- Review form with three decision buttons
- Chronological review history display
- RBAC-aware UI (review buttons only shown for LAWYER/ADMIN)

## Persistence Points

AnalysisRecords are created in:
1. **Chat endpoint** — when Agent Router produces a reviewable intent (summary, extraction, risk, Q&A)
2. **Direct analysis endpoints** — `/analysis/summary`, `/analysis/extract`, `/analysis/compare`, `/analysis/risks`
3. **Automation service** — during post-upload automation (summary + risk analysis steps)

## Versioning

- `version` field starts at 1
- `parent_analysis_id` links to previous version
- New versions can be created when an analysis is regenerated after NEEDS_CHANGES
- The versioning is minimal and structural — no automatic regeneration endpoint in this stage
