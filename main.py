from board_cell import Square
from piece import Piece
from pawn import Pawn

#TODO turn that into a package

board = [[Square() for _ in range(8)] for _ in range(8)]
for col in range(8):
  board[1][col].piece = Pawn("white", [1, col])
  board[6][col].piece = Pawn("black", [6, col])

"""Prints ths square name of a coordinate (ex: [0,0] maps to A1)"""
def print_cell(coordinates):
  print(chr(ord('A')+coordinates[1])+str(coordinates[0]+1))

"""Takes in an input, like "A4" and maps it to the coordinates [0,3]"""
def get_coordinates(square_name):
  assert len(square_name) == 2
  return [int(square_name[1])-1,ord(square_name[0].upper()) - ord('A')]


print("verify valid board")
print(board)
print("\n checking white E pawn's moves")
E2 = get_coordinates("E2")
white_e_pawn = board[E2[0]][E2[1]].piece

for val in white_e_pawn.available_moves(board):
  print_cell(val)

print("\n checking black E pawn's moves")
E7 = get_coordinates("E7")
black_e_pawn = board[E7[0]][E7[1]].piece

for val in black_e_pawn.available_moves(board):
  print_cell(val)