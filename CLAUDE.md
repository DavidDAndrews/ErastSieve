# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python desktop application that calculates prime numbers using the Sieve of Eratosthenes algorithm. Version 2.0 features a modern GUI with dark mode, export functionality, and improved performance.

## Development Commands

### Running the Application
```bash
# Original version
python ErastSieve.py

# Enhanced version 2.0
python ErastSieve_v2.py
```

### Virtual Environment
The project uses a Python virtual environment (venv). To activate:
```bash
source venv/bin/activate  # On macOS/Linux
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Running Tests
```bash
python -m pytest tests/
# or
python tests/test_calculator.py
```

## Project Structure

```
ErastSieve/
├── src/                    # New modular structure
│   ├── __init__.py
│   ├── config.py          # Configuration and constants
│   ├── prime_calculator.py # Core algorithm implementation
│   ├── gui.py             # GUI implementation
│   └── utils.py           # Utility functions
├── tests/
│   └── test_calculator.py # Unit tests
├── ErastSieve.py          # Original single-file version
├── ErastSieve_v2.py       # New entry point
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
   - Export functionality (CSV, TXT, JSON, clipboard)
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
- Automatic memory usage warnings for large calculations
- Progress updates during long-running calculations
- LRU cache for frequently requested prime lists