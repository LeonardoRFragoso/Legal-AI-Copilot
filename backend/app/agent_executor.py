"""
Agent Execution Service.

Provides reusable functions for executing agent tools (summary, extraction,
comparison, risk analysis, question answering) that can be called from:
- Direct endpoints
- Chat integration
- Post-upload automation

Does NOT call internal HTTP endpoints. All execution is in-process.
"""

from sqlalchemy.orm import Session
from typing import Optional, List, Dict, Any
import json
import logging
import time

from app.models import Document, Chunk, DocumentEmbedding, User, UserRole
from app.agent_router import LegalAgentRouter, AgentIntent, RouterDecision
from app.risk_analysis import RiskAnalyzer, RiskAnalysisResult
from app.ai_validator import AIValidator, CitationSource
from app.legal_agent import LegalAgent
from app.logger import logger

router = LegalAgentRouter()


def check_document_access(
    db: Session, document_id: str, user: User
) -> Document:
    """Check document exists and user has access. Raises ValueError if not."""
    document = db.query(Document).filter(Document.id == document_id).first()
    if not document:
        raise ValueError("Document not found")
    if user.role != UserRole.ADMIN and document.user_id != user.id:
        raise PermissionError("Access denied to this document")
    return document


def execute_summary(db: Session, document_id: str, legal_agent: LegalAgent) -> Dict:
    """Execute summary tool and return structured result."""
    start = time.time()
    logger.info("agent_tool_started", extra={"tool": "summarize_document", "document_id": document_id})

    try:
        result = legal_agent.tools[1]._run(str(document_id))
        duration_ms = int((time.time() - start) * 1000)
        logger.info("agent_tool_completed", extra={
            "tool": "summarize_document", "document_id": document_id, "duration_ms": duration_ms
        })
        return {
            "content": result,
            "structured_data": None,
            "error": None,
        }
    except Exception as e:
        duration_ms = int((time.time() - start) * 1000)
        logger.error("agent_tool_failed", extra={
            "tool": "summarize_document", "document_id": document_id,
            "duration_ms": duration_ms, "error_type": type(e).__name__
        })
        return {"content": "", "structured_data": None, "error": str(e)}


def execute_extraction(db: Session, document_id: str, legal_agent: LegalAgent) -> Dict:
    """Execute extraction tool and return structured result."""
    start = time.time()
    logger.info("agent_tool_started", extra={"tool": "extract_information", "document_id": document_id})

    try:
        result = legal_agent.tools[2]._run(str(document_id))

        json_str = result
        if json_str.startswith("```json"):
            json_str = json_str[7:]
        if json_str.startswith("```"):
            json_str = json_str[3:]
        if json_str.endswith("```"):
            json_str = json_str[:-3]

        data = json.loads(json_str.strip())

        duration_ms = int((time.time() - start) * 1000)
        logger.info("agent_tool_completed", extra={
            "tool": "extract_information", "document_id": document_id, "duration_ms": duration_ms
        })
        return {
            "content": "Informações extraídas com sucesso.",
            "structured_data": data,
            "error": None,
        }
    except json.JSONDecodeError:
        duration_ms = int((time.time() - start) * 1000)
        logger.error("agent_tool_failed", extra={
            "tool": "extract_information", "document_id": document_id,
            "duration_ms": duration_ms, "error_type": "JSONDecodeError"
        })
        return {
            "content": "Erro ao processar extração.",
            "structured_data": {"parties": [], "dates": [], "values": [], "clauses": []},
            "error": "JSON parsing error",
        }
    except Exception as e:
        duration_ms = int((time.time() - start) * 1000)
        logger.error("agent_tool_failed", extra={
            "tool": "extract_information", "document_id": document_id,
            "duration_ms": duration_ms, "error_type": type(e).__name__
        })
        return {"content": "", "structured_data": None, "error": str(e)}


def execute_comparison(
    db: Session, document_a_id: str, document_b_id: str, legal_agent: LegalAgent
) -> Dict:
    """Execute comparison tool and return structured result."""
    start = time.time()
    logger.info("agent_tool_started", extra={
        "tool": "compare_documents",
        "document_id": f"{document_a_id}+{document_b_id}"
    })

    try:
        result = legal_agent.tools[3]._run(str(document_a_id), str(document_b_id))
        duration_ms = int((time.time() - start) * 1000)
        logger.info("agent_tool_completed", extra={
            "tool": "compare_documents", "duration_ms": duration_ms
        })
        return {
            "content": result,
            "structured_data": None,
            "error": None,
        }
    except Exception as e:
        duration_ms = int((time.time() - start) * 1000)
        logger.error("agent_tool_failed", extra={
            "tool": "compare_documents", "duration_ms": duration_ms, "error_type": type(e).__name__
        })
        return {"content": "", "structured_data": None, "error": str(e)}


