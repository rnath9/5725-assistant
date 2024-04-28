from board_cell import Square
from piece import Piece
from pawn import Pawn
from rook import Rook
from bishop import Bishop
from queen import Queen

#TODO turn that into a package

board = [[Square() for _ in range(8)] for _ in range(8)]
for col in range(8):
  board[1][col].piece = Pawn("white", [1, col])
  board[6][col].piece = Pawn("black", [6, col])

for r in [0,7]:
  for c in [0,7]:
    board[r][c].piece = Rook("white" if r == 0 else "black", [r,c])
  for c in [2,5]:
    board[r][c].piece = Bishop("white" if r == 0 else "black", [r,c])


"""Prints ths square name of a coordinate (ex: [0,0] maps to A1)"""
def print_cell(coordinates):
  print(chr(ord('A')+coordinates[1])+str(coordinates[0]+1))

"""Takes in an input, like "A4" and maps it to the coordinates [0,3]"""
def get_coordinates(square_name):
  assert len(square_name) == 2
  return [int(square_name[1])-1,ord(square_name[0].upper()) - ord('A')]


print("verify valid board")
print(board)
print("\nchecking white E pawn's moves")
E2 = get_coordinates("E2")
white_e_pawn = board[E2[0]][E2[1]].piece

for val in white_e_pawn.available_moves(board):
  print_cell(val)

print("\nchecking black E pawn's moves")
E7 = get_coordinates("E7")
black_e_pawn = board[E7[0]][E7[1]].piece

for val in black_e_pawn.available_moves(board):
  print_cell(val)


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