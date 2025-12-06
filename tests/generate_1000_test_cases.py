#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Generate 1000 comprehensive test cases for Hybrid NLP Pipeline
Covers: Normal cases, Edge cases, Stress tests, Vietnamese variations
"""

import json
from datetime import datetime, timedelta
import random

def generate_test_cases():
    """Generate 1000 diverse test cases"""
    cases = []
    
    # =========================================================================
    # CATEGORY 1: NORMAL CASES (300 cases)
    # =========================================================================
    
    # Basic events with common patterns
    normal_events = [
        "họp", "họp nhóm", "họp team", "họp dự án", "họp khách hàng",
        "gặp", "gặp khách", "gặp bạn", "gặp đối tác", "gặp sếp",
        "học", "học bài", "học online", "học tiếng anh", "học python",
        "đi", "đi chợ", "đi siêu thị", "đi khám", "đi công tác",
        "ăn", "ăn trưa", "ăn tối", "ăn sáng", "ăn cơm",
        "tập", "tập gym", "tập yoga", "tập thể dục", "chạy bộ",
        "xem", "xem phim", "xem bóng đá", "xem tivi",
        "làm", "làm việc", "làm bài tập", "làm báo cáo",
        "đọc", "đọc sách", "đọc báo", "đọc báo cáo",
        "viết", "viết báo cáo", "viết code", "viết email"
    ]
    
    times = [
        "8h sáng mai", "9:00 sáng mai", "10h30 sáng mai",
        "14h chiều nay", "15:30 chiều mai", "16h chiều mai",
        "18h tối nay", "19:30 tối mai", "20h tối mai",
        "lúc 8h", "lúc 10:30", "lúc 14h", "lúc 18h30",
        "vào 9h sáng", "vào 15h chiều", "vào 20h tối"
    ]
    
    locations = [
        "phòng 302", "văn phòng", "nhà hàng", "quán cafe", 
        "bệnh viện", "trường học", "công ty", "sân bay",
        "bưu điện", "ngân hàng", "siêu thị", "chợ"
    ]
    
    # Generate 300 normal cases
    for i in range(300):
        event = random.choice(normal_events)
        time = random.choice(times)
        loc = random.choice(locations) if random.random() > 0.3 else None
        
        if loc:
            prompt = f"{event} {time} tại {loc}"
        else:
            prompt = f"{event} {time}"
        
        cases.append({
            "id": f"normal_{i+1}",
            "input": prompt,
            "category": "normal",
            "expected_fields": ["event_name", "start_time"]
        })
    
    # =========================================================================
    # CATEGORY 2: EDGE CASES - Time Formats (150 cases)
    # =========================================================================
    
    edge_times = [
        # Ambiguous times
        ("sáng mai", "morning_ambiguous"),
        ("chiều nay", "afternoon_ambiguous"),
        ("tối mai", "evening_ambiguous"),
        ("trưa nay", "noon_ambiguous"),
        
        # Multiple time references
        ("8h đến 10h sáng mai", "time_range"),
        ("từ 14h đến 16h chiều nay", "time_range"),
        
        # Relative dates
        ("ngày mốt", "day_after_tomorrow"),
        ("ngày kia", "three_days_later"),
        ("tuần sau", "next_week"),
        ("tuần tới", "next_week_variant"),
        ("tháng sau", "next_month"),
        
        # Day of week
        ("thứ 2 tuần sau", "next_monday"),
        ("thứ 3 tuần này", "this_tuesday"),
        ("thứ 4 tuần tới", "next_wednesday"),
        ("thứ 5", "thursday"),
        ("thứ 6", "friday"),
        ("thứ 7", "saturday"),
        ("chủ nhật", "sunday"),
        ("cn tuần sau", "next_sunday"),
        
        # Abbreviated formats
        ("t2", "monday_abbr"),
        ("t3", "tuesday_abbr"),
        ("t4", "wednesday_abbr"),
        ("cn", "sunday_abbr"),
        
        # Edge hour times
        ("0h đêm nay", "midnight"),
        ("23:59 tối nay", "almost_midnight"),
        ("12h trưa", "noon"),
        ("6h sáng", "early_morning"),
        
        # Mixed formats
        ("10h30 sáng ngày 15", "date_with_time"),
        ("14:45 chiều thứ 2", "time_with_dow"),
    ]
    
    for i, (time_str, time_type) in enumerate(edge_times * 5):  # Repeat to get 150
        if i >= 150:
            break
        event = random.choice(["họp", "gặp khách", "học bài", "làm việc"])
        cases.append({
            "id": f"edge_time_{i+1}",
            "input": f"{event} {time_str}",
            "category": "edge_time",
            "time_type": time_type,
            "expected_fields": ["event_name", "start_time"]
        })
    
    # =========================================================================
    # CATEGORY 3: EDGE CASES - Event Names (150 cases)
    # =========================================================================
    
    edge_events = [
        # Very short events
        ("đi", "single_word"),
        ("ăn", "single_word"),
        ("học", "single_word"),
        
        # Long compound events
        ("họp ban giám đốc công ty", "long_compound"),
        ("tham gia buổi hội thảo khoa học", "long_compound"),
        ("đi khám sức khỏe định kỳ", "long_compound"),
        
        # Events with numbers
        ("họp lần 2", "event_with_number"),
        ("sprint planning số 5", "event_with_number"),
        ("review tuần 3", "event_with_number"),
        
        # Events with special chars (should be cleaned)
        ("họp + gặp khách", "event_with_special"),
        ("học & làm bài tập", "event_with_special"),
        
        # Capitalized variations
        ("HỌP NHÓM", "all_caps"),
        ("Gặp Khách Hàng", "title_case"),
        
        # Mixed Vietnamese tones
        ("hop nhom", "no_tones"),
        ("hoc bai", "no_tones"),
        
        # Events that look like time words
        ("ăn trưa", "event_contains_time_word"),
        ("ăn sáng", "event_contains_time_word"),
        ("họp sáng", "event_contains_time_word"),
    ]
    
    for i, (event, event_type) in enumerate(edge_events * 10):
        if i >= 150:
            break
        time = random.choice(["10h sáng mai", "14h chiều nay", "18h tối mai"])
        cases.append({
            "id": f"edge_event_{i+1}",
            "input": f"{event} {time}",
            "category": "edge_event",
            "event_type": event_type,
            "expected_fields": ["event_name", "start_time"]
        })
    
    # =========================================================================
    # CATEGORY 4: EDGE CASES - Locations (100 cases)
    # =========================================================================
    
    edge_locations = [
        # Very specific locations
        ("phòng 302 tòa A", "specific_room"),
        ("bệnh viện Bạch Mai khoa nội", "hospital_department"),
        ("quán cafe Trung Nguyên chi nhánh 1", "chain_location"),
        
        # Locations with special chars
        ("văn phòng ABC & Associates", "location_with_special"),
        
        # No location marker
        ("công ty", "implicit_location"),
        ("nhà", "implicit_location"),
        ("trường", "implicit_location"),
        
        # Multiple locations (ambiguous)
        ("phòng 302 hoặc phòng 303", "multiple_locations"),
        
        # Location in event name (should be separated)
        ("họp công ty", "location_in_event"),
        ("học trường", "location_in_event"),
    ]
    
    for i, (loc, loc_type) in enumerate(edge_locations * 10):
        if i >= 100:
            break
        event = random.choice(["họp", "gặp", "học"])
        time = random.choice(["10h sáng mai", "14h chiều nay"])
        cases.append({
            "id": f"edge_location_{i+1}",
            "input": f"{event} {time} tại {loc}",
            "category": "edge_location",
            "location_type": loc_type,
            "expected_fields": ["event_name", "start_time", "location"]
        })
    
    # =========================================================================
    # CATEGORY 5: EDGE CASES - Reminders (50 cases)
    # =========================================================================
    
    reminder_patterns = [
        ("nhắc trước 5 phút", 5),
        ("nhắc trước 10 phút", 10),
        ("nhắc trước 15 phút", 15),
        ("nhắc trước 30 phút", 30),
        ("nhắc trước 1 giờ", 60),
        ("nhắc trước 2 giờ", 120),
        ("nhắc sớm hơn 30 phút", 30),
        ("nhắc sớm hơn 1 tiếng", 60),
        ("nhac truoc 15 phut", 15),  # No tones
        ("nhắc tôi trước 20 phút", 20),
    ]
    
    for i, (reminder, minutes) in enumerate(reminder_patterns * 5):
        if i >= 50:
            break
        event = random.choice(["họp", "gặp khách", "phỏng vấn"])
        time = random.choice(["9h sáng mai", "14h chiều nay"])
        cases.append({
            "id": f"edge_reminder_{i+1}",
            "input": f"{event} {time}, {reminder}",
            "category": "edge_reminder",
            "expected_reminder": minutes,
            "expected_fields": ["event_name", "start_time", "reminder_minutes"]
        })
    
    # =========================================================================
    # CATEGORY 6: STRESS TESTS - Very Long Inputs (50 cases)
    # =========================================================================
    
    for i in range(50):
        # Very long event descriptions
        long_event = " ".join(random.choices([
            "họp", "bàn", "về", "dự án", "phát triển", "sản phẩm",
            "mới", "cho", "khách hàng", "quan trọng", "tại", "công ty"
        ], k=15))
        
        time = random.choice(["10h sáng mai", "14h chiều nay"])
        
        cases.append({
            "id": f"stress_long_{i+1}",
            "input": f"{long_event} {time}",
            "category": "stress_long",
            "expected_fields": ["event_name", "start_time"]
        })
    
    # =========================================================================
    # CATEGORY 7: STRESS TESTS - Missing Information (50 cases)
    # =========================================================================
    
    # Missing time
    for i in range(15):
        event = random.choice(normal_events)
        cases.append({
            "id": f"stress_no_time_{i+1}",
            "input": event,
            "category": "stress_missing",
            "missing": "time",
            "should_fail": True
        })
    
    # Missing event (only time)
    for i in range(15):
        time = random.choice(["10h sáng mai", "14h chiều nay", "lúc 8h"])
        cases.append({
            "id": f"stress_no_event_{i+1}",
            "input": time,
            "category": "stress_missing",
            "missing": "event",
            "should_fail": True
        })
    
    # Very minimal input
    for i in range(20):
        minimal = random.choice([
            "họp mai",
            "gặp nay",
            "học tối",
            "đi sáng",
            "ăn trưa"
        ])
        cases.append({
            "id": f"stress_minimal_{i+1}",
            "input": minimal,
            "category": "stress_minimal",
            "expected_fields": ["event_name", "start_time"]
        })
    
    # =========================================================================
    # CATEGORY 8: STRESS TESTS - Typos & Variations (50 cases)
    # =========================================================================
    
    typo_patterns = [
        ("hpo nhom", "họp nhóm"),  # typo
        ("gapp khach", "gặp khách"),  # typo
        ("hoc bai", "học bài"),  # missing tones
        ("an trua", "ăn trưa"),  # missing tones
        ("10h sang mai", "10h sáng mai"),  # typo in time
        ("14h chieu nay", "14h chiều nay"),  # missing tones
    ]
    
    for i, (typo_input, correct) in enumerate(typo_patterns * 9):
        if i >= 50:
            break
        cases.append({
            "id": f"stress_typo_{i+1}",
            "input": typo_input,
            "category": "stress_typo",
            "note": f"Should handle typo/variation of: {correct}"
        })
    
    # =========================================================================
    # CATEGORY 9: REAL WORLD EXAMPLES (50 cases)
    # =========================================================================
    
    real_world = [
        "Họp nhóm lúc 10h sáng mai ở phòng 302, nhắc trước 15 phút",
        "Đi khám bệnh 8:30 ngày mai tại bệnh viện Bạch Mai",
        "Gặp khách 14h ngày 15 tháng 12 tại quán cà phê Trung Nguyên",
        "Sinh nhật mẹ tối mai ở nhà",
        "Học tiếng Anh 18:00 thứ 2 tuần sau",
        "Đá bóng 17h30 hôm nay tại sân A2",
        "Phỏng vấn 9 giờ sáng mai, nhắc sớm hơn 1 giờ",
        "Nộp báo cáo cuối tuần ở công ty",
        "Mua sắm 19:00 hôm nay tại Vincom",
        "Cafe với Minh lúc 15h ngày mai",
        "Họp dự án 10 giờ 30 phút ngày mai tại phòng họp 1",
        "Chạy bộ 6h sáng mai ở công viên Thống Nhất",
        "Xem phim 20:15 hôm nay",
        "Dọn nhà chiều mai",
        "Học online 21h hôm nay tại phòng 101",
        "Đưa con đi học 7:00 ngày mai",
        "Thăm bà ngoại lúc 16 giờ thứ 7 tuần sau",
        "Tập gym 18h hôm nay ở California Fitness",
        "Họp online 9h sáng mai nhắc trước 30 phút",
        "Đi chợ 8 giờ sáng mai",
    ]
    
    for i, prompt in enumerate(real_world * 3):
        if i >= 50:
            break
        cases.append({
            "id": f"real_world_{i+1}",
            "input": prompt,
            "category": "real_world",
            "expected_fields": ["event_name", "start_time"]
        })
    
    # =========================================================================
    # CATEGORY 10: BOUNDARY TESTS (50 cases)
    # =========================================================================
    
    # Very early/late times
    boundary_times = ["0h", "1h", "2h", "3h", "22h", "23h", "23:59"]
    for i, time in enumerate(boundary_times * 7):
        if i >= 25:
            break
        event = random.choice(["học", "làm việc", "họp"])
        cases.append({
            "id": f"boundary_time_{i+1}",
            "input": f"{event} {time}",
            "category": "boundary",
            "boundary_type": "extreme_hours"
        })
    
    # Empty/whitespace
    for i in range(10):
        cases.append({
            "id": f"boundary_empty_{i+1}",
            "input": "   ",
            "category": "boundary",
            "boundary_type": "empty_input",
            "should_fail": True
        })
    
    # Very short
    for i in range(15):
        short_input = random.choice(["h", "g", "đ", "12", "ab"])
        cases.append({
            "id": f"boundary_short_{i+1}",
            "input": short_input,
            "category": "boundary",
            "boundary_type": "too_short",
            "should_fail": True
        })
    
    return cases

def main():
    print("🔧 Generating 1000 comprehensive test cases...")
    
    cases = generate_test_cases()
    
    # Verify count
    print(f"✅ Generated {len(cases)} test cases")
    
    # Count by category
    categories = {}
    for case in cases:
        cat = case.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📊 Test Cases by Category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat:20s}: {count:4d} cases")
    
    # Save to JSON
    output_file = "tests/hybrid_test_1000_cases.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cases, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Saved to: {output_file}")
    print(f"📦 File size: {len(json.dumps(cases, ensure_ascii=False))} bytes")
    
    # Sample cases
    print("\n📝 Sample Cases:")
    for i in range(5):
        case = cases[i]
        print(f"  [{i+1}] {case['category']:15s}: {case['input']}")

if __name__ == "__main__":
    main()
