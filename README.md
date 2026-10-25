# Meli AI Agent Suite

Herramientas de inteligencia comercial para Mercado Libre: análisis de competencia con estadísticas calculadas sobre resultados reales, generación de publicaciones con Amazon Bedrock y recomendaciones de precio basadas en precios observados.

> **Estado:** MVP. Análisis y alertas consultan Mercado Libre; generación de copy requiere acceso a Bedrock. No publica ni modifica artículos automáticamente.

## Funcionalidades
- **Análisis de competencia:** media, mediana, mínimo y máximo de precios observados; no inventa métricas si faltan datos.
- **Generación de publicaciones:** copy estructurado con Bedrock, usando hechos proporcionados y validando el formato.
- **Optimización de precios:** contrasta precio actual y precios observados; puede aplicar un piso de margen con costo y margen objetivo.
- **Alertas de stock:** umbral configurable, sin modificar inventario.
- **CLI:** límites de entrada y errores legibles.

## Arquitectura
```text
Typer CLI -> MeliWorkflow -> Mercado Libre API
                       |-> CompetitorAnalystAgent (estadística determinista)
                       |-> ContentGeneratorAgent -> Bedrock Converse API
                       |-> PricingOptimizerAgent (reglas deterministas)
                       |-> StockAlertAgent
Pydantic models -> validación de entradas/salidas
```

## Requisitos e instalación
Python 3.11+, credenciales de Mercado Libre si el endpoint lo requiere, y AWS con permiso `bedrock:InvokeModel` para generar contenido.

```bash
git clone https://github.com/Lazaro549/meli-ai-agent-suite.git
cd meli-ai-agent-suite
python -m venv .venv
# Windows PowerShell: .venv\\Scripts\\Activate.ps1
# macOS/Linux: source .venv/bin/activate
python -m pip install -U pip
pip install -e ".[dev]"
cp .env.example .env
```

Editá `.env` con credenciales propias y no subas ese archivo. AWS usa la cadena estándar de credenciales de boto3 (variables de entorno, perfil local o rol de ejecución).

## Uso
```bash
meli-ai analyze --query "teclado mecánico" --limit 10
meli-ai generate-listing --title "Cable USB-C 1 metro" --description "Cable USB-C de 1 metro" --keywords "USB-C,carga,datos"
meli-ai price --item-id MLA123456789 --target-margin 0.25 --cost 10000
meli-ai stock-alert --item-id MLA123456789
```
También funciona con `python -m src.main ...`.

## Recomendaciones y límites
Las recomendaciones son orientativas. La aplicación no conoce automáticamente todos los costos, impuestos, comisiones, promociones o costos logísticos. Proporcioná un costo fiable para calcular un piso por margen. Si no hay precios de mercado o precio actual válido, la herramienta falla explícitamente en vez de inventar una cifra. Las métricas representan la muestra devuelta por la API, no todo el mercado.

## Calidad y CI
```bash
ruff check src tests
pytest -q
```
GitHub Actions ejecuta lint y tests. Los tests usan HTTP y Bedrock simulados: no necesitan secretos ni consumen servicios externos.

## Docker
```bash
docker build -t meli-ai-agent-suite .
docker run --rm meli-ai-agent-suite --help
```
Inyectá variables al contenedor desde un gestor de secretos o un archivo local no versionado.

## Seguridad
Nunca guardes credenciales en código ni commits. Usá IAM de mínimo privilegio y rotá credenciales expuestas. Las respuestas del LLM se consideran datos no confiables y se validan antes de mostrarlas. La aplicación no publica ni modifica artículos automáticamente. Ver [SECURITY.md](SECURITY.md) y [LICENSE](LICENSE).

## Limitaciones conocidas
- La reputación no se calcula si la búsqueda no la incluye.
- La integración puede requerir token según endpoint y permisos vigentes de Mercado Libre.
- La disponibilidad de modelos Bedrock depende de región, cuenta y proveedor.
