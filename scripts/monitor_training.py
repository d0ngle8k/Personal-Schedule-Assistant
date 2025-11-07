"""
Monitor PhoBERT Training Progress in Real-time
Usage: python scripts/monitor_training.py
"""

import time
import os
import sys
from pathlib import Path

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_terminal_size():
    """Get terminal size"""
    try:
        import shutil
        return shutil.get_terminal_size()
    except:
        return (80, 24)

def monitor_training(log_file="models/phobert_finetuned/training.log", interval=2):
    """
    Monitor training progress by tailing log file
    
    Args:
        log_file: Path to training log file
        interval: Update interval in seconds
    """
    print("🔍 PhoBERT Training Monitor")
    print("=" * 70)
    print(f"📁 Log file: {log_file}")
    print(f"🔄 Update interval: {interval}s")
    print("=" * 70)
    print("\n⌛ Waiting for training to start...")
    
    # Wait for log file to be created
    while not Path(log_file).exists():
        time.sleep(1)
        print(".", end="", flush=True)
    
    print("\n✅ Training started! Monitoring...\n")
    
    # Track last position in file
    last_position = 0
    last_lines = []
    epoch_info = {}
    
    try:
        while True:
            # Read new lines from log
            try:
                with open(log_file, 'r', encoding='utf-8') as f:
                    f.seek(last_position)
                    new_lines = f.readlines()
                    last_position = f.tell()
                    
                    if new_lines:
                        last_lines.extend(new_lines)
                        # Keep last 50 lines
                        last_lines = last_lines[-50:]
                        
                        # Parse epoch info
                        for line in new_lines:
                            if "Epoch" in line and "/" in line:
                                try:
                                    parts = line.split("Epoch")[1].split("/")
                                    current_epoch = int(parts[0].strip())
                                    total_epochs = int(parts[1].split()[0].strip())
                                    epoch_info['current'] = current_epoch
                                    epoch_info['total'] = total_epochs
                                except:
                                    pass
                            
                            if "Train Loss:" in line:
                                try:
                                    loss = float(line.split("Train Loss:")[1].split(",")[0].strip())
                                    epoch_info['train_loss'] = loss
                                except:
                                    pass
                            
                            if "Val Loss:" in line:
                                try:
                                    loss = float(line.split("Val Loss:")[1].split(",")[0].strip())
                                    epoch_info['val_loss'] = loss
                                except:
                                    pass
                            
                            if "Accuracy:" in line:
                                try:
                                    acc = float(line.split("Accuracy:")[1].strip().replace("%", ""))
                                    epoch_info['accuracy'] = acc
                                except:
                                    pass
                        
                        # Clear and redraw
                        clear_screen()
                        
                        print("🔍 PhoBERT Training Monitor")
                        print("=" * 70)
                        
                        # Show progress
                        if epoch_info:
                            if 'current' in epoch_info:
                                progress = (epoch_info['current'] / epoch_info['total']) * 100
                                bar_length = 40
                                filled = int(bar_length * progress / 100)
                                bar = "█" * filled + "░" * (bar_length - filled)
                                
                                print(f"\n📊 Progress: [{bar}] {progress:.1f}%")
                                print(f"   Epoch {epoch_info['current']}/{epoch_info['total']}")
                            
                            if 'train_loss' in epoch_info:
                                print(f"\n📉 Train Loss: {epoch_info['train_loss']:.4f}")
                            
                            if 'val_loss' in epoch_info:
                                print(f"📉 Val Loss: {epoch_info['val_loss']:.4f}")
                            
                            if 'accuracy' in epoch_info:
                                print(f"🎯 Accuracy: {epoch_info['accuracy']:.2f}%")
                        
                        print("\n" + "=" * 70)
                        print("📝 Recent Log Lines:")
                        print("-" * 70)
                        
                        # Show last 10 lines
                        for line in last_lines[-10:]:
                            print(line.rstrip())
                        
                        print("-" * 70)
                        print(f"\n🔄 Last update: {time.strftime('%H:%M:%S')}")
                        print("Press Ctrl+C to exit")
                        
            except FileNotFoundError:
                print("⚠️  Log file not found, waiting...")
            except Exception as e:
                print(f"⚠️  Error reading log: {e}")
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n\n👋 Monitoring stopped.")
        return

if __name__ == "__main__":
    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser(description="Monitor PhoBERT training progress")
    parser.add_argument("--log", default="models/phobert_finetuned/training.log", help="Path to log file")
    parser.add_argument("--interval", type=int, default=2, help="Update interval in seconds")
    
    args = parser.parse_args()
    
    monitor_training(args.log, args.interval)
