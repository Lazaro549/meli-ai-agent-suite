# Meli AI Agent Suite

Meli AI Agent Suite is a multi-agent e-commerce intelligence platform designed for Mercado Libre marketplaces. It combines the Mercado Libre API with Amazon Bedrock to help sellers analyze competition, generate SEO-friendly listing content, optimize pricing, and monitor stock and price changes through orchestrated AI agents.

## Project goal

The system is intended to support Latin American e-commerce operations by giving sellers actionable recommendations in three key areas:

- Competition analysis: price comparison, sales signals, reputation, and market positioning
- Listing generation: SEO-optimized titles and descriptions for higher conversion
- Pricing optimization: recommended price ranges based on demand and competitor behavior
- Alerts: stock thresholds and pricing changes that require attention

## Architecture

```text
┌──────────────────────────────────────────────────────────────────────┐
│                         Mercado Libre API                             │
│  Search, item lookup, product metadata, site data                     │
└──────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────────┐
                    │   Meli Client / API Layer │
                    │   OAuth + HTTP requests    │
                    └───────────────┬───────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │    LangGraph Workflow      │
                    │  orchestrator + agents     │
                    │  - competitor analyst      │
                    │  - content generator       │
                    │  - pricing optimizer       │
                    │  - stock alert             │
                    └───────────────┬───────────┘
                                    │
                                    ▼
                    ┌───────────────────────────┐
                    │    Amazon Bedrock / LLM    │
                    │  reasoning + generation   │
                    └───────────────────────────┘
```

## Stack

- Python 3.11+
- LangGraph for agent orchestration
- LangChain AWS + boto3 for Bedrock integration
- Pydantic and pydantic-settings for configuration and model validation
- Typer for the CLI
- HTTPX for HTTP client requests
- Python-dotenv for environment variables
- Rich for terminal UX

## Repository structure

```text
meli-ai-agent-suite/
├── README.md
├── .env.example
├── .gitignore
├── pyproject.toml
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── main.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── orchestrator.py
│   │   ├── competitor_analyst.py
│   │   ├── content_generator.py
│   │   ├── pricing_optimizer.py
│   │   └── stock_alert.py
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── meli_client.py
│   │   └── bedrock_tools.py
│   ├── graphs/
│   │   └── meli_workflow.py
│   └── schemas/
│       └── models.py
├── examples/
│   ├── analyze_competitor.py
│   └── generate_listing.py
└── notebooks/
    └── 01_quickstart.ipynb
```

## Environment variables

Copy `.env.example` to `.env` and configure the values for your environment.

```bash
cp .env.example .env
```

Required variables:

```env
MELI_BASE_URL=https://api.mercadolibre.com
MELI_ACCESS_TOKEN=your_access_token_here
MELI_APP_ID=your_app_id_here
MELI_APP_SECRET=your_app_secret_here
MELI_REDIRECT_URI=https://localhost:8000/callback

AWS_REGION=us-east-1
AWS_ACCESS_KEY_ID=your_aws_access_key_id
AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key
AWS_SESSION_TOKEN=
BEDROCK_MODEL_ID=anthropic.claude-3-5-sonnet-20240620-v1:0

APP_ENV=development
LOG_LEVEL=INFO
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/Lazaro549/meli-ai-agent-suite.git
cd meli-ai-agent-suite
```

### 2. Create a virtual environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -U pip
pip install -e .
```

### 4. Configure environment

```bash
cp .env.example .env
# Fill in the required production values
```

## Usage

After installation, use the CLI commands:

```bash
python -m src.main analyze --query "iphone 15 case"
python -m src.main generate-listing --title "Cargador USB Type C 20W para iPhone"
python -m src.main price --item-id "MLA123456789"
```

You can also invoke the package entry point if installed in editable mode:

```bash
meli-ai analyze --query "celular samsung"
meli-ai generate-listing --title "Auriculares Bluetooth Inalámbricos"
meli-ai price --item-id "MLA123456789"
```

## Example use cases

### Competitor analysis

```bash
python -m src.main analyze --query "smartwatch mujer gps"
```

This can help identify:

- average competitor price
- price dispersion across the market
- opportunities to position a product more competitively
- signals related to trust and perceived quality

### Listing generation

```bash
python -m src.main generate-listing --title "Teclado Mecánico RGB USB C"
```

This can produce:

- SEO-friendly product title
- product description
- keyword list
- bullet points optimized for Mercado Libre conversion

### Pricing optimization

```bash
python -m src.main price --item-id "MLA123456789"
```

This can generate:

- current price reference
- recommended price
- recommended price range
- rationale and confidence score

## Development notes

This project is intentionally structured as a robust foundation for real-world multi-agent e-commerce operations. The initial skeleton is designed to be extended with real API calls, Bedrock-powered reasoning, database persistence, and more advanced monitoring workflows.

## Author

Lazaro Gomez Vitolo
GitHub: https://github.com/Lazaro549

## License

This project is provided as a starter architecture and can be adapted to commercial or internal use depending on the deployment context.

## 💸 Donations

If you'd like to support this project:

- 🇦🇷 ARS (Argentina)  
  Alias: `lazaro.503.alaba.mp`

- 🌎 USD (Argentina only, local transfers)  
  Alias: `ahogada.duras.foca`
