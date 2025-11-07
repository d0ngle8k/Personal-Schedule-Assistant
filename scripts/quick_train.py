"""
Quick Training Script với các preset cấu hình
Tự động chọn config phù hợp với hardware
"""

import argparse
import torch
import psutil
import os

def get_system_info():
    """Lấy thông tin hệ thống"""
    info = {
        'cpu_cores': os.cpu_count() or 1,
        'ram_gb': psutil.virtual_memory().total / (1024**3),
        'has_cuda': torch.cuda.is_available(),
        'gpu_count': torch.cuda.device_count() if torch.cuda.is_available() else 0,
    }
    
    if info['has_cuda']:
        info['gpu_name'] = torch.cuda.get_device_name(0)
        info['gpu_memory_gb'] = torch.cuda.get_device_properties(0).total_memory / (1024**3)
    
    return info

def recommend_config(system_info):
    """Recommend training config based on hardware"""
    
    if system_info['has_cuda']:
        gpu_mem = system_info['gpu_memory_gb']
        
        if gpu_mem >= 12:  # RTX 3080/3090, A100
            return {
                'batch_size': 32,
                'gradient_accumulation_steps': 1,
                'num_epochs': 40,
                'name': 'GPU High-end (12GB+)',
                'estimated_time': '30-60 phút'
            }
        elif gpu_mem >= 8:  # RTX 3060 Ti, RTX 3070
            return {
                'batch_size': 16,
                'gradient_accumulation_steps': 2,
                'num_epochs': 40,
                'name': 'GPU Mid-range (8GB)',
                'estimated_time': '1-1.5 giờ'
            }
        else:  # GTX 1060, RTX 3050
            return {
                'batch_size': 8,
                'gradient_accumulation_steps': 4,
                'num_epochs': 40,
                'name': 'GPU Budget (6GB)',
                'estimated_time': '2-3 giờ'
            }
    else:
        # CPU configs based on RAM
        ram_gb = system_info['ram_gb']
        
        if ram_gb >= 16:
            return {
                'batch_size': 8,
                'gradient_accumulation_steps': 4,
                'num_epochs': 30,  # Giảm epochs để nhanh hơn
                'name': 'CPU 16GB+ RAM',
                'estimated_time': '6-8 giờ'
            }
        elif ram_gb >= 8:
            return {
                'batch_size': 4,
                'gradient_accumulation_steps': 8,
                'num_epochs': 30,
                'name': 'CPU 8GB RAM',
                'estimated_time': '8-10 giờ'
            }
        else:
            return {
                'batch_size': 2,
                'gradient_accumulation_steps': 16,
                'num_epochs': 20,  # Giảm epochs
                'name': 'CPU Low RAM (<8GB)',
                'estimated_time': '10-12 giờ'
            }

def main():
    parser = argparse.ArgumentParser(description="Quick PhoBERT Training với auto config")
    parser.add_argument('--preset', choices=['fast', 'balanced', 'quality'], default='balanced',
                       help='fast: Nhanh (20 epochs), balanced: Cân bằng (30 epochs), quality: Chất lượng cao (40 epochs)')
    parser.add_argument('--batch-size', type=int, help='Override batch size')
    parser.add_argument('--epochs', type=int, help='Override số epochs')
    parser.add_argument('--data', default='./training_data/phobert_training_augmented.json',
                       help='Path to training data')
    parser.add_argument('--output', default='./models/phobert_finetuned',
                       help='Output directory')
    
    args = parser.parse_args()
    
    # Get system info
    print("🔍 Phát hiện cấu hình hệ thống...")
    print("=" * 70)
    
    system_info = get_system_info()
    
    print(f"💻 CPU Cores: {system_info['cpu_cores']}")
    print(f"💾 RAM: {system_info['ram_gb']:.1f} GB")
    
    if system_info['has_cuda']:
        print(f"🎮 GPU: {system_info['gpu_name']} ({system_info['gpu_memory_gb']:.1f} GB)")
        if system_info['gpu_count'] > 1:
            print(f"   📊 Total GPUs: {system_info['gpu_count']}")
    else:
        print("🎮 GPU: Không phát hiện")
    
    print("=" * 70)
    
    # Get recommended config
    config = recommend_config(system_info)
    
    # Apply preset adjustments
    if args.preset == 'fast':
        config['num_epochs'] = max(20, config['num_epochs'] // 2)
        print("\n⚡ Preset: FAST (Ưu tiên tốc độ)")
    elif args.preset == 'quality':
        config['num_epochs'] = 40
        print("\n🎯 Preset: QUALITY (Ưu tiên chất lượng)")
    else:
        print("\n⚖️  Preset: BALANCED (Cân bằng)")
    
    # Override with manual args
    if args.batch_size:
        config['batch_size'] = args.batch_size
    if args.epochs:
        config['num_epochs'] = args.epochs
    
    print(f"\n📋 Cấu hình khuyến nghị: {config['name']}")
    print(f"   Batch Size: {config['batch_size']}")
    print(f"   Gradient Accumulation: {config['gradient_accumulation_steps']}")
    print(f"   Effective Batch: {config['batch_size'] * config['gradient_accumulation_steps']}")
    print(f"   Epochs: {config['num_epochs']}")
    print(f"   ⏱️  Thời gian ước tính: {config['estimated_time']}")
    
    print("\n" + "=" * 70)
    
    # Confirm
    response = input("\n▶️  Bắt đầu training? (y/n): ")
    if response.lower() != 'y':
        print("❌ Đã hủy.")
        return
    
    print("\n🚀 Bắt đầu training...")
    print("=" * 70)
    
    # Import and train
    from core_nlp.phobert_trainer import PhoBERTTrainer
    
    trainer = PhoBERTTrainer(
        batch_size=config['batch_size'],
        num_epochs=config['num_epochs'],
        gradient_accumulation_steps=config['gradient_accumulation_steps'],
    )
    
    # Load data
    train_data, val_data = trainer.load_data_from_test_cases(args.data)
    
    # Train
    trainer.train(train_data, val_data, save_dir=args.output)
    
    print("\n" + "=" * 70)
    print("✅ HOÀN THÀNH!")
    print(f"📁 Model đã lưu tại: {args.output}")
    print("\n🎯 Test model:")
    print('   python -c "from core_nlp.hybrid_pipeline import HybridNLPPipeline; p = HybridNLPPipeline(); print(p.process(\'đặt lịch họp nhắc trước 2 tuần\'))"')
    print("\n🔨 Rebuild EXE:")
    print("   python scripts/build_exe.py --name TroLyLichTrinhHybrid --console")
    print("=" * 70)

if __name__ == "__main__":
    main()
