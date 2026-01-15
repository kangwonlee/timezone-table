# begin tests/test_timezone_table.py

import datetime
import json
import pathlib
import pytest
import sys

from io import StringIO
from unittest.mock import patch
from zoneinfo import ZoneInfo

test_folder = pathlib.Path(__file__).parent.resolve()
project_folder = test_folder.parent.resolve()
sys.path.insert(0, str(project_folder))

from timezone_table import format_meeting, main, CITY_ZONES, read_city_zones

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
    assert "**Original time:** 2026-01-14 10:00 PST (America/Los_Angeles)" in output
    assert "**Duration:** 60 minutes" in output
    assert "| San Diego " in output and "10:00 – 11:00" in output and "PST" in output  # Fuzzy match for dynamic width
    assert "Unavailable timezones:" not in output  # Assuming all are available

def test_main_invalid_timezone(mock_argv):
    mock_argv[6] = "Invalid/TZ"
    with patch("sys.argv", mock_argv), pytest.raises(SystemExit):
        main()

def test_main_invalid_date(mock_argv):
    mock_argv[2] = "13"  # Invalid month
    with patch("sys.argv", mock_argv), pytest.raises(SystemExit):
        main()

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
    with patch("timezone_table.available_timezones", return_value=set()), patch("sys.argv", mock_argv):
        main()
    captured = capsys.readouterr()
    assert "**Unavailable timezones:**" in captured.out
    assert "- San Diego: America/Los_Angeles" in captured.out


def test_read_city_zones_no_file(tmp_path):
    # Test fallback to hardcoded when file doesn't exist
    non_existent_file = tmp_path / "non_existent.json"
    result = read_city_zones(non_existent_file)
    assert result == CITY_ZONES
    assert isinstance(result, list)
    assert all(isinstance(item, tuple) and len(item) == 2 for item in result)


def test_read_city_zones_valid_json(tmp_path):
    # Test loading from a valid JSON file
    valid_data = [
        {"city": "Test City1", "timezone": "America/Test1"},
        {"city": "Test City2", "timezone": "Europe/Test2"}
    ]
    valid_file = tmp_path / "valid.json"
    with open(valid_file, "w", encoding="utf-8") as f:
        json.dump(valid_data, f)
    
    result = read_city_zones(valid_file)
    expected = [("Test City1", "America/Test1"), ("Test City2", "Europe/Test2")]
    assert result == expected


def test_read_city_zones_invalid_json(tmp_path):
    # Test malformed JSON raises JSONDecodeError
    invalid_file = tmp_path / "invalid.json"
    with open(invalid_file, "w", encoding="utf-8") as f:
        f.write("this is not json")  # Malformed
    
    with pytest.raises(json.JSONDecodeError):
        read_city_zones(invalid_file)


def test_read_city_zones_wrong_structure(tmp_path):
    # Test JSON with missing keys raises KeyError
    wrong_data = [
        {"city": "Test City"},  # Missing "timezone"
        {"timezone": "Europe/Test"}  # Missing "city"
    ]
    wrong_file = tmp_path / "wrong.json"
    with open(wrong_file, "w", encoding="utf-8") as f:
        json.dump(wrong_data, f)
    
    with pytest.raises(KeyError):
        read_city_zones(wrong_file)


def test_read_city_zones_empty_file(tmp_path):
    # Test empty JSON list returns empty list
    empty_data = []
    empty_file = tmp_path / "empty.json"
    with open(empty_file, "w", encoding="utf-8") as f:
        json.dump(empty_data, f)
    
    result = read_city_zones(empty_file)
    assert result == []


def test_read_city_zones_default_file_not_present():
    # Test default filename when not present (fallback)
    result = read_city_zones()  # Uses default "city_zones.json"
    assert result == CITY_ZONES  # Assuming no real file exists in test env


if "__main__" == __name__:
    pytest.main(["-v", __file__])

# end tests/test_timezone_table.py
