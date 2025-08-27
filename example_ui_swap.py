#!/usr/bin/env python3
"""
Example script showing how easy it is to swap UI implementations.
"""

from tennis_scoreboard_simple import SimpleTennisScoreboard
from ui.console_ui import ConsoleUI
from ui.led_ui import LEDMatrixUI

def main():
    """Demonstrate UI swapping."""
    print("Tennis Scoreboard UI Swapping Example")
    print("=====================================")
    print()
    
    # Option 1: Console UI (default)
    print("1. Starting with Console UI...")
    console_ui = ConsoleUI()
    console_scoreboard = SimpleTennisScoreboard(console_ui)
    print("Console UI initialized!")
    print()
    
    # Option 2: LED Matrix UI
    print("2. Starting with LED Matrix UI...")
    led_ui = LEDMatrixUI()
    led_scoreboard = SimpleTennisScoreboard(led_ui)
    print("LED Matrix UI initialized!")
    print()
    
    # Option 3: You could easily add more UI types:
    # web_ui = WebUI()
    # gui_ui = GUIUI()
    # sound_ui = SoundUI()
    
    print("3. UI implementations can be easily swapped!")
    print("   - Console UI: Text-based display")
    print("   - LED Matrix UI: Hardware LED display")
    print("   - Web UI: Browser-based interface")
    print("   - GUI UI: Desktop application")
    print("   - Sound UI: Audio feedback")
    print()
    
    print("To use a different UI, just change one line:")
    print("   scoreboard = SimpleTennisScoreboard(desired_ui)")
    print()
    
    print("All UIs implement the same BaseUI interface,")
    print("so the core tennis logic never changes!")

if __name__ == "__main__":
    main()
