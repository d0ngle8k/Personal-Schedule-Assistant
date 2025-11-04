from __future__ import annotations
import json
from typing import Any
from ics import Calendar, Event
from datetime import datetime


def export_to_json(db_manager, filepath: str = 'schedule_export.json') -> None:
    all_events = db_manager.get_all_events()
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(all_events, f, ensure_ascii=False, indent=2)


def export_to_ics(db_manager, filepath: str = 'schedule_export.ics') -> None:
    all_events = db_manager.get_all_events()
    cal = Calendar()
    for ev in all_events:
        e = Event()
        e.name = ev.get('event_name')
        st = ev.get('start_time')
        if st:
            try:
                e.begin = datetime.fromisoformat(st)
            except Exception:
                pass
        e.location = ev.get('location') or None
        cal.events.add(e)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(cal.serialize())
