#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test 50 edge cases for specific date/month/year patterns
Focus: ngày cụ thể, tháng cụ thể, năm cụ thể, validation against past dates
"""

import json
from datetime import datetime

def generate_specific_date_tests():
    """Generate 50 specific test cases for date/month/year patterns"""
    
    cases = []
    test_id = 1
    
    # Category 1: Ngày cụ thể (Specific day - 10 cases)
    print("Category 1: Ngày cụ thể (without month)")
    specific_days = [
        ("Họp nhóm ngày 15", "ngày 15", "Assumes current/next month day 15"),
        ("Gặp khách ngày 20 lúc 10h", "ngày 20 + 10h", "Day 20 at 10:00"),
        ("Học bài ngày 25 sáng mai", "ngày 25 + sáng", "Day 25 morning"),
        ("Đi khám ngày 5 chiều", "ngày 5 + chiều", "Day 5 afternoon"),
        ("Meeting ngày 30", "ngày 30", "End of month"),
        ("Review ngày 1", "ngày 1", "First day of month"),
        ("Họp ngày 10 tối", "ngày 10 + tối", "Day 10 evening"),
        ("Gặp ngày 18 14h", "ngày 18 + 14h", "Day 18 at 14:00"),
        ("Học ngày 22 trưa", "ngày 22 + trưa", "Day 22 noon"),
        ("Đi ngày 28 lúc 16h30", "ngày 28 + 16h30", "Day 28 at 16:30"),
    ]
    
    for prompt, pattern, description in specific_days:
        cases.append({
            "id": f"specific_day_{test_id}",
            "input": prompt,
            "category": "specific_day",
            "pattern": pattern,
            "description": description,
            "expected_fields": ["event_name", "start_time"],
            "validation": "day should be in current or next month"
        })
        test_id += 1
    
    # Category 2: Ngày tháng cụ thể (Specific day and month - 10 cases)
    print("Category 2: Ngày tháng cụ thể")
    day_month = [
        ("Họp nhóm ngày 15 tháng 12", "15/12", "December 15"),
        ("Gặp khách ngày 20 tháng 11 lúc 10h", "20/11 + 10h", "November 20 at 10:00"),
        ("Sinh nhật ngày 25 tháng 12 tối", "25/12 + tối", "Christmas evening"),
        ("Review ngày 1 tháng 1", "1/1", "New Year's Day"),
        ("Meeting ngày 30 tháng 11 sáng", "30/11 + sáng", "November 30 morning"),
        ("Họp ngày 10 tháng 12 14h", "10/12 + 14h", "December 10 at 14:00"),
        ("Gặp ngày 5 tháng 12", "5/12", "December 5"),
        ("Học ngày 18 tháng 11 chiều", "18/11 + chiều", "November 18 afternoon"),
        ("Đi ngày 22 tháng 12 lúc 9h", "22/12 + 9h", "December 22 at 9:00"),
        ("Cafe ngày 8 tháng 12 15h30", "8/12 + 15h30", "December 8 at 15:30"),
    ]
    
    for prompt, pattern, description in day_month:
        cases.append({
            "id": f"day_month_{test_id}",
            "input": prompt,
            "category": "day_month",
            "pattern": pattern,
            "description": description,
            "expected_fields": ["event_name", "start_time"],
            "validation": "should be in current year"
        })
        test_id += 1
    
    # Category 3: Ngày tháng năm cụ thể (Full date with year - 10 cases)
    print("Category 3: Ngày tháng năm cụ thể")
    full_dates = [
        ("Họp ngày 15 tháng 12 năm 2025", "15/12/2025", "Full date 2025"),
        ("Gặp khách ngày 20 tháng 1 năm 2026 lúc 10h", "20/1/2026 + 10h", "January 2026"),
        ("Review ngày 1 tháng 1 năm 2026", "1/1/2026", "New Year 2026"),
        ("Meeting ngày 25 tháng 12 năm 2025 sáng", "25/12/2025 + sáng", "Christmas 2025"),
        ("Họp ngày 10 tháng 11 năm 2025 14h", "10/11/2025 + 14h", "November 2025"),
        ("Gặp ngày 5 tháng 6 năm 2026", "5/6/2026", "June 2026"),
        ("Học ngày 18 tháng 3 năm 2026 chiều", "18/3/2026 + chiều", "March 2026"),
        ("Đi ngày 22 tháng 7 năm 2026 lúc 9h", "22/7/2026 + 9h", "July 2026"),
        ("Cafe ngày 8 tháng 12 năm 2025 15h30", "8/12/2025 + 15h30", "December 2025"),
        ("Sprint ngày 30 tháng 11 năm 2025", "30/11/2025", "November 30, 2025"),
    ]
    
    for prompt, pattern, description in full_dates:
        cases.append({
            "id": f"full_date_{test_id}",
            "input": prompt,
            "category": "full_date",
            "pattern": pattern,
            "description": description,
            "expected_fields": ["event_name", "start_time"],
            "validation": "should match exact year"
        })
        test_id += 1
    
    # Category 4: Tháng cụ thể (Specific month - 5 cases)
    print("Category 4: Tháng cụ thể")
    specific_months = [
        ("Họp tháng 12", "tháng 12", "Assumes 1st of December"),
        ("Gặp khách tháng 11 lúc 10h", "tháng 11 + 10h", "November 1st at 10:00"),
        ("Review tháng 1", "tháng 1", "January 1st (next year if past)"),
        ("Meeting tháng 12 sáng", "tháng 12 + sáng", "December 1st morning"),
        ("Học tháng 6 năm 2026", "tháng 6 năm 2026", "June 1st, 2026"),
    ]
    
    for prompt, pattern, description in specific_months:
        cases.append({
            "id": f"specific_month_{test_id}",
            "input": prompt,
            "category": "specific_month",
            "pattern": pattern,
            "description": description,
            "expected_fields": ["event_name", "start_time"],
            "validation": "should default to 1st of month"
        })
        test_id += 1
    
    # Category 5: Năm cụ thể và tương đối (Specific and relative years - 10 cases)
    print("Category 5: Năm cụ thể và tương đối")
    year_patterns = [
        ("Họp năm sau", "năm sau", "Next year (Jan 1)"),
        ("Gặp khách năm tới lúc 10h", "năm tới + 10h", "Next year Jan 1 at 10:00"),
        ("Review năm 2026", "năm 2026", "Year 2026 (Jan 1)"),
        ("Meeting năm 2027 sáng", "năm 2027 + sáng", "Year 2027 morning"),
        ("Học năm 2025 chiều", "năm 2025 + chiều", "Current year afternoon"),
        ("Deadline năm sau tháng 6", "năm sau + tháng 6", "Next year June"),
        ("Sprint planning năm 2026", "năm 2026", "Year 2026"),
        ("Annual review năm tới", "năm tới", "Next year"),
        ("Conference năm 2028", "năm 2028", "Year 2028"),
        ("Audit năm sau ngày 15", "năm sau + ngày 15", "Next year day 15"),
    ]
    
    for prompt, pattern, description in year_patterns:
        cases.append({
            "id": f"year_pattern_{test_id}",
            "input": prompt,
            "category": "year_pattern",
            "pattern": pattern,
            "description": description,
            "expected_fields": ["event_name", "start_time"],
            "validation": "should be future year only"
        })
        test_id += 1
    
    # Category 6: Past date validation (Should FAIL - 5 cases)
    print("Category 6: Past dates (should be rejected)")
    # Note: These will fail validation if current date is after Nov 7, 2025
    past_dates = [
        ("Họp ngày 1 tháng 1 năm 2024", "năm 2024", "Past year - should fail"),
        ("Gặp ngày 15 tháng 10 năm 2024", "15/10/2024", "Past date - should fail"),
        ("Review năm 2023", "năm 2023", "Old year - should fail"),
        ("Meeting ngày 20 tháng 5 năm 2024", "20/5/2024", "Past month - should fail"),
        ("Học năm 2020", "năm 2020", "Very old year - should fail"),
    ]
    
    for prompt, pattern, description in past_dates:
        cases.append({
            "id": f"past_date_{test_id}",
            "input": prompt,
            "category": "past_date_validation",
            "pattern": pattern,
            "description": description,
            "should_fail": True,
            "validation": "MUST reject past dates"
        })
        test_id += 1
    
    return cases

def main():
    print("🔧 Generating 50 specific date/month/year test cases...")
    print("=" * 80)
    
    cases = generate_specific_date_tests()
    
    print("\n" + "=" * 80)
    print(f"✅ Generated {len(cases)} test cases")
    
    # Count by category
    categories = {}
    for case in cases:
        cat = case.get('category', 'unknown')
        categories[cat] = categories.get(cat, 0) + 1
    
    print("\n📊 Test Cases by Category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat:25s}: {count:2d} cases")
    
    # Save to JSON
    output_file = "tests/specific_date_edge_cases.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(cases, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Saved to: {output_file}")
    print(f"📦 File size: {len(json.dumps(cases, ensure_ascii=False))} bytes")
    
    # Sample cases
    print("\n📝 Sample Cases (first 5):")
    for i in range(min(5, len(cases))):
        case = cases[i]
        print(f"\n  [{i+1}] {case['category']}")
        print(f"      Input: {case['input']}")
        print(f"      Pattern: {case['pattern']}")
        print(f"      Description: {case['description']}")
    
    print("\n" + "=" * 80)
    print("✅ Test case generation complete!")
    print("\nNext steps:")
    print("  1. Run: python tests/run_specific_date_tests.py")
    print("  2. Check results and fix any issues")
    print("  3. Validate past date rejection works correctly")

if __name__ == "__main__":
    main()
