from __future__ import annotations
import os
import sys
import sqlite3
from datetime import date
from typing import List, Dict, Any
import threading
from queue import Queue, Empty

DB_FILE = "events.db"

def _writable_base_dir() -> str:
    """Return a writable base dir for DB when running normally or as a frozen exe.
    - In dev: use the module directory (database/)
    - In frozen exe: use a 'database' folder next to the executable
    """
    if getattr(sys, 'frozen', False):  # PyInstaller onefile
        exe_dir = os.path.dirname(sys.executable)
        base = os.path.join(exe_dir, 'database')
    else:
        base = os.path.dirname(__file__)
    os.makedirs(base, exist_ok=True)
    return base


def _schema_file_path() -> str:
    """Locate schema.sql both in dev and in PyInstaller runtime.
    In frozen mode, data files are extracted under sys._MEIPASS.
    """
    # Prefer packaged resource under _MEIPASS when frozen
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        candidate = os.path.join(sys._MEIPASS, 'database', 'schema.sql')
        if os.path.exists(candidate):
            return candidate
    # Fallback to local file next to this module
    return os.path.join(os.path.dirname(__file__), 'schema.sql')


DB_PATH = os.path.join(_writable_base_dir(), DB_FILE)
SCHEMA_PATH = _schema_file_path()


