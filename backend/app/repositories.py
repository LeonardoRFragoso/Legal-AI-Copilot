from sqlalchemy.orm import Session
from app.models import Document, Chunk, DocumentEmbedding, Conversation, Message
from typing import List, Optional
import pickle
import numpy as np


class DocumentRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, title: str, filename: str, file_path: str, page_count: int) -> Document:
        document = Document(
            title=title,
            filename=filename,
            file_path=file_path,
            page_count=page_count,
            status="processing"
        )
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        return document
    
    def get(self, document_id: str) -> Optional[Document]:
        return self.db.query(Document).filter(Document.id == document_id).first()
    
    def list_all(self) -> List[Document]:
        return self.db.query(Document).order_by(Document.created_at.desc()).all()
    
    def update_status(self, document_id: str, status: str) -> Optional[Document]:
        document = self.get(document_id)
        if document:
            document.status = status
            self.db.commit()
            self.db.refresh(document)
        return document
    
    def delete(self, document_id: str) -> bool:
        document = self.get(document_id)
        if document:
            self.db.delete(document)
            self.db.commit()
            return True
        return False


class ChunkRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_batch(self, chunks_data: List[dict]) -> List[Chunk]:
        chunks = []
        for chunk_data in chunks_data:
            chunk = Chunk(**chunk_data)
            self.db.add(chunk)
            chunks.append(chunk)
        self.db.commit()
        for chunk in chunks:
            self.db.refresh(chunk)
        return chunks
    
    def get_by_document(self, document_id: str) -> List[Chunk]:
        return self.db.query(Chunk).filter(Chunk.document_id == document_id).all()


class EmbeddingRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create_batch(self, embeddings_data: List[dict]) -> List[DocumentEmbedding]:
        embeddings = []
        for emb_data in embeddings_data:
            # Convert list to binary for SQLite
            if isinstance(emb_data["embedding"], list):
                emb_data["embedding"] = pickle.dumps(emb_data["embedding"])
            embedding = DocumentEmbedding(**emb_data)
            self.db.add(embedding)
            embeddings.append(embedding)
        self.db.commit()
        for emb in embeddings:
            self.db.refresh(emb)
        return embeddings
    
    def search_similar(self, query_embedding: list, document_id: str = None, top_k: int = 5) -> List[dict]:
        query = self.db.query(DocumentEmbedding).options(
            DocumentEmbedding.chunk
        )
        
        if document_id:
            query = query.filter(DocumentEmbedding.document_id == document_id)
        
        embeddings = query.all()
        
        results = []
        for emb in embeddings:
            if emb.embedding:
                # Deserialize binary to list
                stored_embedding = pickle.loads(emb.embedding)
                similarity = self._cosine_similarity(query_embedding, stored_embedding)
                if similarity > 0.7:
                    results.append({
                        "chunk": emb.chunk,
                        "similarity": similarity
                    })
        
        results.sort(key=lambda x: x["similarity"], reverse=True)
        return results[:top_k]
    
    def _cosine_similarity(self, a: list, b: list) -> float:
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class ConversationRepository:
    def __init__(self, db: Session):
        self.db = db
    
    def create(self, document_id: str = None, title: str = None) -> Conversation:
        conversation = Conversation(document_id=document_id, title=title)
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation
    
    def get(self, conversation_id: str) -> Optional[Conversation]:
        return self.db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    def list_all(self) -> List[Conversation]:
        return self.db.query(Conversation).order_by(Conversation.created_at.desc()).all()
    
    def add_message(self, conversation_id: str, role: str, content: str, citations: list = None) -> Message:
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            citations=citations
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message
    
    def get_messages(self, conversation_id: str) -> List[Message]:
        return self.db.query(Message).filter(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).all()