def execute_risk_analysis(db: Session, document_id: str) -> Dict:
    """Execute risk analysis and return structured result."""
    start = time.time()
    logger.info("agent_tool_started", extra={"tool": "contract_risk_analysis", "document_id": document_id})

    try:
        analyzer = RiskAnalyzer(db)
        result = analyzer.analyze(document_id)

        duration_ms = int((time.time() - start) * 1000)
        logger.info("agent_tool_completed", extra={
            "tool": "contract_risk_analysis", "document_id": document_id,
            "duration_ms": duration_ms, "overall_risk": result.overall_risk.value
        })

        return {
            "content": _format_risk_response_for_chat(result),
            "structured_data": result.to_dict(),
            "error": None,
        }
    except Exception as e:
        duration_ms = int((time.time() - start) * 1000)
        logger.error("agent_tool_failed", extra={
            "tool": "contract_risk_analysis", "document_id": document_id,
            "duration_ms": duration_ms, "error_type": type(e).__name__
        })
        return {"content": "", "structured_data": None, "error": str(e)}


def execute_question_answering(
    db: Session,
    query: str,
    chat_history: List[Dict],
    document_id: Optional[str],
    legal_agent: LegalAgent,
) -> Dict:
    """Execute question answering via RAG and return result with validation."""
    start = time.time()
    logger.info("agent_tool_started", extra={
        "tool": "semantic_search", "document_id": document_id or "none"
    })

    try:
        result = legal_agent.query(query, chat_history, document_id)

        # Validate with guardrails
        validator = AIValidator.get_default_validator()

        retrieved_chunks = []
        if document_id:
            doc = db.query(Document).filter(Document.id == document_id).first()
            if doc:
                chunks = db.query(Chunk).filter(Chunk.document_id == document_id).all()
                for chunk in chunks:
                    embedding = db.query(DocumentEmbedding).filter(
                        DocumentEmbedding.chunk_id == chunk.id
                    ).first()
                    retrieved_chunks.append({
                        "id": chunk.id,
                        "text": chunk.text,
                        "page_number": chunk.page_number,
                        "similarity_score": 0.5,
                        "document_id": doc.id,
                        "document_title": doc.title,
                    })

        citations_data = []
        if result.get("citations"):
            for citation in result["citations"]:
                if isinstance(citation, dict):
                    citations_data.append(citation)

        validated = validator.validate(
            response_content=result["response"],
            retrieved_chunks=retrieved_chunks,
            citations=citations_data,
            document_title=document_id or "Documento",
        )

        duration_ms = int((time.time() - start) * 1000)
        logger.info("agent_tool_completed", extra={
            "tool": "semantic_search", "document_id": document_id or "none",
            "duration_ms": duration_ms, "blocked": validated.blocked
        })

        final_content = validated.content if not validated.blocked else validated.block_reason

        return {
            "content": final_content,
            "structured_data": None,
            "validation": {
                "confidence_score": validated.validation.confidence_score,
                "confidence_level": validated.validation.confidence_level,
                "hallucination_risk": validated.validation.hallucination_risk,
                "blocked": validated.blocked,
                "disclaimer": validated.validation.disclaimer,
            },
            "citations": [c.to_dict() for c in validated.validation.citations],
            "blocked": validated.blocked,
            "error": None,
        }
    except ValueError as e:
        # OpenAI API key not configured
        duration_ms = int((time.time() - start) * 1000)
        logger.warning("agent_tool_failed", extra={
            "tool": "semantic_search", "duration_ms": duration_ms, "error_type": "ValueError"
        })
        return {
            "content": f"OPENAI_API_KEY não configurada. Mensagem recebida: {query}",
            "structured_data": None,
            "validation": None,
            "citations": [],
            "blocked": False,
            "error": None,
        }
    except Exception as e:
        duration_ms = int((time.time() - start) * 1000)
        logger.error("agent_tool_failed", extra={
            "tool": "semantic_search", "duration_ms": duration_ms, "error_type": type(e).__name__
        })
        return {"content": "", "structured_data": None, "error": str(e)}


