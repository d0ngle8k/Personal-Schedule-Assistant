#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Compare Rule-based vs Hybrid Pipeline performance
"""

import json
from pathlib import Path

def main():
    test_dir = Path(__file__).parent
    
    # Find the latest reports
    rule_reports = sorted(test_dir.glob("comprehensive_test_report_*.json"), reverse=True)
    hybrid_reports = sorted(test_dir.glob("hybrid_comprehensive_test_report_*.json"), reverse=True)
    
    if not rule_reports:
        print("❌ No rule-based test report found!")
        return
    
    if not hybrid_reports:
        print("❌ No hybrid test report found!")
        return
    
    rule_report_path = rule_reports[0]
    hybrid_report_path = hybrid_reports[0]
    
    print("="*80)
    print("PIPELINE COMPARISON: Rule-based vs Hybrid")
    print("="*80)
    print(f"\nRule-based Report: {rule_report_path.name}")
    print(f"Hybrid Report: {hybrid_report_path.name}")
    
    # Load reports
    with open(rule_report_path, 'r', encoding='utf-8') as f:
        rule_data = json.load(f)
    
    with open(hybrid_report_path, 'r', encoding='utf-8') as f:
        hybrid_data = json.load(f)
    
    # Extract stats
    rule_stats = rule_data['total_stats']
    hybrid_stats = hybrid_data['total_stats']
    
    # Overall comparison
    print("\n" + "="*80)
    print("OVERALL STATISTICS")
    print("="*80)
    
    print(f"\n{'Metric':<30} {'Rule-based':<15} {'Hybrid':<15} {'Difference':<15}")
    print("-"*80)
    
    # Total cases
    print(f"{'Total Test Cases':<30} {rule_stats['total_cases']:<15} {hybrid_stats['total_cases']:<15} {'-':<15}")
    
    # Passed
    rule_passed = rule_stats['total_passed']
    hybrid_passed = hybrid_stats['total_passed']
    diff_passed = hybrid_passed - rule_passed
    symbol = "✅" if diff_passed > 0 else "❌" if diff_passed < 0 else "="
    print(f"{'Passed':<30} {rule_passed:<15} {hybrid_passed:<15} {diff_passed:+d} {symbol}")
    
    # Failed
    rule_failed = rule_stats['total_failed']
    hybrid_failed = hybrid_stats['total_failed']
    diff_failed = hybrid_failed - rule_failed
    symbol = "✅" if diff_failed < 0 else "❌" if diff_failed > 0 else "="
    print(f"{'Failed':<30} {rule_failed:<15} {hybrid_failed:<15} {diff_failed:+d} {symbol}")
    
    # Accuracy
    rule_acc = (rule_passed / rule_stats['total_cases']) * 100 if rule_stats['total_cases'] > 0 else 0
    hybrid_acc = (hybrid_passed / hybrid_stats['total_cases']) * 100 if hybrid_stats['total_cases'] > 0 else 0
    diff_acc = hybrid_acc - rule_acc
    symbol = "✅" if diff_acc > 0 else "❌" if diff_acc < 0 else "="
    print(f"{'Overall Accuracy':<30} {rule_acc:.2f}%{'':<9} {hybrid_acc:.2f}%{'':<9} {diff_acc:+.2f}% {symbol}")
    
    # Field comparison
    print("\n" + "="*80)
    print("FIELD-BY-FIELD COMPARISON")
    print("="*80)
    
    print(f"\n{'Field':<20} {'Rule-based':<20} {'Hybrid':<20} {'Difference':<15}")
    print("-"*80)
    
    field_accuracies_rule = []
    field_accuracies_hybrid = []
    
    for field in ['event', 'time_str', 'location', 'reminder_minutes']:
        rule_field = rule_stats['field_totals'][field]
        hybrid_field = hybrid_stats['field_totals'][field]
        
        rule_field_acc = (rule_field['correct'] / rule_field['total']) * 100 if rule_field['total'] > 0 else 0
        hybrid_field_acc = (hybrid_field['correct'] / hybrid_field['total']) * 100 if hybrid_field['total'] > 0 else 0
        
        field_accuracies_rule.append(rule_field_acc)
        field_accuracies_hybrid.append(hybrid_field_acc)
        
        diff = hybrid_field_acc - rule_field_acc
        symbol = "✅" if diff > 0 else "❌" if diff < 0 else "="
        
        print(f"{field:<20} {rule_field_acc:.2f}%{'':<14} {hybrid_field_acc:.2f}%{'':<14} {diff:+.2f}% {symbol}")
    
    # Macro F1
    rule_macro = sum(field_accuracies_rule) / len(field_accuracies_rule) if field_accuracies_rule else 0
    hybrid_macro = sum(field_accuracies_hybrid) / len(field_accuracies_hybrid) if field_accuracies_hybrid else 0
    diff_macro = hybrid_macro - rule_macro
    symbol = "✅" if diff_macro > 0 else "❌" if diff_macro < 0 else "="
    
    print("-"*80)
    print(f"{'Macro F1 Score':<20} {rule_macro:.2f}%{'':<14} {hybrid_macro:.2f}%{'':<14} {diff_macro:+.2f}% {symbol}")
    
    # Summary
    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    
    if hybrid_acc > rule_acc:
        print(f"\n✅ HYBRID PIPELINE is BETTER by {diff_acc:.2f}%")
    elif hybrid_acc < rule_acc:
        print(f"\n❌ RULE-BASED PIPELINE is BETTER by {abs(diff_acc):.2f}%")
    else:
        print(f"\n= BOTH PIPELINES have EQUAL performance")
    
    print(f"\nHybrid improvements:")
    improvements = []
    regressions = []
    
    for field in ['event', 'time_str', 'location', 'reminder_minutes']:
        rule_field = rule_stats['field_totals'][field]
        hybrid_field = hybrid_stats['field_totals'][field]
        
        rule_field_acc = (rule_field['correct'] / rule_field['total']) * 100 if rule_field['total'] > 0 else 0
        hybrid_field_acc = (hybrid_field['correct'] / hybrid_field['total']) * 100 if hybrid_field['total'] > 0 else 0
        
        diff = hybrid_field_acc - rule_field_acc
        
        if diff > 0:
            improvements.append(f"  ✅ {field}: +{diff:.2f}%")
        elif diff < 0:
            regressions.append(f"  ❌ {field}: {diff:.2f}%")
    
    if improvements:
        print("\nImprovements:")
        for imp in improvements:
            print(imp)
    
    if regressions:
        print("\nRegressions:")
        for reg in regressions:
            print(reg)
    
    print("\n" + "="*80)

if __name__ == '__main__':
    main()
