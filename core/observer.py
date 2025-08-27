"""
Observer interface for tennis scoreboard UI components.
Allows UIs to subscribe to match state changes and update accordingly.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class UIObserver(ABC):
    """Abstract base class for UI components that observe match state."""
    
    @abstractmethod
    def update(self, match_state: Dict[str, Any]) -> None:
        """
        Called when match state changes.
        
        Args:
            match_state: Dictionary containing current match state
        """
        pass


class Subject:
    """Subject class that notifies observers of state changes."""
    
    def __init__(self):
        self._observers: List[UIObserver] = []
    
    def attach(self, observer: UIObserver) -> None:
        """Attach an observer to this subject."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer: UIObserver) -> None:
        """Detach an observer from this subject."""
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
    
    def notify(self, match_state: Dict[str, Any]) -> None:
        """Notify all observers of a state change."""
        for observer in self._observers:
            observer.update(match_state)
