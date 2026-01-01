# begin timezone_table.py
# timezone_table.py
from __future__ import annotations

import datetime
import sys
from zoneinfo import ZoneInfo


# List of cities you want to show
CITY_ZONES = [
    ("San Diego", "America/Los_Angeles"),
    ("Chicago", "America/Chicago"),
    ("New York", "America/New_York"),
    ("Lisbon", "Europe/Lisbon"),
    ("London", "Europe/London"),
    ("Rome", "Europe/Rome"),
    ("Oslo", "Europe/Oslo"),
    ("Paris", "Europe/Paris"),
    ("Berlin", "Europe/Berlin"),
    ("Bucharest", "Europe/Bucharest"),
    ("Dubai", "Asia/Dubai"),
    ("New Delhi", "Asia/Kolkata"),
    ("Seoul", "Asia/Seoul"),
    ("Sydney", "Australia/Sydney"),
]


def format_meeting(
    start: datetime.datetime,
    end: datetime.datetime,
    city: str,
    tz_str: str,
) -> str:
    tz = ZoneInfo(tz_str)
    local_start = start.astimezone(tz)
    local_end = end.astimezone(tz)
    zone_abbr = local_start.strftime("%Z")
    return f"| {city.ljust(12)} | {local_start.strftime('%H:%M')} – {local_end.strftime('%H:%M')} | {zone_abbr} |"


def main() -> None:
    if len(sys.argv) != 8:
        print("Usage: python timezone_table.py <year> <month> <day> <hour> <minute> <timezone> <duration_minutes>")
        sys.exit(1)

    year = int(sys.argv[1])
    month = int(sys.argv[2])
    day = int(sys.argv[3])
    hour = int(sys.argv[4])
    minute = int(sys.argv[5])
    tz_name = sys.argv[6]
    duration_min = int(sys.argv[7])

    try:
        tz = ZoneInfo(tz_name)
    except Exception as e:
        print(f"Invalid timezone: {tz_name}")
        print(e)
        sys.exit(1)

    # Create aware datetime in the given timezone
    meeting_start = datetime.datetime(year, month, day, hour, minute, tzinfo=tz)
    meeting_end = meeting_start + datetime.timedelta(minutes=duration_min)

    print(f"# Meeting Time Converter\n")
    print(f"**Original time:** {meeting_start.strftime('%Y-%m-%d %H:%M %Z')} ({tz_name})")
    print(f"**Duration:** {duration_min} minutes\n")
    print("| City         | Local Time          | Time Zone |")
    print("|--------------|---------------------|-----------|")

    for city, tz_str in CITY_ZONES:
        print(format_meeting(meeting_start, meeting_end, city, tz_str))


if __name__ == "__main__":
    main()
# end timezone_table.py
