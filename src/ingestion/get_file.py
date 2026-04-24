"""HTTP file fetching with caching support."""

import json
from typing import Literal

from requests_cache import CachedSession

from logger.log_handler import log


def get_url_from_endpoints(
    endpoints_path: str = "src/ingestion/endpoints.json", filetype: Literal["parquet", "json", "csv"] = "parquet"
) -> str | None:
    """Read the API URL for the given filetype from the endpoints config."""
    with open(endpoints_path) as file:
        endpoints: dict[str, str] = json.load(file)
    if filetype not in endpoints:
        log.error("filetype '%s' not found in endpoints.json", filetype)
        return None
    return endpoints[filetype]


def get_file_from_url(url: str | None, session: CachedSession) -> dict[str, object]:
    """Fetch a file from the given URL using a cached session."""
    if url is None:
        log.error("No URL provided.")
        return {"status": 404, "from_cache": False, "response": None}

    session.cache.delete(expired=True)

    response = session.get(url)

    return {"status": response.status_code, "from_cache": response.from_cache, "response": response.content}
