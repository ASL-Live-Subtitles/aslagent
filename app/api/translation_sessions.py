from __future__ import annotations

from typing import List, Optional
from uuid import UUID

import logging

from fastapi import APIRouter, HTTPException, Path, Query

from app.db import TranslationSessionMySQLService
from app.models.translation_session import (
    TranslationSessionComposeRequest,
    TranslationSessionCreate,
    TranslationSessionRead,
    TranslationSessionUpdate,
)
from app.services.translation import TranslationSessionManager

router = APIRouter(prefix="/translation_sessions", tags=["TranslationSession"])
logger = logging.getLogger(__name__)


def _service() -> TranslationSessionMySQLService:
    return TranslationSessionMySQLService()


@router.post("", response_model=TranslationSessionRead, status_code=201)
def create_translation_session(session: TranslationSessionCreate):
    service = _service()
    try:
        return service.create(session)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}") from exc
    finally:
        service.close_connection()


@router.get("", response_model=List[TranslationSessionRead])
def list_translation_sessions(
    detected_emotion: Optional[str] = Query(None, description="Filter by detected emotion"),
    detected_intent: Optional[str] = Query(None, description="Filter by detected intent"),
):
    service = _service()
    try:
        return service.list(
            detected_emotion=detected_emotion,
            detected_intent=detected_intent,
        )
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}") from exc
    finally:
        service.close_connection()


@router.get("/{session_id}", response_model=TranslationSessionRead)
def get_translation_session(session_id: UUID = Path(..., description="Translation session ID")):
    service = _service()
    try:
        record = service.get(session_id)
        if not record:
            raise HTTPException(status_code=404, detail="TranslationSession not found")
        return record
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}") from exc
    finally:
        service.close_connection()


@router.put("/{session_id}", response_model=TranslationSessionRead)
def update_translation_session(session_id: UUID, session_update: TranslationSessionUpdate):
    service = _service()
    try:
        updated = service.update(session_id, session_update)
        if not updated:
            raise HTTPException(status_code=404, detail="TranslationSession not found")
        return updated
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}") from exc
    finally:
        service.close_connection()


@router.post("/{session_id}/compose", response_model=TranslationSessionRead)
async def compose_sentence_for_session(session_id: UUID, payload: TranslationSessionComposeRequest):
    service = _service()
    manager = TranslationSessionManager(service)
    try:
        return await manager.compose(session_id, payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Compose request failed: {exc}") from exc
    finally:
        service.close_connection()


@router.delete("/{session_id}", status_code=200)
def delete_translation_session(session_id: UUID):
    service = _service()
    try:
        deleted = service.delete(session_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="TranslationSession not found")
        return {"message": "TranslationSession deleted successfully."}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}") from exc
    finally:
        service.close_connection()
