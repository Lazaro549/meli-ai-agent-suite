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
                                 "temperature": float(kwargs.get("temperature", settings.temperature))})
            content = response["output"]["message"]["content"]
            result = next((p["text"] for p in content if isinstance(p, dict) and "text" in p), None)
            if not isinstance(result, str) or not result.strip():
                raise BedrockGenerationError("Bedrock returned an empty response.")
            return result.strip()
        except (BotoCoreError, ClientError, KeyError, IndexError, TypeError) as exc:
            logger.exception("Bedrock generation failed")
            raise BedrockGenerationError(f"Bedrock generation failed: {exc}") from exc

    def generate_json(self, prompt: str, **kwargs: Any) -> dict[str, Any]:
        text = self.generate_text(prompt, **kwargs).strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[-1]
            if text.endswith("```"):
                text = text[:-3].strip()
        try:
            data = json.loads(text)
        except json.JSONDecodeError as exc:
            raise BedrockGenerationError("Bedrock did not return valid JSON.") from exc
        if not isinstance(data, dict):
            raise BedrockGenerationError("Bedrock JSON response must be an object.")
        return data
