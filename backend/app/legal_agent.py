from langchain.agents import AgentExecutor, create_openai_tools_agent
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.tools import BaseTool, StructuredTool
from pydantic import BaseModel, Field
from typing import Type, Optional, List
from app.config import get_settings
from app.database import SessionLocal
from app.models import Document, Chunk, DocumentEmbedding
from sqlalchemy.orm import joinedload
import numpy as np
import os
import re
import pickle

settings = get_settings()


class SearchInput(BaseModel):
    query: str = Field(description="Query to search for in the documents")
    document_id: Optional[str] = Field(default=None, description="Specific document ID to search in")


class SearchTool(BaseTool):
    name = "semantic_search"
    description = "Search for relevant chunks in the document database using semantic search"
    args_schema: Type[BaseModel] = SearchInput
    
    def _run(self, query: str, document_id: Optional[str] = None) -> str:
        db = SessionLocal()
        try:
            from app.embedding_service import EmbeddingService
            embedding_service = EmbeddingService()
            
            # Extract document_id from query if it's in the format [Document ID: xxx]
            actual_document_id = document_id
            if query.startswith("[Document ID:"):
                match = re.search(r'\[Document ID: ([^\]]+)\]', query)
                if match:
                    actual_document_id = match.group(1).strip()
                    query = query[match.end():].strip()
            
            query_embedding = embedding_service.generate_embedding(query)
            
            # Simple cosine similarity search
            embeddings = db.query(DocumentEmbedding)
            
            if actual_document_id:
                embeddings = embeddings.filter(DocumentEmbedding.document_id == actual_document_id)
            
            embeddings = embeddings.all()
            
            results = []
            for emb in embeddings:
                if emb.embedding:
                    # Deserialize embedding from binary
                    try:
                        stored_embedding = pickle.loads(emb.embedding)
                    except:
                        # If deserialization fails, skip this embedding
                        continue
                    
                    similarity = self._cosine_similarity(query_embedding, stored_embedding)
                    results.append({
                        "text": emb.chunk.text,
                        "document": emb.chunk.document.title,
                        "page": emb.chunk.page_number,
                        "similarity": similarity
                    })
            
            results.sort(key=lambda x: x["similarity"], reverse=True)
            top_results = results[:5]
            
            if not top_results:
                return "Nenhuma informação relevante encontrada nos documentos. Por favor, tente reformular sua pergunta."
            
            output = "Relevant chunks found:\n\n"
            for i, r in enumerate(top_results, 1):
                output += f"{i}. Document: {r['document']}, Page: {r['page']}\n"
                output += f"   {r['text'][:500]}...\n\n"
            
            return output
        finally:
            db.close()
    
    def _cosine_similarity(self, a: list, b: list) -> float:
        a = np.array(a)
        b = np.array(b)
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


class SummaryInput(BaseModel):
    document_id: str = Field(description="Document ID to summarize")


class SummaryTool(BaseTool):
    name = "summarize_document"
    description = "Generate a summary of a document"
    args_schema: Type[BaseModel] = SummaryInput
    
    def _run(self, document_id: str) -> str:
        db = SessionLocal()
        try:
            document = db.query(Document).filter(Document.id == document_id).first()
            if not document:
                return "Document not found."
            
            chunks = db.query(Chunk).filter(Chunk.document_id == document_id).all()
            text = "\n\n".join([c.text for c in chunks])
            
            # Use LLM to summarize
            api_key = settings.openai_api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                return "OPENAI_API_KEY not configured for summarization."
            
            llm = ChatOpenAI(
                model="gpt-4o",
                temperature=0.3,
                openai_api_key=api_key
            )
            
            summary = llm.invoke(f"Faça um resumo detalhado do seguinte documento legal em português (pt-BR):\n\n{text}")
            return summary.content
        finally:
            db.close()


class ExtractInput(BaseModel):
    document_id: str = Field(description="Document ID to extract information from")


class ExtractTool(BaseTool):
    name = "extract_information"
    description = "Extract structured information from a document (parties, dates, values, clauses)"
    args_schema: Type[BaseModel] = ExtractInput
    
    def _run(self, document_id: str) -> str:
        db = SessionLocal()
        try:
            chunks = db.query(Chunk).filter(Chunk.document_id == document_id).all()
            text = "\n\n".join([c.text for c in chunks])
            
            api_key = settings.openai_api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                return "OPENAI_API_KEY not configured for extraction."
            
            llm = ChatOpenAI(
                model="gpt-4o",
                temperature=0.3,
                openai_api_key=api_key
            )
            
            prompt = f"""Extract the following information from this legal document and return ONLY a valid JSON object with no additional text:

{{
  "parties": [
    {{"name": "party name", "role": "contratante/contratada/ambos", "description": "brief description"}}
  ],
  "dates": [
    {{"date": "DD/MM/YYYY or description", "type": "inicio/termino/renovacao/prazo", "description": "what this date means"}}
  ],
  "values": [
    {{"amount": "value with currency", "type": "salario_mensal/salario_total/multa/taxa/outro", "description": "detailed explanation of what this value is for"}}
  ],
  "clauses": [
    {{"clause": "clause name", "type": "confidencialidade/multa/rescisao/pagamento/lgpd/outro", "description": "detailed explanation", "risk": "baixo/medio/alto"}}
  ]
}}

IMPORTANT RULES:
1. For parties: Identify WHO is contracting WHO. Be specific about roles.
2. For dates: Explain WHAT each date means (e.g., "Contract starts on 01/08/2026" not just "01/08/2026")
3. For values: Distinguish between:
   - salario_mensal: Monthly payment amount
   - salario_total: Total contract value
   - multa: Penalty amounts
   - taxa: Percentages or rates
4. For clauses: Provide DETAILED explanations of what each clause means and its implications.
5. All descriptions must be in Portuguese (pt-BR).

Document:
{text}

Return ONLY the JSON object, no other text."""
            
            result = llm.invoke(prompt)
            return result.content
        finally:
            db.close()


