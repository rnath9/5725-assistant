class Square():
  def __init__(self):
    self.piece = None #keeps track of what piece is on it

  def __str__(self):
    if self.piece == None:
      return ""
    else:
      return self.piece.__str__()
    
  def __repr__(self):
    return self.__str__()
