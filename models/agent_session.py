from __future__ import annotations
from typing import Optional, Dict
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class AgentSessionBase(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    input_text: str = Field(
        ...,
        description="Text produced by ASL translation model.",
        json_schema_extra={"example": "What time is it"},
    )
    detected_emotion: str = Field(
        ...,
        description="Detected emotion from the ASL model output.",
        json_schema_extra={"example": "frustrated"},
    )
    detected_intent: str = Field(
        ...,
        description="Detected intent from ASL model output.",
        json_schema_extra={"example": "question"},
    )
    adjusted_text: str = Field(
        ...,
        description="Text after punctuation and tone adjustment.",
        json_schema_extra={"example": "What time is it?"},
    )
    tts_metadata: Dict[str, str] = Field(
        ...,
        description="Metadata for TTS tone and pitch adjustment.",
        json_schema_extra={"example": {"tone": "soft", "pitch": "low"}},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": str(uuid4()),
                    "input_text": "What time is it",
                    "detected_emotion": "frustrated",
                    "detected_intent": "question",
                    "adjusted_text": "What time is it?",
                    "tts_metadata": {"tone": "soft", "pitch": "low"},
                }
            ]
        }
    }


class AgentSessionCreate(AgentSessionBase):
    pass


class AgentSessionRead(AgentSessionBase):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": str(uuid4()),
                    "input_text": "What time is it",
                    "detected_emotion": "frustrated",
                    "detected_intent": "question",
                    "adjusted_text": "What time is it?",
                    "tts_metadata": {"tone": "soft", "pitch": "low"},
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                }
            ]
        }
    }


class AgentSessionUpdate(BaseModel):
    adjusted_text: Optional[str] = Field(None, description="Updated adjusted text.", json_schema_extra={"example": "What time is it?"})
    tts_metadata: Optional[Dict[str, str]] = Field(None, description="Updated TTS metadata.", json_schema_extra={"example": {"tone": "neutral", "pitch": "medium"}})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "adjusted_text": "What time is it?",
                    "tts_metadata": {"tone": "neutral", "pitch": "medium"},
                }
            ]
        }
    }