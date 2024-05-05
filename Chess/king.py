from Chess.piece import Piece

class King(Piece):

    def __init__(self, color, position):
        super().__init__(color, position,"king")

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
        dirs = [[-1,1],[0,1],[1,1],[-1,0],[1,0],[1,-1],[-1,0],[-1,-1]]
        for dr, dc in dirs:
            if self.row + dr <0 or self.row + dr >7 or self.col + dc <0 or self.col + dc >7:
                continue
            if board[self.col + dc][self.row+dr].piece == None and not Piece.check_map((self.col+dc,self.row+dr),map):
                # print((self.col+dc,self.row+dr))
                # print(Piece.check_map((self.col+dc,self.row+dr),map))
                # print(map)
                res.append((self.col + dc, self.row+ dr))
            #piece present, can we capture it?
            if board[self.col + dc][self.row+dr].piece != None and not Piece.check_map((self.col+dc,self.row+dr),map):
                if board[self.col + dc][self.row+dr].piece.color != self.color:
                    res.append((self.col + dc, self.row+dr)) # can take
                continue
        temp = self.col
        self.col = self.row
        self.row = temp
        return res
