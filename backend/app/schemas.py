from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


class DocumentCreate(BaseModel):
    title: str
    filename: str


class DocumentResponse(BaseModel):
    id: str
    title: str
    filename: str
    status: str
    page_count: Optional[int]
    created_at: datetime
    
    class Config:
        from_attributes = True


class MessageCreate(BaseModel):
    content: str


class MessageResponse(BaseModel):
    id: str
    role: str
    content: str
    citations: Optional[List[Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ConversationCreate(BaseModel):
    document_id: Optional[str] = None
    title: Optional[str] = None


class ConversationResponse(BaseModel):
    id: str
    document_id: Optional[str]
    title: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class SummaryRequest(BaseModel):
    document_id: str


class SummaryResponse(BaseModel):
    summary: str
    key_points: List[str]


class ExtractionRequest(BaseModel):
    document_id: str


class PartyInfo(BaseModel):
    name: str
    role: str
    description: Optional[str] = None


class DateInfo(BaseModel):
    date: str
    type: str
    description: str


class ValueInfo(BaseModel):
    amount: str
    type: str
    description: str


class ClauseInfo(BaseModel):
    clause: str
    type: str
    description: str
    risk: str


class ExtractionResponse(BaseModel):
    parties: List[Any]
    dates: List[Any]
    values: List[Any]
    clauses: List[Any]


class ComparisonRequest(BaseModel):
    document_a_id: str
    document_b_id: str


class ComparisonResponse(BaseModel):
    similarities: List[str]
    differences: List[str]
    summary: str
