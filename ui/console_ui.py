"""
Console UI for tennis scoreboard system.
Ultra-simple, bulletproof ASCII rendering.
"""

import os
import time
from .base_ui import BaseUI


class ConsoleUI(BaseUI):
    """Console-based UI implementation for the tennis scoreboard."""
    
    def __init__(self):
        pass
    
    def clear_screen(self):
        """Clear the console screen."""
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def render_display(self, match_state):
        """Render the current match state to console."""
        self.clear_screen()
        
        # Header
        print("=" * 10)
        print("TENNIS SCOREBOARD")
        print("=" * 10)
        print()
        
        # Score section
        sets, games, points = match_state['sets'], match_state['games'], match_state['points']
        
        print("SCORE:")
        print("------")
        print(f"Sets:   Home {sets[0]} - Away {sets[1]}")
        print(f"Games:  Home {games[0]} - Away {games[1]}")
        
        # Points display
        if match_state['in_tiebreak']:
            tp = match_state['tiebreak_points']
            points_display = f"Tiebreak: {tp[0]} - {tp[1]}"
        else:
            if points[0] >= 3 and points[1] >= 3:
                if points[0] == points[1]:
                    points_display = "40 - 40 (Deuce)"
                elif points[0] > points[1]:
                    points_display = "Advantage - 40"
                else:
                    points_display = "40 - Advantage"
            else:
                point_names = ['0', '15', '30', '40']
                points_display = f"{point_names[min(points[0], 3)]} - {point_names[min(points[1], 3)]}"
        
        print(f"Points: {points_display}")
        print()
        
        # Server and Status
        server = "Home" if match_state['server'] == 0 else "Away"
        print(f"SERVER: {server}")
        
        if match_state['match_complete']:
            winner = "Home" if match_state['winner'] == 0 else "Away"
            print(f"STATUS: COMPLETE - {winner} WINS!")
        else:
            status = "TIEBREAK IN PROGRESS" if match_state['in_tiebreak'] else "IN PROGRESS"
            print(f"STATUS: {status}")
        
        print()
        
        # Keyboard Controls
        print("KEYBOARD CONTROLS:")
        print("------------------")
        print("↑ (Up Arrow)    - Home scores point")
        print("↓ (Down Arrow)  - Away scores point")
        print("→ (Right Arrow) - Reset match")
        print("q                - Quit")
        print()
        
        # Footer
        print("-" * 10)
        print(f"Last updated: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 10)
    
    def show_message(self, message):
        """Show a message to the user."""
        print(message)
    
    def show_startup_message(self):
        """Show the startup message."""
        print("Starting Simplified Tennis Scoreboard with Keyboard Controls...")
        print("Press any key to continue...")
    
    def show_quit_message(self):
        """Show the quit message."""
        print("Tennis Scoreboard stopped.")
