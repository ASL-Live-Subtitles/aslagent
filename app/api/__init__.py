from fastapi import APIRouter

from .composer import router as compose_router
from .expression_rules import router as expression_rule_router
from .translation_sessions import router as translation_session_router

api_router = APIRouter()
api_router.include_router(compose_router)
api_router.include_router(expression_rule_router)
api_router.include_router(translation_session_router)

__all__ = ["api_router"]
