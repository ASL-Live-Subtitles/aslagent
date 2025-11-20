from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException

from app.models.compose import ComposeSentenceRequest, ComposeSentenceResponse
from app.services.composer import SentenceComposer

router = APIRouter(prefix="/compose", tags=["Compose"])
logger = logging.getLogger(__name__)


@router.post("/sentence", response_model=ComposeSentenceResponse, status_code=200)
def compose_sentence(request: ComposeSentenceRequest):
    try:
        composer = SentenceComposer()
        logger.info("Standalone compose request | glosses=%s | letters=%s | context=%s", request.glosses, request.letters, request.context)
        response = composer.compose(request)
        logger.info("Standalone compose result | text=%s", response.text)
        return response
    except RuntimeError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"Failed to call OpenAI: {exc}") from exc
