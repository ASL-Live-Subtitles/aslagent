"""Application configuration helpers."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv


# Load .env once when the module is imported (works locally; Cloud Run injects env vars).
load_dotenv(dotenv_path=Path(".env"), override=False)


class Settings:
    def __init__(self) -> None:
        self.fastapi_port: int = int(os.environ.get("FASTAPI_PORT", 8000))
        self.title: str = os.environ.get("FASTAPI_TITLE", "ASL Emotion Agent API")
        self.version: str = os.environ.get("FASTAPI_VERSION", "1.0.0")


@lru_cache
def get_settings() -> Settings:
    return Settings()
