"""
Automation service for post-upload processing.

Runs summary + risk analysis after document upload, persists results,
and sends webhook notification. Uses FastAPI BackgroundTasks (non-durable).
"""

from sqlalchemy.orm import Session
from app.models import AutomationRun, Document, User
from app.agent_executor import execute_summary, execute_risk_analysis
from app.webhook_service import build_analysis_completed_payload, send_webhook
from app.logger import logger
from app.database import SessionLocal
from datetime import datetime
from typing import Optional, Dict, Any
import json


def create_automation_run(
    db: Session,
    document_id: str,
    user_id: str,
    automation_type: str = "post_upload",
) -> AutomationRun:
    """Create a new automation run record."""
    run = AutomationRun(
        document_id=document_id,
        user_id=user_id,
        automation_type=automation_type,
        status="PENDING",
        current_step="DOCUMENT_PROCESSING",
        progress_percent=0,
        webhook_status="pending",
    )
    db.add(run)
    db.commit()
    db.refresh(run)

    logger.info("automation_started", extra={
        "run_id": run.id,
        "document_id": document_id,
        "user_id": user_id,
    })

    return run


def update_run_status(
    db: Session,
    run_id: str,
    status: str = None,
    current_step: str = None,
    progress_percent: int = None,
    error_message: str = None,
    summary_result: Any = None,
    risk_result: Any = None,
    webhook_status: str = None,
    webhook_error: str = None,
):
    """Update automation run fields."""
    run = db.query(AutomationRun).filter(AutomationRun.id == run_id).first()
    if not run:
        return

    if status is not None:
        run.status = status
    if current_step is not None:
        run.current_step = current_step
    if progress_percent is not None:
        run.progress_percent = progress_percent
    if error_message is not None:
        run.error_message = error_message
    if summary_result is not None:
        run.summary_result = summary_result
    if risk_result is not None:
        run.risk_result = risk_result
    if webhook_status is not None:
        run.webhook_status = webhook_status
    if webhook_error is not None:
        run.webhook_error = webhook_error

    if status in ("COMPLETED", "FAILED", "PARTIAL_SUCCESS"):
        run.completed_at = datetime.utcnow()

    if status == "RUNNING" and run.started_at is None:
        run.started_at = datetime.utcnow()

    run.updated_at = datetime.utcnow()
    db.commit()


def run_post_upload_automation(
    run_id: str,
    document_id: str,
    user_id: str,
):
    """
    Background task: run summary + risk analysis + webhook.

    Uses its own DB session since it runs in background.
    """
    db = SessionLocal()

    try:
        # Step 1: Start
        update_run_status(
            db, run_id,
            status="RUNNING",
            current_step="DOCUMENT_PROCESSING",
            progress_percent=10,
        )
        logger.info("automation_step_started", extra={
            "run_id": run_id, "step": "DOCUMENT_PROCESSING"
        })

        document = db.query(Document).filter(Document.id == document_id).first()
        if not document:
            update_run_status(
                db, run_id,
                status="FAILED",
                error_message="Document not found",
                progress_percent=100,
            )
            logger.error("automation_failed", extra={
                "run_id": run_id, "reason": "document_not_found"
            })
            return

        # Step 2: Summary
        update_run_status(
            db, run_id,
            current_step="SUMMARY",
            progress_percent=30,
        )
        logger.info("automation_step_started", extra={
            "run_id": run_id, "step": "SUMMARY"
        })

        from app.legal_agent import LegalAgent
        legal_agent = LegalAgent()

        summary_result = execute_summary(db, document_id, legal_agent)

        if summary_result.get("error"):
            logger.warning("automation_step_completed", extra={
                "run_id": run_id, "step": "SUMMARY", "status": "partial_error"
            })
        else:
            logger.info("automation_step_completed", extra={
                "run_id": run_id, "step": "SUMMARY", "status": "success"
            })

        update_run_status(
            db, run_id,
            progress_percent=50,
            summary_result={"summary": summary_result.get("content", "")},
        )

        # Step 3: Risk Analysis
        update_run_status(
            db, run_id,
            current_step="RISK_ANALYSIS",
            progress_percent=70,
        )
        logger.info("automation_step_started", extra={
            "run_id": run_id, "step": "RISK_ANALYSIS"
        })

        risk_result = execute_risk_analysis(db, document_id)

        if risk_result.get("error"):
            logger.warning("automation_step_completed", extra={
                "run_id": run_id, "step": "RISK_ANALYSIS", "status": "partial_error"
            })
        else:
            logger.info("automation_step_completed", extra={
                "run_id": run_id, "step": "RISK_ANALYSIS", "status": "success"
            })

        risk_data = risk_result.get("structured_data")
        update_run_status(
            db, run_id,
            progress_percent=85,
            risk_result=risk_data,
        )

        # Step 4: Webhook
        update_run_status(
            db, run_id,
            current_step="WEBHOOK",
            progress_percent=90,
        )
        logger.info("automation_step_started", extra={
            "run_id": run_id, "step": "WEBHOOK"
        })

        overall_risk = risk_data.get("overall_risk", "") if risk_data else ""
        confidence_score = risk_data.get("confidence_score", 0) if risk_data else 0

        payload = build_analysis_completed_payload(
            run_id=run_id,
            document_id=document_id,
            document_title=document.title,
            status="COMPLETED",
            summary_available=bool(summary_result.get("content")),
            risk_analysis_available=bool(risk_data),
            overall_risk=overall_risk,
            confidence_score=confidence_score,
        )

        webhook_result = send_webhook(payload, payload["event_id"])

        if webhook_result["success"]:
            update_run_status(
                db, run_id,
                webhook_status="sent",
                progress_percent=95,
            )
            logger.info("automation_step_completed", extra={
                "run_id": run_id, "step": "WEBHOOK", "status": "success"
            })
        else:
            update_run_status(
                db, run_id,
                webhook_status="failed",
                webhook_error=webhook_result.get("error", "Unknown error"),
            )
            logger.warning("automation_step_completed", extra={
                "run_id": run_id, "step": "WEBHOOK", "status": "failed"
            })

        # Step 5: Finalize
        has_errors = bool(summary_result.get("error") or risk_result.get("error"))
        webhook_failed = not webhook_result["success"]

        if has_errors and webhook_failed:
            final_status = "PARTIAL_SUCCESS"
        elif webhook_failed:
            final_status = "PARTIAL_SUCCESS"
        elif has_errors:
            final_status = "PARTIAL_SUCCESS"
        else:
            final_status = "COMPLETED"

        update_run_status(
            db, run_id,
            status=final_status,
            current_step="COMPLETED",
            progress_percent=100,
        )
        logger.info("automation_completed", extra={
            "run_id": run_id, "status": final_status
        })

    except Exception as e:
        logger.error("automation_failed", extra={
            "run_id": run_id, "error_type": type(e).__name__
        })
        update_run_status(
            db, run_id,
            status="FAILED",
            error_message=str(e)[:500],
            progress_percent=100,
        )
    finally:
        db.close()
