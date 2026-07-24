from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey, JSON, LargeBinary, Boolean, Enum
from sqlalchemy.orm import relationship
from app.database import Base
import uuid
from datetime import datetime
import enum


class UserRole(str, enum.Enum):
    ADMIN = "admin"
    LAWYER = "lawyer"
    ASSISTANT = "assistant"
    CLIENT = "client"
    VIEWER = "viewer"


class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(UserRole), default=UserRole.VIEWER, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    
    documents = relationship("Document", back_populates="owner")
    conversations = relationship("Conversation", back_populates="owner")


class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    title = Column(String, nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    status = Column(String, default="processing")
    page_count = Column(Integer)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="documents")
    chunks = relationship("Chunk", back_populates="document", cascade="all, delete-orphan")
    embeddings = relationship("DocumentEmbedding", back_populates="document", cascade="all, delete-orphan")


class Chunk(Base):
    __tablename__ = "chunks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    chunk_index = Column(Integer, nullable=False)
    text = Column(Text, nullable=False)
    page_number = Column(Integer)
    chunk_metadata = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("Document", back_populates="chunks")
    embedding = relationship("DocumentEmbedding", back_populates="chunk", uselist=False)


class DocumentEmbedding(Base):
    __tablename__ = "document_embeddings"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    chunk_id = Column(String, ForeignKey("chunks.id"), nullable=False, unique=True)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    embedding = Column(LargeBinary)  # Store as binary for SQLite
    created_at = Column(DateTime, default=datetime.utcnow)
    
    document = relationship("Document", back_populates="embeddings")
    chunk = relationship("Chunk", back_populates="embedding")


class Conversation(Base):
    __tablename__ = "conversations"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.id"), nullable=True)
    document_id = Column(String, ForeignKey("documents.id"))
    title = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="conversations")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    conversation_id = Column(String, ForeignKey("conversations.id"), nullable=False)
    role = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    citations = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    conversation = relationship("Conversation", back_populates="messages")


class AutomationRun(Base):
    __tablename__ = "automation_runs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    document_id = Column(String, ForeignKey("documents.id"), nullable=False, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False, index=True)
    automation_type = Column(String, default="post_upload", nullable=False)
    status = Column(String, default="PENDING", nullable=False, index=True)
    current_step = Column(String, default="DOCUMENT_PROCESSING", nullable=False)
    progress_percent = Column(Integer, default=0, nullable=False)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)
    summary_result = Column(JSON, nullable=True)
    risk_result = Column(JSON, nullable=True)
    webhook_status = Column(String, default="pending", nullable=False)
    webhook_error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    document = relationship("Document")
    user = relationship("User")
