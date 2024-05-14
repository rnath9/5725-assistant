from Chess.piece import Piece
from Chess import main
class Rook(Piece):
    def __init__(self, color, position,label):
        super().__init__(color, position,"rook",label)
        self.has_moved = False

    def __str__(self):
        return "r"

    def __repr__(self):
       return self.__str__()
    
    #Checks the moves that the piece can make and does a lot of computations (It's our special sauce)
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