"""
Utility functions for the Prime Number Calculator.

This module provides helper functions for exporting data, formatting numbers,
and other utility operations.
"""

import json
import csv
import math
import webbrowser
from typing import List, Optional, Union
from pathlib import Path
import pyperclip
from datetime import datetime


def format_number_with_commas(n: Union[int, str]) -> str:
    """
    Format a number with thousands separators.
    
    Args:
        n: Number to format (int or string)
        
    Returns:
        Formatted string with commas
    """
    if isinstance(n, str):
        n = n.replace(",", "")
        if n.isdigit():
            n = int(n)
        else:
            return n
    return f"{n:,}"


def parse_number_input(input_str: str) -> Optional[int]:
    """
    Parse user input into an integer, handling various formats.
    
    Args:
        input_str: User input string
        
    Returns:
        Parsed integer or None if invalid
        
    Supports:
        - Comma-separated numbers: "1,000,000"
        - Scientific notation: "1e6", "1E6"
        - Regular integers: "1000000"
    """
    input_str = input_str.strip()
    
    # Handle empty input
    if not input_str:
        return None
    
    # Remove commas
    input_str = input_str.replace(",", "")
    
    # Handle scientific notation
    if "e" in input_str.lower():
        try:
            return int(float(input_str))
        except ValueError:
            return None
    
    # Handle regular integer
    try:
        return int(input_str)
    except ValueError:
        return None


def export_to_csv(primes: List[int], filepath: Path) -> bool:
    """
    Export prime numbers to a CSV file.
    
    Args:
        primes: List of prime numbers
        filepath: Path to save the CSV file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Index", "Prime"])
            for i, prime in enumerate(primes, 1):
                writer.writerow([i, prime])
        return True
    except Exception:
        return False


def export_to_txt(primes: List[int], filepath: Path, columns: int = 10) -> bool:
    """
    Export prime numbers to a text file.
    
    Args:
        primes: List of prime numbers
        filepath: Path to save the text file
        columns: Number of columns per row
        
    Returns:
        True if successful, False otherwise
    """
    try:
        with open(filepath, 'w') as f:
            f.write(f"Prime Numbers (Total: {len(primes)})\n")
            f.write("=" * 50 + "\n\n")
            
            for i in range(0, len(primes), columns):
                row = primes[i:i + columns]
                f.write(" ".join(f"{p:>7}" for p in row) + "\n")
                
        return True
    except Exception:
        return False


def export_to_json(primes: List[int], filepath: Path, include_stats: bool = True) -> bool:
    """
    Export prime numbers to a JSON file.
    
    Args:
        primes: List of prime numbers
        filepath: Path to save the JSON file
        include_stats: Whether to include statistics
        
    Returns:
        True if successful, False otherwise
    """
    try:
        data = {
            "count": len(primes),
            "primes": primes
        }
        
        if include_stats and primes:
            data["statistics"] = {
                "smallest": primes[0],
                "largest": primes[-1],
                "density": len(primes) / primes[-1] if primes[-1] > 0 else 0
            }
            
            if len(primes) > 1:
                gaps = [primes[i+1] - primes[i] for i in range(len(primes)-1)]
                data["statistics"]["largest_gap"] = max(gaps)
                data["statistics"]["average_gap"] = sum(gaps) / len(gaps)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
            
        return True
    except Exception:
        return False


def copy_to_clipboard(primes: List[int], format_type: str = "space") -> bool:
    """
    Copy prime numbers to clipboard.
    
    Args:
        primes: List of prime numbers
        format_type: How to format ("space", "comma", "newline")
        
    Returns:
        True if successful, False otherwise
    """
    try:
        if format_type == "comma":
            text = ", ".join(str(p) for p in primes)
        elif format_type == "newline":
            text = "\n".join(str(p) for p in primes)
        else:  # space
            text = " ".join(str(p) for p in primes)
            
        pyperclip.copy(text)
        return True
    except Exception:
        return False


def estimate_memory_usage(n: int) -> int:
    """
    Estimate memory usage for calculating primes up to n.
    
    Args:
        n: Upper limit for prime calculation
        
    Returns:
        Estimated memory usage in bytes
    """
    # Boolean array for sieve
    sieve_memory = n + 1
    
    # Approximate number of primes (prime number theorem)
    if n > 10:
        approx_primes = int(n / (math.log(n) - 1))
    else:
        approx_primes = n // 2
    
    # Memory for storing primes (assuming 8 bytes per integer)
    primes_memory = approx_primes * 8
    
    return sieve_memory + primes_memory


def format_time(seconds: float) -> str:
    """
    Format time in seconds to a human-readable string.
    
    Args:
        seconds: Time in seconds
        
    Returns:
        Formatted time string
    """
    if seconds < 0.001:
        return f"{seconds * 1000000:.0f} μs"
    elif seconds < 1:
        return f"{seconds * 1000:.1f} ms"
    elif seconds < 60:
        return f"{seconds:.2f} s"
    else:
        minutes = int(seconds // 60)
        secs = seconds % 60
        return f"{minutes}m {secs:.1f}s"


def format_bytes(bytes_val: int) -> str:
    """
    Format bytes to human-readable string.
    
    Args:
        bytes_val: Number of bytes
        
    Returns:
        Formatted string (KB, MB, GB)
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} TB"


