#!/usr/bin/env python3
"""
GUI Launcher for GRC Compliance Tool
"""

import sys
import os

def main():
    """Launch the GRC GUI application"""
    try:
        from grc_tool.gui.main_window import GRCMainWindow
        
        print("Starting GRC Compliance Tool GUI...")
        print("ISO 31000:2018 Risk Management with Advanced ML")
        print("=" * 60)
        
        app = GRCMainWindow()
        app.run()
        
    except ImportError as e:
        print(f"Error: Failed to import required modules: {e}")
        print("\nPlease ensure all dependencies are installed:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
