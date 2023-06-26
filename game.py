import pygame
from pygame.locals import *

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
PLAYER_SPEED = 5

# Gravity
GRAVITY = 0.5

# Load level data from file
def load_level_data(filename):
    with open(filename, 'r') as file:
        data = file.readlines()
        level_data = [line.strip() for line in data]
    return level_data

# Initialize the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Obby Game")

# Load level data
level_data = load_level_data("leveldata.txt")

# Game loop
running = True
clock = pygame.time.Clock()

# Player attributes
player_x = 50
player_y = SCREEN_HEIGHT - PLAYER_HEIGHT
player_vel_x = 0
player_vel_y = 0

# Flag to indicate if collisions with black blocks are enabled
enable_collisions = True

while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_vel_x = -PLAYER_SPEED
    elif keys[pygame.K_RIGHT]:
        player_vel_x = PLAYER_SPEED
    else:
        player_vel_x = 0

    if keys[pygame.K_SPACE] and player_y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
        player_vel_y = -10
    if keys[pygame.K_UP] and player_y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
        player_vel_y = -10
        enable_collisions = False
    else:
        enable_collisions = True

    player_x += player_vel_x
    player_y += player_vel_y
    player_vel_y += GRAVITY

    # Check collision with the ground
    if player_y >= SCREEN_HEIGHT - PLAYER_HEIGHT:
        player_y = SCREEN_HEIGHT - PLAYER_HEIGHT
        player_vel_y = 0

    # Check collision with obstacles
    for row in range(len(level_data)):
        for col in range(len(level_data[row])):
            if level_data[row][col] == 'B':
                obstacle_rect = pygame.Rect(col * PLAYER_WIDTH, row * PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
                player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
                if enable_collisions and player_rect.colliderect(obstacle_rect):
                    # Collision detected! Player Dies
                    pygame.quit()
            elif level_data[row][col] == 'X':
                obstacle_rect = pygame.Rect(col * PLAYER_WIDTH, row * PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
                player_rect = pygame.Rect(player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT)
                if enable_collisions and player_rect.colliderect(obstacle_rect):
                    # Collision detected! Block is solid to player
                    if player_vel_y > 0:
                        # Player is moving downward, stop vertical velocity
                        player_y = obstacle_rect.y - PLAYER_HEIGHT
                        player_vel_y = 0
                    elif player_vel_y < 0:
                        # Player is moving upward, stop vertical velocity
                        player_y = obstacle_rect.y + obstacle_rect.height
                        player_vel_y = 0

    # Fill the background color
    screen.fill(WHITE)

    # Draw the player
    pygame.draw.rect(screen, GREEN, (player_x, player_y, PLAYER_WIDTH, PLAYER_HEIGHT))

    # Draw the level
    for row in range(len(level_data)):
        for col in range(len(level_data[row])):
            if level_data[row][col] == 'B':
                pygame.draw.rect(screen, BLUE, (col * PLAYER_WIDTH, row * PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT))
            elif level_data[row][col] == 'O':
                pygame.draw.rect(screen, RED, (col * PLAYER_WIDTH, row * PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT))
            elif level_data[row][col] == 'X':
                pygame.draw.rect(screen, BLACK, (col * PLAYER_WIDTH, row * PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT))

    # Update the display
    pygame.display.flip()
    clock.tick(60)

# Quit the game
pygame.quit()
