#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Run 1000 comprehensive test cases on Hybrid NLP Pipeline
Identify issues and generate detailed report
"""

import json
import sys
import os
from datetime import datetime
from collections import defaultdict

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core_nlp.hybrid_pipeline import HybridNLPPipeline

def validate_result(result, expected_fields=None, should_fail=False):
    """
    Validate NLP result
    Returns: (is_valid, error_message)
    """
    if should_fail:
        # For cases that SHOULD fail
        if not result or result.get('event_name') is None:
            return True, "Correctly failed (as expected)"
        else:
            return False, f"Should fail but got: {result.get('event_name')}"
    
    # Check basic structure
    if not isinstance(result, dict):
        return False, f"Result not a dict: {type(result)}"
    
    # Check for event_name key (not 'event')
    if 'event' in result and 'event_name' not in result:
        return False, "❌ CRITICAL: Result has 'event' key instead of 'event_name'"
    
    if 'event_name' not in result:
        return False, "Missing 'event_name' key"
    
    # Check event_name is not None/empty
    event_name = result.get('event_name')
    if not event_name or event_name.strip() == '':
        return False, "event_name is None or empty"
    
    # Check start_time if expected
    if expected_fields and 'start_time' in expected_fields:
        if not result.get('start_time'):
            return False, "Missing or None start_time"
    
    # Check location if expected
    if expected_fields and 'location' in expected_fields:
        if not result.get('location'):
            return False, "Missing expected location"
    
    # Check reminder if expected
    if expected_fields and 'reminder_minutes' in expected_fields:
        reminder = result.get('reminder_minutes')
        if reminder is None or reminder == 0:
            return False, "Missing expected reminder"
    
    return True, "OK"

def run_tests():
    """Run all 1000 test cases"""
    
    # Set UTF-8 encoding for Windows console
    import sys
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    
    print("=" * 80)
    print("🔬 HYBRID NLP PIPELINE - 1000 TEST CASES")
    print("=" * 80)
    
    # Load test cases
    test_file = "tests/hybrid_test_1000_cases.json"
    print(f"\n📂 Loading test cases from: {test_file}")
    
    try:
        with open(test_file, 'r', encoding='utf-8') as f:
            test_cases = json.load(f)
    except FileNotFoundError:
        print(f"❌ Test file not found: {test_file}")
        print("💡 Run: python tests/generate_1000_test_cases.py first")
        return
    
    print(f"✅ Loaded {len(test_cases)} test cases\n")
    
    # Initialize pipeline
    print("🔥 Initializing Hybrid NLP Pipeline...")
    try:
        pipeline = HybridNLPPipeline()
        print("✅ Pipeline ready\n")
    except Exception as e:
        print(f"❌ Failed to initialize pipeline: {e}")
        return
    
    # Results tracking
    results = {
        'total': 0,
        'passed': 0,
        'failed': 0,
        'errors': 0,
        'by_category': defaultdict(lambda: {'total': 0, 'passed': 0, 'failed': 0, 'errors': 0}),
        'failures': [],
        'critical_issues': [],
        'performance': []
    }
    
    print("🧪 Running tests...\n")
    
    # Run tests
    for i, test_case in enumerate(test_cases, 1):
        test_id = test_case.get('id', f'test_{i}')
        input_text = test_case.get('input', '')
        category = test_case.get('category', 'unknown')
        expected_fields = test_case.get('expected_fields', [])
        should_fail = test_case.get('should_fail', False)
        
        results['total'] += 1
        results['by_category'][category]['total'] += 1
        
        # Progress indicator (every 100 tests)
        if i % 100 == 0:
            print(f"  Progress: {i}/{len(test_cases)} tests completed...")
        
        try:
            # Run NLP
            start_time = datetime.now()
            result = pipeline.process(input_text)
            duration_ms = (datetime.now() - start_time).total_seconds() * 1000
            
            results['performance'].append(duration_ms)
            
            # Validate result
            is_valid, error_msg = validate_result(result, expected_fields, should_fail)
            
            if is_valid:
                results['passed'] += 1
                results['by_category'][category]['passed'] += 1
            else:
                results['failed'] += 1
                results['by_category'][category]['failed'] += 1
                
                failure_info = {
                    'id': test_id,
                    'category': category,
                    'input': input_text,
                    'error': error_msg,
                    'result': result
                }
                results['failures'].append(failure_info)
                
                # Check for critical issues (wrong key)
                if 'event_name' in error_msg and 'event' in error_msg:
                    results['critical_issues'].append(failure_info)
        
        except Exception as e:
            results['errors'] += 1
            results['by_category'][category]['errors'] += 1
            
            error_info = {
                'id': test_id,
                'category': category,
                'input': input_text,
                'exception': str(e),
                'type': type(e).__name__
            }
            results['failures'].append(error_info)
    
    # Print results
    print("\n" + "=" * 80)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 80)
    
    total = results['total']
    passed = results['passed']
    failed = results['failed']
    errors = results['errors']
    
    success_rate = (passed / total * 100) if total > 0 else 0
    
    print(f"\n🎯 Overall Results:")
    print(f"  Total Tests:    {total:5d}")
    print(f"  ✅ Passed:      {passed:5d} ({passed/total*100:6.2f}%)")
    print(f"  ❌ Failed:      {failed:5d} ({failed/total*100:6.2f}%)")
    print(f"  ⚠️  Errors:      {errors:5d} ({errors/total*100:6.2f}%)")
    print(f"  📈 Success Rate: {success_rate:6.2f}%")
    
    # Performance stats
    if results['performance']:
        avg_time = sum(results['performance']) / len(results['performance'])
        min_time = min(results['performance'])
        max_time = max(results['performance'])
        
        print(f"\n⚡ Performance:")
        print(f"  Average: {avg_time:7.2f} ms")
        print(f"  Min:     {min_time:7.2f} ms")
        print(f"  Max:     {max_time:7.2f} ms")
    
    # Results by category
    print(f"\n📋 Results by Category:")
    print(f"  {'Category':<20} {'Total':>6} {'Passed':>6} {'Failed':>6} {'Errors':>6} {'Rate':>7}")
    print(f"  {'-'*20} {'-'*6} {'-'*6} {'-'*6} {'-'*6} {'-'*7}")
    
    for category in sorted(results['by_category'].keys()):
        stats = results['by_category'][category]
        cat_total = stats['total']
        cat_passed = stats['passed']
        cat_failed = stats['failed']
        cat_errors = stats['errors']
        cat_rate = (cat_passed / cat_total * 100) if cat_total > 0 else 0
        
        print(f"  {category:<20} {cat_total:6d} {cat_passed:6d} {cat_failed:6d} {cat_errors:6d} {cat_rate:6.1f}%")
    
    # Critical issues
    if results['critical_issues']:
        print(f"\n🚨 CRITICAL ISSUES FOUND: {len(results['critical_issues'])}")
        print("  These issues require immediate attention!")
        for issue in results['critical_issues'][:5]:  # Show first 5
            print(f"\n  ID: {issue['id']}")
            print(f"  Input: {issue['input']}")
            print(f"  Error: {issue['error']}")
            if 'result' in issue:
                print(f"  Result: {issue['result']}")
    
    # Sample failures
    if results['failures'] and not results['critical_issues']:
        print(f"\n❌ Sample Failures ({min(10, len(results['failures']))} of {len(results['failures'])}):")
        for failure in results['failures'][:10]:
            print(f"\n  ID: {failure['id']}")
            print(f"  Category: {failure.get('category', 'N/A')}")
            print(f"  Input: {failure.get('input', 'N/A')}")
            if 'error' in failure:
                print(f"  Error: {failure['error']}")
            if 'exception' in failure:
                print(f"  Exception: {failure['type']}: {failure['exception']}")
    
    # Save detailed report
    report_file = f"tests/hybrid_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_file, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total': total,
                'passed': passed,
                'failed': failed,
                'errors': errors,
                'success_rate': success_rate
            },
            'by_category': dict(results['by_category']),
            'performance': {
                'avg_ms': sum(results['performance']) / len(results['performance']) if results['performance'] else 0,
                'min_ms': min(results['performance']) if results['performance'] else 0,
                'max_ms': max(results['performance']) if results['performance'] else 0
            },
            'failures': results['failures'][:100],  # First 100 failures
            'critical_issues': results['critical_issues']
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 Detailed report saved to: {report_file}")
    
    # Overall assessment
    print("\n" + "=" * 80)
    if success_rate >= 95:
        print("✅ EXCELLENT: Pipeline is working very well!")
    elif success_rate >= 85:
        print("✅ GOOD: Pipeline is mostly working, minor issues to fix")
    elif success_rate >= 70:
        print("⚠️  WARNING: Pipeline has significant issues")
    else:
        print("🚨 CRITICAL: Pipeline needs major fixes")
    
    if results['critical_issues']:
        print(f"🚨 {len(results['critical_issues'])} CRITICAL ISSUES require immediate attention!")
    
    print("=" * 80)
    
    return results

if __name__ == "__main__":
    results = run_tests()
    
    # Exit code based on critical issues
    if results and results['critical_issues']:
        sys.exit(1)
    elif results and results['failed'] + results['errors'] > results['total'] * 0.15:
        sys.exit(1)
    else:
        sys.exit(0)
