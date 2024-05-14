from Chess.board_cell import Square
from Chess.piece import Piece
from Chess.pawn import Pawn
from Chess.rook import Rook
from Chess.bishop import Bishop
from Chess.queen import Queen
from Chess.knight import Knight
from Chess.king import King
import math

def initialize_board(): #SETUP THE GLORIOUS BOARD AND THE ATTACK MAPS
  board = [[None for _ in range(8)] for _ in range(8)]
  for c in range(8):
    for r in range(8):
      board[r][c] = Square(r,c)
  white_attack_map = {}
  black_attack_map = {}    
  for col in range(8):
    board[1][col].piece = Pawn(True, [1, col],f"pawn{col}")
    white_attack_map[f"pawn{col}"] = [board[1][col].piece, set()]
    board[6][col].piece = Pawn(False, [6, col],f"pawn{col}")
    black_attack_map[f"pawn{col}"] = [board[6][col].piece, set()]
  for r in [0,7]:
    for c in [0,7]:
      board[r][c].piece = Rook(True if r == 0 else False, [r,c],f"rook{c}" if r== 0 else f"rook{c}")
      if r == 0:
        white_attack_map[f"rook{c}"] = [board[r][c].piece, set()]
      else:
        black_attack_map[f"rook{c}"] = [board[r][c].piece, set()]
    for c in [2,5]:
      board[r][c].piece = Bishop(True if r == 0 else False, [r,c],f"bishop{c}" if r== 0 else f"bishop{c}")
      if r == 0:
        white_attack_map[f"bishop{c}"] = [board[r][c].piece, set()]
      else:
        black_attack_map[f"bishop{c}"] = [board[r][c].piece, set()]
    for c in [1,6]:
      board[r][c].piece = Knight(True if r == 0 else False, [r,c],f"knight{c}" if r== 0 else f"knight{c}")
      if r == 0:
        white_attack_map[f"knight{c}"] = [board[r][c].piece, set()]
      else:
        black_attack_map[f"knight{c}"] = [board[r][c].piece, set()]
    board[r][3].piece = Queen(True if r == 0 else False, [r,3],"queen")
    board[r][4].piece = King(True if r == 0 else False, [r,4],"king")
    if r == 0:
      white_attack_map["queen"] = [board[r][3].piece, set()]
      white_attack_map["king"] = [board[r][4].piece, set()]
    else:
      black_attack_map["queen"] = [board[r][3].piece, set()]
      black_attack_map["king"] = [board[r][4].piece, set()]
    for k,_ in white_attack_map.items():
      white_attack_map[k][1] = set(white_attack_map[k][0].available_moves(board,white_attack_map,black_attack_map,(0,4),(7,4),False))
    for k,_ in black_attack_map.items():
      black_attack_map[k][1] = set(black_attack_map[k][0].available_moves(board,white_attack_map,black_attack_map,(0,4),(7,4),False))
  return [board,white_attack_map,black_attack_map] 

def attack_map_update(board,white_attack_map,black_attack_map,w_king,b_king):
  for k,_ in white_attack_map.items():
    if (isinstance(white_attack_map[k][0], Pawn)):
      white_attack_map[k][1] = set(white_attack_map[k][0].available_pawn_attack(board,white_attack_map,black_attack_map,w_king,b_king, False))
    else:
      white_attack_map[k][1] = set(white_attack_map[k][0].available_moves(board,white_attack_map,black_attack_map,w_king,b_king, False))
  for k,_ in black_attack_map.items():
    if (isinstance(black_attack_map[k][0], Pawn)):
      black_attack_map[k][1] = set(black_attack_map[k][0].available_pawn_attack(board,white_attack_map,black_attack_map,w_king,b_king, False))
    else:
      black_attack_map[k][1] = set(black_attack_map[k][0].available_moves(board,white_attack_map,black_attack_map,w_king,b_king, False))

def predict(board,map,w_king,b_king, king,new_pos,og_pos): #Look at potential board setups to see if certain moves are possible
  changed = False
  old_piece = board[new_pos[0]][new_pos[1]].piece
  if (board[new_pos[0]][new_pos[1]].piece != None):
    name = board[new_pos[0]][new_pos[1]].piece.label
    del map[name]
    changed = True
  board[new_pos[0]][new_pos[1]].piece = board[og_pos[0]][og_pos[1]].piece
  board[og_pos[0]][og_pos[1]].piece = None
  for k,_ in map.items():
    map[k][1] = set(map[k][0].available_moves(board,map,map,w_king,b_king, False))
  result = Piece.check_map(king,map)
  board[og_pos[0]][og_pos[1]].piece = board[new_pos[0]][new_pos[1]].piece
  board[new_pos[0]][new_pos[1]].piece = old_piece
  if changed:
    map[name] = [board[new_pos[0]][new_pos[1]].piece, set()]
  for k,_ in map.items():
    if (isinstance(map[k][0], Pawn)):
      map[k][1] = set(map[k][0].available_pawn_attack(board,map,map,w_king,b_king, False))
    else:  
      map[k][1] = set(map[k][0].available_moves(board,map,map,w_king,b_king, False))
  return result

def pawn_promote(board, turn, num_promoted):
    for cell in board[7 if turn else 0]:
      if isinstance(cell.piece, Pawn):
        old_name = cell.piece.label
        cell.piece = Queen(turn, [7 if turn else 0, cell.col], f"queen_p{num_promoted}")
        return cell, old_name
    return None

def piece_at(board, x,y): #translates screen coordinates to board
  if (x>=220 or x<=10):
    return False
  elif (y<50 or y>270):
    return False
  else:
    x = x - 10
    y = y - 50
    return board[math.floor(x/27)][math.floor(y/27)]
  
def tile_at(board,x,y): #deprecated
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
def print_cell(coordinates): #used in original version which was in the terminal
    print(chr(ord('A')+coordinates[1])+str(coordinates[0]+1))

"""Takes in an input, like "A4" and maps it to the coordinates [0,3]"""
def get_coordinates(square_name): #used for translating AI
    assert len(square_name) == 2
    return [int(square_name[1])-1,ord(square_name[0].upper()) - ord('A')]

