from __future__ import annotations

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, HTTPException, Path, Query

from app.db import ExpressionRuleMySQLService
from app.models.expression_rule import (
    ExpressionRuleCreate,
    ExpressionRuleRead,
    ExpressionRuleUpdate,
)

router = APIRouter(prefix="/expression_rules", tags=["ExpressionRule"])


def _service() -> ExpressionRuleMySQLService:
    return ExpressionRuleMySQLService()


@router.post("", response_model=ExpressionRuleRead, status_code=201)
def create_expression_rule(rule: ExpressionRuleCreate):
    service = _service()
    try:
        return service.create(rule)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}") from exc
    finally:
        service.close_connection()


@router.get("", response_model=List[ExpressionRuleRead])
def list_expression_rules(
    emotion: Optional[str] = Query(None, description="Filter by emotion"),
    intent: Optional[str] = Query(None, description="Filter by intent"),
):
    service = _service()
    try:
        return service.list(emotion=emotion, intent=intent)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}") from exc
    finally:
        service.close_connection()


@router.get("/{rule_id}", response_model=ExpressionRuleRead)
def get_expression_rule(rule_id: UUID = Path(..., description="ID of the rule to retrieve")):
    service = _service()
    try:
        record = service.get(rule_id)
        if not record:
            raise HTTPException(status_code=404, detail="ExpressionRule not found")
        return record
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}") from exc
    finally:
        service.close_connection()


@router.put("/{rule_id}", response_model=ExpressionRuleRead)
def update_expression_rule(rule_id: UUID, update: ExpressionRuleUpdate):
    service = _service()
    try:
        updated = service.update(rule_id, update)
        if not updated:
            raise HTTPException(status_code=404, detail="ExpressionRule not found")
        return updated
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}") from exc
    finally:
        service.close_connection()


@router.delete("/{rule_id}", status_code=200)
def delete_expression_rule(rule_id: UUID):
    service = _service()
    try:
        deleted = service.delete(rule_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="ExpressionRule not found")
        return {"message": "ExpressionRule deleted successfully."}
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Database error: {exc}") from exc
    finally:
        service.close_connection()
