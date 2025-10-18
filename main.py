from __future__ import annotations

import os
from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from fastapi import FastAPI, HTTPException, Query, Path

# Import models
from models.emotion_analysis import (
    EmotionAnalysisCreate,
    EmotionAnalysisRead,
    EmotionAnalysisUpdate,
)
from models.agent_session import (
    AgentSessionCreate,
    AgentSessionRead,
    AgentSessionUpdate,
)

port = int(os.environ.get("FASTAPI_PORT", 8000))
app = FastAPI(
    title="ASL Emotion Agent API",
    version="1.0.0",
    description=(
        "Microservice for mapping ASL model outputs (emotion, intent) into expressive "
        "metadata such as punctuation and TTS tone adjustments."
    ),
    license_info={
        "name": "Apache 2.0",
        "url": "http://www.apache.org/licenses/LICENSE-2.0.html",
    },
    openapi_tags=[
        {
            "name": "EmotionAnalysis",
            "description": "Operations for managing emotion-intent mapping rules",
        },
        {
            "name": "AgentSession",
            "description": "Operations for processing ASL model outputs and generating expressive metadata",
        },
    ],
    servers=[
        {
            "url": "https://virtserver.swaggerhub.com/personalcx/ASLAgent/1.0.0",
            "description": "SwaggerHub API Auto Mocking Server",
        }
    ],
)

# In-memory database simulation
emotion_analyses: Dict[UUID, EmotionAnalysisRead] = {}
agent_sessions: Dict[UUID, AgentSessionRead] = {}

# EmotionAnalysis Endpoints
@app.post(
    "/emotion_analyses",
    response_model=EmotionAnalysisRead,
    status_code=201,
    tags=["EmotionAnalysis"],
)
def create_emotion_analysis(analysis: EmotionAnalysisCreate):
    """Create a new EmotionAnalysis rule."""
    new_analysis = EmotionAnalysisRead(**analysis.model_dump())
    emotion_analyses[new_analysis.id] = new_analysis
    return new_analysis


@app.get(
    "/emotion_analyses",
    response_model=List[EmotionAnalysisRead],
    tags=["EmotionAnalysis"],
)
def list_emotion_analyses(
    emotion: Optional[str] = Query(None, description="Filter by emotion"),
    intent: Optional[str] = Query(None, description="Filter by intent"),
):
    """List all EmotionAnalysis rules with optional filters."""
    results = list(emotion_analyses.values())
    if emotion:
        results = [a for a in results if a.emotion == emotion]
    if intent:
        results = [a for a in results if a.intent == intent]
    return results


@app.get(
    "/emotion_analyses/{analysis_id}",
    response_model=EmotionAnalysisRead,
    tags=["EmotionAnalysis"],
)
def get_emotion_analysis(analysis_id: UUID = Path(..., description="ID of the analysis to retrieve")):
    """Get a specific EmotionAnalysis rule by ID."""
    analysis = emotion_analyses.get(analysis_id)
    if not analysis:
        raise HTTPException(status_code=404, detail="EmotionAnalysis not found")
    return analysis


@app.put(
    "/emotion_analyses/{analysis_id}",
    response_model=EmotionAnalysisRead,
    tags=["EmotionAnalysis"],
)
def update_emotion_analysis(analysis_id: UUID, update: EmotionAnalysisUpdate):
    """Update an existing EmotionAnalysis rule."""
    existing = emotion_analyses.get(analysis_id)
    if not existing:
        raise HTTPException(status_code=404, detail="EmotionAnalysis not found")
    updated = existing.model_copy(update=update.model_dump(exclude_unset=True))
    updated.updated_at = datetime.utcnow()
    emotion_analyses[analysis_id] = updated
    return updated


@app.delete(
    "/emotion_analyses/{analysis_id}",
    status_code=200,
    tags=["EmotionAnalysis"],
)
def delete_emotion_analysis(analysis_id: UUID):
    """Delete a specific EmotionAnalysis rule."""
    analysis = emotion_analyses.pop(analysis_id, None)
    if analysis is None:
        raise HTTPException(status_code=404, detail="EmotionAnalysis not found")
    return {
        "message": f"EmotionAnalysis ({analysis.emotion}, {analysis.intent}) deleted successfully."
    }

# AgentSession Endpoints
@app.post(
    "/agent_sessions",
    response_model=AgentSessionRead,
    status_code=201,
    tags=["AgentSession"],
)
def create_agent_session(session: AgentSessionCreate):
    """Create a new AgentSession record."""
    new_session = AgentSessionRead(**session.model_dump())
    agent_sessions[new_session.id] = new_session
    return new_session


@app.get(
    "/agent_sessions",
    response_model=List[AgentSessionRead],
    tags=["AgentSession"],
)
def list_agent_sessions(
    detected_emotion: Optional[str] = Query(None, description="Filter by detected emotion"),
    detected_intent: Optional[str] = Query(None, description="Filter by detected intent"),
):
    """List all AgentSession records with optional filters."""
    results = list(agent_sessions.values())
    if detected_emotion:
        results = [s for s in results if s.detected_emotion == detected_emotion]
    if detected_intent:
        results = [s for s in results if s.detected_intent == detected_intent]
    return results


@app.get(
    "/agent_sessions/{session_id}",
    response_model=AgentSessionRead,
    tags=["AgentSession"],
)
def get_agent_session(session_id: UUID):
    """Retrieve a specific AgentSession record by ID."""
    session = agent_sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="AgentSession not found")
    return session


@app.put(
    "/agent_sessions/{session_id}",
    response_model=AgentSessionRead,
    tags=["AgentSession"],
)
def update_agent_session(session_id: UUID, session_update: AgentSessionUpdate):
    """Update an existing AgentSession record."""
    existing_session = agent_sessions.get(session_id)
    if not existing_session:
        raise HTTPException(status_code=404, detail="AgentSession not found")
    updated_session = existing_session.model_copy(update=session_update.model_dump(exclude_unset=True))
    updated_session.updated_at = datetime.utcnow()
    agent_sessions[session_id] = updated_session
    return updated_session


@app.delete(
    "/agent_sessions/{session_id}",
    status_code=200,
    tags=["AgentSession"],
)
def delete_agent_session(session_id: UUID):
    """Delete a specific AgentSession record."""
    session = agent_sessions.pop(session_id, None)
    if session is None:
        raise HTTPException(status_code=404, detail="AgentSession not found")
    return {
        "message": f"AgentSession for input '{session.input_text}' has been deleted."
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
