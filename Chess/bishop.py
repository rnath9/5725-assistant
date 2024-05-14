from Chess.piece import Piece
from Chess import main
class Bishop(Piece):
    def __init__(self, color, position,label):
        super().__init__(color, position,"bishop",label)

    def __str__(self):
        return "b"

    def __repr__(self):
        return self.__str__()
  
    #Checks the moves that the piece can make and does a lot of computations (It's our special sauce)
    def available_moves(self, board,white_map, black_map,w_king,b_king,pred):
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
        #check if can move up one or two
        possible = [range(-1, -8, -1),range(1,8)]
        diagonals = [zip(possible[0], possible[0]), zip(possible[0], possible[1]),
                     zip(possible[1], possible[0]), zip(possible[1], possible[1])]
        for diagonal in diagonals:
            for (dr, dc) in diagonal:
                if self.row + dr <0 or self.row + dr >7 or self.col + dc <0 or self.col + dc >7:
                    break #check if out of bounds
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
                    break
        temp = self.col
        self.col = self.row
        self.row = temp
        return res