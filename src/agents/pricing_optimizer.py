from __future__ import annotations

from statistics import median
from typing import Any

from src.schemas.models import PriceRecommendation


class PricingOptimizerAgent:
    """Creates transparent price suggestions from observed competitor prices."""

    def recommend(self, item_id: str, current_price: float | None,
                  competitor_products: list[dict[str, Any]], target_margin: float | None = None,
                  cost: float | None = None) -> PriceRecommendation:
        if current_price is None or current_price <= 0:
            raise ValueError("A verified current_price is required; no default price is assumed.")
        if target_margin is not None and not 0 <= target_margin < 1:
            raise ValueError("target_margin must be >= 0 and < 1")
        if cost is not None and cost < 0:
            raise ValueError("cost cannot be negative")
        prices = sorted(float(p["price"]) for p in competitor_products
                        if isinstance(p.get("price"), (int, float)) and p["price"] > 0)
        if not prices:
            raise ValueError("No valid competitor prices; cannot make a market-based recommendation.")
        market_median = float(median(prices))
        suggested = market_median
        if cost is not None and target_margin is not None:
            suggested = max(suggested, cost / (1 - target_margin))
        suggested = round(suggested, 2)
        rationale = (f"Basado en {len(prices)} precios observados: mediana {market_median:.2f}, "
                     f"mínimo {min(prices):.2f}, máximo {max(prices):.2f}. No incluye comisiones "
                     "ni envío salvo que estén incorporados en el costo suministrado.")
        return PriceRecommendation(
            item_id=item_id, current_price=current_price, recommended_price=suggested,
            suggested_range_min=round(min(suggested, market_median), 2),
            suggested_range_max=round(max(suggested, market_median), 2),
            rationale=rationale, confidence=min(0.9, 0.45 + 0.05 * len(prices)),
        )
