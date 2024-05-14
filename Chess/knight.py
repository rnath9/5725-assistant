from Chess.piece import Piece
from Chess import main
import copy

class Knight(Piece):
    def __init__(self, color, position,label):
        super().__init__(color, position,"knight",label)

    def __str__(self):
        return "n"

    def __repr__(self):
        return self.__str__()
  
    #Checks the moves that the piece can make and does a lot of computations (It's our special sauce)
    def available_moves(self, board,white_map, black_map, w_king,b_king,pred):
        if self.color:
            king = w_king
            map = black_map
        else:
            king = b_king
            map = white_map
        temp = self.col
        self.col = self.row
        self.row = temp
        res = []
        dirs = [[2,1],[2,-1],[1,2],[1,-2],[-1,2],[-1,-2],[-2,1],[-2,-1]]
        for dr, dc in dirs:
            if self.row + dr <0 or self.row + dr >7 or self.col + dc <0 or self.col + dc >7:
                continue
            if board[self.col + dc][self.row+dr].piece == None:
                if pred:
                    if not main.predict(board,map,w_king,b_king, (king[0],king[1]),(self.col+dc,self.row+dr),(self.col,self.row)):
                        res.append((self.col + dc, self.row+ dr))
                else:
                    res.append((self.col + dc, self.row+ dr))
            #piece present, can we capture it?
            if board[self.col + dc][self.row+dr].piece != None:
                if board[self.col + dc][self.row+dr].piece.color != self.color:
                    if pred:
                        if not main.predict(board,map,w_king,b_king, (king[0],king[1]),(self.col+dc,self.row+dr),(self.col,self.row)):
                            res.append((self.col + dc, self.row+ dr))
                    else:
                        res.append((self.col + dc, self.row+ dr))
                continue
        temp = self.col
        self.col = self.row
        self.row = temp
        return res
