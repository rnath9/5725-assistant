from Chess.board_cell import Square
from Chess.piece import Piece
from Chess.pawn import Pawn
from Chess.rook import Rook
from Chess.bishop import Bishop
from Chess.queen import Queen
from Chess.knight import Knight
from Chess.king import King
import math
#TODO turn that into a package
def initialize_board():
  board = [[None for _ in range(8)] for _ in range(8)]
  for c in range(8):
    for r in range(8):
      board[r][c] = Square(r,c)
  for col in range(8):
    board[1][col].piece = Pawn(True, [1, col])
    board[6][col].piece = Pawn(False, [6, col])
  white_attack_map = {}
  black_attack_map = {}
  for r in [0,7]:
    for c in [0,7]:
      board[r][c].piece = Rook(True if r == 0 else False, [r,c])
      if r == 0:
        white_attack_map[f"rook{c}"] = [board[r][c].piece, set()]
      else:
        black_attack_map[f"rook{col}"] = [board[r][c].piece, set()]
    for c in [2,5]:
      board[r][c].piece = Bishop(True if r == 0 else False, [r,c])
      if r == 0:
        white_attack_map[f"bishop{c}"] = [board[r][c].piece, set()]
      else:
        black_attack_map[f"bishop{col}"] = [board[r][c].piece, set()]
    for c in [1,6]:
      board[r][c].piece = Knight(True if r == 0 else False, [r,c])
      if r == 0:
        white_attack_map[f"knight{c}"] = [board[r][c].piece, set()]
      else:
        black_attack_map[f"knight{col}"] = [board[r][c].piece, set()]
    board[r][3].piece = Queen(True if r == 0 else False, [r,3])
    board[r][4].piece = King(True if r == 0 else False, [r,4])
    if r == 0:
      white_attack_map["queen"] = [board[r][3].piece, set()]
      white_attack_map["king"] = [board[r][4].piece, set()]
    else:
      black_attack_map["queen"] = [board[r][3].piece, set()]
      black_attack_map["king"] = [board[r][4].piece, set()]
    for k,_ in white_attack_map.items():
      white_attack_map[k][1] = set(white_attack_map[k][0].available_moves(board))
    for k,_ in black_attack_map.items():
      black_attack_map[k][1] = set(black_attack_map[k][0].available_moves(board))
  print(white_attack_map)
  return board 


def piece_at(board, x,y):
  if (x>220 or x<10):
    return False
  elif (y<50 or y>270):
    return False
  else:
    x = x - 10
    y = y - 50
    return board[math.floor(x/27)][math.floor(y/27)]
  
def tile_at(board,x,y):
  if (x>220 or x<10):
    return False
  elif (y<50 or y>270):
    return False
  else:
    x = x - 10
    y = y - 50
    try:
      return board[math.floor(x/27)][math.floor(y/27)]
    except:
      return False
"""Prints ths square name of a coordinate (ex: [0,0] maps to A1)"""
def print_cell(coordinates):
    print(chr(ord('A')+coordinates[1])+str(coordinates[0]+1))

"""Takes in an input, like "A4" and maps it to the coordinates [0,3]"""
def get_coordinates(square_name):
    assert len(square_name) == 2
    return [int(square_name[1])-1,ord(square_name[0].upper()) - ord('A')]

# def print_board():
#   for row in board[::-1]:
#     print(row)

# whiteTurn = True
# while True:
#   print_board()
#   print("make a move")
#   goodMove = False 
#   while not goodMove:
#     userstatement = input().split(" ")
#     piece_place = userstatement[0]
#     destination = userstatement[-1]
#     piece_coords = get_coordinates(piece_place)
#     piece = board[piece_coords[0]][piece_coords[1]].piece
#     try:
#       print(piece.available_moves(board))
#     except AttributeError:
#       print("Not a valid move, try again")
#       continue
#     print(piece.color)
#     if get_coordinates(destination) in piece.available_moves(board) and ((whiteTurn and piece.color == "white") or (not whiteTurn and piece.color != "white")):
#       board[piece_coords[0]][piece_coords[1]].piece = None
#       coords = get_coordinates(destination)
#       board[coords[0]][coords[1]].piece = piece
#       piece.row = coords[0]
#       piece.col = coords[1]
#       goodMove = True
#       whiteTurn = not whiteTurn
# print("\nchecking white E pawn's moves")
# E2 = get_coordinates("E2")
# white_e_pawn = board[E2[0]][E2[1]].piece

# for val in white_e_pawn.available_moves(board):
#   print_cell(val)

# print("\nchecking black E pawn's moves")
# E7 = get_coordinates("E7")
# black_e_pawn = board[E7[0]][E7[1]].piece

# for val in black_e_pawn.available_moves(board):
#   print_cell(val)


# print("\nrook A1's moves")
# A1 = get_coordinates("A1")
# rook = board[A1[0]][A1[1]].piece


# for val in rook.available_moves(board):
#   print_cell(val)

# print(rook.available_moves(board))

# print("\ncreating a dummy black rook at A3, testing moves\n")
# board[2][0].piece = Rook("black", [2,0])
# rookA3 = board[2][0].piece
# for val in rookA3.available_moves(board):
#   print_cell(val)

#bishop testing
# print()
# board[3][3].piece = Bishop("black", [3,3])
# print_cell([3,3])
# print()
# for cell in (board[3][3].piece.available_moves(board)):
#   print_cell(cell)

#queen testing
# print()
# board[3][3].piece = Queen("black", [3,3])
# print(board)
# print()
# for cell in (board[3][3].piece.available_moves(board)):
#   print_cell(cell)

#knight testing
# for cell in (board[7][1].piece.available_moves(board)):
#   print_cell(cell)
