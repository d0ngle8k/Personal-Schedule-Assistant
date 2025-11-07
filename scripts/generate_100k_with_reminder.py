"""
Generate 100K+ COMPREHENSIVE training data for PhoBERT fine-tuning
Focus: ALL edge cases + Week/Month reminders + Special patterns
Version: 1.0 - Complete coverage
"""

import json
import random
from datetime import datetime, timedelta

# Vietnamese word mappings - EXPANDED
WEEKDAYS = {
    'full': ['thứ hai', 'thứ ba', 'thứ tư', 'thứ năm', 'thứ sáu', 'thứ bảy', 'chủ nhật'],
    'short': ['t2', 't3', 't4', 't5', 't6', 't7', 'cn'],
    'no_diacritic': ['thu hai', 'thu ba', 'thu tu', 'thu nam', 'thu sau', 'thu bay', 'chu nhat'],
    'typo_h': ['thứ haih', 'thứ bah', 'thứ tuh', 'thứ namh', 'thứ sauh', 'thứ bayh'],
    'extreme_typo': ['thur hai', 'thua ba', 'thuw tu', 'thuu nam', 'thux sau', 'thuy bay'],
    'variant': ['thứ 2', 'thứ 3', 'thứ 4', 'thứ 5', 'thứ 6', 'thứ 7', 'chúa nhật'],
}

NUMBERS = {
    'digit': list(range(1, 25)),
    'word': ['một', 'hai', 'ba', 'bốn', 'năm', 'sáu', 'bảy', 'tám', 'chín', 'mười', 'mười một', 'mười hai'],
    'no_diacritic': ['mot', 'hai', 'ba', 'bon', 'nam', 'sau', 'bay', 'tam', 'chin', 'muoi', 'muoi mot', 'muoi hai'],
    'typo_h': ['moth', 'haih', 'bah', 'bonh', 'namh', 'sauh', 'bayh', 'tamh', 'chinh', 'muoih'],
    'extreme_typo': ['moat', 'hhai', 'baa', 'bown', 'naem', 'xau', 'byay', 'taam', 'chien', 'muuoi'],
}

PERIODS = {
    'full': ['sáng', 'trưa', 'chiều', 'tối', 'đêm', 'khuya'],
    'no_diacritic': ['sang', 'trua', 'chieu', 'toi', 'dem', 'khuya'],
    'short': ['s', 'tr', 'ch', 't', 'd'],
    'variant': ['buổi sáng', 'buổi trưa', 'buổi chiều', 'buổi tối'],
}

EVENTS = [
    # Work events
    'họp nhóm', 'họp team', 'họp khách', 'họp ban giám đốc', 'họp dự án',
    'đi làm', 'làm việc', 'làm báo cáo', 'làm bài tập', 'nộp hồ sơ', 'ký hợp đồng', 'phỏng vấn',
    'training', 'seminar', 'workshop', 'presentation',
    # Personal events
    'đi học', 'đi khám bệnh', 'đi chợ', 'đi cafe', 'đi ăn', 'đi du lịch',
    'gặp bạn', 'gặp khách', 'gặp đối tác', 'gặp gia đình',
    'ăn sáng', 'ăn trưa', 'ăn tối', 'ăn nhẹ', 'ăn buffet',
    # Sports & Hobbies
    'chạy bộ', 'tập gym', 'đá bóng', 'bơi lội', 'chơi tennis', 'yoga',
    'xem phim', 'nghe nhạc', 'đọc sách', 'chơi game',
    # Special events
    'sinh nhật', 'kỷ niệm', 'tiệc tùng', 'đám cưới', 'lễ hội',
    'cắt tóc', 'làm nail', 'spa', 'massage',
    'học lái xe', 'thi bằng lái', 'đăng kiểm xe',
]

LOCATIONS = [
    # Office/Work
    'văn phòng', 'công ty', 'phòng họp', 'tầng 5', 'phòng 302', 'toà A', 'khu B',
    # Education
    'trường học', 'thư viện', 'lớp học', 'giảng đường',
    # Public places
    'bệnh viện', 'nhà hàng', 'quán cafe', 'siêu thị', 'chợ', 'công viên', 'sân bay',
    'rạp chiếu phim', 'trung tâm thương mại', 'khách sạn',
    # Cities
    'Hà Nội', 'Sài Gòn', 'Đà Nẵng', 'Hải Phòng', 'Cần Thơ',
    # Specific
    'Starbucks', 'Highlands Coffee', '30 Shines', 'Lotteria', 'KFC',
    'số 123 đường ABC', 'ngõ 45', 'quận 1', 'quận 3',
]

