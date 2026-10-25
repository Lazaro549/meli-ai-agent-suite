from __future__ import annotations

import logging
from typing import Annotated

import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from src.config import settings
from src.graphs.meli_workflow import meli_workflow

logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO))
logger = logging.getLogger("meli_ai")
console = Console()
app = typer.Typer(help="Mercado Libre AI Agent Suite")


def _print_json(data: object) -> None:
    console.print(Syntax(str(data).replace("'", '"'), "json", theme="monokai"))


@app.callback()
def main_callback() -> None:
    """Application entry point."""


@app.command("analyze")
def analyze_competitor(
    query: Annotated[str, typer.Option(..., help="Search query to analyze")],
) -> None:
    """Analyze competitor pricing, reputation, and positioning for a target product."""

    console.print(Panel.fit(f"Competitor analysis for: {query}", style="cyan"))

    result = meli_workflow.invoke({"query": query})
    _print_json(result)


@app.command("generate-listing")
def generate_listing(
    title: Annotated[str, typer.Option(..., help="Product title to generate SEO metadata for")],
) -> None:
    """Generate listing title and description suggestions."""

    console.print(Panel.fit(f"Generating listing for: {title}", style="green"))
    result = meli_workflow.invoke({"title": title})
    _print_json(result)


@app.command("price")
def optimize_price(
    item_id: Annotated[str, typer.Option(..., help="Mercado Libre item identifier")],
) -> None:
    """Generate a price recommendation for an item."""

    console.print(Panel.fit(f"Pricing optimization for item: {item_id}", style="magenta"))
    result = meli_workflow.invoke({"item_id": item_id})
    _print_json(result)


if __name__ == "__main__":
    app()
