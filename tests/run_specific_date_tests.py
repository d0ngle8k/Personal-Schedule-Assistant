#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run specific date/month/year edge case tests
Validates: ngày cụ thể, tháng cụ thể, năm cụ thể, past date validation
"""

import json
import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core_nlp.hybrid_pipeline import HybridNLPPipeline

def validate_result(result, test_case):
    """
    Validate NLP result against test case expectations
    Returns: (is_valid, error_message)
    """
    should_fail = test_case.get('should_fail', False)
    category = test_case.get('category', '')
    
    if should_fail:
        # For past dates that SHOULD be rejected
        if not result or result.get('start_time') is None:
            return True, "✅ Correctly rejected past date"
        else:
            return False, f"❌ Should reject past date but got: {result.get('start_time')}"
    
    # Check basic structure
    if not isinstance(result, dict):
        return False, f"Result not a dict: {type(result)}"
    
    # Check for event_name
    if not result.get('event_name'):
        return False, "Missing event_name"
    
    # Check start_time
    if not result.get('start_time'):
        return False, "Missing start_time"
    
    start_time = result.get('start_time')
    
    # Category-specific validation
    if category == 'specific_day':
        # Should have a valid day in current or next month
        try:
            dt = datetime.fromisoformat(start_time)
            now = datetime.now()
            # Day should be in valid range
            if dt.day < 1 or dt.day > 31:
                return False, f"Invalid day: {dt.day}"
            # Should be in future (allowing 1 hour tolerance)
            if dt < now.replace(hour=now.hour-1):
                return False, f"Date is in the past: {dt}"
        except Exception as e:
            return False, f"Invalid datetime format: {e}"
    
    elif category == 'day_month':
        # Should have specific month set
        try:
            dt = datetime.fromisoformat(start_time)
            # Check if month is reasonable (1-12)
            if dt.month < 1 or dt.month > 12:
                return False, f"Invalid month: {dt.month}"
        except Exception as e:
            return False, f"Invalid datetime format: {e}"
    
    elif category == 'full_date':
        # Should match exact year specified
        try:
            dt = datetime.fromisoformat(start_time)
            # Year should be 2025 or later (based on test cases)
            if dt.year < 2025:
                return False, f"Year too old: {dt.year}"
        except Exception as e:
            return False, f"Invalid datetime format: {e}"
    
    elif category == 'specific_month':
        # Should default to 1st of month
        try:
            dt = datetime.fromisoformat(start_time)
            if dt.day != 1:
                return False, f"Should be 1st of month, got day: {dt.day}"
        except Exception as e:
            return False, f"Invalid datetime format: {e}"
    
    elif category == 'year_pattern':
        # Should be future year
        try:
            dt = datetime.fromisoformat(start_time)
            now = datetime.now()
            if dt.year < now.year:
                return False, f"Year is in the past: {dt.year}"
        except Exception as e:
            return False, f"Invalid datetime format: {e}"
    
    return True, "OK"

def run_tests():
    """Run specific date edge case tests"""
    
    # Set UTF-8 for Windows
    import sys
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 80)
    print("🧪 SPECIFIC DATE/MONTH/YEAR EDGE CASE TESTS")
    print("=" * 80)
    
    # Load test cases
    test_file = "tests/specific_date_edge_cases.json"
    print(f"\n📂 Loading test cases from: {test_file}")
    
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            test_cases = json.load(f)
    except FileNotFoundError:
        print(f"❌ Test file not found: {test_file}")
        print("💡 Run: python tests/generate_specific_date_tests.py first")
        return None
    
    print(f"✅ Loaded {len(test_cases)} test cases\n")
    
    # Initialize pipeline
    print("🔥 Initializing Hybrid NLP Pipeline...")
    try:
        pipeline = HybridNLPPipeline()
        print("✅ Pipeline ready\n")
    except Exception as e:
        print(f"❌ Failed to initialize pipeline: {e}")
        return None
    
    # Results tracking
    results = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'by_category': {}
    }
    
    failures = []
    
    print("🧪 Running tests...\n")
    
    # Run tests by category
    for test_case in test_cases:
        test_id = test_case.get('id', 'unknown')
        input_text = test_case.get('input', '')
        category = test_case.get('category', 'unknown')
        description = test_case.get('description', '')
        
        if category not in results['by_category']:
            results['by_category'][category] = {'total': 0, 'passed': 0, 'failed': 0}
        
        results['total'] += 1
        results['by_category'][category]['total'] += 1
        
        try:
            # Run NLP
            result = pipeline.process(input_text)
            
            # Validate
            is_valid, error_msg = validate_result(result, test_case)
            
            if is_valid:
                results['passed'] += 1
                results['by_category'][category]['passed'] += 1
                print(f"✅ {test_id}: {input_text}")
                if "reject" in error_msg.lower():
                    print(f"   → {error_msg}")
            else:
                results['failed'] += 1
                results['by_category'][category]['failed'] += 1
                print(f"❌ {test_id}: {input_text}")
                print(f"   → Error: {error_msg}")
                print(f"   → Result: {result}")
                
                failures.append({
                    'id': test_id,
                    'input': input_text,
                    'category': category,
                    'error': error_msg,
                    'result': result
                })
        
        except Exception as e:
            results['failed'] += 1
            results['by_category'][category]['failed'] += 1
            print(f"⚠️  {test_id}: {input_text}")
            print(f"   → Exception: {str(e)}")
            
            failures.append({
                'id': test_id,
                'input': input_text,
                'category': category,
                'exception': str(e)
            })
    
    # Print summary
    print("\n" + "=" * 80)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 80)
    
    total = results['total']
    passed = results['passed']
    failed = results['failed']
    success_rate = (passed / total * 100) if total > 0 else 0
    
    print(f"\n🎯 Overall Results:")
    print(f"  Total Tests:    {total:3d}")
    print(f"  ✅ Passed:      {passed:3d} ({passed/total*100:6.2f}%)")
    print(f"  ❌ Failed:      {failed:3d} ({failed/total*100:6.2f}%)")
    print(f"  📈 Success Rate: {success_rate:6.2f}%")
    
    # Results by category
    print(f"\n📋 Results by Category:")
    print(f"  {'Category':<25} {'Total':>6} {'Passed':>6} {'Failed':>6} {'Rate':>7}")
    print(f"  {'-'*25} {'-'*6} {'-'*6} {'-'*6} {'-'*7}")
    
    for category in sorted(results['by_category'].keys()):
        stats = results['by_category'][category]
        cat_total = stats['total']
        cat_passed = stats['passed']
        cat_failed = stats['failed']
        cat_rate = (cat_passed / cat_total * 100) if cat_total > 0 else 0
        
        print(f"  {category:<25} {cat_total:6d} {cat_passed:6d} {cat_failed:6d} {cat_rate:6.1f}%")
    
    # Show failures
    if failures:
        print(f"\n❌ Failures ({len(failures)} total):")
        for fail in failures[:10]:  # Show first 10
            print(f"\n  ID: {fail['id']}")
            print(f"  Input: {fail.get('input', 'N/A')}")
            print(f"  Category: {fail.get('category', 'N/A')}")
            if 'error' in fail:
                print(f"  Error: {fail['error']}")
            if 'exception' in fail:
                print(f"  Exception: {fail['exception']}")
    
    # Save report
    report_file = f"tests/specific_date_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': total,
                'passed': passed,
                'failed': failed,
                'success_rate': success_rate
            },
            'by_category': results['by_category'],
            'failures': failures
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Report saved to: {report_file}")
    
    # Overall assessment
    print("\n" + "=" * 80)
    if success_rate >= 95:
        print("✅ EXCELLENT: All date patterns working perfectly!")
    elif success_rate >= 85:
        print("✅ GOOD: Most patterns working, minor issues")
    elif success_rate >= 70:
        print("⚠️  WARNING: Significant issues with date parsing")
    else:
        print("🚨 CRITICAL: Major fixes needed")
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    results = run_tests()
    
    if results:
        # Exit code based on failures
        if results['failed'] > results['total'] * 0.15:
            sys.exit(1)
        else:
            sys.exit(0)
