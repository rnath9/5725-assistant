import pygame
class Piece:
  def __init__(self, color, position, piece,label):
    self.color = color
    self.row = position[0]
    self.col = position[1]
    self.label = label
    if (color):
      cname = "white"
    else:
      cname = "black"
    self.image = pygame.image.load('Chess/Images/'+piece+'_'+cname+".png")
    self.image = pygame.transform.scale(self.image,(22,22))
  
    def move(self, board, row, col): #Deprecated
        if [row, col] not in self.available_moves(board):
            return False
        self.row = row
        self.col = col
        return True
  
  def get_image(self):
    return self.image
  
  def check_map(position, map): #used to see if king is in check
    for key, value in map.items():
      if position in value[1]:
        return True
    return False
