"""
Sound Manager - Handle notification sounds
Supports preset sounds and custom user sounds
"""
import os
import platform
from pathlib import Path
from typing import Optional
import threading
import time

# Try import sound libraries
try:
    import winsound  # Windows only
except ImportError:
    winsound = None

try:
    from playsound import playsound
    PLAYSOUND_AVAILABLE = True
except ImportError:
    PLAYSOUND_AVAILABLE = False


class SoundManager:
    """Manage notification sounds with presets and custom sounds"""
    
    # Preset sound names - Windows System Sounds
    PRESETS = {
        'system_default': 'System Default Sound',
        'system_hand': 'Critical Stop',
        
    }
    
    def __init__(self, base_dir: str = '.', db_manager=None):
        """Initialize sound manager with optional database for persistence
        
        Args:
            base_dir: Base directory for sound files
            db_manager: DatabaseManager instance for saving settings (optional)
        """
        self.base_dir = Path(base_dir)
        self.preset_dir = self.base_dir / 'sounds' / 'presets'
        self.custom_dir = self.base_dir / 'sounds' / 'custom'
        
        # Database for persistence
        self.db_manager = db_manager
        
        # Ensure directories exist
        self.preset_dir.mkdir(parents=True, exist_ok=True)
        self.custom_dir.mkdir(parents=True, exist_ok=True)
        
        # Default sound setting
        self.current_sound = 'system_default'
        self.custom_sound_path: Optional[str] = None
        
        # Load saved settings from database
        self._load_settings_from_db()
        
        # Thread management for non-blocking playback
        self._playback_lock = threading.Lock()
        self._last_play_time = 0
        self._min_play_interval = 0.3  # Debounce: 300ms between plays
        
        # Async DB save management (prevent UI blocking)
        self._save_lock = threading.Lock()
        self._pending_save = None  # Store pending save data
        self._save_timer = None  # Debounce timer for batch saves
    
    def _load_settings_from_db(self):
        """Load sound settings from database (if available)"""
        if not self.db_manager:
            return
        
        try:
            # Load sound type (preset or custom)
            sound_type = self.db_manager.get_setting('sound_type', 'preset')
            
            if sound_type == 'custom':
                # Load custom sound path
                custom_path = self.db_manager.get_setting('sound_custom_path')
                if custom_path and Path(custom_path).exists():
                    self.custom_sound_path = custom_path
                    self.current_sound = 'custom'
                    print(f"✅ Loaded custom sound from DB: {custom_path}")
                else:
                    # File not found, fallback to default
                    print(f"⚠️ Custom sound file not found: {custom_path}, using default")
                    self.current_sound = 'system_default'
                    self.custom_sound_path = None
            else:
                # Load preset sound
                preset_name = self.db_manager.get_setting('sound_preset_name', 'system_default')
                if preset_name in self.PRESETS:
                    self.current_sound = preset_name
                    self.custom_sound_path = None
                    print(f"✅ Loaded preset sound from DB: {preset_name}")
                else:
                    print(f"⚠️ Unknown preset: {preset_name}, using default")
                    self.current_sound = 'system_default'
        except Exception as e:
            print(f"⚠️ Error loading sound settings from DB: {e}")
            # Fallback to default
            self.current_sound = 'system_default'
            self.custom_sound_path = None
    
    def _save_settings_to_db(self):
        """Save current sound settings to database (ASYNC + DEBOUNCED)
        
        Uses background thread + debouncing to prevent UI blocking.
        Multiple rapid changes are batched into single DB write.
        """
        if not self.db_manager:
            return
        
        # Prepare data to save (in memory - instant)
        if self.current_sound == 'custom' and self.custom_sound_path:
            save_data = {
                'sound_type': 'custom',
                'sound_custom_path': self.custom_sound_path
            }
        else:
            save_data = {
                'sound_type': 'preset',
                'sound_preset_name': self.current_sound
            }
        
        with self._save_lock:
            # Store pending data (will overwrite if called multiple times)
            self._pending_save = save_data
            
            # Cancel previous timer if exists (debounce)
            if self._save_timer is not None:
                self._save_timer.cancel()
            
            # Schedule save after 200ms delay (batch rapid changes)
            def _async_save():
                """Background thread to save to DB"""
                with self._save_lock:
                    data = self._pending_save
                    self._pending_save = None
                    self._save_timer = None
                
                if data is None:
                    return
                
                try:
                    # BATCH WRITE - 1 DB call instead of 2
                    self.db_manager.set_settings_batch(data)
                    
                    if data.get('sound_type') == 'custom':
                        print(f"💾 [Async] Saved custom sound: {data['sound_custom_path']}")
                    else:
                        print(f"💾 [Async] Saved preset: {data['sound_preset_name']}")
                except Exception as e:
                    print(f"❌ [Async] DB save error: {e}")
            
            # Start debounced save timer (non-blocking)
            self._save_timer = threading.Timer(0.2, _async_save)
            self._save_timer.daemon = True
            self._save_timer.start()
    
    def get_preset_sounds(self) -> dict:
        """Get list of preset sounds"""
        return self.PRESETS.copy()
    
    def get_custom_sounds(self) -> list:
        """Get list of user's custom sound files"""
        if not self.custom_dir.exists():
            return []
        
        # Supported formats
        extensions = ['.wav', '.mp3', '.ogg', '.m4a']
        custom_sounds = []
        
        for file in self.custom_dir.iterdir():
            if file.is_file() and file.suffix.lower() in extensions:
                custom_sounds.append(file.name)
        
        return sorted(custom_sounds)
    
    def set_preset_sound(self, preset_name: str) -> bool:
        """
        Set current sound to a preset (INSTANT - non-blocking)
        
        Args:
            preset_name: Name from PRESETS dict
            
        Returns:
            True if valid preset
        """
        if preset_name in self.PRESETS:
            # Update state immediately (in-memory)
            self.current_sound = preset_name
            self.custom_sound_path = None
            
            # Async save to DB (non-blocking, debounced)
            self._save_settings_to_db()
            
            return True
        return False
    
    def set_custom_sound(self, filepath: str) -> bool:
        """
        Set current sound to a custom file (INSTANT - non-blocking)
        
        Args:
            filepath: Full path to sound file
            
        Returns:
            True if file exists and valid
        """
        path = Path(filepath)
        
        # Convert to absolute path
        if not path.is_absolute():
            path = (self.base_dir / path).resolve()
        
        if path.exists() and path.is_file():
            # Update state immediately (in-memory)
            self.custom_sound_path = str(path.resolve())
            self.current_sound = 'custom'
            
            # Async save to DB (non-blocking, debounced)
            self._save_settings_to_db()
            
            print(f"✅ Set custom sound: {self.custom_sound_path}")
            return True
        else:
            print(f"❌ File not found: {path}")
            return False
    
    def add_custom_sound(self, source_path: str) -> Optional[str]:
        """
        Copy a custom sound file to custom sounds directory
        
        Args:
            source_path: Path to source sound file
            
        Returns:
            Filename if successful, None otherwise
        """
        import shutil
        
        source = Path(source_path)
        if not source.exists():
            return None
        
        # Copy to custom directory
        dest = self.custom_dir / source.name
        
        # Avoid overwrite - add number if exists
        counter = 1
        while dest.exists():
            stem = source.stem
            suffix = source.suffix
            dest = self.custom_dir / f"{stem}_{counter}{suffix}"
            counter += 1
        
        try:
            shutil.copy2(source, dest)
            return dest.name
        except Exception as e:
            print(f"Error copying sound file: {e}")
            return None
    
    def remove_custom_sound(self, filename: str) -> bool:
        """
        Remove a custom sound file
        
        Args:
            filename: Name of the custom sound file
            
        Returns:
            True if removed successfully
        """
        try:
            file_path = self.custom_dir / filename
            if file_path.exists() and file_path.is_file():
                file_path.unlink()
                
                # If this was the current sound, switch to default
                if self.current_sound == 'custom' and self.custom_sound_path:
                    if Path(self.custom_sound_path).name == filename:
                        self.set_preset_sound('system_default')
                
                print(f"✅ Removed custom sound: {filename}")
                return True
            return False
        except Exception as e:
            print(f"❌ Error removing sound: {e}")
            return False
    
    def get_all_sounds(self) -> dict:
        """
        Get all sounds (presets + custom) organized for UI
        
        Returns:
            Dict with 'presets' and 'custom' lists
        """
        return {
            'presets': [
                {'id': key, 'name': name, 'type': 'preset'}
                for key, name in self.PRESETS.items()
            ],
            'custom': [
                {'id': f'custom:{name}', 'name': name, 'type': 'custom'}
                for name in self.get_custom_sounds()
            ]
        }
    
    def play_notification_sound(self) -> bool:
        """
        Play the current notification sound (non-blocking with debounce)
        
        Returns:
            True if sound played successfully
        """
        # Debounce: Prevent rapid-fire clicks
        current_time = time.time()
        with self._playback_lock:
            if current_time - self._last_play_time < self._min_play_interval:
                print(f"⏭️ Skipping sound (debounce: {self._min_play_interval}s)")
                return False
            self._last_play_time = current_time
        
        try:
            print(f"🔊 Playing sound - Type: {self.current_sound}")
            
            # Custom sound file
            if self.current_sound == 'custom' and self.custom_sound_path:
                print(f"   → Custom file: {self.custom_sound_path}")
                return self._play_file(self.custom_sound_path)
            
            # Preset system sounds (Windows)
            if platform.system() == 'Windows' and winsound:
                print(f"   → Windows preset: {self.current_sound}")
                return self._play_windows_preset(self.current_sound)
            
            # Fallback: Tk bell
            print(f"   → Fallback: Tk bell")
            return self._play_tk_bell()
            
        except Exception as e:
            print(f"❌ Error playing sound: {e}")
            return False
    
    def _play_file(self, filepath: str) -> bool:
        """Play a sound file using playsound or winsound"""
        try:
            # Ensure absolute path
            file_path = Path(filepath)
            if not file_path.is_absolute():
                file_path = self.base_dir / filepath
            
            abs_path = str(file_path.resolve())
            
            if not file_path.exists():
                print(f"❌ Sound file not found: {abs_path}")
                return False
            
            print(f"   → Playing file: {abs_path}")
            
            # Windows: Use winsound for .wav files (fast, async)
            if platform.system() == 'Windows' and winsound and abs_path.lower().endswith('.wav'):
                winsound.PlaySound(abs_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
                return True
            
            # For MP3/OGG/M4A: Use playsound in thread (to avoid blocking)
            if PLAYSOUND_AVAILABLE:
                def play_async():
                    try:
                        playsound(abs_path)
                        print(f"✅ Finished playing: {file_path.name}")
                    except Exception as e:
                        print(f"❌ Playsound error: {e}")
                
                thread = threading.Thread(target=play_async, daemon=True)
                thread.start()
                return True
            
            print(f"⚠️ No audio library available for: {abs_path}")
            return False
            
        except Exception as e:
            print(f"❌ Error playing file {filepath}: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _play_windows_preset(self, preset_name: str) -> bool:
        """Play Windows system sound (fast, direct call)"""
        if not winsound or platform.system() != 'Windows':
            return False
        
        sound_map = {
            'system_default': winsound.MB_OK,
            'system_asterisk': winsound.MB_ICONASTERISK,
            'system_exclamation': winsound.MB_ICONEXCLAMATION,
            'system_hand': winsound.MB_ICONHAND,
            'system_question': winsound.MB_ICONQUESTION,
            'system_ok': winsound.MB_OK  # Same as default but explicit
        }
        
        sound_type = sound_map.get(preset_name, winsound.MB_OK)
        
        try:
            # Direct call - MessageBeep is very fast (<10ms)
            winsound.MessageBeep(sound_type)
            return True
        except Exception as e:
            print(f"Windows preset error: {e}")
            return False
    
    def _play_tk_bell(self) -> bool:
        """Fallback: Play simple Tk bell sound"""
        try:
            import tkinter as tk
            root = tk._get_default_root()
            if root:
                root.bell()
                return True
        except Exception:
            pass
        return False
    
    def preview_sound(self, skip_debounce: bool = False) -> bool:
        """
        Preview current sound (for UI testing)
        
        Args:
            skip_debounce: If True, bypass debounce check (for manual testing)
        """
        # For preview, use shorter debounce (0.1s instead of 0.3s)
        if not skip_debounce:
            current_time = time.time()
            with self._playback_lock:
                if current_time - self._last_play_time < 0.1:  # Shorter for preview
                    print(f"⏭️ Preview skipped (too soon)")
                    return False
                self._last_play_time = current_time
        
        # Play without additional debounce check
        try:
            print(f"🔊 PREVIEW - Playing sound...")
            
            # Custom sound file
            if self.current_sound == 'custom' and self.custom_sound_path:
                print(f"   → Custom file: {self.custom_sound_path}")
                return self._play_file(self.custom_sound_path)
            
            # Preset system sounds (Windows)
            if platform.system() == 'Windows' and winsound:
                print(f"   → Windows preset: {self.current_sound}")
                return self._play_windows_preset(self.current_sound)
            
            # Fallback: Tk bell
            print(f"   → Fallback: Tk bell")
            return self._play_tk_bell()
            
        except Exception as e:
            print(f"❌ Preview error: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def get_current_sound_info(self) -> dict:
        """Get info about current sound setting"""
        if self.current_sound == 'custom' and self.custom_sound_path:
            filename = Path(self.custom_sound_path).name
            return {
                'type': 'custom',
                'name': filename,
                'path': self.custom_sound_path,
                'id': f'custom:{filename}'
            }
        elif self.current_sound in self.PRESETS:
            return {
                'type': 'preset',
                'name': self.PRESETS[self.current_sound],
                'preset_key': self.current_sound,
                'id': self.current_sound
            }
        else:
            return {
                'type': 'preset',
                'name': 'System Default',
                'preset_key': 'system_default',
                'id': 'system_default'
            }
    
    def flush_pending_saves(self, timeout: float = 1.0):
        """Force flush any pending DB saves (call before app exit)
        
        Args:
            timeout: Max seconds to wait for save completion
        """
        with self._save_lock:
            if self._save_timer is not None:
                # Cancel timer and execute save immediately
                self._save_timer.cancel()
                self._save_timer = None
                
                data = self._pending_save
                self._pending_save = None
                
                if data and self.db_manager:
                    try:
                        print(f"💾 [Flush] Saving pending data...")
                        self.db_manager.set_settings_batch(data)
                        print(f"✅ [Flush] Save completed")
                    except Exception as e:
                        print(f"❌ [Flush] Save error: {e}")
