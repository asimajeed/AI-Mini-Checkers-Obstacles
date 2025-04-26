import pygame
from ..board import Board

class BoardRenderer:
    """
    Handles all drawing: board grid, obstacles, pieces, selection highlights.
    """

    def __init__(self, screen: pygame.Surface, board: Board):
        self.screen = screen
        self.board = board
        self.rows = board.rows
        self.cols = board.cols
        self.tile_size = min(screen.get_width() // self.cols,
                              screen.get_height() // self.rows)

        # Colors
        self.light_color = (232, 235, 239)
        self.dark_color  = (125, 135, 150)
        self.obs_color   = (50,  50,  50)
        self.sel_color   = (0,   255,   0)
        self.move_color  = (255,   0,   0)
        self.p1_color    = (255, 255, 255)
        self.p2_color    = (0,    0,   0)

    def draw(self, selected=None, legal_moves=None):
        # Draw board squares and obstacles
        for r in range(self.rows):
            for c in range(self.cols):
                rect = pygame.Rect(
                    c * self.tile_size,
                    r * self.tile_size,
                    self.tile_size,
                    self.tile_size
                )
                base = self.dark_color if (r + c) % 2 else self.light_color
                pygame.draw.rect(self.screen, base, rect)
                if self.board.is_obstacle(r, c):
                    pygame.draw.rect(self.screen, self.obs_color, rect)

        # Highlight selected piece
        if selected:
            r, c = selected
            rect = pygame.Rect(
                c * self.tile_size,
                r * self.tile_size,
                self.tile_size,
                self.tile_size
            )
            pygame.draw.rect(self.screen, self.sel_color, rect, 3)

        # Highlight legal move targets
        if legal_moves:
            for m in legal_moves:
                end = m['path'][-1] if isinstance(m, dict) else m[1]
                r, c = end
                center = (
                    c * self.tile_size + self.tile_size // 2,
                    r * self.tile_size + self.tile_size // 2
                )
                radius = self.tile_size // 6
                pygame.draw.circle(self.screen, self.move_color, center, radius)

        # Draw pieces
        for r in range(self.rows):
            for c in range(self.cols):
                code = self.board.get_piece(r, c)
                if not code:
                    continue
                color = self.p1_color if code > 0 else self.p2_color
                center = (
                    c * self.tile_size + self.tile_size // 2,
                    r * self.tile_size + self.tile_size // 2
                )
                radius = self.tile_size // 2 - 8
                pygame.draw.circle(self.screen, color, center, radius)
                # King indicator
                if abs(code) == 2:
                    inner_radius = radius // 2
                    pygame.draw.circle(self.screen, (200, 200, 0), center, inner_radius)


    def animate_move(self, start, end, selected=None, legal_moves=None):
        piece = self.board.get_piece(*start)
        start_x = start[1] * self.tile_size + self.tile_size // 2
        start_y = start[0] * self.tile_size + self.tile_size // 2
        end_x = end[1] * self.tile_size + self.tile_size // 2
        end_y = end[0] * self.tile_size + self.tile_size // 2

        frames = 20
        dx = (end_x - start_x) / frames
        dy = (end_y - start_y) / frames

        clock = pygame.time.Clock()

        for frame in range(frames + 1):
            self.draw(selected, legal_moves)  # normal draw

            # Cover the start square manually to avoid duplicate piece
            r, c = start
            rect = pygame.Rect(
                c * self.tile_size,
                r * self.tile_size,
                self.tile_size,
                self.tile_size
            )
            base_color = self.dark_color if (r + c) % 2 else self.light_color
            pygame.draw.rect(self.screen, base_color, rect)

            if self.board.is_obstacle(r, c):
                pygame.draw.rect(self.screen, self.obs_color, rect)

            # Draw the moving piece
            current_x = start_x + dx * frame
            current_y = start_y + dy * frame
            color = self.p1_color if piece > 0 else self.p2_color
            radius = self.tile_size // 2 - 8

            pygame.draw.circle(self.screen, color, (int(current_x), int(current_y)), radius)

            if abs(piece) == 2:  # king indicator
                inner_radius = radius // 2
                pygame.draw.circle(self.screen, (200, 200, 0), (int(current_x), int(current_y)), inner_radius)

            pygame.display.flip()
            clock.tick(60)
