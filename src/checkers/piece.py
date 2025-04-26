from enum import Enum, auto

class PieceType(Enum):
    MAN = auto()
    KING = auto()

class Piece:
    def __init__(self, color: int, piece_type: PieceType = PieceType.MAN):
        assert color in (1, 2), "Color must be 1 or 2"
        self.color = color
        self.piece_type = piece_type

    @property
    def is_man(self) -> bool:
        return self.piece_type == PieceType.MAN

    @property
    def is_king(self) -> bool:
        return self.piece_type == PieceType.KING

    def crown(self):
        """Promote a man to a king."""
        self.piece_type = PieceType.KING
