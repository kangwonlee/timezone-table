# begin tests/test_timezone_table.py

import datetime
import pathlib
import pytest
import sys

from io import StringIO
from unittest.mock import patch
from zoneinfo import ZoneInfo

test_folder = pathlib.Path(__file__).parent.resolve()
project_folder = test_folder.parent.resolve()
sys.path.insert(0, str(project_folder))

from timezone_table import format_meeting, main, CITY_ZONES  # Assuming the script is in timezone_table.py

@pytest.fixture
def mock_argv():
    return [
        "timezone_table.py",  # sys.argv[0]
        "2026", "1", "14", "10", "0", "America/Los_Angeles", "60"
    ]

def test_format_meeting():
    start = datetime.datetime(2026, 1, 14, 10, 0, tzinfo=ZoneInfo("America/Los_Angeles"))
    end = start + datetime.timedelta(minutes=60)
    result = format_meeting(start, end, "San Diego", "America/Los_Angeles", city_width=12)
    assert result == "| San Diego    | 10:00 – 11:00 | PST |"

    # Test with different timezone
    result = format_meeting(start, end, "New York", "America/New_York", city_width=12)
    assert result == "| New York     | 13:00 – 14:00 | EST |"

def test_main_valid_input(capsys, mock_argv):
    with patch("sys.argv", mock_argv):
        main()
    captured = capsys.readouterr()
    output = captured.out

    assert "# Meeting Time Converter" in output
    assert "Original time: 2026-01-14 10:00 PST (America/Los_Angeles)" in output
    assert "Duration: 60 minutes" in output
    assert "| San Diego      | 10:00 – 11:00 | PST |" in output  # Adjusted for dynamic width, but testing presence
    assert "Unavailable timezones:" not in output  # Assuming all are available

def test_main_invalid_timezone(mock_argv):
    mock_argv[6] = "Invalid/TZ"
    with patch("sys.argv", mock_argv), pytest.raises(SystemExit):
        main()

def test_main_invalid_date(mock_argv):
    mock_argv[2] = "13"  # Invalid month
    with patch("sys.argv", mock_argv), pytest.raises(SystemExit):
        main()

def test_main_ambiguous_time():
    # Example with DST ambiguity (US fall back, e.g., Nov 3, 2024, 1:30 AM in America/Los_Angeles)
    start = datetime.datetime(2024, 11, 3, 1, 30, tzinfo=ZoneInfo("America/Los_Angeles"))
    end = start + datetime.timedelta(minutes=60)
    with pytest.raises(ValueError, match="Ambiguous time"):
        format_meeting(start, end, "San Diego", "America/Los_Angeles", city_width=12)

def test_main_sort_by_offset(capsys):
    argv = [
        "timezone_table.py", "2026", "1", "14", "10", "0", "America/Los_Angeles", "60", "--sort-by-offset"
    ]
    with patch("sys.argv", argv):
        main()
    captured = capsys.readouterr()
    output_lines = captured.out.splitlines()
    # Check if table rows are sorted (e.g., San Diego first, then eastwards)
    table_start = next(i for i, line in enumerate(output_lines) if line.startswith("| City"))
    first_city_row = output_lines[table_start + 2]  # After header and separator
    assert "San Diego" in first_city_row  # Westernmost

def test_unavailable_timezone(capsys, mock_argv):
    # Mock unavailable timezone
    with patch("zoneinfo.available_timezones", return_value=set()), patch("sys.argv", mock_argv):
        main()
    captured = capsys.readouterr()
    assert "**Unavailable timezones:**" in captured.out
    assert "- San Diego: America/Los_Angeles" in captured.out


if "__main__" == __name__:
    pytest.main(["-v", __file__])

# end tests/test_timezone_table.py
