from __future__ import annotations

from src.config import settings
from src.schemas.models import StockAlert


class StockAlertAgent:
    """Evaluates stock and price-change triggers using supplied item data."""

    def evaluate(self, item_id: str, item_title: str, available_quantity: int | None = None,
                 price_change_percent: float | None = None) -> StockAlert:
        if available_quantity is not None and available_quantity <= 0:
            return StockAlert(item_id=item_id, item_title=item_title, alert_type="out_of_stock",
                              severity="high", message="El artículo figura sin stock.", threshold_value=0)
        if available_quantity is not None and available_quantity <= settings.low_stock_threshold:
            return StockAlert(item_id=item_id, item_title=item_title, alert_type="stock_low",
                              severity="high", message="El stock está en el umbral bajo configurado.",
                              threshold_value=float(settings.low_stock_threshold))
        if price_change_percent is not None and price_change_percent <= -10:
            return StockAlert(item_id=item_id, item_title=item_title, alert_type="price_drop",
                              severity="medium", message="El precio cayó al menos un 10% respecto del valor previo.",
                              threshold_value=10.0)
        if price_change_percent is not None and price_change_percent >= 10:
            return StockAlert(item_id=item_id, item_title=item_title, alert_type="price_increase",
                              severity="medium", message="El precio subió al menos un 10% respecto del valor previo.",
                              threshold_value=10.0)
        return StockAlert(item_id=item_id, item_title=item_title, alert_type="stock_low",
                          severity="low", message="No se detectó una alerta con los datos proporcionados.",
                          threshold_value=float(settings.low_stock_threshold))
