from __future__ import annotations

import json
import logging
from typing import Any

import boto3

from src.config import settings

logger = logging.getLogger(__name__)


class BedrockClient:
    """Lightweight Bedrock runtime wrapper for structured generation and text completion."""

    def __init__(self, model_id: str | None = None) -> None:
        self.model_id = model_id or settings.bedrock_model_id
        self.client = boto3.client(
            "bedrock-runtime",
            region_name=settings.aws_region,
            aws_access_key_id=settings.aws_access_key_id or None,
            aws_secret_access_key=settings.aws_secret_access_key or None,
            aws_session_token=settings.aws_session_token or None,
        )

    def generate_text(self, prompt: str, **kwargs: Any) -> str:
        params = {
            "modelId": self.model_id,
            "contentType": "application/json",
            "accept": "application/json",
            "body": json.dumps(
                {
                    "anthropic_version": "bedrock-2023-05-31",
                    "max_tokens": kwargs.get("max_tokens", settings.max_tokens),
                    "temperature": kwargs.get("temperature", settings.temperature),
                    "messages": [{"role": "user", "content": prompt}],
                }
            ),
        }

        response = self.client.invoke_model(**params)
        payload = json.loads(response["body"].read())
        return payload["content"][0]["text"]

    def generate_json(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        text = self.generate_text(prompt, **kwargs)

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            logger.warning("Bedrock response was not valid JSON. Falling back to parsed text extraction.")
            return {"summary": text}

    def converse(self, messages: list[dict[str, str]], **kwargs: Any) -> str:
        response = self.client.converse(
            modelId=self.model_id,
            messages=messages,
            inferenceConfig={
                "maxTokens": kwargs.get("max_tokens", settings.max_tokens),
                "temperature": kwargs.get("temperature", settings.temperature),
            },
        )
        return response["output"]["message"]["content"][0]["text"]
