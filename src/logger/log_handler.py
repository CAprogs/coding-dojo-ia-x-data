"""Rich logging handler configuration."""

import logging

from rich.logging import RichHandler


logging.basicConfig(level=logging.INFO, format="%(message)s", handlers=[RichHandler(rich_tracebacks=True)])

log = logging.getLogger("paris-events-analyzer")
