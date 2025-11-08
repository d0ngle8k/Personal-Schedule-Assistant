#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Analyze event extraction failures in detail
"""

import json
from pathlib import Path
from collections import Counter

def main():
    report_path = Path(__file__).parent / "hybrid_comprehensive_test_report_20251108_100349.json"
    
    with open(report_path, 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    print("="*80)
    print("EVENT EXTRACTION FAILURE ANALYSIS")
    print("="*80)
    
    all_event_failures = []
    
    for file_result in report['file_results']:
        file_name = file_result['file']
        failures = file_result['failures']
        
        for failure in failures:
            field_results = failure.get('field_results', {})
            
            # Only event failures
            if not field_results.get('event', True):
                expected_event = failure['expected'].get('event', '')
                actual_event = failure['actual'].get('event_name', '')
                
                all_event_failures.append({
                    'file': file_name,
                    'input': failure['input'],
                    'expected': expected_event,
                    'actual': actual_event
                })
    
    print(f"\nTotal Event Failures: {len(all_event_failures)}")
    
    # Categorize failures
    print("\n" + "="*80)
    print("FAILURE CATEGORIES")
    print("="*80)
    
    # Category 1: Missing words (actual is substring of expected)
    missing_words = []
    # Category 2: Extra words (expected is substring of actual)
    extra_words = []
    # Category 3: Completely different
    completely_different = []
    # Category 4: Diacritic issues
    diacritic_issues = []
    
    for failure in all_event_failures:
        exp = (failure['expected'] or '').lower().strip()
        act = (failure['actual'] or '').lower().strip()
        
        if not act:
            missing_words.append(failure)
        elif exp in act:
            extra_words.append(failure)
        elif act in exp:
            missing_words.append(failure)
        else:
            # Check if it's just diacritic difference
            exp_no_space = exp.replace(' ', '')
            act_no_space = act.replace(' ', '')
            if len(exp_no_space) == len(act_no_space):
                diacritic_issues.append(failure)
            else:
                completely_different.append(failure)
    
    print(f"\n1. Missing Words (actual is incomplete): {len(missing_words)}")
    for i, f in enumerate(missing_words[:10], 1):
        print(f"   {i}. Input: {f['input']}")
        print(f"      Expected: '{f['expected']}'")
        print(f"      Actual: '{f['actual']}'")
    
    print(f"\n2. Extra Words (actual has too much): {len(extra_words)}")
    for i, f in enumerate(extra_words[:10], 1):
        print(f"   {i}. Input: {f['input']}")
        print(f"      Expected: '{f['expected']}'")
        print(f"      Actual: '{f['actual']}'")
    
    print(f"\n3. Completely Different: {len(completely_different)}")
    for i, f in enumerate(completely_different[:10], 1):
        print(f"   {i}. Input: {f['input']}")
        print(f"      Expected: '{f['expected']}'")
        print(f"      Actual: '{f['actual']}'")
    
    print(f"\n4. Diacritic Issues: {len(diacritic_issues)}")
    for i, f in enumerate(diacritic_issues[:10], 1):
        print(f"   {i}. Input: {f['input']}")
        print(f"      Expected: '{f['expected']}'")
        print(f"      Actual: '{f['actual']}'")
    
    # Pattern analysis
    print("\n" + "="*80)
    print("COMMON PATTERNS IN FAILURES")
    print("="*80)
    
    # Missing word patterns
    print("\nMissing Word Patterns (what's being dropped):")
    missing_patterns = Counter()
    for f in missing_words:
        exp_words = set((f['expected'] or '').lower().split())
        act_words = set((f['actual'] or '').lower().split())
        dropped = exp_words - act_words
        for word in dropped:
            if word:  # Skip empty strings
                missing_patterns[word] += 1
    
    for word, count in missing_patterns.most_common(20):
        print(f"   '{word}': {count} times")
    
    # Extra word patterns
    print("\nExtra Word Patterns (what's being added):")
    extra_patterns = Counter()
    for f in extra_words:
        exp_words = set((f['expected'] or '').lower().split())
        act_words = set((f['actual'] or '').lower().split())
        added = act_words - exp_words
        for word in added:
            if word:  # Skip empty strings
                extra_patterns[word] += 1
    
    for word, count in extra_patterns.most_common(20):
        print(f"   '{word}': {count} times")
    
    # Recommendations
    print("\n" + "="*80)
    print("OPTIMIZATION RECOMMENDATIONS")
    print("="*80)
    
    print("\n1. FIX MISSING WORDS:")
    print("   - Expand three-word event dictionaries")
    print("   - Add common compound events")
    print("   - Improve event boundary detection")
    
    print("\n2. FIX EXTRA WORDS:")
    print("   - Better reminder text cleaning")
    print("   - Improve time word removal")
    print("   - Add post-processing cleanup")
    
    print("\n3. FIX DIACRITIC ISSUES:")
    print("   - Normalize diacritics in comparison")
    print("   - Add more variant forms to dictionaries")
    
    print("\n" + "="*80)

if __name__ == '__main__':
    main()
