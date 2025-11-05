#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test edge case fixes"""

from core_nlp.pipeline import NLPPipeline

def test_edge_case_fixes():
    p = NLPPipeline()
    
    test_cases = [
        {
            'input': 'an trua 18:00 thứ 2 tuần sau tại bệnh viện bạch mai nhắc trước 60 phút',
            'expected_event': 'an trua',
            'expected_time_str': '18:00 thứ 2 tuần sau',
            'fix': 'Fix #1: Multi-segment time merge'
        },
        {
            'input': 'SINH NHẬT 8:30 ngày mai nhắc trước 60 phút',
            'expected_event': 'sinh nhật',
            'expected_time_str': '8:30 ngày mai',
            'fix': 'Fix #2: Uppercase + colon pattern'
        },
        {
            'input': 'Gặp mặt 20h toi',
            'expected_event': 'gặp mặt',
            'expected_time_str': '20h toi',
            'fix': 'Fix #3: Period word cleanup'
        }
    ]
    
    print("\n" + "="*80)
    print("EDGE CASE FIX VALIDATION")
    print("="*80)
    
    passed = 0
    failed = 0
    
    for tc in test_cases:
        result = p.process(tc['input'])
        actual_event = result.get('event', '')
        start_time = result.get('start_time')
        
        event_match = actual_event.strip() == tc['expected_event']
        has_time = start_time is not None
        
        status = "✅ PASS" if event_match and has_time else "❌ FAIL"
        if event_match and has_time:
            passed += 1
        else:
            failed += 1
        
        print(f"\n{status} - {tc['fix']}")
        print(f"  Input: {tc['input']}")
        print(f"  Expected Event: '{tc['expected_event']}'")
        print(f"  Actual Event: '{actual_event}'")
        print(f"  Event Match: {event_match}")
        print(f"  Has Time: {has_time} ({start_time})")
        if not event_match:
            print(f"  ❌ Event mismatch!")
        if not has_time:
            print(f"  ❌ Time extraction failed!")
    
    print("\n" + "="*80)
    print(f"SUMMARY: {passed} passed, {failed} failed")
    print("="*80 + "\n")
    
    return failed == 0

if __name__ == "__main__":
    success = test_edge_case_fixes()
    exit(0 if success else 1)
