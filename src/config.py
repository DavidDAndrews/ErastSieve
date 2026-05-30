"""
Configuration settings for the Prime Number Calculator application.

This module contains all configurable parameters including colors, fonts,
window settings, and algorithm limits.
"""

from typing import Dict, Tuple

# Window Configuration
WINDOW_WIDTH = 900
WINDOW_HEIGHT = 800
MIN_WINDOW_WIDTH = 600
MIN_WINDOW_HEIGHT = 500

# Algorithm Limits
MAX_SIEVE_MEMORY = 10_000_000  # Maximum number for standard sieve
SEGMENT_SIZE = 65536  # Size for segmented sieve chunks
PROGRESS_UPDATE_INTERVAL = 0.1  # Seconds between progress updates

# Colors - Light Theme
LIGHT_THEME = {
    "bg": "#F0F2F5",
    "fg": "#202124",
    "input_bg": "#FFFFFF",
    "input_fg": "#202124",
    "button_bg": "#007ACC",
    "button_fg": "#FFFFFF",
    "button_hover": "#005A9E",
    "success": "#28A745",
    "warning": "#FFA500",
    "error": "#DC3545",
    "gradient_top": (30, 144, 255),
    "gradient_bottom": (255, 255, 255),
}

# Colors - Dark Theme
DARK_THEME = {
    "bg": "#1E1E1E",
    "fg": "#E0E0E0",
    "input_bg": "#2D2D2D",
    "input_fg": "#E0E0E0",
    "button_bg": "#0E639C",
    "button_fg": "#FFFFFF",
    "button_hover": "#1177BB",
    "success": "#4EC866",
    "warning": "#FFA500",
    "error": "#F14C4C",
    "gradient_top": (15, 25, 35),
    "gradient_bottom": (30, 40, 50),
}

# Font Configuration
FONTS = {
    "title": ("Segoe UI", 16, "bold"),
    "normal": ("Segoe UI", 11),
    "small": ("Segoe UI", 10),
    "monospace": ("Courier New", 11),
    "button": ("Segoe UI", 10, "bold"),
}

# Input Presets
PRESETS = [
    ("1K", 1_000),
    ("10K", 10_000),
    ("100K", 100_000),
    ("1M", 1_000_000),
    ("10M", 10_000_000),
    ("100M", 100_000_000),
    ("500M", 500_000_000),
]

# Export Formats
EXPORT_FORMATS = {
    "csv": {
        "extension": ".csv",
        "description": "CSV files",
        "delimiter": ",",
    },
    "txt": {
        "extension": ".txt",
        "description": "Text files",
        "delimiter": " ",
    },
    "json": {
        "extension": ".json",
        "description": "JSON files",
    },
}

# Performance Settings
DEBOUNCE_DELAY = 250  # Milliseconds for resize debouncing
CACHE_SIZE = 10  # Number of results to cache
THREAD_POOL_SIZE = 4  # Maximum worker threads

# UI Settings
SCROLLBAR_WIDTH = 12
PADDING = 20
BUTTON_PADDING = 10
CORNER_RADIUS = 8

# Validation Limits
MIN_INPUT = 2
MAX_INPUT = 1_000_000_000  # 1 billion
INPUT_WARNING_THRESHOLD = 100_000_000  # Show warning for large inputs

def get_theme(dark_mode: bool = False) -> Dict[str, str]:
    """
    Get the color theme based on the dark mode setting.
    
    Args:
        dark_mode: Whether to use dark theme
        
    Returns:
        Dictionary of color settings
    """
    return DARK_THEME if dark_mode else LIGHT_THEME

def get_gradient_colors(dark_mode: bool = False) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
    """
    Get gradient colors for the background.
    
    Args:
        dark_mode: Whether to use dark theme
        
    Returns:
        Tuple of (top_color, bottom_color) as RGB tuples
    """
    theme = get_theme(dark_mode)
    return theme["gradient_top"], theme["gradient_bottom"]