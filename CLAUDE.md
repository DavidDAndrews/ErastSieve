# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python desktop application that calculates prime numbers using the Sieve of Eratosthenes algorithm. Version 2.0 features a modern GUI with dark mode, export functionality, and improved performance.

## Development Commands

### Running the Application
```bash
python ErastSieve_v2.py
```

The original single-file `ErastSieve.py` was removed in the move to `src/` (still in git history).

### Virtual Environment
No virtual environment is committed (`.venv/` is git-ignored). To create and activate one:
```bash
python3 -m venv .venv
source .venv/bin/activate  # On macOS/Linux
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Running Tests
Install `requirements.txt` first: `src/__init__.py` imports `utils`, which imports `pyperclip`.
```bash
python tests/test_calculator.py
# or
python -m unittest discover tests
# or, if pytest is installed (it is not in requirements.txt)
python -m pytest tests/
```

## Project Structure

```
ErastSieve/
├── src/                    # New modular structure
│   ├── __init__.py
│   ├── config.py          # Configuration and constants
│   ├── prime_calculator.py # Core algorithm implementation
│   ├── gui.py             # GUI implementation
│   ├── gui_fix.py         # Stand-alone Tk button-visibility test (macOS)
│   └── utils.py           # Utility functions
├── tests/
│   └── test_calculator.py # Unit tests
├── ErastSieve_v2.py       # Entry point
├── README.md              # User-facing documentation
└── requirements.txt       # Python dependencies
```

## Architecture

### Version 2.0 Components

1. **PrimeCalculator Class** (`src/prime_calculator.py`)
   - Standard Sieve of Eratosthenes for numbers up to 10M
   - Segmented Sieve for larger numbers (reduced memory usage)
   - Caching system for repeated calculations
   - Progress callback support for GUI updates
   - Additional features: nth prime, prime factors, statistics

2. **PrimeCalculatorGUI Class** (`src/gui.py`)
   - Modern GUI with light/dark theme toggle
   - Export functionality (CSV, TXT, JSON, HTML to ~/Downloads; clipboard)
   - Progress bar for long calculations
   - Input presets for quick access
   - Enhanced statistics display

3. **Configuration** (`src/config.py`)
   - Centralized configuration for colors, fonts, limits
   - Theme definitions (light and dark)
   - Performance settings

4. **Utilities** (`src/utils.py`)
   - Number formatting and parsing (supports scientific notation)
   - Export functions for various formats
   - Memory usage estimation
   - Time and byte formatting

### Key Improvements in v2.0

- **Performance**: Segmented sieve for large numbers, result caching
- **UI/UX**: Dark mode, progress bar, export options, input presets
- **Code Quality**: Type hints, modular structure, unit tests
- **Features**: Statistics display, clipboard support, memory warnings

## Important Implementation Details

- Uses threading for non-blocking calculations
- Supports scientific notation input (e.g., 1e6)
- Memory warning dialog when estimated memory use exceeds 2 GB
- Progress updates during long-running calculations
- LRU cache of the last `CACHE_SIZE` (10) prime lists