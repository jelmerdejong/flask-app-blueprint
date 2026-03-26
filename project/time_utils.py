from datetime import datetime, timezone


def utc_now() -> datetime:
    """Return a naive UTC timestamp to preserve DB compatibility."""
    return datetime.now(timezone.utc).replace(tzinfo=None)
