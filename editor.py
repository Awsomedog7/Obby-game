import pygame
from pygame.locals import *
import os

filecheckname = "leveldata.txt"

if not os.path.exists(filecheckname):
    # Create the file if it doesn't exist
    with open(filecheckname, 'w') as file:
        # Write empty level data
        file.write("........\n........\n........\n........\n........\n........\n........")

# Initialize Pygame
pygame.init()

# Window dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

# Player dimensions
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50

# Block dimensions
BLOCK_WIDTH = 50
BLOCK_HEIGHT = 50

# Load level data from file
def load_level_data(filename):
    with open(filename, 'r') as file:
        data = file.readlines()
        level_data = [line.strip() for line in data]
    return level_data

# Save level data to file
def save_level_data(filename, level_data):
    with open(filename, 'w') as file:
        for row in level_data:
            file.write(row + '\n')

# Initialize the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Level Editor")

# Load level data
level_data = load_level_data("leveldata.txt")
# Level editor variables
current_block = 'B'
# Game loop
running = True
clock = pygame.time.Clock()
while running:
    # Change current block
    keys = pygame.key.get_pressed()
    if keys[K_1]:
        current_block = 'X'
    if keys[K_2]:
        current_block = 'B'
    if keys[K_3]:
        current_block = 'O'
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                ctrl_held = True
            elif event.key == pygame.K_s and ctrl_held:
                save_level_data("leveldata.txt", [''.join(row) for row in level_data])
                pygame.quit()
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LCTRL or event.key == pygame.K_RCTRL:
                ctrl_held = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Get the mouse position and button pressed
            mouse_x, mouse_y = pygame.mouse.get_pos()
            mouse_button = pygame.mouse.get_pressed()

            # Check if the mouse position is within the level data range
            if mouse_x < SCREEN_WIDTH and mouse_y < SCREEN_HEIGHT:
                # Calculate the block position based on mouse position
                block_col = mouse_x // BLOCK_WIDTH
                block_row = mouse_y // BLOCK_HEIGHT

                # Update the level data based on the mouse button
                if mouse_button[0]:  # Left-click to place blocks
                    level_data[block_row] = level_data[block_row][:block_col] + current_block + level_data[block_row][block_col + 1:]
                elif mouse_button[2]:  # Right-click to delete blocks
                    level_data[block_row] = level_data[block_row][:block_col] + '.' + level_data[block_row][block_col + 1:]
                    

    # Fill the background color
    screen.fill(WHITE)

    # Draw the level
    for row in range(len(level_data)):
        for col in range(len(level_data[row])):
            if level_data[row][col] == 'X':
                pygame.draw.rect(screen, BLACK, (col * BLOCK_WIDTH, row * BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT))
            elif level_data[row][col] == 'O':
                pygame.draw.rect(screen, RED, (col * BLOCK_WIDTH, row * BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT))
            elif level_data[row][col] == 'B':
                pygame.draw.rect(screen, BLUE, (col * BLOCK_WIDTH, row * BLOCK_HEIGHT, BLOCK_WIDTH, BLOCK_HEIGHT))

    # Draw the current block type indicator
    if current_block == 'X':
        pygame.draw.rect(screen, BLACK, (10, 10, 20, 20))
    elif current_block == 'O':
        pygame.draw.rect(screen, RED, (10, 10, 20, 20))
    elif current_block == 'B':
        pygame.draw.rect(screen, BLUE, (10, 10, 20, 20))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit the level editor
pygame.quit()
