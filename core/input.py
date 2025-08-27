"""
Input handler for tennis scoreboard system.
Manages input devices and translates key presses to match actions.
"""

import sys
import select
import threading
import time
from typing import Dict, Any, Callable, Optional, List
from pathlib import Path

try:
    import evdev
    EVDEV_AVAILABLE = True
except ImportError:
    EVDEV_AVAILABLE = False


class InputHandler:
    """
    Handles input from various devices and translates to match actions.
    
    Phase 1: Hardcoded key bindings
    Phase 2: Configurable input mapping via JSON
    """
    
    def __init__(self):
        self.running = False
        self.input_thread = None
        self.action_handlers: Dict[str, Callable] = {}
        self.input_devices: List[Any] = []
        self.fallback_to_stdin = True
        self.raw_terminal_mode = False
        
        # Phase 1: Hardcoded key bindings
        self.key_bindings = {
            'KEY_UP': 'home_point',
            'KEY_DOWN': 'away_point',
            'KEY_S': 'swap_server',
            'KEY_R': 'reset_match',
            'KEY_N': 'new_match',
            'KEY_L': 'load_latest'
        }
        
        # Arrow key alternatives for common remotes
        self.arrow_key_bindings = {
            'KEY_UP': 'home_point',
            'KEY_DOWN': 'away_point',
            'KEY_LEFT': 'swap_server',
            'KEY_RIGHT': 'reset_match'
        }
    
    def set_action_handlers(self, handlers: Dict[str, Callable]) -> None:
        """
        Set the action handler functions.
        
        Args:
            handlers: Dictionary mapping action names to handler functions
        """
        self.action_handlers = handlers
    
    def start(self) -> None:
        """Start the input handling thread."""
        if self.running:
            return
        
        self.running = True
        
        # Try to discover input devices
        self._discover_input_devices()
        
        # Start input thread
        self.input_thread = threading.Thread(target=self._input_loop, daemon=True)
        self.input_thread.start()
    
    def stop(self) -> None:
        """Stop the input handling thread."""
        self.running = False
        if self.input_thread:
            self.input_thread.join(timeout=1.0)
    
    def _discover_input_devices(self) -> None:
        """Discover available input devices."""
        if not EVDEV_AVAILABLE:
            print("Warning: evdev not available, falling back to stdin")
            return
        
        try:
            # Look for input devices in /dev/input/
            input_dir = Path("/dev/input")
            if not input_dir.exists():
                return
            
            for event_file in input_dir.glob("event*"):
                try:
                    device = evdev.InputDevice(str(event_file))
                    
                    # Check if it's a keyboard-like device
                    if self._is_keyboard_device(device):
                        self.input_devices.append(device)
                        print(f"Found input device: {device.name} ({event_file})")
                except Exception as e:
                    # Skip devices we can't access
                    continue
            
            if not self.input_devices:
                print("No input devices found, falling back to stdin")
        except Exception as e:
            print(f"Error discovering input devices: {e}")
    
    def _is_keyboard_device(self, device) -> bool:
        """Check if a device is keyboard-like."""
        try:
            # Check if device has key events
            capabilities = device.capabilities()
            if evdev.ecodes.EV_KEY in capabilities:
                key_codes = capabilities[evdev.ecodes.EV_KEY]
                # Look for common key codes
                common_keys = [evdev.ecodes.KEY_UP, evdev.ecodes.KEY_DOWN, 
                             evdev.ecodes.KEY_S, evdev.ecodes.KEY_R]
                if any(key in key_codes for key in common_keys):
                    return True
        except Exception:
            pass
        return False
    
    def _input_loop(self) -> None:
        """Main input processing loop."""
        while self.running:
            try:
                # Process evdev devices
                if self.input_devices:
                    self._process_evdev_input()
                elif self.fallback_to_stdin:
                    # Fallback to stdin if no devices found
                    self._process_stdin_input()
                
                time.sleep(0.01)  # Small delay to prevent busy waiting
            except Exception as e:
                print(f"Error in input loop: {e}")
                time.sleep(0.1)
    
    def _process_evdev_input(self) -> None:
        """Process input from evdev devices."""
        for device in self.input_devices:
            try:
                # Non-blocking read
                events = device.read()
                for event in events:
                    if event.type == evdev.ecodes.EV_KEY and event.value == 1:  # Key press
                        key_name = evdev.ecodes.KEY[event.code]
                        self._handle_key_press(key_name)
            except BlockingIOError:
                # No events available
                pass
            except Exception as e:
                print(f"Error reading from device {device.name}: {e}")
    
    def _process_stdin_input(self) -> None:
        """Process input from stdin (fallback)."""
        if select.select([sys.stdin], [], [], 0.01)[0]:
            try:
                # Read one character at a time to detect special keys
                char = sys.stdin.read(1)
                if char:
                    # Check for special key sequences
                    if char == '\x1b':  # ESC sequence
                        # Read next character
                        next_char = sys.stdin.read(1)
                        if next_char == '[':
                            # Arrow key sequence
                            arrow_char = sys.stdin.read(1)
                            if arrow_char == 'A':  # UP arrow
                                self._execute_action('home_point')
                            elif arrow_char == 'B':  # DOWN arrow
                                self._execute_action('away_point')
                            elif arrow_char == 'C':  # RIGHT arrow
                                self._execute_action('reset_match')
                            elif arrow_char == 'D':  # LEFT arrow
                                self._execute_action('swap_server')
                    else:
                        # Handle single character input
                        self._handle_stdin_input(char)
            except Exception as e:
                print(f"Error reading stdin: {e}")
    
    def _handle_stdin_input(self, input_str: str) -> None:
        """Handle input from stdin."""
        input_str = input_str.upper()
        
        # Map common input strings to actions
        stdin_mapping = {
            'UP': 'home_point',
            'DOWN': 'away_point',
            'S': 'swap_server',
            'R': 'reset_match',
            'N': 'new_match',
            'L': 'load_latest',
            'H': 'home_point',  # Alternative
            'A': 'away_point',  # Alternative
            'SWAP': 'swap_server',
            'RESET': 'reset_match',
            'NEW': 'new_match',
            'LOAD': 'load_latest',
            # Single character mappings
            'U': 'home_point',  # U for Up
            'D': 'away_point',  # D for Down
            'W': 'home_point',  # W for Win (home)
            'L': 'away_point',  # L for Lose (away)
            'X': 'swap_server', # X for swap
            'Z': 'reset_match', # Z for reset
            'M': 'new_match',   # M for new Match
            'O': 'load_latest'  # O for lOad
        }
        
        action = stdin_mapping.get(input_str)
        if action:
            self._execute_action(action)
        else:
            print(f"Unknown input: {input_str}")
    
    def _handle_key_press(self, key_name: str) -> None:
        """Handle a key press from an evdev device."""
        # Check standard bindings first
        action = self.key_bindings.get(key_name)
        
        # Check arrow key bindings
        if not action:
            action = self.arrow_key_bindings.get(key_name)
        
        if action:
            self._execute_action(action)
        else:
            print(f"Unbound key: {key_name}")
    
    def _execute_action(self, action: str) -> None:
        """Execute an action by calling the appropriate handler."""
        handler = self.action_handlers.get(action)
        if handler:
            try:
                handler()
            except Exception as e:
                print(f"Error executing action {action}: {e}")
        else:
            print(f"No handler for action: {action}")
    
    def get_input_status(self) -> Dict[str, Any]:
        """Get status information about input handling."""
        return {
            'running': self.running,
            'evdev_available': EVDEV_AVAILABLE,
            'input_devices_count': len(self.input_devices),
            'input_devices': [str(d.name) for d in self.input_devices],
            'fallback_to_stdin': self.fallback_to_stdin,
            'action_handlers_count': len(self.action_handlers)
        }
    
    def simulate_key_press(self, key_name: str) -> None:
        """Simulate a key press (useful for testing)."""
        self._handle_key_press(key_name)
    
    def simulate_stdin_input(self, input_str: str) -> None:
        """Simulate stdin input (useful for testing)."""
        self._handle_stdin_input(input_str)
    
    def enable_raw_terminal_mode(self) -> None:
        """Enable raw terminal mode for better key detection."""
        try:
            import termios
            import tty
            
            # Save current terminal settings
            self.old_terminal_settings = termios.tcgetattr(sys.stdin)
            
            # Set raw mode
            tty.setraw(sys.stdin.fileno())
            self.raw_terminal_mode = True
            print("Raw terminal mode enabled - arrow keys should work now!")
            
        except ImportError:
            print("Raw terminal mode not available on this system")
        except Exception as e:
            print(f"Could not enable raw terminal mode: {e}")
    
    def disable_raw_terminal_mode(self) -> None:
        """Disable raw terminal mode and restore settings."""
        if hasattr(self, 'old_terminal_settings') and self.raw_terminal_mode:
            try:
                import termios
                termios.tcsetattr(sys.stdin, termios.TCSADRAIN, self.old_terminal_settings)
                self.raw_terminal_mode = False
            except Exception as e:
                print(f"Could not disable raw terminal mode: {e}")


class InputConfig:
    """Configuration class for input mapping (Phase 2)."""
    
    def __init__(self, config_file: str = "input_config.json"):
        self.config_file = Path(config_file)
        self.key_mappings: Dict[str, str] = {}
        self.device_mappings: Dict[str, Dict[str, str]] = {}
        self.load_config()
    
    def load_config(self) -> None:
        """Load input configuration from JSON file."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                
                self.key_mappings = config.get('key_mappings', {})
                self.device_mappings = config.get('device_mappings', {})
        except Exception as e:
            print(f"Warning: Could not load input config: {e}")
    
    def save_config(self) -> None:
        """Save input configuration to JSON file."""
        try:
            config = {
                'key_mappings': self.key_mappings,
                'device_mappings': self.device_mappings
            }
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
        except Exception as e:
            print(f"Warning: Could not save input config: {e}")
    
    def get_key_mapping(self, key_name: str) -> Optional[str]:
        """Get the action mapped to a key."""
        return self.key_mappings.get(key_name)
    
    def set_key_mapping(self, key_name: str, action: str) -> None:
        """Set a key mapping."""
        self.key_mappings[key_name] = action
        self.save_config()