RELATIVE_TIME = [
    'hôm nay', 'ngày mai', 'ngày kia', 'mai', 'mốt', 'hôm qua',
    'tuần sau', 'tuần tới', 'tuần này', 'tháng sau', 'tháng tới', 'năm sau',
]

# ============ NEW: REMINDER PATTERNS ============
REMINDER_UNITS = {
    'minute': {
        'full': ['phút', 'phut', 'minute', 'min'],
        'values': [5, 10, 15, 20, 30, 45],
        'multiplier': 1,
    },
    'hour': {
        'full': ['giờ', 'gio', 'tiếng', 'tieng', 'hour', 'h'],
        'values': [1, 2, 3, 4, 5, 6, 12],
        'multiplier': 60,
    },
    'day': {
        'full': ['ngày', 'ngay', 'day', 'd'],
        'values': [1, 2, 3, 5, 7],
        'multiplier': 1440,  # 24 * 60
    },
    'week': {
        'full': ['tuần', 'tuan', 'week', 'w'],
        'values': [1, 2, 3, 4],
        'multiplier': 10080,  # 7 * 24 * 60
    },
    'month': {
        'full': ['tháng', 'thang', 'month', 'm'],
        'values': [1, 2, 3, 6],
        'multiplier': 43200,  # 30 * 24 * 60
    },
}

REMINDER_VERBS = [
    'nhắc', 'nhac', 'nhắc nhở', 'nhac nho', 'reminder', 'remind',
    'báo', 'bao', 'thông báo', 'thong bao', 'notify',
]

REMINDER_POSITIONS = [
    'trước', 'truoc', 'trc', 'before',
    'sớm hơn', 'som hon', 'earlier',
]

def generate_extreme_typos(word):
    """Generate creative typos"""
    if len(word) < 3:
        return word
    
    typos = []
    
    # Missing chars
    if len(word) > 3:
        typos.append(word[:2] + word[3:])
    
    # Double chars
    idx = random.randint(1, len(word)-1)
    typos.append(word[:idx] + word[idx] + word[idx:])
    
    # Swap adjacent
    idx = random.randint(0, len(word)-2)
    chars = list(word)
    chars[idx], chars[idx+1] = chars[idx+1], chars[idx]
    typos.append(''.join(chars))
    
    # Add 'h' suffix
    if word[-1] in 'aiou':
        typos.append(word + 'h')
    
    return random.choice(typos + [word])

def calculate_datetime(days_offset=1, hour=10, minute=0):
    """Calculate target datetime"""
    base_date = datetime(2025, 11, 7)
    return (base_date + timedelta(days=days_offset)).replace(hour=hour % 24, minute=minute)

# ============ GENERATOR 1: WEEK/MONTH REMINDER PATTERNS (15K) ============
def generate_week_month_reminders(count=15000):
    """Focus on week/month reminder patterns"""
    samples = []
    
    templates = [
        # Pattern 1: "nhắc trước X tuần/tháng"
        lambda unit, value, verb, pos: f"nhắc {pos} {value} {unit}",
        # Pattern 2: "nhắc X tuần/tháng trước"  
        lambda unit, value, verb, pos: f"{verb} {value} {unit} {pos}",
        # Pattern 3: "nhắc tôi trước X tuần/tháng"
        lambda unit, value, verb, pos: f"{verb} tôi {pos} {value} {unit}",
        # Pattern 4: No diacritics
        lambda unit, value, verb, pos: f"nhac truoc {value} {unit}",
        # Pattern 5: With event
        lambda unit, value, verb, pos: f"{verb} {value} {unit} {pos}",
    ]
    
    for i in range(count):
        # Focus on week/month units
        unit_type = random.choice(['week', 'month', 'day'])
        unit_data = REMINDER_UNITS[unit_type]
        
        value = random.choice(unit_data['values'])
        unit = random.choice(unit_data['full'])
        verb = random.choice(REMINDER_VERBS)
        pos = random.choice(REMINDER_POSITIONS)
        
        # Generate reminder phrase
        template = random.choice(templates)
        reminder_phrase = template(unit, value, verb, pos)
        
        # Add event context
        event = random.choice(EVENTS)
        location = random.choice(LOCATIONS) if random.random() > 0.5 else None
        time_phrase = f"{random.randint(8, 20)}h {random.choice(RELATIVE_TIME)}"
        
        # Construct full text
        text_variants = [
            f"{event} {time_phrase} {reminder_phrase}",
            f"{reminder_phrase} {event} {time_phrase}",
            f"{time_phrase} {event} {reminder_phrase}",
            f"{event} {time_phrase} ở {location} {reminder_phrase}" if location else f"{event} {time_phrase} {reminder_phrase}",
        ]
        text = random.choice(text_variants)
        
        sample = {
            "id": len(samples) + 1,
            "text": text,
            "event": event,
            "start_time": calculate_datetime(days_offset=random.randint(1, 30), hour=random.randint(8, 20)).isoformat(),
            "location": location,
            "reminder_minutes": value * unit_data['multiplier']
        }
        samples.append(sample)
    
    return samples

