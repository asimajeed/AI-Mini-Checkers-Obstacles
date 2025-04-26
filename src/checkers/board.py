import numpy as np
import random

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

        # Track for dynamic obstacle scaling
        self.initial_obstacle_count = obstacle_count
        self.initial_piece_count = 12  # 6 per side

        self._place_initial_pieces()
        self._place_obstacles(self.initial_obstacle_count)

    def _is_dark_square(self, r, c):
        return (0 <= r < self.rows and 0 <= c < self.cols
                and (r + c) % 2 == 1)

    def _place_initial_pieces(self):
        # Player 2 on top two rows
        for r in (0, 1):
            for c in range(self.cols):
                if self._is_dark_square(r, c):
                    self.grid[r, c] = -1
        # Player 1 on bottom two rows
        for r in (4, 5):
            for c in range(self.cols):
                if self._is_dark_square(r, c):
                    self.grid[r, c] = 1

    def _place_obstacles(self, count):
        # Randomly choose 'count' empty dark squares
        empties = [
            (r, c)
            for r in range(self.rows)
            for c in range(self.cols)
            if self._is_dark_square(r, c)
               and self.grid[r, c] == 0
        ]
        count = min(count, len(empties))
        self.obstacles = set(random.sample(empties, count))

    def update_obstacles(self):
        """
        Re‑randomize obstacle positions based on:
          new_count = initial_obstacles + floor((pieces_removed)/2)
        """
        # count current pieces (men + kings)
        current_pieces = np.count_nonzero(self.grid)
        removed = self.initial_piece_count - current_pieces
        # add one obstacle for every two pieces removed
        new_count = self.initial_obstacle_count + (removed // 2)
        self._place_obstacles(new_count)

    def is_within_bounds(self, r, c):
        return 0 <= r < self.rows and 0 <= c < self.cols

    def is_obstacle(self, r, c):
        return (r, c) in self.obstacles

    def is_empty(self, r, c):
        return (self.is_within_bounds(r, c)
                and not self.is_obstacle(r, c)
                and self.grid[r, c] == 0
                and self._is_dark_square(r, c))

    def get_piece(self, r, c):
        """Return integer code of piece at (r,c), or None if invalid/obstacle."""
        if not self.is_within_bounds(r, c) or self.is_obstacle(r, c):
            return None
        return int(self.grid[r, c])

    def move_piece(self, start, end):
        """
        Move a piece (with optional promotion).
        `start` and `end` are (r,c) tuples.
        """
        r0, c0 = start
        r1, c1 = end
        piece = self.grid[r0, c0]
        self.grid[r0, c0] = 0
        self.grid[r1, c1] = piece
        # Promotion
        if piece == 1 and r1 == 0:
            self.grid[r1, c1] = 2
        elif piece == -1 and r1 == self.rows - 1:
            self.grid[r1, c1] = -2

    def remove_piece(self, r, c):
        """Clear a piece at (r,c)."""
        if self.is_within_bounds(r, c) and not self.is_obstacle(r, c):
            self.grid[r, c] = 0
