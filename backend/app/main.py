from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Form
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
    RiskItem, CitationSourceSchema
)
from app.logger import logger
from app.validators import ResponseValidator
from app.auth import get_current_user, require_role
from app.auth_routes import router as auth_router
from app.ai_validator import AIValidator, CitationSource
from app.agent_router import LegalAgentRouter, AgentIntent
from app.risk_analysis import RiskAnalyzer
from typing import List
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
    
    # Query agent with document context
    try:
        result = legal_agent.query(message.content, chat_history, conversation.document_id)
    except ValueError as e:
        # If agent not initialized, return mock response
        result = {
            "response": f"OPENAI_API_KEY não configurada. Mensagem recebida: {message.content}",
            "citations": []
        }
    
    # Validate response with AI validator
    validator = AIValidator.get_default_validator()
    
    # Retrieve chunks for validation
    retrieved_chunks = []
    if conversation.document_id:
        doc = db.query(Document).filter(Document.id == conversation.document_id).first()
        if doc:
            chunks = db.query(Chunk).filter(Chunk.document_id == conversation.document_id).all()
            for chunk in chunks:
                # Get similarity score if available
                embedding = db.query(DocumentEmbedding).filter(
                    DocumentEmbedding.chunk_id == chunk.id
                ).first()
                
                retrieved_chunks.append({
                    "id": chunk.id,
                    "text": chunk.text,
                    "page_number": chunk.page_number,
                    "similarity_score": embedding.similarity_score if embedding else 0.5,
                    "document_id": doc.id,
                    "document_title": doc.title,
                })
    
    # Process citations from result
    citations_data = []
    if result.get("citations"):
        for citation in result["citations"]:
            if isinstance(citation, dict):
                citations_data.append(citation)
    
    # Validate the response
    validated_response = validator.validate(
        response_content=result["response"],
        retrieved_chunks=retrieved_chunks,
        citations=citations_data,
        document_title=conversation.document_id or "Documento"
    )
    
    # Prepare final response content and metadata
    final_content = validated_response.content if not validated_response.blocked else validated_response.block_reason
    
    # Prepare citations for storage
    final_citations = [c.to_dict() for c in validated_response.validation.citations]
    
    # Add validation metadata to citations
    validation_metadata = {
        "confidence_score": validated_response.validation.confidence_score,
        "confidence_level": validated_response.validation.confidence_level,
        "hallucination_risk": validated_response.validation.hallucination_risk,
        "blocked": validated_response.blocked,
        "disclaimer": validated_response.validation.disclaimer,
    }
    
    # Add assistant message with validation metadata
    assistant_message = conv_repo.add_message(
        conversation_id, 
        "assistant", 
        final_content,
        {
            "citations": final_citations,
            "validation": validation_metadata
        }
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
