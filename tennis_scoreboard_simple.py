#!/usr/bin/env python3
"""
Simplified Tennis Scoreboard - Clean, working version with keyboard controls
"""

import os
import time
import sys
import tty
import termios
import threading
from pathlib import Path

# Add current directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from core.match import Match
from core.persistence import PersistenceManager
from ui.console_ui import ConsoleUI


class SimpleTennisScoreboard:
    """
    Simplified tennis scoreboard with clean console output and keyboard controls.
    """
    
    def __init__(self, ui=None):
        self.match = Match()
        self.persistence = PersistenceManager()
        self.running = False
        
        # Use provided UI or default to console
        self.ui = ui if ui else ConsoleUI()
        
        # Load latest match if available
        self._load_latest_match()
    
    def _load_latest_match(self):
        """Load the latest saved match."""
        try:
            latest_data = self.persistence.load_latest()
            if latest_data:
                self.match.from_dict(latest_data)
                print("Latest match loaded")
            else:
                print("No saved matches found")
        except Exception as e:
            print(f"Error loading match: {e}")
    
    def _save_match(self):
        """Save the current match state."""
        try:
            match_data = self.match.to_dict()
            filename = self.persistence.save_match(match_data)
            print(f"Match saved: {filename}")
        except Exception as e:
            print(f"Warning: Failed to save match: {e}")
    
    def _get_key(self):
        """Get a single keypress from the terminal."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
            # Handle arrow keys (they send escape sequences)
            if ch == '\x1b':
                next1 = sys.stdin.read(1)
                if next1 == '[':
                    next2 = sys.stdin.read(1)
                    if next2 == 'A':
                        return 'UP'
                    elif next2 == 'B':
                        return 'DOWN'
                    elif next2 == 'C':
                        return 'RIGHT'
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def _handle_keyboard_input(self, key):
        """Handle keyboard input."""
        if key == 'UP':
            self.match.home_scores_point()
            self._save_match()
            self.ui.show_message("Home scores point!")
        elif key == 'DOWN':
            self.match.away_scores_point()
            self._save_match()
            self.ui.show_message("Away scores point!")
        elif key == 'RIGHT':
            self.match.reset()
            self._save_match()
            self.ui.show_message("Match reset!")
        elif key == 'q':
            self.running = False
            self.ui.show_message("Quitting...")
    
    def _render_display(self):
        """Render the current match state using the UI."""
        match_state = self.match.get_state()
        self.ui.render_display(match_state)
    
    def start(self):
        """Start the simplified scoreboard with keyboard controls."""
        self.ui.show_startup_message()
        input()
        
        self.running = True
        
        # Main loop with keyboard listening
        while self.running:
            self._render_display()
            
            try:
                key = self._get_key()
                self._handle_keyboard_input(key)
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error reading key: {e}")
                break
        
        # Save final state
        self._save_match()
        self.ui.show_quit_message()


def main():
    """Main entry point."""
    print("Simplified Tennis Scoreboard v1.5 - UI Abstraction")
    print("==================================================")
    print()
    
    # Create UI and scoreboard
    ui = ConsoleUI()
    scoreboard = SimpleTennisScoreboard(ui)
    
    try:
        scoreboard.start()
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