class CompareInput(BaseModel):
    document_a_id: str = Field(description="First document ID")
    document_b_id: str = Field(description="Second document ID")


class CompareTool(BaseTool):
    name = "compare_documents"
    description = "Compare two documents and highlight similarities and differences"
    args_schema: Type[BaseModel] = CompareInput
    
    def _run(self, document_a_id: str, document_b_id: str) -> str:
        db = SessionLocal()
        try:
            chunks_a = db.query(Chunk).filter(Chunk.document_id == document_a_id).all()
            chunks_b = db.query(Chunk).filter(Chunk.document_id == document_b_id).all()
            
            text_a = "\n\n".join([c.text for c in chunks_a])
            text_b = "\n\n".join([c.text for c in chunks_b])
            
            api_key = settings.openai_api_key or os.getenv("OPENAI_API_KEY")
            if not api_key:
                return "OPENAI_API_KEY not configured for comparison."
            
            llm = ChatOpenAI(
                model="gpt-4o",
                temperature=0.3,
                openai_api_key=api_key
            )
            
            prompt = f"""Compare estes dois documentos legais e forneça em português (pt-BR):
            1. Similaridades entre eles
            2. Diferenças entre eles
            3. Um resumo da comparação
            
            Documento A:
            {text_a[:3000]}
            
            Documento B:
            {text_b[:3000]}
            """
            
            result = llm.invoke(prompt)
            return result.content
        finally:
            db.close()


class LegalAgent:
    def __init__(self):
        api_key = settings.openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("WARNING: OPENAI_API_KEY not set. Legal Agent will not work.")
            self.llm = None
            self.agent_executor = None
        else:
            self.llm = ChatOpenAI(
                model="gpt-4o",
                temperature=0.3,
                openai_api_key=api_key
            )
            
            self.tools = [
                SearchTool(),
                SummaryTool(),
                ExtractTool(),
                CompareTool()
            ]
            
            self.prompt = ChatPromptTemplate.from_messages([
                ("system", """Você é um assistente de Legal AI Copilot especializado em análise de contratos. 
                Seu papel é ajudar os usuários a entender documentos legais pesquisando informações, 
                resumindo documentos, extraindo informações-chave e comparando documentos.
                
                REGRAS IMPORTANTES:
                - Sempre baseie suas respostas no conteúdo do documento recuperado pela ferramenta de busca
                - Se a informação não for encontrada nos documentos, diga "Não encontrei essa informação no documento enviado."
                - Nunca invente ou alucine informações
                - Sempre cite o documento de origem e o número da página ao fornecer informações
                - Seja preciso e profissional em suas respostas
                - SEMPRE responda em português (pt-BR)"""),
                MessagesPlaceholder(variable_name="chat_history"),
                ("human", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ])
            
            self.agent = create_openai_tools_agent(self.llm, self.tools, self.prompt)
            self.agent_executor = AgentExecutor(
                agent=self.agent,
                tools=self.tools,
                verbose=True,
                handle_parsing_errors=True
            )
    
    def query(self, query: str, chat_history: list = None, document_id: str = None) -> dict:
        if not self.agent_executor:
            raise ValueError("OPENAI_API_KEY not configured")
        if chat_history is None:
            chat_history = []
        
        # Add document context to the input if document_id is provided
        input_text = query
        if document_id:
            input_text = f"[Document ID: {document_id}] {query}"
        
        result = self.agent_executor.invoke({
            "input": input_text,
            "chat_history": chat_history
        })
        
        return {
            "response": result["output"],
            "citations": self._extract_citations(result)
        }
    
    def _extract_citations(self, result: dict) -> list:
        # Extract citations from the agent's output
        citations = []
        output = result.get("output", "")
        
        # Simple extraction - in production, use more sophisticated parsing
        if "Document:" in output or "Page:" in output:
            # This is a placeholder - implement proper citation extraction
            citations.append({"source": "document", "text": output[:200]})
        
        return citations
