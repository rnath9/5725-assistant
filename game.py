# import the pygame module 
import pygame 
  
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

source_image = pygame.image.load('Chess/chessPieces.png')  # Replace 'image.png' with the path to your image file
bishop = pygame.image.load('Chess/Images/bishop_black.png')
image_width, image_height = source_image.get_rect().size
pieces = []
for i in range(2):
    for j in range(3):
        # Define the rectangle for each sub-image
        sub_rect = pygame.Rect(j * image_width/3, i * image_height/2, image_width/3, image_height/2)
        # Extract the sub-image using the sub-rectangle
        sub_image = source_image.subsurface(sub_rect)
        pieces.append(sub_image)

# Get the dimensions of the image
pieces[1] = pygame.transform.scale(pieces[1], (cell_size, cell_size))
bishop = pygame.transform.scale(bishop, (cell_size-4,cell_size-4))
# Calculate the position to center the image on the screen
image_width, image_height = bishop.get_rect().size
# Calculate the position to center the image on the screen
image_x = (screen_width - image_width) // 2
image_y = (screen_height - image_height) // 2

print(cell_size)
# Draw the scaled image ont
# o the screen
screen.blit(bishop, (55, 12))
# Draw the image onto the screen
# Update the display using flip 
pygame.display.flip() 
  
# Variable to keep our game loop running 
running = True
  
# game loop 
while running: 
    
# for loop through the event queue   
    for event in pygame.event.get(): 
      
        # Check for QUIT event       
        if event.type == pygame.QUIT: 
            running = False