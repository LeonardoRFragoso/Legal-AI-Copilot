#!/usr/bin/env python3
"""
Teste final com API key configurada
"""
import requests
import time

BASE_URL = "http://localhost:8000"

print("=" * 100)
print("TESTE FINAL - COM OPENAI_API_KEY CONFIGURADA")
print("=" * 100)

results = []

# 1. Backend
print("\n[1] Backend inicia")
try:
    resp = requests.get(f"{BASE_URL}/health", timeout=5)
    if resp.status_code == 200:
        print("✓ PASSOU")
        results.append(("Backend inicia", "PASSOU"))
    else:
        print(f"✗ FALHOU - {resp.status_code}")
        results.append(("Backend inicia", "FALHOU"))
except Exception as e:
    print(f"✗ FALHOU - {str(e)}")
    results.append(("Backend inicia", "FALHOU"))

# 2. Upload PDF
print("\n[2] Upload de PDF")
doc_id = None
try:
    with open("test_contract.pdf", "rb") as f:
        files = {"file": f}
        data = {"title": "Contrato Teste"}
        resp = requests.post(f"{BASE_URL}/documents/upload", files=files, data=data)
    
    if resp.status_code == 200:
        doc = resp.json()
        doc_id = doc["id"]
        print(f"✓ PASSOU - ID: {doc_id}")
        results.append(("Upload PDF", "PASSOU"))
    else:
        print(f"✗ FALHOU - {resp.status_code}")
        results.append(("Upload PDF", "FALHOU"))
except Exception as e:
    print(f"✗ FALHOU - {str(e)}")
    results.append(("Upload PDF", "FALHOU"))

# 3. Verificar documento
print("\n[3] Documento persistido")
if doc_id:
    try:
        resp = requests.get(f"{BASE_URL}/documents/{doc_id}")
        if resp.status_code == 200:
            print(f"✓ PASSOU")
            results.append(("Documento persistido", "PASSOU"))
        else:
            print(f"✗ FALHOU - {resp.status_code}")
            results.append(("Documento persistido", "FALHOU"))
    except Exception as e:
        print(f"✗ FALHOU - {str(e)}")
        results.append(("Documento persistido", "FALHOU"))
else:
    print("⚠ PARCIAL - Sem documento")
    results.append(("Documento persistido", "PARCIAL"))

# 4. Criar conversa
print("\n[4] Criar conversa")
conv_id = None
if doc_id:
    try:
        conv_data = {"document_id": doc_id, "title": "Teste"}
        resp = requests.post(f"{BASE_URL}/conversations", json=conv_data)
        
        if resp.status_code == 200:
            conv = resp.json()
            conv_id = conv["id"]
            print(f"✓ PASSOU - ID: {conv_id}")
            results.append(("Criar conversa", "PASSOU"))
        else:
            print(f"✗ FALHOU - {resp.status_code}")
            results.append(("Criar conversa", "FALHOU"))
    except Exception as e:
        print(f"✗ FALHOU - {str(e)}")
        results.append(("Criar conversa", "FALHOU"))
else:
    print("⚠ PARCIAL - Sem documento")
    results.append(("Criar conversa", "PARCIAL"))

# 5. Chat com RAG
print("\n[5] Chat com RAG")
if conv_id:
    try:
        msg_data = {"content": "Qual é o valor do contrato?"}
        resp = requests.post(f"{BASE_URL}/conversations/{conv_id}/messages", json=msg_data)
        
        if resp.status_code == 200:
            msg = resp.json()
            print(f"✓ PASSOU - Resposta: {msg['content'][:100]}...")
            results.append(("Chat com RAG", "PASSOU"))
        else:
            print(f"✗ FALHOU - {resp.status_code}")
            results.append(("Chat com RAG", "FALHOU"))
    except Exception as e:
        print(f"✗ FALHOU - {str(e)}")
        results.append(("Chat com RAG", "FALHOU"))
else:
    print("⚠ PARCIAL - Sem conversa")
    results.append(("Chat com RAG", "PARCIAL"))

# 6. Resumo
print("\n[6] Resumo do contrato")
if doc_id:
    try:
        summary_data = {"document_id": doc_id}
        resp = requests.post(f"{BASE_URL}/analysis/summary", json=summary_data)
        
        if resp.status_code == 200:
            result = resp.json()
            print(f"✓ PASSOU - Resumo gerado")
            results.append(("Resumo", "PASSOU"))
        else:
            print(f"✗ FALHOU - {resp.status_code}")
            results.append(("Resumo", "FALHOU"))
    except Exception as e:
        print(f"✗ FALHOU - {str(e)}")
        results.append(("Resumo", "FALHOU"))
else:
    print("⚠ PARCIAL - Sem documento")
    results.append(("Resumo", "PARCIAL"))

# 7. Extração
print("\n[7] Extração de entidades")
if doc_id:
    try:
        extract_data = {"document_id": doc_id}
        resp = requests.post(f"{BASE_URL}/analysis/extract", json=extract_data)
        
        if resp.status_code == 200:
            result = resp.json()
            print(f"✓ PASSOU - Entidades extraídas")
            results.append(("Extração", "PASSOU"))
        else:
            print(f"✗ FALHOU - {resp.status_code}")
            results.append(("Extração", "FALHOU"))
    except Exception as e:
        print(f"✗ FALHOU - {str(e)}")
        results.append(("Extração", "FALHOU"))
else:
    print("⚠ PARCIAL - Sem documento")
    results.append(("Extração", "PARCIAL"))

# 8. Comparação
print("\n[8] Comparação de contratos")
if doc_id:
    try:
        # Upload segundo documento
        with open("test_contract.pdf", "rb") as f:
            files = {"file": f}
            data = {"title": "Contrato 2"}
            resp = requests.post(f"{BASE_URL}/documents/upload", files=files, data=data)
        
        if resp.status_code == 200:
            doc2 = resp.json()
            doc2_id = doc2["id"]
            
            compare_data = {"document_a_id": doc_id, "document_b_id": doc2_id}
            resp = requests.post(f"{BASE_URL}/analysis/compare", json=compare_data)
            
            if resp.status_code == 200:
                print(f"✓ PASSOU - Comparação realizada")
                results.append(("Comparação", "PASSOU"))
            else:
                print(f"✗ FALHOU - {resp.status_code}")
                results.append(("Comparação", "FALHOU"))
        else:
            print(f"✗ FALHOU - Upload segundo doc falhou")
            results.append(("Comparação", "FALHOU"))
    except Exception as e:
        print(f"✗ FALHOU - {str(e)}")
        results.append(("Comparação", "FALHOU"))
else:
    print("⚠ PARCIAL - Sem documento")
    results.append(("Comparação", "PARCIAL"))

# Resumo
print("\n" + "=" * 100)
print("RESUMO DOS TESTES")
print("=" * 100)

passed = sum(1 for _, status in results if status == "PASSOU")
failed = sum(1 for _, status in results if status == "FALHOU")
partial = sum(1 for _, status in results if status == "PARCIAL")

for func, status in results:
    symbol = "✓" if status == "PASSOU" else "✗" if status == "FALHOU" else "⚠"
    print(f"{symbol} {func:<30} {status}")

print("-" * 100)
print(f"TOTAL: {passed} PASSOU | {partial} PARCIAL | {failed} FALHOU")

if failed == 0:
    print("\n✓ TODOS OS TESTES PASSARAM!")
else:
    print(f"\n✗ {failed} TESTE(S) FALHARAM")
