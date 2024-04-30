from piece import Piece

class Rook(Piece):
    def __init__(self, color, position):
        super().__init__(color, position)

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
                if board[self.row + dr][self.col].piece == None:
                    res.append([self.row + dr, self.col])
                #piece present, can we capture it?
                if board[self.row + dr][self.col].piece != None:
                    if board[self.row + dr][self.col].piece.color != self.color:
                #print("takeable piece at " + str(self.row + dr) + "," + str(self.col))
                        res.append([self.row + dr, self.col]) # can take
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
                if board[self.row][self.col+dc].piece == None:
                    res.append([self.row, self.col+dc])
                #piece present
                if board[self.row ][self.col+dc].piece != None:
                    if board[self.row ][self.col+dc].piece.color != self.color:
                    #print("takeable piece at " + str(self.row) + "," + str(self.col+dc))
                        res.append([self.row, dc+ self.col]) # can take
                #else:
                #print("not takeable piece at " + str(self.row) + "," + str(self.col+dc))
                    break
        return res