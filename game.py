# import the pygame module 
import pygame 
from Chess import main
from Chess.piece import Piece
  
# Define the background colour 
# using RGB color coding. 
background_colour = (234, 212, 252) 
blue = (0,0,255)
red = (255,0,0)
  
# Define the dimensions of 
# screen object(width,height) 
screen_width = 320
screen_height = 220
screen = pygame.display.set_mode((320, 240)) 
  
# Set the caption of the screen 
pygame.display.set_caption('Mungo Chess') 
  
# Fill the background colour to the screen 
screen.fill(background_colour) 
  

cell_size = min(screen_width, screen_height) // 8

# Calculate the offset to center the grid on the screen
x_offset = (screen_width - cell_size * 8) // 2
y_offset = ((screen_height - cell_size * 8) // 2)*5

# Draw the grid
for i in range(8):
    for j in range(8):
        # Calculate the position of the cell
        x = x_offset + j * cell_size
        y = y_offset + i * cell_size
        # Draw a rectangle for the cell
        pygame.draw.rect(screen, (255, 255, 255), (x, y, cell_size, cell_size), 1) 

pygame.display.flip() 
board_initialized = main.initialize_board()
board = board_initialized[0]
white_map = board_initialized[1]
black_map = board_initialized[2]
# Variable to keep our game loop running 
running = True
turn = True
good_move = False
selected_piece = None
dest = None
clock = pygame.time.Clock()
timer = 0
available_moves = []
white_king_pos = [0,4]
black_king_pos = [7,4]
num_white_promoted = 0
num_black_promoted = 0
white_check = False
black_check = False
# game loop 
while running: 
    clock.tick(60)
    timer += clock.get_time()
    #logic
    if (selected_piece == None and timer>500):
        mouse_pos = pygame.mouse.get_pos()
        if (pygame.mouse.get_pressed()[0]):
            choice = main.piece_at(board,mouse_pos[1],mouse_pos[0])
            if (choice != False):
                if (choice.piece != None and choice.piece.color == turn):
                    selected_piece = choice.piece
                
                    available_moves = selected_piece.available_moves(board,white_map,black_map,white_king_pos,black_king_pos, True)
                    if available_moves == []:
                        selected_piece = None
                        print("wrong piece dummy")
                    timer = 0
                    
    
    if (dest == None and selected_piece != None and timer>500):
        mouse_pos = pygame.mouse.get_pos() 
        if (pygame.mouse.get_pressed()[0]): 
            dest_choice = main.tile_at(board,mouse_pos[1],mouse_pos[0])
            if (dest_choice!=False):
                temp = selected_piece.col
                selected_piece.col = selected_piece.row
                selected_piece.row = temp
                # print((dest_choice.row,dest_choice.col) in selected_piece.available_moves(board,white_map,black_map))
                if ((dest_choice.row,dest_choice.col) in available_moves):
                    dest = dest_choice  
                    board[selected_piece.col][selected_piece.row].piece = None  
                else:
                    temp = selected_piece.col
                    selected_piece.col = selected_piece.row
                    selected_piece.row = temp
                    selected_piece = None
                    print("NOT A LEGAL MOVE")    
                         
    if (dest != None and selected_piece != None):
        white_check = False
        black_check = False
        board[selected_piece.col][selected_piece.row].piece = None
        if(isinstance(selected_piece,main.King)):
            if selected_piece.color:
                white_king_pos[0] = dest.row
                white_king_pos[1] = dest.col
            else:
                black_king_pos[0] = dest.row
                black_king_pos[1] = dest.col    
        if (isinstance(selected_piece,main.Pawn)):
            selected_piece.has_moved = True
            if selected_piece.en_passant_possible:
                selected_piece.en_passant_possible = False
                # print("used")
            if abs(selected_piece.col - dest.row)>1:
                #en passant possible
                selected_piece.en_passant_possible = True
                # print("possible")
        if (dest.piece != None):
            #delete piece from map
            if dest.piece.color:
                name = dest.piece.label
                del white_map[name]
                print("deleted")
            else:
                name = dest.piece.label
                del black_map[name]  
                print("deleted")  
        dest.piece = selected_piece
        dest.piece.col = dest.col
        dest.piece.row = dest.row
        selected_piece = None
        dest = None
        pawn_promoted = main.pawn_promote(board,turn, num_white_promoted if turn else num_black_promoted)
        if pawn_promoted:
            name = pawn_promoted[0].piece.label
            old_name = pawn_promoted[1]
            if turn:
                num_white_promoted += 1
                del white_map[old_name]
                white_map[name] = [pawn_promoted[0].piece, set()]
                white_map[name][1] = set(white_map[name][0].available_moves(board,white_map,black_map,white_king_pos,black_king_pos, False))
            else:
                num_black_promoted += 1
                del black_map[old_name]
                black_map[name] = [pawn_promoted[0].piece, set()]
                black_map[name][1] = set(black_map[name][0].available_moves(board,white_map,black_map,white_king_pos,black_king_pos, False))
        timer = 0
        turn = not turn
        main.attack_map_update(board,white_map,black_map,white_king_pos,black_king_pos)
        if (Piece.check_map((white_king_pos[0],white_king_pos[1]),black_map)):
            white_check = True
        if (Piece.check_map((black_king_pos[0],black_king_pos[1]),white_map)):
            black_check = True
        print(white_map)
        print(black_map)
        # print((2,0) in white_map)
        # print(white_king_pos)
        # print("move made")
     #Drawing
    pygame.display.flip() 
    screen.fill(background_colour) 
    x_offset = (screen_width - cell_size * 8) // 2
    y_offset = ((screen_height - cell_size * 8) // 2)*5

    # Draw the grid
    for i in range(8):
        for j in range(8):
            # Calculate the position of the cell
            x = x_offset + j * cell_size
            y = y_offset + i * cell_size
            # Draw a rectangle for the cell
            pygame.draw.rect(screen, (255, 255, 255), (x, y, cell_size, cell_size), 1) 
    if selected_piece != None:
        for x in available_moves:
            pygame.draw.rect(screen, blue, (x[1]*27 + 53, x[0]*27+11, 25, 25))
    if white_check:
        pygame.draw.rect(screen, red, (white_king_pos[1]*27 + 53, white_king_pos[0]*27+11, 25, 25))
    if black_check:
        pygame.draw.rect(screen, red, (black_king_pos[1]*27 + 53, black_king_pos[0]*27+11, 25, 25))

    for i in range(len(board)):
        for j in range(len(board[0])):
            square = board[i][j]
            if square.piece != None:
                image = square.get_image()
                screen.blit(image,(j*27+55,i*27+12))
    for event in pygame.event.get(): 
    
        # Check for QUIT event       
        if event.type == pygame.QUIT: 
            running = False


   