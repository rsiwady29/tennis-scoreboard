"""
UI package for tennis scoreboard.
Provides different UI implementations that can be easily swapped.
"""

from .base_ui import BaseUI
from .console_ui import ConsoleUI
from .led_ui import LEDMatrixUI

__all__ = ['BaseUI', 'ConsoleUI', 'LEDMatrixUI']
