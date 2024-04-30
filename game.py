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