# import the pygame module 
import os
import pygame,pigame 
from stockfish import Stockfish
from Chess import main
from Chess.piece import Piece
from playsound import playsound
from pygame import mixer
import RPi.GPIO as GPIO
os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0')
os.putenv('SDL_MOUSEDRV', 'dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')

def play_chess(elo = 1000):
    # Define the background colour 
    # using RGB color coding. 
    GPIO.setmode(GPIO.BCM)
    
    #Physical quit button
    available_buttons = set([27])
    for i in available_buttons:
            GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    #Initialize AI        
    stockfish = Stockfish("stockfish/stockfish-android-armv7")
    stockfish.set_depth(20)
    stockfish.set_elo_rating(elo)

    #Load resources
    pygame.init()
    background_colour = (128, 128, 128) 
    pitft = pigame.PiTft()
    blue = (0,0,255)
    red = (255,0,0)
    BLACK = (0,0,0)
    font = pygame.font.Font(None, 32)
    mixer.init()
    mixer.music.load("resources/move-self.mp3")
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
    #Initialize Board and attack maps
    board_initialized = main.initialize_board()
    board = board_initialized[0]
    white_map = board_initialized[1]
    black_map = board_initialized[2]
    # Variables to keep our game loop running 
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
    white_mate = False
    black_mate = False
    prevmouse = None
    #print(board_to_fen(board))
    # game loop 
    try: 
        while running: 
            #Increment timer to prevent double clicking   
            clock.tick(60)
            timer += clock.get_time()
            #Physical quit button that uses polling
            if (not GPIO.input(27)):
                raise KeyError
            #Update touch on tft
            pitft.update()
            #logic
            if not white_mate and not black_mate: #Make sure that game is not over
                if not turn: #Player turn
                    if (selected_piece == None and timer>500):
                        mouse_pos = pygame.mouse.get_pos()
                        if (mouse_pos!=prevmouse): #find piece that the player selected
                            prevmouse = mouse_pos
                            choice = main.piece_at(board,mouse_pos[1],mouse_pos[0])
                            if (choice != False):
                                if (choice.piece != None and choice.piece.color == turn):
                                    selected_piece = choice.piece #select piece
                                
                                    available_moves = selected_piece.available_moves(board,white_map,black_map,white_king_pos,black_king_pos, True) #set available moves
                                    if available_moves == []:
                                        selected_piece = None #reset if the piece cannot move
                                    timer = 0
                                    
                    
                    if (dest == None and selected_piece != None and timer>500):
                        mouse_pos = pygame.mouse.get_pos() #Find position that the player wants to move the piece to 
                        if (mouse_pos != prevmouse): 
                            prevmouse = mouse_pos
                            dest_choice = main.tile_at(board,mouse_pos[1],mouse_pos[0])
                            if (dest_choice!=False):
                                temp = selected_piece.col #Weird flipping of variables that should have been avoided
                                selected_piece.col = selected_piece.row
                                selected_piece.row = temp
                                if ((dest_choice.row,dest_choice.col) in available_moves): #make sure move is possible
                                    dest = dest_choice  
                                    board[selected_piece.col][selected_piece.row].piece = None  
                                else:
                                    temp = selected_piece.col
                                    selected_piece.col = selected_piece.row
                                    selected_piece.row = temp
                                    selected_piece = None
                                       
                                        
                    if (dest != None and selected_piece != None): #Piece and destination are chosen
                        white_check = False
                        black_check = False
                        if (turn): #Update all of the pawns for en passant logic
                            for x in board:
                                for y in x:
                                    if y.piece!= None:
                                        if not y.piece.color:
                                            if isinstance(y.piece,main.Pawn):
                                                y.piece.en_passant_possible = False
                        else: 
                            for x in board:
                                for y in x:
                                    if y.piece!= None:
                                        if y.piece.color:
                                            if isinstance(y.piece,main.Pawn):
                                                y.piece.en_passant_possible = False   
                        board[selected_piece.col][selected_piece.row].piece = None #remove piece from original location
                        if(isinstance(selected_piece,main.King)): 
                            selected_piece.has_moved = True
                            if selected_piece.color: #update global location
                                white_king_pos[0] = dest.row
                                white_king_pos[1] = dest.col
                            else:
                                black_king_pos[0] = dest.row
                                black_king_pos[1] = dest.col  
                            if abs(selected_piece.row - dest.col)>1: #Move the appropriate rook when castling
                                if dest.col >4:
                                    if turn:
                                        board[0][5].piece = board[0][7].piece
                                        board[0][5].piece.row = 0
                                        board[0][5].piece.col = 5
                                        board[0][7].piece = None
                                    else:
                                        board[7][5].piece = board[7][7].piece
                                        board[7][5].piece.row = 7
                                        board[7][5].piece.col = 5
                                        board[7][7].piece = None   
                                else:
                                    if turn:
                                        board[0][3].piece = board[0][0].piece
                                        board[0][3].piece.row = 0
                                        board[0][3].piece.col = 3
                                        board[0][0].piece = None
                                    else:
                                        board[7][3].piece = board[7][0].piece
                                        board[7][3].piece.row = 7
                                        board[7][3].piece.col = 3
                                        board[7][0].piece = None 
                            
                        if (isinstance(selected_piece,main.Pawn)):
                            selected_piece.has_moved = True #used for two square pawn move
                            if abs(selected_piece.col - dest.row)>1:
                                #en passant possible
                                selected_piece.en_passant_possible = True
                                if (board[dest.row][dest.col].piece == None and isinstance(board[dest.row +(-1 if turn else +1) ][dest.col].piece,main.Pawn)): 
                                    #Deleting the correct pieces for en passant
                                    name = board[dest.row +(-1 if turn else +1) ][dest.col].piece.label
                                    if turn:
                                        del black_map[name]
                                    else:
                                        del white_map[name]  
                                    board[dest.row +(-1 if turn else +1) ][dest.col].piece = None   
                        if (isinstance(selected_piece,main.Rook)): #Used for castling logic
                            selected_piece.has_moved = True
                        if (dest.piece != None):
                            #delete piece from map
                            if dest.piece.color:
                                name = dest.piece.label
                                del white_map[name]
                            else:
                                name = dest.piece.label
                                del black_map[name]     
                        dest.piece = selected_piece
                        dest.piece.col = dest.col
                        dest.piece.row = dest.row
                        selected_piece = None
                        dest = None
                        pawn_promoted = main.pawn_promote(board,turn, num_white_promoted if turn else num_black_promoted)
                        if pawn_promoted: #promote pawn to a queen when possible by changing board and attack map
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
                        main.attack_map_update(board,white_map,black_map,white_king_pos,black_king_pos) #update the attack map
                        if (Piece.check_map((white_king_pos[0],white_king_pos[1]),black_map)): #Checking if either player is in check and also checkmate
                            white_check = True
                            white_mate = True
                            for x in board:
                                for y in x:
                                    if y.piece !=None and y.piece.color:
                                        if y.piece.available_moves(board,white_map,black_map,white_king_pos,black_king_pos, True) != []:
                                            white_mate = False              
                        if (Piece.check_map((black_king_pos[0],black_king_pos[1]),white_map)):
                            black_check = True
                            black_mate = True
                            for x in board:
                                for y in x:
                                    if y.piece !=None and not y.piece.color:
                                        if y.piece.available_moves(board,white_map,black_map,white_king_pos,black_king_pos, True) != []:
                                            black_mate = False
                        mixer.music.play() #Play chess move noise
                else: #AI Turn
                    if timer>500: 
                        FEN = board_to_fen(board) #Translate board for AI
                        stockfish.set_fen_position(FEN)
                        move = stockfish.get_best_move(10000) #Give it about 3 seconds to think
                        start, end = AI_move(move) 
                        #translate the move onto the actual board (Same as for the player)
                        selected_piece = board[start[0]][start[1]].piece
                        dest = board[end[0]][end[1]]
                        tmp = selected_piece.row
                        selected_piece.row = selected_piece.col
                        selected_piece.col = tmp
                        white_check = False
                        black_check = False
                        if (turn):
                            for x in board:
                                for y in x:
                                    if y.piece!= None:
                                        if not y.piece.color:
                                            if isinstance(y.piece,main.Pawn):
                                                y.piece.en_passant_possible = False
                        else: 
                            for x in board:
                                for y in x:
                                    if y.piece!= None:
                                        if y.piece.color:
                                            if isinstance(y.piece,main.Pawn):
                                                y.piece.en_passant_possible = False   
                        board[selected_piece.col][selected_piece.row].piece = None
                        if(isinstance(selected_piece,main.King)):
                            selected_piece.has_moved = True
                            if selected_piece.color:
                                white_king_pos[0] = dest.row
                                white_king_pos[1] = dest.col
                            else:
                                black_king_pos[0] = dest.row
                                black_king_pos[1] = dest.col  
                            if abs(selected_piece.row - dest.col)>1:
                                if dest.col >4:
                                    if turn:
                                        board[0][5].piece = board[0][7].piece
                                        board[0][5].piece.row = 0
                                        board[0][5].piece.col = 5
                                        board[0][7].piece = None
                                    else:
                                        board[7][5].piece = board[7][7].piece
                                        board[7][5].piece.row = 7
                                        board[7][5].piece.col = 5
                                        board[7][7].piece = None   
                                else:
                                    if turn:
                                        board[0][3].piece = board[0][0].piece
                                        board[0][3].piece.row = 0
                                        board[0][3].piece.col = 3
                                        board[0][0].piece = None
                                    else:
                                        board[7][3].piece = board[7][0].piece
                                        board[7][3].piece.row = 7
                                        board[7][3].piece.col = 3
                                        board[7][0].piece = None 
                            
                        if (isinstance(selected_piece,main.Pawn)):
                            selected_piece.has_moved = True
                            if abs(selected_piece.col - dest.row)>1:
                                #en passant possible
                                selected_piece.en_passant_possible = True
                                # print("possible")
                                if (board[dest.row][dest.col].piece == None and isinstance(board[dest.row +(-1 if turn else +1) ][dest.col].piece,main.Pawn)):
                                    name = board[dest.row +(-1 if turn else +1) ][dest.col].piece.label
                                    if turn:
                                        del black_map[name]
                                    else:
                                        del white_map[name]  
                                    board[dest.row +(-1 if turn else +1) ][dest.col].piece = None   
                        if (isinstance(selected_piece,main.Rook)):
                            selected_piece.has_moved = True
                        if (dest.piece != None):
                            #delete piece from map
                            if dest.piece.color:
                                name = dest.piece.label
                                del white_map[name]
                            else:
                                name = dest.piece.label
                                del black_map[name]     
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
                            white_mate = True
                            for x in board:
                                for y in x:
                                    if y.piece !=None and y.piece.color:
                                        if y.piece.available_moves(board,white_map,black_map,white_king_pos,black_king_pos, True) != []:
                                            white_mate = False               
                        if (Piece.check_map((black_king_pos[0],black_king_pos[1]),white_map)):
                            black_check = True
                            black_mate = True
                            for x in board:
                                for y in x:
                                    if y.piece !=None and not y.piece.color:
                                        if y.piece.available_moves(board,white_map,black_map,white_king_pos,black_king_pos, True) != []:
                                            black_mate = False
                        turn = False #swamp turn
                        mixer.music.play() #play sound
            else:
                if timer > 5000:
                    raise ValueError
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
                    if (x+y) % 2 == 0:
                        pygame.draw.rect(screen, (92, 64, 51), (x, y, 25,25))
                    else:
                        pygame.draw.rect(screen, (225, 193, 110), (x, y, 25,25))
                    #     pygame.draw.rect(screen, (225, 193, 110), (x, y, cell_size, cell_size), 27) 
                    pygame.draw.rect(screen, (255, 255, 255), (x, y, cell_size, cell_size), 1) 
            if selected_piece != None: #Draw available moves
                for x in available_moves:
                    pygame.draw.rect(screen, blue, (x[1]*27 + 53, x[0]*27+11, 25, 25))
            if white_check: #Draw if in check
                pygame.draw.rect(screen, red, (white_king_pos[1]*27 + 53, white_king_pos[0]*27+11, 25, 25))
            if black_check:
                pygame.draw.rect(screen, red, (black_king_pos[1]*27 + 53, black_king_pos[0]*27+11, 25, 25))

            for i in range(len(board)): #draw pieces on board
                for j in range(len(board[0])):
                    square = board[i][j]
                    if square.piece != None:
                        image = square.get_image()
                        screen.blit(image,(j*27+55,i*27+12))
            if white_mate: #Draw winning or losing text
                text = font.render("CHECKMATE: BLACK WINS", True, BLACK)

                # Get the rectangle object that has the dimensions of the text surface
                text_rect = text.get_rect()

                # Center the text
                text_rect.center = (screen_width // 2, screen_height // 2)

                # Blit the text surface onto the screen
                screen.blit(text, text_rect)
            if black_mate:
                text = font.render("CHECKMATE: WHITE WINS", True, BLACK)

                # Get the rectangle object that has the dimensions of the text surface
                text_rect = text.get_rect()

                # Center the text
                text_rect.center = (screen_width // 2, screen_height // 2)

                # Blit the text surface onto the screen
                screen.blit(text, text_rect)
            for event in pygame.event.get(): #quitting using the x button (Used for when testing on laptop)
            
                # Check for QUIT event       
                if event.type == pygame.QUIT: 
                    running = False
    except: #close out cleanly
        del (pitft)
        pass
    finally:
        pass

def board_to_fen(board):
    fen = ''
    empty_squares = 0

    for i in range(7,-1,-1):
        for square in board[i]:
            if square.piece == None:
                empty_squares += 1
            else:
                if empty_squares > 0:
                    fen += str(empty_squares)
                    empty_squares = 0
                piece = square.piece
                if piece.color:
                    fen += square.piece.__str__().upper()
                else:
                    fen += square.piece.__str__().lower()    
        if empty_squares > 0:
            fen += str(empty_squares)
            empty_squares = 0
        fen += '/'

    fen = fen[:-1]  # Remove the trailing '/'
    fen += ' w - - 0 1'

    return fen

def AI_move(command): #Parsing the AI command
    start = command[:2]
    dest = command[2:]
    return main.get_coordinates(start), main.get_coordinates(dest)


if __name__ == "__main__": #Used for testing
    play_chess(1000)
