# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Meeting Time Converter — a GitHub Actions tool and CLI that converts meeting times across multiple timezones, outputting a Markdown table. Optionally generates a 24-hour XLSX file with color-coded working/sleep hours.

## Commands

```bash
# Install dependencies
uv venv && uv sync --group dev

# Run the tool (positional args: year month day hour minute timezone duration_minutes)
uv run timezone_table.py 2026 1 15 14 0 Europe/Paris 60

# Optional flags
uv run timezone_table.py 2026 1 15 14 0 Europe/Paris 60 --sort-by-offset --generate-24hour-xlsx --cities-file cities.json

# Run all tests
uv run pytest -v

# Run a single test
uv run pytest -v tests/test_timezone_table.py::test_format_meeting
```

## Architecture

Single-module design: all logic lives in `timezone_table.py` (~200 lines). No frameworks — just stdlib + minimal deps (`tzdata`, `openpyxl`).

**Key design choices:**
- `openpyxl` is lazy-imported only when `--generate-24hour-xlsx` is used
- City list is configurable via `cities.json` (array of `{"city", "timezone"}` objects); falls back to hardcoded `CITY_ZONES` if file is missing
- All datetimes are converted through UTC internally to avoid DST ambiguity
- Uses `zoneinfo.ZoneInfo` (stdlib, Python 3.10+) with modern type hints (`from __future__ import annotations`)

**`cities.json` schema:** Array of objects with `"city"` (display name) and `"timezone"` (IANA timezone string). Validated at load time.

## CI

- **ci.yml**: Runs pytest across Python 3.10–3.14 on push/PR
- **meeting-time.yml**: Manual workflow dispatch for generating timezone tables via GitHub Actions UI
- No linter or formatter is configured
