from __future__ import annotations

import logging
import os

import uvicorn
from fastapi import FastAPI

from app.api import api_router
from app.core.config import get_settings


logging.basicConfig(
    level=os.environ.get("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s | %(message)s",
)


settings = get_settings()

app = FastAPI(
    title=settings.title,
    version=settings.version,
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
            "name": "ExpressionRule",
            "description": "Operations for managing emotion-intent mapping rules",
        },
        {
            "name": "TranslationSession",
            "description": "Operations for processing ASL model outputs and generating expressive metadata",
        },
        {
            "name": "ComposeSentence",
            "description": "Compose fluent English sentences from ASL glosses using OpenAI",
        },
    ],
    # servers=[
    #     {
    #         "url": "https://virtserver.swaggerhub.com/personalcx/ASLAgent/1.0.0",
    #         "description": "SwaggerHub API Auto Mocking Server",
    #     }
    # ],
)

app.include_router(api_router)


@app.get("/")
def root():
    return {"message": "ASL Agent API is running. See /docs for details."}


def run() -> None:
    uvicorn.run("app.main:app", host="0.0.0.0", port=8080, reload=True)


if __name__ == "__main__":
    run()
