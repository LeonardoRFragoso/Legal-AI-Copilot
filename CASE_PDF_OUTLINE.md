# Case PDF Outline — Legal AI Copilot

## Document Structure

### 1. Executive Summary
- Project objective: AI-powered contract analysis with human review
- MVP scope: Summary, extraction, risk analysis, Q&A, comparison
- Key differentiator: Human-in-the-loop review with audit trail

### 2. Problem Statement
- Manual contract review is time-consuming and error-prone
- Lawyers spend 30-120 minutes per contract on routine analysis
- Need for consistent, traceable, and reviewable AI assistance

### 3. Solution Architecture
- **Backend**: FastAPI + SQLAlchemy + SQLite
- **Frontend**: React + TypeScript + TailwindCSS
- **AI**: LangChain + OpenAI GPT-4 (with heuristic fallback)
- **Agent Router**: Deterministic intent classification
- **Automation**: Post-upload pipeline with webhook integration

### 4. Key Features

#### 4.1 Agent Router
- Deterministic keyword-based intent classification
- 5 intents: summarize, extract, compare, identify risks, Q&A
- Confidence scoring and fallback handling

#### 4.2 Risk Analysis
- Heuristic + LLM layered analysis
- Risk severity: low, medium, high, critical
- Risk categories: payment, liability, termination, confidentiality, etc.
- Citations with page numbers and excerpts
- Confidence score and disclaimer

#### 4.3 Human Review Workflow
- AnalysisRecord persistence for all AI outputs
- State machine: GENERATED → PENDING_REVIEW → APPROVED/REJECTED/NEEDS_CHANGES
- Append-only review history (AnalysisReview)
- RBAC: LAWYER/ADMIN can review, ASSISTANT can view
- Versioning support (parent_analysis_id, version number)

#### 4.4 Impact Metrics
- Estimated manual time vs. AI processing time
- Configurable reference values per analysis type
- Approval rate, confidence averages
- Risk distribution by severity
- Time saved estimates (hours)

#### 4.5 Automation
- Post-upload pipeline: process → summarize → risk analysis → webhook
- AutomationRun model with progress tracking
- Webhook integration with n8n (idempotency keys, retries)
- Error handling and retry capability

### 5. Security & RBAC
- JWT authentication (access + refresh tokens)
- Role-based access control: ADMIN, LAWYER, ASSISTANT, CLIENT, VIEWER
- Document ownership enforcement
- Password hashing with Argon2

### 6. Testing
- 149+ backend tests covering auth, agent, risk analysis, reviews, metrics
- Test categories: unit, integration, API, RBAC, state transitions
- Shared test database with per-test cleanup

### 7. Technology Decisions
- SQLite for MVP (no Docker required)
- LangChain for AI orchestration
- Alembic for database migrations
- Zustand for frontend state management
- TailwindCSS for styling

### 8. Limitations & Future Work
- No OCR (PDF text extraction only)
- No electronic signature
- No multi-agent orchestration
- No billing or subscription management
- Versioning is structural (no automatic regeneration)
- Metrics are estimates (not calibrated against real workflows)

### 9. Conclusion
- MVP demonstrates viable AI-assisted contract review
- Human-in-the-loop ensures quality and accountability
- Productivity metrics provide business value visibility
- Architecture supports incremental enhancement
