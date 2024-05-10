from Chess.piece import Piece
from Chess import main

class Pawn(Piece):
    def __init__(self, color, position,label):
        super().__init__(color, position, "pawn",label)
        self.has_moved = False 
        self.en_passant_possible = False

    def __str__(self):
        return "p"

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
        # Define movement direction based on pawn color (1 for white, -1 for black)
        direction = 1 if self.color == True else -1
        # Pawn can move one square forward if that square is empty

        if 0 <= self.col + direction < 8 and board[self.col+direction][self.row].piece is None:
            if pred:
                if not main.predict(board,map,w_king,b_king, (king[0],king[1]),(self.col+direction,self.row),(self.col,self.row)):
                    res.append((self.col +direction, self.row))
            else:
                res.append((self.col + direction, self.row))

            # Pawn can move two squares forward from starting position if both squares are empty
            if not self.has_moved and board[self.col+ 2 * direction][self.row].piece is None:
                if pred:
                    if not main.predict(board,map,w_king,b_king, (king[0],king[1]),(self.col+2*direction,self.row),(self.col,self.row)):
                        res.append((self.col +2*direction, self.row))
                else:
                    res.append((self.col + 2*direction, self.row))

        # Pawn can capture diagonally
        for dc in [-1, 1]:
            if 0 <= self.col + direction < 8 and 0 <= self.row + dc < 8:
                target_square = board[self.col + direction][self.row+dc]
                if target_square.piece is not None and target_square.piece.color != self.color:
                    if pred:
                        if not main.predict(board,map,w_king,b_king, (king[0],king[1]),(self.col+direction,self.row+dc),(self.col,self.row)):
                            res.append((self.col +direction, self.row+dc))
                    else:
                        res.append((self.col + direction, self.row+dc))
        if (self.color and (self.col == 4)) or ((not self.color) and (self.col == 3)):
            for dc in [-1,1]:
                if 0 <= self.col + direction < 8 and 0 <= self.row + dc < 8:
                    target_square = board[self.col + direction][self.row+dc]
                    target = board[self.col][self.row+dc]
                    if target.piece != None and target_square.piece == None and isinstance(target.piece,Pawn) and target.piece.en_passant_possible:
                        if pred:
                            if not main.predict(board,map,w_king,b_king, (king[0],king[1]),(self.col+direction,self.row+dc),(self.col,self.row)):
                                res.append((self.col+direction, self.row+dc))
                        else:
                            res.append((self.col+direction, self.row+dc))
        temp = self.col
        self.col = self.row
        self.row = temp
        return res
    
    def available_pawn_attack(self,board,white_map,black_map,w_king,b_king, pred):
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
        # Define movement direction based on pawn color (1 for white, -1 for black)
        direction = 1 if self.color == True else -1
        # Pawn can move one square forward if that square is empty

        # Pawn can capture diagonally
        for dc in [-1, 1]:
            if 0 <= self.col + direction < 8 and 0 <= self.row + dc < 8:
                target_square = board[self.col + direction][self.row+dc]
                if target_square.piece is None:
                    if pred:
                        if not main.predict(board,map,w_king,b_king, (king[0],king[1]),(self.col+direction,self.row+dc),(self.col,self.row)):
                            res.append((self.col +direction, self.row+dc))
                    else:
                        res.append((self.col + direction, self.row+dc))
                if target_square.piece is not None and target_square.piece.color != self.color:
                    if pred:
                        if not main.predict(board,map,w_king,b_king, (king[0],king[1]),(self.col+direction,self.row+dc),(self.col,self.row)):
                            res.append((self.col +direction, self.row+dc))
                    else:
                        res.append((self.col + direction, self.row+dc))
        
        #En Passant (GOD I HATE THIS MOVE)
        if (self.color and self.col == 4) or (not self.color and self.col == 3):
            # print("hello")
            for dc in [-1,1]:
                if 0 <= self.col + direction < 8 and 0 <= self.row + dc < 8:
                    target_square = board[self.col + direction][self.row+dc]
                    target = board[self.col+direction][self.row]
                    if target.piece != None and target_square.piece == None and isinstance(target.piece,Pawn) and target.piece.en_passant_possible:
                        if pred:
                            if not main.predict(board,map,w_king,b_king, (king[0],king[1]),(self.col+direction,self.row+dc),(self.col,self.row)):
                                res.append((self.col +direction, self.row+dc))
                        else:
                            res.append((self.col + direction, self.row+dc))

        temp = self.col
        self.col = self.row
        self.row = temp
        return res