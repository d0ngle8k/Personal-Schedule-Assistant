from __future__ import annotations
import os
import sqlite3
from datetime import date
from typing import List, Dict, Any

DB_FILE = "events.db"
DB_PATH = os.path.join(os.path.dirname(__file__), DB_FILE)
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")


class DatabaseManager:
    def __init__(self, db_path: str = DB_PATH) -> None:
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._create_table()

    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _create_table(self) -> None:
        with self._conn() as conn:
            with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())

    # CRUD
    def add_event(self, event_dict: Dict[str, Any]) -> None:
        sql = (
            "INSERT INTO events (event_name, start_time, end_time, location, reminder_minutes) "
            "VALUES (:event, :start_time, :end_time, :location, :reminder_minutes)"
        )
        with self._conn() as conn:
            conn.execute(sql, event_dict)

    def update_event(self, event_id: int, event_dict: Dict[str, Any]) -> None:
        sql = (
            "UPDATE events SET event_name=:event, start_time=:start_time, end_time=:end_time, "
            "location=:location, reminder_minutes=:reminder_minutes WHERE id=:id"
        )
        data = dict(event_dict)
        data['id'] = event_id
        with self._conn() as conn:
            conn.execute(sql, data)

    def delete_event(self, event_id: int) -> None:
        with self._conn() as conn:
            conn.execute("DELETE FROM events WHERE id=?", (event_id,))

    def get_events_by_date(self, date_obj: date) -> List[Dict[str, Any]]:
        date_str = date_obj.strftime('%Y-%m-%d')
        sql = "SELECT * FROM events WHERE DATE(start_time)=? ORDER BY start_time"
        with self._conn() as conn:
            cur = conn.execute(sql, (date_str,))
            return [dict(r) for r in cur.fetchall()]

    def get_all_events(self) -> List[Dict[str, Any]]:
        with self._conn() as conn:
            cur = conn.execute("SELECT * FROM events ORDER BY start_time")
            return [dict(r) for r in cur.fetchall()]

    def get_event_by_id(self, event_id: int) -> Dict[str, Any] | None:
        with self._conn() as conn:
            cur = conn.execute("SELECT * FROM events WHERE id=?", (event_id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def get_pending_reminders(self, now_iso: str) -> List[Dict[str, Any]]:
        sql = (
            "SELECT * FROM events WHERE start_time > ? AND status='pending' AND reminder_minutes > 0 "
            "ORDER BY start_time ASC"
        )
        with self._conn() as conn:
            cur = conn.execute(sql, (now_iso,))
            return [dict(r) for r in cur.fetchall()]

    def update_event_status(self, event_id: int, new_status: str) -> None:
        with self._conn() as conn:
            conn.execute("UPDATE events SET status=? WHERE id=?", (new_status, event_id))
