from __future__ import annotations

import logging
from typing import Any
from urllib.parse import quote

import httpx

from src.config import settings

logger = logging.getLogger(__name__)


class MercadoLibreAPIError(RuntimeError):
    """Raised when Mercado Libre returns an unusable response."""


class RateLimitExceededError(MercadoLibreAPIError):
    """Raised when the API rate limit is exceeded."""


class MercadoLibreClient:
    """Small, timeout-bounded client for public Mercado Libre item/search endpoints."""

    def __init__(self, base_url: str | None = None, access_token: str | None = None,
                 timeout: float | None = None, client: httpx.Client | None = None) -> None:
        self.base_url = (base_url or settings.meli_base_url).rstrip("/")
        self.access_token = access_token if access_token is not None else settings.meli_access_token
        self._client = client or httpx.Client(timeout=timeout or settings.request_timeout)
        self._owns_client = client is None

    def close(self) -> None:
        if self._owns_client:
            self._client.close()

    def __enter__(self) -> "MercadoLibreClient":
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        headers = {"Accept": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        try:
            response = self._client.get(f"{self.base_url}{path}", params=params, headers=headers)
        except httpx.HTTPError as exc:
            raise MercadoLibreAPIError(f"Mercado Libre request failed: {exc}") from exc
        if response.status_code == 429:
            raise RateLimitExceededError("Mercado Libre rate limit exceeded; retry later.")
        if response.is_error:
            detail = response.text[:300]
            raise MercadoLibreAPIError(f"Mercado Libre returned HTTP {response.status_code}: {detail}")
        try:
            payload = response.json()
        except ValueError as exc:
            raise MercadoLibreAPIError("Mercado Libre returned invalid JSON.") from exc
        if not isinstance(payload, dict):
            raise MercadoLibreAPIError("Mercado Libre returned an unexpected response shape.")
        return payload

    def search_items(self, query: str, site_id: str | None = None, limit: int = 10) -> dict[str, Any]:
        query = query.strip()
        if not query:
            raise ValueError("Search query cannot be empty.")
        if not 1 <= limit <= 50:
            raise ValueError("limit must be between 1 and 50.")
        site = quote(site_id or settings.meli_site_id, safe="")
        return self._get(f"/sites/{site}/search", {"q": query, "limit": limit})

    def get_item(self, item_id: str) -> dict[str, Any]:
        if not item_id.strip():
            raise ValueError("item_id cannot be empty.")
        return self._get(f"/items/{quote(item_id.strip(), safe='')}")

    def search_products(self, query: str, site_id: str | None = None, limit: int = 10) -> list[dict[str, Any]]:
        payload = self.search_items(query, site_id, limit)
        results = payload.get("results", [])
        if not isinstance(results, list):
            raise MercadoLibreAPIError("Search response has no valid results list.")
        return [item for item in results if isinstance(item, dict)]
