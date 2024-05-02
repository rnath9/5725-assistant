from Chess.piece import Piece

class Pawn(Piece):
  def __init__(self, color, position):
    super().__init__(color, position, "pawn")

    def __repr__(self):
        return self.__str__()
    def available_moves(self, board):
        res = []
        #check if can move up one or two
        for dr in range(1,3): 
            if self.color == "black":
                dr *= -1 #reverse direction
            if self.row + dr <0 or self.row + dr >7:
                break #check if out of bounds
            if board[self.row + dr][self.col].piece == None:
                res.append([self.row + dr, self.col])
             #check if can take 
            if self.color == "white":
                dr = 1
            else:
                dr = -1
            if self.row + dr >=0 and self.row+dr <= 7:
                if self.col >0 and board[self.row + dr][self.col-1].piece != None and board[self.row + dr][self.col-1].piece.color != self.color:
                    res.append([self.row+dr, self.col-1])
                if self.col <7 and board[self.row + dr][self.col+1].piece != None and board[self.row + dr][self.col-1].piece.color != self.color:
                    res.append([self.row+dr, self.col+1])
                #check if en passant
                if (self.color == "white" and self.row == 4) or (self.row == 3 and self.color == "black"):
                    if self.col -1 >0 and type(board[self.row+dr][self.col-1].piece) == Pawn and board[self.row + dr][self.col-1].piece.color != self.color:
                        res.append([self.row+1, self.col-1])
                    if self.col +1 <7 and type(board[self.row+dr][self.col+1].piece) == Pawn and board[self.row + dr][self.col-1].piece.color != self.color:
                        res.append([self.row+1, self.col-1])
        return res