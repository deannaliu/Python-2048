import pygame
import random
import math 

pygame.init()

# CONSTANTS
FPS = 60                    # SPEED
WIDTH, HEIGHT = 800, 800    # FRAME
ROWS, COLUMNS = 4, 4        # GRID

TILE_HEIGHT = HEIGHT // ROWS 
TILE_WIDTH = WIDTH // COLUMNS

OUTLINE_COLOR = (187, 173, 160) # RGB (255, 255, 255)
OUTLINE_THICKNESS = 8
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)
FONT = pygame.font.SysFont("calibri", 60, bold = True)
MOVE_SPEED = 30

# pygame has a window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

# paint / drawing events in the order of the code
def draw(window):
    window.fill(BACKGROUND_COLOR)
    draw_grid(window)
    pygame.display.update()

# helper method to draw the grid
def draw_grid(window):
    for row in range(1, ROWS):
        y = row * TILE_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)
    
    for col in range(1, COLUMNS):
        x = col * TILE_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)


# game loop, event loop, runs constantly, checks for clicks 
def main(window):
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS) # 1 time every 60 seconds 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(WINDOW)

    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)