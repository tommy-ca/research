#!/usr/bin/env python3
"""
Create/open today's daily note at vault/daily/YYYY/MM-month/YYYY-MM-DD.md
Using template vault/templates/daily-note.md if available.
"""
from pathlib import Path
from datetime import date
import calendar
import sys

REPO_ROOT = Path(__file__).resolve().parents[1]
VAULT = REPO_ROOT / "vault"

def month_dir(today: date) -> str:
    month_name = calendar.month_name[today.month].lower()
    return f"{today:%m}-{month_name}"

def ensure_daily(today: date | None = None) -> Path:
    today = today or date.today()
    day_name = f"{today:%Y-%m-%d}.md"
    path = VAULT / "daily" / f"{today:%Y}" / month_dir(today)
    path.mkdir(parents=True, exist_ok=True)
    note_path = path / day_name

    if not note_path.exists():
        template = VAULT / "templates" / "daily-note.md"
        if template.exists():
            content = template.read_text(encoding="utf-8")
        else:
            content = (
                "---\n"
                f"date: {today:%Y-%m-%d}\n"
                "type: daily\n"
                "tags: [daily]\n"
                "status: active\n"
                "links: []\n"
                "---\n\n"
                f"# Daily Note - {today:%Y-%m-%d}\n\n"
            )
        note_path.write_text(content, encoding="utf-8")
    return note_path


def main() -> int:
    p = ensure_daily()
    print(str(p))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