# ============ GENERATOR 2: ALL REMINDER UNITS MIXED (10K) ============
def generate_all_reminder_units(count=10000):
    """Mix all reminder units (minute/hour/day/week/month)"""
    samples = []
    
    for i in range(count):
        # Randomly select any unit
        unit_type = random.choice(list(REMINDER_UNITS.keys()))
        unit_data = REMINDER_UNITS[unit_type]
        
        value = random.choice(unit_data['values'])
        unit = random.choice(unit_data['full'])
        verb = random.choice(REMINDER_VERBS)
        pos = random.choice(REMINDER_POSITIONS)
        
        event = random.choice(EVENTS)
        location = random.choice(LOCATIONS) if random.random() > 0.3 else None
        
        # Vary construction order
        if random.random() > 0.5:
            text = f"{event} ngày {random.randint(10, 28)}/11 {verb} {pos} {value} {unit}"
        else:
            text = f"đặt lịch {event} {random.choice(RELATIVE_TIME)} {verb} {value} {unit} {pos}"
        
        if location:
            text += f" tại {location}"
        
        sample = {
            "id": len(samples) + 1,
            "text": text,
            "event": event,
            "start_time": calculate_datetime(days_offset=random.randint(1, 20), hour=random.randint(7, 21)).isoformat(),
            "location": location,
            "reminder_minutes": value * unit_data['multiplier']
        }
        samples.append(sample)
    
    return samples

# ============ GENERATOR 3: REVERSED PATTERNS (10K) ============
def generate_reversed_patterns(count=10000):
    """Reversed word order patterns"""
    samples = []
    
    for i in range(count):
        weekday = random.choice(WEEKDAYS['full'] + WEEKDAYS['short'])
        period = random.choice(PERIODS['full'] + PERIODS['no_diacritic'])
        hour = random.choice(NUMBERS['digit'][:15])
        event = random.choice(EVENTS)
        location = random.choice(LOCATIONS) if random.random() > 0.5 else None
        
        # Reversed orders
        text_parts = [period, f"{hour}h", weekday, event]
        random.shuffle(text_parts)
        
        if location:
            text_parts.append(f"ở {location}")
        
        text = " ".join(text_parts)
        
        sample = {
            "id": len(samples) + 1,
            "text": text,
            "event": event,
            "start_time": calculate_datetime(days_offset=random.randint(1, 7), hour=hour).isoformat(),
            "location": location,
            "reminder_minutes": 0
        }
        samples.append(sample)
    
    return samples

# ============ GENERATOR 4: EXTREME TYPO PATTERNS (15K) ============
def generate_extreme_typo_patterns(count=15000):
    """Extreme typo combinations"""
    samples = []
    
    for i in range(count):
        typo_rate = random.uniform(0.2, 0.7)
        
        weekday = random.choice(WEEKDAYS['full'] + WEEKDAYS['typo_h'] + WEEKDAYS['extreme_typo'])
        number = random.choice(NUMBERS['word'] + NUMBERS['typo_h'])
        period = random.choice(PERIODS['full'] + PERIODS['no_diacritic'])
        event = random.choice(EVENTS)
        
        # Apply typos
        if random.random() < typo_rate:
            weekday = generate_extreme_typos(weekday)
        if random.random() < typo_rate:
            period = generate_extreme_typos(period)
        
        text = f"{weekday} {number} gio {period} {event}"
        
        sample = {
            "id": len(samples) + 1,
            "text": text,
            "event": event,
            "start_time": calculate_datetime(days_offset=random.randint(1, 7), hour=10).isoformat(),
            "location": None,
            "reminder_minutes": 0
        }
        samples.append(sample)
    
    return samples

