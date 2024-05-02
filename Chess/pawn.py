from Chess.piece import Piece

class Pawn(Piece):
    def __init__(self, color, position):
        super().__init__(color, position, "pawn")
        self.has_moved = False 

    def __repr__(self):
        return self.__str__()
    # def available_moves(self, board):
    #     res = []
    #     #check if can move up one or two
    #     for dr in range(1,3): 
    #         if self.color == False:
    #             dr *= -1 #reverse direction
    #         if self.row + dr <0 or self.row + dr >7:
    #             break #check if out of bounds
    #         print('What Im looking for')
    #         print(self.col)
    #         print(self.row+dr)
    #         if board[self.col+dr][self.row].piece == None:
    #             res.append([self.col+dr, self.row])
    #             #check if can take 
    #         if self.color == True:
    #             dr = 1
    #         else:
    #             dr = -1
    #         if self.row + dr >=0 and self.row+dr <= 7:
    #             if self.col >0 and board[self.col-1][self.row+dr].piece != None and board[self.col-1][self.row+dr].piece.color != self.color:
    #                 res.append([self.col-1, self.row+dr])
    #             if self.col <7 and board[self.col+1][self.row+dr].piece != None and board[self.col+1][self.row+dr].piece.color != self.color:
    #                 res.append([self.col+1, self.row+dr])
    #             #check if en passant
    #             if (self.color == False and self.row == 4) or (self.row == 3 and self.color == False):
    #                 if self.col -1 >0 and type(board[self.row+dr][self.col-1].piece) == Pawn and board[self.row + dr][self.col-1].piece.color != self.color:
    #                     res.append([self.row+1, self.col-1])
    #                 if self.col +1 <7 and type(board[self.row+dr][self.col+1].piece) == Pawn and board[self.row + dr][self.col+1].piece.color != self.color:
    #                     res.append([self.row+1, self.col+1])
    #     return res
    def available_moves(self, board):
        res = []
        # Define movement direction based on pawn color (1 for white, -1 for black)
        direction = 1 if self.color == True else -1
        # Pawn can move one square forward if that square is empty

        if 0 <= self.col + direction < 8 and board[self.col+direction][self.row].piece is None:
        
            res.append([self.col+ direction, self.row])

            # Pawn can move two squares forward from starting position if both squares are empty
            if not self.has_moved and board[self.col+ 2 * direction][self.row].piece is None:
                res.append([self.col+ 2 * direction, self.row])

        # Pawn can capture diagonally
        for dc in [-1, 1]:
            if 0 <= self.col + direction < 8 and 0 <= self.row + dc < 8:
                target_square = board[self.col + direction][self.row+dc]
                if target_square.piece is not None and target_square.piece.color != self.color:
                    res.append([self.col + direction, self.row+dc])

        return res