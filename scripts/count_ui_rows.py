"""Count how many events the UI would load on startup.

This mimics Application._load_today logic WITHOUT launching the Tk mainloop to avoid blocking.
It fetches events in range (today-30 .. today+60) and applies the same 1000 item cap.

Usage:
    python scripts/count_ui_rows.py
"""
from datetime import date, timedelta
import sys
from pathlib import Path

# Ensure project root on sys.path for import
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.db_manager import DatabaseManager

def main():
    db = DatabaseManager()
    today = date.today()
    start_date = today - timedelta(days=30)
    end_date = today + timedelta(days=60)
    events = db.get_events_by_date_range(start_date, end_date)
    capped = events[:1000]
    print(f"Events in date window (-30/+60 days): {len(events)}")
    print(f"Rows UI will display (capped to 1000): {len(capped)}")
    if len(events) > 1000:
        print("NOTE: Some events won't show until you narrow the date range or search.")

if __name__ == '__main__':
    main()
