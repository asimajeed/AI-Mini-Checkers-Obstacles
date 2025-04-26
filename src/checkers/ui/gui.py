import sys
import copy
import pygame
from ..board import Board
from ..move_generator import MoveGenerator
from ..ai.minimax import choose_move

class GameGUI:
    """
    Pygame GUI for Mini-Checkers with Obstacles.
    Human is Player 1 (grid>0), AI is Player 2 (grid<0).
    """

    def __init__(self, width=600, height=600, ai_depth=4, obstacle_count=2):
        pygame.init()
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Mini-Checkers with Obstacles")
        self.clock = pygame.time.Clock()

        self.ai_depth       = ai_depth
        self.obstacle_count = obstacle_count

        # initialize game state (board, move_gen, turn, etc.)
        self._reset_game_state()

        from .renderer import BoardRenderer
        self.renderer = BoardRenderer(self.screen, self.board)

    def _reset_game_state(self):
        """Reset board, move generator, turn, selection, etc."""
        self.board       = Board(obstacle_count=self.obstacle_count)
        self.move_gen    = MoveGenerator(self.board)
        self.turn        = 1               # 1 = human; -1 = AI
        self.selected    = None
        self.legal_moves = []
        # update renderer to point at the new board
        if hasattr(self, "renderer"):
            self.renderer.board = self.board

    def run(self):
        running = True
        while running:
            # ─── Human input ─────────────────────────────────────────
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and self.turn == 1:
                    self._handle_human_click(event.pos)

            # Draw after human
            self.renderer.draw(self.selected, self.legal_moves)
            pygame.display.flip()
            self.clock.tick(60)

            # ─── AI turn ───────────────────────────────────────────
            if self.turn == -1:
                # if AI has no moves → human wins
                if not self._has_moves(-1):
                    again = self._show_game_over_screen(winner=1)
                    if again:
                        self._reset_game_state()
                        continue
                    break

                # pause a bit then let AI move
                pygame.time.delay(300)
                self._handle_ai_move()

            # Draw after AI
            self.renderer.draw(self.selected, self.legal_moves)
            pygame.display.flip()
            self.clock.tick(60)

            # ─── Check if next player (human) has no moves → AI wins ─
            if not self._has_moves(self.turn):
                again = self._show_game_over_screen(winner=-self.turn)
                if again:
                    self._reset_game_state()
                    continue
                break

        pygame.quit()
        sys.exit()

    def _show_game_over_screen(self, winner: int) -> bool:
        """
        Draw “You Win!” or “AI Wins!” plus a Play Again button.
        Returns True if Play Again clicked, False if window closed.
        """
        # first, render the final board state
        self.renderer.draw(None, [])
        pygame.display.flip()

        # prepare fonts and messages
        font      = pygame.font.SysFont(None, 64)
        small     = pygame.font.SysFont(None, 36)
        msg       = "You Win!" if winner == 1 else "AI Wins!"
        text      = font.render(msg, True, (255, 0, 0))
        txt_rect  = text.get_rect(center=(self.screen.get_width()//2,
                                          self.screen.get_height()//2 - 40))

        # prepare button
        btn_text  = small.render("Play Again", True, (255, 255, 255))
        btn_w, btn_h = btn_text.get_size()
        btn_rect  = pygame.Rect(
            self.screen.get_width()//2 - btn_w//2 - 10,
            txt_rect.bottom + 20,
            btn_w + 20,
            btn_h + 12
        )

        while True:
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    return False
                elif ev.type == pygame.MOUSEBUTTONDOWN:
                    if btn_rect.collidepoint(ev.pos):
                        return True

            # re-draw board behind the UI elements
            self.renderer.draw(None, [])

            # draw message
            self.screen.blit(text, txt_rect)

            # draw button
            pygame.draw.rect(self.screen, (0, 128, 0), btn_rect)
            self.screen.blit(btn_text, (btn_rect.x + 10, btn_rect.y + 6))

            pygame.display.flip()
            self.clock.tick(30)

    def _handle_human_click(self, pos):
        r, c = pos[1] // self.renderer.tile_size, pos[0] // self.renderer.tile_size
        code = self.board.get_piece(r, c)

        # select
        if self.selected is None and code and code > 0:
            all_caps = self.move_gen.get_capture_moves(1)
            if all_caps:
                self.legal_moves = [seq for seq in all_caps if seq['path'][0] == (r, c)]
            else:
                sims = self.move_gen.get_legal_moves(1)
                self.legal_moves = [m for m in sims if m[0] == (r, c)]
            if self.legal_moves:
                self.selected = (r, c)

        # move
        elif self.selected:
            chosen = None
            for m in self.legal_moves:
                end = m['path'][-1] if isinstance(m, dict) else m[1]
                if end == (r, c):
                    chosen = m
                    break
            if chosen:
                self.renderer.animate_move(
                    self.selected,
                    chosen['path'][-1] if isinstance(chosen, dict) else chosen[1],
                    selected=self.selected,
                    legal_moves=self.legal_moves
                )
                self._apply_move(self.board, chosen, 1)
                self.board.update_obstacles()
                self.turn = -1

            self.selected    = None
            self.legal_moves = []

    def _handle_ai_move(self):
        move = choose_move(self.board, self.ai_depth)
        if move:
            start = move['path'][0] if isinstance(move, dict) else move[0]
            end   = move['path'][-1] if isinstance(move, dict) else move[1]
            self.renderer.animate_move(start, end)
            self._apply_move(self.board, move, -1)
            self.board.update_obstacles()
        self.turn = 1

    def _apply_move(self, board: Board, move, player: int):
        if isinstance(move, dict):
            path, caps = move['path'], move['captures']
            for i in range(1, len(path)):
                board.move_piece(path[i-1], path[i])
                board.remove_piece(*caps[i-1])
        else:
            board.move_piece(move[0], move[1])

    def _has_moves(self, player: int) -> bool:
        return bool(self.move_gen.get_capture_moves(player)
                    or self.move_gen.get_legal_moves(player))
