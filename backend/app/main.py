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
from app.config import get_settings
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
from app.models import AutomationRun, AnalysisRecord, AnalysisReview
from app.analysis_record_service import (
    create_analysis_record,
    get_analysis_record,
    list_analysis_records,
    check_access,
    create_review,
    get_reviews,
    validate_transition,
    can_review,
    DECISION_TO_STATUS,
    ANALYSIS_TYPE_SUMMARY,
    ANALYSIS_TYPE_EXTRACTION,
    ANALYSIS_TYPE_COMPARISON,
    ANALYSIS_TYPE_QUESTION_ANSWERING,
    ANALYSIS_TYPE_RISK_ANALYSIS,
)
from app.schemas import (
    AnalysisRecordResponse,
    AnalysisRecordListResponse,
    AnalysisReviewCreate,
    AnalysisReviewResponse,
    ImpactMetricsResponse,
)
from typing import List, Optional
from datetime import datetime
import os
import uuid
import json
import time as time_module

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
settings = get_settings()


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
    
    # Persist AnalysisRecord for reviewable intents
    reviewable_intents = {
        AgentIntent.SUMMARIZE_DOCUMENT.value,
        AgentIntent.EXTRACT_INFORMATION.value,
        AgentIntent.IDENTIFY_RISKS.value,
        AgentIntent.QUESTION_ANSWERING.value,
    }
    if execution_result["intent"] in reviewable_intents and not execution_result.get("error"):
        intent = execution_result["intent"]
        type_map = {
            AgentIntent.SUMMARIZE_DOCUMENT.value: ANALYSIS_TYPE_SUMMARY,
            AgentIntent.EXTRACT_INFORMATION.value: ANALYSIS_TYPE_EXTRACTION,
            AgentIntent.IDENTIFY_RISKS.value: ANALYSIS_TYPE_RISK_ANALYSIS,
            AgentIntent.QUESTION_ANSWERING.value: ANALYSIS_TYPE_QUESTION_ANSWERING,
        }
        analysis_type = type_map.get(intent, "QUESTION_ANSWERING")
        validation = execution_result.get("validation")
        structured = execution_result.get("structured_data")
        
        create_analysis_record(
            db=db,
            document_id=conversation.document_id or "",
            user_id=current_user.id,
            analysis_type=analysis_type,
            content_summary=execution_result["content"][:500],
            structured_result=structured,
            confidence_score=validation.get("confidence_score") if validation else None,
            confidence_level=validation.get("confidence_level") if validation else None,
            overall_risk=structured.get("overall_risk") if structured else None,
            citations=execution_result.get("citations", []),
            disclaimer=execution_result.get("disclaimer", ""),
            model_name="gpt-4" if settings.openai_api_key else "heuristic",
            blocked=execution_result.get("blocked", False),
            conversation_id=conversation_id,
            message_id=assistant_message.id,
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
    
    create_analysis_record(
        db=db,
        document_id=request.document_id,
        user_id=current_user.id,
        analysis_type=ANALYSIS_TYPE_SUMMARY,
        content_summary=result[:500],
        model_name="gpt-4" if settings.openai_api_key else "heuristic",
    )
    
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
        
        create_analysis_record(
            db=db,
            document_id=request.document_id,
            user_id=current_user.id,
            analysis_type=ANALYSIS_TYPE_EXTRACTION,
            content_summary=f"Parties: {len(data.get('parties', []))}, Clauses: {len(data.get('clauses', []))}",
            structured_result=data,
            model_name="gpt-4" if settings.openai_api_key else "heuristic",
        )
        
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
    
    create_analysis_record(
        db=db,
        document_id=request.document_a_id,
        user_id=current_user.id,
        analysis_type=ANALYSIS_TYPE_COMPARISON,
        content_summary=result[:500],
        model_name="gpt-4" if settings.openai_api_key else "heuristic",
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

    # Persist AnalysisRecord
    create_analysis_record(
        db=db,
        document_id=request.document_id,
        user_id=current_user.id,
        analysis_type=ANALYSIS_TYPE_RISK_ANALYSIS,
        content_summary=result.summary[:500],
        structured_result=result.to_dict(),
        confidence_score=result.confidence_score,
        confidence_level=result.confidence_level,
        overall_risk=result.overall_risk.value,
        citations=[c.to_dict() for c in result.citations],
        disclaimer=result.disclaimer,
        model_name="heuristic",
    )

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
# Analysis Records & Review Endpoints
# ============================================================================

@app.get("/analyses", response_model=List[AnalysisRecordListResponse])
def list_analyses(
    document_id: Optional[str] = Query(None),
    analysis_type: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    confidence_level: Optional[str] = Query(None),
    overall_risk: Optional[str] = Query(None),
    created_from: Optional[datetime] = Query(None),
    created_to: Optional[datetime] = Query(None),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """List analysis records with filters. Users see only their own; ADMIN sees all."""
    return list_analysis_records(
        db=db,
        user=current_user,
        document_id=document_id,
        analysis_type=analysis_type,
        status=status,
        confidence_level=confidence_level,
        overall_risk=overall_risk,
        created_from=created_from,
        created_to=created_to,
        skip=skip,
        limit=limit,
    )


@app.get("/analyses/{analysis_id}", response_model=AnalysisRecordResponse)
def get_analysis(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get a specific analysis record with review history."""
    record = get_analysis_record(db, analysis_id)
    if not record:
        raise HTTPException(status_code=404, detail="Analysis record not found")
    if not check_access(db, record, current_user):
        raise HTTPException(status_code=403, detail="Access denied")
    return record


@app.post("/analyses/{analysis_id}/reviews", response_model=AnalysisReviewResponse, status_code=201)
def create_analysis_review(
    analysis_id: str,
    review: AnalysisReviewCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Create a review (approve/reject/request_changes) for an analysis record."""
    record = get_analysis_record(db, analysis_id)
    if not record:
        raise HTTPException(status_code=404, detail="Analysis record not found")
    if not check_access(db, record, current_user):
        raise HTTPException(status_code=403, detail="Access denied")

    if not can_review(current_user, record):
        raise HTTPException(status_code=403, detail="Your role cannot review analyses")

    try:
        review_entry = create_review(
            db=db,
            record=record,
            reviewer=current_user,
            decision=review.decision,
            comment=review.comment,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Build response with reviewer name
    resp = AnalysisReviewResponse(
        id=review_entry.id,
        analysis_record_id=review_entry.analysis_record_id,
        reviewer_user_id=review_entry.reviewer_user_id,
        reviewer_name=current_user.name,
        previous_status=review_entry.previous_status,
        new_status=review_entry.new_status,
        decision=review_entry.decision,
        comment=review_entry.comment,
        created_at=review_entry.created_at,
    )
    return resp


@app.get("/analyses/{analysis_id}/reviews", response_model=List[AnalysisReviewResponse])
def list_analysis_reviews(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get review history for an analysis record (chronological order)."""
    record = get_analysis_record(db, analysis_id)
    if not record:
        raise HTTPException(status_code=404, detail="Analysis record not found")
    if not check_access(db, record, current_user):
        raise HTTPException(status_code=403, detail="Access denied")

    reviews = get_reviews(db, analysis_id)
    result = []
    for r in reviews:
        reviewer = db.query(User).filter(User.id == r.reviewer_user_id).first()
        result.append(AnalysisReviewResponse(
            id=r.id,
            analysis_record_id=r.analysis_record_id,
            reviewer_user_id=r.reviewer_user_id,
            reviewer_name=reviewer.name if reviewer else "",
            previous_status=r.previous_status,
            new_status=r.new_status,
            decision=r.decision,
            comment=r.comment,
            created_at=r.created_at,
        ))
    return result


# ============================================================================
# Metrics Endpoint
# ============================================================================

@app.get("/metrics/impact", response_model=ImpactMetricsResponse)
def get_impact_metrics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Get aggregated impact metrics. ADMIN sees global; others see own data."""
    query = db.query(AnalysisRecord)
    if current_user.role != UserRole.ADMIN:
        query = query.filter(AnalysisRecord.user_id == current_user.id)

    records = query.all()

    analyses_by_type = {}
    reviews_by_status = {}
    risks_by_severity = {}
    total_confidence = 0
    total_processing_ms = 0
    total_manual_min = 0
    total_saved_min = 0
    approved = 0
    rejected = 0
    pending = 0

    for r in records:
        analyses_by_type[r.analysis_type] = analyses_by_type.get(r.analysis_type, 0) + 1
        reviews_by_status[r.status] = reviews_by_status.get(r.status, 0) + 1

        if r.status == "APPROVED":
            approved += 1
        elif r.status == "REJECTED":
            rejected += 1
        elif r.status in ("GENERATED", "PENDING_REVIEW", "NEEDS_CHANGES"):
            pending += 1

        if r.confidence_score:
            total_confidence += r.confidence_score
        if r.processing_duration_ms:
            total_processing_ms += r.processing_duration_ms
        if r.estimated_manual_minutes:
            total_manual_min += r.estimated_manual_minutes
        if r.estimated_time_saved_minutes:
            total_saved_min += r.estimated_time_saved_minutes

        if r.structured_result and isinstance(r.structured_result, dict):
            risks = r.structured_result.get("risks", [])
            if isinstance(risks, list):
                for risk in risks:
                    if isinstance(risk, dict):
                        sev = risk.get("severity", "unknown")
                        risks_by_severity[sev] = risks_by_severity.get(sev, 0) + 1

    total = len(records)
    approval_rate = (approved / total * 100) if total > 0 else 0.0
    avg_confidence = (total_confidence / total) if total > 0 else 0.0
    avg_processing = (total_processing_ms / total) if total > 0 else 0.0

    # Automation stats
    auto_query = db.query(AutomationRun)
    if current_user.role != UserRole.ADMIN:
        auto_query = auto_query.filter(AutomationRun.user_id == current_user.id)
    auto_runs = auto_query.all()
    automations_by_status = {}
    failed_webhooks = 0
    for run in auto_runs:
        automations_by_status[run.status] = automations_by_status.get(run.status, 0) + 1
        if run.webhook_status == "failed":
            failed_webhooks += 1

    total_docs = db.query(Document).count()
    if current_user.role != UserRole.ADMIN:
        total_docs = db.query(Document).filter(Document.user_id == current_user.id).count()

    return ImpactMetricsResponse(
        documents_total=total_docs,
        analyses_total=total,
        analyses_by_type=analyses_by_type,
        reviews_by_status=reviews_by_status,
        approval_rate=round(approval_rate, 1),
        average_confidence_score=round(avg_confidence, 1),
        risks_by_severity=risks_by_severity,
        automations_by_status=automations_by_status,
        failed_webhooks=failed_webhooks,
        average_processing_duration_ms=round(avg_processing, 1),
        estimated_manual_minutes=total_manual_min,
        estimated_time_saved_minutes=total_saved_min,
        estimated_time_saved_hours=round(total_saved_min / 60.0, 1),
        estimation_notice="As métricas de produtividade são estimativas do MVP baseadas em tempos manuais configuráveis.",
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

    # Analysis records — blocked and pending review
    blocked_analyses = db.query(AnalysisRecord).filter(
        AnalysisRecord.blocked == True
    ).count()
    pending_review = db.query(AnalysisRecord).filter(
        AnalysisRecord.status.in_(["GENERATED", "PENDING_REVIEW", "NEEDS_CHANGES"])
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
        "health": "healthy",
        "automation_runs_by_status": status_counts,
        "total_documents": total_docs,
        "total_risk_analyses": total_risk,
        "recent_failures": recent_failures,
        "avg_automation_duration_seconds": round(avg_duration, 2) if avg_duration else None,
        "failed_webhooks": failed_webhooks,
        "blocked_analyses": blocked_analyses,
        "pending_review": pending_review,
    }
