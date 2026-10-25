from __future__ import annotations

from src.schemas.models import ListingSuggestion
from src.tools.bedrock_tools import BedrockClient


class ContentGeneratorAgent:
    """Generates structured listing copy grounded in supplied product facts."""

    def __init__(self, bedrock_client: BedrockClient | None = None) -> None:
        self.bedrock_client = bedrock_client or BedrockClient()

    def generate(self, title: str, keywords: list[str] | None = None,
                 description: str | None = None) -> ListingSuggestion:
        title = title.strip()
        if not title:
            raise ValueError("title cannot be empty")
        keyword_text = ", ".join(keywords or [])
        prompt = f"""Actuá como redactor de publicaciones para Mercado Libre Argentina.
Usá únicamente datos explícitos del producto; no inventes marca, materiales,
compatibilidad, certificaciones, garantía ni especificaciones.
Título: {title}
Descripción/datos disponibles: {description or "No proporcionados"}
Palabras clave: {keyword_text or "No proporcionadas"}
Devolvé SOLO JSON con title (máximo 60 caracteres si es posible), description,
bullet_points (3 a 5 puntos), keywords (hasta 5) y seo_score (0 a 1).
Si falta información, no la inventes."""
        data = self.bedrock_client.generate_json(prompt)
        score = float(data.get("seo_score", 0.0))
        if not 0 <= score <= 1:
            raise ValueError("Bedrock seo_score must be between 0 and 1")
        return ListingSuggestion(
            title=str(data.get("title") or title),
            description=str(data.get("description") or description or ""),
            bullet_points=[str(x) for x in data.get("bullet_points", [])][:5],
            keywords=[str(x) for x in data.get("keywords", [])][:5],
            seo_score=score,
        )
