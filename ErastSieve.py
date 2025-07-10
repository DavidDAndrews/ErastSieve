import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkfont
import time
from tkinter import ttk
from PIL import Image, ImageTk

# First, define the rounded rectangle function at the top of the file
def create_rounded_rect(self, x1, y1, x2, y2, radius=25, **kwargs):
    """Create rounded rectangle on canvas"""
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    return self.create_polygon(points, **kwargs, smooth=True)

# Then add it to the Canvas class
tk.Canvas.create_rounded_rect = create_rounded_rect

class PrimeCalculator:
    def __init__(self, root):
        self.root = root
        self.last_n = None
        self.last_primes = []
        self.count_label = None
        self.status_label = None
        self.text = None  # Will hold the Text widget reference
        self.calculation_time = 0
        
        # Initialize font metrics using a true monospace font
        self.text_font = tkfont.Font(family="Courier New", size=11)
        self.char_width = self.text_font.measure("0")  # Width of a single character
        self.char_height = self.text_font.metrics("linespace")  # Height of a single line

        # Add gradient background
        self.bg_image = self.create_gradient(root.winfo_screenwidth(), root.winfo_screenheight())
        self.bg_label = tk.Label(root, image=self.bg_image)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def create_gradient(self, width, height):
        """Create a gradient background image"""
        from PIL import Image, ImageDraw
        image = Image.new('RGB', (width, height))
        draw = ImageDraw.Draw(image)
        
        # Create gradient from top to bottom
        for y in range(height):
            r = int(30 + (225 * y / height))
            g = int(144 + (111 * y / height))
            b = int(255 - (255 * y / height))
            draw.line((0, y, width, y), fill=(r, g, b))
            
        return ImageTk.PhotoImage(image)

    def format_primes(self):
        if not self.last_primes:
            return ""
            
        # Update status labels
        count = len(self.last_primes)
        self.count_label.config(
            text=f"Found {count:,} prime numbers up to {self.last_n:,}",
            fg="#007ACC"
        )
        self.status_label.config(
            text=f"✓ Calculation complete in {self.calculation_time:.2f} seconds",
            fg="#28A745"
        )
        
        # Determine the maximum number of digits in primes
        max_digits = len(str(max(self.last_primes)))

        # Define number formatting with fixed width
        num_format = f"{{:>{max_digits}}} "  # One space between numbers

        # Calculate the number of characters that fit per line
        widget_width = self.text.winfo_width()
        total_width = max(widget_width - 20, 0)  # Reduced from 40 to 20
        chars_per_line = total_width // self.char_width if self.char_width != 0 else 0

        num_cols = max(1, chars_per_line // (max_digits + 1)) if (max_digits + 1) != 0 else 1

        # Generate formatted rows
        formatted_rows = []
        row = []
        
        for index, prime in enumerate(self.last_primes, start=1):
            row.append(num_format.format(prime))
            if index % num_cols == 0:
                formatted_rows.append(''.join(row).rstrip())
                row = []

        # Append any remaining numbers, padding with spaces if necessary
        if row:
            while len(row) < num_cols:
                row.append(' ' * (max_digits + 1))
            formatted_rows.append(''.join(row).rstrip())

        # Create header
        header = f"Prime numbers up to {self.last_n:,}:\n"
        if formatted_rows:
            separator = '=' * len(formatted_rows[0])
        else:
            separator = '=' * (num_cols * (max_digits + 1))
        header += separator + "\n"
        
        return header + '\n'.join(formatted_rows)

    def calculate_primes(self, n):
        self.last_n = n
        sieve = [True] * (n+1)
        sieve[0] = sieve[1] = False
        start_time = time.time()
        for current in range(2, int(n**0.5) + 1):
            if sieve[current]:
                for multiple in range(current*current, n+1, current):
                    sieve[multiple] = False
        
        self.last_primes = [i for i, is_prime in enumerate(sieve) if is_prime]
        end_time = time.time()
        self.calculation_time = end_time - start_time
        return self.format_primes()

    def set_text_widget(self, text_widget):
        """Store the Text widget reference."""
        self.text = text_widget

def create_gui(root):
    root.title("Prime Number Calculator")
    root.configure(bg="#F0F2F5")
    
    calculator = PrimeCalculator(root)
    
    # Main container with padding
    main_frame = tk.Frame(root, bg="#F0F2F5")
    main_frame.pack(padx=25, pady=25, fill=tk.BOTH, expand=True)
    
    # Title Section
    title_frame = tk.Frame(main_frame, bg="#F0F2F5")
    title_frame.pack(fill=tk.X, pady=(0, 20))
    
    title_label = tk.Label(
        title_frame,
        text="Prime Number Calculator",
        font=("Segoe UI", 16, "bold"),
        bg="#F0F2F5",
        fg="#202124"
    )
    title_label.pack()
    
    # Input Section - removed LabelFrame and using regular Frame
    input_frame = tk.Frame(
        main_frame,
        bg="#FFFFFF"
    )
    input_frame.pack(fill=tk.X, pady=(0, 20))
    
    # Instructions (updated to mention Enter key)
    instruction_label = tk.Label(
        input_frame,
        text="Enter a number greater than 1 and press Enter to find all prime numbers up to that value:",
        font=("Segoe UI", 10),
        bg="#FFFFFF",
        fg="#202124"
    )
    instruction_label.pack(pady=(10, 5), padx=15)
    
    # Entry with validation feedback
    entry = tk.Entry(
        input_frame,
        width=20,
        font=("Segoe UI", 11),
        relief=tk.SOLID,
        bd=1,
        justify='center',
        highlightthickness=2,
        highlightbackground="#0000FF"  # Blue color for the border
    )
    entry.pack(pady=10, padx=15)

    def format_number(event=None):
        # Get current value and cursor position
        value = entry.get().replace(',', '')  # Remove existing commas
        cursor_pos = entry.index(tk.INSERT)
        
        # Only proceed if the value is numeric
        if value.isdigit():
            # Count commas before cursor to adjust position
            orig_commas = entry.get()[:cursor_pos].count(',')
            
            # Format with commas
            formatted = "{:,}".format(int(value))
            
            # Count new commas before cursor
            new_commas = formatted[:cursor_pos].count(',')
            
            # Update entry with formatted text
            entry.delete(0, tk.END)
            entry.insert(0, formatted)
            
            # Adjust cursor position based on added/removed commas
            new_pos = cursor_pos + (new_commas - orig_commas)
            entry.icursor(new_pos)
        
        return True

    # Bind to key events
    entry.bind('<KeyRelease>', format_number)
    
    # Status labels
    status_frame = tk.Frame(input_frame, bg="#FFFFFF")
    status_frame.pack(fill=tk.X, padx=15, pady=(0, 10))  # Added bottom padding
    
    count_label = tk.Label(
        status_frame,
        text="",
        font=("Segoe UI", 12, "bold"),  # Increased size from 10 to 12 and added bold
        bg="#FFFFFF",
        anchor="center"
    )
    count_label.pack(fill=tk.X, pady=(5,0))  # Added some padding above
    
    status_label = tk.Label(
        status_frame,
        text="",
        font=("Segoe UI", 10),
        bg="#FFFFFF",
        anchor="center"
    )
    status_label.pack(fill=tk.X)  # Changed from side=tk.RIGHT to fill=tk.X
    
    calculator.count_label = count_label
    calculator.status_label = status_label
    
    # Results Section with centered content
    results_frame = tk.Frame(
        main_frame,
        bg="#FFFFFF",
        highlightthickness=0
    )
    results_frame.pack(fill=tk.BOTH, expand=True)
    
    # Add vertical scrollbar only
    v_scroll = tk.Scrollbar(results_frame, orient=tk.VERTICAL)

    # Create text area with monospace font
    text = tk.Text(
        results_frame,
        wrap=tk.WORD,
        font=calculator.text_font,
        bg="#FFFFFF",
        relief=tk.SOLID,
        bd=1,
        padx=3,
        pady=3,
        state=tk.DISABLED,
        yscrollcommand=v_scroll.set
    )
    text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    
    v_scroll.config(command=text.yview)
    
    # Show scrollbar only when needed
    def update_scrollbar_visibility(event=None):
        text_height = float(text.index('end-1c').split('.')[0])
        visible_lines = text.winfo_height() / text.dlineinfo('1.0')[3] if text.dlineinfo('1.0') else 1
        
        if text_height > visible_lines:
            v_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        else:
            v_scroll.pack_forget()
    
    # Bind the update to relevant events
    text.bind('<<Modified>>', update_scrollbar_visibility)
    
    # Resize handling with debouncing
    resize_after_id = None
    def on_resize(event):
        nonlocal resize_after_id
        if calculator.last_primes:
            # Cancel previous scheduled update
            if resize_after_id:
                root.after_cancel(resize_after_id)
            # Schedule new update with 250ms delay
            resize_after_id = root.after(250, lambda: update_text_content())
    
    def update_text_content():
        text.config(state=tk.NORMAL)
        text.delete(1.0, tk.END)
        formatted_text = calculator.format_primes()
        text.insert(tk.END, formatted_text)
        text.config(state=tk.DISABLED)
        update_scrollbar_visibility()
    
    root.bind("<Configure>", on_resize)

    # Store the text widget in the PrimeCalculator instance
    calculator.set_text_widget(text)

    def on_calculate(n_str):
        try:
            # Clear previous status
            status_label.config(text="Calculating...", fg="#FFA500")
            root.update()
            
            # Remove commas from the input string
            n_str = n_str.replace(',', '')
            
            if not n_str.strip():
                messagebox.showerror("Input Error", "Please enter a number")
                status_label.config(text="")
                return
                
            if not n_str.strip().isdigit():
                messagebox.showerror("Input Error", "Please enter only numbers (no letters or special characters)")
                status_label.config(text="")
                return
                
            n = int(n_str)
            
            if n <= 1:
                messagebox.showerror("Input Error", "Number must be greater than 1")
                status_label.config(text="")
                return
            
            # Start timing
            start_time = time.time()
            
            primes = calculator.calculate_primes(n)
            
            # Calculate elapsed time
            calculator.calculation_time = time.time() - start_time
            
            text.config(state=tk.NORMAL)  # Make editable temporarily
            text.delete(1.0, tk.END)
            formatted_text = calculator.format_primes()
            text.insert(tk.END, formatted_text)
            text.config(state=tk.DISABLED)  # Make read-only again
            
        except ValueError:
            messagebox.showerror("Input Error", "Please enter a valid integer greater than 1")
            status_label.config(text="")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {str(e)}")
            status_label.config(text="")

    # Bind keys
    entry.bind('<Key>', lambda e: None if e.char == '' else None)
    entry.bind("<Return>", lambda event: on_calculate(entry.get()))
    entry.bind("<KP_Enter>", lambda event: on_calculate(entry.get()))
    entry.bind("<BackSpace>", lambda event: "break" if event.widget.select_present() 
              else entry.delete(entry.index(tk.INSERT)-1))

    # Set focus to entry
    entry.focus_set()  # Automatically focus the entry field when the app starts

def main():
    root = tk.Tk()
    
    # Get screen width and height
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    
    # Set window size (doubled from 400x400 to 800x800)
    window_width = 800
    window_height = 800
    
    # Calculate position x, y coordinates
    x = int((screen_width / 2) - (window_width / 2))
    y = int((screen_height / 2) - (window_height / 2))
    
    root.geometry(f'{window_width}x{window_height}+{x}+{y}')
    root.title("Prime Number Calculator")
    
    create_gui(root)
    
    # Start the main event loop
    root.mainloop()

# Add this to actually run the main function when the script is executed
if __name__ == "__main__":
    main()