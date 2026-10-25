from __future__ import annotations

from statistics import median
from typing import Any

from src.schemas.models import CompetitorAnalysis


class CompetitorAnalystAgent:
    """Computes market statistics from actual Mercado Libre search results."""

    def analyze(self, query: str, products: list[dict[str, Any]], limit: int = 10) -> CompetitorAnalysis:
        if not query.strip():
            raise ValueError("query cannot be empty")
        valid = [p for p in products if isinstance(p.get("price"), (int, float)) and p["price"] > 0]
        prices = [float(p["price"]) for p in valid]
        reputations = [
            float(seller["seller_reputation"]["transactions"]["ratings"]["positive"])
            for seller in []  # Search results usually don't include seller reputation.
        ]
        if prices:
            avg = sum(prices) / len(prices)
            low, high, mid = min(prices), max(prices), float(median(prices))
            spread = (high - low) / mid if mid else 0
            opportunities = []
            if spread >= 0.25:
                opportunities.append("El mercado presenta una dispersión de precios relevante; comparar atributos y costos antes de posicionarse.")
            opportunities.append("Contrastar calidad, envío, reputación y comisiones antes de competir solo por precio.")
            opportunities.append("Revisar títulos y atributos de las publicaciones con precios comparables.")
            summary = f"Estadísticas calculadas a partir de {len(prices)} publicaciones con precio válido."
        else:
            avg = low = high = mid = None
            opportunities = ["No hay suficientes publicaciones con precio válido para calcular estadísticas."]
            summary = "La búsqueda no devolvió datos de precio suficientes; no se generaron estimaciones."
        return CompetitorAnalysis(
            query=query, competitor_count=len(valid), avg_price=avg, min_price=low,
            max_price=high, market_median_price=mid, avg_reputation=None,
            opportunities=opportunities, summary=summary,
        )
