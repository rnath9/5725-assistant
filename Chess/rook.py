from Chess.piece import Piece

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position,"rook")

    def __str__(self):
        return "r"

    def __repr__(self):
       return self.__str__()
    def available_moves(self, board):
        res = []
        #check if can move up one or two
        #print("row logic")
        possible = [range(-1, -8, -1),range(1,8)]
        for ranges in possible:
            for dr in ranges:
                if self.row + dr <0 or self.row + dr >7:
            #print(str(self.row+dr) + " out of bounds, breaking")
                    break #check if out of bounds
                if board[self.col][self.row+dr].piece == None:
                    res.append([self.col, self.row+dr])
                #piece present, can we capture it?
                if board[self.col][self.row+dr].piece != None:
                    if board[self.col][self.row+dr].piece.color != self.color:
                #print("takeable piece at " + str(self.row + dr) + "," + str(self.col))
                        res.append([self.col, self.row +dr]) # can take
            #else:
                #print("not takeable piece at " + str(self.row + dr) + "," + str(self.col))
                    break
        #same logic but for the columns
        #print("cols logic")
        for ranges in possible:
            for dc in ranges:
                if self.col + dc <0 or self.col + dc >7:
                #print(str(self.col+dc) + " out of bounds, breaking")
                    break #check if out of bounds
                if board[self.col+dc][self.row].piece == None:
                    res.append([self.row, self.col+dc])
                #piece present
                if board[self.col +dc ][self.row].piece != None:
                    if board[self.col+dc ][self.row].piece.color != self.color:
                    #print("takeable piece at " + str(self.row) + "," + str(self.col+dc))
                        res.append([self.col+dc, self.row]) # can take
                #else:
                #print("not takeable piece at " + str(self.row) + "," + str(self.col+dc))
                    break
        return res