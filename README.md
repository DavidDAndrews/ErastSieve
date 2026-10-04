# Prime Number Calculator v2.0 - Enhanced Edition

An upgraded version of the Prime Number Calculator with significant improvements in performance, features, and user experience.

## 🚀 What's New in Version 2.0

### Features
- **🌓 Dark Mode**: Toggle between light and dark themes
- **📊 Export Options**: Save results as CSV, TXT, JSON or HTML (to your Downloads folder), or copy to clipboard
- **📈 Progress Bar**: Visual feedback for long calculations
- **🎯 Input Presets**: Quick buttons for common values (1K, 10K, 100K, 1M, 10M, 100M, 500M)
- **📐 Scientific Notation**: Support for inputs like "1e6" (1 million)
- **📊 Enhanced Statistics**: Shows calculation time, largest gap, twin primes count
- **💾 Result Caching**: Instant results for repeated calculations
- **⚡ Segmented Sieve**: Used above 10 million (inputs up to 1 billion) to keep the sieve itself small

### Technical Improvements
- **Modular Architecture**: Separated into logical modules (calculator, GUI, config, utils)
- **Type Hints**: Better code documentation and IDE support
- **Threading**: Non-blocking UI during calculations
- **Memory Warnings**: Asks before calculations whose estimated memory use exceeds 2 GB
- **Unit Tests**: `unittest` tests for the calculator (`tests/test_calculator.py`)

## 📋 Installation

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   python ErastSieve_v2.py
   ```

## 🎮 Usage

### Basic Usage
1. Enter a number in the input field or click a preset button
2. Press Enter or click "Calculate"
3. View results and statistics
4. Export or copy results as needed

### Advanced Features
- **Dark Mode**: Click the "Dark Mode" / "Light Mode" button in the top-right
- **Export**: Use the export buttons; files are saved to `~/Downloads` as `PrimeNumbers in <first>-<last>.<ext>` (HTML also opens in your browser)
- **Large Numbers**: Try scientific notation like "1e8" for 100 million
- **Stop Calculation**: Click "Stop" during long calculations

## 🏗️ Architecture

```
ErastSieve_v2.py        # Entry point
src/
├── prime_calculator.py  # Core algorithm with caching and segmented sieve
├── gui.py              # Modern GUI with themes and export features
├── config.py           # Centralized configuration
├── utils.py            # Export and formatting utilities
└── gui_fix.py          # Stand-alone Tk button-visibility test (macOS)
tests/
└── test_calculator.py  # Unit tests
```

## ⚡ Performance

Calculation only (no GUI), peak process memory, measured on an Apple M2 Ultra with Python 3.14:

| Input Size | Memory Usage | Time (approx) |
|------------|--------------|---------------|
| 1 Million  | ~30 MB       | <0.1s         |
| 10 Million | ~130 MB      | <1s           |
| 100 Million| ~300 MB*     | ~6s           |
| 1 Billion  | ~2.4 GB*     | ~66s          |

*Uses the segmented sieve (inputs above 10 million). Memory is then dominated by the returned list of primes (about 50.8 million of them below 1 billion).

## 🔧 Configuration

Edit `src/config.py` to customize:
- Window size and limits
- Color themes
- Font settings
- Performance parameters

## 🧪 Testing

Run the test suite (install `requirements.txt` first; the package imports `pyperclip`):
```bash
python tests/test_calculator.py
# or
python -m unittest discover tests
```

## 📝 Notes

- The original single-file version (`ErastSieve.py`) was removed when the project moved to the `src/` package; it remains in the git history
- Settings (such as the theme) are not saved between runs

Enjoy the enhanced prime calculation experience! 🎉