#!/usr/bin/env python3
"""
Bluetooth Controller for Tennis Scoreboard
Uses evdev to listen for button presses from a Bluetooth device.
"""

import evdev
import threading
import time
from typing import Callable, Optional

class BluetoothController:
    """
    Bluetooth controller that listens for button presses using evdev.
    
    Expected button mapping:
    - UP arrow: Home scores point
    - DOWN arrow: Away scores point  
    - RIGHT arrow: Reset match
    - LEFT arrow: (reserved for future use)
    - CENTER button: Pause/Play (reserved for future use)
    """
    
    def __init__(self, device_path: Optional[str] = None):
        self.device_path = device_path
        self.running = False
        self.thread = None
        self.device = None
        
        # Button event codes (these may need adjustment based on your device)
        self.BUTTON_UP = 103      # KEY_UP
        self.BUTTON_DOWN = 108    # KEY_DOWN
        self.BUTTON_LEFT = 105    # KEY_LEFT
        self.BUTTON_RIGHT = 106   # KEY_RIGHT
        self.BUTTON_CENTER = 28   # KEY_ENTER
        
        # Callback functions for button actions
        self.on_up_press: Optional[Callable] = None
        self.on_down_press: Optional[Callable] = None
        self.on_right_press: Optional[Callable] = None
        self.on_left_press: Optional[Callable] = None
        self.on_center_press: Optional[Callable] = None
        
        # Find and initialize the Bluetooth device
        self._find_device()
    
    def _find_device(self):
        """Find the Bluetooth input device."""
        if self.device_path:
            # Use specific device path if provided
            try:
                self.device = evdev.InputDevice(self.device_path)
                print(f"Using specified device: {self.device.name}")
                return
            except Exception as e:
                print(f"Failed to open specified device {self.device_path}: {e}")
        
        # Auto-detect Bluetooth devices
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        
        # Look for Bluetooth devices (common names/patterns)
        bluetooth_keywords = ['bluetooth', 'bt', 'wireless', 'remote', 'controller']
        
        for device in devices:
            device_name = device.name.lower()
            if any(keyword in device_name for keyword in bluetooth_keywords):
                try:
                    # Test if we can read from this device
                    self.device = device
                    print(f"Found Bluetooth device: {device.name} at {device.path}")
                    print(f"Device info: {device.info}")
                    print(f"Capabilities: {device.capabilities()}")
                    return
                except Exception as e:
                    print(f"Failed to initialize device {device.name}: {e}")
                    continue
        
        # If no Bluetooth device found, try any input device
        if devices:
            try:
                self.device = devices[0]
                print(f"Using fallback device: {self.device.name}")
                print("Note: This may not be a Bluetooth device")
            except Exception as e:
                print(f"Failed to initialize fallback device: {e}")
        
        if not self.device:
            print("No input devices found!")
    
    def set_callbacks(self, 
                     on_up: Optional[Callable] = None,
                     on_down: Optional[Callable] = None,
                     on_right: Optional[Callable] = None,
                     on_left: Optional[Callable] = None,
                     on_center: Optional[Callable] = None):
        """Set callback functions for button presses."""
        self.on_up_press = on_up
        self.on_down_press = on_down
        self.on_right_press = on_right
        self.on_left_press = on_left
        self.on_center_press = on_center
    
    def _handle_button_press(self, event_code: int):
        """Handle button press events."""
        if event_code == self.BUTTON_UP and self.on_up_press:
            print("↑ UP button pressed")
            self.on_up_press()
        elif event_code == self.BUTTON_DOWN and self.on_down_press:
            print("↓ DOWN button pressed")
            self.on_down_press()
        elif event_code == self.BUTTON_RIGHT and self.on_right_press:
            print("→ RIGHT button pressed")
            self.on_right_press()
        elif event_code == self.BUTTON_LEFT and self.on_left_press:
            print("← LEFT button pressed")
            self.on_left_press()
        elif event_code == self.BUTTON_CENTER and self.on_center_press:
            print("● CENTER button pressed")
            self.on_center_press()
    
    def _listen_loop(self):
        """Main listening loop for button events."""
        if not self.device:
            print("No device available for listening")
            return
        
        print(f"Listening for button presses on: {self.device.name}")
        print("Press Ctrl+C to stop")
        
        try:
            for event in self.device.read_loop():
                if event.type == evdev.ecodes.EV_KEY and event.value == 1:  # Key press
                    self._handle_button_press(event.code)
        except KeyboardInterrupt:
            print("\nStopping Bluetooth controller...")
        except Exception as e:
            print(f"Error reading from device: {e}")
        finally:
            self.running = False
    
    def start(self):
        """Start listening for button presses in a background thread."""
        if not self.device:
            print("Cannot start: No device available")
            return False
        
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.thread.start()
            print("Bluetooth controller started in background thread")
            return True
        return False
    
    def stop(self):
        """Stop listening for button presses."""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
            print("Bluetooth controller stopped")
    
    def is_listening(self):
        """Check if the controller is currently listening."""
        return self.running and self.thread and self.thread.is_alive()
    
    def list_devices(self):
        """List all available input devices for debugging."""
        print("Available input devices:")
        for path in evdev.list_devices():
            try:
                device = evdev.InputDevice(path)
                print(f"  {path}: {device.name}")
            except Exception as e:
                print(f"  {path}: Error reading device info: {e}")


def main():
    """Test the Bluetooth controller."""
    print("Bluetooth Controller Test")
    print("========================")
    
    # List available devices
    controller = BluetoothController()
    controller.list_devices()
    print()
    
    # Test callbacks
    def on_up():
        print("  → Home scores point!")
    
    def on_down():
        print("  → Away scores point!")
    
    def on_right():
        print("  → Match reset!")
    
    def on_left():
        print("  → Left button (reserved)")
    
    def on_center():
        print("  → Center button (reserved)")
    
    # Set callbacks
    controller.set_callbacks(
        on_up=on_up,
        on_down=on_down,
        on_right=on_right,
        on_left=on_left,
        on_center=on_center
    )
    
    # Start listening
    if controller.start():
        print("Controller started. Press buttons on your Bluetooth device.")
        print("Press Ctrl+C to stop.")
        
        try:
            while controller.is_listening():
                time.sleep(0.1)
        except KeyboardInterrupt:
            pass
        finally:
            controller.stop()
    else:
        print("Failed to start controller")


if __name__ == "__main__":
    main()
