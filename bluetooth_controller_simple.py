#!/usr/bin/env python3
"""
Simple Bluetooth Controller Event Code Listener for Raspberry Pi
Listens for input events using evdev and prints event codes in readable form.
"""

import evdev
import threading
import time

class SimpleBluetoothController:
    """
    Simple controller that listens for input events using evdev and prints event codes.
    """
    
    def __init__(self, device_path=None):
        self.device_path = device_path
        self.running = False
        self.thread = None
        self.device = None
        
        # Comprehensive event code mapping for Bluetooth devices
        self.EVENT_CODES = {
            # Arrow keys
            103: 'UP_ARROW',
            108: 'DOWN_ARROW', 
            105: 'LEFT_ARROW',
            106: 'RIGHT_ARROW',
            
            # Media controls
            164: 'PLAY_PAUSE',
            165: 'NEXT_TRACK',
            166: 'PREVIOUS_TRACK',
            115: 'VOLUME_UP',
            114: 'VOLUME_DOWN',
            113: 'MUTE',
            
            # Navigation keys
            102: 'HOME',
            107: 'END',
            104: 'PAGE_UP',
            109: 'PAGE_DOWN',
            
            # Function keys
            59: 'F1', 60: 'F2', 61: 'F3', 62: 'F4',
            63: 'F5', 64: 'F6', 65: 'F7', 66: 'F8',
            67: 'F9', 68: 'F10', 87: 'F11', 88: 'F12',
            
            # Common buttons
            28: 'ENTER',
            57: 'SPACE',
            14: 'BACKSPACE',
            111: 'DELETE',
            1: 'ESCAPE',
            15: 'TAB',
            
            # Number keys
            2: 'ONE', 3: 'TWO', 4: 'THREE', 5: 'FOUR', 6: 'FIVE',
            7: 'SIX', 8: 'SEVEN', 9: 'EIGHT', 10: 'NINE', 11: 'ZERO',
            
            # Letter keys (common shortcuts)
            30: 'A', 48: 'B', 46: 'C', 32: 'D', 18: 'E',
            33: 'F', 34: 'G', 35: 'H', 23: 'I', 36: 'J',
            37: 'K', 38: 'L', 50: 'M', 49: 'N', 24: 'O',
            25: 'P', 16: 'Q', 19: 'R', 31: 'S', 20: 'T',
            22: 'U', 47: 'V', 17: 'W', 45: 'X', 21: 'Y', 44: 'Z',
            
            # Additional common keys
            12: 'MINUS',
            13: 'EQUAL',
            26: 'LEFT_BRACE',
            27: 'RIGHT_BRACE',
            39: 'SEMICOLON',
            40: 'APOSTROPHE',
            41: 'GRAVE',
            43: 'BACKSLASH',
            51: 'COMMA',
            52: 'DOT',
            53: 'SLASH',
            
            # Modifier keys
            29: 'LEFT_CTRL',
            56: 'LEFT_ALT',
            57: 'LEFT_SHIFT',
            100: 'LEFT_META',
            97: 'RIGHT_CTRL',
            100: 'RIGHT_ALT',
            54: 'RIGHT_SHIFT',
            126: 'RIGHT_META',
            
            # Mouse buttons (if device has them)
            272: 'LEFT_MOUSE',
            273: 'RIGHT_MOUSE',
            274: 'MIDDLE_MOUSE',
            
            # Special keys
            125: 'LEFT_GUI',
            126: 'RIGHT_GUI',
            127: 'COMPOSE',
            128: 'STOP',
            129: 'AGAIN',
            130: 'PROPS',
            131: 'UNDO',
            132: 'FRONT',
            133: 'COPY',
            134: 'OPEN',
            135: 'PASTE',
            136: 'FIND',
            137: 'CUT',
            138: 'HELP',
            139: 'MENU',
            140: 'CALC',
            141: 'SETUP',
            142: 'SLEEP',
            143: 'WAKEUP',
            144: 'FILE',
            145: 'SENDFILE',
            146: 'DELETEFILE',
            147: 'XFER',
            148: 'PROG1',
            149: 'PROG2',
            150: 'WWW',
            151: 'MSDOS',
            152: 'COFFEE',
            153: 'ROTATE_DISPLAY',
            154: 'CYCLEWINDOWS',
            155: 'MAIL',
            156: 'BOOKMARKS',
            157: 'COMPUTER',
            158: 'BACK',
            159: 'FORWARD',
            160: 'CLOSECD',
            161: 'EJECTCD',
            162: 'EJECTCLOSECD',
            163: 'NEXTSONG',
            164: 'PLAYPAUSE',
            165: 'PREVIOUSSONG',
            166: 'STOPCD',
            167: 'RECORD',
            168: 'REWIND',
            169: 'PHONE',
            170: 'ISO',
            171: 'CONFIG',
            172: 'HOMEPAGE',
            173: 'REFRESH',
            174: 'EXIT',
            175: 'MOVE',
            176: 'EDIT',
            177: 'SCROLLUP',
            178: 'SCROLLDOWN',
            179: 'KPLEFTPAREN',
            180: 'KPRIGHTPAREN',
            181: 'NEW',
            182: 'REDO',
            183: 'F13',
            184: 'F14',
            185: 'F15',
            186: 'F16',
            187: 'F17',
            188: 'F18',
            189: 'F19',
            190: 'F20',
            191: 'F21',
            192: 'F22',
            193: 'F23',
            194: 'F24',
        }
        
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
        bluetooth_keywords = ['bluetooth', 'bt', 'wireless', 'remote', 'controller', 'keyboard']
        
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
    
    def _get_event_name(self, event_code):
        """Get readable name for event code."""
        return self.EVENT_CODES.get(event_code, f"UNKNOWN_{event_code}")
    
    def _listen_loop(self):
        """Main listening loop for button events."""
        if not self.device:
            print("No device available for listening")
            return
        
        print(f"Listening for button presses on: {self.device.name}")
        print("Press buttons on your Bluetooth device to see event codes.")
        print("Press Ctrl+C to stop.")
        print()
        
        try:
            for event in self.device.read_loop():
                if event.type == evdev.ecodes.EV_KEY:
                    event_code = event.code
                    event_value = event.value
                    event_name = self._get_event_name(event_code)
                    
                    # Event values: 0=release, 1=press, 2=repeat
                    if event_value == 1:
                        print(f"PRESS: {event_name} (code: {event_code})")
                    elif event_value == 0:
                        print(f"RELEASE: {event_name} (code: {event_code})")
                    elif event_value == 2:
                        print(f"REPEAT: {event_name} (code: {event_code})")
                        
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
    print("Simple Bluetooth Controller Event Code Listener")
    print("=============================================")
    print()
    
    # List available devices
    controller = SimpleBluetoothController()
    controller.list_devices()
    print()
    
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
