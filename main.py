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
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)
FONT = pygame.font.SysFont("calibri", 60, bold = True)
MOVE_SPEED = 20

# pygame has a window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

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
                    self.y + (TILE_HEIGHT / 2 - text.get_height() / 2),),) # this is how you put a surface on a screen

    def set_position(self, ceil=False):
        if ceil: 
            self.row = math.ceil(self.y / TILE_HEIGHT)
            self.col = math.ceil(self.x / TILE_WIDTH)
        else:
            self.row = math.floor(self.y / TILE_HEIGHT)
            self.col = math.floor(self.x / TILE_WIDTH)

    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]

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


# helper method to look for a random EMPTY space
def get_random_position(tiles):
    row = None
    col = None

    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLUMNS)

        if f"{row}-{col}" not in tiles: 
            break

    return row, col

def move_tiles(window, tiles, clock, direction):
    updated = True
    blocks = set()      # which tiles have already been merged 
    
    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-MOVE_SPEED, 0)
        bound_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}-{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_SPEED
        move_check = (
            lambda tile, next_tile: tile.x > next_tile.x + TILE_WIDTH + MOVE_SPEED
        )
        ceil = True
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_SPEED, 0)
        bound_check = lambda tile: tile.col == COLUMNS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}-{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_SPEED
        move_check = (
            lambda tile, next_tile: tile.x + TILE_WIDTH + MOVE_SPEED < next_tile.x
        )
        ceil = False
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_SPEED)
        bound_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}-{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_SPEED
        move_check = (
            lambda tile, next_tile: tile.y > next_tile.y + TILE_HEIGHT + MOVE_SPEED
        )
        ceil = True
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, MOVE_SPEED)
        bound_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}-{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_SPEED
        move_check = (
            lambda tile, next_tile: tile.y + TILE_HEIGHT + MOVE_SPEED < next_tile.y
        )
        ceil = False

    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)
        for i, tile in enumerate(sorted_tiles):
            if bound_check(tile):
                continue 

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            # if the two tiles together are the same and it hasnt been merged, then continue
            elif (tile.value == next_tile.value and tile not in blocks and next_tile not in blocks):
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue

            tile.set_position(ceil)
            updated = True
        
        update_tiles(window, tiles, sorted_tiles)
    return end_moves(tiles)
 
def end_moves(tiles):
    if len(tiles) == 16:
        return "lost"
    
    row, col = get_random_position(tiles)
    tiles["f{row}-{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"

# helper method to update the tiles after they have been moved
def update_tiles(window, tiles, sorted_tiles):
    tiles.clear()
    for tile in sorted_tiles:
        tiles[f"{tile.row}-{tile.col}"] = tile
    
    draw(window, tiles)

# helper method to start the game with 2 random tiles on screen
def generate_tiles():
    # key: row col
    # value: tile
    tiles = {}

    for _ in range(2):
        row, col = get_random_position(tiles)
        tiles[f"{row}-{col}"] = Tile(2, row, col)

    return tiles

# game loop, event loop, runs constantly, checks for clicks 
def main(window):
    clock = pygame.time.Clock()
    run = True

    tiles = generate_tiles()
    
    while run:
        clock.tick(FPS) # 1 time every 60 seconds 

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_tiles(window, tiles, clock, "left")
                if event.key == pygame.K_RIGHT:
                    move_tiles(window, tiles, clock, "right")
                if event.key == pygame.K_UP:
                    move_tiles(window, tiles, clock, "up")
                if event.key == pygame.K_DOWN:
                    move_tiles(window, tiles, clock, "down")

        draw(window, tiles)

    pygame.quit()

if __name__ == "__main__":
    main(WINDOW)