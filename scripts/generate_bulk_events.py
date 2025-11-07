"""Generate ~1000 valid Vietnamese scheduling prompts and insert them via NLP pipeline.

This script:
1. Builds a diverse set of events (meetings, study, exercise, social, errands, deadlines, travel, reminders optional).
2. Ensures all times are in the future (spreads across next 120 days).
3. Randomizes hour, minute, location pool, reminder choices.
4. Uses existing NLP pipeline to parse each prompt and database manager to insert.
5. Skips duplicates (time conflict) automatically (db_manager already handles) and counts successes vs duplicates vs parsing failures.
6. Prints summary statistics.

Usage (from project root):
    python scripts/generate_bulk_events.py

After running, launch UI (python main.py) and scroll to see how many rows render (limited to 1000 recent ± date range window).
"""
from __future__ import annotations
import random
from datetime import datetime, timedelta
import os
import sys
from pathlib import Path

# Ensure project root is on sys.path so we can import database, core_nlp, etc. when executed from scripts/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from database.db_manager import DatabaseManager

# Try hybrid first then fallback
try:
    from core_nlp.hybrid_pipeline import HybridNLPPipeline as ActivePipeline
    PIPELINE_MODE = 'hybrid'
except ImportError:
    try:
        from core_nlp.phobert_model import PhoBERTNLPPipeline as ActivePipeline
        PIPELINE_MODE = 'phobert'
    except ImportError:
        from core_nlp.pipeline import NLPPipeline as ActivePipeline
        PIPELINE_MODE = 'rule'

EVENT_ACTIONS = [
    "Họp dự án", "Họp nhóm", "Trao đổi sprint", "Review code", "Deploy phiên bản", "Ăn trưa",
    "Chạy bộ", "Tập gym", "Học tiếng Anh", "Học tiếng Nhật", "Học toán", "Ôn thi",
    "Đá bóng", "Xem phim", "Đi siêu thị", "Đi mua sắm", "Sinh nhật bạn", "Sinh nhật mẹ", "Gặp khách",
    "Gọi điện khách hàng", "Phỏng vấn", "Báo cáo tuần", "Nộp báo cáo tháng", "Kiểm thử hệ thống",
    "Dọn nhà", "Thăm bà ngoại", "Thăm ông nội", "Đi chơi", "Cafe với Minh", "Cafe với đối tác",
    "Gặp đối tác", "Họp phụ huynh", "Đưa con đi học", "Đi khám bệnh", "Đặt lịch nha sĩ",
    "Tư vấn dự án", "Pitch ý tưởng", "Kiểm tra sức khỏe", "Workshop nội bộ", "Workshop sản phẩm",
]

TIME_PREFIXES = ["", "lúc", "vào", "tầm", "khoảng"]
DAY_VARIANTS = ["hôm nay", "ngày mai", "mai", "tối mai", "sáng mai", "chiều mai", "thứ {} tuần sau", "CN tuần sau"]
# For weekday placeholders we will substitute numbers 2..7
WEEKDAY_MAP = {1: "CN", 2: "thứ 2", 3: "thứ 3", 4: "thứ 4", 5: "thứ 5", 6: "thứ 6", 7: "thứ 7"}
LOCATIONS = [
    "phòng họp 1", "phòng 302", "quán cà phê Trung Nguyên", "nhà", "công ty",
    "vincom", "sân A2", "nha khoa Paris", "công viên Thống Nhất", "California Fitness",
    "nhà hàng Hoàng Yến", "trường học", "bệnh viện Bạch Mai", "bể bơi Linh Đàm", "sân tập",
    "phòng lab", "văn phòng chính", "phòng họp 2", "phòng họp 3", "khu R&D"
]
REMINDER_CHOICES = [0, 5, 10, 15, 20, 30, 45, 60, 90, 120]

# Some explicit date patterns (ngày D tháng M) to diversify prompts
EXPLICIT_DATES_COUNT = 200  # subset using explicit date syntax
TOTAL_TARGET = 1000

random.seed(42)

