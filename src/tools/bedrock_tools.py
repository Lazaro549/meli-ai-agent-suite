from __future__ import annotations

import json
import logging
from typing import Any

import boto3
from botocore.exceptions import BotoCoreError, ClientError

from src.config import settings

logger = logging.getLogger(__name__)


class BedrockGenerationError(RuntimeError):
    """Raised when Bedrock cannot return a usable completion."""


class BedrockClient:
    """Amazon Bedrock Runtime client using the Converse API."""

    def __init__(self, model_id: str | None = None, client: Any | None = None) -> None:
        self.model_id = model_id or settings.bedrock_model_id
        self.client = client or boto3.client("bedrock-runtime", region_name=settings.aws_region)

    def generate_text(self, prompt: str, **kwargs: Any) -> str:
        if not prompt.strip():
            raise ValueError("prompt cannot be empty")
        try:
            response = self.client.converse(
                modelId=self.model_id,
                messages=[{"role": "user", "content": [{"text": prompt}]}],
                inferenceConfig={"maxTokens": int(kwargs.get("max_tokens", settings.max_tokens)),
                                 "temperature": float(kwargs.get("temperature", settings.temperature))},
            )
            content = response["output"]["message"]["content"]
            text = next((part["text"] for part in content if isinstance(part, dict) and "text" in part), None)
            if not isinstance(text, str) or not text.strip():
                raise BedrockGenerationError("Bedrock returned an empty response.")
            return text.strip()
        except (BotoCoreError, ClientError, KeyError, IndexError, TypeError) as exc:
            logger.exception("Bedrock generation failed")
            raise BedrockGenerationError(f"Bedrock generation failed: {exc}") from exc

    def generate_json(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        text = self.generate_text(prompt, **kwargs)
        candidate = text.strip()
        if candidate.startswith("```"):
            candidate = candidate.split("\n", 1)[-1]
            if candidate.endswith("```"):
                candidate = candidate[:-3].strip()
        try:
            result = json.loads(candidate)
        except json.JSONDecodeError as exc:
            raise BedrockGenerationError("Bedrock did not return valid JSON.") from exc
        if not isinstance(result, dict):
            raise BedrockGenerationError("Bedrock JSON response must be an object.")
        return result
