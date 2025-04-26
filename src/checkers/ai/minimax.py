import copy
from typing import Union, Tuple, Dict, List
from ..board import Board
from ..move_generator import MoveGenerator
from .heuristic import evaluate

# AI is Player 2 (encoded as -1 in the grid)
AI_PLAYER = -1

MoveSimple = Tuple[Tuple[int,int], Tuple[int,int]]
MoveCapture = Dict[str, List[Tuple[int,int]]]  # {'path': [...], 'captures': [...]}
MoveType = Union[MoveSimple, MoveCapture]

def minimax(board: Board, depth: int, alpha: float, beta: float, player: int) -> float:
    """
    Minimax search with alpha-beta pruning.
    Returns the heuristic score from the point of view of `player`.
    """
    mg = MoveGenerator(board)
    # If any captures exist, they are mandatory
    capture_seqs = mg.get_capture_moves(player)
    moves: List[MoveType] = capture_seqs if capture_seqs else mg.get_legal_moves(player)

    # Terminal condition: no moves or max depth reached
    if depth == 0 or not moves:
        return evaluate(board, player)

    if player == AI_PLAYER:
        value = float('-inf')
        for move in moves:
            new_board = copy.deepcopy(board)
            _apply_move(new_board, move, player)
            score = minimax(new_board, depth - 1, alpha, beta, -player)
            value = max(value, score)
            alpha = max(alpha, score)
            if alpha >= beta:
                break  # β cutoff
        return value
    else:
        value = float('inf')
        for move in moves:
            new_board = copy.deepcopy(board)
            _apply_move(new_board, move, player)
            score = minimax(new_board, depth - 1, alpha, beta, -player)
            value = min(value, score)
            beta = min(beta, score)
            if beta <= alpha:
                break  # α cutoff
        return value

def _apply_move(board: Board, move: MoveType, player: int):
    """
    Mutates `board` by applying either a simple move or a capture sequence.
    """
    if isinstance(move, dict):
        # Multi‑jump capture
        path = move['path']
        caps = move['captures']
        for i in range(1, len(path)):
            start = path[i-1]
            end = path[i]
            board.move_piece(start, end)
            board.remove_piece(*caps[i-1])
    else:
        # Simple diagonal move
        start, end = move
        board.move_piece(start, end)

def choose_move(board: Board, depth: int) -> MoveType:
    """
    Select the best move for the AI (Player 2, code = -1) at given search depth.
    Returns either a (start,end) tuple or a {'path':…, 'captures':…} dict.
    """
    player = AI_PLAYER
    mg = MoveGenerator(board)
    capture_seqs = mg.get_capture_moves(player)
    moves = capture_seqs if capture_seqs else mg.get_legal_moves(player)

    best_move = None
    best_score = float('-inf')
    for move in moves:
        new_board = copy.deepcopy(board)
        _apply_move(new_board, move, player)
        score = minimax(new_board, depth - 1, float('-inf'), float('inf'), -player)
        if score > best_score:
            best_score = score
            best_move = move

    return best_move
