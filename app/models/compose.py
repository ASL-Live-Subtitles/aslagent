from __future__ import annotations

from typing import List, Optional
from pydantic import BaseModel, Field


class ComposeSentenceRequest(BaseModel):
    glosses: List[str] = Field(..., description="Ordered list of glosses or words to compose.", json_schema_extra={"example": ["IX-1", "GOOD", "IDEA"]})
    letters: Optional[List[str]] = Field(None, description="Optional detected finger-spelled letters.", json_schema_extra={"example": ["A", "I"]})
    context: Optional[str] = Field(None, description="Additional conversational context.", json_schema_extra={"example": "Brainstorming a new sprint plan."})
    openai_api_key: Optional[str] = Field(
        None,
        description="Optional per-request OpenAI API key. Falls back to server env if omitted.",
        json_schema_extra={"example": "sk-your-key"},
    )
    openai_model: Optional[str] = Field(
        None,
        description="Optional per-request model override.",
        json_schema_extra={"example": "gpt-4o-mini"},
    )


class ComposeSentenceResponse(BaseModel):
    text: str = Field(..., description="Fluent English sentence produced by the composer.", json_schema_extra={"example": "That's a good idea for our next sprint."})
    confidence: Optional[float] = Field(None, description="Optional heuristic confidence for the generation.", json_schema_extra={"example": 0.92})
    model: str = Field(..., description="OpenAI model used for generation.", json_schema_extra={"example": "gpt-4o-mini"})
