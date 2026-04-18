import uuid
import os
from datetime import datetime
from typing import Any


def generate_uuid() -> str:
    """Generate a new UUID string."""
    return str(uuid.uuid4())


def ensure_dir(path: str) -> None:
    """Ensure directory exists."""
    os.makedirs(path, exist_ok=True)


def format_datetime(dt: datetime) -> str:
    """Format datetime to ISO string."""
    return dt.isoformat()


def parse_date(date_str: str) -> datetime:
    """Parse date string to datetime."""
    from dateutil import parser
    return parser.parse(date_str)


def clean_text(text: str) -> str:
    """Clean and normalize text."""
    return " ".join(text.split())


def safe_get(d: dict, *keys, default: Any = None) -> Any:
    """Safely get nested dict value."""
    for key in keys:
        try:
            d = d[key]
        except (KeyError, TypeError, IndexError):
            return default
    return d
