#!/usr/bin/env python3
"""
Demo script to show GUI layout without requiring full dependencies.
This creates a simplified version for testing GUI elements.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import json
from datetime import datetime

def demo_gui():
    """Create a demo GUI window showing the interface."""
    root = tk.Tk()
    root.title("GRC Compliance Tool - GUI Demo")
    root.geometry("1000x700")
    
    # Setup styles
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c5aa0')
    style.configure('Start.TButton', font=('Arial', 10, 'bold'))
    
    # Create main container
    main_container = ttk.Frame(root, padding="10")
    main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    # Configure grid weights
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    main_container.columnconfigure(0, weight=1)
    
    # Title
    title_label = ttk.Label(
        main_container,
        text="GRC Compliance Tool",
        style='Title.TLabel'
    )
    title_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
    
    subtitle = ttk.Label(
        main_container,
        text="ISO 31000:2018 Risk Assessment with ML-based Threat Detection"
    )
    subtitle.grid(row=1, column=0, pady=(0, 20), sticky=tk.W)
    
    # Scan configuration frame
    config_frame = ttk.LabelFrame(main_container, text="Scan Configuration", padding="10")
    config_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
    config_frame.columnconfigure(1, weight=1)
    
    # Target input
    ttk.Label(config_frame, text="Target:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
    target_var = tk.StringVar(value="127.0.0.1")
    target_entry = ttk.Entry(config_frame, textvariable=target_var, width=40)
    target_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
    
    ttk.Label(
        config_frame,
        text="(IP address, hostname, or CIDR range, e.g., 192.168.1.0/24)",
        font=('Arial', 8)
    ).grid(row=1, column=1, sticky=tk.W)
    
    # Quick scan checkbox
    quick_scan_var = tk.BooleanVar(value=True)
    quick_check = ttk.Checkbutton(
        config_frame,
        text="Quick Scan (Common ports only)",
        variable=quick_scan_var
    )
    quick_check.grid(row=2, column=1, sticky=tk.W, pady=5)
    
    # Output directory
    ttk.Label(config_frame, text="Output Directory:").grid(row=3, column=0, sticky=tk.W, padx=(0, 10))
    
    output_frame = ttk.Frame(config_frame)
    output_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
    output_frame.columnconfigure(0, weight=1)
    
    output_dir_var = tk.StringVar(value="./reports")
    output_entry = ttk.Entry(output_frame, textvariable=output_dir_var)
    output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
    
    browse_btn = ttk.Button(output_frame, text="Browse...")
    browse_btn.grid(row=0, column=1)
    
    # Action buttons frame
    action_frame = ttk.Frame(main_container)
    action_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)
    
    def show_demo_message():
        messagebox.showinfo(
            "Demo Mode",
            "This is a demo of the GUI interface.\n\n"
            "In the full version:\n"
            "• Click 'Start Scan' to begin scanning\n"
            "• Monitor progress in real-time\n"
            "• View results in the tabs below\n"
            "• Export to PDF, JSON, or HTML formats"
        )
    
    scan_btn = ttk.Button(
        action_frame,
        text="Start Scan",
        command=show_demo_message,
        style='Start.TButton'
    )
    scan_btn.grid(row=0, column=0, padx=(0, 5))
    
    stop_btn = ttk.Button(action_frame, text="Stop Scan", state=tk.DISABLED)
    stop_btn.grid(row=0, column=1, padx=5)
    
    export_pdf_btn = ttk.Button(action_frame, text="Export PDF", state=tk.DISABLED)
    export_pdf_btn.grid(row=0, column=2, padx=5)
    
    export_json_btn = ttk.Button(action_frame, text="Export JSON", state=tk.DISABLED)
    export_json_btn.grid(row=0, column=3, padx=5)
    
    export_html_btn = ttk.Button(action_frame, text="Export HTML", state=tk.DISABLED)
    export_html_btn.grid(row=0, column=4, padx=5)
    
    # Progress bar
    progress = ttk.Progressbar(main_container, mode='determinate', length=300, value=0)
    progress.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=5)
    
    # Status label
    status_var = tk.StringVar(value="Ready - Demo Mode")
    status_label = ttk.Label(main_container, textvariable=status_var)
    status_label.grid(row=5, column=0, sticky=tk.W)
    
    # Output text area with tabs
    output_notebook = ttk.Notebook(main_container)
    output_notebook.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
    
    # Console tab
    console_frame = ttk.Frame(output_notebook)
    output_notebook.add(console_frame, text="Console Output")
    
    console_text = scrolledtext.ScrolledText(
        console_frame,
        wrap=tk.WORD,
        width=100,
        height=20,
        font=('Courier', 9)
    )
    console_text.pack(fill=tk.BOTH, expand=True)
    console_text.insert(1.0, "GRC Compliance Tool - Demo Mode\n")
    console_text.insert(tk.END, "=" * 80 + "\n\n")
    console_text.insert(tk.END, "This is a demonstration of the GUI interface.\n\n")
    console_text.insert(tk.END, "Features:\n")
    console_text.insert(tk.END, "• Easy target configuration\n")
    console_text.insert(tk.END, "• Quick and full scan modes\n")
    console_text.insert(tk.END, "• Real-time progress monitoring\n")
    console_text.insert(tk.END, "• Multiple export formats (PDF, JSON, HTML)\n")
    console_text.insert(tk.END, "• Professional reporting\n\n")
    console_text.insert(tk.END, "To use the full version, install dependencies and run:\n")
    console_text.insert(tk.END, "  pip install -r requirements.txt\n")
    console_text.insert(tk.END, "  grc-gui\n")
    
    # Results tab
    results_frame = ttk.Frame(output_notebook)
    output_notebook.add(results_frame, text="Scan Results")
    
    results_text = scrolledtext.ScrolledText(
        results_frame,
        wrap=tk.WORD,
        width=100,
        height=20,
        font=('Courier', 9)
    )
    results_text.pack(fill=tk.BOTH, expand=True)
    results_text.insert(1.0, "Scan results will appear here after scanning completes.\n\n")
    results_text.insert(tk.END, "Results include:\n")
    results_text.insert(tk.END, "• Host discovery summary\n")
    results_text.insert(tk.END, "• Vulnerability assessment\n")
    results_text.insert(tk.END, "• Risk analysis and ratings\n")
    results_text.insert(tk.END, "• ML-based threat detection\n")
    results_text.insert(tk.END, "• Compliance status\n")
    results_text.insert(tk.END, "• Mitigation recommendations\n")
    
    # Make window resizable
    main_container.rowconfigure(6, weight=1)
    
    # Show info message on startup
    root.after(500, show_demo_message)
    
    root.mainloop()


if __name__ == "__main__":
    print("Starting GRC Tool GUI Demo...")
    demo_gui()
