import threading

import pygame

from graphics import Graphics
from search import Graph

(VERT, HORIZ,  # done
 C_UP_LEFT, C_UP_RIGHT, C_DOWN_LEFT, C_DOWN_RIGHT,  # done
 C_UP, C_DOWN, C_LEFT, C_RIGHT,  # done
 T_UP, T_DOWN,  # done
 T_LEFT, T_RIGHT,
 SKIP, CIRCLE, CROSS) \
    = 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 14, 15, 16, 17


class Map:
    shapes = []
    ghosts = []
    dot_count = 0
    search_location = None
    pacman_location = None

    def __init__(self, screen, map_data, cell_width, cell_height, search):
        self.screen = screen
        self.map_data = map_data
        self.cell_width = cell_width
        self.cell_height = cell_height
        self.search = search

        self.shift_amount = (self.cell_width * self.cell_height) // (3.5 * (self.cell_width + self.cell_height))
        self.map_graph = Graph()

        self.build_map()
        self.build_graph()

    def build_graph(self):
        for row, line in enumerate(self.map_data):
            for col, char in enumerate(line):
                if (row, col) in self.map_graph.graph:
                    if col > 0:
                        if (row, col - 1) in self.map_graph.graph:
                            self.map_graph.add_edge((row, col), (row, col - 1))
                    if row > 0:
                        if (row - 1, col) in self.map_graph.graph:
                            self.map_graph.add_edge((row, col), (row - 1, col))

    def get_shape(self, row, col):
        neighbors = {"UP": False, "DOWN": False, "LEFT": False, "RIGHT": False,
                     'CUL': False, 'CUR': False, 'CDL': False, 'CDR': False}
        rows, cols = len(self.map_data), len(self.map_data[0])
        directions = {"UP": (row - 1, col), "DOWN": (row + 1, col), "LEFT": (row, col - 1), "RIGHT": (row, col + 1),
                      'CUL': (row - 1, col - 1), 'CUR': (row - 1, col + 1),
                      'CDL': (row + 1, col - 1), 'CDR': (row + 1, col + 1)}

        for direction, (r, c) in directions.items():
            if 0 <= r < rows and 0 <= c < cols:
                if self.map_data[r][c] == '%':
                    neighbors[direction] = True

        if list(neighbors.values()).count(True) == len(neighbors.values()):
            return SKIP

        c_count = [neighbors['CUL'], neighbors['CUR'], neighbors['CDL'], neighbors['CDR']].count(True)

        if c_count == 4:
            if neighbors['UP'] and neighbors['DOWN']:
                return VERT
            if neighbors['LEFT'] and neighbors['RIGHT']:
                return HORIZ

        if c_count == 3:
            if not neighbors['CUL'] and (neighbors['UP'] and neighbors['LEFT']):
                return C_UP_LEFT
            if not neighbors['CUR'] and (neighbors['UP'] and neighbors['RIGHT']):
                return C_UP_RIGHT
            if not neighbors['CDL'] and (neighbors['DOWN'] and neighbors['LEFT']):
                return C_DOWN_LEFT
            if not neighbors['CDR'] and (neighbors['DOWN'] and neighbors['RIGHT']):
                return C_DOWN_RIGHT

        if (((neighbors['CUL'] and neighbors['CUR']) or (neighbors['CDL'] and neighbors['CDR'])) and
                (neighbors['LEFT'] and neighbors['RIGHT'])):
            return HORIZ

        if (((neighbors['CUL'] and neighbors['CDL']) or (neighbors['CUR'] and neighbors['CDR'])) and
                (neighbors['UP'] and neighbors['DOWN'])):
            return VERT

        if neighbors["UP"]:
            if neighbors["DOWN"]:
                if neighbors['LEFT']:
                    if neighbors['RIGHT']:
                        return CROSS
                    return T_LEFT
                if neighbors['RIGHT']:
                    return T_RIGHT
                return VERT
            if neighbors["LEFT"]:
                if neighbors["RIGHT"]:
                    return T_UP
                return C_UP_LEFT
            if neighbors["RIGHT"]:
                return C_UP_RIGHT
            return C_UP

        if neighbors["DOWN"]:
            if neighbors["LEFT"] and neighbors["RIGHT"]:
                return T_DOWN
            if neighbors["LEFT"]:
                return C_DOWN_LEFT
            if neighbors["RIGHT"]:
                return C_DOWN_RIGHT
            return C_DOWN

        if neighbors["LEFT"]:
            if neighbors["UP"] and neighbors["DOWN"]:
                return T_LEFT
            if neighbors["RIGHT"]:
                return HORIZ
            return C_LEFT

        if neighbors["RIGHT"]:
            if neighbors["UP"] and neighbors["DOWN"]:
                return T_RIGHT
            return C_RIGHT

        return CIRCLE

    def build_map(self):
        for row, line in enumerate(self.map_data):
            shapes_util = {}
            for col, char in enumerate(line):
                if char == "%":
                    shape = self.get_shape(row, col)
                    if shape == SKIP:
                        shapes_util[col] = None
                    elif shape == VERT:
                        shapes_util[col] = Graphics.draw_vert
                    elif shape == HORIZ:
                        shapes_util[col] = Graphics.draw_horiz
                    elif shape == C_UP:
                        shapes_util[col] = Graphics.draw_c_up
                    elif shape == C_DOWN:
                        shapes_util[col] = Graphics.draw_c_down
                    elif shape == C_LEFT:
                        shapes_util[col] = Graphics.draw_c_left
                    elif shape == C_RIGHT:
                        shapes_util[col] = Graphics.draw_c_right
                    elif shape == C_UP_LEFT:
                        shapes_util[col] = Graphics.draw_c_up_left
                    elif shape == C_UP_RIGHT:
                        shapes_util[col] = Graphics.draw_c_up_right
                    elif shape == C_DOWN_LEFT:
                        shapes_util[col] = Graphics.draw_c_down_left
                    elif shape == C_DOWN_RIGHT:
                        shapes_util[col] = Graphics.draw_c_down_right
                    elif shape == T_UP:
                        shapes_util[col] = Graphics.draw_t_up
                    elif shape == T_DOWN:
                        shapes_util[col] = Graphics.draw_t_down
                    elif shape == T_LEFT:
                        shapes_util[col] = Graphics.draw_t_left
                    elif shape == T_RIGHT:
                        shapes_util[col] = Graphics.draw_t_right
                    elif shape == CIRCLE:
                        shapes_util[col] = Graphics.draw_circle
                    elif shape == CROSS:
                        shapes_util[col] = Graphics.draw_cross
                else:
                    self.map_graph.add_vertex((row, col))
                if char == 'P':
                    self.pacman_location = (row, col)
                if char == 'G':
                    self.ghosts.append((row, col))
                if char == '.':
                    if self.search:
                        self.search_location = (row, col)
                    self.dot_count += 1
                if char == 'o':
                    self.dot_count += 1

            self.shapes.append(shapes_util)

    def draw_map(self):
        map_threads = [
            threading.Thread(target=self.draw_map_util, daemon=True, args=(
                0,
                0,
                len(self.map_data) // 2,
                len(self.map_data[0]) // 2
            )),
            threading.Thread(target=self.draw_map_util, daemon=True, args=(
                0,
                len(self.map_data[0]) // 2,
                len(self.map_data) // 2,
                len(self.map_data[0])
            )),
            threading.Thread(target=self.draw_map_util, daemon=True, args=(
                len(self.map_data) // 2,
                0,
                len(self.map_data),
                len(self.map_data[0]) // 2
            )),
            threading.Thread(target=self.draw_map_util, daemon=True, args=(
                len(self.map_data) // 2,
                len(self.map_data[0]) // 2,
                len(self.map_data),
                len(self.map_data[0])
            ))
        ]
        for th in map_threads:
            th.start()
        for th in map_threads:
            th.join()

    def draw_map_util(self, si, sj, ei, ej):
        for row in range(si, ei):
            for col in range(sj, ej):
                rect = pygame.Rect(col * self.cell_width, row * self.cell_height, self.cell_width, self.cell_height)
                if self.map_data[row][col] == "%" and self.shapes[row][col] is not None:
                    self.shapes[row][col](self.screen, rect, self.shift_amount)
                if self.map_data[row][col] == ".":
                    pygame.draw.circle(self.screen, (255, 255, 255), rect.center, self.cell_width // 8)
                elif self.map_data[row][col] == "o":
                    pygame.draw.circle(self.screen, (255, 255, 255), rect.center, self.cell_width // 4)
