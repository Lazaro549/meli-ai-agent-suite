from __future__ import annotations

import json
import logging
from typing import Any

from src.schemas.models import ListingSuggestion
from src.tools.bedrock_tools import BedrockClient

logger = logging.getLogger(__name__)


class ContentGeneratorAgent:
    """Generates SEO-optimized titles and descriptions for Mercado Libre listings."""

    def __init__(self, bedrock_client: BedrockClient | None = None) -> None:
        self.bedrock_client = bedrock_client or BedrockClient()

    def generate(self, title: str, keywords: list[str] | None = None) -> ListingSuggestion:
        logger.info("Generating listing content for title=%s", title)

        keyword_text = ", ".join(keywords or ["premium", "calidad", "valor", "material"])
        prompt = f"""
        You are an SEO copywriter for Mercado Libre listings.

        Create a listing for this product title: "{title}".
        Embed related keywords naturally: {keyword_text}.

        Return JSON with:
        - title: string
        - description: string
        - bullet_points: array of 3 concise strings
        - keywords: array of 5 short strings
        - seo_score: number between 0 and 1
        """

        raw_response = self.bedrock_client.generate_json(prompt)

        return ListingSuggestion(
            title=str(raw_response.get("title") or title),
            description=str(raw_response.get("description") or "High-quality product for conversion-focused marketplaces."),
            bullet_points=list(raw_response.get("bullet_points") or ["High-quality material", "Built for daily use", "Optimized for conversion"]),
            keywords=list(raw_response.get("keywords") or keyword_text.split(", ")),
            seo_score=float(raw_response.get("seo_score", 0.9) or 0.9),
        )
