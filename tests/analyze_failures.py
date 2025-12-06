#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Analyze test failures to identify patterns
"""

import json
from pathlib import Path
from collections import Counter

def main():
    report_path = Path(__file__).parent / "comprehensive_test_report_20251108_035602.json"
    
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    print("="*80)
    print("FAILURE ANALYSIS")
    print("="*80)
    
    for file_result in report['file_results']:
        file_name = file_result['file']
        failures = file_result['failures']
        
        if not failures:
            continue
        
        print(f"\n{'='*80}")
        print(f"File: {file_name}")
        print(f"Failures: {len(failures)}")
        print(f"{'='*80}")
        
        # Analyze by field
        field_failures = Counter()
        location_contamination = []
        event_failures = []
        
        for failure in failures:
            field_results = failure.get('field_results', {})
            
            for field, passed in field_results.items():
                if not passed:
                    field_failures[field] += 1
                    
                    # Check for location contamination with time
                    if field == 'location':
                        actual_loc = failure['actual'].get('location')
                        if actual_loc and any(word in str(actual_loc).lower() for word in ['thứ', 't2', 't3', 't4', 't5', 't6', 't7', 'cn', ':00', 'giờ', 'h ']):
                            location_contamination.append({
                                'input': failure['input'],
                                'location': actual_loc
                            })
                    
                    # Check for event failures
                    if field == 'event':
                        event_failures.append({
                            'input': failure['input'],
                            'expected': failure['expected'].get('event'),
                            'actual': failure['actual'].get('event_name')
                        })
        
        print(f"\nField Failure Breakdown:")
        for field, count in field_failures.most_common():
            print(f"  {field}: {count}")
        
        if location_contamination:
            print(f"\n⚠️ Location Contamination with Time ({len(location_contamination)} cases):")
            for i, item in enumerate(location_contamination[:10], 1):
                print(f"  {i}. Input: {item['input']}")
                print(f"     Location: {item['location']}")
        
        if event_failures and len(event_failures) <= 10:
            print(f"\n❌ Event Extraction Failures ({len(event_failures)} cases):")
            for i, item in enumerate(event_failures, 1):
                print(f"  {i}. Input: {item['input']}")
                print(f"     Expected: {item['expected']}")
                print(f"     Actual: {item['actual']}")

if __name__ == '__main__':
    main()
