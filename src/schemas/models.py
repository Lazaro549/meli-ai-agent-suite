from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


class Product(BaseModel):
    """Represents a Mercado Libre product or item."""

    model_config = ConfigDict(populate_by_name=True)

    id: str
    title: str
    category_id: str | None = None
    price: float | None = None
    currency_id: str | None = None
    condition: str | None = None
    available_quantity: int | None = None
    sold_quantity: int | None = None
    permalink: str | None = None
    thumbnail: str | None = None
    listing_type_id: str | None = None
    buy_box_winner: bool | None = None
    status: str | None = None


class PricePoint(BaseModel):
    """A single price observation for one competitor or historical point."""

    date: datetime | None = None
    price: float | None = None
    currency_id: str | None = None


class CompetitorAnalysis(BaseModel):
    """Price, reputation, and positioning analysis of a product's competition."""

    query: str
    product_id: str | None = None
    competitor_count: int = 0
    avg_price: float | None = None
    min_price: float | None = None
    max_price: float | None = None
    market_median_price: float | None = None
    avg_reputation: float | None = None
    opportunities: list[str] = Field(default_factory=list)
    summary: str = ""


class ListingSuggestion(BaseModel):
    """Structured SEO listing recommendation."""

    title: str
    description: str
    bullet_points: list[str] = Field(default_factory=list)
    keywords: list[str] = Field(default_factory=list)
    seo_score: float | None = None


class PriceRecommendation(BaseModel):
    """Recommended price based on market and margin assumptions."""

    item_id: str
    current_price: float | None = None
    recommended_price: float
    suggested_range_min: float
    suggested_range_max: float
    rationale: str
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)


class StockAlert(BaseModel):
    """Alert describing a stock or pricing change condition."""

    item_id: str
    item_title: str
    alert_type: Literal["stock_low", "price_drop", "price_increase", "out_of_stock"]
    severity: Literal["low", "medium", "high"]
    message: str
    threshold_value: float | None = None


class AnalysisRequest(BaseModel):
    """Request for product analysis workflow."""

    query: str
    site_id: str = "MLA"
    limit: int = Field(default=10, gt=0)


class PriceRequest(BaseModel):
    """Request for pricing optimization workflow."""

    item_id: str
    target_margin: float | None = None
    min_price: float | None = None
    max_price: float | None = None


class WorkflowResult(BaseModel):
    """Generic output returned by a graph execution."""

    status: Literal["success", "partial", "error"] = "success"
    summary: str
    data: dict[str, Any] = Field(default_factory=dict)


class ListingInput(BaseModel):
    """Input for listing generation."""

    title: str
    description: str | None = None
    keywords: list[str] = Field(default_factory=list)
    brand: str | None = None
    target_audience: str | None = None


class SearchResult(BaseModel):
    """Search results response from the Mercado Libre API."""

    query: str
    total: int | None = None
    products: list[Product] = Field(default_factory=list)


class ErrorResponse(BaseModel):
    """Standardized API error payload."""

    message: str
    status_code: int | None = None
    error_type: str | None = None
