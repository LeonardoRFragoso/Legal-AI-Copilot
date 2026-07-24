# Legal AI Copilot - MVP

Sistema de IA para análise de contratos jurídicos utilizando RAG.

## Stack

- **Backend**: FastAPI, Python 3.12, LangChain, OpenAI GPT-4o
- **Frontend**: React, TypeScript, Vite, TailwindCSS
- **Banco**: SQLite (para MVP sem Docker)
- **IA**: OpenAI GPT-4o, text-embedding-3-small
- **Framework**: LangChain

## Funcionalidades

- ✅ Upload de contratos PDF
- ✅ Extração de texto e chunking
- ✅ Geração de embeddings (OpenAI)
- ✅ Chat com RAG e citações
- ✅ Resumo de contratos
- ✅ Extração de informações estruturadas (partes, datas, valores, cláusulas)
- ✅ Comparação entre contratos
- ✅ Legal Agent com Tools integradas

## Setup Rápido

### Pré-requisitos

- Python 3.12+
- Node.js 18+
- OpenAI API Key

### 1. Configurar Backend

```bash
cd backend

# Criar virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

# Instalar dependências
pip install -r requirements.txt

# Configurar API Key
cp .env.example .env
# Editar .env e adicionar: OPENAI_API_KEY=sk-sua-chave-aqui

# Iniciar servidor
uvicorn app.main:app --reload
```

Backend estará rodando em: http://localhost:8000
API Docs: http://localhost:8000/docs

### 2. Configurar Frontend

```bash
cd frontend

# Instalar dependências
npm install

# Configurar API URL
cp .env.example .env
# Editar .env se necessário (padrão: http://localhost:8000)

# Iniciar servidor
npm run dev
```

Frontend estará rodando em: http://localhost:3000 (ou porta disponível)

## Estrutura do Projeto

```
.
├── backend/
│   ├── app/
│   │   ├── main.py              # Entry point FastAPI
│   │   ├── config.py            # Configurações
│   │   ├── database.py          # SQLite connection
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── repositories.py      # Repository pattern
│   │   ├── pdf_extractor.py     # Extração de texto PDF
│   │   ├── chunker.py           # Chunking strategy
│   │   ├── embedding_service.py # OpenAI embeddings
│   │   └── legal_agent.py       # LangChain Agent + Tools
│   ├── requirements.txt
│   └── SETUP.md
├── frontend/
│   ├── src/
│   │   ├── pages/               # Dashboard, Upload, Chat, Analysis, Comparison
│   │   ├── components/          # UI components
│   │   ├── services/            # API clients
│   │   ├── store/               # Zustand state
│   │   └── types/               # TypeScript types
│   └── package.json
└── README.md
```

## APIs Disponíveis

### Documentos
- `POST /documents/upload` - Upload de PDF
- `GET /documents` - Listar documentos
- `GET /documents/{id}` - Detalhes do documento
- `DELETE /documents/{id}` - Remover documento

### Chat
- `POST /conversations` - Criar conversa
- `GET /conversations` - Listar conversas
- `POST /conversations/{id}/messages` - Enviar mensagem
- `GET /conversations/{id}/messages` - Histórico

### Análise
- `POST /analysis/summary` - Gerar resumo
- `POST /analysis/extract` - Extrair informações
- `POST /analysis/compare` - Comparar documentos

## Notas Importantes

1. **OPENAI_API_KEY**: Obrigatória para funcionalidades de IA. Sem ela, o backend inicia mas as funções de IA não funcionam.

2. **SQLite**: O MVP usa SQLite para simplicidade. O banco é criado automaticamente como `legal_ai.db`.

3. **Arquivos PDF**: São salvos localmente em `backend/uploads/`.

4. **Embeddings**: Armazenados como binário no SQLite usando pickle.

## Demonstração

Para demonstrar o projeto:

1. Acesse http://localhost:3000
2. Faça upload de um contrato PDF
3. Aguarde processamento (extração + embeddings)
4. Use o Chat para fazer perguntas sobre o contrato
5. Use Análise para ver resumo e informações extraídas
6. Use Comparação para comparar dois contratos

## Licença

MIT
# Legal-AI-Copilot
# Legal-AI-Copilot
