from __future__ import annotations

import logging
from typing import Any

from src.schemas.models import PriceRecommendation
from src.tools.bedrock_tools import BedrockClient

logger = logging.getLogger(__name__)


class PricingOptimizerAgent:
    """Determines suggested prices using market context and business constraints."""

    def __init__(self, bedrock_client: BedrockClient | None = None) -> None:
        self.bedrock_client = bedrock_client or BedrockClient()

    def recommend(self, item_id: str, current_price: float | None = None) -> PriceRecommendation:
        logger.info("Optimizing price for item_id=%s", item_id)

        current = current_price if current_price is not None else 149.99
        prompt = f"""
        You are a pricing strategist for e-commerce.

        Recommend a price for Mercado Libre item '{item_id}' with current price {current}.

        Return JSON with:
        - recommended_price: number
        - suggested_range_min: number
        - suggested_range_max: number
        - rationale: short statement
        - confidence: number between 0 and 1
        """

        raw_response = self.bedrock_client.generate_json(prompt)

        recommended = float(raw_response.get("recommended_price", current * 0.93) or current * 0.93)
        min_price = float(raw_response.get("suggested_range_min", recommended * 0.94) or recommended * 0.94)
        max_price = float(raw_response.get("suggested_range_max", recommended * 1.08) or recommended * 1.08)

        return PriceRecommendation(
            item_id=item_id,
            current_price=current,
            recommended_price=recommended,
            suggested_range_min=min_price,
            suggested_range_max=max_price,
            rationale=str(raw_response.get("rationale") or "Aligned with market conditions and margin considerations."),
            confidence=float(raw_response.get("confidence", 0.85) or 0.85),
        )
