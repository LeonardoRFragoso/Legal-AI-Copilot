"""
Webhook service for automation events.

Sends analysis.completed events to external systems (e.g., n8n).
Handles timeouts, retries, and idempotency keys.
"""

import httpx
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import logging

from app.config import get_settings
from app.logger import logger

logger = logging.getLogger(__name__)


def build_analysis_completed_payload(
    run_id: str,
    document_id: str,
    document_title: str,
    status: str,
    summary_available: bool,
    risk_analysis_available: bool,
    overall_risk: str = "",
    confidence_score: int = 0,
) -> Dict[str, Any]:
    """Build the webhook payload for analysis.completed event."""
    return {
        "event": "analysis.completed",
        "event_id": str(uuid.uuid4()),
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "document": {
            "id": document_id,
            "title": document_title,
        },
        "automation": {
            "run_id": run_id,
            "status": status,
        },
        "analysis": {
            "summary_available": summary_available,
            "risk_analysis_available": risk_analysis_available,
            "overall_risk": overall_risk,
            "confidence_score": confidence_score,
        },
    }


def send_webhook(
    payload: Dict[str, Any],
    event_id: str,
) -> Dict[str, Any]:
    """
    Send webhook to configured URL.

    Returns dict with:
    - success: bool
    - status_code: int or None
    - error: str or None
    """
    settings = get_settings()

    if not settings.automation_webhook_enabled:
        logger.info("webhook_skipped", extra={"reason": "webhook_disabled"})
        return {"success": False, "status_code": None, "error": "Webhook disabled"}

    if not settings.automation_webhook_url:
        logger.info("webhook_skipped", extra={"reason": "no_url_configured"})
        return {"success": False, "status_code": None, "error": "No URL configured"}

    max_retries = settings.automation_webhook_max_retries
    timeout = settings.automation_webhook_timeout_seconds

    logger.info("webhook_started", extra={
        "event_id": event_id,
        "url": settings.automation_webhook_url,
        "max_retries": max_retries,
    })

    for attempt in range(1, max_retries + 1):
        try:
            with httpx.Client(timeout=timeout) as client:
                response = client.post(
                    settings.automation_webhook_url,
                    json=payload,
                    headers={
                        "Content-Type": "application/json",
                        "X-Idempotency-Key": event_id,
                    },
                )

                if response.status_code < 400:
                    logger.info("webhook_succeeded", extra={
                        "event_id": event_id,
                        "status_code": response.status_code,
                        "attempt": attempt,
                    })
                    return {
                        "success": True,
                        "status_code": response.status_code,
                        "error": None,
                    }
                else:
                    logger.warning("webhook_failed", extra={
                        "event_id": event_id,
                        "status_code": response.status_code,
                        "attempt": attempt,
                    })

        except httpx.TimeoutException:
            logger.warning("webhook_failed", extra={
                "event_id": event_id,
                "error_type": "TimeoutException",
                "attempt": attempt,
            })
        except httpx.ConnectError:
            logger.warning("webhook_failed", extra={
                "event_id": event_id,
                "error_type": "ConnectError",
                "attempt": attempt,
            })
        except Exception as e:
            logger.error("webhook_failed", extra={
                "event_id": event_id,
                "error_type": type(e).__name__,
                "attempt": attempt,
            })

    logger.error("webhook_failed", extra={
        "event_id": event_id,
        "reason": "max_retries_exhausted",
    })
    return {
        "success": False,
        "status_code": None,
        "error": "Max retries exhausted",
    }
