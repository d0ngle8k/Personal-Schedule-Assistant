"""
Analyze ONLY event extraction failures from the latest test report.
Focus on cases where field_results.event == false.
"""

import json
import glob
import os
from collections import Counter

# Find most recent report
report_files = glob.glob('tests/hybrid_comprehensive_test_report_*.json')
latest_report = max(report_files, key=os.path.getctime)

print(f"📄 Analyzing: {latest_report}")
print(f"=" * 80)

with open(latest_report, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Collect event failures
event_failures = []
for file_result in data['file_results']:
    for test in file_result.get('failures', []):
        # Only include if event field actually failed
        if not test.get('field_results', {}).get('event', True):
            event_failures.append({
                'input': test['input'],
                'expected': test['expected'].get('event'),
                'actual': test['actual'].get('event_name', test['actual'].get('event'))
            })

# Also check passed cases for event field failures (test can pass overall but event fail)
for file_result in data['file_results']:
    # Need to scan all tests, not just failures
    # But test report doesn't include passed cases details
    pass

print(f"\n📊 Event Failures Found: {len(event_failures)}")
print(f"\nFrom Summary Stats:")
print(f"  Event Correct: {data['total_stats']['field_totals']['event']['correct']}")
print(f"  Event Total: {data['total_stats']['field_totals']['event']['total']}")
print(f"  Event Failures: {data['total_stats']['field_totals']['event']['total'] - data['total_stats']['field_totals']['event']['correct']}")

# Categorize
missing_words = []
extra_words = []
completely_different = []

for f in event_failures:
    exp = (f['expected'] or '').lower().strip()
    act = (f['actual'] or '').lower().strip()
    
    # Skip test artifacts
    if exp in ['event_extracted', 'event_with_typo', '']:
        continue
    
    if not act:
        missing_words.append(f)
    elif exp in act:
        extra_words.append(f)
    elif act in exp:
        missing_words.append(f)
    else:
        completely_different.append(f)

print(f"\n" + "=" * 80)
print("EVENT FAILURE BREAKDOWN")
print("=" * 80)
print(f"\n1. Missing Words: {len(missing_words)}")
for i, f in enumerate(missing_words[:30], 1):
    print(f"   {i}. '{f['input'][:60]}...'")
    print(f"      Expected: '{f['expected']}'")
    print(f"      Actual: '{f['actual']}'")

print(f"\n2. Extra Words: {len(extra_words)}")
for i, f in enumerate(extra_words[:30], 1):
    print(f"   {i}. '{f['input'][:60]}...'")
    print(f"      Expected: '{f['expected']}'")
    print(f"      Actual: '{f['actual']}'")

print(f"\n3. Completely Different: {len(completely_different)}")
for i, f in enumerate(completely_different[:30], 1):
    print(f"   {i}. '{f['input'][:60]}...'")
    print(f"      Expected: '{f['expected']}'")
    print(f"      Actual: '{f['actual']}'")

# Pattern analysis
if missing_words:
    missing_counts = Counter()
    for f in missing_words:
        exp_words = set((f['expected'] or '').lower().split())
        act_words = set((f['actual'] or '').lower().split()) if f['actual'] else set()
        dropped = exp_words - act_words
        missing_counts.update(dropped)
    
    print(f"\n" + "=" * 80)
    print("TOP 30 MOST FREQUENTLY DROPPED WORDS")
    print("=" * 80)
    for word, count in missing_counts.most_common(30):
        print(f"  '{word}': {count} times")

if extra_words:
    extra_counts = Counter()
    for f in extra_words:
        exp_words = set((f['expected'] or '').lower().split())
        act_words = set((f['actual'] or '').lower().split()) if f['actual'] else set()
        added = act_words - exp_words
        extra_counts.update(added)
    
    print(f"\n" + "=" * 80)
    print("TOP 30 MOST FREQUENTLY ADDED WORDS")
    print("=" * 80)
    for word, count in extra_counts.most_common(30):
        print(f"  '{word}': {count} times")

print(f"\n" + "=" * 80)
print("SUMMARY")
print("=" * 80)
total_real = len(missing_words) + len(extra_words) + len(completely_different)
print(f"Total Real Event Failures: {total_real}")
print(f"  Missing Words: {len(missing_words)}")
print(f"  Extra Words: {len(extra_words)}")
print(f"  Completely Different: {len(completely_different)}")
print(f"\nTo reach 90% accuracy (996/1107):")
print(f"  Current: {data['total_stats']['field_totals']['event']['correct']}/1107 = {data['total_stats']['field_totals']['event']['correct']/1107*100:.2f}%")
print(f"  Need: {996 - data['total_stats']['field_totals']['event']['correct']} more correct extractions")
