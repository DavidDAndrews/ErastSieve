"""
Graphical User Interface for the Prime Number Calculator.

This module provides a modern, feature-rich GUI with dark mode support,
export functionality, and improved user experience.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.font as tkfont
import threading
from pathlib import Path
from typing import Optional, List

from .prime_calculator import PrimeCalculator
from .config import *
from .utils import (
    format_number_with_commas,
    parse_number_input,
    export_to_csv,
    export_to_txt,
    export_to_json,
    export_to_html,
    copy_to_clipboard,
    format_time,
    format_bytes,
    estimate_memory_usage
)


class PrimeCalculatorGUI:
    """Main GUI class for the Prime Number Calculator."""
    
    def __init__(self, root: tk.Tk):
        """Initialize the GUI with all components."""
        self.root = root
        self.calculator = PrimeCalculator()
        self.dark_mode = False
        self.current_primes: List[int] = []
        self.calculation_thread: Optional[threading.Thread] = None
        self.progress_var = tk.DoubleVar()
        
        self._setup_window()
        self._create_widgets()
        self._apply_theme()
        self._setup_resize_handler()
        
    def _setup_window(self):
        """Configure the main window."""
        self.root.title("Prime Number Calculator v2.0")
        self.root.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)
        
        # Center window
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width - WINDOW_WIDTH) // 2
        y = (screen_height - WINDOW_HEIGHT) // 2
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{x}+{y}")
        
    def _create_widgets(self):
        """Create all GUI widgets."""
        # Main container
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING, pady=PADDING)
        
        # Title and theme toggle
        self._create_header()
        
        # Input section
        self._create_input_section()
        
        # Progress bar
        self._create_progress_section()
        
        # Results section
        self._create_results_section()
        
        # Export buttons
        self._create_export_section()
        
    def _create_header(self):
        """Create header with title and theme toggle."""
        header_frame = tk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        self.title_label = tk.Label(
            header_frame,
            text="Prime Number Calculator",
            font=FONTS["title"]
        )
        self.title_label.pack(side=tk.LEFT)
        
        # Theme toggle button - use ttk
        self.theme_btn = ttk.Button(
            header_frame,
            text="Dark Mode",
            command=self._toggle_theme,
            cursor="hand2",
            style="Theme.TButton"
        )
        self.theme_btn.pack(side=tk.RIGHT)
        
    def _create_input_section(self):
        """Create input section with entry and preset buttons."""
        input_frame = tk.LabelFrame(
            self.main_frame,
            text="Input",
            font=FONTS["normal"],
            padx=15,
            pady=10
        )
        input_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Instructions
        instruction_label = tk.Label(
            input_frame,
            text="Enter a number or use presets:",
            font=FONTS["small"]
        )
        instruction_label.pack(anchor=tk.W)
        
        # Entry and calculate button frame
        entry_frame = tk.Frame(input_frame)
        entry_frame.pack(fill=tk.X, pady=(5, 10))
        
        # Entry field
        self.entry = tk.Entry(
            entry_frame,
            font=FONTS["normal"],
            width=30
        )
        self.entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.entry.bind("<Return>", lambda _: self._calculate())
        self.entry.bind("<KeyRelease>", self._format_entry)
        
        # Calculate button - use ttk for better macOS compatibility
        self.calc_btn = ttk.Button(
            entry_frame,
            text="Calculate",
            command=self._calculate,
            cursor="hand2"
        )
        self.calc_btn.pack(side=tk.LEFT, padx=(10, 0))
        
        # Stop button (hidden initially) - use ttk
        self.stop_btn = ttk.Button(
            entry_frame,
            text="Stop",
            command=self._stop_calculation,
            cursor="hand2"
        )
        
        # Preset buttons
        preset_frame = tk.Frame(input_frame)
        preset_frame.pack(fill=tk.X)
        
        tk.Label(preset_frame, text="Presets:", font=FONTS["small"]).pack(side=tk.LEFT, padx=(0, 10))
        
        # Store preset buttons for theme updates
        self.preset_buttons = []
        for label, value in PRESETS:
            # Use ttk.Button for better macOS compatibility
            btn = ttk.Button(
                preset_frame,
                text=str(label),
                command=lambda v=value: self._set_preset(v),
                cursor="hand2",
                width=6
            )
            btn.pack(side=tk.LEFT, padx=3)
            self.preset_buttons.append(btn)
            
    def _create_progress_section(self):
        """Create progress bar section."""
        self.progress_frame = tk.Frame(self.main_frame)
        self.progress_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.progress_label = tk.Label(
            self.progress_frame,
            text="",
            font=FONTS["small"]
        )
        self.progress_label.pack(side=tk.LEFT)
        
        self.progress_bar = ttk.Progressbar(
            self.progress_frame,
            variable=self.progress_var,
            mode='determinate'
        )
        
    def _create_results_section(self):
        """Create results display section."""
        results_frame = tk.LabelFrame(
            self.main_frame,
            text="Results",
            font=FONTS["normal"],
            padx=10,
            pady=10
        )
        results_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Statistics labels
        stats_frame = tk.Frame(results_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.count_label = tk.Label(
            stats_frame,
            text="Ready to calculate",
            font=FONTS["normal"]
        )
        self.count_label.pack()
        
        self.stats_label = tk.Label(
            stats_frame,
            text="",
            font=FONTS["small"]
        )
        self.stats_label.pack()
        
        # Text display with scrollbar
        text_frame = tk.Frame(results_frame)
        text_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbars - use ttk for better theming
        v_scroll = ttk.Scrollbar(text_frame, orient=tk.VERTICAL)
        h_scroll = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
        
        # Text widget with equal padding on both sides
        self.text = tk.Text(
            text_frame,
            wrap=tk.NONE,
            font=FONTS["monospace"],
            yscrollcommand=v_scroll.set,
            xscrollcommand=h_scroll.set,
            state=tk.DISABLED,
            padx=10  # Equal padding left and right
        )
        
        v_scroll.config(command=self.text.yview)
        h_scroll.config(command=self.text.xview)
        
        # Grid layout
        self.text.grid(row=0, column=0, sticky="nsew")
        v_scroll.grid(row=0, column=1, sticky="ns")
        h_scroll.grid(row=1, column=0, sticky="ew")
        
        text_frame.grid_rowconfigure(0, weight=1)
        text_frame.grid_columnconfigure(0, weight=1)
        
    def _create_export_section(self):
        """Create export buttons section."""
        export_frame = tk.LabelFrame(
            self.main_frame,
            text="Export Options",
            font=FONTS["normal"],
            padx=10,
            pady=10
        )
        export_frame.pack(fill=tk.X)
        
        # Export buttons
        buttons = [
            ("Copy to Clipboard", self._copy_to_clipboard),
            ("Save as CSV", lambda: self._export("csv")),
            ("Save as TXT", lambda: self._export("txt")),
            ("Save as JSON", lambda: self._export("json")),
            ("Save as HTML", lambda: self._export("html")),
        ]
        
        # Initialize export buttons list
        self.export_buttons = []
        
        for text, command in buttons:
            # Use ttk.Button for better macOS compatibility
            btn = ttk.Button(
                export_frame,
                text=str(text),
                command=command,
                cursor="hand2",
                state=tk.DISABLED
            )
            btn.pack(side=tk.LEFT, padx=5)
            self.export_buttons.append(btn)
            
    def _toggle_theme(self):
        """Toggle between light and dark themes."""
        self.dark_mode = not self.dark_mode
        self.theme_btn.config(text="Light Mode" if self.dark_mode else "Dark Mode")
        self._apply_theme()
        
    def _apply_theme(self):
        """Apply the current theme to all widgets."""
        theme = get_theme(self.dark_mode)
        
        # Configure root and main frame
        self.root.config(bg=theme["bg"])
        self.main_frame.config(bg=theme["bg"])
        
        # Update all widgets recursively
        self._apply_theme_to_widget(self.root, theme)
        
        # Update ttk styles
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure ttk button style
        style.configure("TButton",
                       background=theme["button_bg"],
                       foreground=theme["button_fg"],
                       bordercolor=theme["fg"],
                       focuscolor='none',
                       relief="raised")
        style.map("TButton",
                 background=[('active', theme["button_hover"]), ('pressed', theme["button_hover"])],
                 foreground=[('active', theme["button_fg"]), ('pressed', theme["button_fg"])])
        
        # Configure progress bar
        style.configure("TProgressbar", 
                       background=theme["button_bg"],
                       troughcolor=theme["input_bg"],
                       bordercolor=theme["fg"],
                       lightcolor=theme["button_bg"],
                       darkcolor=theme["button_bg"])
        
        # Configure theme button style separately
        style.configure("Theme.TButton",
                       background=theme["button_bg"],
                       foreground=theme["button_fg"],
                       bordercolor=theme["fg"],
                       focuscolor='none')
        style.map("Theme.TButton",
                 background=[('active', theme["button_hover"])],
                 foreground=[('active', theme["button_fg"])])
        
        # Configure scrollbar style based on theme
        if self.dark_mode:
            # Dark scrollbar for dark mode
            style.configure("Vertical.TScrollbar",
                           background="#3d3d3d",
                           troughcolor="#2d2d2d",
                           bordercolor="#2d2d2d",
                           arrowcolor="#e0e0e0",
                           darkcolor="#3d3d3d",
                           lightcolor="#3d3d3d")
            style.map("Vertical.TScrollbar",
                     background=[('active', '#4d4d4d'), ('pressed', '#5d5d5d')])
            
            style.configure("Horizontal.TScrollbar",
                           background="#3d3d3d",
                           troughcolor="#2d2d2d",
                           bordercolor="#2d2d2d",
                           arrowcolor="#e0e0e0",
                           darkcolor="#3d3d3d",
                           lightcolor="#3d3d3d")
            style.map("Horizontal.TScrollbar",
                     background=[('active', '#4d4d4d'), ('pressed', '#5d5d5d')])
        else:
            # Light/white scrollbar for light mode
            style.configure("Vertical.TScrollbar",
                           background="#f0f0f0",
                           troughcolor="#ffffff",
                           bordercolor="#cccccc",
                           arrowcolor="#333333",
                           darkcolor="#dddddd",
                           lightcolor="#ffffff")
            style.map("Vertical.TScrollbar",
                     background=[('active', '#e0e0e0'), ('pressed', '#d0d0d0')])
            
            style.configure("Horizontal.TScrollbar",
                           background="#f0f0f0",
                           troughcolor="#ffffff",
                           bordercolor="#cccccc",
                           arrowcolor="#333333",
                           darkcolor="#dddddd",
                           lightcolor="#ffffff")
            style.map("Horizontal.TScrollbar",
                     background=[('active', '#e0e0e0'), ('pressed', '#d0d0d0')])
        
    def _apply_theme_to_widget(self, widget, theme):
        """Recursively apply theme to a widget and its children."""
        try:
            # Skip ttk widgets (handled by style)
            if isinstance(widget, (ttk.Progressbar, ttk.Scrollbar, ttk.Button)):
                return
                
            # Apply colors based on widget type
            if isinstance(widget, (tk.Frame, tk.LabelFrame)):
                widget.config(bg=theme["bg"])
                if isinstance(widget, tk.LabelFrame):
                    widget.config(fg=theme["fg"], bg=theme["bg"])
            elif isinstance(widget, tk.Label):
                widget.config(bg=theme["bg"], fg=theme["fg"])
            elif isinstance(widget, tk.Button):
                if widget != self.theme_btn:  # Skip theme button
                    widget.config(
                        bg=theme["button_bg"],
                        fg=theme["button_fg"],
                        activebackground=theme["button_hover"],
                        activeforeground=theme["button_fg"],
                        relief=tk.RAISED,
                        bd=2,
                        highlightthickness=0
                    )
            elif isinstance(widget, tk.Entry):
                widget.config(
                    bg=theme["input_bg"], 
                    fg=theme["input_fg"],
                    insertbackground=theme["fg"],
                    highlightbackground=theme["input_bg"],
                    highlightcolor=theme["button_bg"]
                )
            elif isinstance(widget, tk.Text):
                widget.config(
                    bg=theme["input_bg"],
                    fg=theme["input_fg"],
                    insertbackground=theme["fg"],
                    selectbackground=theme["button_bg"],
                    selectforeground=theme["button_fg"]
                )
            elif isinstance(widget, tk.Scrollbar):
                widget.config(
                    bg=theme["bg"],
                    troughcolor=theme["bg"],
                    activebackground=theme["button_hover"],
                    highlightbackground=theme["bg"],
                    highlightcolor=theme["bg"],
                    highlightthickness=0
                )
                
            # Recursively apply to children
            for child in widget.winfo_children():
                self._apply_theme_to_widget(child, theme)
                
        except tk.TclError:
            pass  # Some widgets might not support all options
            
    def _format_entry(self, _=None):
        """Format number in entry field with commas."""
        value = self.entry.get().replace(',', '')
        cursor_pos = self.entry.index(tk.INSERT)
        
        if value.isdigit():
            formatted = format_number_with_commas(value)
            
            # Calculate cursor adjustment
            orig_commas = self.entry.get()[:cursor_pos].count(',')
            new_commas = formatted[:cursor_pos].count(',')
            
            self.entry.delete(0, tk.END)
            self.entry.insert(0, formatted)
            
            # Restore cursor position
            new_pos = cursor_pos + (new_commas - orig_commas)
            self.entry.icursor(new_pos)
            
    def _set_preset(self, value: int):
        """Set a preset value in the entry field."""
        self.entry.delete(0, tk.END)
        self.entry.insert(0, format_number_with_commas(value))
        
    def _calculate(self):
        """Start prime calculation in a separate thread."""
        # Parse input
        n = parse_number_input(self.entry.get())
        
        if n is None:
            messagebox.showerror("Invalid Input", "Please enter a valid number")
            return
            
        if n < MIN_INPUT:
            messagebox.showerror("Invalid Input", f"Number must be at least {MIN_INPUT}")
            return
            
        if n > MAX_INPUT:
            messagebox.showerror("Input Too Large", 
                               f"Maximum supported value is {format_number_with_commas(MAX_INPUT)}")
            return
            
        # Check memory usage
        mem_usage = estimate_memory_usage(n)
        if mem_usage > 2 * 1024**3:  # 2GB warning
            response = messagebox.askyesno(
                "Large Calculation",
                f"This calculation may use approximately {format_bytes(mem_usage)} of memory. Continue?"
            )
            if not response:
                return
                
        # Disable controls and show progress
        self._set_calculating_state(True)
        
        # Start calculation thread
        self.calculation_thread = threading.Thread(
            target=self._calculation_worker,
            args=(n,),
            daemon=True
        )
        self.calculation_thread.start()
        
    def _calculation_worker(self, n: int):
        """Worker thread for prime calculation."""
        try:
            # Calculate primes with progress callback
            primes = self.calculator.calculate_primes(n, self._update_progress)
            
            # Update GUI in main thread
            self.root.after(0, self._calculation_complete, primes, n)
            
        except Exception as e:
            self.root.after(0, self._calculation_error, str(e))
            
    def _update_progress(self, progress: float):
        """Update progress bar from worker thread."""
        self.progress_var.set(progress * 100)
        self.root.after(0, self.progress_label.config, 
                       {"text": f"Progress: {progress*100:.1f}%"})
        
    def _calculation_complete(self, primes: List[int], n: int):
        """Handle calculation completion."""
        self.current_primes = primes
        self._set_calculating_state(False)
        
        # Update statistics
        theme = get_theme(self.dark_mode)
        self.count_label.config(
            text=f"Found {format_number_with_commas(len(primes))} prime numbers up to {format_number_with_commas(n)}",
            fg=theme["success"]
        )
        
        # Calculate and show statistics
        stats = self.calculator.get_statistics(primes)
        stats_text = f"Time: {format_time(self.calculator.calculation_time)}"
        if stats.get("largest_gap"):
            stats_text += f" | Largest Gap: {stats['largest_gap']}"
        if stats.get("twin_primes"):
            stats_text += f" | Twin Primes: {stats['twin_primes']}"
            
        self.stats_label.config(text=stats_text)
        
        # Display results
        self._display_results(primes)
        
        # Enable export buttons
        for btn in self.export_buttons:
            btn.config(state=tk.NORMAL)
            
    def _calculation_error(self, error: str):
        """Handle calculation error."""
        self._set_calculating_state(False)
        messagebox.showerror("Calculation Error", f"An error occurred: {error}")
        
    def _stop_calculation(self):
        """Stop the current calculation."""
        self.calculator.stop_calculation()
        self._set_calculating_state(False)
        self.stats_label.config(text="Calculation stopped by user")
        
    def _set_calculating_state(self, calculating: bool):
        """Update GUI state during calculation."""
        if calculating:
            self.calc_btn.pack_forget()
            self.stop_btn.pack(side=tk.LEFT, padx=(10, 0))
            self.entry.config(state=tk.DISABLED)
            self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(10, 0))
            self.progress_var.set(0)
            self.progress_label.config(text="Starting calculation...")
        else:
            self.stop_btn.pack_forget()
            self.calc_btn.pack(side=tk.LEFT, padx=(10, 0))
            self.entry.config(state=tk.NORMAL)
            self.progress_bar.pack_forget()
            self.progress_label.config(text="")
            
    def _display_results(self, primes: List[int]):
        """Display prime numbers in the text widget."""
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        
        if not primes:
            self.text.insert(tk.END, "No primes found.")
        else:
            # Store primes for resize handling
            self.current_primes = primes
            
            # Format and display with dynamic columns
            self._format_and_display_primes()
                
        self.text.config(state=tk.DISABLED)
    
    def _format_and_display_primes(self):
        """Format and display primes with dynamic column calculation."""
        if not hasattr(self, 'current_primes') or not self.current_primes:
            return
            
        primes = self.current_primes
        
        # Calculate optimal column width
        max_digits = len(str(primes[-1]))
        # Add 1 space between numbers instead of 2
        col_width = max_digits + 1
        
        # Calculate number of columns based on widget width
        widget_width = self.text.winfo_width()
        if widget_width > 1:  # Widget has been displayed
            # Update to ensure we have current dimensions
            self.text.update_idletasks()
            
            # Get font metrics
            font = tkfont.Font(font=FONTS["monospace"])
            char_width = font.measure("0")
            
            # Get the actual internal text widget width
            # Account for internal padding (padx) and border
            internal_padding = int(str(self.text.cget("padx"))) * 2
            border_width = int(str(self.text.cget("bd"))) * 2
            
            # Calculate usable width more precisely
            usable_width = widget_width - internal_padding - border_width - 2
            cols = max(1, usable_width // (char_width * col_width))
        else:
            cols = 10  # Default
            
        # Clear and redisplay
        self.text.config(state=tk.NORMAL)
        self.text.delete(1.0, tk.END)
        
        # Format and display
        self.text.insert(tk.END, f"Prime Numbers up to {format_number_with_commas(primes[-1])}\n")
        # Make separator match actual display width
        separator_width = cols * col_width - 1
        self.text.insert(tk.END, "=" * separator_width + "\n\n")
        
        for i in range(0, len(primes), cols):
            row = primes[i:i + cols]
            line = " ".join(f"{p:>{max_digits}}" for p in row) + "\n"
            self.text.insert(tk.END, line)
            
        self.text.config(state=tk.DISABLED)
    
    def _setup_resize_handler(self):
        """Set up window resize handling with debouncing."""
        self.resize_after_id = None
        
        def on_resize(event):
            # Only handle resize events for the main window
            if event.widget != self.root:
                return
                
            # Cancel previous resize callback
            if self.resize_after_id:
                self.root.after_cancel(self.resize_after_id)
                
            # Schedule new resize callback with debouncing
            self.resize_after_id = self.root.after(250, self._handle_resize)
        
        # Bind to window configure event
        self.root.bind("<Configure>", on_resize)
        
    def _handle_resize(self):
        """Handle window resize by reformatting prime display."""
        if hasattr(self, 'current_primes') and self.current_primes:
            self._format_and_display_primes()
        
    def _copy_to_clipboard(self):
        """Copy results to clipboard."""
        if not self.current_primes:
            return
            
        success = copy_to_clipboard(self.current_primes, "space")
        if success:
            messagebox.showinfo("Success", "Primes copied to clipboard!")
        else:
            messagebox.showerror("Error", "Failed to copy to clipboard")
            
    def _export(self, format_type: str):
        """Export results to file."""
        if not self.current_primes:
            return
            
        # Get Downloads folder
        downloads_path = Path.home() / "Downloads"
        if not downloads_path.exists():
            downloads_path = Path.home()  # Fallback to home directory
            
        # Create filename: PrimeNumbers in X-Y.ext
        min_prime = self.current_primes[0] if self.current_primes else 2
        max_prime = self.current_primes[-1]
        filename = f"PrimeNumbers in {min_prime}-{max_prime}.{format_type}"
        filepath = downloads_path / filename
        
        # Check if file exists and ask for confirmation
        if filepath.exists():
            response = messagebox.askyesno(
                "File Exists",
                f"File {filename} already exists in Downloads folder.\nDo you want to overwrite it?"
            )
            if not response:
                return
                
        # Export based on format
        success = False
        filepath = Path(filepath)
        
        if format_type == "csv":
            success = export_to_csv(self.current_primes, filepath)
        elif format_type == "txt":
            success = export_to_txt(self.current_primes, filepath)
        elif format_type == "json":
            success = export_to_json(self.current_primes, filepath)
        elif format_type == "html":
            success = export_to_html(self.current_primes, filepath, 
                                   calculation_time=self.calculator.calculation_time)
            
        if success:
            if format_type == "html":
                # For HTML, don't show success dialog since browser opens automatically
                pass
            else:
                messagebox.showinfo("Success", f"Exported to:\n{filepath}")
        else:
            messagebox.showerror("Error", "Failed to export file")


def main():
    """Main entry point for the application."""
    root = tk.Tk()
    PrimeCalculatorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()