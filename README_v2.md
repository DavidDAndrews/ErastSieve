# Prime Number Calculator v2.0 - Enhanced Edition

An upgraded version of the Prime Number Calculator with significant improvements in performance, features, and user experience.

## 🚀 What's New in Version 2.0

### Features
- **🌓 Dark Mode**: Toggle between light and dark themes
- **📊 Export Options**: Save results as CSV, TXT, JSON, or copy to clipboard
- **📈 Progress Bar**: Visual feedback for long calculations
- **🎯 Input Presets**: Quick buttons for common values (1K, 10K, 100K, 1M, 10M)
- **📐 Scientific Notation**: Support for inputs like "1e6" (1 million)
- **📊 Enhanced Statistics**: Shows calculation time, largest gap, twin primes count
- **💾 Result Caching**: Instant results for repeated calculations
- **⚡ Segmented Sieve**: Handles numbers up to 1 billion with reduced memory usage

### Technical Improvements
- **Modular Architecture**: Separated into logical modules (calculator, GUI, config, utils)
- **Type Hints**: Better code documentation and IDE support
- **Threading**: Non-blocking UI during calculations
- **Memory Warnings**: Alerts for calculations requiring >2GB RAM
- **Unit Tests**: Comprehensive test coverage

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
- **Dark Mode**: Click the moon/sun icon in the top-right
- **Export**: Use the export buttons to save in your preferred format
- **Large Numbers**: Try scientific notation like "1e8" for 100 million
- **Stop Calculation**: Click "Stop" during long calculations

## 🏗️ Architecture

```
src/
├── prime_calculator.py  # Core algorithm with caching and segmented sieve
├── gui.py              # Modern GUI with themes and export features
├── config.py           # Centralized configuration
└── utils.py            # Export and formatting utilities
```

## ⚡ Performance

| Input Size | Memory Usage | Time (approx) |
|------------|--------------|---------------|
| 1 Million  | ~10 MB       | <0.5s         |
| 10 Million | ~100 MB      | <5s           |
| 100 Million| ~1 GB        | <60s          |
| 1 Billion  | ~256 MB*     | <10min        |

*Uses segmented sieve for reduced memory

## 🔧 Configuration

Edit `src/config.py` to customize:
- Window size and limits
- Color themes
- Font settings
- Performance parameters
- Export formats

## 🧪 Testing

Run the test suite:
```bash
python tests/test_calculator.py
```

## 📝 Notes

- The original single-file version (`ErastSieve.py`) is still available
- Both versions can run independently
- Settings are not shared between versions

Enjoy the enhanced prime calculation experience! 🎉