class DatabaseManager:
    """
    Database manager with connection pooling for better multithreading performance
    """
    # Connection pool settings
    MAX_POOL_SIZE = 10
    POOL_TIMEOUT = 5.0
    
    def __init__(self, db_path: str = DB_PATH) -> None:
        self.db_path = db_path
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        # Connection pool for thread-safe access
        self._connection_pool = Queue(maxsize=self.MAX_POOL_SIZE)
        self._pool_lock = threading.Lock()
        self._pool_size = 0
        
        # Initialize connection pool with 3 connections
        for _ in range(3):
            self._create_connection()
        
        self._create_table()

    def _create_connection(self) -> None:
        """Create a new connection and add to pool"""
        with self._pool_lock:
            if self._pool_size < self.MAX_POOL_SIZE:
                conn = sqlite3.connect(
                    self.db_path,
                    check_same_thread=False,  # Allow multithreading
                    timeout=30.0  # Long timeout for busy database
                )
                conn.row_factory = sqlite3.Row
                # Enable WAL mode for better concurrent access
                conn.execute("PRAGMA journal_mode=WAL")
                conn.execute("PRAGMA synchronous=NORMAL")
                self._connection_pool.put(conn)
                self._pool_size += 1

    def _get_connection(self) -> sqlite3.Connection:
        """Get connection from pool (or create new if pool empty)"""
        try:
            # Try to get from pool with timeout
            conn = self._connection_pool.get(timeout=self.POOL_TIMEOUT)
            return conn
        except Empty:
            # Pool exhausted, create new connection if under limit
            with self._pool_lock:
                if self._pool_size < self.MAX_POOL_SIZE:
                    conn = sqlite3.connect(
                        self.db_path,
                        check_same_thread=False,
                        timeout=30.0
                    )
                    conn.row_factory = sqlite3.Row
                    conn.execute("PRAGMA journal_mode=WAL")
                    conn.execute("PRAGMA synchronous=NORMAL")
                    self._pool_size += 1
                    return conn
                else:
                    # Wait longer for available connection
                    return self._connection_pool.get(timeout=30.0)

    def _return_connection(self, conn: sqlite3.Connection) -> None:
        """Return connection to pool"""
        try:
            self._connection_pool.put_nowait(conn)
        except:
            # Pool full, close connection
            conn.close()
            with self._pool_lock:
                self._pool_size -= 1

    def _conn(self) -> sqlite3.Connection:
        """Legacy method for backward compatibility - returns pooled connection"""
        return self._get_connection()
    
    class _PooledConnection:
        """Context manager for pooled connections"""
        def __init__(self, manager):
            self.manager = manager
            self.conn = None
        
        def __enter__(self):
            self.conn = self.manager._get_connection()
            return self.conn
        
        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.conn:
                if exc_type is None:
                    self.conn.commit()
                else:
                    self.conn.rollback()
                self.manager._return_connection(self.conn)

    def _create_table(self) -> None:
        """Create database table from schema.sql if not exists."""
        # Ensure schema file exists
        if not os.path.exists(SCHEMA_PATH):
            raise FileNotFoundError(
                f"Schema file not found: {SCHEMA_PATH}\n"
                f"frozen={getattr(sys, 'frozen', False)}, "
                f"_MEIPASS={getattr(sys, '_MEIPASS', 'NOT SET')}"
            )
        
        with self._PooledConnection(self) as conn:
            with open(SCHEMA_PATH, 'r', encoding='utf-8') as f:
                conn.executescript(f.read())

    # CRUD
    def add_event(self, event_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a new event to the database.
        
        Returns:
            Dict with 'success': bool and optional 'error': str or 'duplicates': List
        """
        # Check for time conflict
        start_time = event_dict.get('start_time')
        
        if start_time:
            duplicates = self.check_duplicate_time(start_time)
            if duplicates:
                return {
                    'success': False,
                    'error': 'duplicate_time',
                    'duplicates': duplicates
                }
        
        sql = (
            "INSERT INTO events (event_name, start_time, end_time, location, reminder_minutes) "
            "VALUES (:event_name, :start_time, :end_time, :location, :reminder_minutes)"
        )
        
        # Pass event_dict directly - validation should be done by caller
        # event_name must not be None or empty - caller must validate
        try:
            with self._PooledConnection(self) as conn:
                conn.execute(sql, event_dict)
            return {'success': True}
        except sqlite3.IntegrityError as e:
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': 'integrity_error',
                'message': str(e)
            }
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': 'unexpected_error',
                'message': str(e)
            }

    def update_event(self, event_id: int, event_dict: Dict[str, Any]) -> Dict[str, Any]:
        """
        Update an existing event.
        
        Returns:
            Dict with 'success': bool and optional 'error': str or 'duplicates': List
        """
        # Check for time conflict (excluding current event)
        start_time = event_dict.get('start_time')
        if start_time:
            duplicates = self.check_duplicate_time(start_time, exclude_id=event_id)
            if duplicates:
                return {
                    'success': False,
                    'error': 'duplicate_time',
                    'duplicates': duplicates
                }
        
        sql = (
            "UPDATE events SET event_name=:event_name, start_time=:start_time, end_time=:end_time, "
            "location=:location, reminder_minutes=:reminder_minutes WHERE id=:id"
        )
        data = dict(event_dict)
        data['id'] = event_id
        try:
            with self._PooledConnection(self) as conn:
                conn.execute(sql, data)
            return {'success': True}
        except sqlite3.IntegrityError as e:
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': 'integrity_error',
                'message': str(e)
            }

    def delete_event(self, event_id: int) -> None:
        with self._PooledConnection(self) as conn:
            conn.execute("DELETE FROM events WHERE id=?", (event_id,))
            # Check if all events are deleted, if so reset the AUTOINCREMENT counter
            cur = conn.execute("SELECT COUNT(*) FROM events")
            count = cur.fetchone()[0]
            if count == 0:
                # Reset the sqlite_sequence table to restart ID from 1
                conn.execute("DELETE FROM sqlite_sequence WHERE name='events'")

    def delete_all_events(self) -> int:
        """
        Delete all events from the database.
        
        Returns:
            int: Number of events deleted
        """
        with self._PooledConnection(self) as conn:
            # Count events before deletion
            cur = conn.execute("SELECT COUNT(*) FROM events")
            count = cur.fetchone()[0]
            
            # Delete all events
            conn.execute("DELETE FROM events")
            
            # Reset the AUTOINCREMENT counter
            conn.execute("DELETE FROM sqlite_sequence WHERE name='events'")
            
            return count

    def get_events_by_date(self, date_obj: date) -> List[Dict[str, Any]]:
        date_str = date_obj.strftime('%Y-%m-%d')
        sql = "SELECT * FROM events WHERE DATE(start_time)=? ORDER BY start_time"
        conn = self._get_connection()
        try:
            cur = conn.execute(sql, (date_str,))
            results = [dict(r) for r in cur.fetchall()]
            return results
        finally:
            self._return_connection(conn)
    
    def get_events_by_date_range(self, start_date: date, end_date: date) -> List[Dict[str, Any]]:
        """
        Get all events within a date range using optimized SQL query.
        
        Args:
            start_date: Start date (inclusive)
            end_date: End date (inclusive)
            
        Returns:
            List of event dictionaries
        """
        start_str = start_date.strftime('%Y-%m-%d')
        end_str = end_date.strftime('%Y-%m-%d')
        
        # Use BETWEEN for efficient range query
        sql = """
            SELECT * FROM events 
            WHERE DATE(start_time) BETWEEN ? AND ?
            ORDER BY start_time
        """
        
        conn = self._get_connection()
        try:
            cur = conn.execute(sql, (start_str, end_str))
            results = [dict(r) for r in cur.fetchall()]
            return results
        finally:
            self._return_connection(conn)

    def get_all_events(self) -> List[Dict[str, Any]]:
        conn = self._get_connection()
        try:
            cur = conn.execute("SELECT * FROM events ORDER BY start_time")
            results = [dict(r) for r in cur.fetchall()]
            return results
        finally:
            self._return_connection(conn)

    def get_event_by_id(self, event_id: int) -> Dict[str, Any] | None:
        conn = self._get_connection()
        try:
            cur = conn.execute("SELECT * FROM events WHERE id=?", (event_id,))
            row = cur.fetchone()
            return dict(row) if row else None
        finally:
            self._return_connection(conn)

    def get_pending_reminders(self) -> List[Dict[str, Any]]:
        """
        Lấy tất cả sự kiện chưa được thông báo hoàn toàn (status IN ('pending','reminded')).
        Không lọc theo thời gian để đảm bảo:
          - Sự kiện sắp diễn ra sẽ được nhắc trước nếu đủ điều kiện.
          - Sự kiện đã tới giờ (hoặc trễ nhẹ) nhưng app mới mở vẫn sẽ được thông báo "đúng giờ" ngay lần kiểm tra kế tiếp.
        """
        sql = (
            "SELECT * FROM events WHERE status IN ('pending', 'reminded') "
            "ORDER BY start_time ASC"
        )
        conn = self._get_connection()
        try:
            cur = conn.execute(sql)
            results = [dict(r) for r in cur.fetchall()]
            return results
        finally:
            self._return_connection(conn)

    def update_event_status(self, event_id: int, new_status: str) -> None:
        with self._PooledConnection(self) as conn:
            conn.execute("UPDATE events SET status=? WHERE id=?", (new_status, event_id))

    # --- Search helpers ---
    def search_events_by_id(self, event_id: int) -> List[Dict[str, Any]]:
        ev = self.get_event_by_id(event_id)
        return [ev] if ev else []

    def search_events_by_name(self, keyword: str) -> List[Dict[str, Any]]:
        kw = (keyword or '').strip().lower()
        if not kw:
            return []
        like = f"%{kw}%"
        sql = "SELECT * FROM events WHERE LOWER(event_name) LIKE ? ORDER BY start_time"
        conn = self._get_connection()
        try:
            cur = conn.execute(sql, (like,))
            results = [dict(r) for r in cur.fetchall()]
            return results
        finally:
            self._return_connection(conn)

    def search_events_by_location(self, keyword: str) -> List[Dict[str, Any]]:
        kw = (keyword or '').strip().lower()
        if not kw:
            return []
        like = f"%{kw}%"
        sql = "SELECT * FROM events WHERE location IS NOT NULL AND LOWER(location) LIKE ? ORDER BY start_time"
        conn = self._get_connection()
        try:
            cur = conn.execute(sql, (like,))
            results = [dict(r) for r in cur.fetchall()]
            return results
        finally:
            self._return_connection(conn)

    # --- Duplicate checking helpers ---
    def check_duplicate_time(self, start_time_iso: str, exclude_id: int = None) -> List[Dict[str, Any]]:
        """
        Check if there's already an event at the exact same time (date + hour + minute).
        Used to prevent scheduling conflicts.
        
        Args:
            start_time_iso: ISO 8601 datetime string (e.g., "2025-11-06T10:00:00")
            exclude_id: Optional event ID to exclude from check (for updates)
            
        Returns:
            List of conflicting events (empty if no duplicates)
        """
        # Extract date and time components (YYYY-MM-DD HH:MM)
        if not start_time_iso or len(start_time_iso) < 16:
            return []
        
        datetime_key = start_time_iso[:16]  # "2025-11-06T10:00"
        
        # Check for events with same date-time (ignoring seconds)
        sql = """
            SELECT * FROM events 
            WHERE substr(start_time, 1, 16) = ?
        """
        params = [datetime_key]
        
        if exclude_id is not None:
            sql += " AND id != ?"
            params.append(exclude_id)
        
        conn = self._get_connection()
        try:
            cur = conn.execute(sql, params)
            results = [dict(r) for r in cur.fetchall()]
            return results
        finally:
            self._return_connection(conn)
    
    def close_pool(self):
        """Close all connections in pool (call on app shutdown)"""
        with self._pool_lock:
            while not self._connection_pool.empty():
                try:
                    conn = self._connection_pool.get_nowait()
                    conn.close()
                except:
                    pass
            self._pool_size = 0
            print(f"🔒 Database connection pool closed")
