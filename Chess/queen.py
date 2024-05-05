from Chess.piece import Piece
from Chess.rook import Rook
from Chess.bishop import Bishop


class Queen(Piece):
  def __init__(self, color, position):
    super().__init__(color, position,"queen")

  def __str__(self):
    return "q"

  def __repr__(self):
    return self.__str__()
  
  def available_moves(self, board,white_map, black_map):
    res = []
    res += Rook.available_moves(self, board,white_map, black_map)
    res += Bishop.available_moves(self, board,white_map, black_map)
    return res