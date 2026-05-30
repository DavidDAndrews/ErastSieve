#!/usr/bin/env python3
"""
Prime Number Calculator v2.0 - Enhanced Edition

A modern, feature-rich desktop application for calculating prime numbers
using the Sieve of Eratosthenes algorithm.

New features in v2.0:
- Dark mode support
- Export to CSV, TXT, JSON, and clipboard
- Segmented sieve for large numbers
- Progress bar for long calculations
- Input presets for quick access
- Enhanced statistics display
- Improved performance and memory management

Author: David Andrews
License: MIT
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.gui import main

if __name__ == "__main__":
    main()