"""
GRC Tool GUI Main Window
Professional GUI interface for GRC compliance scanning.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
import logging
from datetime import datetime
import json
import os
from typing import Optional

from ..main import GRCScanner
from ..utils import Config
from ..reporting.pdf_exporter import PDFExporter
from ..reporting.report_generator import ReportGenerator

logger = logging.getLogger(__name__)


class GRCToolGUI:
    """
    Main GUI window for GRC Compliance Tool.
    Provides user-friendly interface for scanning and report generation.
    """
    
    def __init__(self, root):
        """
        Initialize GUI window.
        
        Args:
            root: Tkinter root window
        """
        self.root = root
        self.root.title("GRC Compliance Tool - ISO 31000 Risk Assessment")
        self.root.geometry("1000x700")
        
        # Initialize variables
        self.scanner: Optional[GRCScanner] = None
        self.config = Config()
        self.scan_results = None
        self.is_scanning = False
        
        # Setup GUI components
        self._setup_styles()
        self._create_widgets()
        self._setup_logging()
        
        logger.info("GRC Tool GUI initialized")
    
    def _setup_styles(self):
        """Setup custom styles for widgets."""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configure colors
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#2c5aa0')
        style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Success.TLabel', foreground='green', font=('Arial', 10, 'bold'))
        style.configure('Error.TLabel', foreground='red', font=('Arial', 10, 'bold'))
        style.configure('Start.TButton', font=('Arial', 10, 'bold'))
    
    def _create_widgets(self):
        """Create all GUI widgets."""
        # Create main container
        main_container = ttk.Frame(self.root, padding="10")
        main_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(4, weight=1)
        
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
        self.target_var = tk.StringVar(value="127.0.0.1")
        target_entry = ttk.Entry(config_frame, textvariable=self.target_var, width=40)
        target_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(
            config_frame,
            text="(IP address, hostname, or CIDR range, e.g., 192.168.1.0/24)",
            font=('Arial', 8)
        ).grid(row=1, column=1, sticky=tk.W)
        
        # Quick scan checkbox
        self.quick_scan_var = tk.BooleanVar(value=True)
        quick_check = ttk.Checkbutton(
            config_frame,
            text="Quick Scan (Common ports only)",
            variable=self.quick_scan_var
        )
        quick_check.grid(row=2, column=1, sticky=tk.W, pady=5)
        
        # Output directory
        ttk.Label(config_frame, text="Output Directory:").grid(row=3, column=0, sticky=tk.W, padx=(0, 10))
        
        output_frame = ttk.Frame(config_frame)
        output_frame.grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        output_frame.columnconfigure(0, weight=1)
        
        self.output_dir_var = tk.StringVar(value="./reports")
        output_entry = ttk.Entry(output_frame, textvariable=self.output_dir_var)
        output_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=(0, 5))
        
        browse_btn = ttk.Button(output_frame, text="Browse...", command=self._browse_output_dir)
        browse_btn.grid(row=0, column=1)
        
        # Action buttons frame
        action_frame = ttk.Frame(main_container)
        action_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=10)
        
        self.scan_btn = ttk.Button(
            action_frame,
            text="Start Scan",
            command=self._start_scan,
            style='Start.TButton'
        )
        self.scan_btn.grid(row=0, column=0, padx=(0, 5))
        
        self.stop_btn = ttk.Button(
            action_frame,
            text="Stop Scan",
            command=self._stop_scan,
            state=tk.DISABLED
        )
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        self.export_pdf_btn = ttk.Button(
            action_frame,
            text="Export PDF",
            command=self._export_pdf,
            state=tk.DISABLED
        )
        self.export_pdf_btn.grid(row=0, column=2, padx=5)
        
        self.export_json_btn = ttk.Button(
            action_frame,
            text="Export JSON",
            command=self._export_json,
            state=tk.DISABLED
        )
        self.export_json_btn.grid(row=0, column=3, padx=5)
        
        self.export_html_btn = ttk.Button(
            action_frame,
            text="Export HTML",
            command=self._export_html,
            state=tk.DISABLED
        )
        self.export_html_btn.grid(row=0, column=4, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(
            main_container,
            mode='indeterminate',
            length=300
        )
        self.progress.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(main_container, textvariable=self.status_var)
        self.status_label.grid(row=5, column=0, sticky=tk.W)
        
        # Output text area with tabs
        output_notebook = ttk.Notebook(main_container)
        output_notebook.grid(row=6, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        
        # Console tab
        console_frame = ttk.Frame(output_notebook)
        output_notebook.add(console_frame, text="Console Output")
        
        self.console_text = scrolledtext.ScrolledText(
            console_frame,
            wrap=tk.WORD,
            width=100,
            height=20,
            font=('Courier', 9)
        )
        self.console_text.pack(fill=tk.BOTH, expand=True)
        
        # Results tab
        results_frame = ttk.Frame(output_notebook)
        output_notebook.add(results_frame, text="Scan Results")
        
        self.results_text = scrolledtext.ScrolledText(
            results_frame,
            wrap=tk.WORD,
            width=100,
            height=20,
            font=('Courier', 9)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True)
    
    def _setup_logging(self):
        """Setup logging to GUI console."""
        class TextHandler(logging.Handler):
            def __init__(self, text_widget):
                logging.Handler.__init__(self)
                self.text_widget = text_widget
            
            def emit(self, record):
                msg = self.format(record)
                def append():
                    self.text_widget.insert(tk.END, msg + '\n')
                    self.text_widget.see(tk.END)
                self.text_widget.after(0, append)
        
        text_handler = TextHandler(self.console_text)
        text_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logging.getLogger().addHandler(text_handler)
        logging.getLogger().setLevel(logging.INFO)
    
    def _browse_output_dir(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(initialdir=self.output_dir_var.get())
        if directory:
            self.output_dir_var.set(directory)
    
    def _start_scan(self):
        """Start the GRC scan in a separate thread."""
        target = self.target_var.get().strip()
        
        if not target:
            messagebox.showerror("Error", "Please enter a target IP address or network range.")
            return
        
        # Disable scan button, enable stop button
        self.scan_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.export_pdf_btn.config(state=tk.DISABLED)
        self.export_json_btn.config(state=tk.DISABLED)
        self.export_html_btn.config(state=tk.DISABLED)
        
        # Clear previous results
        self.console_text.delete(1.0, tk.END)
        self.results_text.delete(1.0, tk.END)
        self.scan_results = None
        
        # Start progress bar
        self.progress.start()
        self.status_var.set("Scanning in progress...")
        self.is_scanning = True
        
        # Run scan in separate thread
        scan_thread = threading.Thread(target=self._run_scan, args=(target,))
        scan_thread.daemon = True
        scan_thread.start()
    
    def _run_scan(self, target: str):
        """
        Run the actual scan (called in separate thread).
        
        Args:
            target: Target to scan
        """
        try:
            # Update config with user settings
            self.config.set("reporting.output_dir", self.output_dir_var.get())
            
            # Initialize scanner
            self.scanner = GRCScanner(self.config)
            
            # Perform scan
            quick_scan = self.quick_scan_var.get()
            results = self.scanner.scan(target, quick=quick_scan)
            
            if "error" in results:
                self._scan_complete(success=False, error=results['error'])
            else:
                self.scan_results = results
                self._scan_complete(success=True)
                self._display_results(results)
        
        except Exception as e:
            logger.exception("Scan failed")
            self._scan_complete(success=False, error=str(e))
    
    def _scan_complete(self, success: bool, error: str = None):
        """
        Handle scan completion.
        
        Args:
            success: Whether scan was successful
            error: Error message if failed
        """
        def update_gui():
            self.progress.stop()
            self.scan_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.is_scanning = False
            
            if success:
                self.status_var.set("Scan completed successfully!")
                self.export_pdf_btn.config(state=tk.NORMAL)
                self.export_json_btn.config(state=tk.NORMAL)
                self.export_html_btn.config(state=tk.NORMAL)
                messagebox.showinfo("Success", "Scan completed successfully!")
            else:
                self.status_var.set(f"Scan failed: {error}")
                messagebox.showerror("Scan Failed", f"Error: {error}")
        
        self.root.after(0, update_gui)
    
    def _stop_scan(self):
        """Stop the current scan."""
        if self.is_scanning:
            self.is_scanning = False
            self.status_var.set("Scan stopped by user")
            messagebox.showinfo("Stopped", "Scan has been stopped.")
    
    def _display_results(self, results: dict):
        """
        Display scan results in the results tab.
        
        Args:
            results: Scan results dictionary
        """
        def update_results():
            self.results_text.delete(1.0, tk.END)
            
            # Format results
            exec_summary = results.get('risk_assessment', {})
            evaluated_risks = exec_summary.get('evaluated_risks', [])
            
            output = "=" * 80 + "\n"
            output += "GRC COMPLIANCE SCAN RESULTS\n"
            output += "=" * 80 + "\n\n"
            
            # Summary statistics
            output += "SUMMARY:\n"
            output += "-" * 80 + "\n"
            output += f"Hosts Scanned: {len(results.get('scan_results', {}).get('hosts', {}))}\n"
            output += f"Vulnerabilities Found: {len(results.get('vulnerabilities', []))}\n"
            output += f"Risks Identified: {len(evaluated_risks)}\n"
            output += f"Threats Detected: {len(results.get('threats', []))}\n"
            output += f"Anomalies Found: {len(results.get('anomalies', []))}\n"
            output += "\n"
            
            # Risk breakdown
            output += "RISK BREAKDOWN:\n"
            output += "-" * 80 + "\n"
            risk_levels = {}
            for risk in evaluated_risks:
                level = risk.get('risk_level', 'UNKNOWN')
                risk_levels[level] = risk_levels.get(level, 0) + 1
            
            for level in ['EXTREME', 'HIGH', 'MEDIUM', 'LOW']:
                if level in risk_levels:
                    output += f"{level}: {risk_levels[level]}\n"
            
            output += "\n"
            
            # Top risks
            output += "TOP 10 RISKS:\n"
            output += "-" * 80 + "\n"
            
            sorted_risks = sorted(
                evaluated_risks,
                key=lambda r: (r.get('cvss_score', 0), r.get('likelihood', 0)),
                reverse=True
            )[:10]
            
            for i, risk in enumerate(sorted_risks, 1):
                output += f"\n{i}. {risk.get('event', 'Unknown Event')}\n"
                output += f"   Risk Level: {risk.get('risk_level', 'N/A')}\n"
                output += f"   CVSS Score: {risk.get('cvss_score', 'N/A')}\n"
                output += f"   Cause: {risk.get('cause', 'N/A')}\n"
            
            output += "\n" + "=" * 80 + "\n"
            output += "Full report has been generated in the output directory.\n"
            output += "Use Export buttons to save in different formats.\n"
            output += "=" * 80 + "\n"
            
            self.results_text.insert(1.0, output)
        
        self.root.after(0, update_results)
    
    def _export_pdf(self):
        """Export results to PDF."""
        if not self.scan_results:
            messagebox.showwarning("No Results", "No scan results available to export.")
            return
        
        try:
            # Generate report data first
            report_gen = ReportGenerator(self.output_dir_var.get())
            report_data = report_gen.generate_comprehensive_report(self.scan_results)
            
            # Export to PDF
            pdf_exporter = PDFExporter(self.output_dir_var.get())
            pdf_path = pdf_exporter.export_to_pdf(report_data)
            
            messagebox.showinfo("Success", f"PDF report exported successfully!\n\nLocation: {pdf_path}")
            logger.info(f"PDF exported to: {pdf_path}")
        
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export PDF: {str(e)}")
            logger.error(f"PDF export failed: {str(e)}")
    
    def _export_json(self):
        """Export results to JSON."""
        if not self.scan_results:
            messagebox.showwarning("No Results", "No scan results available to export.")
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"grc_scan_{timestamp}.json"
            filepath = os.path.join(self.output_dir_var.get(), filename)
            
            with open(filepath, 'w') as f:
                json.dump(self.scan_results, f, indent=2, default=str)
            
            messagebox.showinfo("Success", f"JSON report exported successfully!\n\nLocation: {filepath}")
            logger.info(f"JSON exported to: {filepath}")
        
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export JSON: {str(e)}")
            logger.error(f"JSON export failed: {str(e)}")
    
    def _export_html(self):
        """Export results to HTML."""
        if not self.scan_results:
            messagebox.showwarning("No Results", "No scan results available to export.")
            return
        
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"grc_report_{timestamp}.html"
            filepath = os.path.join(self.output_dir_var.get(), filename)
            
            # Generate HTML report
            html_content = self._generate_html_report(self.scan_results)
            
            with open(filepath, 'w') as f:
                f.write(html_content)
            
            messagebox.showinfo("Success", f"HTML report exported successfully!\n\nLocation: {filepath}")
            logger.info(f"HTML exported to: {filepath}")
        
        except Exception as e:
            messagebox.showerror("Export Failed", f"Failed to export HTML: {str(e)}")
            logger.error(f"HTML export failed: {str(e)}")
    
    def _generate_html_report(self, results: dict) -> str:
        """
        Generate HTML report from results.
        
        Args:
            results: Scan results
            
        Returns:
            HTML content as string
        """
        risk_assessment = results.get('risk_assessment', {})
        evaluated_risks = risk_assessment.get('evaluated_risks', [])
        
        html = """
