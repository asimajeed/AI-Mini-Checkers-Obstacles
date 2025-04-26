from .board import Board

class MoveGenerator:
    """
    Generates legal simple moves and mandatory capture sequences,
    taking obstacles into account.
    """

    def __init__(self, board: Board):
        self.board = board

    def get_legal_moves(self, player: int):
        """
        Return a list of (start, end) moves for `player` where:
          start = (r0, c0), end = (r1, c1)
        Simple diagonal moves only.
        """
        moves = []
        # Men move “forward” only; kings both ways
        man_dirs = [(-1, -1), (-1, +1)] if player == 1 else [(+1, -1), (+1, +1)]
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                code = self.board.get_piece(r, c)
                if code is None or code * player <= 0:
                    continue
                is_king = abs(code) == 2
                dirs = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)] if is_king else man_dirs
                for dr, dc in dirs:
                    nr, nc = r + dr, c + dc
                    if self.board.is_empty(nr, nc):
                        moves.append(((r, c), (nr, nc)))
        return moves

    def get_capture_moves(self, player: int):
        """
        Return a list of capture sequences. Each sequence is a dict:
          {
            'path':     [ (r0,c0), (r1,c1), ..., (rk,ck) ],
            'captures': [ (cr1,cc1), ..., (crm,ccm) ]
          }
        Multi-jumps are explored via DFS.
        """
        all_seqs = []
        # All diagonal directions
        dirs = [(-1, -1), (-1, +1), (+1, -1), (+1, +1)]

        def _dfs(path, caps, visited, r, c, is_king):
            found_jump = False
            for dr, dc in dirs:
                # Men only forward
                if not is_king:
                    if player == 1 and dr > 0:  # P1 moves up (dr must be –1)
                        continue
                    if player == 2 and dr < 0:  # P2 moves down (dr must be +1)
                        continue

                mid_r, mid_c = r + dr, c + dc
                land_r, land_c = r + 2*dr, c + 2*dc

                # Bounds + obstacle checks
                if not (self.board.is_within_bounds(mid_r, mid_c)
                        and self.board.is_within_bounds(land_r, land_c)):
                    continue
                if self.board.is_obstacle(mid_r, mid_c) or self.board.is_obstacle(land_r, land_c):
                    continue

                mid_code = self.board.grid[mid_r, mid_c]
                if mid_code * player < 0 and self.board.is_empty(land_r, land_c):
                    key = (mid_r, mid_c, land_r, land_c)
                    if key in visited:
                        continue
                    found_jump = True
                    new_visited = visited | {key}
                    _dfs(path + [(land_r, land_c)],
                         caps + [(mid_r, mid_c)],
                         new_visited,
                         land_r, land_c,
                         is_king)

            # If no further jumps, and we’ve captured at least once, record it
            if not found_jump and caps:
                all_seqs.append({'path': path, 'captures': caps})

        # Kick off DFS from every piece of `player`
        for r in range(self.board.rows):
            for c in range(self.board.cols):
                code = self.board.get_piece(r, c)
                if code is None or code * player <= 0:
                    continue
                _dfs(path=[(r, c)],
                     caps=[],
                     visited=set(),
                     r=r, c=c,
                     is_king=(abs(code) == 2))

        return all_seqs
