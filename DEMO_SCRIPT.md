# Demo Script — Legal AI Copilot

## Prerequisites

1. Backend running: `cd backend && ENVIRONMENT=development python -m app.seed && uvicorn app.main:app --reload`
2. Frontend running: `cd frontend && npm run dev`
3. Browser open at `http://localhost:5173`

## Demo Flow

### Step 1: Login
1. Navigate to `http://localhost:5173` — redirects to `/login`
2. Click "Advogado" demo credential button (lawyer@demo.com / demo123456)
3. Click "Entrar"
4. Should land on Dashboard with navigation bar showing user name and role

### Step 2: Upload Document
1. Click "Upload" in navigation
2. Enter title: "Contrato de Prestação de Serviços"
3. Select the test PDF (`Contrato_Prestacao_Servicos_Teste.pdf`)
4. Click "Fazer Upload"
5. Wait for success message and redirect to Dashboard

### Step 3: Chat with Agent Router
1. Click "Chat" in navigation
2. Create a new conversation or select existing one
3. Type: "faça um resumo do documento"
4. Wait for AI response with structured content
5. Type: "identifique os riscos do contrato"
6. Observe risk analysis with severity badges and recommendations

### Step 4: View Risk Analysis
1. Click "Riscos" in navigation
2. Select the uploaded document
3. View detailed risk analysis with severity, category, and recommendations

### Step 5: Review Analyses
1. Click "Revisões" in navigation
2. Observe list of analyses generated from chat and direct endpoints
3. Filter by type (e.g., "Resumo") or status
4. Click an analysis to see full detail
5. Review the structured data, confidence score, and content summary
6. Click "Aprovar" to approve, or "Rejeitar" with a comment
7. Observe the review history updates

### Step 6: View Impact Metrics
1. Click "Métricas" in navigation
2. View the dashboard with:
   - Total documents and analyses
   - Estimated time saved
   - Approval rate
   - Analyses by type, risks by severity
   - Productivity estimates

### Step 7: Automations (Optional)
1. Click "Automações" in navigation
2. View automation runs from document upload
3. Observe progress, status, and webhook delivery

### Step 8: Admin View (Optional)
1. Logout and login as admin@demo.com / admin123456
2. View all users' analyses and metrics
3. Access system status at `/admin/system-status`

## Key Points to Highlight

- **Human-in-the-loop**: Every AI analysis is reviewable with append-only history
- **RBAC**: Lawyers can review, assistants can view, admins see everything
- **Productivity metrics**: Estimated time saved based on configurable manual times
- **Agent Router**: Deterministic intent classification routes to appropriate tools
- **Automation**: Post-upload pipeline with summary + risk analysis + webhook
- **Structured data**: Risk items with severity, category, citations, and recommendations
