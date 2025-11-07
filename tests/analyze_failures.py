#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Analyze test failures and generate fix recommendations
"""

import json
from collections import Counter, defaultdict

def analyze_failures():
    """Analyze all test failures and categorize issues"""
    
    print("=" * 80)
    print("🔍 FAILURE ANALYSIS - Hybrid NLP Pipeline")
    print("=" * 80)
    
    # Load report
    with open("tests/hybrid_test_report_20251107_182833.json", 'r', encoding='utf-8') as f:
        report = json.load(f)
    
    failures = report['failures']
    
    print(f"\n📊 Total Failures: {len(failures)}")
    print(f"Success Rate: {report['summary']['success_rate']:.2f}%\n")
    
    # Categorize failures
    failure_types = defaultdict(list)
    
    for failure in failures:
        error = failure.get('error', '')
        category = failure.get('category', '')
        
        if 'Missing or None start_time' in error:
            failure_types['missing_time'].append(failure)
        elif 'None or empty' in error and 'event_name' in error:
            failure_types['missing_event'].append(failure)
        elif 'Should fail but got' in error:
            failure_types['should_fail'].append(failure)
        else:
            failure_types['other'].append(failure)
    
    # Analysis
    print("📋 Failure Types:")
    for ftype, cases in failure_types.items():
        print(f"\n  {ftype}: {len(cases)} cases")
    
    # Deep dive: Missing time
    if failure_types['missing_time']:
        print("\n" + "=" * 80)
        print("🔍 ISSUE 1: Missing Time Parsing")
        print("=" * 80)
        
        # Extract patterns
        time_patterns = Counter()
        for case in failure_types['missing_time']:
            inp = case.get('input', '')
            # Extract likely time words
            words = inp.lower().split()
            for word in words:
                if any(t in word for t in ['tuần', 'tháng', 'ngày', 'sáng', 'chiều', 'tối', 'trưa']):
                    time_patterns[word] += 1
        
        print("\n📊 Most Common Missing Time Patterns:")
        for pattern, count in time_patterns.most_common(10):
            print(f"  {pattern:20s}: {count:3d} occurrences")
        
        print("\n📝 Sample Cases:")
        for case in failure_types['missing_time'][:10]:
            print(f"  Input: {case['input']}")
            result = case.get('result', {})
            print(f"    → Event: {result.get('event_name')}")
            print(f"    → Time:  {result.get('start_time')}")
            print()
    
    # Deep dive: Missing event
    if failure_types['missing_event']:
        print("\n" + "=" * 80)
        print("🔍 ISSUE 2: Missing Event Name")
        print("=" * 80)
        
        print(f"\nTotal: {len(failure_types['missing_event'])} cases")
        print("\n📝 Sample Cases:")
        for case in failure_types['missing_event'][:10]:
            print(f"  Input: {case['input']}")
            result = case.get('result', {})
            print(f"    → Event: {result.get('event_name')}")
            print()
    
    # Deep dive: Should fail
    if failure_types['should_fail']:
        print("\n" + "=" * 80)
        print("🔍 ISSUE 3: Should Fail But Didn't")
        print("=" * 80)
        
        print(f"\nTotal: {len(failure_types['should_fail'])} cases")
        print("\nThese are cases that SHOULD fail (empty input, etc)")
        print("but pipeline returned valid results. This is LOW priority.")
    
    # Recommendations
    print("\n" + "=" * 80)
    print("💡 FIX RECOMMENDATIONS")
    print("=" * 80)
    
    print("\n1️⃣  PRIORITY 1 - Missing Time Parsing:")
    print("   Issue: Pipeline can't parse relative dates:")
    print("   - 'tuần sau', 'tuần tới', 'tháng sau'")
    print("   - 'ngày mốt', 'ngày kia'")
    print("   ")
    print("   Solution: Enhance time_parser.py")
    print("   - Add relative week/month parsing")
    print("   - Add 'tuần sau' → next Monday")
    print("   - Add 'tháng sau' → first day next month")
    print("   ")
    print("   Impact: Will fix ~15 failures (edge_time category)")
    
    print("\n2️⃣  PRIORITY 2 - Missing Event Names:")
    print("   Issue: Pipeline returns None for very short inputs")
    print("   - Single characters, numbers only")
    print("   ")
    print("   Solution: Add minimum input validation")
    print("   - Require at least 2 characters")
    print("   - Require at least one Vietnamese word")
    print("   ")
    print("   Impact: Will fix ~30 failures (stress_missing category)")
    print("   Note: These SHOULD fail, so this is expected behavior")
    
    print("\n3️⃣  PRIORITY 3 - Minimal Input Handling:")
    print("   Issue: Very minimal inputs like 'học tối', 'đi sáng'")
    print("   - Missing specific time (just 'tối', 'sáng')")
    print("   ")
    print("   Solution: Add default time assumptions")
    print("   - 'sáng' → 8:00 AM")
    print("   - 'trưa' → 12:00 PM")
    print("   - 'chiều' → 2:00 PM")
    print("   - 'tối' → 6:00 PM")
    print("   ")
    print("   Impact: Will fix ~12 failures (stress_minimal)")
    
    print("\n" + "=" * 80)
    print("📈 OVERALL ASSESSMENT")
    print("=" * 80)
    
    success_rate = report['summary']['success_rate']
    
    if success_rate >= 95:
        print(f"\n✅ EXCELLENT: {success_rate:.1f}% success rate")
        print("   No critical fixes needed. Optional improvements only.")
    elif success_rate >= 90:
        print(f"\n✅ VERY GOOD: {success_rate:.1f}% success rate")
        print("   Pipeline is production-ready!")
        print("   Optional: Implement Priority 1 fix for edge cases")
    elif success_rate >= 85:
        print(f"\n⚠️  GOOD: {success_rate:.1f}% success rate")
        print("   Recommend implementing Priority 1 and 2 fixes")
    else:
        print(f"\n🚨 NEEDS WORK: {success_rate:.1f}% success rate")
        print("   Implement all priority fixes")
    
    # Check by category
    print("\n📊 Category Assessment:")
    by_cat = report['by_category']
    
    problem_cats = []
    for cat, stats in by_cat.items():
        rate = (stats['passed'] / stats['total'] * 100) if stats['total'] > 0 else 0
        if rate < 90:
            problem_cats.append((cat, rate, stats))
    
    if problem_cats:
        print("\n  Categories needing attention:")
        for cat, rate, stats in sorted(problem_cats, key=lambda x: x[1]):
            print(f"    {cat:20s}: {rate:5.1f}% ({stats['passed']}/{stats['total']})")
    else:
        print("\n  ✅ All categories performing well!")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    analyze_failures()
