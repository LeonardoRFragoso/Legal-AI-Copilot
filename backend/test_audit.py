#!/usr/bin/env python3
"""
Script de auditoria para validar cada funcionalidade do Legal AI Copilot
"""
import sys
import os
sys.path.insert(0, '/home/leonardo/dev/Legal AI Copilot/backend')

from app.pdf_extractor import PDFExtractor
from app.chunker import Chunker
from app.models import Document, Chunk, DocumentEmbedding
from app.database import SessionLocal, engine, Base
from app.repositories import DocumentRepository, ChunkRepository, EmbeddingRepository
import pickle
import numpy as np

# Criar tabelas
Base.metadata.create_all(bind=engine)

print("=" * 80)
print("AUDITORIA - LEGAL AI COPILOT")
print("=" * 80)

# TESTE 1: PDF Extração
print("\n[TESTE 1] Extração de texto do PDF")
try:
    pdf_extractor = PDFExtractor()
    with open("test_contract.pdf", "rb") as f:
        file_bytes = f.read()
    
    text, page_count = pdf_extractor.extract_text(file_bytes)
    
    if text and len(text) > 0 and page_count > 0:
        print(f"✓ PASSOU - Texto extraído: {len(text)} caracteres, {page_count} páginas")
        print(f"  Primeiros 200 chars: {text[:200]}")
    else:
        print(f"✗ FALHOU - Nenhum texto extraído")
except Exception as e:
    print(f"✗ FALHOU - Erro: {str(e)}")

# TESTE 2: Chunking
print("\n[TESTE 2] Chunking de texto")
try:
    chunker = Chunker()
    chunks = chunker.chunk_text(text, page_number=1)
    
    if chunks and len(chunks) > 0:
        print(f"✓ PASSOU - {len(chunks)} chunks criados")
        print(f"  Chunk 1: {chunks[0]['text'][:100]}...")
        print(f"  Chunk 1 metadata: {chunks[0].get('chunk_metadata')}")
    else:
        print(f"✗ FALHOU - Nenhum chunk criado")
except Exception as e:
    print(f"✗ FALHOU - Erro: {str(e)}")

# TESTE 3: Persistência no banco de dados
print("\n[TESTE 3] Persistência de documento e chunks")
try:
    db = SessionLocal()
    doc_repo = DocumentRepository(db)
    
    # Criar documento
    document = doc_repo.create(
        title="Contrato Teste",
        filename="test_contract.pdf",
        file_path="uploads/test_contract.pdf",
        page_count=page_count
    )
    
    doc_id = document.id
    print(f"✓ Documento criado: ID={doc_id}")
    
    # Criar chunks
    chunks_data = []
    for chunk in chunks:
        chunk["document_id"] = doc_id
        chunks_data.append(chunk)
    
    chunk_repo = ChunkRepository(db)
    created_chunks = chunk_repo.create_batch(chunks_data)
    
    if len(created_chunks) == len(chunks_data):
        print(f"✓ PASSOU - {len(created_chunks)} chunks persistidos")
    else:
        print(f"✗ FALHOU - Esperava {len(chunks_data)}, obteve {len(created_chunks)}")
    
    db.close()
    document_id = doc_id  # Guardar ID para testes posteriores
except Exception as e:
    print(f"✗ FALHOU - Erro: {str(e)}")

# TESTE 4: Embeddings simulados (sem OpenAI)
print("\n[TESTE 4] Armazenamento de embeddings (simulado)")
try:
    db = SessionLocal()
    chunk_repo = ChunkRepository(db)
    chunks_from_db = chunk_repo.get_by_document(document_id)
    
    # Criar embeddings simulados (vetores aleatórios de 1536 dimensões)
    embeddings_data = []
    for chunk in chunks_from_db:
        fake_embedding = np.random.randn(1536).tolist()
        embeddings_data.append({
            "chunk_id": chunk.id,
            "document_id": document_id,
            "embedding": fake_embedding
        })
    
    emb_repo = EmbeddingRepository(db)
    created_embeddings = emb_repo.create_batch(embeddings_data)
    
    if len(created_embeddings) == len(embeddings_data):
        print(f"✓ PASSOU - {len(created_embeddings)} embeddings persistidos")
    else:
        print(f"✗ FALHOU - Esperava {len(embeddings_data)}, obteve {len(created_embeddings)}")
    
    db.close()
