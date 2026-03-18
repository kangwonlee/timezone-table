# Meeting Time Converter ⏰🌍

A super-simple GitHub Actions tool that instantly converts your meeting time into **major cities worldwide** — perfect for scheduling international calls without doing time-zone math!

No installation · No dependencies · Just click and run.

### Live Demo
Just go to the **Actions** tab and run it:
→ https://github.com/kangwonlee/timezone-table/actions/workflows/meeting-time.yml

### How to Use

1. Click on the **Actions** tab
2. In the left sidebar, select **Meeting Time Converter**
3. Click the blue button **Run workflow** (top-right)
4. Fill in the form:
   - **Year** – e.g. `2026` (leave empty for current year)
   - **Month** – `1` to `12` (leave empty for current month)
   - **Day** – `1` to `31` (leave empty for today)
   - **Hour** – `0`–`23` (24-hour format)
   - **Minute** – `0`–`59`
   - **Timezone** – IANA name of the original time (default: `Europe/Paris`)
     Common examples:
     `Europe/Paris`, `Europe/London`, `America/New_York`, `America/Los_Angeles`, `Asia/Tokyo`, `Asia/Dubai`, etc.
   - **Duration** – meeting length in minutes (default: `60`)
   - **Generate 24-hour XLSX** – `true` or `false` (default: `false`) to generate an optional 24-hour timezone table in Excel format

5. Click the green **Run workflow** button (may take about 15 seconds)

The result appears immediately in the workflow run summary as a beautiful Markdown table:

# Meeting Time Converter

**Original time:** 2026-01-15 14:00 CET (Europe/Paris)
**Duration:** 60 minutes

| City        | Local Time          | Time Zone |
|-------------|---------------------|-----------|
| San Diego   | 05:00 – 06:00 | PST |
| Phoenix     | 06:00 – 07:00 | MST |
| Chicago     | 07:00 – 08:00 | CST |
| New York    | 08:00 – 09:00 | EST |
| London      | 13:00 – 14:00 | GMT |
| Paris       | 14:00 – 15:00 | CET |
| Singapore   | 21:00 – 22:00 | +08 |
| Sydney      | 00:00 – 01:00 | AEDT |

You can copy-paste the table directly into Slack, Notion, emails, etc.

### Optional: 24-Hour XLSX Table
If you enable `generate_xlsx: true`, the workflow generates an Excel file showing the full 24-hour day in the original timezone, converted to each city's local time.

- **Colors**: Green for typical working hours (9:00–17:00 local), gray for sleep hours (22:00–7:00 local).
- **Download**: After the workflow completes, go to the run page, scroll to the "Artifacts" section at the bottom, and download `24hour_timezones_{day}`.

This is great for visualizing availability across timezones for the entire day.

### Customization
- **Cities**: The tool uses the list from `cities.json`. Fork the repo and edit this file to add/remove cities (format: `{"city": "City Name", "timezone": "IANA/Timezone"}`).
- **Sorting**: By default, cities are in the order listed. To sort west-to-east (by UTC offset), edit the workflow YAML to add `--sort-by-offset` to the `uv run` command.
- **More Options**: See `timezone_table.py` for additional features like handling ambiguous DST times.

### Important
> **Versions before v0.2.0 have incorrect DST/summer-time handling.**
> Duration arithmetic used wall-clock time instead of real elapsed time, producing wrong meeting end times across spring-forward and fall-back boundaries. The 24-hour XLSX table also generated phantom rows for non-existent gap times. Please use v0.2.0 or later.

### Tech
- Python + built-in `zoneinfo`
- Powered by [**uv**](https://github.com/astral-sh/uv) – fast Python dependency management
- Pure GitHub Actions – zero setup

Just fork, star, or reuse in your own team/org repo!

Made with ❤️ for distributed teams.

(Got help from Grok 4 by xAI)
