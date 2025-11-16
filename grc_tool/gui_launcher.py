#!/usr/bin/env python3
"""
GUI Launcher for GRC Compliance Tool
Entry point for launching the graphical user interface.
"""

import sys
import logging
from .gui import launch_gui


def main():
    """Main entry point for GUI launcher."""
    # Setup basic logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    try:
        # Launch GUI
        launch_gui()
        return 0
    
    except KeyboardInterrupt:
        print("\nGUI closed by user")
        return 130
    
    except Exception as e:
        print(f"Error launching GUI: {str(e)}")
        logging.exception("GUI launch failed")
        return 1


if __name__ == "__main__":
    sys.exit(main())