def export_to_html(primes: List[int], filepath: Path, include_stats: bool = True, calculation_time: float = None, open_browser: bool = True) -> bool:
    """
    Export prime numbers to a responsive HTML file.
    
    Args:
        primes: List of prime numbers
        filepath: Path to save the HTML file
        include_stats: Whether to include statistics
        calculation_time: Time taken to calculate primes (in seconds)
        open_browser: Whether to open the file in the default browser
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Calculate statistics
        stats = {}
        if include_stats and primes:
            stats = {
                "count": len(primes),
                "smallest": primes[0],
                "largest": primes[-1],
                "density": len(primes) / primes[-1] if primes[-1] > 0 else 0
            }
            
            if len(primes) > 1:
                gaps = [primes[i+1] - primes[i] for i in range(len(primes)-1)]
                stats["largest_gap"] = max(gaps)
                stats["average_gap"] = sum(gaps) / len(gaps)
                stats["twin_primes"] = sum(1 for i in range(len(primes)-1) if primes[i+1] - primes[i] == 2)
        
        # Create HTML content
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Prime Numbers up to {format_number_with_commas(primes[-1]) if primes else 0}</title>
    <style>
        :root {{
            --primary-color: #007ACC;
            --bg-color: #f0f2f5;
            --text-color: #202124;
            --card-bg: #ffffff;
            --border-color: #e0e0e0;
            --success-color: #28A745;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(to bottom, #1e90ff, #ffffff);
            min-height: 100vh;
            padding: 20px;
            color: var(--text-color);
        }}
        
        .container {{
            width: 90%;
            max-width: 3600px;
            margin: 0 auto;
            background: var(--card-bg);
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 30px;
        }}
        
        h1 {{
            color: var(--primary-color);
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5em;
        }}
        
        .stats {{
            background: var(--bg-color);
            padding: 20px;
            border-radius: 8px;
            margin-bottom: 30px;
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
        }}
        
        .stat-item {{
            text-align: center;
            padding: 15px;
            background: var(--card-bg);
            border-radius: 5px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .stat-label {{
            font-size: 0.9em;
            color: #666;
            margin-bottom: 5px;
        }}
        
        .stat-value {{
            font-size: 1.5em;
            font-weight: bold;
            color: var(--primary-color);
        }}
        
        .primes-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(90px, 1fr));
            gap: 12px;
            margin-top: 20px;
            max-height: 75vh;
            overflow-y: auto;
            padding: 25px;
            background: var(--bg-color);
            border-radius: 8px;
        }}
        
        .prime {{
            background: var(--card-bg);
            padding: 10px;
            text-align: center;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            transition: all 0.2s ease;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }}
        
        .prime:hover {{
            background: var(--primary-color);
            color: white;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }}
        
        .footer {{
            text-align: center;
            margin-top: 30px;
            color: #666;
            font-size: 0.9em;
        }}
        
        @media (max-width: 768px) {{
            .container {{
                padding: 20px;
            }}
            
            h1 {{
                font-size: 1.8em;
            }}
            
            .primes-grid {{
                grid-template-columns: repeat(auto-fill, minmax(60px, 1fr));
                gap: 8px;
                padding: 15px;
            }}
            
            .stats {{
                grid-template-columns: 1fr;
            }}
        }}
        
        /* Dark mode support */
        @media (prefers-color-scheme: dark) {{
            :root {{
                --bg-color: #1e1e1e;
                --text-color: #e0e0e0;
                --card-bg: #2d2d2d;
                --border-color: #444;
            }}
            
            body {{
                background: linear-gradient(to bottom, #0f1419, #1e2832);
            }}
        }}
        
        /* Print styles */
        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            
            .container {{
                box-shadow: none;
                padding: 20px;
            }}
            
            .primes-grid {{
                max-height: none;
                background: white;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Prime Numbers</h1>
        """
        
        # Add statistics if included
        if include_stats and stats:
            html_content += """
        <div class="stats">
            <div class="stat-item">
                <div class="stat-label">Total Count</div>
                <div class="stat-value">{:,}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Range</div>
                <div class="stat-value">{:,} - {:,}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Density</div>
                <div class="stat-value">{:.2%}</div>
            </div>
            """.format(
                stats['count'],
                stats['smallest'], stats['largest'],
                stats['density']
            )
            
            if 'largest_gap' in stats:
                html_content += """
            <div class="stat-item">
                <div class="stat-label">Largest Gap</div>
                <div class="stat-value">{:,}</div>
            </div>
            <div class="stat-item">
                <div class="stat-label">Average Gap</div>
                <div class="stat-value">{:.1f}</div>
            </div>
                """.format(stats['largest_gap'], stats['average_gap'])
                
            if 'twin_primes' in stats:
                html_content += """
            <div class="stat-item">
                <div class="stat-label">Twin Primes</div>
                <div class="stat-value">{:,}</div>
            </div>
                """.format(stats['twin_primes'])
            
            if calculation_time is not None:
                html_content += """
            <div class="stat-item">
                <div class="stat-label">Calculation Time</div>
                <div class="stat-value">{}</div>
            </div>
                """.format(format_time(calculation_time))
                
            html_content += """
        </div>
            """
        
        # Add prime numbers grid
        html_content += """
        <div class="primes-grid">
        """
        
        for prime in primes:
            html_content += f'            <div class="prime">{format_number_with_commas(prime)}</div>\n'
            
        html_content += """
        </div>
        
        <div class="footer">
            Generated on {} by Prime Number Calculator v2.0<br>
            Using the Sieve of Eratosthenes algorithm
        </div>
    </div>
    
    <script>
        // Add some interactivity
        document.addEventListener('DOMContentLoaded', function() {{
            const primes = document.querySelectorAll('.prime');
            let selectedPrimes = new Set();
            
            primes.forEach(prime => {{
                prime.addEventListener('click', function() {{
                    const value = this.textContent.replace(/,/g, '');
                    if (selectedPrimes.has(value)) {{
                        selectedPrimes.delete(value);
                        this.style.background = '';
                        this.style.color = '';
                    }} else {{
                        selectedPrimes.add(value);
                        this.style.background = '#28A745';
                        this.style.color = 'white';
                    }}
                    
                    // Update page title with selection count
                    if (selectedPrimes.size > 0) {{
                        document.title = `Selected: ${{selectedPrimes.size}} primes`;
                    }} else {{
                        document.title = 'Prime Numbers up to {}';
                }});
            }});
        }});
    </script>
</body>
</html>
        """.format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            format_number_with_commas(primes[-1]) if primes else 0
        )
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        # Open in browser if requested
        if open_browser:
            webbrowser.open(f'file://{filepath.absolute()}')
            
        return True
    except Exception as e:
        print(f"Error exporting HTML: {e}")
        return False