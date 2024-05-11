from Chess.piece import Piece
from Chess.rook import Rook
from Chess import main

class King(Piece):

    def __init__(self, color, position,label):
        super().__init__(color, position,"king",label)
        self.has_moved = False

    def __str__(self):
        return "k"
    
    def __repr__(self):
        return self.__str__()
    
    def available_moves(self, board, white_map, black_map,w_king,b_king,pred):
        if self.color:
            map = black_map
        else:
            map = white_map    
        temp = self.col
        self.col = self.row
        self.row = temp
        res = []
        dirs = [[-1,1],[0,1],[1,1],[-1,0],[1,0],[1,-1],[0,-1],[-1,-1]]
        for dr, dc in dirs:
            if self.row + dr <0 or self.row + dr >7 or self.col + dc <0 or self.col + dc >7:
                continue
            if board[self.col + dc][self.row+dr].piece == None and not Piece.check_map((self.col+dc,self.row+dr),map):
                if pred:
                    if not main.predict(board,map,w_king,b_king, (self.col+dc,self.row+dr),(self.col+dc,self.row+dr),(self.col,self.row)):
                        res.append((self.col + dc, self.row+ dr))
                else:
                    res.append((self.col + dc, self.row+ dr))
                # print((self.col+dc,self.row+dr))
                # print(Piece.check_map((self.col+dc,self.row+dr),map))
                # print(map)
                # res.append((self.col + dc, self.row+ dr))
            #piece present, can we capture it?
            if board[self.col + dc][self.row+dr].piece != None and not Piece.check_map((self.col+dc,self.row+dr),map):
                if board[self.col + dc][self.row+dr].piece.color != self.color:
                    if pred:
                        if not main.predict(board,map,w_king,b_king, (self.col,self.row),(self.col+dc,self.row+dr),(self.col,self.row)):
                            res.append((self.col + dc, self.row+ dr))
                    else:
                        res.append((self.col + dc, self.row+ dr))
                    # res.append((self.col + dc, self.row+dr)) # can take
                continue
        if (not Piece.check_map((self.col,self.row),map) and not self.has_moved):
            possible = True
            for x in [1,2]:
                if board[self.col][self.row+x].piece != None or Piece.check_map((self.col,self.row+x),map):
                    possible = False
            if board[self.col][self.row+3].piece != None and isinstance(board[self.col][self.row+3].piece,Rook) and not board[self.col][self.row+3].piece.has_moved and possible:  
                res.append((self.col, self.row+2))
            possible = True    
            for x in [-1,-2,-3]:
                if board[self.col][self.row+x].piece != None or (x != -3 and Piece.check_map((self.col,self.row+x),map)):
                    possible = False   
            if board[self.col][self.row-4].piece != None and isinstance(board[self.col][self.row-4].piece,Rook) and not board[self.col][self.row-4].piece.has_moved and possible:  
                res.append((self.col, self.row-2))    
        temp = self.col
        self.col = self.row
        self.row = temp
        return res
