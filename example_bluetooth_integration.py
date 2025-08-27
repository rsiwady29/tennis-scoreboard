#!/usr/bin/env python3
"""
Example: Integrating Bluetooth Controller with Tennis Scoreboard
Shows how to use the Bluetooth controller instead of keyboard input.
"""

from tennis_scoreboard_simple import SimpleTennisScoreboard
from ui.console_ui import ConsoleUI
from bluetooth_controller import BluetoothController
import time

def main():
    """Demonstrate Bluetooth controller integration."""
    print("Bluetooth Controller + Tennis Scoreboard Integration")
    print("==================================================")
    print()
    
    # Create UI and scoreboard
    ui = ConsoleUI()
    scoreboard = SimpleTennisScoreboard(ui)
    
    # Create Bluetooth controller
    controller = BluetoothController()
    
    # Set up button callbacks that integrate with the scoreboard
    def on_up_press():
        """Home scores point."""
        scoreboard.match.home_scores_point()
        scoreboard._save_match()
        ui.show_message("Home scores point!")
        scoreboard._render_display()
    
    def on_down_press():
        """Away scores point."""
        scoreboard.match.away_scores_point()
        scoreboard._save_match()
        ui.show_message("Away scores point!")
        scoreboard._render_display()
    
    def on_right_press():
        """Reset match."""
        scoreboard.match.reset()
        scoreboard._save_match()
        ui.show_message("Match reset!")
        scoreboard._render_display()
    
    def on_left_press():
        """Left button - reserved for future use."""
        ui.show_message("Left button pressed (reserved)")
    
    def on_center_press():
        """Center button - reserved for future use."""
        ui.show_message("Center button pressed (reserved)")
    
    # Connect the Bluetooth controller to the scoreboard
    controller.set_callbacks(
        on_up=on_up_press,
        on_down=on_down_press,
        on_right=on_right_press,
        on_left=on_left_press,
        on_center=on_center_press
    )
    
    print("Bluetooth controller callbacks set up!")
    print("Button mapping:")
    print("  ↑ UP: Home scores point")
    print("  ↓ DOWN: Away scores point")
    print("  → RIGHT: Reset match")
    print("  ← LEFT: Reserved")
    print("  ● CENTER: Reserved")
    print()
    
    # Start the Bluetooth controller
    if not controller.start():
        print("Failed to start Bluetooth controller!")
        return
    
    print("Bluetooth controller started successfully!")
    print("Press buttons on your Bluetooth device to control the scoreboard.")
    print("Press Ctrl+C to stop.")
    print()
    
    # Show initial display
    scoreboard._render_display()
    
    # Main loop - keep the scoreboard running
    try:
        while controller.is_listening():
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        controller.stop()
        scoreboard._save_match()
        ui.show_quit_message()

if __name__ == "__main__":
    main()
