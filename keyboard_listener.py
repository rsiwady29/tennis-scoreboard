import sys
import tty
import termios
import threading
import time

class KeyboardListener:
    """
    A simple class that listens for keyboard events and prints text based on input.
    Handles up/down arrow keys and ignores other inputs.
    """
    
    def __init__(self):
        self.running = False
        self.thread = None
        
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
                    elif next2 == 'D':
                        return 'LEFT'
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    def _listen_loop(self):
        """Main listening loop that runs in a separate thread."""
        print("Keyboard listener started. Press up/down/left/right arrows or any other key.")
        print("Press 'q' to quit.")
        
        while self.running:
            try:
                key = self._get_key()
                
                if key == 'q':
                    print("\nQuitting...")
                    self.running = False
                    break
                elif key == 'UP':
                    print("↑ Up arrow pressed!")
                elif key == 'DOWN':
                    print("↓ Down arrow pressed!")
                elif key == 'LEFT':
                    print("← Left arrow pressed!")
                elif key == 'RIGHT':
                    print("→ Right arrow pressed!")
                else:
                    print(f"Ignoring key: '{key}' (not an arrow key)")
                    
            except KeyboardInterrupt:
                print("\nInterrupted by user")
                self.running = False
                break
            except Exception as e:
                print(f"Error reading key: {e}")
                break
    
    def start(self):
        """Start listening for keyboard events in a background thread."""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._listen_loop, daemon=True)
            self.thread.start()
            print("Keyboard listener started in background thread.")
    
    def stop(self):
        """Stop listening for keyboard events."""
        self.running = False
        if self.thread and self.thread.is_alive():
            self.thread.join(timeout=1.0)
            print("Keyboard listener stopped.")
    
    def is_listening(self):
        """Check if the listener is currently running."""
        return self.running and self.thread and self.thread.is_alive()


def main():
    """Example usage of the KeyboardListener class."""
    listener = KeyboardListener()
    
    try:
        listener.start()
        
        # Keep the main thread alive while listening
        while listener.is_listening():
            time.sleep(0.1)
            
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        listener.stop()


if __name__ == "__main__":
    main()