def future_datetime_spread(idx: int) -> datetime:
    """Spread events across next 120 days deterministically with randomness."""
    base = datetime.now() + timedelta(days=idx % 120)
    # Random hour/minute
    hour = random.randint(7, 21)  # daytime to evening
    minute = random.choice([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
    dt = base.replace(hour=hour, minute=minute, second=0, microsecond=0)
    # Ensure strictly future
    if dt <= datetime.now():
        dt = datetime.now() + timedelta(hours=2)
    return dt


def build_prompt(idx: int, dt: datetime) -> str:
    action = random.choice(EVENT_ACTIONS)
    prefix = random.choice(TIME_PREFIXES)
    reminder = random.choice(REMINDER_CHOICES)
    loc = random.choice(LOCATIONS)

    # Decide style: explicit date vs relative
    use_explicit = idx < EXPLICIT_DATES_COUNT
    if use_explicit:
        # Explicit: "14h ngày 6 tháng 12" or with minutes
        h_fmt = dt.strftime("%Hh") if dt.minute == 0 else dt.strftime("%H:%M")
        prompt_time = f"{h_fmt} ngày {dt.day} tháng {dt.month}"
    else:
        # Relative patterns: choose from DAY_VARIANTS; handle weekday substitution
        # Map actual dt weekday to Vietnamese constructs sometimes
        weekday_num = dt.isoweekday()  # Monday=1..Sunday=7
        # Build a variant deterministically
        if idx % 5 == 0:
            # Use explicit weekday next week format
            target_wd = (weekday_num % 7) + 1
            prompt_time = f"{dt.strftime('%H:%M')} {WEEKDAY_MAP.get(target_wd, 'thứ 2')} tuần sau"
        elif idx % 5 == 1:
            prompt_time = f"{dt.strftime('%Hh')} sáng mai"
        elif idx % 5 == 2:
            prompt_time = f"{dt.strftime('%H:%M')} chiều mai"
        elif idx % 5 == 3:
            prompt_time = f"{dt.strftime('%Hh')} tối mai"
        else:
            prompt_time = f"{dt.strftime('%H:%M')} ngày mai"

    # Optional prefix
    if prefix:
        prompt = f"{action} {prefix} {prompt_time} tại {loc}"
    else:
        prompt = f"{action} {prompt_time} tại {loc}"

    # Append reminder sometimes (avoid always to diversify)
    if reminder and (idx % 3 != 0):
        # Variation of wording
        if idx % 2 == 0:
            prompt += f", nhắc trước {reminder} phút"
        else:
            prompt += f", nhắc sớm hơn {reminder} phút"

    return prompt


def main():
    print(f"🚀 Bulk generation started (mode={PIPELINE_MODE})")
    db = DatabaseManager()
    nlp = ActivePipeline() if PIPELINE_MODE != 'hybrid' else ActivePipeline(model_path=None)

    success = 0
    duplicates = 0
    parse_fail = 0
    total = TOTAL_TARGET
    sample_failed = []

    for idx in range(total):
        dt = future_datetime_spread(idx)
        prompt = build_prompt(idx, dt)
        try:
            result = nlp.process(prompt)
            if not result.get('event_name') or not result.get('start_time'):
                parse_fail += 1
                if len(sample_failed) < 5:
                    sample_failed.append((prompt, result))
                continue
            insert_res = db.add_event(result)
            if insert_res.get('success'):
                success += 1
            else:
                if insert_res.get('error') == 'duplicate_time':
                    duplicates += 1
                else:
                    parse_fail += 1
                    if len(sample_failed) < 5:
                        sample_failed.append((prompt, insert_res))
        except Exception as e:
            parse_fail += 1
            if len(sample_failed) < 5:
                sample_failed.append((prompt, str(e)))

        if (idx + 1) % 100 == 0:
            print(f"Progress: {idx+1}/{total} | OK={success} dup={duplicates} fail={parse_fail}")

    all_events = db.get_all_events()

    print("\n===== SUMMARY =====")
    print(f"Generated prompts: {total}")
    print(f"Inserted successfully: {success}")
    print(f"Duplicates (time conflict): {duplicates}")
    print(f"Parse/other failures: {parse_fail}")
    print(f"Total events now in DB: {len(all_events)}")
    if sample_failed:
        print("\nSample failures (up to 5):")
        for p, r in sample_failed:
            print(f"- PROMPT: {p}\n  RESULT: {r}")
    print("===================")

if __name__ == '__main__':
    main()
