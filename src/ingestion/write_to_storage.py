"""MinIO storage operations for ingested data."""

from datetime import datetime, timedelta
from io import BytesIO
from typing import Literal

from minio import Minio
from minio.error import S3Error

from logger.log_handler import log


def today_date() -> str:
    """Return today's date as YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")


def day_before_date() -> str:
    """Return yesterday's date as YYYY-MM-DD."""
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def write_to_storage(
    client: Minio, data: BytesIO, filetype: Literal["parquet", "json", "csv"] = "parquet"
) -> bool | None:
    """Write data to MinIO storage with date-based filenames."""
    try:
        if not client.bucket_exists(filetype):
            log.error("Bucket '%s' does not exist. Please check your Docker setup.", filetype)
            return False

        if datetime.now().hour >= 9:
            filename = f"{today_date()}_data.{filetype}"
        else:
            filename = f"{day_before_date()}_data.{filetype}"

        objects = client.list_objects(bucket_name=filetype, prefix=filename)
        if any(objects):
            log.warning("Object '%s' already exists in bucket '%s'.", filename, filetype)
            return None

        result = client.put_object(filetype, filename, data, length=-1, part_size=5 * 1024 * 1024)

        log.info("Created %s object; etag: %s, version-id: %s", result.object_name, result.etag, result.version_id)
        return True
    except S3Error as e:
        log.error("An error occurred: %s", e)
        return False
