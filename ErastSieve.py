"""
Prime Number Calculator - Sieve of Eratosthenes Implementation

A modern desktop application that efficiently finds all prime numbers up to a specified
limit using the classical Sieve of Eratosthenes algorithm. This implementation features
a beautiful GUI with gradient backgrounds, intelligent number formatting, and responsive
design that adapts to different window sizes.

Key Features:
- Fast prime calculation using the Sieve of Eratosthenes algorithm
- Beautiful gradient GUI with professional styling
- Intelligent number formatting with thousands separators
- Responsive design that adjusts to window size
- Performance metrics showing calculation time and prime count
- Auto-hiding scrollbars for large result sets
- Comprehensive input validation and error handling

Algorithm Complexity:
- Time: O(n log log n) where n is the input limit
- Space: O(n) for the boolean sieve array

Author: David Andrews
Version: 1.0.0
Python Version: 3.6+

Dependencies:
- tkinter (usually included with Python)
- PIL (Pillow) for gradient backgrounds
- time (built-in) for performance timing

Usage:
    python ErastSieve.py

The application will launch a GUI window where users can enter a number and
find all prime numbers up to that limit using the efficient Sieve of Eratosthenes.
"""

import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont
import time
from tkinter import ttk
from PIL import Image, ImageTk, ImageDraw


def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
    """
    Create a rounded rectangle on a tkinter Canvas.
    
    This is a helper function that extends the Canvas class to support
    rounded rectangles by creating a polygon with smooth curves.
    
    Args:
        self: The Canvas instance
        x1, y1 (int): Top-left corner coordinates
        x2, y2 (int): Bottom-right corner coordinates
        radius (int, optional): Corner radius in pixels. Defaults to 25.
        **kwargs: Additional keyword arguments passed to create_polygon
        
    Returns:
        int: The canvas item ID of the created rounded rectangle
        
    Note:
        This function is dynamically added to the Canvas class below.
    """
    # Calculate points for rounded rectangle using polygon approximation
    points = [
        x1 + radius, y1,        # Top edge start
        x2 - radius, y1,        # Top edge end
        x2, y1,                 # Top-right corner start
        x2, y1 + radius,        # Top-right corner end
        x2, y2 - radius,        # Right edge end
        x2, y2,                 # Bottom-right corner start
        x2 - radius, y2,        # Bottom-right corner end
        x1 + radius, y2,        # Bottom edge end
        x1, y2,                 # Bottom-left corner start
        x1, y2 - radius,        # Bottom-left corner end
        x1, y1 + radius,        # Left edge start
        x1, y1                  # Left edge end
    ]
    return self.create_polygon(points, **kwargs, smooth=True)


# Extend the Canvas class with rounded rectangle functionality
tk.Canvas.create_rounded_rect = create_rounded_rect


