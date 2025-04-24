#!/usr/bin/env python3
"""
Entry point to launch the Mini-Checkers with Obstacles game (human vs AI).
"""

import argparse
import sys
import pygame
from src.checkers.ui.gui import GameGUI

def main():
    parser = argparse.ArgumentParser(
        description="Play Mini-Checkers with Obstacles (6×6 board) against an AI."
    )
    parser.add_argument(
        "--ai-depth",
        type=int,
        default=4,
        help="Search depth (plies) for the AI (default: 4)"
    )
    parser.add_argument(
        "--obstacles",
        type=int,
        default=2,  # reduced initial obstacles
        help="Number of obstacles to place on the board (default: 2)"
    )
    parser.add_argument(
        "--width",
        type=int,
        default=600,
        help="Window width in pixels (default: 600)"
    )
    parser.add_argument(
        "--height",
        type=int,
        default=600,
        help="Window height in pixels (default: 600)"
    )

    args = parser.parse_args()

    # Initialize Pygame and launch the GUI
    try:
        gui = GameGUI(
            width=args.width,
            height=args.height,
            ai_depth=args.ai_depth,
            obstacle_count=args.obstacles
        )
        gui.run()
    except pygame.error as e:
        print("Pygame error:", e, file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
