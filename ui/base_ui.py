from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseUI(ABC):
    """Base interface for all UI implementations."""
    
    @abstractmethod
    def render_display(self, match_state: Dict[str, Any]) -> None:
        """Render the current match state."""
        pass
    
    @abstractmethod
    def show_message(self, message: str) -> None:
        """Show a message to the user."""
        pass
    
    @abstractmethod
    def show_startup_message(self) -> None:
        """Show the startup message."""
        pass
    
    @abstractmethod
    def show_quit_message(self) -> None:
        """Show the quit message."""
        pass
