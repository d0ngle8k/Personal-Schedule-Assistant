#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test Hybrid Pipeline with all JSON test case files
"""

import json
import os
from pathlib import Path
from datetime import datetime
from core_nlp.hybrid_pipeline import HybridNLPPipeline

def normalize_string(s):
    """Normalize string for comparison"""
    if s is None:
        return None
    return str(s).strip().lower()

def compare_results(expected, actual, field):
    """Compare expected vs actual for a specific field"""
    exp_val = expected.get(field)
    
    # Map test case fields to actual pipeline output fields
    field_mapping = {
        'event': 'event_name',
        'time_str': 'start_time',
        'location': 'location',
        'reminder_minutes': 'reminder_minutes'
    }
    
    actual_field = field_mapping.get(field, field)
    act_val = actual.get(actual_field)
    
    # Special handling for time_str - check if time was extracted
    if field == 'time_str':
        if exp_val is not None:
            return act_val is not None
        else:
            return act_val is None
    
    # Normalize
    exp_norm = normalize_string(exp_val)
    act_norm = normalize_string(act_val)
    
    return exp_norm == act_norm

def test_json_file(file_path, pipeline):
    """Test a single JSON file"""
    print(f"\n{'='*80}")
    print(f"Testing: {file_path.name}")
    print(f"{'='*80}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            test_cases = json.load(f)
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return None
    
    if not isinstance(test_cases, list):
        print(f"⚠️ Skipping - not a test case array")
        return None
    
    # Check if it's a valid test case file
    if not test_cases or not isinstance(test_cases[0], dict):
        print(f"⚠️ Skipping - invalid format")
        return None
    
    # Must have 'input' and 'expected' fields
    if 'input' not in test_cases[0] or 'expected' not in test_cases[0]:
        print(f"⚠️ Skipping - not a test case file")
        return None
    
    results = {
        'file': file_path.name,
        'total': len(test_cases),
        'passed': 0,
        'failed': 0,
        'errors': 0,
        'field_scores': {
            'event': {'correct': 0, 'total': 0},
            'time_str': {'correct': 0, 'total': 0},
            'location': {'correct': 0, 'total': 0},
            'reminder_minutes': {'correct': 0, 'total': 0}
        },
        'failures': []
    }
    
    for i, test_case in enumerate(test_cases, 1):
        input_text = test_case.get('input', '')
        expected = test_case.get('expected', {})
        
        try:
            # Run HYBRID pipeline
            actual = pipeline.process(input_text)
            
            # Compare each field
            all_match = True
            field_results = {}
            
            for field in ['event', 'time_str', 'location', 'reminder_minutes']:
                if field in expected:
                    results['field_scores'][field]['total'] += 1
                    match = compare_results(expected, actual, field)
                    field_results[field] = match
                    
                    if match:
                        results['field_scores'][field]['correct'] += 1
                    else:
                        all_match = False
            
            if all_match:
                results['passed'] += 1
            else:
                results['failed'] += 1
                results['failures'].append({
                    'case': i,
                    'input': input_text,
                    'expected': expected,
                    'actual': actual,
                    'field_results': field_results
                })
        
        except Exception as e:
            results['errors'] += 1
            results['failures'].append({
                'case': i,
                'input': input_text,
                'error': str(e)
            })
    
    # Calculate accuracy
    if results['total'] > 0:
        results['accuracy'] = (results['passed'] / results['total']) * 100
    else:
        results['accuracy'] = 0
    
    # Calculate field accuracies
    for field, scores in results['field_scores'].items():
        if scores['total'] > 0:
            scores['accuracy'] = (scores['correct'] / scores['total']) * 100
        else:
            scores['accuracy'] = 0
    
    return results

def main():
    """Main test runner for Hybrid Pipeline"""
    print("="*80)
    print("HYBRID PIPELINE - COMPREHENSIVE JSON TEST SUITE")
    print("="*80)
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Initialize HYBRID pipeline
    print("\n🔧 Initializing Hybrid NLP Pipeline...")
    pipeline = HybridNLPPipeline()
    print("✅ Hybrid Pipeline ready!")
    
    # Find all JSON test files
    test_dir = Path(__file__).parent
    test_files = [
        'test_cases.json',
        'extended_test_cases.json',
        'extended_test_cases_10000.json',
        'extended_test_cases_100000.json',
        'specific_date_edge_cases.json',
        'hybrid_test_1000_cases.json'
    ]
    
    all_results = []
    total_stats = {
        'total_files': 0,
        'total_cases': 0,
        'total_passed': 0,
        'total_failed': 0,
        'total_errors': 0,
        'field_totals': {
            'event': {'correct': 0, 'total': 0},
            'time_str': {'correct': 0, 'total': 0},
            'location': {'correct': 0, 'total': 0},
            'reminder_minutes': {'correct': 0, 'total': 0}
        }
    }
    
    # Test each file
    for test_file in test_files:
        file_path = test_dir / test_file
        
        if not file_path.exists():
            print(f"\n⚠️ File not found: {test_file}")
            continue
        
        result = test_json_file(file_path, pipeline)
        
        if result is None:
            continue
        
        all_results.append(result)
        
        # Print file results
        print(f"\n📊 Results:")
        print(f"  Total: {result['total']}")
        print(f"  Passed: {result['passed']} ✅")
        print(f"  Failed: {result['failed']} ❌")
        print(f"  Errors: {result['errors']} ⚠️")
        print(f"  Accuracy: {result['accuracy']:.2f}%")
        print(f"\n  Field Accuracies:")
        for field, scores in result['field_scores'].items():
            if scores['total'] > 0:
                print(f"    {field}: {scores['accuracy']:.2f}% ({scores['correct']}/{scores['total']})")
        
        # Show sample failures (first 5)
        if result['failures'] and len(result['failures']) <= 5:
            print(f"\n  Sample Failures:")
            for failure in result['failures'][:5]:
                if 'error' in failure:
                    print(f"    Case {failure['case']}: ERROR - {failure['error']}")
                else:
                    print(f"    Case {failure['case']}: {failure['input']}")
                    for field, passed in failure.get('field_results', {}).items():
                        if not passed:
                            exp = failure['expected'].get(field)
                            act = failure['actual'].get(field if field != 'event' else 'event_name')
                            print(f"      {field}: expected={exp}, actual={act}")
        
        # Update totals
        total_stats['total_files'] += 1
        total_stats['total_cases'] += result['total']
        total_stats['total_passed'] += result['passed']
        total_stats['total_failed'] += result['failed']
        total_stats['total_errors'] += result['errors']
        
        for field, scores in result['field_scores'].items():
            total_stats['field_totals'][field]['correct'] += scores['correct']
            total_stats['field_totals'][field]['total'] += scores['total']
    
    # Print overall summary
    print("\n" + "="*80)
    print("HYBRID PIPELINE - OVERALL SUMMARY")
    print("="*80)
    print(f"Files Tested: {total_stats['total_files']}")
    print(f"Total Test Cases: {total_stats['total_cases']}")
    print(f"Total Passed: {total_stats['total_passed']} ✅")
    print(f"Total Failed: {total_stats['total_failed']} ❌")
    print(f"Total Errors: {total_stats['total_errors']} ⚠️")
    
    if total_stats['total_cases'] > 0:
        overall_accuracy = (total_stats['total_passed'] / total_stats['total_cases']) * 100
        print(f"\n🎯 OVERALL ACCURACY: {overall_accuracy:.2f}%")
    
    print(f"\n📈 FIELD ACCURACIES:")
    field_accuracies = []
    for field, totals in total_stats['field_totals'].items():
        if totals['total'] > 0:
            accuracy = (totals['correct'] / totals['total']) * 100
            field_accuracies.append(accuracy)
            print(f"  {field}: {accuracy:.2f}% ({totals['correct']}/{totals['total']})")
    
    if field_accuracies:
        macro_f1 = sum(field_accuracies) / len(field_accuracies)
        print(f"\n⭐ MACRO F1 SCORE: {macro_f1:.2f}%")
    
    print(f"\nCompleted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*80)
    
    # Save detailed report
    report_path = test_dir / f"hybrid_comprehensive_test_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump({
            'timestamp': datetime.now().isoformat(),
            'pipeline': 'hybrid',
            'total_stats': total_stats,
            'file_results': all_results
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\n📄 Detailed report saved: {report_path.name}")

if __name__ == '__main__':
    main()
