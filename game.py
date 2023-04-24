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
ship = Ship()  # ship is now an object that *has* a surface

game_objects = pygame.sprite.Group()
game_objects.add(island, ship)

num_tiles = screen_rect.width // water_rect.width

# same size as the screen
background = pygame.surface.Surface((screen_rect.width,
                                     screen_rect.height))
# screen is square so same number of tiles in row and col
for y in range(num_tiles):
    for x in range(num_tiles):
        background.blit(water, (x * water_rect.width, y * water_rect.height))

# NEW: add serial connection to PICO
pico = serial.Serial("COM19")
####################################

coordinate = (0, 0)

clock = pygame.time.Clock()
while True:

    ###############################################
    #  NEW: check serial for new ship coordinate
    pico.write("\n".encode())
    x, y = pico.readline().strip().decode().split(',')
    if (x, y) != ('-1', '-1'):
        x_coord = int(int(x) / 316 * WINDOW_SIZE)
        y_coord = int(int(y) / 208 * WINDOW_SIZE)
        coordinate = x_coord, y_coord
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
    ship.move(coordinate)
    game_objects.update()
    collision = pygame.sprite.collide_rect(ship, island)
    if collision:
        ship.health = ship.health - 1
        # print(f"Collision: ship health={ship.health}!!")

    # draw the screen
    screen.blit(background, (0, 0))
    game_objects.draw(screen)
    pygame.display.flip()
    clock.tick(60)
