import pygame
import sys
from ship import Ship
from island import Island

# NEW: import serial library, install pyserial first
import serial
########################
TILE_SIZE = 64
WINDOW_SIZE = 15 * TILE_SIZE
pygame.init()

screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
water = pygame.image.load("assets/water_tile.png")
water_rect = water.get_rect()
screen_rect = screen.get_rect()

# add an island to the center of the screen
island = Island(screen_rect.center)

# add a ship
ship_red = Ship()  # ship is now an object that *has* a surface
ship_blue = Ship()

game_objects = pygame.sprite.Group()
game_objects.add(island, ship_red, ship_blue)

num_tiles = screen_rect.width // water_rect.width

# same size as the screen
background = pygame.surface.Surface((screen_rect.width,
                                     screen_rect.height))
# screen is square so same number of tiles in row and col
for y in range(num_tiles):
    for x in range(num_tiles):
        background.blit(water, (x * water_rect.width, y * water_rect.height))

# NEW: add serial connection to PICO
pico = serial.Serial("COM21")
####################################

coordinate_red = (0, 0)
coordinate_blue = (0, 0)

clock = pygame.time.Clock()
while True:

    ###############################################
    #  NEW: check serial for new ship coordinate
    pico.write("\n".encode())
    red_x, red_y, blue_x, blue_y = pico.readline().strip().decode().split(',')
    if (red_x, red_y) != ('-1', '-1'):
        x_coord_red = int(int(red_x) / 316 * WINDOW_SIZE)
        y_coord_red = int(int(red_y) / 208 * WINDOW_SIZE)
        coordinate_red = (WINDOW_SIZE - x_coord_red, y_coord_red)
    if (blue_x, blue_y) != ('-1', '-1'):
        x_coord_blue = int(int(blue_x) / 316 * WINDOW_SIZE)
        y_coord_blue = int(int(blue_y) / 208 * WINDOW_SIZE)
        coordinate_blue = (WINDOW_SIZE - x_coord_blue, y_coord_blue)
    ###############################################

    # check for user input (key press, mouse clicks, joystick)
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            print("BOOM!")
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.K_q:
            sys.exit()

    # update game objects
    ship_red.move(coordinate_red)
    ship_blue.move(coordinate_blue)
    game_objects.update()
    collision = pygame.sprite.collide_rect(ship_red, island)
    if collision:
        ship_red.health = ship_red.health - 1
        # print(f"Collision: ship health={ship.health}!!")

    # draw the screen
    screen.blit(background, (0, 0))
    game_objects.draw(screen)
    pygame.display.flip()
    clock.tick(60)
