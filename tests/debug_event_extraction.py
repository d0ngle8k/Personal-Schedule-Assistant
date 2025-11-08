"""
Deep debug for event extraction
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from core_nlp.pipeline import NLPPipeline

def debug_pipeline():
    pipeline = NLPPipeline()
    
    text = "toi di bao ve luan van ngay 20 thang 11 nam 2026 tai dai hoc sai gon"
    
    print("="*80)
    print("DEBUG: Event Extraction Pipeline")
    print("="*80)
    print(f"Input: {text}")
    print("\n" + "-"*80)
    
    # Process
    result = pipeline.process(text)
    
    print("\n📊 FINAL RESULT:")
    print("-"*80)
    for key, value in result.items():
        print(f"{key:20s}: {value}")
    
    print("\n" + "="*80)
    
    # Test _extract_entities_regex directly
    print("\n🔍 INTERNAL EXTRACTION TEST:")
    print("-"*80)
    
    text_lower = text.lower()
    ex = pipeline._extract_entities_regex(text_lower)
    
    print(f"time_str:   {ex.get('time_str')}")
    print(f"location:   {ex.get('location')}")
    print(f"event_name: {ex.get('event_name')}")
    
    print("\n" + "="*80)

if __name__ == "__main__":
    debug_pipeline()
