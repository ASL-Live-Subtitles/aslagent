"""SQL helpers for bootstrapping the ASL Agent MySQL schema."""

DEFAULT_DB_NAME = "asl_agent"
DEFAULT_DB_USER = "asl_agent"
DEFAULT_DB_PASSWORD = "changeme"

EXPRESSION_RULES_TABLE_NAME = "expression_rules"
TRANSLATION_SESSIONS_TABLE_NAME = "translation_sessions"

EXPRESSION_RULES_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {EXPRESSION_RULES_TABLE_NAME} (
    id CHAR(36) PRIMARY KEY,
    emotion VARCHAR(50) NOT NULL,
    intent VARCHAR(50) NOT NULL,
    punctuation_adjustment TEXT NOT NULL,
    tts_tone VARCHAR(50) NOT NULL,
    confidence_threshold FLOAT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_emotion_intent (emotion, intent)
);
"""

TRANSLATION_SESSIONS_TABLE_SQL = f"""
CREATE TABLE IF NOT EXISTS {TRANSLATION_SESSIONS_TABLE_NAME} (
    id CHAR(36) PRIMARY KEY,
    user_id VARCHAR(64) NULL,
    glosses JSON NOT NULL,
    letters JSON NULL,
    preferred_words JSON NOT NULL,
    context TEXT NULL,
    input_text TEXT NOT NULL,
    compose_confidence FLOAT NOT NULL,
    compose_alternatives JSON NOT NULL,
    detected_emotion VARCHAR(50) NOT NULL,
    detected_intent VARCHAR(50) NOT NULL,
    emphasis JSON NOT NULL,
    adjusted_text TEXT NOT NULL,
    tts_metadata JSON NOT NULL,
    tool_metadata JSON NOT NULL,
    summary_text TEXT NULL,
    summary_topics JSON NOT NULL,
    summary_action_items JSON NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_sessions_emotion (detected_emotion),
    INDEX idx_sessions_intent (detected_intent),
    INDEX idx_sessions_user (user_id)
);
"""

EXPRESSION_RULES_SEED_SQL = f"""
INSERT INTO {EXPRESSION_RULES_TABLE_NAME} (id, emotion, intent, punctuation_adjustment, tts_tone, confidence_threshold)
VALUES
    ('11111111-1111-1111-1111-111111111111', 'happy', 'statement', 'add exclamation mark', 'bright', 0.9),
    ('22222222-2222-2222-2222-222222222222', 'frustrated', 'question', 'add question mark', 'concerned', 0.85)
ON DUPLICATE KEY UPDATE
    emotion = VALUES(emotion),
    intent = VALUES(intent),
    punctuation_adjustment = VALUES(punctuation_adjustment),
    tts_tone = VALUES(tts_tone),
    confidence_threshold = VALUES(confidence_threshold);
"""

TRANSLATION_SESSIONS_SEED_SQL = f"""
INSERT INTO {TRANSLATION_SESSIONS_TABLE_NAME} (id, user_id, glosses, letters, preferred_words, context, input_text, compose_confidence, compose_alternatives, detected_emotion, detected_intent, emphasis, adjusted_text, tts_metadata, tool_metadata, summary_text, summary_topics, summary_action_items)
VALUES
    (
        '33333333-3333-3333-3333-333333333333',
        'user_123',
        '["IX-1","GOOD","IDEA"]',
        '["A","I"]',
        '{{"GOOD":"fantastic"}}',
        'Brainstorming product ideas',
        'That''s a good idea',
        0.9,
        '["Good idea."]',
        'positive',
        'statement',
        '["good"]',
        'That''s a good idea!',
        '{{"voice":"en-female-1","tone":"bright","audio_url":"https://example.com/audio.wav","visemes":["AA","B"]}}',
        '{{"compose_version":"2024-09-25","tts_version":"v2"}}',
        'Discussed next sprint scope and agreed on deliverables.',
        '["planning","next steps"]',
        '["Send sprint summary","Update roadmap"]'
    )
ON DUPLICATE KEY UPDATE
    preferred_words = VALUES(preferred_words),
    compose_confidence = VALUES(compose_confidence),
    tts_metadata = VALUES(tts_metadata);
"""
