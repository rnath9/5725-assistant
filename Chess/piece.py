class Piece:
  def __init__(self, color, position):
    self.color = color
    self.row = position[0]
    self.col = position[1]
  
  def move(self, board, row, col):
    if [row, col] not in self.available_moves(board):
      return False
    self.row = row
    self.col = col
    return True
  
  def available_moves(self):
    raise NotImplementedError("Subclasses must implement this method")
