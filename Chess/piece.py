import pygame
class Piece:
  def __init__(self, color, position, piece):
    self.color = color
    self.row = position[0]
    self.col = position[1]
    if (color):
      cname = "white"
    else:
      cname = "black"
    self.image = pygame.image.load('Chess/Images/'+piece+'_'+cname+".png")
    self.image = pygame.transform.scale(self.image,(22,22))
  
    def move(self, board, row, col):
        if [row, col] not in self.available_moves(board):
            return False
        self.row = row
        self.col = col
        return True
  
  def get_image(self):
    return self.image
  
  def check_map(position, map):
    for key, value in map.items():
      if position in value[1]:
        return True
    return False
  # def available_moves(self):
  #   raise NotImplementedError("Subclasses must implement this method")
