from __future__ import annotations

import logging
from typing import Optional
from uuid import UUID

from app.db.translation_session_service import TranslationSessionMySQLService
from app.models.compose import ComposeSentenceRequest
from app.models.translation_session import (
    TranslationSessionComposeRequest,
    TranslationSessionRead,
    TranslationSessionUpdate,
)
from .composer import SentenceComposer


class TranslationSessionManager:
    """Coordinates session persistence with the SentenceComposer."""

    def __init__(self, service: TranslationSessionMySQLService, composer: Optional[SentenceComposer] = None) -> None:
        self.service = service
        self.composer = composer or SentenceComposer()
        self.logger = logging.getLogger(__name__)

    async def compose(self, session_id: UUID, payload: TranslationSessionComposeRequest) -> TranslationSessionRead:
        session = self.service.get(session_id)
        if not session:
            raise ValueError("TranslationSession not found")

        context = session.context or ""
        compose_request = ComposeSentenceRequest(glosses=payload.glosses, letters=payload.letters, context=context)

        self.logger.info(
            "Compose start | session=%s | glosses=%s | letters=%s | context_len=%d",
            session_id,
            payload.glosses,
            payload.letters,
            len(context),
        )

        compose_result = await self.composer.compose_async(compose_request)

        updated_glosses = list(session.glosses) + payload.glosses
        existing_letters = session.letters or []
        new_letters = existing_letters + (payload.letters or [])
        updated_context = f"{context} {compose_result.text}".strip() if context else compose_result.text
        confidence = compose_result.confidence if compose_result.confidence is not None else 1.0

        update_payload = TranslationSessionUpdate(
            glosses=updated_glosses,
            letters=new_letters or None,
            context=updated_context,
            input_text=compose_result.text,
            adjusted_text=compose_result.text,
            compose_confidence=confidence,
        )

        updated_session = self.service.update(session_id, update_payload)
        if not updated_session:
            raise ValueError("TranslationSession not found after compose")

        self.logger.info("Compose complete | session=%s | text=%s", session_id, compose_result.text)
        return updated_session
