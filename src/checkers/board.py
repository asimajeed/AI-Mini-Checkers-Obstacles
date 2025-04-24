import numpy as np

class Board:
    """
    Represents a 6×6 mini‑checkers board with dynamic obstacles.
    Uses an integer grid:
      0  = empty
      1  = Player 1 man
      2  = Player 1 king
     -1  = Player 2 man
     -2  = Player 2 king
    Obstacles are stored in a separate set of (row, col) tuples.
    """

    def __init__(self, obstacle_count=2):
        self.rows = 6
        self.cols = 6
        self.grid = np.zeros((self.rows, self.cols), dtype=int)
        self.obstacles = set()

        self.initial_obstacle_count = obstacle_count
        self.initial_piece_count = 12  # 6 per side
