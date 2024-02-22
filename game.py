import random
import threading
import time
import math

import pygame

from search import Graph

LEFT, RIGHT, UP, DOWN = (0, -1), (0, 1), (-1, 0), (1, 0)


class Pacman:
    SPEED = 7

    MOUTH_SPEED = 9
    LOSE_SPEED = 5
    ANGLES = {
        LEFT: (-155, 155),
        RIGHT: (25, 335),
        UP: (-65, 245),
        DOWN: (-245, 65)
    }
    OPENING = 30

    __open_close = False

    __direction = RIGHT
    next_direction = RIGHT
    __changed = True
    movement = True
    target = (0, 0)

    dots_collected = 0

    __start_angle, __end_angle = 0, 0
    way = None

    def __init__(self, screen, center, cell_width, cell_height, graph: Graph,
                 map_data, dot_count, game_on, search_loc):
        self.__screen = screen
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.pacman_loc = list(center)
        if search_loc is not None:
            self.way = graph.bfs_shortest_path(center, search_loc)
            self.way.pop(0)
        self.center = list(self.corespondent(center))
        self.map_graph = graph
        self.radius = min(cell_width, cell_height) // 1.9
        self.map_data = map_data
        self.super_power = 0
        self.dot_count = dot_count
        self.game_on = game_on
        self.speed_util = {LEFT: (-self.SPEED, 0),
                           RIGHT: (self.SPEED, 0),
                           UP: (0, -self.SPEED),
                           DOWN: (0, self.SPEED)}

    def __draw(self, draw_angle):
        points = [self.center]
        for angle in range(draw_angle[0], draw_angle[1] + 1):
            x = self.center[0] + int(self.radius * math.cos(math.radians(angle)))
            y = self.center[1] + int(self.radius * math.sin(math.radians(angle)))
            points.append((x, y))

        pygame.draw.polygon(self.__screen, (255, 255, 0), points)

    def stay(self):
        self.__draw((self.ANGLES[self.__direction][0] + self.OPENING // 8,
                     self.ANGLES[self.__direction][1] - self.OPENING // 8))

    def eat(self):
        if self.__changed:
            self.__start_angle = self.ANGLES[self.__direction][0]
            self.__end_angle = self.ANGLES[self.__direction][1]
            self.__changed = False

        if self.__end_angle > self.ANGLES[self.__direction][1] + self.OPENING / 2:
            self.__open_close = True
        if self.__end_angle < self.ANGLES[self.__direction][1] - self.OPENING / 2:
            self.__open_close = False

        self.__draw((self.__start_angle, self.__end_angle))

        if self.__open_close:
            self.__start_angle += self.MOUTH_SPEED
            self.__end_angle -= self.MOUTH_SPEED
        else:
            self.__start_angle -= self.MOUTH_SPEED
            self.__end_angle += self.MOUTH_SPEED

    def lose_animation(self):
        if self.__start_angle >= self.__end_angle:
            return
        self.__draw((self.__start_angle, self.__end_angle))

        self.__start_angle += self.LOSE_SPEED
        self.__end_angle -= self.LOSE_SPEED

    def change_direction(self, direction):
        if direction == self.__direction:
            return
        self.next_direction = direction

    def move(self):
        updated_pos = [i + j for i, j in zip(self.center, self.speed_util[self.__direction])]
        if (self.__direction in {UP, LEFT} and
            any(updated > target for updated, target in zip(updated_pos, self.target))) or \
                (self.__direction not in {UP, LEFT} and
                 any(updated < target for updated, target in zip(updated_pos, self.target))):
            self.center = updated_pos
        else:
            self.center = self.target
            self.movement = True
        self.eat()

    first = True

    def modify_map(self, position, char):
        if self.first:
            self.first = False
            return
        string_as_list = list(self.map_data[position[0]])
        string_as_list[position[1]] = char
        self.map_data[position[0]] = string_as_list

    def start_timer(self):
        while self.super_power != 0:
            self.super_power -= 1
            time.sleep(0.2)

    def check_powers(self, location):
        if self.map_data[location[0]][location[1]] == 'o':
            self.dots_collected += 1
            self.super_power = 35
            threading.Thread(target=self.start_timer).start()

    def collect_dot(self, location):
        if self.map_data[location[0]][location[1]] == '.':
            self.dots_collected += 1

    def update_by_keyboard(self):
        if not self.check_collisions(self.next_direction):
            self.__direction = self.next_direction
            self.__changed = True
        if self.check_collisions(self.__direction):
            self.stay()
            return False
        self.pacman_loc[0] += self.__direction[0]
        self.pacman_loc[1] += self.__direction[1]
        self.target = list(self.corespondent(self.pacman_loc))
        return True

    def determine_direction(self):
        if not self.way:
            return
        loc = self.way.pop(0)
        for d in (LEFT, RIGHT, UP, DOWN):
            if (self.pacman_loc[0] + d[0], self.pacman_loc[1] + d[1]) == loc:
                self.__direction = d
                self.__changed = True
                return

    def update_by_graph(self):
        self.determine_direction()
        self.pacman_loc[0] += self.__direction[0]
        self.pacman_loc[1] += self.__direction[1]
        self.target = list(self.corespondent(self.pacman_loc))

    def draw_way(self):
        for loc in self.way[:-1]:
            pygame.draw.rect(self.__screen, (150, 230, 100),
                             (loc[1] * self.cell_width, loc[0] * self.cell_height, self.cell_width, self.cell_height))

    def update(self):
        if self.dots_collected == self.dot_count:
            self.game_on[0] = False
            return
        if self.movement:
            self.collect_dot(self.pacman_loc)
            self.check_powers(self.pacman_loc)
            self.modify_map((self.pacman_loc[0] - self.__direction[0],
                             self.pacman_loc[1] - self.__direction[1]), ' ')
            self.modify_map(self.pacman_loc, 'P')

            if self.way is None:
                if not self.update_by_keyboard():
                    return
            else:
                self.update_by_graph()

            self.movement = False
        self.move()
        if self.way is not None:
            self.draw_way()

    def check_collisions(self, direction):
        return self.map_data[self.pacman_loc[0] + direction[0]][self.pacman_loc[1] + direction[1]] == '%'

    def corespondent(self, pos):
        return pygame.Rect(pos[1] * self.cell_width, pos[0] * self.cell_height,
                           self.cell_width, self.cell_height).center


class Ghost:
    location: pygame.Rect

    SPEED = 6
    __direction = RIGHT
    movement = True
    target = (0, 0)
    opposite_direction = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}
    collided_once = False
    scared = True

    def __init__(self, screen, colour, position, map_data, cell_width, cell_height, powerup, pacman, running):
        self.screen = screen
        self.map_data = map_data
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.pacman = pacman

        self.init_loc = list(position)
        self.init_pos = list(self.corespondent(self.init_loc))
        self.ghost_loc = list(position)
        self.image = self.init_image(pygame.image.load(colour), position)
        self.powerup = powerup
        self.speed_util = {LEFT: (-self.SPEED, 0),
                           RIGHT: (self.SPEED, 0),
                           UP: (0, -self.SPEED),
                           DOWN: (0, self.SPEED)}
        self.running = running

    def init_image(self, image, position):
        new_image = pygame.transform.scale(image, (self.cell_width, self.cell_height))
        self.location = new_image.get_rect()
        corespondent = self.corespondent((position[0], position[1]))
        self.location.x = corespondent[0]
        self.location.y = corespondent[1]
        return new_image

    def rebuild_speed(self, new_speed):
        self.SPEED = new_speed
        self.speed_util = {LEFT: (-self.SPEED, 0),
                           RIGHT: (self.SPEED, 0),
                           UP: (0, -self.SPEED),
                           DOWN: (0, self.SPEED)}

    def draw(self):
        if self.collided_once and self.pacman.super_power != 0:
            self.rebuild_speed(3)
            self.screen.blit(self.image, self.location)
            return
        if self.pacman.super_power == 0:
            self.rebuild_speed(3)
            self.screen.blit(self.image, self.location)
            self.scared = True
            self.collided_once = False
        else:
            self.rebuild_speed(2)
            if self.pacman.super_power > 12:
                self.screen.blit(self.powerup, self.location)
            else:
                if self.pacman.super_power % 2 != 0:
                    self.screen.blit(self.image, self.location)
                else:
                    self.screen.blit(self.powerup, self.location)

    def move(self):
        updated_pos = [i + j for i, j in zip((self.location.x, self.location.y), self.speed_util[self.__direction])]
        if (self.__direction in {UP, LEFT} and
            any(updated > target for updated, target in zip(updated_pos, self.target))) or \
                (self.__direction not in {UP, LEFT} and
                 any(updated < target for updated, target in zip(updated_pos, self.target))):

            self.location.x = updated_pos[0]
            self.location.y = updated_pos[1]
        else:
            self.location.x = self.target[0]
            self.location.y = self.target[1]
            self.movement = True
        self.draw()

    def change_direction(self):
        count = 0
        while True:
            new_direction = random.choice([LEFT, RIGHT, UP, DOWN])
            if count < 3:
                if new_direction == self.opposite_direction.get(self.__direction):
                    count += 1
                    continue
            if not self.check_collisions(new_direction):
                self.__direction = new_direction
                break

    def pacman_collision(self):
        target = self.location.center
        distance = math.sqrt((target[0] - self.pacman.center[0]) ** 2 + (target[1] - self.pacman.center[1]) ** 2)
        if distance < min(self.cell_width, self.cell_height) // 5:
            return True
        return False

    def update(self):
        if self.pacman_collision():
            if self.pacman.super_power != 0 and not self.collided_once:
                self.ghost_loc[0] = self.init_loc[0]
                self.ghost_loc[1] = self.init_loc[1]
                self.target = list(self.corespondent(self.init_loc))
                self.location[0] = self.init_pos[0]
                self.location[1] = self.init_pos[1]
                self.change_direction()
                self.collided_once = True
                return
            self.running[0] = False
            return
        if self.movement:
            if self.pacman.super_power != 0 and self.scared:
                if not self.check_collisions(self.opposite_direction[self.__direction]):
                    self.__direction = self.opposite_direction[self.__direction]
                self.scared = False
            else:
                if self.check_random_direction():
                    self.change_direction()
                if self.check_collisions(self.__direction):
                    self.change_direction()
            self.ghost_loc[0] += self.__direction[0]
            self.ghost_loc[1] += self.__direction[1]
            self.target = list(self.corespondent(self.ghost_loc))
            self.movement = False
        self.move()

    def check_random_direction(self):
        if self.__direction == UP or self.__direction == DOWN:
            return not self.check_collisions(random.choice([LEFT, RIGHT]))
        else:
            return not self.check_collisions(random.choice([UP, DOWN]))

    def check_collisions(self, direction):
        return self.map_data[self.ghost_loc[0] + direction[0]][self.ghost_loc[1] + direction[1]] == '%'

    def corespondent(self, pos):
        return pygame.Rect(pos[1] * self.cell_width, pos[0] * self.cell_height,
                           self.cell_width, self.cell_height)
