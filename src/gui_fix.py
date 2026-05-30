"""
Quick fix to test button text visibility on macOS.
"""

import tkinter as tk
from tkinter import ttk

def test_buttons():
    root = tk.Tk()
    root.title("Button Test")
    
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()
    
    # Test different button styles
    tk.Label(frame, text="Testing button text visibility:").pack(pady=10)
    
    # Standard button
    btn1 = tk.Button(frame, text="Standard Button", relief=tk.RAISED, bd=2)
    btn1.pack(pady=5)
    
    # Button with explicit colors
    btn2 = tk.Button(frame, text="Colored Button", bg="blue", fg="white", relief=tk.RAISED, bd=2)
    btn2.pack(pady=5)
    
    # ttk Button
    btn3 = ttk.Button(frame, text="TTK Button")
    btn3.pack(pady=5)
    
    # Label styled as button
    btn4 = tk.Label(frame, text="Label as Button", bg="lightblue", fg="black", 
                    relief=tk.RAISED, bd=2, padx=10, pady=5, cursor="hand2")
    btn4.pack(pady=5)
    
    root.mainloop()

if __name__ == "__main__":
    test_buttons()