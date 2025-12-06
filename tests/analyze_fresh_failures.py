"""
Analyze event extraction failures from the LATEST test report.
This script reads the most recent hybrid test report JSON file.
"""

import json
import glob
import os
from collections import Counter

# Find the most recent test report
report_files = glob.glob('tests/hybrid_comprehensive_test_report_*.json')
if not report_files:
    print("No test report files found!")
    exit(1)

latest_report = max(report_files, key=os.path.getctime)
print(f"📄 Analyzing: {latest_report}")
print(f"=" * 80)

with open(latest_report, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Collect all event failures
event_failures = []
for file_result in data['file_results']:
    for test in file_result.get('failures', []):
        # Check if event field failed
        if 'event' in test.get('fields_failed', []):
            event_failures.append({
                'input': test['input'],
                'expected': test['expected'].get('event'),
                'actual': test['actual'].get('event')
            })

print(f"\n📊 Total Event Failures: {len(event_failures)}\n")

# Categorize failures
missing_words = []  # Expected has more words than actual
extra_words = []    # Actual has more words than expected
completely_different = []  # Totally different
diacritic_issues = []  # Only diacritic differences

for failure in event_failures:
    expected = (failure['expected'] or '').lower().strip()
    actual = (failure['actual'] or '').lower().strip()
    
    # Skip test artifacts
    if expected in ['event_extracted', 'event_with_typo']:
        continue
    
    if not actual:
        missing_words.append(failure)
    elif expected in actual:
        extra_words.append(failure)
    elif actual in expected:
        missing_words.append(failure)
    else:
        # Check if only diacritic difference
        from unicodedata import normalize
        exp_normalized = normalize('NFKD', expected).encode('ascii', 'ignore').decode()
        act_normalized = normalize('NFKD', actual).encode('ascii', 'ignore').decode()
        
        if exp_normalized == act_normalized:
            diacritic_issues.append(failure)
        else:
            completely_different.append(failure)

print(f"=" * 80)
print("REAL FAILURE CATEGORIES (excluding test artifacts)")
print(f"=" * 80)
print(f"\n1. Missing Words (actual incomplete): {len(missing_words)}")
for i, f in enumerate(missing_words[:20], 1):
    print(f"   {i}. Input: {f['input']}")
    print(f"      Expected: '{f['expected']}'")
    print(f"      Actual: '{f['actual']}'")

print(f"\n2. Extra Words (actual has too much): {len(extra_words)}")
for i, f in enumerate(extra_words[:20], 1):
    print(f"   {i}. Input: {f['input']}")
    print(f"      Expected: '{f['expected']}'")
    print(f"      Actual: '{f['actual']}'")

print(f"\n3. Completely Different: {len(completely_different)}")
for i, f in enumerate(completely_different[:20], 1):
    print(f"   {i}. Input: {f['input']}")
    print(f"      Expected: '{f['expected']}'")
    print(f"      Actual: '{f['actual']}'")

print(f"\n4. Diacritic Issues: {len(diacritic_issues)}")
for i, f in enumerate(diacritic_issues[:10], 1):
    print(f"   {i}. Expected: '{f['expected']}' vs Actual: '{f['actual']}'")

# Analyze patterns in missing/extra words
print(f"\n{'=' * 80}")
print("PATTERN ANALYSIS")
print(f"{'=' * 80}")

if missing_words:
    missing_word_counts = Counter()
    for failure in missing_words:
        expected = (failure['expected'] or '').lower().split()
        actual = (failure['actual'] or '').lower().split() if failure['actual'] else []
        dropped = [w for w in expected if w not in actual]
        missing_word_counts.update(dropped)
    
    print(f"\nTop 20 Missing Words (most frequently dropped):")
    for word, count in missing_word_counts.most_common(20):
        print(f"   '{word}': {count} times")

if extra_words:
    extra_word_counts = Counter()
    for failure in extra_words:
        expected = (failure['expected'] or '').lower().split()
        actual = (failure['actual'] or '').lower().split() if failure['actual'] else []
        added = [w for w in actual if w not in expected]
        extra_word_counts.update(added)
    
    print(f"\nTop 20 Extra Words (most frequently added):")
    for word, count in extra_word_counts.most_common(20):
        print(f"   '{word}': {count} times")

# Summary
print(f"\n{'=' * 80}")
print("SUMMARY")
print(f"{'=' * 80}")
print(f"Total Real Failures: {len(missing_words) + len(extra_words) + len(completely_different) + len(diacritic_issues)}")
print(f"  - Missing Words: {len(missing_words)}")
print(f"  - Extra Words: {len(extra_words)}")
print(f"  - Completely Different: {len(completely_different)}")
print(f"  - Diacritic Issues: {len(diacritic_issues)}")
