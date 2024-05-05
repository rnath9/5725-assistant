from Chess.piece import Piece
from Chess import main
class Rook(Piece):
    def __init__(self, color, position,label):
        super().__init__(color, position,"rook",label)

    def __str__(self):
        return "r"

    def __repr__(self):
       return self.__str__()
    # def available_moves(self, board,white_map, black_map,w_king,b_king,pred):
    #     temp = self.col
    #     self.col = self.row
    #     self.row = temp
    #     res = []
    #     #check if can move up one or two
    #     #print("row logic")
    #     possible = [range(-1, -8, -1),range(1,8)]
    #     for ranges in possible:
    #         for dr in ranges:
    #             if self.row + dr <0 or self.row + dr >7:
    #         #print(str(self.row+dr) + " out of bounds, breaking")
    #                 break #check if out of bounds
    #             if board[self.col][self.row+dr].piece == None:
    #                 res.append((self.col, self.row+dr))
    #             #piece present, can we capture it?
    #             if board[self.col][self.row+dr].piece != None:
    #                 if board[self.col][self.row+dr].piece.color != self.color:
    #             #print("takeable piece at " + str(self.row + dr) + "," + str(self.col))
    #                     res.append((self.col, self.row +dr)) # can take
    #         #else:
    #             #print("not takeable piece at " + str(self.row + dr) + "," + str(self.col))
    #                 break
    #     #same logic but for the columns
    #     #print("cols logic")
    #     for ranges in possible:
    #         for dc in ranges:
    #             if self.col + dc <0 or self.col + dc >7:
    #             #print(str(self.col+dc) + " out of bounds, breaking")
    #                 break #check if out of bounds
    #             if board[self.col+dc][self.row].piece == None:
    #                 res.append((self.row, self.col+dc))
    #             #piece present
    #             if board[self.col +dc ][self.row].piece != None:
    #                 if board[self.col+dc ][self.row].piece.color != self.color:
    #                 #print("takeable piece at " + str(self.row) + "," + str(self.col+dc))
    #                     res.append((self.col+dc, self.row)) # can take
    #             #else:
    #             #print("not takeable piece at " + str(self.row) + "," + str(self.col+dc))
    #                 break
    #     temp = self.col
    #     self.col = self.row
    #     self.row = temp
    #     return res
    def available_moves(self, board, white_map, black_map, w_king, b_king, pred):
        if self.color:
            king = w_king
            map = black_map
        else:
            king = b_king
            map = white_map
        res = []
        # Check vertical moves (up and down)
        for dr in range(-1, -8, -1):  # Up
            if self.row + dr < 0:
                break
            if board[self.row + dr][self.col].piece is None:
                res.append((self.row + dr, self.col))
            else:
                if board[self.row + dr][self.col].piece.color != self.color:
                    if pred:
                        if not main.predict(board,map,w_king,b_king, (king[0],king[1]),(self.row+dr,self.col),(self.row,self.col)):
                            res.append((self.row+dr, self.col))
                    else:
                        res.append((self.row+dr, self.col))
                break

        for dr in range(1, 8):  # Down
            if self.row + dr > 7:
                break
            if board[self.row + dr][self.col].piece is None:
                if pred:
                    if not main.predict(board,map,w_king,b_king, (king[0],king[1]),(self.row+dr,self.col),(self.row,self.col)):
                        res.append((self.row+dr, self.col))
                else:
                    res.append((self.row+dr, self.col))
            else:
                if board[self.row + dr][self.col].piece.color != self.color:
                    if pred:
                        if not main.predict(board,map,w_king,b_king, (king[0],king[1]),(self.row+dr,self.col),(self.row,self.col)):
                            res.append((self.row+dr, self.col))
                    else:
                        res.append((self.row+dr, self.col))
                break

        # Check horizontal moves (left and right)
        for dc in range(-1, -8, -1):  # Left
            if self.col + dc < 0:
                break
            if board[self.row][self.col + dc].piece is None:
                if pred:
                    if not main.predict(board,map,w_king,b_king, (king[0],king[1]),(self.row,self.col+dc),(self.row,self.col)):
                        res.append((self.row, self.col+dc))
                else:
                    res.append((self.row, self.col+dc))
            else:
                if board[self.row][self.col + dc].piece.color != self.color:
                    if pred:
                        if not main.predict(board,map,w_king,b_king, (king[0],king[1]),(self.row,self.col+dc),(self.row,self.col)):
                            res.append((self.row, self.col+dc))
                    else:
                        res.append((self.row, self.col+dc))
                break

        for dc in range(1, 8):  # Right
            if self.col + dc > 7:
                break
            if board[self.row][self.col + dc].piece is None:
                if pred:
                    if not main.predict(board,map,w_king,b_king, (king[0],king[1]),(self.row,self.col+dc),(self.row,self.col)):
                        res.append((self.row, self.col+dc))
                else:
                    res.append((self.row, self.col+dc))
            else:
                if board[self.row][self.col + dc].piece.color != self.color:
                    if pred:
                        if not main.predict(board,map,w_king,b_king, (king[0],king[1]),(self.row,self.col+dc),(self.row,self.col)):
                            res.append((self.row, self.col+dc))
                    else:
                        res.append((self.row, self.col+dc))
                break

        return res