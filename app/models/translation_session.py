from __future__ import annotations
from typing import Optional, Dict, List, Any
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class TranslationSessionBase(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    user_id: Optional[str] = Field(
        None,
        description="External user identifier to associate preferences.",
        json_schema_extra={"example": "user_123"},
    )
    glosses: List[str] = Field(
        ...,
        description="Ordered list of glosses sent to compose_sentence.",
        json_schema_extra={"example": ["IX-1", "GOOD", "IDEA"]},
    )
    letters: Optional[List[str]] = Field(
        None,
        description="Optional detected fingerspelling letters.",
        json_schema_extra={"example": ["A", "I"]},
    )
    preferred_words: Dict[str, str] = Field(
        default_factory=dict,
        description="Per-user overrides for gloss → spoken words.",
        json_schema_extra={"example": {"GOOD": "fantastic"}},
    )
    context: Optional[str] = Field(
        None,
        description="Conversation context forwarded to compose_sentence.",
        json_schema_extra={"example": "Planning the next sprint"},
    )
    input_text: str = Field(
        ...,
        description="Text produced by ASL translation model.",
        json_schema_extra={"example": "What time is it"},
    )
    compose_confidence: float = Field(
        ...,
        description="Confidence score from compose_sentence.",
        json_schema_extra={"example": 0.9},
    )
    compose_alternatives: List[str] = Field(
        default_factory=list,
        description="Alternate phrases to display to the user.",
        json_schema_extra={"example": ["Good idea."]},
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
    emphasis: List[str] = Field(
        default_factory=list,
        description="Tokens called out for emphasis by analyze_clip.",
        json_schema_extra={"example": ["good"]},
    )
    adjusted_text: str = Field(
        ...,
        description="Text after punctuation and tone adjustment.",
        json_schema_extra={"example": "What time is it?"},
    )
    tts_metadata: Dict[str, Any] = Field(
        ...,
        description="Metadata used when calling TTS (voice, tone, audio URL, visemes).",
        json_schema_extra={
            "example": {
                "voice": "en-female-1",
                "tone": "soft",
                "audio_url": "https://example.com/audio.wav",
                "visemes": ["AA", "B"],
            }
        },
    )
    tool_metadata: Dict[str, str] = Field(
        default_factory=dict,
        description="Version identifiers for the external tools invoked.",
        json_schema_extra={"example": {"compose_version": "2024-09-25"}},
    )
    summary_text: Optional[str] = Field(
        None,
        description="Summary returned by summarize_session.",
        json_schema_extra={"example": "Confirmed timeline for Friday delivery."},
    )
    summary_topics: List[str] = Field(
        default_factory=list,
        description="Topics extracted by summarize_session.",
        json_schema_extra={"example": ["timelines", "next steps"]},
    )
    summary_action_items: List[str] = Field(
        default_factory=list,
        description="Action items extracted by summarize_session.",
        json_schema_extra={"example": ["Email recap", "Update roadmap"]},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": str(uuid4()),
                    "user_id": "user_123",
                    "glosses": ["IX-1", "GOOD", "IDEA"],
                    "letters": ["G"],
                    "preferred_words": {"GOOD": "fantastic"},
                    "context": "Brainstorming session",
                    "input_text": "What time is it",
                    "compose_confidence": 0.9,
                    "compose_alternatives": ["Could you tell me the time?"],
                    "detected_emotion": "frustrated",
                    "detected_intent": "question",
                    "emphasis": ["time"],
                    "adjusted_text": "What time is it?",
                    "tts_metadata": {
                        "voice": "en-female-1",
                        "tone": "soft",
                        "audio_url": "https://example.com/audio.wav",
                        "visemes": ["AA", "B"],
                    },
                    "tool_metadata": {"compose_version": "2024-09-25"},
                    "summary_text": "Asked for the current time.",
                    "summary_topics": ["time"],
                    "summary_action_items": [],
                }
            ]
        }
    }


class TranslationSessionCreate(TranslationSessionBase):
    pass


class TranslationSessionRead(TranslationSessionBase):
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


class TranslationSessionUpdate(BaseModel):
    user_id: Optional[str] = Field(None, description="Updated user identifier.")
    glosses: Optional[List[str]] = Field(None, description="Updated gloss list.")
    letters: Optional[List[str]] = Field(None, description="Updated letters.")
    context: Optional[str] = Field(None, description="Updated dialog context.")
    input_text: Optional[str] = Field(None, description="Updated model output text.")
    preferred_words: Optional[Dict[str, str]] = Field(
        None,
        description="Updated gloss preferences.",
        json_schema_extra={"example": {"GOOD": "great"}},
    )
    compose_confidence: Optional[float] = Field(
        None, description="Updated compose confidence.", json_schema_extra={"example": 0.95}
    )
    compose_alternatives: Optional[List[str]] = Field(
        None,
        description="Updated alternative phrasings.",
        json_schema_extra={"example": ["It's a great plan."]},
    )
    detected_emotion: Optional[str] = Field(
        None, description="Override detected emotion.", json_schema_extra={"example": "neutral"}
    )
    detected_intent: Optional[str] = Field(
        None, description="Override detected intent.", json_schema_extra={"example": "statement"}
    )
    emphasis: Optional[List[str]] = Field(
        None, description="Updated emphasis tokens.", json_schema_extra={"example": ["idea"]}
    )
    adjusted_text: Optional[str] = Field(
        None, description="Updated adjusted text.", json_schema_extra={"example": "What time is it?"}
    )
    tts_metadata: Optional[Dict[str, Any]] = Field(
        None,
        description="Updated TTS metadata.",
        json_schema_extra={
            "example": {
                "voice": "en-male-1",
                "tone": "neutral",
                "audio_url": "https://example.com/audio2.wav",
            }
        },
    )
    tool_metadata: Optional[Dict[str, str]] = Field(
        None, description="Updated tool version metadata.", json_schema_extra={"example": {"compose_version": "2024-10-01"}}
    )
    summary_text: Optional[str] = Field(
        None,
        description="Updated session summary.",
        json_schema_extra={"example": "Aligned on final deliverable."},
    )
    summary_topics: Optional[List[str]] = Field(
        None, description="Updated summary topics.", json_schema_extra={"example": ["deliverables"]}
    )
    summary_action_items: Optional[List[str]] = Field(
        None,
        description="Updated action items.",
        json_schema_extra={"example": ["Follow up with stakeholders"]},
    )


class TranslationSessionComposeRequest(BaseModel):
    glosses: List[str] = Field(
        ...,
        description="Incoming glosses/words from the ASL recognizer.",
        json_schema_extra={"example": ["IX-1", "FINISH", "WORK"]},
    )
    letters: Optional[List[str]] = Field(
        None,
        description="Optional letters from fingerspelling.",
        json_schema_extra={"example": ["A", "I"]},
    )

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
