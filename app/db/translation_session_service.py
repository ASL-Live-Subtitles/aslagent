from __future__ import annotations

import json
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from mysql.connector import Error

from app.models.translation_session import (
    TranslationSessionCreate,
    TranslationSessionRead,
    TranslationSessionUpdate,
)
from .base import MySQLService


class TranslationSessionMySQLService(MySQLService):
    """CRUD operations for the translation_sessions table."""

    JSON_DEFAULT_FACTORIES = {
        "glosses": list,
        "letters": lambda: None,
        "preferred_words": dict,
        "compose_alternatives": list,
        "emphasis": list,
        "tts_metadata": dict,
        "tool_metadata": dict,
        "summary_topics": list,
        "summary_action_items": list,
    }

    def _deserialize_json_column(self, row, column):
        value = row.get(column)
        if isinstance(value, str) and value:
            row[column] = json.loads(value)
        elif column in self.JSON_DEFAULT_FACTORIES and value is None:
            factory = self.JSON_DEFAULT_FACTORIES[column]
            row[column] = factory()

    def _row_to_model(self, row) -> TranslationSessionRead:
        for column in self.JSON_DEFAULT_FACTORIES.keys():
            self._deserialize_json_column(row, column)
        return TranslationSessionRead(**row)

    def list(
        self,
        detected_emotion: Optional[str] = None,
        detected_intent: Optional[str] = None,
    ) -> List[TranslationSessionRead]:
        query = "SELECT * FROM translation_sessions"
        clauses = []
        params = []

        if detected_emotion:
            clauses.append("detected_emotion = %s")
            params.append(detected_emotion)
        if detected_intent:
            clauses.append("detected_intent = %s")
            params.append(detected_intent)

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

    def get(self, session_id: UUID) -> Optional[TranslationSessionRead]:
        cursor = self.cursor()
        try:
            cursor.execute("SELECT * FROM translation_sessions WHERE id = %s", (str(session_id),))
            row = cursor.fetchone()
            return self._row_to_model(row) if row else None
        finally:
            cursor.close()

    def create(self, payload: TranslationSessionCreate) -> TranslationSessionRead:
        now = datetime.utcnow()
        record = TranslationSessionRead(**payload.model_dump(), created_at=now, updated_at=now)

        cursor = self.cursor()
        try:
            cursor.execute(
                "INSERT INTO translation_sessions (id, user_id, glosses, letters, preferred_words, context, input_text, compose_confidence, compose_alternatives, detected_emotion, detected_intent, emphasis, adjusted_text, tts_metadata, tool_metadata, summary_text, summary_topics, summary_action_items, created_at, updated_at) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    str(record.id),
                    record.user_id,
                    json.dumps(record.glosses),
                    json.dumps(record.letters) if record.letters is not None else None,
                    json.dumps(record.preferred_words),
                    record.context,
                    record.input_text,
                    record.compose_confidence,
                    json.dumps(record.compose_alternatives),
                    record.detected_emotion,
                    record.detected_intent,
                    json.dumps(record.emphasis),
                    record.adjusted_text,
                    json.dumps(record.tts_metadata),
                    json.dumps(record.tool_metadata),
                    record.summary_text,
                    json.dumps(record.summary_topics),
                    json.dumps(record.summary_action_items),
                    record.created_at,
                    record.updated_at,
                ),
            )
            self.connection.commit()
            return record
        except Error as exc:
            self.connection.rollback()
            raise RuntimeError(f"Failed to create translation session: {exc}") from exc
        finally:
            cursor.close()

    def update(self, session_id: UUID, payload: TranslationSessionUpdate) -> Optional[TranslationSessionRead]:
        data = payload.model_dump(exclude_unset=True)
        if not data:
            return self.get(session_id)

        json_fields = {
            "glosses",
            "letters",
            "preferred_words",
            "compose_alternatives",
            "emphasis",
            "tts_metadata",
            "tool_metadata",
            "summary_topics",
            "summary_action_items",
        }
        for column in list(data.keys()):
            if column in json_fields and data[column] is not None:
                data[column] = json.dumps(data[column])
        data["updated_at"] = datetime.utcnow()

        set_clause = ", ".join(f"{column} = %s" for column in data.keys())
        values = list(data.values()) + [str(session_id)]

        cursor = self.cursor()
        try:
            cursor.execute(
                f"UPDATE translation_sessions SET {set_clause} WHERE id = %s",
                values,
            )
            self.connection.commit()
        except Error as exc:
            self.connection.rollback()
            raise RuntimeError(f"Failed to update translation session: {exc}") from exc
        finally:
            cursor.close()

        return self.get(session_id)

    def delete(self, session_id: UUID) -> bool:
        cursor = self.cursor()
        try:
            cursor.execute("DELETE FROM translation_sessions WHERE id = %s", (str(session_id),))
            deleted = cursor.rowcount > 0
            self.connection.commit()
            return deleted
        except Error as exc:
            self.connection.rollback()
            raise RuntimeError(f"Failed to delete translation session: {exc}") from exc
        finally:
            cursor.close()
