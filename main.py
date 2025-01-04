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
def draw(window, tiles):
    window.fill(BACKGROUND_COLOR)

    for tile in tiles.values():
        tile.draw(window) 

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

class Tile:
    COLORS = [
       (237, 229, 218),
       (238, 225, 201),
       (243, 178, 122),
       (246, 150, 101),
       (247, 124, 95),
       (247, 95, 59),
       (237, 208, 115),
       (237, 204, 99),
       (236, 202, 80),
    ]

    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * TILE_WIDTH
        self.y = row * TILE_HEIGHT

    def get_color(self):
        # using log to get the index in the map to get the color of the tile based
        color_idx = int(math.log2(self.value)) - 1
        return self.COLORS[color_idx]

    def draw(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, TILE_WIDTH, TILE_HEIGHT))
        text = FONT.render(str(self.value), 1, FONT_COLOR) # creates the surface that creates the text
        window.blit(text, 
                    (self.x + (TILE_WIDTH / 2 - text.get_width() / 2), 
                    self.y + (TILE_HEIGHT / 2 - text.get_height() / 2))) # this is how you put a surface on a screen

    def move(self, delta):
        pass

    def set_position(self):
        pass

# game loop, event loop, runs constantly, checks for clicks 
def main(window):
    clock = pygame.time.Clock()
    run = True

    # key: row col
    # value: tile
    tiles = {"00": Tile(4, 0, 0), 
             "20": Tile(128, 2, 0)}

    while run:
        clock.tick(FPS) # 1 time every 60 seconds 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        draw(WINDOW, tiles)

    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)