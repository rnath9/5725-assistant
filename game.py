# import the pygame module 
import pygame 
from Chess import main
  
# Define the background colour 
# using RGB color coding. 
background_colour = (234, 212, 252) 
  
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
board = main.initialize_board()
# Variable to keep our game loop running 
running = True
turn = True
good_move = False
selected_piece = None
dest = None
clock = pygame.time.Clock()
timer = 0
# game loop 
while running: 
    clock.tick(60)
    timer += clock.get_time()
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

    if (selected_piece == None and timer>500):
        mouse_pos = pygame.mouse.get_pos()
        if (pygame.mouse.get_pressed()[0]):
            choice = main.piece_at(board,mouse_pos[1],mouse_pos[0])
            if (choice != False):
                if (choice.piece != None and choice.piece.color == turn):
                    selected_piece = choice.piece
                    print("piece picked")
                    temp = selected_piece.col
                    selected_piece.col = selected_piece.row
                    selected_piece.row = temp
                    print(selected_piece.row)
                    print(selected_piece.col)
                    timer = 0
                    
    
    if (dest == None and selected_piece != None and timer>500):
        mouse_pos = pygame.mouse.get_pos() 
        if (pygame.mouse.get_pressed()[0]): 
            dest_choice = main.tile_at(board,mouse_pos[1],mouse_pos[0])
            if (dest_choice!=False):
                if (dest_choice.piece != None):
                    if (dest_choice.piece.color == turn):
                        print("NOT A LEGAL MOVE")
                        selected_piece = None
                        timer = 0
                    else:
                        print("Taken")
                        dest = dest_choice  
                        board[selected_piece.col][selected_piece.row].piece = None  
                else:
                    dest = dest_choice          
    if (dest != None and selected_piece != None):
        board[selected_piece.col][selected_piece.row].piece = None
        dest.piece = selected_piece
        dest.piece.col = dest.col
        dest.piece.row = dest.row
        selected_piece = None
        dest = None
        timer = 0
        turn = not turn
        print("move made")


   