from datetime import datetime, timezone
from typing import Any, Dict


# Price is considered LIVE for one minute.
FRESH_SECONDS = 60

# Price is considered RECENT for fifteen minutes.
RECENT_SECONDS = 15 * 60

# Price becomes STALE after one hour.
STALE_SECONDS = 60 * 60


def get_current_time() -> datetime:
    """
    Return the current UTC time.
    """

    return datetime.now(
        timezone.utc
    )


def parse_timestamp(
    timestamp: str,
) -> datetime:
    """
    Convert an ISO timestamp into a datetime object.
    """

    parsed = datetime.fromisoformat(
        timestamp.replace(
            "Z",
            "+00:00",
        )
    )

    if parsed.tzinfo is None:
        parsed = parsed.replace(
            tzinfo=timezone.utc
        )

    return parsed


def seconds_since_check(
    checked_at: str,
) -> float:
    """
    Calculate the number of seconds since
    the price was checked.
    """

    checked_time = parse_timestamp(
        checked_at
    )

    now = get_current_time()

    return max(
        0,
        (
            now - checked_time
        ).total_seconds(),
    )


def freshness_status(
    checked_at: str,
) -> str:
    """
    Determine the freshness status of a price.

    Possible values:

    live
    recent
    aging
    stale
    """

    age = seconds_since_check(
        checked_at
    )

    if age <= FRESH_SECONDS:
        return "live"

    if age <= RECENT_SECONDS:
        return "recent"

    if age <= STALE_SECONDS:
        return "aging"

    return "stale"


def freshness_label(
    checked_at: str,
) -> str:
    """
    Return a human-readable freshness label.
    """

    age = seconds_since_check(
        checked_at
    )

    if age < 60:
        seconds = int(age)

        if seconds <= 1:
            return "Checked just now"

        return (
            f"Checked {seconds} seconds ago"
        )

    minutes = int(
        age // 60
    )

    if minutes < 60:
        return (
            f"Checked {minutes} minutes ago"
        )

    hours = int(
        minutes // 60
    )

    if hours < 24:
        return (
            f"Checked {hours} hours ago"
        )

    days = int(
        hours // 24
    )

    return (
        f"Checked {days} days ago"
    )


def enrich_freshness(
    product: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Add freshness information to a product.
    """

    result = dict(
        product
    )

    checked_at = result.get(
        "checked_at"
    )

    if not checked_at:
        result["freshness"] = "unknown"

        result["freshness_label"] = (
            "Not checked yet"
        )

        return result

    result["freshness"] = (
        freshness_status(
            checked_at
        )
    )

    result["freshness_label"] = (
        freshness_label(
            checked_at
        )
    )

    result["age_seconds"] = (
        seconds_since_check(
            checked_at
        )
    )

    return result