# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A data pipeline for Paris Open Data events, built around a medallion architecture:
**Ingestion** (API → MinIO) → **Transformation** (DBT + DuckDB) → **Exposition** (Streamlit).

## Data Stack

| Tool | Role |
|------|------|
| Python 3.12 | Runtime |
| uv | Package manager + virtual environments |
| Just (rust-just) | Task runner — all workflow commands go through `just` |
| MinIO | S3-compatible object storage (data lake) — runs via Docker |
| DuckDB | Embedded analytical database (warehouse) |
| dbt-core + dbt-duckdb | SQL transformation framework (bronze/silver/gold layers) |
| Streamlit | Web exposition layer |
| pandas | Data manipulation |
| pendulum | Datetime handling |
| requests-cache | HTTP response caching (1-day TTL) |
| fsspec[s3] | S3-compatible filesystem access from DuckDB/DBT |
| Rich | Console + file logging |
| Ruff | Python linter + formatter |
| mypy (strict) | Static type checker |
| SQLFluff | SQL linter (DuckDB dialect, DBT templater) |
| pre-commit | Git hooks framework (5 repos configured) |
| commitizen | Conventional commits + changelog |

## Commands

All tasks run via [Just](https://just.systems/). Prefix commands with `uv run`.

```bash
# Setup
uv sync --frozen --all-groups
uv pip install -e .

# Infrastructure
uv run just comp-check        # Validate docker-compose file
uv run just comp-start        # Create datalake directory and start MinIO (Docker)
uv run just comp-restart      # Restart the docker stack
uv run just comp-clean        # Stop and remove containers
uv run just comp-show         # Display all docker compose services

# Pipeline
uv run just ingest            # Fetch Paris Open Data → MinIO
uv run just dbt-run           # Transform data (DBT + DuckDB)
uv run just expose            # Start Streamlit app
uv run just final-workflow    # Run full pipeline (ingest → dbt-run → expose)

# Code quality
uv run just quality-all       # Run all pre-commit hooks on all files
uv run just quality-default   # Run only on staged files

# DBT
uv run just dbt-debug         # Debug dbt profile configuration
uv run just dbt-run           # Execute dbt models
uv run just dbt-catalog       # Build and serve DBT docs (port 3000)
uv run just dbt-clean         # Clean compiled files, artifacts, and logs
uv run just duckdb-ui         # Run dbt models and start DuckDB UI
```

### Environment Variables

Create a `.env` file at the project root:

```bash
DBT_ENV_SECRET_MINIO_ACCESS_KEY="<username, 3+ chars>"
DBT_ENV_SECRET_MINIO_SECRET_KEY="<password, 8+ chars>"
DBT_PROFILES_DIR="./src/transformation/dbt_paris_event_analyzer/profiles/"
DBT_PROJECT_DIR="./src/transformation/dbt_paris_event_analyzer/"
```

## Architecture

### Data Flow

```
Paris Open Data API
    ↓ (requests-cache, 1-day TTL)
src/ingestion/          → MinIO (parquet/csv/json buckets)
    ↓
src/transformation/     → DuckDB warehouse (bronze/silver/gold layers)
    ↓
src/exposition/         → Streamlit web app
```

### Layer Details

**Ingestion** (`src/ingestion/`): Fetches events from endpoints defined in `endpoints.json`, caches responses to avoid redundant API calls, and writes to MinIO S3-compatible storage.

**Transformation** (`src/transformation/dbt_paris_event_analyzer/`): DBT project using DuckDB. Three model layers:
- `bronze/` — raw data materialized from MinIO
- `silver/` — deduplicated, cleaned, enriched (accessibility, geocoding)
- `gold/` — business views consumed by the app (`today_events`, `nb_events_by_tags`, `handicap_friendly_events`)

**Exposition** (`src/exposition/`): Streamlit app that reads gold-layer tables from DuckDB. Supports filtering by price, tags, accessibility, and postal code. Entry point is `app.py`.

**Logger** (`src/logger/log_handler.py`): Centralized Rich-based logger writing to both console and `app.log`. All modules use this; the CI enforces exactly 12 calls to `log.` across the Python codebase.

## Code Quality & Linting

| Tool | Scope | Config |
|------|-------|--------|
| Ruff | Python lint + format | `pyproject.toml` |
| mypy (strict) | Python type checking | `pyproject.toml` |
| SQLFluff | SQL linting (DuckDB dialect, DBT templater) | `.sqlfluff` |
| commitizen | Conventional commits | `.pre-commit-config.yaml` |

- Python line length: 120 chars
- Docstring style: Google convention
- SQL: UPPERCASE keywords, lowercase identifiers, UPPERCASE types, max 230 chars/line
- Pre-commit hooks enforce all of the above on every commit

## CI/CD

`.github/workflows/lille.yml` runs pre-commit hooks via `prek` on pull requests to the `lille` branch.

## Data Exploration Workflow

A reproducible workflow to inspect the warehouse and answer business questions with Claude Code — no plugin required.

### Prerequisites

```bash
uv sync --frozen --all-groups   # Install dependencies
uv run just comp-start          # Start MinIO (Docker)
uv run just ingest              # Fetch today's events from Paris Open Data
uv run just dbt-run             # Build bronze/silver/gold tables in DuckDB
```

### Entry points

| Goal | Command |
|------|---------|
| Interactive SQL queries | `uv run just duckdb-ui` — opens the DuckDB UI on `warehouse/prod.duckdb` |
| Browse the model DAG + column docs | `uv run just dbt-catalog` — serves dbt docs on port 3000 |
| Explore via the app | `uv run just expose` — Streamlit UI with tag/price/accessibility filters |
| Quick CLI query | `duckdb warehouse/prod.duckdb "SELECT ..."` |

### Key tables

Start from the gold layer; go deeper into silver only if you need raw fields.

| Table | Schema | What it contains |
|-------|--------|-----------------|
| `today_events` | gold | Events with at least one occurrence today |
| `nb_events_by_tags` | gold | Tag frequency — good entry point for category analysis |
| `handicap_friendly_events` | gold | Events accessible to people with disabilities |
| `up_to_date_events` | silver | All non-outdated events, fully enriched (coordinates, accessibility struct, parsed schedule) |
| `agenda` | silver | Parsed occurrence slots — use when querying schedules |
| `filtered_rows` | silver | Cleaned raw columns (spatial extraction, HTML stripping) |
| `raw_events` | bronze | All 75 raw columns straight from the parquet file |

### Useful starter queries

```sql
-- How many events are available today?
SELECT count(*) FROM gold.today_events;

-- Top 10 tags by event count
SELECT qfap_tags_distinct, nb_events
FROM gold.nb_events_by_tags
LIMIT 10;

-- Free events happening today with an address
SELECT title, full_address, prochains_creneaux
FROM gold.today_events
WHERE price_type = 'Gratuit'
  AND full_address IS NOT NULL
ORDER BY rank DESC
LIMIT 20;

-- Accessible events with coordinates (for a map)
SELECT title, latitude, longitude, handicap_friendly_details
FROM gold.handicap_friendly_events
WHERE latitude IS NOT NULL
LIMIT 50;

-- Schema introspection: list all columns of a table
DESCRIBE silver.up_to_date_events;
```

### Asking Claude Code to explore the data

With the warehouse populated, you can delegate exploration directly to Claude Code:

- *"Combien d'événements gratuits ont lieu cette semaine dans le 11e ?"*
- *"Quels sont les tags les plus fréquents pour les événements pour enfants ?"*
- *"Montre-moi les 5 événements les mieux classés avec une adresse complète."*

Claude will run `duckdb warehouse/prod.duckdb "..."` queries against the local file — no external connection needed.
