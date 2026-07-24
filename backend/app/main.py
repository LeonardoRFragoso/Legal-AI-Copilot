from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Form, BackgroundTasks, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.models import Document, Chunk, DocumentEmbedding, Conversation, Message, User, UserRole
from app.repositories import DocumentRepository, ChunkRepository, EmbeddingRepository, ConversationRepository, UserRepository
from app.pdf_extractor import PDFExtractor
from app.chunker import Chunker
from app.embedding_service import EmbeddingService
from app.legal_agent import LegalAgent
from app.schemas import (
    DocumentResponse, MessageCreate, MessageResponse, 
    ConversationCreate, ConversationResponse,
    SummaryRequest, SummaryResponse,
    ExtractionRequest, ExtractionResponse,
    ComparisonRequest, ComparisonResponse,
    RiskAnalysisRequest, RiskAnalysisResponse,
    RiskItem, CitationSourceSchema,
    AutomationRunResponse
)
from app.logger import logger
from app.validators import ResponseValidator
from app.auth import get_current_user, require_role
from app.auth_routes import router as auth_router
from app.ai_validator import AIValidator, CitationSource
from app.agent_router import LegalAgentRouter, AgentIntent
from app.risk_analysis import RiskAnalyzer
from app.agent_executor import router as agent_router, execute_agent_decision
from app.automation_service import (
    create_automation_run,
    run_post_upload_automation,
    update_run_status,
)
from app.models import AutomationRun
from typing import List, Optional
from datetime import datetime
import os
import uuid
import json

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Legal AI Copilot")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register authentication routes
app.include_router(auth_router)

# Initialize services
pdf_extractor = PDFExtractor()
chunker = Chunker()
embedding_service = EmbeddingService()
legal_agent = LegalAgent()


