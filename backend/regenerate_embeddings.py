#!/usr/bin/env python3
"""
Script para regenerar embeddings de um documento
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import SessionLocal
from app.models import Document, Chunk, DocumentEmbedding
from app.repositories import ChunkRepository, EmbeddingRepository, DocumentRepository
from app.embedding_service import EmbeddingService
from app.logger import logger

def regenerate_embeddings(document_id: str):
    """Regenera embeddings para um documento específico"""
    db = SessionLocal()
    try:
        # Verificar se documento existe
        doc_repo = DocumentRepository(db)
        document = doc_repo.get(document_id)
        
        if not document:
            print(f"❌ Documento com ID '{document_id}' não encontrado")
            return False
        
        print(f"📄 Documento encontrado: {document.title}")
        
        # Obter chunks
        chunk_repo = ChunkRepository(db)
        chunks = chunk_repo.get_by_document(document_id)
        
        if not chunks:
            print(f"❌ Nenhum chunk encontrado para o documento")
            return False
        
        print(f"📦 {len(chunks)} chunks encontrados")
        
        # Gerar embeddings
        embedding_service = EmbeddingService()
        
        if not embedding_service.embeddings:
            print("❌ OPENAI_API_KEY não configurada")
            return False
        
        print("🔄 Gerando embeddings...")
        texts = [chunk.text for chunk in chunks]
        embeddings = embedding_service.generate_embeddings_batch(texts)
        
        embeddings_data = []
        for chunk, embedding in zip(chunks, embeddings):
            embeddings_data.append({
                "chunk_id": chunk.id,
                "document_id": document_id,
                "embedding": embedding
            })
        
        # Deletar embeddings antigos
        db.query(DocumentEmbedding).filter(DocumentEmbedding.document_id == document_id).delete()
        db.commit()
        print("🗑️  Embeddings antigos removidos")
        
        # Criar novos embeddings
        emb_repo = EmbeddingRepository(db)
        emb_repo.create_batch(embeddings_data)
        
        print(f"✅ {len(embeddings_data)} embeddings gerados com sucesso!")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao regenerar embeddings: {str(e)}")
        logger.error(f"Error regenerating embeddings: {str(e)}", exc_info=True)
        return False
    finally:
        db.close()

def list_documents():
    """Lista todos os documentos"""
    db = SessionLocal()
    try:
        doc_repo = DocumentRepository(db)
        documents = doc_repo.list_all()
        
        if not documents:
            print("Nenhum documento encontrado")
            return
        
        print("\n📚 Documentos disponíveis:")
        print("-" * 80)
        for doc in documents:
            print(f"ID: {doc.id}")
            print(f"Título: {doc.title}")
            print(f"Status: {doc.status}")
            print("-" * 80)
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python regenerate_embeddings.py <document_id>")
        print("\nOu para listar documentos:")
        print("python regenerate_embeddings.py --list")
        list_documents()
        sys.exit(1)
    
    if sys.argv[1] == "--list":
        list_documents()
    else:
        document_id = sys.argv[1]
        success = regenerate_embeddings(document_id)
        sys.exit(0 if success else 1)
