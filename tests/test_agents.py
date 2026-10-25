from src.agents.competitor_analyst import CompetitorAnalystAgent
from src.agents.pricing_optimizer import PricingOptimizerAgent
from src.agents.stock_alert import StockAlertAgent


def test_competitor_stats_are_computed_from_input():
    result = CompetitorAnalystAgent().analyze("fone", [
        {"price": 100}, {"price": 200}, {"price": 300}, {"title": "no price"}
    ])
    assert result.competitor_count == 3
    assert result.avg_price == 200
    assert result.min_price == 100
    assert result.max_price == 300
    assert result.market_median_price == 200


def test_competitor_stats_do_not_invent_prices_for_empty_results():
    result = CompetitorAnalystAgent().analyze("unknown", [])
    assert result.competitor_count == 0
    assert result.avg_price is None
    assert "No hay suficientes" in result.summary


def test_pricing_requires_real_price_and_market_data():
    agent = PricingOptimizerAgent()
    try:
        agent.recommend("MLA1", None, [{"price": 100}])
        assert False, "must reject missing current price"
    except ValueError as exc:
        assert "current_price" in str(exc)
    try:
        agent.recommend("MLA1", 120, [])
        assert False, "must reject empty market"
    except ValueError as exc:
        assert "competitor prices" in str(exc)


def test_pricing_uses_market_median_and_margin_floor():
    result = PricingOptimizerAgent().recommend(
        "MLA1", 120, [{"price": 100}, {"price": 150}, {"price": 200}],
        target_margin=0.2, cost=160
    )
    assert result.recommended_price == 200
    assert result.confidence <= 1


def test_stock_alert_thresholds():
    agent = StockAlertAgent()
    assert agent.evaluate("MLA1", "x", available_quantity=0).alert_type == "out_of_stock"
    assert agent.evaluate("MLA1", "x", available_quantity=3).severity == "high"
    assert agent.evaluate("MLA1", "x", price_change_percent=-12).alert_type == "price_drop"