@app.get("/")
def root():
    return {"message": "Legal AI Copilot API"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/documents/upload", response_model=DocumentResponse)
async def upload_document(
    background_tasks: BackgroundTasks,
    title: str = Form(...),
    file: UploadFile = File(...),
    current_user: User = Depends(require_role(UserRole.LAWYER, UserRole.ASSISTANT, UserRole.ADMIN)),
    db: Session = Depends(get_db)
):
    try:
        # Read file
        file_bytes = await file.read()
        
        # Extract text
        text, page_count = pdf_extractor.extract_text(file_bytes)
        
        # Save file (in production, use Supabase Storage)
        file_path = f"uploads/{uuid.uuid4()}_{file.filename}"
        os.makedirs("uploads", exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        
        # Create document
        doc_repo = DocumentRepository(db)
        document = doc_repo.create(title, file.filename, file_path, page_count)
        document.user_id = current_user.id
        db.commit()
        db.refresh(document)
        
        # Chunk text
        chunks_data = chunker.chunk_text(text)
        for chunk in chunks_data:
            chunk["document_id"] = document.id
        
        chunk_repo = ChunkRepository(db)
        chunks = chunk_repo.create_batch(chunks_data)
        
        # Generate embeddings (skip if API key not configured)
        if embedding_service.embeddings:
            try:
                texts = [chunk.text for chunk in chunks]
                embeddings = embedding_service.generate_embeddings_batch(texts)
                
                embeddings_data = []
                for chunk, embedding in zip(chunks, embeddings):
                    embeddings_data.append({
                        "chunk_id": chunk.id,
                        "document_id": document.id,
                        "embedding": embedding
                    })
                
                emb_repo = EmbeddingRepository(db)
                emb_repo.create_batch(embeddings_data)
            except Exception as e:
                logger.warning(f"Failed to generate embeddings: {str(e)}. Document will be processed without embeddings.")
        
        # Update status
        doc_repo.update_status(document.id, "ready")
        
        # Create automation run and schedule background processing
        automation_run = create_automation_run(
            db, document.id, current_user.id
        )
        background_tasks.add_task(
            run_post_upload_automation,
            run_id=automation_run.id,
            document_id=document.id,
            user_id=current_user.id,
        )
        
        return document
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/documents", response_model=List[DocumentResponse])
def list_documents(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc_repo = DocumentRepository(db)
    if current_user.role == UserRole.ADMIN:
        return doc_repo.list_all()
    else:
        # Non-admin users see only their documents
        return db.query(Document).filter(Document.user_id == current_user.id).order_by(Document.created_at.desc()).all()


@app.get("/documents/{document_id}", response_model=DocumentResponse)
def get_document(
    document_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    doc_repo = DocumentRepository(db)
    document = doc_repo.get(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check access: ADMIN can access all, others only their own
    if current_user.role != UserRole.ADMIN and document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return document


@app.delete("/documents/{document_id}")
def delete_document(
    document_id: str,
    current_user: User = Depends(require_role(UserRole.LAWYER, UserRole.ASSISTANT, UserRole.ADMIN)),
    db: Session = Depends(get_db)
):
    doc_repo = DocumentRepository(db)
    document = doc_repo.get(document_id)
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    # Check access: ADMIN can delete all, others only their own
    if current_user.role != UserRole.ADMIN and document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if not doc_repo.delete(document_id):
        raise HTTPException(status_code=404, detail="Document not found")
    return {"message": "Document deleted"}


@app.post("/documents/{document_id}/regenerate-embeddings")
def regenerate_embeddings(document_id: str, db: Session = Depends(get_db)):
    try:
        doc_repo = DocumentRepository(db)
        document = doc_repo.get(document_id)
        if not document:
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Get chunks
        chunk_repo = ChunkRepository(db)
        chunks = chunk_repo.get_by_document(document_id)
        
        if not chunks:
            raise HTTPException(status_code=400, detail="No chunks found for document")
        
        # Generate embeddings
        if embedding_service.embeddings:
            try:
                texts = [chunk.text for chunk in chunks]
                embeddings = embedding_service.generate_embeddings_batch(texts)
                
                embeddings_data = []
                for chunk, embedding in zip(chunks, embeddings):
                    embeddings_data.append({
                        "chunk_id": chunk.id,
                        "document_id": document_id,
                        "embedding": embedding
                    })
                
                # Delete old embeddings first
                db.query(DocumentEmbedding).filter(DocumentEmbedding.document_id == document_id).delete()
                db.commit()
                
                # Create new embeddings
                emb_repo = EmbeddingRepository(db)
                emb_repo.create_batch(embeddings_data)
                
                return {"message": f"Embeddings regenerated for {len(embeddings_data)} chunks"}
            except Exception as e:
                logger.error(f"Failed to regenerate embeddings: {str(e)}")
                raise HTTPException(status_code=500, detail=f"Failed to regenerate embeddings: {str(e)}")
        else:
            raise HTTPException(status_code=400, detail="OPENAI_API_KEY not configured")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error regenerating embeddings: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/conversations", response_model=ConversationResponse)
def create_conversation(
    conversation: ConversationCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conv_repo = ConversationRepository(db)
    new_conv = conv_repo.create(
        document_id=conversation.document_id,
        title=conversation.title,
        user_id=current_user.id
    )
    
    # If document_id is provided, add context message with analysis
    if conversation.document_id:
        try:
            doc_repo = DocumentRepository(db)
            document = doc_repo.get(conversation.document_id)
            
            if document:
                # Generate summary and extraction for context
                summary_result = legal_agent.tools[1]._run(str(conversation.document_id))
                extraction_result = legal_agent.tools[2]._run(str(conversation.document_id))
                
                # Parse extraction result
                json_str = extraction_result
                if json_str.startswith("```json"):
                    json_str = json_str[7:]
                if json_str.startswith("```"):
                    json_str = json_str[3:]
                if json_str.endswith("```"):
                    json_str = json_str[:-3]
                
                extraction_data = json.loads(json_str.strip())
                
                # Create context message
                context_message = f"""Análise do documento '{document.title}':

**RESUMO:**
{summary_result}

**INFORMAÇÕES EXTRAÍDAS:**
- Partes: {len(extraction_data.get('parties', []))} identificadas
- Datas importantes: {len(extraction_data.get('dates', []))} encontradas
- Valores: {len(extraction_data.get('values', []))} identificados
- Cláusulas importantes: {len(extraction_data.get('clauses', []))} analisadas

Você pode fazer perguntas sobre qualquer aspecto deste documento."""
                
                # Add context message to conversation
                conv_repo.add_message(new_conv.id, "assistant", context_message)
        except Exception as e:
            logger.warning(f"Failed to add context to conversation: {str(e)}")
    
    return new_conv


@app.get("/conversations", response_model=List[ConversationResponse])
def list_conversations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conv_repo = ConversationRepository(db)
    if current_user.role == UserRole.ADMIN:
        return conv_repo.list_all()
    else:
        # Non-admin users see only their conversations
        return db.query(Conversation).filter(Conversation.user_id == current_user.id).order_by(Conversation.created_at.desc()).all()


@app.post("/conversations/{conversation_id}/messages", response_model=MessageResponse)
def send_message(
    conversation_id: str,
    message: MessageCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conv_repo = ConversationRepository(db)
    
    # Get conversation to retrieve document_id
    conversation = conv_repo.get(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Check access: ADMIN can access all, others only their own
    if current_user.role != UserRole.ADMIN and conversation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Add user message
    conv_repo.add_message(conversation_id, "user", message.content)
    
    # Get chat history
    messages = conv_repo.get_messages(conversation_id)
    chat_history = [{"role": m.role, "content": m.content} for m in messages[:-1]]
    
    # Route via Agent Router
    available_docs = [conversation.document_id] if conversation.document_id else []
    decision = agent_router.route(
        user_input=message.content,
        available_documents=available_docs,
        conversation_context=conversation.document_id,
    )
    
    logger.info("agent_routing_completed", extra={
        "conversation_id": conversation_id,
        "user_id": current_user.id,
        "intent": decision.intent.value,
        "tool": decision.tool,
    })
    
    # Execute the decision
    execution_result = execute_agent_decision(
        db=db,
        user_input=message.content,
        decision=decision,
        user=current_user,
        legal_agent=legal_agent,
        chat_history=chat_history,
        conversation_document_id=conversation.document_id,
    )
    
    # Prepare citations and metadata for storage
    stored_citations = {
        "citations": execution_result.get("citations", []),
        "validation": execution_result.get("validation"),
        "agent": {
            "intent": execution_result["intent"],
            "tool": execution_result["tool"],
            "blocked": execution_result.get("blocked", False),
        },
        "disclaimer": execution_result.get("disclaimer", ""),
    }
    
    if execution_result.get("structured_data"):
        stored_citations["structured_data"] = execution_result["structured_data"]
    
    # Add assistant message
    assistant_message = conv_repo.add_message(
        conversation_id,
        "assistant",
        execution_result["content"],
        stored_citations,
    )
    
    return assistant_message


@app.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
def get_messages(
    conversation_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    conv_repo = ConversationRepository(db)
    conversation = conv_repo.get(conversation_id)
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Check access: ADMIN can access all, others only their own
    if current_user.role != UserRole.ADMIN and conversation.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return conv_repo.get_messages(conversation_id)


@app.post("/analysis/summary", response_model=SummaryResponse)
def generate_summary(
    request: SummaryRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check document access
    doc_repo = DocumentRepository(db)
    document = doc_repo.get(request.document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if current_user.role != UserRole.ADMIN and document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    result = legal_agent.tools[1]._run(str(request.document_id))
    return SummaryResponse(summary=result, key_points=[])


@app.post("/analysis/extract", response_model=ExtractionResponse)
def extract_information(
    request: ExtractionRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    logger.info(f"Extracting information from document: {request.document_id}")
    
    # Check document access
    doc_repo = DocumentRepository(db)
    document = doc_repo.get(request.document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    if current_user.role != UserRole.ADMIN and document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    try:
        result = legal_agent.tools[2]._run(str(request.document_id))
        
        # Parse JSON result (handle markdown code blocks)
        json_str = result
        if json_str.startswith("```json"):
            json_str = json_str[7:]
        if json_str.startswith("```"):
            json_str = json_str[3:]
        if json_str.endswith("```"):
            json_str = json_str[:-3]
        
        data = json.loads(json_str.strip())
        
        # Validate extraction
        validation = ResponseValidator.validate_extraction(data)
        if validation["warnings"]:
            logger.warning(f"Extraction warnings: {validation['warnings']}")
        
        logger.info(f"Extraction completed successfully for document: {request.document_id}")
        
        # Return structured data as-is (already enriched by the LLM)
        return ExtractionResponse(
            parties=data.get("parties", []),
            dates=data.get("dates", []),
            values=data.get("values", []),
            clauses=data.get("clauses", [])
        )
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error during extraction: {str(e)}")
        return ExtractionResponse(parties=[], dates=[], values=[], clauses=[])
    except Exception as e:
        logger.error(f"Error during extraction: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/analysis/compare", response_model=ComparisonResponse)
def compare_documents(
    request: ComparisonRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Check access to both documents
    doc_repo = DocumentRepository(db)
    doc_a = doc_repo.get(request.document_a_id)
    doc_b = doc_repo.get(request.document_b_id)
    
    if not doc_a or not doc_b:
        raise HTTPException(status_code=404, detail="One or both documents not found")
    
    if current_user.role != UserRole.ADMIN:
        if doc_a.user_id != current_user.id or doc_b.user_id != current_user.id:
            raise HTTPException(status_code=403, detail="Access denied")
    
    result = legal_agent.tools[3]._run(
        str(request.document_a_id),
        str(request.document_b_id)
    )
    
    # Parse result
    return ComparisonResponse(
        similarities=[],
        differences=[],
        summary=result
    )


# ============================================================================
# Risk Analysis Endpoints
# ============================================================================

@app.post("/analysis/risks", response_model=RiskAnalysisResponse)
def analyze_risks(
    request: RiskAnalysisRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze contract for potential risks."""
    # Verify document exists and user has access
    document = db.query(Document).filter(Document.id == request.document_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")

    if current_user.role != UserRole.ADMIN and document.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    # Run risk analysis
    analyzer = RiskAnalyzer(db)
    result = analyzer.analyze(request.document_id)

    # Convert to response schema
    risks = [
        RiskItem(
            title=r.title,
            description=r.description,
            severity=r.severity.value,
            category=r.category.value,
            recommendation=r.recommendation,
            citations=[
                CitationSourceSchema(
                    document_id=c.document_id,
                    document_title=c.document_title,
                    chunk_id=c.chunk_id,
                    page_number=c.page_number,
                    excerpt=c.excerpt,
                    similarity_score=c.similarity_score,
                )
                for c in r.citations
            ],
            confidence_score=r.confidence_score,
        )
        for r in result.risks
    ]

    citations = [
        CitationSourceSchema(
            document_id=c.document_id,
            document_title=c.document_title,
            chunk_id=c.chunk_id,
            page_number=c.page_number,
            excerpt=c.excerpt,
            similarity_score=c.similarity_score,
        )
        for c in result.citations
    ]

    return RiskAnalysisResponse(
        overall_risk=result.overall_risk.value,
        confidence_score=result.confidence_score,
        confidence_level=result.confidence_level,
        summary=result.summary,
        risks=risks,
        citations=citations,
        disclaimer=result.disclaimer,
    )


# ============================================================================
# Automation Endpoints
# ============================================================================

@app.get("/automations/runs", response_model=List[AutomationRunResponse])
def list_automation_runs(
    document_id: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List automation runs. Users see only their own; ADMIN sees all."""
    query = db.query(AutomationRun)

    if current_user.role != UserRole.ADMIN:
        query = query.filter(AutomationRun.user_id == current_user.id)

    if document_id:
        query = query.filter(AutomationRun.document_id == document_id)
    if status:
        query = query.filter(AutomationRun.status == status.upper())

    runs = query.order_by(AutomationRun.created_at.desc()).offset(skip).limit(limit).all()
    return runs


@app.get("/automations/runs/{run_id}", response_model=AutomationRunResponse)
def get_automation_run(
    run_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific automation run by ID."""
    run = db.query(AutomationRun).filter(AutomationRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Automation run not found")

    if current_user.role != UserRole.ADMIN and run.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    return run


@app.post("/automations/runs/{run_id}/retry")
def retry_automation_run(
    run_id: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Retry a failed or partial automation run."""
    run = db.query(AutomationRun).filter(AutomationRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Automation run not found")

    if current_user.role != UserRole.ADMIN and run.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Access denied")

    if run.status not in ("FAILED", "PARTIAL_SUCCESS"):
        raise HTTPException(status_code=400, detail="Only FAILED or PARTIAL_SUCCESS runs can be retried")

    # Reset run state
    update_run_status(
        db, run_id,
        status="PENDING",
        current_step="DOCUMENT_PROCESSING",
        progress_percent=0,
        error_message=None,
        webhook_status="pending",
        webhook_error=None,
    )

    background_tasks.add_task(
        run_post_upload_automation,
        run_id=run_id,
        document_id=run.document_id,
        user_id=run.user_id,
    )

    return {"message": "Retry scheduled", "run_id": run_id}


# ============================================================================
# Admin Endpoints
# ============================================================================

@app.get("/admin/system-status")
def get_system_status(
    current_user: User = Depends(require_role(UserRole.ADMIN)),
    db: Session = Depends(get_db)
):
    """Get aggregated system status. ADMIN only."""
    from datetime import datetime, timezone

    # Automation runs by status
    runs = db.query(AutomationRun).all()
    status_counts = {}
    for run in runs:
        status_counts[run.status] = status_counts.get(run.status, 0) + 1

    # Total documents
    total_docs = db.query(Document).count()

    # Total risk analyses (runs with risk_result)
    total_risk = db.query(AutomationRun).filter(AutomationRun.risk_result.isnot(None)).count()

    # Recent failures (last 24h)
    recent_failures = db.query(AutomationRun).filter(
        AutomationRun.status.in_(["FAILED", "PARTIAL_SUCCESS"])
    ).count()

    # Failed webhooks
    failed_webhooks = db.query(AutomationRun).filter(
        AutomationRun.webhook_status == "failed"
    ).count()

    # Average automation duration
    completed = db.query(AutomationRun).filter(
        AutomationRun.completed_at.isnot(None),
        AutomationRun.started_at.isnot(None),
    ).all()
    avg_duration = None
    if completed:
        durations = []
        for r in completed:
            delta = (r.completed_at - r.started_at).total_seconds()
            durations.append(delta)
        avg_duration = sum(durations) / len(durations)

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "automation_runs_by_status": status_counts,
        "total_documents": total_docs,
        "total_risk_analyses": total_risk,
        "recent_failures": recent_failures,
        "avg_automation_duration_seconds": round(avg_duration, 2) if avg_duration else None,
        "failed_webhooks": failed_webhooks,
    }
