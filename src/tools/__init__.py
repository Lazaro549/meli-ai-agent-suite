from __future__ import annotations

import logging

from src.schemas.models import StockAlert

logger = logging.getLogger(__name__)


class StockAlertAgent:
    """Evaluates stock risk and price-change triggers for monitored products."""

    def evaluate(
        self,
        item_id: str,
        item_title: str,
        available_quantity: int | None = None,
        price_change_percent: float | None = None,
    ) -> StockAlert:
        logger.info("Evaluating stock and price conditions for item_id=%s", item_id)

        if available_quantity is not None and available_quantity <= 5:
            return StockAlert(
                item_id=item_id,
                item_title=item_title,
                alert_type="stock_low",
                severity="high",
                message="Inventory is critically low and should be replenished soon.",
                threshold_value=5.0,
            )

        if price_change_percent is not None and price_change_percent <= -10:
            return StockAlert(
                item_id=item_id,
                item_title=item_title,
                alert_type="price_drop",
                severity="medium",
                message="The item price dropped materially relative to the previous value.",
                threshold_value=10.0,
            )

        return StockAlert(
            item_id=item_id,
            item_title=item_title,
            alert_type="stock_low",
            severity="low",
            message="No immediate stock alert triggered; continue monitoring.",
            threshold_value=10.0,
        )
