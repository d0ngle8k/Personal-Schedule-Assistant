"""
Lazy Loading NLP Pipeline Wrapper
Defers model initialization until first use to speed up startup time
"""

from __future__ import annotations
from typing import Optional, Any, Dict
from datetime import datetime
import threading


class LazyLoadPipeline:
    """
    Wrapper that delays NLP pipeline initialization until first use
    
    This allows the UI to appear immediately while models load in background
    """
    
    def __init__(self, model_path: Optional[str] = None, *, relative_base: Optional[datetime] = None):
        """
        Initialize lazy pipeline wrapper
        
        Args:
            model_path: Path to fine-tuned PhoBERT model
            relative_base: Base datetime for relative time parsing
        """
        self.model_path = model_path
        self.relative_base = relative_base
        self._pipeline = None
        self._lock = threading.Lock()
        self._loading = False
        print("⚡ NLP Pipeline: Lazy loading enabled (will load on first use)")
    
    def _ensure_loaded(self):
        """Ensure pipeline is loaded, load if needed"""
        if self._pipeline is not None:
            return  # Already loaded
        
        with self._lock:
            if self._pipeline is not None:
                return  # Another thread just loaded it
            
            if self._loading:
                return  # Another thread is loading, wait for it to finish
            
            self._loading = True
        
        try:
            print("🔄 Loading NLP Pipeline in background...")
            from .hybrid_pipeline import HybridNLPPipeline
            self._pipeline = HybridNLPPipeline(
                model_path=self.model_path,
                relative_base=self.relative_base
            )
            print("✅ NLP Pipeline loaded successfully")
        except Exception as e:
            print(f"❌ Failed to load pipeline: {e}")
            # Fallback to rule-based
            from .pipeline import NLPPipeline
            self._pipeline = NLPPipeline(relative_base=self.relative_base)
            print("⚠️ Using rule-based pipeline as fallback")
    
    def process(self, text: str):
        """Process text (triggers load if needed)"""
        self._ensure_loaded()
        return self._pipeline.process(text)
    
    def extract(self, text: str):
        """Alias for process() for compatibility"""
        return self.process(text)
    
    def extract_event_with_time(self, text: str):
        """Extract event with time information"""
        self._ensure_loaded()
        if hasattr(self._pipeline, 'extract_event_with_time'):
            return self._pipeline.extract_event_with_time(text)
        return self.process(text)
    
    def extract_location(self, text: str):
        """Extract location information"""
        self._ensure_loaded()
        if hasattr(self._pipeline, 'extract_location'):
            return self._pipeline.extract_location(text)
        return self.process(text).get('location')
    
    def extract_reminder(self, text: str):
        """Extract reminder information"""
        self._ensure_loaded()
        if hasattr(self._pipeline, 'extract_reminder'):
            return self._pipeline.extract_reminder(text)
        return self.process(text).get('reminder_minutes')
    
    def get_model_info(self) -> Dict[str, Any]:
        """Get model information (triggers load if needed)"""
        self._ensure_loaded()
        if hasattr(self._pipeline, 'get_model_info'):
            return self._pipeline.get_model_info()
        return {'mode': 'Rule-based (lazy loaded)'}
    
    def __getattr__(self, name):
        """Forward any other attribute access to the underlying pipeline"""
        self._ensure_loaded()
        return getattr(self._pipeline, name)
