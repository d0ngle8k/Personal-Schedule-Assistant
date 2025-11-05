CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_name TEXT NOT NULL,
    start_time TEXT NOT NULL,       -- Lưu trữ dưới dạng chuỗi ISO 8601
    end_time TEXT,                  -- Cho phép NULL (theo Image 2)
    location TEXT,
    reminder_minutes INTEGER DEFAULT 0,
    status TEXT NOT NULL DEFAULT 'pending' -- Dùng cho hệ thống nhắc nhở ('pending', 'notified')
);

-- Performance Indexes (created if not exists)
CREATE INDEX IF NOT EXISTS idx_events_start_time ON events(start_time);
CREATE INDEX IF NOT EXISTS idx_events_status ON events(status);
CREATE INDEX IF NOT EXISTS idx_events_date ON events(DATE(start_time));
