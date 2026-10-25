from __future__ import annotations
import json
import logging
from typing import Annotated, Optional
import typer
from rich.console import Console
from rich.panel import Panel
from src.config import settings
from src.graphs.meli_workflow import meli_workflow

logging.basicConfig(level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("meli_ai")
console = Console()
app = typer.Typer(help="Mercado Libre AI Agent Suite", no_args_is_help=True)

def _emit(data: object) -> None:
    console.print_json(json.dumps(data, ensure_ascii=False, default=str))

def _fail(exc: Exception) -> None:
    logger.error("Command failed: %s", exc)
    console.print(f"[red]Error:[/red] {exc}")
    raise typer.Exit(code=1) from exc

@app.command("analyze")
def analyze_competitor(query: Annotated[str, typer.Option(help="Search query to analyze")],
    limit: Annotated[int, typer.Option(min=1, max=50)] = 10) -> None:
    """Calculate competitor statistics from live Mercado Libre search results."""
    try:
        console.print(Panel.fit(f"Análisis de competencia: {query}", style="cyan"))
        _emit(meli_workflow.analyze(query, limit))
    except (ValueError, RuntimeError) as exc:
        _fail(exc)

@app.command("generate-listing")
def generate_listing(title: Annotated[str, typer.Option(help="Product title")],
    description: Annotated[Optional[str], typer.Option(help="Known product facts")] = None,
    keywords: Annotated[Optional[str], typer.Option(help="Comma-separated keywords")] = None) -> None:
    """Generate listing copy using Bedrock and validate structured output."""
    try:
        keyword_list = [p.strip() for p in (keywords or "").split(",") if p.strip()]
        _emit(meli_workflow.generate_listing(title, keyword_list, description))
    except (ValueError, RuntimeError) as exc:
        _fail(exc)

@app.command("price")
def optimize_price(item_id: Annotated[str, typer.Option(help="Mercado Libre item ID")],
    target_margin: Annotated[Optional[float], typer.Option(min=0.0, max=0.99)] = None,
    cost: Annotated[Optional[float], typer.Option(min=0.0)] = None,
    limit: Annotated[int, typer.Option(min=1, max=50)] = 10) -> None:
    """Recommend a price based on a real item and live competitor prices."""
    try:
        _emit(meli_workflow.optimize_price(item_id, target_margin, cost, limit))
    except (ValueError, RuntimeError) as exc:
        _fail(exc)

@app.command("stock-alert")
def stock_alert(item_id: Annotated[str, typer.Option(help="Mercado Libre item ID")]) -> None:
    """Check stock levels for a live Mercado Libre item."""
    try:
        _emit(meli_workflow.evaluate_stock(item_id))
    except (ValueError, RuntimeError) as exc:
        _fail(exc)

if __name__ == "__main__":
    app()
