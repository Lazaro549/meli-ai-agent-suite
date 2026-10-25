from __future__ import annotations
from typing import Any
from src.agents.competitor_analyst import CompetitorAnalystAgent
from src.agents.content_generator import ContentGeneratorAgent
from src.agents.pricing_optimizer import PricingOptimizerAgent
from src.agents.stock_alert import StockAlertAgent
from src.config import settings
from src.schemas.models import Product
from src.tools.bedrock_tools import BedrockClient
from src.tools.meli_client import MercadoLibreClient

class MeliWorkflow:
    """Application workflow with injectable clients for deterministic tests."""
    def __init__(self, meli_client: MercadoLibreClient | None = None,
                 bedrock_client: BedrockClient | None = None) -> None:
        self.meli = meli_client or MercadoLibreClient()
        self.bedrock = bedrock_client or BedrockClient()
        self.competitors = CompetitorAnalystAgent()
        self.content = ContentGeneratorAgent(self.bedrock)
        self.pricing = PricingOptimizerAgent()
        self.stock = StockAlertAgent()

    def analyze(self, query: str, limit: int = 10) -> dict[str, Any]:
        raw = self.meli.search_products(query, settings.meli_site_id, limit)
        result = self.competitors.analyze(query, raw, limit)
        return {"status": "success", "analysis": result.model_dump(mode="json")}

    def generate_listing(self, title: str, keywords: list[str] | None = None,
                         description: str | None = None) -> dict[str, Any]:
        result = self.content.generate(title, keywords, description)
        return {"status": "success", "listing": result.model_dump(mode="json")}

    def optimize_price(self, item_id: str, target_margin: float | None = None,
                       cost: float | None = None, limit: int = 10) -> dict[str, Any]:
        item = Product.model_validate(self.meli.get_item(item_id))
        competitors = self.meli.search_products(item.title, settings.meli_site_id, limit)
        result = self.pricing.recommend(item_id, item.price, competitors, target_margin, cost)
        return {"status": "success", "pricing": result.model_dump(mode="json"),
                "item": {"id": item.id, "title": item.title, "currency_id": item.currency_id}}

    def evaluate_stock(self, item_id: str) -> dict[str, Any]:
        item = Product.model_validate(self.meli.get_item(item_id))
        result = self.stock.evaluate(item.id, item.title, item.available_quantity)
        return {"status": "success", "stock_alert": result.model_dump(mode="json")}

    def close(self) -> None:
        self.meli.close()

def build_workflow() -> MeliWorkflow:
    return MeliWorkflow()

meli_workflow = build_workflow()
