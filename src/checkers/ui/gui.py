import sys
import copy
import pygame
from ..board import Board
from ..move_generator import MoveGenerator
from ..ai.minimax import choose_move

class GameGUI:
    """
    Pygame GUI for Mini‑Checkers with Obstacles.
    Human is Player 1 (grid>0), AI is Player 2 (grid<0).
    """

    def __init__(self, width=600, height=600, ai_depth=4, obstacle_count=2):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Mini‑Checkers with Obstacles")
        self.clock = pygame.time.Clock()

        # Game state
        self.board = Board(obstacle_count=obstacle_count)
        self.move_gen = MoveGenerator(self.board)
        self.turn = 1               # 1 = human; -1 = AI
        self.selected = None        # (r,c) of selected piece
        self.legal_moves = []       # list of moves for selected piece
        self.ai_depth = ai_depth

        # Renderer
        from .renderer import BoardRenderer
        self.renderer = BoardRenderer(self.screen, self.board)

    def run(self):
        running = True
        while running:
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.turn == 1:
                    self._handle_human_click(event.pos)

            # AI turn
            if self.turn == -1 and running:
                pygame.time.delay(300)  # small pause
                self._handle_ai_move()

            # Draw
            self.renderer.draw(self.selected, self.legal_moves)
            pygame.display.flip()
            self.clock.tick(60)

            # Check for game over
            if not self._has_moves(self.turn):
                self._announce_winner(-self.turn)
                pygame.time.delay(2000)
                running = False

        pygame.quit()
        sys.exit()

    def _handle_human_click(self, pos):
        r, c = pos[1] // self.renderer.tile_size, pos[0] // self.renderer.tile_size
        code = self.board.get_piece(r, c)
        # Select a piece
        if self.selected is None and code and code > 0:
            all_caps = self.move_gen.get_capture_moves(1)
            if all_caps:
                seqs = [seq for seq in all_caps if seq['path'][0] == (r, c)]
                self.legal_moves = seqs
            else:
                sims = self.move_gen.get_legal_moves(1)
                self.legal_moves = [m for m in sims if m[0] == (r, c)]
            if self.legal_moves:
                self.selected = (r, c)

        # Execute a move
        elif self.selected:
            chosen = None
            for m in self.legal_moves:
                end = m['path'][-1] if isinstance(m, dict) else m[1]
                if end == (r, c):
                    chosen = m
                    break
            if chosen:
                # apply human move
                self._apply_move(self.board, chosen, 1)
                # dynamic obstacle update
                self.board.update_obstacles()
                self.turn = -1

            # Reset selection
            self.selected = None
            self.legal_moves = []

    def _handle_ai_move(self):
        move = choose_move(self.board, self.ai_depth)
        if move:
            # apply AI move
            self._apply_move(self.board, move, -1)
            # dynamic obstacle update
            self.board.update_obstacles()
        self.turn = 1

    def _apply_move(self, board: Board, move, player: int):
        # Simple or capture
        if isinstance(move, dict):
            path = move['path']
            caps = move['captures']
            for i in range(1, len(path)):
                board.move_piece(path[i-1], path[i])
                board.remove_piece(*caps[i-1])
        else:
            board.move_piece(move[0], move[1])

    def _has_moves(self, player: int) -> bool:
        return bool(self.move_gen.get_capture_moves(player) or
                    self.move_gen.get_legal_moves(player))

    def _announce_winner(self, winner: int):
        font = pygame.font.SysFont(None, 48)
        msg = "You Win!" if winner == 1 else "AI Wins!"
        text = font.render(msg, True, (255, 0, 0))
        rect = text.get_rect(center=self.screen.get_rect().center)
        self.screen.blit(text, rect)
        pygame.display.flip()
