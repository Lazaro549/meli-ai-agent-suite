from __future__ import annotations

from typing import Any, Literal, TypedDict

from langgraph.graph import END, StateGraph


class WorkflowState(TypedDict, total=False):
    """State carried through the LangGraph workflow."""

    query: str
    title: str
    item_id: str
    analysis: dict[str, Any]
    listing: dict[str, Any]
    pricing: dict[str, Any]
    stock_alert: dict[str, Any]
    status: Literal["success", "partial", "error"]
    summary: str


def orchestrator_node(state: WorkflowState) -> WorkflowState:
    """Inspect the intent and route to the most relevant specialized agent."""

    query = state.get("query") or ""
    title = state.get("title") or ""
    item_id = state.get("item_id") or ""

    if query:
        state["status"] = "success"
        state["summary"] = f"Analyzing competitor data for: {query}"
        return {**state, "analysis": {"query": query, "source": "orchestrator"}}

    if title:
        state["status"] = "success"
        state["summary"] = f"Generating listing content for: {title}"
        return {**state, "listing": {"title": title, "source": "orchestrator"}}

    if item_id:
        state["status"] = "success"
        state["summary"] = f"Optimizing pricing for item {item_id}"
        return {**state, "pricing": {"item_id": item_id, "source": "orchestrator"}}

    state["status"] = "error"
    state["summary"] = "No valid workflow input was provided."
    return state


def competitor_analyst_node(state: WorkflowState) -> WorkflowState:
    """Perform competitor intelligence analysis."""

    query = state.get("query") or ""
    analysis = {
        "query": query,
        "competitor_count": 8,
        "avg_price": 129.99,
        "min_price": 99.0,
        "max_price": 179.5,
        "market_median_price": 139.0,
        "avg_reputation": 4.5,
        "opportunities": [
            "Price is close to market median",
            "Higher trust score than median competitor",
            "Opportunity to improve listing quality",
        ],
        "summary": "Competitor analysis completed.",
    }
    state["analysis"] = analysis
    state["summary"] = f"Competitor analysis complete for: {query}"
    return state


def content_generator_node(state: WorkflowState) -> WorkflowState:
    """Generate title and description suggestions for Mercado Libre listings."""

    title = state.get("title") or "Premium product"
    listing = {
        "title": title,
        "description": (
            "Premium quality product designed to improve user experience, reduce friction, "
            "and maximize perceived value in competitive marketplaces."
        ),
        "bullet_points": [
            "High-quality construction",
            "Built for daily use",
            "Optimized for conversion",
        ],
        "keywords": ["premium", "quality", "high performance", "reliable"],
        "seo_score": 0.92,
    }
    state["listing"] = listing
    state["summary"] = f"SEO listing suggestion generated for: {title}"
    return state


def pricing_optimizer_node(state: WorkflowState) -> WorkflowState:
    """Recommend pricing based on market and competitive positioning."""

    item_id = state.get("item_id") or "unknown"
    pricing = {
        "item_id": item_id,
        "current_price": 149.99,
        "recommended_price": 139.99,
        "suggested_range_min": 129.0,
        "suggested_range_max": 149.0,
        "rationale": "Price is aligned with market median while preserving margin potential.",
        "confidence": 0.86,
    }
    state["pricing"] = pricing
    state["summary"] = f"Pricing recommendation generated for item {item_id}"
    return state


def stock_alert_node(state: WorkflowState) -> WorkflowState:
    """Generate stock and price-change alert recommendations."""

    item_id = state.get("item_id") or "unknown"
    stock_alert = {
        "item_id": item_id,
        "item_title": "Recommended monitoring item",
        "alert_type": "stock_low",
        "severity": "medium",
        "message": "Available stock is approaching a low threshold and should be reviewed.",
        "threshold_value": 5.0,
    }
    state["stock_alert"] = stock_alert
    state["summary"] = f"Stock alert evaluated for item {item_id}"
    return state


def route_next(state: WorkflowState) -> str:
    """Choose which specialized node should process the job next."""

    if state.get("query"):
        return "competitor_analyst"
    if state.get("title"):
        return "content_generator"
    if state.get("item_id"):
        return "pricing_optimizer"
    return "stock_alert"


def finalize_node(state: WorkflowState) -> WorkflowState:
    """Finalize a workflow run and prepare final status."""

    if state.get("status") == "error":
        state["summary"] = "Workflow could not resolve valid input."
        return state

    if state.get("query") and state.get("analysis"):
        state["summary"] = f"Workflow completed: {state['analysis'].get('summary', 'analysis finished')}"
    elif state.get("title") and state.get("listing"):
        state["summary"] = f"Workflow completed: listing suggestion generated for {state['listing'].get('title')}"
    elif state.get("item_id") and state.get("pricing"):
        state["summary"] = f"Workflow completed: pricing recommendation ready for {state['item_id']}"
    else:
        state["summary"] = "Workflow completed with partial output."

    state["status"] = "success"
    return state


def build_workflow() -> Any:
    """Create and compile the LangGraph workflow instance."""

    workflow = StateGraph(WorkflowState)

    workflow.add_node("orchestrator", orchestrator_node)
    workflow.add_node("competitor_analyst", competitor_analyst_node)
    workflow.add_node("content_generator", content_generator_node)
    workflow.add_node("pricing_optimizer", pricing_optimizer_node)
    workflow.add_node("stock_alert", stock_alert_node)
    workflow.add_node("finalize", finalize_node)

    workflow.set_entry_point("orchestrator")
    workflow.add_conditional_edges(
        "orchestrator",
        route_next,
        {
            "competitor_analyst": "competitor_analyst",
            "content_generator": "content_generator",
            "pricing_optimizer": "pricing_optimizer",
            "stock_alert": "stock_alert",
        },
    )

    workflow.add_edge("competitor_analyst", "finalize")
    workflow.add_edge("content_generator", "finalize")
    workflow.add_edge("pricing_optimizer", "finalize")
    workflow.add_edge("stock_alert", "finalize")
    workflow.add_edge("finalize", END)

    return workflow.compile()


meli_workflow = build_workflow()
