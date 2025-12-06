"""
Debug script for date parsing issue
Test case: "toi di bao ve luan van ngay 20 thang 11 nam 2026 tai dai hoc sai gon"
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from core_nlp.time_parser import parse_vietnamese_time_range
from datetime import datetime

def test_date_parsing():
    """Test the problematic prompt"""
    
    # Test case that's failing
    test_prompt = "toi di bao ve luan van ngay 20 thang 11 nam 2026 tai dai hoc sai gon"
    
    print("="*80)
    print("DEBUG: Date Parsing Issue")
    print("="*80)
    print(f"\nPrompt: {test_prompt}")
    print(f"Current date: {datetime.now()}")
    print("\n" + "-"*80)
    
    # Test with time parser
    result = parse_vietnamese_time_range(test_prompt)
    
    print("\n📊 PARSING RESULT:")
    print("-"*80)
    if result:
        start, end = result
        print(f"✅ SUCCESS - Extracted time:")
        print(f"   Start: {start}")
        print(f"   End:   {end}")
    else:
        print("❌ FAILED - No time extracted")
        print("\nPossible reasons:")
        print("1. Pattern 'ngay X thang Y nam Z' not recognized")
        print("2. Year 2026 is too far in future")
        print("3. Pattern priority issue")
        print("4. Regex not matching Vietnamese date format")
    
    print("\n" + "="*80)
    
    # Test variations
    print("\n🧪 TESTING VARIATIONS:")
    print("-"*80)
    
    variations = [
        "bảo vệ luận văn ngày 20 tháng 11 năm 2026",
        "bảo vệ luận văn 20/11/2026",
        "bảo vệ luận văn ngày 20-11-2026",
        "bảo vệ luận văn 20 tháng 11",
        "bảo vệ luận văn ngày 20/11",
    ]
    
    for i, variant in enumerate(variations, 1):
        result = parse_vietnamese_time_range(variant)
        status = "✅" if result else "❌"
        print(f"{status} Variant {i}: {variant}")
        if result:
            print(f"   → {result[0]}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    test_date_parsing()
