"""
Comprehensive test for date parsing bug fix
Tests full NLP pipeline with various date formats
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from core_nlp.pipeline import NLPPipeline
from datetime import datetime
import json

def test_nlp_pipeline():
    """Test NLP pipeline with date formats"""
    
    print("="*80)
    print("NLP PIPELINE - DATE PARSING TEST")
    print("="*80)
    print(f"Current date: {datetime.now()}")
    print("="*80)
    
    # Initialize pipeline
    pipeline = NLPPipeline()
    
    # Test cases with expected results
    test_cases = [
        {
            "input": "toi di bao ve luan van ngay 20 thang 11 nam 2026 tai dai hoc sai gon",
            "expected_date": "2026-11-20",
            "expected_event": "bảo vệ luận văn",
            "expected_location": "dai hoc sai gon"  # Input doesn't have diacritics, so output won't either
        },
        {
            "input": "bảo vệ luận văn ngày 20 tháng 11 năm 2026 lúc 9h sáng tại đại học sài gòn",
            "expected_date": "2026-11-20",
            "expected_time": "09:00",
            "expected_event": "bảo vệ luận văn",
            "expected_location": "đại học sài gòn"
        },
        {
            "input": "họp với giáo viên hướng dẫn ngày 15 tháng 12 năm 2025",
            "expected_date": "2025-12-15",
            "expected_time": "00:00",  # CRITICAL FIX: Default time when no specific time given
            "expected_event": "họp với giáo viên hướng dẫn",
            "expected_location": None  # CRITICAL FIX: No location marker, shouldn't extract "năm 2025"
        },
        {
            "input": "nộp báo cáo ngày 1 tháng 1 năm 2027",
            "expected_date": "2027-01-01",
            "expected_time": "00:00",  # CRITICAL FIX: Default time when no specific time given
            "expected_event": "nộp báo cáo",
            "expected_location": None  # CRITICAL FIX: No location marker, shouldn't extract "tháng 1"
        },
        {
            "input": "đi du lịch ngày 25 tháng 6 năm 2026 nhắc trước 3 ngày",
            "expected_date": "2026-06-25",
            "expected_event": "đi du lịch",
            "expected_reminder": True
        },
        {
            "input": "thi cuối kỳ ngày 30/12/2025 lúc 7h30 sáng",
            "expected_date": "2025-12-30",
            "expected_time": "07:30",
            "expected_event": "thi cuối kỳ"
        },
        {
            "input": "sinh nhật bạn ngày 5 tháng 3",
            "expected_month": "03",
            "expected_day": "05",
            "expected_time": "00:00",  # CRITICAL FIX: Default time when no specific time given
            "expected_event": "sinh nhật bạn",
            "expected_location": None  # CRITICAL FIX: No location marker, shouldn't extract "tháng 3"
        },
    ]
    
    passed = 0
    failed = 0
    
    for i, test in enumerate(test_cases, 1):
        print(f"\n{'-'*80}")
        print(f"Test Case {i}:")
        print(f"Input: {test['input']}")
        print("-"*40)
        
        result = pipeline.process(test['input'])
        
        # Check results
        success = True
        errors = []
        
        # Check event extraction
        if 'expected_event' in test:
            # Pipeline returns 'event_name' not 'event'
            extracted_event = result.get('event_name', '') or result.get('event', '')
            # Normalize for comparison (remove diacritics for flexible matching)
            import unicodedata
            def normalize_text(s):
                # Remove diacritics and convert to lowercase
                s = unicodedata.normalize('NFD', s)
                s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
                return s.lower().strip()
            
            if normalize_text(extracted_event) != normalize_text(test['expected_event']):
                success = False
                errors.append(f"Event mismatch: got '{extracted_event}', expected '{test['expected_event']}'")
        
        # Check date
        if 'expected_date' in test:
            extracted_date = result.get('start_time', '')[:10] if result.get('start_time') else ''
            if extracted_date != test['expected_date']:
                success = False
                errors.append(f"Date mismatch: got '{extracted_date}', expected '{test['expected_date']}'")
        
        # Check time
        if 'expected_time' in test:
            extracted_time = result.get('start_time', '')[11:16] if result.get('start_time') and len(result.get('start_time')) > 11 else ''
            if extracted_time != test['expected_time']:
                success = False
                errors.append(f"Time mismatch: got '{extracted_time}', expected '{test['expected_time']}'")
        
        # Check location
        if 'expected_location' in test:
            extracted_location = result.get('location', '')
            
            # Handle None expectation (location should be empty/None)
            if test['expected_location'] is None:
                if extracted_location and extracted_location.strip():
                    success = False
                    errors.append(f"Location should be empty, got '{extracted_location}'")
            else:
                # Normalize for comparison
                import unicodedata
                def normalize_text(s):
                    s = unicodedata.normalize('NFD', s)
                    s = ''.join(c for c in s if unicodedata.category(c) != 'Mn')
                    return s.lower().strip()
                
                if normalize_text(extracted_location) != normalize_text(test['expected_location']):
                    success = False
                    errors.append(f"Location mismatch: got '{extracted_location}', expected '{test['expected_location']}'")
        
        # Check reminder
        if 'expected_reminder' in test:
            if not result.get('reminder_minutes') or result.get('reminder_minutes') == 0:
                success = False
                errors.append("Reminder not extracted")
        
        # Display result
        if success:
            print("[PASS]")
            passed += 1
        else:
            print("[FAIL]")
            failed += 1
            for error in errors:
                print(f"   - {error}")
        
        print(f"\nExtracted:")
        print(f"   Event:      {result.get('event_name', 'N/A')}")
        print(f"   Start Time: {result.get('start_time', 'N/A')}")
        print(f"   End Time:   {result.get('end_time', 'N/A')}")
        print(f"   Location:   {result.get('location', 'N/A')}")
        print(f"   Reminder:   {result.get('reminder_minutes', 'N/A')}")
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    print(f"Total:  {len(test_cases)}")
    print(f"Pass: {passed}")
    print(f"Fail: {failed}")
    print(f"Success Rate: {passed/len(test_cases)*100:.1f}%")
    print("="*80)
    
    # Save detailed results
    results_file = "test_date_parsing_results.json"
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump({
            "test_date": datetime.now().isoformat(),
            "total": len(test_cases),
            "passed": passed,
            "failed": failed,
            "success_rate": f"{passed/len(test_cases)*100:.1f}%"
        }, f, indent=2, ensure_ascii=False)
    
    print(f"\nResults saved to: {results_file}")
    
    return passed == len(test_cases)

if __name__ == "__main__":
    success = test_nlp_pipeline()
    sys.exit(0 if success else 1)