except Exception as e:
    print(f"✗ FALHOU - Erro: {str(e)}")

# TESTE 5: Busca semântica
print("\n[TESTE 5] Busca semântica")
try:
    db = SessionLocal()
    emb_repo = EmbeddingRepository(db)
    
    # Criar query embedding simulado
    query_embedding = np.random.randn(1536).tolist()
    
    # Buscar
    results = emb_repo.search_similar(query_embedding, document_id=document_id, top_k=3)
    
    if results:
        print(f"✓ PASSOU - {len(results)} resultados encontrados")
        for i, r in enumerate(results, 1):
            print(f"  Resultado {i}: {r['chunk'].text[:100]}... (sim: {r['similarity']:.4f})")
    else:
        print(f"✗ FALHOU - Nenhum resultado encontrado")
    
    db.close()
except Exception as e:
    print(f"✗ FALHOU - Erro: {str(e)}")

# TESTE 6: Verificar arquivo salvo
print("\n[TESTE 6] Arquivo PDF salvo")
try:
    if os.path.exists("uploads/test_contract.pdf"):
        size = os.path.getsize("uploads/test_contract.pdf")
        print(f"✓ PASSOU - Arquivo existe, tamanho: {size} bytes")
    else:
        print(f"✗ FALHOU - Arquivo não encontrado em uploads/")
except Exception as e:
    print(f"✗ FALHOU - Erro: {str(e)}")

# TESTE 7: Verificar imports
print("\n[TESTE 7] Verificar imports")
try:
    from app.pdf_extractor import PDFExtractor
    from app.chunker import Chunker
    from app.embedding_service import EmbeddingService
    from app.legal_agent import LegalAgent
    from app.repositories import DocumentRepository, ChunkRepository, EmbeddingRepository, ConversationRepository
    print(f"✓ PASSOU - Todos os imports funcionam")
except Exception as e:
    print(f"✗ FALHOU - Erro de import: {str(e)}")

# TESTE 8: Verificar TODOs e mocks
print("\n[TESTE 8] Verificar TODOs e mocks em código")
try:
    files_to_check = [
        "app/main.py",
        "app/legal_agent.py",
        "app/repositories.py",
        "app/embedding_service.py"
    ]
    
    todos_found = []
    mocks_found = []
    
    for file in files_to_check:
        with open(file, "r") as f:
            content = f.read()
            lines = content.split("\n")
            for i, line in enumerate(lines, 1):
                if "TODO" in line or "FIXME" in line:
                    todos_found.append(f"{file}:{i} - {line.strip()}")
                if "mock" in line.lower() and "placeholder" not in line.lower():
                    mocks_found.append(f"{file}:{i} - {line.strip()}")
    
    if not todos_found and not mocks_found:
        print(f"✓ PASSOU - Nenhum TODO ou mock encontrado")
    else:
        if todos_found:
            print(f"⚠ PARCIAL - TODOs encontrados:")
            for todo in todos_found:
                print(f"  {todo}")
        if mocks_found:
            print(f"⚠ PARCIAL - Possíveis mocks encontrados:")
            for mock in mocks_found:
                print(f"  {mock}")
except Exception as e:
    print(f"✗ FALHOU - Erro: {str(e)}")

# TESTE 9: Verificar exceções silenciosas
print("\n[TESTE 9] Verificar exceções silenciosas")
try:
    with open("app/main.py", "r") as f:
        content = f.read()
        
    silent_exceptions = []
    lines = content.split("\n")
    for i, line in enumerate(lines, 1):
        if "except:" in line or "except Exception" in line:
            # Verificar se há pass ou return vazio
            if i < len(lines):
                next_line = lines[i].strip()
                if next_line == "pass" or next_line.startswith("return"):
                    silent_exceptions.append(f"main.py:{i} - {line.strip()}")
    
    if not silent_exceptions:
        print(f"✓ PASSOU - Nenhuma exceção silenciosa encontrada")
    else:
        print(f"⚠ PARCIAL - Exceções silenciosas encontradas:")
        for exc in silent_exceptions:
            print(f"  {exc}")
except Exception as e:
    print(f"✗ FALHOU - Erro: {str(e)}")

print("\n" + "=" * 80)
print("FIM DA AUDITORIA")
print("=" * 80)
