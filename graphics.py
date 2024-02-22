import pygame
import math

blue = (0, 0, 255)


class Graphics:

    @staticmethod
    def delay_pos_x(pos: pygame.Rect, wid, amount):
        return pos.center[0] + wid // 2, pos.center[1] + amount

    @staticmethod
    def delay_pos_y(pos: pygame.Rect, hei, amount):
        return pos.center[0] + amount, pos.center[1] + hei // 2

    @staticmethod
    def draw_circle(screen, location: pygame.Rect, shift_amount):
        pygame.draw.circle(screen, blue, location.center, shift_amount * 2, 2)

    @staticmethod
    def draw_horiz(screen, location: pygame.Rect, shift_amount):
        pygame.draw.line(screen, blue, Graphics.delay_pos_x(location, -location.width, shift_amount),
                         Graphics.delay_pos_x(location, location.width, shift_amount), 2)
        pygame.draw.line(screen, blue, Graphics.delay_pos_x(location, -location.width, -shift_amount),
                         Graphics.delay_pos_x(location, location.width, -shift_amount), 2)

    @staticmethod
    def draw_vert(screen, location: pygame.Rect, shift_amount):
        pygame.draw.line(screen, blue, Graphics.delay_pos_y(location, -location.height, shift_amount),
                         Graphics.delay_pos_y(location, location.height, shift_amount), 2)
        pygame.draw.line(screen, blue, Graphics.delay_pos_y(location, -location.height, -shift_amount),
                         Graphics.delay_pos_y(location, location.height, -shift_amount), 2)

    @staticmethod
    def draw_c_up(screen, location: pygame.Rect, shift_amount):
        Graphics.draw_vert(screen, pygame.Rect(location.x, location.y, location.width, location.height // 2),
                           shift_amount)
        pygame.draw.arc(screen, blue,
                        (location.center[0] - shift_amount + 1, location.center[1] - shift_amount - 2,
                         2 * shift_amount, 3 * shift_amount), math.radians(180), math.radians(360), 1)

    @staticmethod
    def draw_c_down(screen, location: pygame.Rect, shift_amount):
        Graphics.draw_vert(screen, pygame.Rect(location.x, location.center[1], location.width, location.height // 2),
                           shift_amount)
        pygame.draw.arc(screen, blue,
                        (location.center[0] - shift_amount + 1, location.center[1] - shift_amount,
                         2 * shift_amount, 3 * shift_amount), math.radians(0), math.radians(180), 1)

    @staticmethod
    def draw_c_left(screen, location: pygame.Rect, shift_amount):
        Graphics.draw_horiz(screen, pygame.Rect(location.x, location.y, location.width // 2, location.height),
                            shift_amount)
        pygame.draw.arc(screen, blue,
                        (location.center[0] - shift_amount - 3, location.center[1] - shift_amount + 1,
                         3 * shift_amount, 2 * shift_amount), math.radians(270), math.radians(90), 1)

    @staticmethod
    def draw_c_right(screen, location: pygame.Rect, shift_amount):
        Graphics.draw_horiz(screen, pygame.Rect(location.center[0], location.y, location.width // 2, location.height),
                            shift_amount)
        pygame.draw.arc(screen, blue,
                        (location.center[0] - shift_amount, location.center[1] - shift_amount + 1,
                         3 * shift_amount, 2 * shift_amount), math.radians(90), math.radians(270), 1)

    @staticmethod
    def draw_c_up_left(screen, location: pygame.Rect, shift_amount):
        Graphics.draw_horiz(screen, pygame.Rect(location.x, location.y,
                                                location.width // 2 - shift_amount, location.height), shift_amount)
        Graphics.draw_vert(screen, pygame.Rect(location.x, location.y,
                                               location.width, location.height // 2 - shift_amount), shift_amount)
        pygame.draw.line(screen, blue, (location.center[0] - shift_amount, location.center[1] + shift_amount),
                         (location.center[0] + shift_amount, location.center[1] - shift_amount), 2)

    @staticmethod
    def draw_c_up_right(screen, location: pygame.Rect, shift_amount):
        Graphics.draw_horiz(screen, pygame.Rect(location.center[0] + shift_amount, location.y,
                                                location.width // 2 - shift_amount, location.height), shift_amount)
        Graphics.draw_vert(screen, pygame.Rect(location.x, location.y,
                                               location.width, location.height // 2 - shift_amount), shift_amount)
        pygame.draw.line(screen, blue, (location.center[0] - shift_amount, location.center[1] - shift_amount),
                         (location.center[0] + shift_amount, location.center[1] + shift_amount), 2)

    @staticmethod
    def draw_c_down_left(screen, location: pygame.Rect, shift_amount):
        Graphics.draw_horiz(screen, pygame.Rect(location.x, location.y,
                                                location.width // 2 - shift_amount, location.height), shift_amount)
        Graphics.draw_vert(screen, pygame.Rect(location.x, location.center[1] + shift_amount,
                                               location.width, location.height // 2 - shift_amount), shift_amount)
        pygame.draw.line(screen, blue, (location.center[0] - shift_amount, location.center[1] - shift_amount),
                         (location.center[0] + shift_amount, location.center[1] + shift_amount), 2)

    @staticmethod
    def draw_c_down_right(screen, location: pygame.Rect, shift_amount):
        Graphics.draw_horiz(screen, pygame.Rect(location.center[0] + shift_amount, location.y,
                                                location.width // 2 - shift_amount, location.height), shift_amount)
        Graphics.draw_vert(screen, pygame.Rect(location.x, location.center[1] + shift_amount,
                                               location.width, location.height // 2 - shift_amount), shift_amount)
        pygame.draw.line(screen, blue, (location.center[0] - shift_amount, location.center[1] + shift_amount),
                         (location.center[0] + shift_amount, location.center[1] - shift_amount), 2)

    @staticmethod
    def draw_t_up(screen, location: pygame.Rect, shift_amount):
        pygame.draw.line(screen, blue, (location.x, location.center[1] + shift_amount),
                         (location.x + location.width, location.center[1] + shift_amount), 2)
        pygame.draw.line(screen, blue, (location.x, location.center[1] - shift_amount),
                         (location.center[0] - shift_amount, location.center[1] - shift_amount), 2)
        pygame.draw.line(screen, blue, (location.center[0] + shift_amount, location.center[1] - shift_amount),
                         (location.x + location.width, location.center[1] - shift_amount), 2)
        Graphics.draw_vert(screen, pygame.Rect(location.x, location.y,
                                               location.width, (location.height // 2) - shift_amount), shift_amount)

    @staticmethod
    def draw_t_down(screen, location: pygame.Rect, shift_amount):
        pygame.draw.line(screen, blue, (location.x, location.center[1] - shift_amount),
                         (location.x + location.width, location.center[1] - shift_amount), 2)
        pygame.draw.line(screen, blue, (location.x, location.center[1] + shift_amount),
                         (location.center[0] - shift_amount, location.center[1] + shift_amount), 2)
        pygame.draw.line(screen, blue, (location.center[0] + shift_amount, location.center[1] + shift_amount),
                         (location.x + location.width, location.center[1] + shift_amount), 2)
        Graphics.draw_vert(screen, pygame.Rect(location.x, location.center[1] + shift_amount,
                                               location.width, (location.height // 2) - shift_amount), shift_amount)

    @staticmethod
    def draw_t_left(screen, location: pygame.Rect, shift_amount):
        pygame.draw.line(screen, blue, (location.center[0] + shift_amount, location.y),
                         (location.center[0] + shift_amount, location.y + location.height), 2)
        pygame.draw.line(screen, blue, (location.center[0] - shift_amount, location.y),
                         (location.center[0] - shift_amount, location.center[1] - shift_amount), 2)
        pygame.draw.line(screen, blue, (location.center[0] - shift_amount, location.center[1] + shift_amount),
                         (location.center[0] - shift_amount, location.y + location.height), 2)
        Graphics.draw_horiz(screen, pygame.Rect(location.center[0] - (4 * shift_amount), location.y,
                                                (location.width // 2) - shift_amount, location.height), shift_amount)

    @staticmethod
    def draw_t_right(screen, location: pygame.Rect, shift_amount):
        pygame.draw.line(screen, blue, (location.center[0] - shift_amount, location.y),
                         (location.center[0] - shift_amount, location.y + location.height), 2)
        pygame.draw.line(screen, blue, (location.center[0] + shift_amount, location.y),
                         (location.center[0] + shift_amount, location.center[1] - shift_amount), 2)
        pygame.draw.line(screen, blue, (location.center[0] + shift_amount, location.center[1] + shift_amount),
                         (location.center[0] + shift_amount, location.y + location.height), 2)
        Graphics.draw_horiz(screen, pygame.Rect(location.center[0] + shift_amount, location.y,
                                                (location.width // 2) - shift_amount, location.height), shift_amount)

    @staticmethod
    def draw_cross(screen, location: pygame.Rect, shift_amount):
        Graphics.draw_vert(screen, pygame.Rect(location.x, location.y,
                                               location.width, (location.height // 2) - shift_amount), shift_amount)
        Graphics.draw_vert(screen, pygame.Rect(location.x, location.center[1] + shift_amount,
                                               location.width, (location.height // 2) - shift_amount), shift_amount)
        Graphics.draw_horiz(screen, pygame.Rect(location.center[0] - (4 * shift_amount), location.y,
                                                (location.width // 2) - shift_amount, location.height), shift_amount)
        Graphics.draw_horiz(screen, pygame.Rect(location.center[0] + shift_amount, location.y,
                                                (location.width // 2) - shift_amount, location.height), shift_amount)
