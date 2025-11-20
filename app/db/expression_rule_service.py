from typing import List, Optional
from uuid import UUID
from mysql.connector import Error
from datetime import datetime

from app.models.expression_rule import (
    ExpressionRuleCreate,
    ExpressionRuleRead,
    ExpressionRuleUpdate,
)
from .base import MySQLService


class ExpressionRuleMySQLService(MySQLService):
    """CRUD operations for the expression_rules table."""

    def _row_to_model(self, row) -> ExpressionRuleRead:
        if "confidence_threshold" in row and row["confidence_threshold"] is not None:
            row["confidence_threshold"] = float(row["confidence_threshold"])
        return ExpressionRuleRead(**row)

    def list(self, emotion: Optional[str] = None, intent: Optional[str] = None) -> List[ExpressionRuleRead]:
        query = "SELECT * FROM expression_rules"
        clauses = []
        params = []

        if emotion:
            clauses.append("emotion = %s")
            params.append(emotion)
        if intent:
            clauses.append("intent = %s")
            params.append(intent)

        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " ORDER BY updated_at DESC"

        cursor = self.cursor()
        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [self._row_to_model(row) for row in rows]
        finally:
            cursor.close()

    def get(self, rule_id: UUID) -> Optional[ExpressionRuleRead]:
        cursor = self.cursor()
        try:
            cursor.execute("SELECT * FROM expression_rules WHERE id = %s", (str(rule_id),))
            row = cursor.fetchone()
            return self._row_to_model(row) if row else None
        finally:
            cursor.close()

    def create(self, payload: ExpressionRuleCreate) -> ExpressionRuleRead:
        now = datetime.utcnow()
        record = ExpressionRuleRead(**payload.model_dump(), created_at=now, updated_at=now)

        cursor = self.cursor()
        try:
            cursor.execute(
                "INSERT INTO expression_rules (id, emotion, intent, punctuation_adjustment, tts_tone, confidence_threshold, created_at, updated_at) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    str(record.id),
                    record.emotion,
                    record.intent,
                    record.punctuation_adjustment,
                    record.tts_tone,
                    record.confidence_threshold,
                    record.created_at,
                    record.updated_at,
                ),
            )
            self.connection.commit()
            return record
        except Error as exc:
            self.connection.rollback()
            raise RuntimeError(f"Failed to create expression rule: {exc}") from exc
        finally:
            cursor.close()

    def update(self, rule_id: UUID, payload: ExpressionRuleUpdate) -> Optional[ExpressionRuleRead]:
        data = payload.model_dump(exclude_unset=True)
        if not data:
            return self.get(rule_id)

        data["updated_at"] = datetime.utcnow()

        set_clause = ", ".join(f"{column} = %s" for column in data.keys())
        values = list(data.values()) + [str(rule_id)]

        cursor = self.cursor()
        try:
            cursor.execute(
                f"UPDATE expression_rules SET {set_clause} WHERE id = %s",
                values,
            )
            self.connection.commit()
        except Error as exc:
            self.connection.rollback()
            raise RuntimeError(f"Failed to update expression rule: {exc}") from exc
        finally:
            cursor.close()

        return self.get(rule_id)

    def delete(self, rule_id: UUID) -> bool:
        cursor = self.cursor()
        try:
            cursor.execute("DELETE FROM expression_rules WHERE id = %s", (str(rule_id),))
            deleted = cursor.rowcount > 0
            self.connection.commit()
            return deleted
        except Error as exc:
            self.connection.rollback()
            raise RuntimeError(f"Failed to delete expression rule: {exc}") from exc
        finally:
            cursor.close()
