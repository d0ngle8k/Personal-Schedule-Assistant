#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Debug location contamination
"""

from core_nlp.pipeline import NLPPipeline

# Test cases with location contamination
test_cases = [
    "Học tiếng Anh 18:00 thứ 2 tuần sau",
    "Họp online 9h sáng mai nhắc trước 30 phút",
    "Họp phụ huynh 8 giờ thứ 2 tuần sau",
    "Đi công viên 7h ngày mốt",
    "Gặp khách 7h t3",
    "Họp 22h thứ 2",
]

pipeline = NLPPipeline()

print("="*80)
print("LOCATION CONTAMINATION DEBUG")
print("="*80)

for text in test_cases:
    result = pipeline._extract_entities_regex(text.lower())
    print(f"\nInput: {text}")
    print(f"  Event: {result.get('event_name')}")
    print(f"  Time: {result.get('time_str')}")
    print(f"  Location: {result.get('location')}")
    
    # Show if location contains time components
    loc = result.get('location')
    if loc:
        time_markers = ['thứ', 't2', 't3', 't4', 't5', 't6', 't7', 'cn', ':00', 'giờ', 'h ', 'sáng', 'chiều', 'tối', 'ngày']
        contaminated = any(marker in loc.lower() for marker in time_markers)
        if contaminated:
            print(f"  ⚠️ CONTAMINATED!")
