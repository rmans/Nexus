"""
Discovery Cache - Caching system for discovery results.
"""

import hashlib
import json
import pickle
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, Any


class DiscoveryCache:
    """Caches discovery results for improved performance."""
    
    def __init__(self, cache_dir: Path):
        """Initialize the cache system.
        
        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.default_ttl = timedelta(hours=24)  # 24 hour default TTL
    
    def get(self, target_path: Path, options: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Get cached discovery results.
        
        Args:
            target_path: Target path that was analyzed
            options: Discovery options used
            
        Returns:
            Cached results if valid, None otherwise
        """
        cache_key = self._generate_cache_key(target_path, options)
        cache_file = self.cache_dir / f"{cache_key}.cache"
        
        if not cache_file.exists():
            return None
        
        try:
            with open(cache_file, 'rb') as f:
                cache_data = pickle.load(f)
            
            # Check if cache is still valid
            if self._is_cache_valid(cache_data, target_path):
                return cache_data['results']
            else:
                # Remove expired cache
                cache_file.unlink()
                return None
                
        except Exception:
            # If cache is corrupted, remove it
            try:
                cache_file.unlink()
            except Exception:
                pass
            return None
    
    def set(self, target_path: Path, options: Dict[str, Any], results: Dict[str, Any]) -> None:
        """Cache discovery results.
        
        Args:
            target_path: Target path that was analyzed
            options: Discovery options used
            results: Discovery results to cache
        """
        cache_key = self._generate_cache_key(target_path, options)
        cache_file = self.cache_dir / f"{cache_key}.cache"
        
        cache_data = {
            'timestamp': datetime.now().isoformat(),
            'target_path': str(target_path),
            'options': options,
            'file_hash': self._calculate_file_hash(target_path),
            'results': results
        }
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(cache_data, f)
        except Exception:
            # Silently fail cache writes
            pass
    
    def clear(self, target_path: Optional[Path] = None) -> None:
        """Clear cache entries.
        
        Args:
            target_path: If provided, clear only cache for this path. Otherwise clear all.
        """
        if target_path:
            # Clear cache for specific path
            for cache_file in self.cache_dir.glob("*.cache"):
                try:
                    with open(cache_file, 'rb') as f:
                        cache_data = pickle.load(f)
                    if cache_data['target_path'] == str(target_path):
                        cache_file.unlink()
                except Exception:
                    pass
        else:
            # Clear all cache
            for cache_file in self.cache_dir.glob("*.cache"):
                try:
                    cache_file.unlink()
                except Exception:
                    pass
    
    def _generate_cache_key(self, target_path: Path, options: Dict[str, Any]) -> str:
        """Generate a cache key based on path and options."""
        # Include path and relevant options in cache key
        key_data = {
            'path': str(target_path.resolve()),
            'options': {k: v for k, v in options.items() if k in ['deep', 'languages']}
        }
        
        key_string = json.dumps(key_data, sort_keys=True)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def _calculate_file_hash(self, target_path: Path) -> str:
        """Calculate hash of important files for cache validation."""
        important_files = [
            'requirements.txt', 'pyproject.toml', 'package.json', 
            'setup.py', 'Pipfile', 'yarn.lock', 'package-lock.json'
        ]
        
        hash_content = str(target_path)
        
        try:
            for file_name in important_files:
                file_path = target_path / file_name
                if file_path.exists():
                    stat = file_path.stat()
                    hash_content += f"{file_name}:{stat.st_mtime}:{stat.st_size}"
        except Exception:
            pass
        
        return hashlib.md5(hash_content.encode()).hexdigest()
    
    def _is_cache_valid(self, cache_data: Dict[str, Any], target_path: Path) -> bool:
        """Check if cached data is still valid."""
        try:
            # Check timestamp
            cache_time = datetime.fromisoformat(cache_data['timestamp'])
            if datetime.now() - cache_time > self.default_ttl:
                return False
            
            # Check file hash
            current_hash = self._calculate_file_hash(target_path)
            if current_hash != cache_data['file_hash']:
                return False
            
            return True
            
        except Exception:
            return False
