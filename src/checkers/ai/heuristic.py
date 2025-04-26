from ..board import Board
from ..move_generator import MoveGenerator

def evaluate(board: Board, player: int) -> float:
    """
    Heuristic combining:
      1. Material balance (+1 per man, +2 per king)
      2. Mobility (legal moves + 2×capture sequences)
      3. Obstacle proximity (fewer obstacles en route to promotion)
    Returns a score positive if favorable for `player`.
    """
    # 1) Material
    p1_men   = ((board.grid ==  1).sum())
    p1_kings = ((board.grid ==  2).sum())
    p2_men   = ((board.grid == -1).sum())
    p2_kings = ((board.grid == -2).sum())
    mat1 = p1_men + 2 * p1_kings
    mat2 = p2_men + 2 * p2_kings
    mat_diff = (mat1 - mat2) * player

    # 2) Mobility
    mg = MoveGenerator(board)
    p1_caps = len(mg.get_capture_moves(1))
    p2_caps = len(mg.get_capture_moves(-1))
    p1_moves = len(mg.get_legal_moves(1))
    p2_moves = len(mg.get_legal_moves(-1))
    mob1 = p1_moves + 2 * p1_caps
    mob2 = p2_moves + 2 * p2_caps
    mob_diff = (mob1 - mob2) * player

    # 3) Obstacle Proximity
    # For each man, count obstacles along its two promotion diagonals
    def obstacle_path_count(r, c, dr, dc):
        count = 0
        nr, nc = r + dr, c + dc
        while 0 <= nr < board.rows and 0 <= nc < board.cols:
            if board.is_obstacle(nr, nc):
                count += 1
            nr += dr
            nc += dc
        return count

    prox1 = 0
    prox2 = 0
    for r in range(board.rows):
        for c in range(board.cols):
            code = board.get_piece(r, c)
            if code == 1:   # P1 man
                # P1 moves up: directions (-1,-1) and (-1,+1)
                prox1 += obstacle_path_count(r, c, -1, -1)
                prox1 += obstacle_path_count(r, c, -1, +1)
            elif code == -1:  # P2 man
                # P2 moves down: (+1,-1) and (+1,+1)
                prox2 += obstacle_path_count(r, c, +1, -1)
                prox2 += obstacle_path_count(r, c, +1, +1)
    prox_diff = (prox2 - prox1) * player  # more obstacles for opponent is good

    # Weights
    W_MAT = 10.0
    W_MOB = 1.0
    W_PROX = 1.0

    return W_MAT * mat_diff + W_MOB * mob_diff + W_PROX * prox_diff
