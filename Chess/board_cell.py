class Square():
  def __init__(self, row, col):
    self.piece = None #keeps track of what piece is on it
    self.row = row
    self.col = col

  def __str__(self):
    if self.piece == None:
      return " "
    else:
      return self.piece.__str__()
    
  def __repr__(self):
    return self.__str__()
  
  def get_image(self):
    return self.piece.image
