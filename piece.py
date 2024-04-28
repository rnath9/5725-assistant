class Piece:
  def __init__(self, color, position):
    self.color = color
    self.row = position[0]
    self.col = position[1]
  
  def move(self, new_position):
    if new_position not in self.available_moves():
      return False
    self.position = new_position
    return True
  
  def available_moves(self):
    raise NotImplementedError("Subclasses must implement this method")
