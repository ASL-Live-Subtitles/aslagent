from __future__ import annotations

import os
from typing import List

import logging

from openai import AsyncOpenAI, OpenAI

from app.models.compose import ComposeSentenceRequest, ComposeSentenceResponse


class SentenceComposer:
    """Wrapper around OpenAI's chat completions for building fluent English sentences."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        self.logger = logging.getLogger(__name__)
        api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured.")
        self.model = model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
        self.client = OpenAI(api_key=api_key)
        self.async_client = AsyncOpenAI(api_key=api_key)

    def _build_prompt(self, glosses: List[str], context: str | None, letters: List[str] | None) -> str:
        base = (
            "You are assisting an ASL translation service. "
            "Given a list of glosses (English upper-case words representing ASL signs), "
            "compose a natural-sounding English sentence. "
            "Preserve the meaning, be concise, and return only the sentence."
        )
        parts = [base, f"Glosses: {', '.join(glosses)}."]
        if letters:
            parts.append(f"Detected spelled letters: {', '.join(letters)}.")
        if context:
            parts.append(f"Conversation context: {context}")
        return "\n".join(parts)

    def compose(self, request: ComposeSentenceRequest) -> ComposeSentenceResponse:
        composer = SentenceComposer(api_key=request.openai_api_key, model=request.openai_model)
        return composer._compose_sync(request)

    def _compose_sync(self, request: ComposeSentenceRequest) -> ComposeSentenceResponse:
        prompt = self._build_prompt(request.glosses, request.context, request.letters)
        self.logger.info("Composing sentence | glosses=%s | letters=%s | context=%s", request.glosses, request.letters, request.context)

        completion = self.client.chat.completions.create(
            model=self.model,
            temperature=0.3,
            messages=[
                {"role": "system", "content": "You convert ASL gloss sequences into fluent English sentences."},
                {"role": "user", "content": prompt},
            ],
        )

        text = completion.choices[0].message.content.strip()
        self.logger.info("Compose result | model=%s | text=%s", self.model, text)
        return ComposeSentenceResponse(text=text, confidence=None, model=self.model)

    async def compose_async(self, request: ComposeSentenceRequest) -> ComposeSentenceResponse:
        composer = SentenceComposer(api_key=request.openai_api_key, model=request.openai_model)
        return await composer._compose_async_internal(request)

    async def _compose_async_internal(self, request: ComposeSentenceRequest) -> ComposeSentenceResponse:
        prompt = self._build_prompt(request.glosses, request.context, request.letters)
        self.logger.info(
            "Composing sentence async | glosses=%s | letters=%s | context=%s",
            request.glosses,
            request.letters,
            request.context,
        )

        completion = await self.async_client.chat.completions.create(
            model=self.model,
            temperature=0.3,
            messages=[
                {"role": "system", "content": "You convert ASL gloss sequences into fluent English sentences."},
                {"role": "user", "content": prompt},
            ],
        )

        text = completion.choices[0].message.content.strip()
        self.logger.info("Compose result async | model=%s | text=%s", self.model, text)
        return ComposeSentenceResponse(text=text, confidence=None, model=self.model)
