# Prime Number Calculator - Sieve of Eratosthenes

A modern, user-friendly desktop application that efficiently finds all prime numbers up to a specified limit using the classical Sieve of Eratosthenes algorithm. Built with Python and tkinter, featuring a beautiful gradient interface and responsive design.

## 🌟 Features

- **Fast Prime Calculation**: Implements the efficient Sieve of Eratosthenes algorithm
- **Beautiful GUI**: Modern interface with gradient backgrounds and professional styling
- **Intelligent Formatting**: Automatic number formatting with thousands separators
- **Responsive Design**: Dynamically adjusts display based on window size
- **Performance Metrics**: Shows calculation time and prime count statistics
- **User-Friendly Input**: Press Enter to calculate, with comprehensive input validation
- **Scrollable Results**: Handles large result sets with auto-hiding scrollbars
- **Monospace Display**: Clean, aligned prime number presentation

## 📋 Requirements

- Python 3.6 or higher
- tkinter (usually included with Python)
- PIL (Pillow) for gradient backgrounds

## 🚀 Installation

1. **Clone or download the repository**
   ```bash
   git clone <repository-url>
   cd ErastSieve
   ```

2. **Install required dependencies**
   ```bash
   pip install Pillow
   ```

3. **Run the application**
   ```bash
   python ErastSieve.py
   ```

## 💡 Usage

1. **Launch the application** - The window will appear centered on your screen
2. **Enter a number** - Type any integer greater than 1 in the input field
3. **Calculate primes** - Press Enter or click the input field to start calculation
4. **View results** - All prime numbers up to your limit will be displayed in a formatted grid
5. **Performance info** - See how many primes were found and calculation time

### Example Usage
- Enter `100` to find all primes up to 100 (25 primes found)
- Enter `10,000` to find all primes up to 10,000 (1,229 primes found)
- Enter `1,000,000` to find all primes up to 1 million (78,498 primes found)

## 🔬 Algorithm: Sieve of Eratosthenes

The Sieve of Eratosthenes is an ancient algorithm for finding all prime numbers up to a given limit. It works by:

1. **Create a list** of consecutive integers from 2 through n
2. **Mark multiples** of each prime starting from 2
3. **Iterate** through unmarked numbers, marking their multiples
4. **Collect** all unmarked numbers as primes

### Time Complexity
- **Time**: O(n log log n)
- **Space**: O(n)

This makes it one of the most efficient algorithms for finding all primes up to a given limit.

## 🏗️ Technical Architecture

### Core Components

#### `PrimeCalculator` Class
- **Purpose**: Handles prime number calculation and result formatting
- **Key Methods**:
  - `calculate_primes(n)`: Implements the Sieve of Eratosthenes
  - `format_primes()`: Formats results for display with intelligent column sizing
  - `create_gradient()`: Generates the beautiful gradient background

#### `create_gui()` Function
- **Purpose**: Builds the entire user interface
- **Features**:
  - Responsive input field with live number formatting
  - Dynamic scrollbar visibility
  - Window resize handling with debouncing
  - Professional color scheme and typography

### Key Features Implementation

#### Smart Number Formatting
- Automatically adds thousands separators (1,000,000)
- Preserves cursor position during formatting
- Handles backspace and selection properly

#### Responsive Display
- Calculates optimal column count based on window width
- Adjusts font metrics for perfect alignment
- Handles window resizing with 250ms debouncing

#### Performance Optimization
- Only marks multiples starting from i²
- Uses boolean array for memory efficiency
- Stops iteration at √n for optimal performance

## 🎨 Design Philosophy

### Visual Design
- **Modern Interface**: Clean, professional appearance
- **Gradient Background**: Subtle blue-to-white gradient
- **Typography**: Segoe UI for text, Courier New for numbers
- **Color Scheme**: Blue accents (#007ACC) with green success indicators

### User Experience
- **Immediate Feedback**: Real-time input validation and formatting
- **Performance Transparency**: Shows calculation time and prime count
- **Keyboard Friendly**: Enter key triggers calculation
- **Error Handling**: Clear error messages for invalid inputs

## 📊 Performance Benchmarks

Typical performance on modern hardware:

| Limit | Primes Found | Time (approx.) |
|-------|-------------|----------------|
| 1,000 | 168 | < 0.01s |
| 10,000 | 1,229 | < 0.01s |
| 100,000 | 9,592 | < 0.05s |
| 1,000,000 | 78,498 | < 0.5s |
| 10,000,000 | 664,579 | < 5s |

## 🔧 Configuration

The application uses several configurable constants:

- **Window Size**: 800x800 pixels (centered on screen)
- **Font**: Segoe UI (11pt) for interface, Courier New (11pt) for numbers
- **Colors**: Defined in the GUI creation function
- **Resize Debounce**: 250ms delay for window resize operations

## 🐛 Error Handling

The application includes comprehensive error handling:

- **Input Validation**: Ensures numbers are integers greater than 1
- **Memory Management**: Handles large calculations gracefully
- **GUI Stability**: Prevents crashes during window operations
- **User Feedback**: Clear error messages for all failure cases

## 🚀 Future Enhancements

Potential improvements for future versions:

- **Export Options**: Save results to CSV or text files
- **Visualization**: Graph prime distribution and gaps
- **Advanced Algorithms**: Implement segmented sieve for larger ranges
- **Multi-threading**: Background calculation for very large numbers
- **Statistics**: Show prime gaps, density, and distribution analysis

## 📝 License

This project is open source and available under the MIT License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## 📞 Support

For questions or issues, please open an issue in the project repository.

---

**Built with ❤️ using Python and the timeless Sieve of Eratosthenes algorithm**
