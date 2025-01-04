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

    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)