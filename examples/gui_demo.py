#!/usr/bin/env python3
"""
GUI Demo Script for GRC Compliance Tool

This script demonstrates how to use the GUI programmatically.
Note: Requires a display to run the actual GUI.

For headless testing, this script will print GUI structure information.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def print_gui_info():
    """Print information about the GUI without launching it"""
    print("=" * 80)
    print("GRC Compliance Tool - GUI Information")
    print("=" * 80)
    print()
    
    print("📊 GUI FEATURES:")
    print("-" * 80)
    print("✅ Modern, Colorful Interface")
    print("   - Professional color scheme (Blue, Purple, Green, Orange, Red)")
    print("   - Clean layout with card-based design")
    print("   - Window size: 1400x900 pixels")
    print()
    
    print("✅ Six Main Tabs:")
    print("   1. Dashboard - Overview and key features")
    print("   2. Start Scan - Configure and launch scans")
    print("   3. Results - View scan results and analysis")
    print("   4. Tool Comparison - Compare with Nessus, OpenVAS, Qualys, Rapid7")
    print("   5. Research Papers - View all 12+ research references")
    print("   6. Settings - Application configuration")
    print()
    
    print("✅ Key Capabilities:")
    print("   - Real-time scan progress monitoring")
    print("   - Visual results display with charts")
    print("   - Integrated tool comparison")
    print("   - Built-in research paper references")
    print("   - Easy configuration without CLI")
    print()
    
    print("=" * 80)
    print("LAUNCHING GUI")
    print("=" * 80)
    print()
    print("To launch the GUI, use one of these methods:")
    print()
    print("1. Command line:")
    print("   $ grc-gui")
    print()
    print("2. Python module:")
    print("   $ python -m grc_tool.gui.launcher")
    print()
    print("3. Python code:")
    print("   from grc_tool.gui.main_window import GRCMainWindow")
    print("   app = GRCMainWindow()")
    print("   app.run()")
    print()
    
    print("=" * 80)
    print("DOCUMENTATION")
    print("=" * 80)
    print()
    print("📖 GUI User Guide: docs/GUI_GUIDE.md")
    print("🖼️ Visual Mockups: docs/GUI_SCREENSHOTS.md")
    print("📊 Tool Comparison: docs/COMPREHENSIVE_COMPARISON.md")
    print("📚 Research Papers: docs/RESEARCH_REFERENCES.md")
    print()

def attempt_gui_launch():
    """Attempt to launch the GUI"""
    try:
        # Try to import tkinter first
        import tkinter as tk
        
        # Check if display is available
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the test window
            root.destroy()
            display_available = True
        except Exception:
            display_available = False
        
        if not display_available:
            print("⚠️  No display available (headless environment)")
            print("   GUI requires a graphical display to run.")
            print("   Please run this on a system with a display or use CLI mode.")
            print()
            return False
        
        # Import and launch GUI
        print("✅ Display available, launching GUI...")
        print()
        
        from grc_tool.gui.main_window import GRCMainWindow
        
        app = GRCMainWindow()
        app.run()
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print()
        print("Please ensure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        print()
        return False
        
    except Exception as e:
        print(f"❌ Error launching GUI: {e}")
        print()
        return False


def main():
    """Main demo function"""
    print()
    print_gui_info()
    
    print("=" * 80)
    print("TESTING GUI LAUNCH")
    print("=" * 80)
    print()
    
    # Check if we should attempt to launch
    if "--no-launch" in sys.argv:
        print("ℹ️  Skipping GUI launch (--no-launch flag provided)")
        print()
    else:
        success = attempt_gui_launch()
        
        if not success:
            print("=" * 80)
            print("ALTERNATIVE: USE CLI MODE")
            print("=" * 80)
            print()
            print("While the GUI provides a user-friendly interface,")
            print("you can use the CLI for full functionality:")
            print()
            print("  $ grc-scan --target 192.168.1.0/24")
            print()
            print("Or use the Python API:")
            print()
            print("  from grc_tool import GRCScanner")
            print("  from grc_tool.utils import Config")
            print()
            print("  config = Config()")
            print("  scanner = GRCScanner(config)")
            print("  results = scanner.scan('192.168.1.100')")
            print()
    
    print("=" * 80)
    print("For more information, see the documentation in docs/")
    print("=" * 80)
    print()


if __name__ == "__main__":
    main()
