from Chess.piece import Piece

class King(Piece):

  def __init__(self, color, position):
    super().__init__(color, position,"king")

    def __str__(self):
        return "k"
    
    def __repr__(self):
        return self.__str__()
    
    def available_moves(self, board):
        res = []
        dirs = [[-1,1],[0,1],[1,1],[-1,0],[1,0],[-1,1],[-1,0],[-1,-1]]
        for dr, dc in dirs:
            if self.row + dr <0 or self.row + dr >7 or self.col + dc <0 or self.col + dc >7:
                continue
            if board[self.row + dr][self.col+dc].piece == None:
                res.append([self.row + dr, self.col+ dc])
            #piece present, can we capture it?
            if board[self.row + dr][self.col+dc].piece != None:
                if board[self.row + dr][self.col+dc].piece.color != self.color:
                    res.append([self.row + dr, self.col+dc]) # can take
                continue
        return res
