# Justfile for Paris Event Analyzer

# Run the ingestion workflow
ingest:
    uv run python src/ingestion/main.py