# ============ GENERATOR 5: TRIPLE COMBINATIONS (15K) ============
def generate_triple_combinations(count=15000):
    """Weekday + Period + Number + Location + Reminder"""
    samples = []
    
    for i in range(count):
        weekday = random.choice(WEEKDAYS['full'] + WEEKDAYS['short'])
        period = random.choice(PERIODS['full'])
        hour = random.choice(NUMBERS['digit'][:18])
        event = random.choice(EVENTS)
        location = random.choice(LOCATIONS)
        
        # Add reminder (30% chance)
        reminder_minutes = 0
        reminder_text = ""
        if random.random() > 0.7:
            unit_type = random.choice(list(REMINDER_UNITS.keys()))
            unit_data = REMINDER_UNITS[unit_type]
            value = random.choice(unit_data['values'])
            unit = random.choice(unit_data['full'])
            reminder_minutes = value * unit_data['multiplier']
            reminder_text = f" nhắc {value} {unit} trước"
        
        # Vary order
        orders = [
            f"{weekday} {period} {hour}h {event} ở {location}{reminder_text}",
            f"{period} {weekday} {hour}h {event} tại {location}{reminder_text}",
            f"{hour}h {period} {weekday} {event} o {location}{reminder_text}",
            f"{event} {weekday} {hour}h {period} tại {location}{reminder_text}",
        ]
        text = random.choice(orders)
        
        sample = {
            "id": len(samples) + 1,
            "text": text,
            "event": event,
            "start_time": calculate_datetime(days_offset=random.randint(1, 7), hour=hour).isoformat(),
            "location": location,
            "reminder_minutes": reminder_minutes
        }
        samples.append(sample)
    
    return samples

# ============ GENERATOR 6: RARE PATTERNS (10K) ============
def generate_rare_patterns(count=10000):
    """Rare/unusual patterns"""
    samples = []
    
    rare_templates = [
        # Range times
        lambda: f"họp từ {random.randint(8,11)}h đến {random.randint(12,15)}h {random.choice(RELATIVE_TIME)}",
        # No explicit time
        lambda: f"{random.choice(PERIODS['full'])} {random.choice(RELATIVE_TIME)} {random.choice(EVENTS)}",
        # Multiple events
        lambda: f"{random.randint(8,10)}h {random.choice(EVENTS)} và {random.choice(EVENTS)}",
        # Complex location
        lambda: f"{random.randint(8,17)}h {random.choice(EVENTS)} tại {random.choice(LOCATIONS)} phòng {random.randint(101,501)}",
        # Date format DD/MM
        lambda: f"đặt lịch {random.choice(EVENTS)} ngày {random.randint(10,28)}/11 ở {random.choice(LOCATIONS)}",
    ]
    
    for i in range(count):
        template = random.choice(rare_templates)
        text = template()
        
        sample = {
            "id": len(samples) + 1,
            "text": text,
            "event": random.choice(EVENTS),
            "start_time": calculate_datetime(days_offset=random.randint(1, 20), hour=10).isoformat(),
            "location": random.choice([None, random.choice(LOCATIONS)]),
            "reminder_minutes": 0
        }
        samples.append(sample)
    
    return samples

# ============ GENERATOR 7: REGIONAL VARIANTS (10K) ============
def generate_regional_variants(count=10000):
    """Regional pronunciation variants"""
    samples = []
    
    southern_mappings = {
        'thứ': 'thớ', 'giờ': 'zờ', 'trưa': 'chưa',
        'sáng': 'xáng', 'chiều': 'giều',
    }
    
    for i in range(count):
        text = f"{random.choice(WEEKDAYS['full'])} {random.randint(7,18)}h {random.choice(PERIODS['full'])} {random.choice(EVENTS)}"
        
        for std, regional in southern_mappings.items():
            if random.random() > 0.5:
                text = text.replace(std, regional)
        
        sample = {
            "id": len(samples) + 1,
            "text": text,
            "event": random.choice(EVENTS),
            "start_time": calculate_datetime(days_offset=random.randint(1, 7), hour=random.randint(7, 18)).isoformat(),
            "location": None,
            "reminder_minutes": 0
        }
        samples.append(sample)
    
    return samples

