from __future__ import annotations
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class EmotionAnalysisBase(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    emotion: str = Field(
        ...,
        description="Detected emotion (e.g., happy, frustrated)",
        json_schema_extra={"example": "frustrated"},
    )
    intent: str = Field(
        ...,
        description="Detected intent (e.g., question, statement)",
        json_schema_extra={"example": "question"},
    )
    punctuation_adjustment: str = Field(
        ...,
        description="Rule for punctuation modification based on emotion and intent.",
        json_schema_extra={"example": "add question mark"},
    )
    tts_tone: str = Field(
        ...,
        description="Tone adjustment for the text-to-speech system.",
        json_schema_extra={"example": "curious"},
    )
    confidence_threshold: float = Field(
        0.7,
        description="Minimum confidence to apply this mapping rule.",
        json_schema_extra={"example": 0.85},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": str(uuid4()),
                    "emotion": "frustrated",
                    "intent": "question",
                    "punctuation_adjustment": "add question mark",
                    "tts_tone": "curious",
                    "confidence_threshold": 0.85,
                }
            ]
        }
    }


class EmotionAnalysisCreate(EmotionAnalysisBase):
    pass


class EmotionAnalysisRead(EmotionAnalysisBase):
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": str(uuid4()),
                    "emotion": "frustrated",
                    "intent": "question",
                    "punctuation_adjustment": "add question mark",
                    "tts_tone": "curious",
                    "confidence_threshold": 0.85,
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat(),
                }
            ]
        }
    }


class EmotionAnalysisUpdate(BaseModel):
    emotion: Optional[str] = Field(None, description="Detected emotion.", json_schema_extra={"example": "neutral"})
    intent: Optional[str] = Field(None, description="Detected intent.", json_schema_extra={"example": "statement"})
    punctuation_adjustment: Optional[str] = Field(None, description="Updated punctuation rule.", json_schema_extra={"example": "add period"})
    tts_tone: Optional[str] = Field(None, description="Updated tone rule.", json_schema_extra={"example": "soft"})
    confidence_threshold: Optional[float] = Field(None, description="Updated confidence threshold.", json_schema_extra={"example": 0.75})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "emotion": "neutral",
                    "intent": "statement",
                    "punctuation_adjustment": "add period",
                    "tts_tone": "soft",
                    "confidence_threshold": 0.75,
                }
            ]
        }
    }
