"""
Augment training data by merging comprehensive 100K dataset with existing data
Prepare final dataset for PhoBERT fine-tuning
"""

import json
import random
from pathlib import Path

def load_json(filepath):
    """Load JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"⚠️  File not found: {filepath}")
        return []

def save_json(data, filepath):
    """Save JSON file"""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"💾 Saved {len(data):,} samples to {filepath}")

def normalize_sample(sample):
    """Normalize sample to standard format"""
    return {
        "id": sample.get("id", 0),
        "text": sample.get("text", ""),
        "event": sample.get("event", sample.get("event_name", "")),
        "start_time": sample.get("start_time"),
        "end_time": sample.get("end_time"),
        "location": sample.get("location"),
        "reminder_minutes": sample.get("reminder_minutes", 0)
    }

def deduplicate(samples):
    """Remove duplicate texts"""
    seen_texts = set()
    unique = []
    
    for sample in samples:
        text_lower = sample["text"].lower().strip()
        if text_lower not in seen_texts:
            seen_texts.add(text_lower)
            unique.append(sample)
    
    return unique

def main():
    print("🔄 Augmenting training data with comprehensive 100K dataset...")
    print("=" * 70)
    
    # Load datasets
    datasets = {
        "comprehensive_100k": "tests/training_100k_comprehensive.json",
        "existing_10k": "tests/extended_test_cases_10000.json",
        "existing_100k": "tests/extended_test_cases_100000.json",
        "base_cases": "tests/test_cases.json",
    }
    
    all_samples = []
    
    for name, filepath in datasets.items():
        data = load_json(filepath)
        if data:
            # Normalize samples
            normalized = [normalize_sample(s) for s in data]
            all_samples.extend(normalized)
            print(f"✅ Loaded {len(normalized):,} samples from {name}")
    
    print(f"\n📊 Total samples before deduplication: {len(all_samples):,}")
    
    # Deduplicate
    unique_samples = deduplicate(all_samples)
    print(f"📊 Unique samples after deduplication: {len(unique_samples):,}")
    print(f"🗑️  Removed {len(all_samples) - len(unique_samples):,} duplicates")
    
    # Shuffle
    random.shuffle(unique_samples)
    
    # Re-assign IDs
    for i, sample in enumerate(unique_samples):
        sample['id'] = i + 1
    
    # Statistics
    print("\n📈 FINAL DATASET STATISTICS:")
    reminder_count = sum(1 for s in unique_samples if s['reminder_minutes'] > 0)
    location_count = sum(1 for s in unique_samples if s['location'])
    
    # Reminder breakdown
    minute_reminders = sum(1 for s in unique_samples if 0 < s['reminder_minutes'] < 60)
    hour_reminders = sum(1 for s in unique_samples if 60 <= s['reminder_minutes'] < 1440)
    day_reminders = sum(1 for s in unique_samples if 1440 <= s['reminder_minutes'] < 10080)
    week_reminders = sum(1 for s in unique_samples if 10080 <= s['reminder_minutes'] < 43200)
    month_reminders = sum(1 for s in unique_samples if s['reminder_minutes'] >= 43200)
    
    print(f"   - Total samples: {len(unique_samples):,}")
    print(f"   - With reminders: {reminder_count:,} ({reminder_count/len(unique_samples)*100:.1f}%)")
    print(f"   - With locations: {location_count:,} ({location_count/len(unique_samples)*100:.1f}%)")
    print(f"\n   Reminder breakdown:")
    print(f"   - Minutes (1-59 min): {minute_reminders:,}")
    print(f"   - Hours (1-23 hours): {hour_reminders:,}")
    print(f"   - Days (1-6 days): {day_reminders:,}")
    print(f"   - Weeks (1+ weeks): {week_reminders:,}")
    print(f"   - Months (1+ months): {month_reminders:,}")
    
    # Save augmented dataset
    output_file = "training_data/phobert_training_augmented.json"
    save_json(unique_samples, output_file)
    
    # Also create train/validation split (90/10)
    split_idx = int(len(unique_samples) * 0.9)
    train_data = unique_samples[:split_idx]
    val_data = unique_samples[split_idx:]
    
    save_json(train_data, "training_data/phobert_train.json")
    save_json(val_data, "training_data/phobert_validation.json")
    
    print(f"\n📊 Split into:")
    print(f"   - Training: {len(train_data):,} samples (90%)")
    print(f"   - Validation: {len(val_data):,} samples (10%)")
    
    # Sample preview
    print("\n📋 RANDOM SAMPLES WITH WEEK/MONTH REMINDERS:")
    week_month_samples = [s for s in unique_samples if s['reminder_minutes'] >= 10080]
    for sample in random.sample(week_month_samples, min(5, len(week_month_samples))):
        reminder_display = f"{sample['reminder_minutes']} min"
        if sample['reminder_minutes'] >= 43200:
            reminder_display += f" ({sample['reminder_minutes'] // 43200} months)"
        elif sample['reminder_minutes'] >= 10080:
            reminder_display += f" ({sample['reminder_minutes'] // 10080} weeks)"
        
        print(f"   - {sample['text']}")
        print(f"     → Reminder: {reminder_display}, Location: {sample['location']}")
    
    print("\n" + "=" * 70)
    print("✅ Augmentation complete! Ready for PhoBERT training.")

if __name__ == "__main__":
    main()