# ============ GENERATOR 8: EDGE CASE - LOCATION CONFLICTS (5K) ============
def generate_location_edge_cases(count=5000):
    """Edge cases where location contains reminder keywords"""
    samples = []
    
    # Locations with time/reminder keywords
    tricky_locations = [
        '30 Shines', 'Cafe 24h', 'Phố Tuần', 'Quán Tháng',
        'Nhà hàng Ngày Mới', 'Khách sạn Giờ Vàng',
        'Trung tâm Nhắc Nhở', 'Cafe Reminder',
    ]
    
    for i in range(count):
        location = random.choice(tricky_locations)
        event = random.choice(EVENTS)
        hour = random.randint(8, 20)
        
        # Add actual reminder
        unit_type = random.choice(['week', 'month', 'day'])
        unit_data = REMINDER_UNITS[unit_type]
        value = random.choice(unit_data['values'])
        unit = random.choice(unit_data['full'])
        reminder_minutes = value * unit_data['multiplier']
        
        text = f"đặt lịch {event} ngày {random.randint(15,28)}/11 ở {location} nhắc trước {value} {unit}"
        
        sample = {
            "id": len(samples) + 1,
            "text": text,
            "event": event,
            "start_time": calculate_datetime(days_offset=random.randint(1, 21), hour=hour).isoformat(),
            "location": location,
            "reminder_minutes": reminder_minutes
        }
        samples.append(sample)
    
    return samples

# ============ GENERATOR 9: NO DIACRITICS FULL SENTENCES (10K) ============
def generate_no_diacritics(count=10000):
    """Complete sentences without diacritics"""
    samples = []
    
    for i in range(count):
        event = random.choice(EVENTS).replace('ă', 'a').replace('ư', 'u').replace('ơ', 'o')
        event = event.replace('â', 'a').replace('ê', 'e').replace('ô', 'o')
        event = event.replace('đ', 'd').replace('Đ', 'D')
        
        text = f"dat lich {event} ngay {random.randint(10,28)}/11 luc {random.randint(8,20)}h nhac truoc {random.randint(1,3)} tuan"
        
        sample = {
            "id": len(samples) + 1,
            "text": text,
            "event": event,
            "start_time": calculate_datetime(days_offset=random.randint(1, 18), hour=random.randint(8, 20)).isoformat(),
            "location": None,
            "reminder_minutes": random.randint(1, 3) * 10080
        }
        samples.append(sample)
    
    return samples

def main():
    print("🚀 Generating 100K+ COMPREHENSIVE training data with Week/Month reminders...")
    print("=" * 70)
    
    all_samples = []
    
    generators = [
        ("Week/Month Reminder Patterns", generate_week_month_reminders, 15000),
        ("All Reminder Units Mixed", generate_all_reminder_units, 10000),
        ("Reversed Patterns", generate_reversed_patterns, 10000),
        ("Extreme Typo Patterns", generate_extreme_typo_patterns, 15000),
        ("Triple Combinations", generate_triple_combinations, 15000),
        ("Rare Patterns", generate_rare_patterns, 10000),
        ("Regional Variants", generate_regional_variants, 10000),
        ("Location Edge Cases", generate_location_edge_cases, 5000),
        ("No Diacritics", generate_no_diacritics, 10000),
    ]
    
    for name, generator, count in generators:
        print(f"📝 Generating {name} ({count:,})...")
        samples = generator(count)
        all_samples.extend(samples)
        print(f"   ✅ Generated {len(samples):,} samples")
    
    # Shuffle
    random.shuffle(all_samples)
    
    # Re-assign IDs
    for i, sample in enumerate(all_samples):
        sample['id'] = i + 1
    
    # Save
    output_file = "tests/training_100k_comprehensive.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_samples, f, ensure_ascii=False, indent=2)
    
    print("=" * 70)
    print(f"✅ COMPLETE! Generated {len(all_samples):,} samples")
    print(f"💾 Saved to: {output_file}")
    print(f"📊 File size: {len(json.dumps(all_samples, ensure_ascii=False)) / 1024 / 1024:.2f} MB")
    
    # Statistics
    reminder_count = sum(1 for s in all_samples if s['reminder_minutes'] > 0)
    location_count = sum(1 for s in all_samples if s['location'])
    
    print("\n📈 STATISTICS:")
    print(f"   - Total samples: {len(all_samples):,}")
    print(f"   - With reminders: {reminder_count:,} ({reminder_count/len(all_samples)*100:.1f}%)")
    print(f"   - With locations: {location_count:,} ({location_count/len(all_samples)*100:.1f}%)")
    
    # Reminder breakdown
    week_month_count = sum(1 for s in all_samples if s['reminder_minutes'] >= 1440)
    print(f"   - Week/Month/Day reminders: {week_month_count:,}")
    
    # Sample preview
    print("\n📋 SAMPLE PREVIEW (random 5):")
    for sample in random.sample(all_samples, 5):
        print(f"   - {sample['text']}")
        print(f"     → Event: {sample['event']}, Reminder: {sample['reminder_minutes']} min, Location: {sample['location']}")

if __name__ == "__main__":
    main()
