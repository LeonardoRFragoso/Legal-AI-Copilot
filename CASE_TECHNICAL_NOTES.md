# Technical Notes — Legal AI Copilot Case

## Architecture Overview

```
┌─────────────────────────────────────────────────────────┐
│                     Frontend (React)                     │
│  Login → Dashboard → Chat → Analysis → Reviews → Insights │
└────────────────────────┬────────────────────────────────┘
                         │ HTTP/JWT
┌────────────────────────▼────────────────────────────────┐
│                    Backend (FastAPI)                     │
│  ┌──────────┐  ┌────────────┐  ┌──────────────────┐    │
│  │Auth Routes│  │Agent Router│  │Analysis Records  │    │
│  │/auth/*    │  │(deterministic)│  │& Reviews API    │    │
│  └──────────┘  └────────────┘  └──────────────────┘    │
│  ┌──────────┐  ┌────────────┐  ┌──────────────────┐    │
│  │Automation│  │Risk Analyzer│  │Metrics Endpoint  │    │
│  │Service   │  │(heuristic) │  │/metrics/impact   │    │
│  └──────────┘  └────────────┘  └──────────────────┘    │
│  ┌──────────┐  ┌────────────┐  ┌──────────────────┐    │
│  │AI Validator│  │Webhook Svc │  │System Status    │    │
│  │(guardrails)│  │(n8n)      │  │/admin/system-status│  │
│  └──────────┘  └────────────┘  └──────────────────┘    │
└────────────────────────┬────────────────────────────────┘
                         │ SQLAlchemy ORM
┌────────────────────────▼────────────────────────────────┐
│                    SQLite (legal_ai.db)                  │
│  users | documents | chunks | embeddings | conversations│
│  messages | automation_runs | analysis_records | reviews │
└─────────────────────────────────────────────────────────┘
```

## Key Design Decisions

### 1. AnalysisRecord as Separate Entity
- **Decision**: Create a new `AnalysisRecord` model rather than reusing `AutomationRun`
- **Rationale**: AutomationRun tracks pipeline execution, not individual analyses. AnalysisRecord captures the reviewable output with structured data, confidence, and review history.
- **Trade-off**: Some data duplication between AutomationRun.summary_result and AnalysisRecord.structured_result, but separation of concerns is cleaner.

### 2. Append-Only Review History
- **Decision**: AnalysisReview entries are never modified or deleted
- **Rationale**: Audit trail integrity. Every review decision is traceable with timestamp, reviewer, and comment.
- **Implementation**: No update/delete endpoints for reviews. New entries are always appended.

### 3. State Machine with Validated Transitions
- **Decision**: Explicit state machine with `VALID_TRANSITIONS` dict
- **Rationale**: Prevents invalid status changes (e.g., APPROVED → REJECTED). Terminal states are enforced.
- **Implementation**: `validate_transition()` checks allowed transitions before creating reviews.

### 4. Deterministic Agent Router
- **Decision**: Keyword-based intent classification (no LLM for routing)
- **Rationale**: Predictable, testable, fast. LLM is used only for content generation.
- **Trade-off**: Less flexible than LLM-based routing, but sufficient for MVP scope.

### 5. Frontend Auth with localStorage
- **Decision**: Store JWT in localStorage with axios interceptor
- **Rationale**: Simple, works with page refresh, no cookie complexity
- **Trade-off**: XSS vulnerability if frontend is compromised. Acceptable for MVP.

### 6. Productivity Metrics as Estimates
- **Decision**: Use configurable manual time estimates, not measured benchmarks
- **Rationale**: No baseline data available. Configurable values allow adjustment.
- **Notice**: Frontend and API include explicit disclaimer about estimate nature.

## Database Schema (Stage 4 additions)

### analysis_records
- 14 indexed columns for efficient filtering
- JSON columns for structured_result and citations
- Self-referential FK for versioning (parent_analysis_id)
- FKs to documents, users, automation_runs, conversations, messages

### analysis_reviews
- 3 indexed columns (analysis_record_id, reviewer_user_id, created_at)
- FKs to analysis_records and users
- Append-only (no update/delete operations)

## Test Coverage

### New Tests (22 tests in test_analysis_review.py)
- AnalysisRecord creation and field validation
- State transition validation (7 tests)
- Review endpoint tests (10 tests): list, detail, approve, reject, comment validation, history, invalid transitions, 404, unauthenticated
- Metrics endpoint tests (2 tests)
- System status enhanced fields test (1 test)

### Pre-existing Tests (149 tests)
- Auth: JWT creation, validation, expiration, RBAC
- Agent Router: Intent classification, tool selection
- Agent Chat Integration: End-to-end chat flow with mocked LLM
- Risk Analysis: Heuristic keyword-based analysis, severity classification
- AI Validator: Guardrails, confidence scoring, citation validation
- Automation: Pipeline execution, webhook delivery, retry logic
- Config: Environment validation, secret key enforcement

## Migration Strategy

- Migration `b8678ebaa440` creates analysis_records and analysis_reviews tables
- Down migration cleanly drops both tables with indexes
- Migration is idempotent (safe to re-run after rollback)

## Known Limitations

1. **No automatic regeneration**: Versioning is structural only. Manual creation of new versions.
2. **No frontend tests**: No test framework configured for frontend. Validated via TypeScript build.
3. **Risk analysis is heuristic-only**: No LLM or semantic embedding-based retrieval (RAG). Uses keyword matching.
4. **SQLite**: Adequate for MVP. PostgreSQL recommended for production.
5. **No refresh token auto-refresh**: Frontend redirects to login on 401. No silent refresh.
6. **AIValidator imported but unused in risk analysis**: The validator is available but not called in the risk analysis flow.
7. **Citation similarity_score is fixed**: The value 0.7 is hardcoded, not computed from semantic similarity.