class PrimeCalculator:
    """
    Core class for prime number calculation and result formatting.
    
    This class implements the Sieve of Eratosthenes algorithm and handles
    all aspects of prime number calculation, result formatting, and display
    optimization. It also manages the gradient background generation and
    font metrics for responsive text display.
    
    Attributes:
        last_n (int): The last number used for prime calculation
        last_primes (list): List of calculated prime numbers
        count_label (tk.Label): GUI label for displaying prime count
        status_label (tk.Label): GUI label for displaying calculation status
        text (tk.Text): GUI text widget for displaying results
        calculation_time (float): Time taken for the last calculation
        text_font (tkfont.Font): Monospace font for number display
        char_width (int): Width of a single character in pixels
        char_height (int): Height of a single line in pixels
        bg_image (ImageTk.PhotoImage): Gradient background image
        bg_label (tk.Label): Label containing the background image
    """
    
    def __init__(self, root):
        """
        Initialize the PrimeCalculator with default values and UI setup.
        
        Args:
            root (tk.Tk): The main tkinter window instance
            
        Sets up font metrics, creates the gradient background, and initializes
        all instance variables for prime calculation and display.
        """
        # Initialize calculation state
        self.last_n = None
        self.last_primes = []
        self.calculation_time = 0
        
        # Initialize GUI component references (set later by create_gui)
        self.count_label = None
        self.status_label = None
        self.text = None
        
        # Setup font metrics for responsive text display
        # Using Courier New ensures consistent character width (monospace)
        self.text_font = tkfont.Font(family="Courier New", size=11)
        self.char_width = self.text_font.measure("0")  # All chars same width in monospace
        self.char_height = self.text_font.metrics("linespace")
        
        # Create and apply gradient background
        self.bg_image = self.create_gradient(root.winfo_screenwidth(), root.winfo_screenheight())
        self.bg_label = tk.Label(root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_gradient(self, width, height):
        """
        Generate a beautiful gradient background image.
        
        Creates a vertical gradient from blue at the top to white at the bottom,
        providing a modern, professional appearance for the application.
        
        Args:
            width (int): Width of the gradient image in pixels
            height (int): Height of the gradient image in pixels
            
        Returns:
            ImageTk.PhotoImage: The gradient image ready for tkinter display
            
        Note:
            Uses PIL to create the gradient by drawing horizontal lines
            with gradually changing colors from top to bottom.
        """
        # Create new RGB image with specified dimensions
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)
        
        # Create vertical gradient from blue-ish top to white bottom
        for y in range(height):
            # Calculate RGB values based on vertical position
            # Top: darker blue (30, 144, 255)
            # Bottom: lighter blue-white (255, 255, 255)
            r = int(30 + (225 * y / height))    # Red: 30 → 255
            g = int(144 + (111 * y / height))   # Green: 144 → 255  
            b = int(255 - (255 * y / height))  # Blue: 255 → 0
            
            # Draw horizontal line at current y position
            draw.line((0, y, width, y), fill=(r, g, b))
            
        return ImageTk.PhotoImage(image)

    def format_primes(self):
        """
        Format the calculated prime numbers for display in the GUI.
        
        Creates a nicely formatted string representation of all prime numbers
        with intelligent column sizing based on the current window width.
        Also updates the status labels with calculation statistics.
        
        Returns:
            str: Formatted string ready for display in the text widget
            
        Features:
            - Calculates optimal number of columns based on window width
            - Aligns numbers in a clean grid using monospace font
            - Includes header with total count and separator line
            - Updates GUI labels with count and timing information
            
        Note:
            Returns empty string if no primes have been calculated yet.
        """
        if not self.last_primes:
            return ""
        
        # Update GUI status labels with calculation results
        count = len(self.last_primes)
        self.count_label.config(
            text=f"Found {count:,} prime numbers up to {self.last_n:,}",
            fg="#007ACC"  # Professional blue color
        )
        self.status_label.config(
            text=f"✓ Calculation complete in {self.calculation_time:.2f} seconds",
            fg="#28A745"  # Success green color
        )
        
        # Calculate formatting parameters
        max_digits = len(str(max(self.last_primes)))  # Width needed for largest prime
        num_format = f"{{:>{max_digits}}} "           # Right-aligned with space separator
        
        # Calculate optimal column layout based on window width
        widget_width = self.text.winfo_width()
        total_width = max(widget_width - 20, 0)  # Account for padding
        chars_per_line = total_width // self.char_width if self.char_width != 0 else 0
        num_cols = max(1, chars_per_line // (max_digits + 1)) if (max_digits + 1) != 0 else 1
        
        # Format primes into rows and columns
        formatted_rows = []
        row = []
        
        for index, prime in enumerate(self.last_primes, start=1):
            row.append(num_format.format(prime))
            
            # Start new row when current row is full
            if index % num_cols == 0:
                formatted_rows.append(''.join(row).rstrip())
                row = []
        
        # Handle any remaining numbers in the last incomplete row
        if row:
            # Pad incomplete row with spaces for consistent formatting
            while len(row) < num_cols:
                row.append(' ' * (max_digits + 1))
            formatted_rows.append(''.join(row).rstrip())
        
        # Create header section
        header = f"Prime numbers up to {self.last_n:,}:\n"
        if formatted_rows:
            separator = '=' * len(formatted_rows[0])
        else:
            separator = '=' * (num_cols * (max_digits + 1))
        header += separator + "\n"
        
        return header + '\n'.join(formatted_rows)

    def calculate_primes(self, n):
        """
        Calculate all prime numbers up to n using the Sieve of Eratosthenes.
        
        This is the core algorithm implementation that efficiently finds all
        prime numbers up to a given limit using the ancient Sieve of Eratosthenes
        algorithm, which is one of the most efficient methods for this purpose.
        
        Args:
            n (int): The upper limit for prime calculation (inclusive)
            
        Returns:
            str: Formatted string of all prime numbers ready for display
            
        Algorithm Steps:
            1. Create a boolean array "sieve" of size n+1, initially all True
            2. Mark 0 and 1 as not prime (special cases)
            3. For each number i from 2 to √n:
               - If sieve[i] is True (i is prime):
                 - Mark all multiples of i starting from i² as not prime
            4. Collect all numbers where sieve[i] is True
            
        Time Complexity: O(n log log n)
        Space Complexity: O(n)
        
        Performance Optimizations:
            - Only check numbers up to √n (any composite > √n has a factor ≤ √n)
            - Start marking multiples from i² (smaller multiples already marked)
            - Use boolean array for memory efficiency
            - Time the calculation for performance feedback
        """
        self.last_n = n
        
        # Step 1: Create boolean array - True means "potentially prime"
        sieve = [True] * (n + 1)
        
        # Step 2: Mark 0 and 1 as not prime (by mathematical definition)
        sieve[0] = sieve[1] = False
        
        # Step 3: Start timing the core algorithm
        start_time = time.time()
        
        # Step 4: Sieve of Eratosthenes main loop
        # Only need to check up to √n because any composite number > √n
        # must have a prime factor ≤ √n
        for current in range(2, int(n**0.5) + 1):
            if sieve[current]:  # If current number is prime
                # Mark all multiples of current as not prime
                # Start from current² because smaller multiples
                # were already marked by smaller primes
                for multiple in range(current * current, n + 1, current):
                    sieve[multiple] = False
        
        # Step 5: Collect all prime numbers (indices where sieve[i] is True)
        self.last_primes = [i for i, is_prime in enumerate(sieve) if is_prime]
        
        # Step 6: Calculate and store timing information
        end_time = time.time()
        self.calculation_time = end_time - start_time
        
        # Step 7: Return formatted results for display
        return self.format_primes()

    def set_text_widget(self, text_widget):
        """
        Store a reference to the GUI text widget for formatting calculations.
        
        This method is called by the GUI creation function to provide the
        PrimeCalculator with access to the text widget, which is needed
        for calculating optimal column layouts based on widget width.
        
        Args:
            text_widget (tk.Text): The text widget that will display results
        """
        self.text = text_widget


def create_gui(root):
    """
    Create and configure the complete user interface for the application.
    
    This function builds the entire GUI including input fields, result display,
    status labels, and all interactive elements. It also sets up event handlers
    for user interactions and window resizing.
    
    Args:
        root (tk.Tk): The main tkinter window instance
        
    GUI Components Created:
        - Title section with application name
        - Input section with entry field and instructions
        - Status section with count and timing labels
        - Results section with scrollable text display
        - Event handlers for input validation and window resizing
        
    Features:
        - Responsive design that adapts to window size
        - Real-time number formatting with thousands separators
        - Auto-hiding scrollbars that appear only when needed
        - Comprehensive input validation and error handling
        - Keyboard shortcuts (Enter key for calculation)
        - Professional color scheme and typography
    """
    # Configure main window properties
    root.title("Prime Number Calculator")
    root.configure(bg="#F0F2F5")  # Light gray background
    
    # Initialize the core calculator logic
    calculator = PrimeCalculator(root)
    
    # Create main container with padding for professional appearance
    main_frame = tk.Frame(root, bg="#F0F2F5")
    main_frame.pack(padx=25, pady=25, fill=tk.BOTH, expand=True)
    
    # === TITLE SECTION ===
    title_frame = tk.Frame(main_frame, bg="#F0F2F5")
    title_frame.pack(fill=tk.X, pady=(0, 20))
    
    title_label = tk.Label(
        title_frame,
        text="Prime Number Calculator",
        font=("Segoe UI", 16, "bold"),
        bg="#F0F2F5",
        fg="#202124"  # Dark gray text
    )
    title_label.pack()
    
    # === INPUT SECTION ===
    # Container for input field and instructions
    input_frame = tk.Frame(main_frame, bg="#FFFFFF")
    input_frame.pack(fill=tk.X, pady=(0, 20))
    
    # Instructions for users
    instruction_label = tk.Label(
        input_frame,
        text="Enter a number greater than 1 and press Enter to find all prime numbers up to that value:",
        font=("Segoe UI", 10),
        bg="#FFFFFF",
        fg="#202124"
    )
    instruction_label.pack(pady=(10, 5), padx=15)
    
    # Main input field with professional styling
    entry = tk.Entry(
        input_frame,
        width=20,
        font=("Segoe UI", 11),
        relief=tk.SOLID,
        bd=1,
        justify='center',
        highlightthickness=2,
        highlightbackground="#0000FF"  # Blue focus border
    )
    entry.pack(pady=10, padx=15)

    def format_number(event=None):
        """
        Format the input number with thousands separators in real-time.
        
        This function is called on every keystroke to automatically format
        the entered number with commas for better readability. It preserves
        the cursor position and handles edge cases like backspace and selection.
        
        Args:
            event: The tkinter event object (not used)
            
        Returns:
            bool: Always returns True to allow the event to continue
            
        Features:
            - Adds thousands separators (1,000,000)
            - Preserves cursor position during formatting
            - Only formats valid numeric input
            - Handles cursor position adjustment for added/removed commas
        """
        # Get current value without existing commas and cursor position
        value = entry.get().replace(',', '')
        cursor_pos = entry.index(tk.INSERT)
        
        # Only format if the value is purely numeric
        if value.isdigit():
            # Count existing commas before cursor for position adjustment
            orig_commas = entry.get()[:cursor_pos].count(',')
            
            # Format with thousands separators
            formatted = "{:,}".format(int(value))
            
            # Count new commas before cursor position
            new_commas = formatted[:cursor_pos].count(',')
            
            # Update entry field with formatted text
            entry.delete(0, tk.END)
            entry.insert(0, formatted)
            
            # Adjust cursor position based on comma changes
            new_pos = cursor_pos + (new_commas - orig_commas)
            entry.icursor(new_pos)
        
        return True

    # Bind number formatting to key release events
    entry.bind('<KeyRelease>', format_number)
    
    # === STATUS SECTION ===
    # Container for status and count labels
    status_frame = tk.Frame(input_frame, bg="#FFFFFF")
    status_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
    
    # Label for displaying prime count
    count_label = tk.Label(
        status_frame,
        text="",
        font=("Segoe UI", 12, "bold"),
        bg="#FFFFFF",
        anchor="center"
    )
    count_label.pack(fill=tk.X, pady=(5, 0))
    
    # Label for displaying calculation status and timing
    status_label = tk.Label(
        status_frame,
        text="",
        font=("Segoe UI", 10),
        bg="#FFFFFF",
        anchor="center"
    )
    status_label.pack(fill=tk.X)
    
    # Connect status labels to calculator instance
    calculator.count_label = count_label
    calculator.status_label = status_label
    
    # === RESULTS SECTION ===
    # Container for results display with scrolling
    results_frame = tk.Frame(main_frame, bg="#FFFFFF", highlightthickness=0)
    results_frame.pack(fill=tk.BOTH, expand=True)
    
    # Vertical scrollbar (hidden by default, shown when needed)
    v_scroll = tk.Scrollbar(results_frame, orient=tk.VERTICAL)

    # Main text area for displaying prime numbers
    text = tk.Text(
        results_frame,
        wrap=tk.WORD,
        font=calculator.text_font,  # Monospace font for alignment
        bg="#FFFFFF",
        relief=tk.SOLID,
        bd=1,
        padx=3,
        pady=3,
        state=tk.DISABLED,  # Read-only by default
        yscrollcommand=v_scroll.set
    )
    text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    # Configure scrollbar
    v_scroll.config(command=text.yview)
    
    def update_scrollbar_visibility(event=None):
        """
        Show or hide the scrollbar based on content length.
        
        This function automatically manages scrollbar visibility to keep
        the interface clean when scrolling isn't needed.
        
        Args:
            event: The tkinter event object (not used)
            
        Logic:
            - Shows scrollbar when content exceeds visible area
            - Hides scrollbar when all content fits in the widget
            - Prevents unnecessary UI clutter
        """
        # Calculate total content height vs visible area
        text_height = float(text.index('end-1c').split('.')[0])
        visible_lines = text.winfo_height() / text.dlineinfo('1.0')[3] if text.dlineinfo('1.0') else 1
        
        # Show scrollbar only when content overflows
        if text_height > visible_lines:
            v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            v_scroll.pack_forget()
    
    # Bind scrollbar visibility updates to text changes
    text.bind('<<Modified>>', update_scrollbar_visibility)
    
    # === WINDOW RESIZE HANDLING ===
    # Debounced resize handling for better performance
    resize_after_id = None
    
    def on_resize(event):
        """
        Handle window resize events with debouncing for performance.
        
        When the window is resized, the prime number display needs to be
        reformatted to fit the new width. This function uses debouncing
        to avoid excessive recalculations during window dragging.
        
        Args:
            event: The tkinter resize event object
            
        Features:
            - 250ms debounce delay to avoid excessive calculations
            - Only reformats if prime numbers are already calculated
            - Cancels previous scheduled updates to prevent overlap
        """
        nonlocal resize_after_id
        
        # Only reformat if we have results to display
        if calculator.last_primes:
            # Cancel any pending update to avoid duplicate work
            if resize_after_id:
                root.after_cancel(resize_after_id)
            
            # Schedule new update with 250ms delay
            resize_after_id = root.after(250, lambda: update_text_content())
    
    def update_text_content():
        """
        Update the text widget with reformatted prime numbers.
        
        This function is called after window resize to reformat the
        prime number display to fit the new window width optimally.
        """
        # Temporarily enable editing to update content
        text.config(state=tk.NORMAL)
        text.delete(1.0, tk.END)
        
        # Get newly formatted text with updated column layout
        formatted_text = calculator.format_primes()
        text.insert(tk.END, formatted_text)
        
        # Restore read-only state and update scrollbar
        text.config(state=tk.DISABLED)
        update_scrollbar_visibility()
    
    # Bind resize handler to root window
    root.bind("<Configure>", on_resize)

    # Store text widget reference in calculator for width calculations
    calculator.set_text_widget(text)

    def on_calculate(n_str):
        """
        Handle prime number calculation with comprehensive error handling.
        
        This function is the main entry point for prime calculation, handling
        input validation, error cases, and updating the GUI with results.
        
        Args:
            n_str (str): The input string from the entry field
            
        Error Handling:
            - Empty input validation
            - Non-numeric input detection
            - Range validation (must be > 1)
            - Unexpected error catching with user-friendly messages
            
        Features:
            - Real-time status updates during calculation
            - Performance timing display
            - Input sanitization (removes commas)
            - User-friendly error messages
        """
        try:
            # Show calculation in progress
            status_label.config(text="Calculating...", fg="#FFA500")  # Orange color
            root.update()  # Force GUI update
            
            # Sanitize input by removing formatting
            n_str = n_str.replace(',', '')
            
            # Validate input is not empty
            if not n_str.strip():
                messagebox.showerror("Input Error", "Please enter a number")
                status_label.config(text="")
                return
            
            # Validate input is numeric
            if not n_str.strip().isdigit():
                messagebox.showerror("Input Error", "Please enter only numbers (no letters or special characters)")
                status_label.config(text="")
                return
            
            # Convert to integer
            n = int(n_str)
            
            # Validate range (must be > 1 for meaningful prime calculation)
            if n <= 1:
                messagebox.showerror("Input Error", "Number must be greater than 1")
                status_label.config(text="")
                return
            
            # Record start time for performance measurement
            start_time = time.time()
            
            # Perform the prime calculation
            primes = calculator.calculate_primes(n)
            
            # Update timing information
            calculator.calculation_time = time.time() - start_time
            
            # Update the display with results
            text.config(state=tk.NORMAL)  # Enable editing temporarily
            text.delete(1.0, tk.END)
            formatted_text = calculator.format_primes()
            text.insert(tk.END, formatted_text)
            text.config(state=tk.DISABLED)  # Restore read-only state
            
        except ValueError:
            # Handle conversion errors
            messagebox.showerror("Input Error", "Please enter a valid integer greater than 1")
            status_label.config(text="")
        except Exception as e:
            # Handle any unexpected errors
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            status_label.config(text="")

    # === EVENT BINDING ===
    # Bind calculation to Enter key presses
    entry.bind("<Return>", lambda event: on_calculate(entry.get()))
    entry.bind("<KP_Enter>", lambda event: on_calculate(entry.get()))  # Numeric keypad Enter
    
    # Custom backspace handling for formatted input
    entry.bind("<BackSpace>", lambda event: "break" if event.widget.select_present() 
              else entry.delete(entry.index(tk.INSERT)-1))

    # Set initial focus to input field for immediate use
    entry.focus_set()


def main():
    """
    Main entry point for the Prime Number Calculator application.
    
    This function initializes the tkinter window, sets up the GUI,
    and starts the main event loop. It handles window sizing,
    positioning, and initial configuration.
    
    Features:
        - Centers the window on screen
        - Sets appropriate window size (800x800)
        - Initializes all GUI components
        - Starts the tkinter event loop
        
    Window Configuration:
        - Size: 800x800 pixels
        - Position: Centered on screen
        - Title: "Prime Number Calculator"
        - Resizable: Yes (responsive design)
    """
    # Create main tkinter window
    root = tk.Tk()
    
    # Get screen dimensions for centering
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Set window dimensions
    window_width = 800
    window_height = 800
    
    # Calculate center position
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    
    # Apply window geometry and title
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    root.title("Prime Number Calculator")
    
    # Build the complete GUI
    create_gui(root)
    
    # Start the main event loop
    root.mainloop()


# Application entry point
if __name__ == "__main__":
    main()