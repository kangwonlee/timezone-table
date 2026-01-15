#!/usr/bin/env python3
# timezone_table.py
from __future__ import annotations

import argparse
import datetime
import sys
from zoneinfo import ZoneInfo, available_timezones, ZoneInfoNotFoundError

# List of cities you want to show
CITY_ZONES = [
    ("San Diego", "America/Los_Angeles"),
    ("Phoenix", "America/Phoenix"),
    ("Edmonton", "America/Edmonton"),
    ("Chicago", "America/Chicago"),
    ("New York", "America/New_York"),
    ("Lisbon", "Europe/Lisbon"),
    ("London", "Europe/London"),
    ("Zurich", "Europe/Zurich"),
    ("Rome", "Europe/Rome"),
    ("Oslo", "Europe/Oslo"),
    ("Paris", "Europe/Paris"),
    ("Berlin", "Europe/Berlin"),
    ("Bucharest", "Europe/Bucharest"),
    ("Dubai", "Asia/Dubai"),
    ("New Delhi", "Asia/Kolkata"),
    ("Singapore", "Asia/Singapore"),
    ("Seoul", "Asia/Seoul"),
    ("Sydney", "Australia/Sydney"),
]

def get_utc_offset(tz: ZoneInfo, dt: datetime.datetime) -> datetime.timedelta:
    """Get UTC offset for sorting."""
    return dt.astimezone(tz).utcoffset() or datetime.timedelta(0)

def format_meeting(
    start: datetime.datetime,
    end: datetime.datetime,
    city: str,
    tz_str: str,
    city_width: int,
) -> str:
    """Format a table row for the meeting in local time."""
    tz = ZoneInfo(tz_str)
    try:
        local_start = start.astimezone(tz)
        local_end = end.astimezone(tz)
    except datetime.zoneinfo.AmbiguousTimeError:
        raise ValueError(f"Ambiguous time in {tz_str} due to DST transition.")
    zone_abbr = local_start.strftime("%Z")
    return f"| {city.ljust(city_width)} | {local_start.strftime('%H:%M')} – {local_end.strftime('%H:%M')} | {zone_abbr} |"

def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate a Markdown timezone table for a meeting.",
        epilog="Example: python timezone_table.py 2026 1 14 10 0 America/Los_Angeles 60"
    )
    parser.add_argument("year", type=int, help="Year (e.g., 2026)")
    parser.add_argument("month", type=int, help="Month (1-12)")
    parser.add_argument("day", type=int, help="Day (1-31)")
    parser.add_argument("hour", type=int, help="Hour (0-23)")
    parser.add_argument("minute", type=int, help="Minute (0-59)")
    parser.add_argument("timezone", type=str, help="IANA timezone (e.g., America/Los_Angeles)")
    parser.add_argument("duration_minutes", type=int, help="Duration in minutes (positive integer)")
    parser.add_argument("--sort-by-offset", action="store_true", help="Sort cities by UTC offset (west to east)")

    args = parser.parse_args()

    if args.duration_minutes <= 0:
        parser.error("Duration must be positive.")

    try:
        tz = ZoneInfo(args.timezone)
    except ZoneInfoNotFoundError as e:
        print(f"Invalid timezone: {args.timezone}")
        print(e)
        sys.exit(1)

    try:
        meeting_start = datetime.datetime(
            args.year, args.month, args.day, args.hour, args.minute, tzinfo=tz
        )
        meeting_end = meeting_start + datetime.timedelta(minutes=args.duration_minutes)
    except ValueError as e:
        print(f"Invalid date/time: {e}")
        sys.exit(1)

    # Optional: Sort by UTC offset
    if args.sort_by_offset:
        CITY_ZONES.sort(key=lambda x: get_utc_offset(ZoneInfo(x[1]), meeting_start))

    # Dynamic city width
    city_width = max(len(city) for city, _ in CITY_ZONES) + 2  # Padding

    print("# Meeting Time Converter\n")
    print(f"**Original time:** {meeting_start.strftime('%Y-%m-%d %H:%M %Z')} ({args.timezone})")
    print(f"**Duration:** {args.duration_minutes} minutes\n")
    print(f"| {'City'.ljust(city_width)} | Local Time          | Time Zone |")
    print(f"|{'-' * (city_width + 2)}|---------------------|-----------|")

    not_available = []
    for city, tz_str in CITY_ZONES:
        if tz_str not in available_timezones():
            not_available.append((city, tz_str))
            continue
        try:
            print(format_meeting(meeting_start, meeting_end, city, tz_str, city_width))
        except ValueError as e:
            print(f"Error for {city} ({tz_str}): {e}")

    if not_available:
        print("\n**Unavailable timezones:**")
        for city, tz_str in not_available:
            print(f"- {city}: {tz_str}")

if __name__ == "__main__":
    main()
