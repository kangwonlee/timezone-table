# Meeting Time Converter ⏰🌍

여러 나라의 **주요 도시 시간대**로 회의 시간을 즉시 변환해 주는 GitHub Actions 도구입니다. 시차 계산 없이 국제 회의를 쉽게 예약하세요!

설치 불필요 · 의존성 없음 · 클릭만으로 실행.

### 라이브 데모
**Actions** 탭에서 바로 실행해 보세요:
→ https://github.com/kangwonlee/timezone-table/actions/workflows/meeting-time.yml

### 사용 방법

1. **Actions** 탭을 클릭합니다
2. 왼쪽 사이드바에서 **Meeting Time Converter**를 선택합니다
3. 오른쪽 상단의 **Run workflow** 파란색 버튼을 클릭합니다
4. 양식을 작성합니다:
   - **Year** – 예: `2026` (비워두면 현재 연도 사용)
   - **Month** – `1`~`12` (비워두면 현재 월 사용)
   - **Day** – `1`~`31` (비워두면 오늘 날짜 사용)
   - **Hour** – `0`~`23` (24시간 형식)
   - **Minute** – `0`~`59`
   - **Timezone** – 원래 시간대의 IANA 이름 (기본값: `Europe/Paris`)
     자주 쓰는 예시:
     `Europe/Paris`, `Europe/London`, `America/New_York`, `America/Los_Angeles`, `Asia/Tokyo`, `Asia/Seoul`, `Asia/Dubai` 등
   - **Duration** – 회의 길이 (분 단위, 기본값: `60`)
   - **Generate 24-hour XLSX** – `true` 또는 `false` (기본값: `false`). 24시간 시간대 비교표를 Excel 파일로 생성합니다

5. 녹색 **Run workflow** 버튼을 클릭합니다 (약 15초 소요)

결과가 워크플로 실행 요약에 마크다운 표로 즉시 표시됩니다:

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

표를 복사해서 Slack, Notion, 이메일 등에 바로 붙여넣기 할 수 있습니다.

### 선택 사항: 24시간 XLSX 표
`generate_xlsx: true`를 설정하면, 원래 시간대의 24시간 전체를 각 도시의 현지 시간으로 변환한 Excel 파일이 생성됩니다.

- **색상 구분**: 녹색은 일반 근무 시간 (현지 9:00~17:00), 회색은 수면 시간 (현지 22:00~7:00)
- **다운로드**: 워크플로 실행 완료 후, 실행 페이지 하단의 "Artifacts" 섹션에서 `24hour_timezones_{day}`를 다운로드합니다

하루 전체의 시간대별 가용 시간을 한눈에 파악하는 데 유용합니다.

### 커스터마이징
- **도시 목록**: `cities.json` 파일의 도시 목록을 사용합니다. 저장소를 포크한 후 이 파일을 편집하여 도시를 추가/제거하세요 (형식: `{"city": "도시명", "timezone": "IANA/Timezone"}`). `--cities-file` 옵션으로 다른 JSON 파일을 지정할 수도 있습니다.
- **정렬**: 기본적으로 도시는 나열된 순서대로 표시됩니다. UTC 오프셋 순 (서→동)으로 정렬하려면 워크플로 YAML에서 `uv run` 명령에 `--sort-by-offset`를 추가하세요.
- **기타 옵션**: 추가 기능은 `timezone_table.py`를 참조하세요.

### 기술 스택
- Python + 내장 `zoneinfo`
- [**uv**](https://github.com/astral-sh/uv) – 빠른 Python 의존성 관리 도구
- GitHub Actions만으로 동작 – 별도 설정 불필요

포크, 스타, 또는 팀/조직 저장소에서 자유롭게 활용하세요!

분산 팀을 위해 ❤️를 담아 만들었습니다.

(xAI의 Grok 4의 도움을 받았습니다)