<!DOCTYPE html>
<html>
<head>
    <title>GRC Compliance Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        h1 {{ color: #2c5aa0; }}
        h2 {{ color: #333; border-bottom: 2px solid #2c5aa0; padding-bottom: 5px; }}
        table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
        th {{ background-color: #2c5aa0; color: white; padding: 10px; text-align: left; }}
        td {{ border: 1px solid #ddd; padding: 8px; }}
        tr:nth-child(even) {{ background-color: #f2f2f2; }}
        .critical {{ color: red; font-weight: bold; }}
        .high {{ color: orange; font-weight: bold; }}
        .summary {{ background-color: #f9f9f9; padding: 15px; border-left: 4px solid #2c5aa0; margin: 20px 0; }}
    </style>
</head>
<body>
    <h1>GRC Compliance Assessment Report</h1>
    <p><strong>Generated:</strong> {date}</p>
    
    <div class="summary">
        <h2>Executive Summary</h2>
        <p><strong>Hosts Scanned:</strong> {hosts}</p>
        <p><strong>Vulnerabilities Found:</strong> {vulns}</p>
        <p><strong>Risks Identified:</strong> {risks}</p>
        <p><strong>Threats Detected:</strong> {threats}</p>
    </div>
    
    <h2>Risk Distribution</h2>
    <table>
        <tr>
            <th>Risk Level</th>
            <th>Count</th>
        </tr>
        {risk_rows}
    </table>
    
    <h2>Top Risks</h2>
    <table>
        <tr>
            <th>Event</th>
            <th>Risk Level</th>
            <th>CVSS Score</th>
            <th>Cause</th>
        </tr>
        {top_risks}
    </table>
    
    <p><em>Full detailed report available in JSON format.</em></p>
</body>
</html>
        """.format(
            date=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            hosts=len(results.get('scan_results', {}).get('hosts', {})),
            vulns=len(results.get('vulnerabilities', [])),
            risks=len(evaluated_risks),
            threats=len(results.get('threats', [])),
            risk_rows=self._generate_risk_rows(evaluated_risks),
            top_risks=self._generate_top_risks_html(evaluated_risks)
        )
        
        return html
    
    def _generate_risk_rows(self, evaluated_risks: list) -> str:
        """Generate HTML table rows for risk distribution."""
        risk_levels = {}
        for risk in evaluated_risks:
            level = risk.get('risk_level', 'UNKNOWN')
            risk_levels[level] = risk_levels.get(level, 0) + 1
        
        rows = ""
        for level in ['EXTREME', 'HIGH', 'MEDIUM', 'LOW']:
            if level in risk_levels:
                css_class = 'critical' if level == 'EXTREME' else ('high' if level == 'HIGH' else '')
                rows += f'<tr><td class="{css_class}">{level}</td><td>{risk_levels[level]}</td></tr>\n'
        
        return rows
    
    def _generate_top_risks_html(self, evaluated_risks: list) -> str:
        """Generate HTML table rows for top risks."""
        sorted_risks = sorted(
            evaluated_risks,
            key=lambda r: (r.get('cvss_score', 0), r.get('likelihood', 0)),
            reverse=True
        )[:10]
        
        rows = ""
        for risk in sorted_risks:
            level = risk.get('risk_level', 'N/A')
            css_class = 'critical' if level == 'EXTREME' else ('high' if level == 'HIGH' else '')
            rows += f"""
            <tr>
                <td>{risk.get('event', 'Unknown Event')}</td>
                <td class="{css_class}">{level}</td>
                <td>{risk.get('cvss_score', 'N/A')}</td>
                <td>{risk.get('cause', 'N/A')}</td>
            </tr>
            """
        
        return rows


def launch_gui():
    """Launch the GUI application."""
    root = tk.Tk()
    app = GRCToolGUI(root)
    root.mainloop()


if __name__ == "__main__":
    launch_gui()
