from fastapi import FastAPI, UploadFile, File, HTTPException, Depends, Form
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.database import get_db, engine, Base
from app.models import Document, Chunk, DocumentEmbedding, Conversation, Message
from app.repositories import DocumentRepository, ChunkRepository, EmbeddingRepository, ConversationRepository
from app.pdf_extractor import PDFExtractor
from app.chunker import Chunker
from app.embedding_service import EmbeddingService
from app.legal_agent import LegalAgent
from app.schemas import (
    DocumentResponse, MessageCreate, MessageResponse, 
    ConversationCreate, ConversationResponse,
    SummaryRequest, SummaryResponse,
    ExtractionRequest, ExtractionResponse,
    ComparisonRequest, ComparisonResponse
)
from app.logger import logger
from app.validators import ResponseValidator
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
def list_documents(db: Session = Depends(get_db)):
    doc_repo = DocumentRepository(db)
    return doc_repo.list_all()


@app.get("/documents/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str, db: Session = Depends(get_db)):
    doc_repo = DocumentRepository(db)
    document = doc_repo.get(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@app.delete("/documents/{document_id}")
def delete_document(document_id: str, db: Session = Depends(get_db)):
    doc_repo = DocumentRepository(db)
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
def create_conversation(conversation: ConversationCreate, db: Session = Depends(get_db)):
    conv_repo = ConversationRepository(db)
    new_conv = conv_repo.create(
        document_id=conversation.document_id,
        title=conversation.title
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
def list_conversations(db: Session = Depends(get_db)):
    conv_repo = ConversationRepository(db)
    return conv_repo.list_all()


@app.post("/conversations/{conversation_id}/messages", response_model=MessageResponse)
def send_message(
    conversation_id: str,
    message: MessageCreate,
    db: Session = Depends(get_db)
):
    conv_repo = ConversationRepository(db)
    
    # Get conversation to retrieve document_id
    conversation = conv_repo.get(conversation_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
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
    
    # Add assistant message
    assistant_message = conv_repo.add_message(
        conversation_id, 
        "assistant", 
        result["response"],
        result["citations"]
    )
    
    return assistant_message


@app.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse])
def get_messages(conversation_id: str, db: Session = Depends(get_db)):
    conv_repo = ConversationRepository(db)
    return conv_repo.get_messages(conversation_id)


@app.post("/analysis/summary", response_model=SummaryResponse)
def generate_summary(request: SummaryRequest):
    result = legal_agent.tools[1]._run(str(request.document_id))
    return SummaryResponse(summary=result, key_points=[])


@app.post("/analysis/extract", response_model=ExtractionResponse)
def extract_information(request: ExtractionRequest):
    logger.info(f"Extracting information from document: {request.document_id}")
    
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
def compare_documents(request: ComparisonRequest):
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
