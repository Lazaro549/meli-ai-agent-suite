from __future__ import annotations

import logging
from typing import Any

logger = logging.getLogger(__name__)


class OrchestratorAgent:
    """Routes incoming workflow requests to the most suitable specialist agent."""

    def route(self, payload: dict[str, Any]) -> str:
        if payload.get("query"):
            logger.info("Routing request to competitor analyst")
            return "competitor_analyst"
        if payload.get("title"):
            logger.info("Routing request to content generator")
            return "content_generator"
        if payload.get("item_id"):
            logger.info("Routing request to pricing optimizer")
            return "pricing_optimizer"
        logger.info("Routing request to stock alert agent")
        return "stock_alert"