def execute_agent_decision(
    db: Session,
    user_input: str,
    decision: RouterDecision,
    user: User,
    legal_agent: LegalAgent,
    chat_history: List[Dict] = None,
    conversation_document_id: Optional[str] = None,
) -> Dict:
    """
    Execute a router decision and return the result.

    This is the main entry point for chat integration and automation.
    Validates document access before executing any tool.
    """
    if chat_history is None:
        chat_history = []

    intent = decision.intent
    result = {
        "intent": intent.value,
        "tool": decision.tool,
        "content": "",
        "structured_data": None,
        "validation": None,
        "citations": [],
        "disclaimer": "",
        "blocked": False,
        "error": None,
    }

    if intent == AgentIntent.UNKNOWN:
        result["content"] = (
            "Não consegui identificar o que você precisa. "
            "Tente perguntar sobre resumos, extração de informações, "
            "comparação de documentos, análise de riscos ou faça "
            "uma pergunta específica sobre o documento."
        )
        return result

    # Determine document_id
    document_id = None
    if decision.required_documents:
        document_id = decision.required_documents[0]
    elif conversation_document_id:
        document_id = conversation_document_id

    # Validate document access for tools that need it
    if intent in [
        AgentIntent.SUMMARIZE_DOCUMENT,
        AgentIntent.EXTRACT_INFORMATION,
        AgentIntent.IDENTIFY_RISKS,
        AgentIntent.QUESTION_ANSWERING,
    ]:
        if not document_id:
            result["error"] = "Nenhum documento associado. Selecione um documento para continuar."
            result["content"] = result["error"]
            return result

        try:
            check_document_access(db, document_id, user)
        except ValueError:
            result["error"] = "Documento não encontrado."
            result["content"] = result["error"]
            return result
        except PermissionError:
            result["error"] = "Acesso negado a este documento."
            result["content"] = result["error"]
            return result

    # Execute the appropriate tool
    if intent == AgentIntent.SUMMARIZE_DOCUMENT:
        tool_result = execute_summary(db, document_id, legal_agent)
        result.update(tool_result)

    elif intent == AgentIntent.EXTRACT_INFORMATION:
        tool_result = execute_extraction(db, document_id, legal_agent)
        result.update(tool_result)

    elif intent == AgentIntent.IDENTIFY_RISKS:
        tool_result = execute_risk_analysis(db, document_id)
        result.update(tool_result)
        if result["structured_data"]:
            risk_data = result["structured_data"]
            result["disclaimer"] = risk_data.get("disclaimer", "")
            result["citations"] = risk_data.get("citations", [])

    elif intent == AgentIntent.COMPARE_DOCUMENTS:
        # Need two documents
        doc_ids = decision.required_documents
        if len(doc_ids) < 2:
            result["error"] = "Comparação requer dois documentos. Selecione dois documentos para continuar."
            result["content"] = result["error"]
            return result

        try:
            check_document_access(db, doc_ids[0], user)
            check_document_access(db, doc_ids[1], user)
        except ValueError:
            result["error"] = "Um ou ambos os documentos não foram encontrados."
            result["content"] = result["error"]
            return result
        except PermissionError:
            result["error"] = "Acesso negado a um ou ambos os documentos."
            result["content"] = result["error"]
            return result

        tool_result = execute_comparison(db, doc_ids[0], doc_ids[1], legal_agent)
        result.update(tool_result)

    elif intent == AgentIntent.QUESTION_ANSWERING:
        tool_result = execute_question_answering(
            db, user_input, chat_history, document_id, legal_agent
        )
        result.update(tool_result)
        if result.get("validation"):
            result["disclaimer"] = result["validation"].get("disclaimer", "")

    return result


def _format_risk_response_for_chat(result: RiskAnalysisResult) -> str:
    """Format risk analysis result as readable text for chat."""
    lines = []
    lines.append(f"🔍 **Análise de Riscos**")
    lines.append(f"")
    lines.append(f"**Risco Geral:** {result.overall_risk.value.upper()}")
    lines.append(f"**Sustentação Documental:** {result.confidence_score}% ({result.confidence_level})")
    lines.append(f"")
    lines.append(f"**Resumo:** {result.summary}")
    lines.append(f"")

    if result.risks:
        lines.append(f"**Riscos Identificados ({len(result.risks)}):**")
        lines.append(f"")
        for i, risk in enumerate(result.risks, 1):
            lines.append(f"{i}. **{risk.title}** [{risk.severity.value.upper()}]")
            lines.append(f"   - Categoria: {risk.category.value}")
            lines.append(f"   - {risk.description}")
            lines.append(f"   - Recomendação: {risk.recommendation}")
            lines.append(f"")
    else:
        lines.append("Nenhum risco significativo detectado.")
        lines.append(f"")

    if result.disclaimer:
        lines.append(f"_{result.disclaimer}_")

    return "\n".join(lines)
