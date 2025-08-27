"""
Persistence manager for tennis scoreboard system.
Handles saving and loading match state to/from JSON files.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List


class PersistenceManager:
    """
    Manages persistence of match state to JSON files.
    
    File structure:
    - ~/matches/YYYY-MM-DD-N.json (individual match files)
    - ~/matches/latest.json (symlink to most recent match)
    """
    
    def __init__(self, base_dir: str = "~/matches"):
        self.base_dir = Path(base_dir).expanduser()
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self.latest_file = self.base_dir / "latest.json"
    
    def save_match(self, match_data: Dict[str, Any], match_id: Optional[str] = None) -> str:
        """
        Save match state to a JSON file.
        
        Args:
            match_data: Match state dictionary
            match_id: Optional custom match ID, auto-generated if None
            
        Returns:
            The filename where the match was saved
        """
        if match_id is None:
            match_id = self._generate_match_id()
        
        # Add metadata
        match_data_with_meta = {
            'match_id': match_id,
            'timestamp': datetime.now().isoformat(),
            'data': match_data
        }
        
        # Save to numbered file
        filename = f"{match_id}.json"
        filepath = self.base_dir / filename
        
        try:
            with open(filepath, 'w') as f:
                json.dump(match_data_with_meta, f, indent=2)
            
            # Update latest.json symlink
            self._update_latest_symlink(filepath)
            
            return filename
        except Exception as e:
            raise RuntimeError(f"Failed to save match: {e}")
    
    def load_match(self, filename: str) -> Dict[str, Any]:
        """
        Load match state from a JSON file.
        
        Args:
            filename: Name of the file to load (with or without .json extension)
            
        Returns:
            Match state dictionary
        """
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = self.base_dir / filename
        
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            # Return the actual match data
            return data.get('data', data)
        except FileNotFoundError:
            raise FileNotFoundError(f"Match file not found: {filename}")
        except Exception as e:
            raise RuntimeError(f"Failed to load match: {e}")
    
    def load_latest(self) -> Optional[Dict[str, Any]]:
        """
        Load the most recent match from latest.json.
        
        Returns:
            Match state dictionary or None if no matches exist
        """
        try:
            if self.latest_file.exists():
                return self.load_match(str(self.latest_file))
            return None
        except Exception:
            return None
    
    def get_match_history(self) -> List[Dict[str, Any]]:
        """
        Get list of all saved matches with metadata.
        
        Returns:
            List of match metadata dictionaries
        """
        matches = []
        
        for filepath in self.base_dir.glob("*.json"):
            if filepath.name == "latest.json":
                continue
            
            try:
                with open(filepath, 'r') as f:
                    data = json.load(f)
                
                matches.append({
                    'filename': filepath.name,
                    'match_id': data.get('match_id', 'unknown'),
                    'timestamp': data.get('timestamp', 'unknown'),
                    'sets': data.get('data', {}).get('sets', [0, 0]),
                    'winner': data.get('data', {}).get('winner')
                })
            except Exception:
                # Skip corrupted files
                continue
        
        # Sort by timestamp (newest first)
        matches.sort(key=lambda x: x.get('timestamp', ''), reverse=True)
        return matches
    
    def delete_match(self, filename: str) -> bool:
        """
        Delete a match file.
        
        Args:
            filename: Name of the file to delete
            
        Returns:
            True if successful, False otherwise
        """
        if not filename.endswith('.json'):
            filename += '.json'
        
        filepath = self.base_dir / filename
        
        try:
            if filepath.exists():
                filepath.unlink()
                
                # If this was the latest match, update the symlink
                if self.latest_file.exists() and self.latest_file.resolve() == filepath.resolve():
                    self._update_latest_symlink()
                
                return True
            return False
        except Exception:
            return False
    
    def _generate_match_id(self) -> str:
        """Generate a unique match ID based on current date and time."""
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d")
        
        # Find the next available number for today
        counter = 1
        while True:
            match_id = f"{date_str}-{counter:02d}"
            filename = f"{match_id}.json"
            if not (self.base_dir / filename).exists():
                return match_id
            counter += 1
    
    def _update_latest_symlink(self, target_file: Optional[Path] = None) -> None:
        """
        Update the latest.json symlink to point to the most recent match.
        
        Args:
            target_file: Optional specific file to link to, otherwise finds most recent
        """
        try:
            # Remove existing symlink if it exists
            if self.latest_file.exists():
                self.latest_file.unlink()
            
            if target_file is None:
                # Find the most recent match file
                match_files = [f for f in self.base_dir.glob("*.json") 
                             if f.name != "latest.json"]
                
                if not match_files:
                    return
                
                # Sort by modification time (newest first)
                target_file = max(match_files, key=lambda f: f.stat().st_mtime)
            
            # Create symlink
            if target_file.exists():
                self.latest_file.symlink_to(target_file.name)
        except Exception:
            # If symlink creation fails, just continue
            # The system will still work, just without the latest.json convenience
            pass
    
    def get_storage_info(self) -> Dict[str, Any]:
        """
        Get information about storage usage and match count.
        
        Returns:
            Dictionary with storage statistics
        """
        match_files = [f for f in self.base_dir.glob("*.json") 
                      if f.name != "latest.json"]
        
        total_size = sum(f.stat().st_size for f in match_files)
        
        return {
            'total_matches': len(match_files),
            'total_size_bytes': total_size,
            'total_size_mb': round(total_size / (1024 * 1024), 2),
            'storage_directory': str(self.base_dir)
        }
