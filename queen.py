from piece import Piece
from rook import Rook
from bishop import Bishop


class Queen(Piece):
  def __init__(self, color, position):
    super().__init__(color, position)

  def __str__(self):
    return "q"

  def __repr__(self):
    return self.__str__()
  
  def available_moves(self, board):
    res = []
    res += Rook.available_moves(self, board)
    res += Bishop.available_moves(self, board)
    return res