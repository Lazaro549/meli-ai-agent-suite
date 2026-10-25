from __future__ import annotations

import logging
from typing import Any

from src.config import settings
from src.schemas.models import CompetitorAnalysis
from src.tools.bedrock_tools import BedrockClient

logger = logging.getLogger(__name__)


class CompetitorAnalystAgent:
    """Assesses competitor pricing, market standing, and reputation signals."""

    def __init__(self, bedrock_client: BedrockClient | None = None) -> None:
        self.bedrock_client = bedrock_client or BedrockClient()

    def analyze(self, query: str, limit: int = 10) -> CompetitorAnalysis:
        logger.info("Analyzing competitor landscape for query=%s", query)

        prompt = f"""
        You are a senior e-commerce strategist focused on Mercado Libre.
        Analyze the competitive landscape for: "{query}".

        Return a brief JSON object with the following keys:
        - competitor_count: integer
        - avg_price: number
        - min_price: number
        - max_price: number
        - market_median_price: number
        - avg_reputation: number
        - opportunities: array of short strings
        - summary: short string
        """

        raw_response = self.bedrock_client.generate_json(prompt)

        opportunities = raw_response.get("opportunities", [])
        if not isinstance(opportunities, list):
            opportunities = ["Review price positioning", "Improve product presentation"]

        return CompetitorAnalysis(
            query=query,
            competitor_count=int(raw_response.get("competitor_count", 0)),
            avg_price=float(raw_response.get("avg_price", 0.0) or 0.0),
            min_price=float(raw_response.get("min_price", 0.0) or 0.0),
            max_price=float(raw_response.get("max_price", 0.0) or 0.0),
            market_median_price=float(raw_response.get("market_median_price", 0.0) or 0.0),
            avg_reputation=float(raw_response.get("avg_reputation", 0.0) or 0.0),
            opportunities=opportunities,
            summary=str(raw_response.get("summary", "Competitive analysis completed.")),
        )
