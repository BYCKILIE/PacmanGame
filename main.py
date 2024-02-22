import sys

from game import *
from map import Map

CELL_WIDTH = 25
CELL_HEIGHT = 25

MAP_PATH = "layouts/mediumClassic.lay"
SEARCH = False

ghost_colours = ["assets/blue.png", "assets/orange.png", "assets/pink.png", "assets/red.png"]


def get_random_colour():
    colour = ghost_colours[random.randint(0, len(ghost_colours) - 1)]
    ghost_colours.remove(colour)
    return colour


def powerup_ghost():
    return pygame.transform.scale(pygame.image.load("assets/powerup.png"), (CELL_WIDTH, CELL_HEIGHT))


def read_map():
    file = open(MAP_PATH, "r")
    map_data = [i.strip() for i in file.readlines()]
    file.close()
    return map_data


def key_callback(pacman: Pacman):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        pacman.change_direction(UP)
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        pacman.change_direction(DOWN)
    if keys[pygame.K_a] or keys[pygame.K_LEFT]:
        pacman.change_direction(LEFT)
    if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
        pacman.change_direction(RIGHT)


def main():
    map_data = read_map()

    pygame.init()

    width, height = len(map_data[0]) * CELL_WIDTH, len(map_data) * CELL_HEIGHT
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Pacman")

    clock = pygame.time.Clock()

    screen.fill((0, 0, 0))

    pygame.display.set_icon(pygame.image.load("assets/logo.png"))

    game_on = [True]

    powerup = powerup_ghost()
    map_ = Map(screen, map_data, CELL_WIDTH, CELL_HEIGHT, SEARCH)
    pacman = Pacman(screen, map_.pacman_location, CELL_WIDTH, CELL_HEIGHT,
                    map_.map_graph, map_data, map_.dot_count, game_on, map_.search_location)
    ghosts = [Ghost(screen, get_random_colour(), i, map_data, CELL_WIDTH, CELL_HEIGHT, powerup, pacman, game_on)
              for i in map_.ghosts]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        screen.fill((0, 0, 0))
        map_.draw_map()

        key_callback(pacman)

        if game_on[0]:
            pacman.update()
            for ghost in ghosts:
                ghost.update()
        else:
            pacman.lose_animation()

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
