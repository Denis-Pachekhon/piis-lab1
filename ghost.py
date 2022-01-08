import pygame, random
from helper import *
from pygame.math import Vector2 as vec 

class Ghost:
    def __init__(self, game, position):
        self.game = game
        self.grid_coordinate = position
        self.type = type
        self.direction = vec(0, 0)
        self.pixel_coordinate = self.get_pixel_coordinate()
        self.starting_coordinate = [position.x, position.y]
        self.target = None

    def get_pixel_coordinate(self):
        return vec((self.grid_coordinate.x * SQUARE_WIDTH) + HALF_INDENT + SQUARE_WIDTH // 2, (self.grid_coordinate.y * SQUARE_HEIGHT) + HALF_INDENT + SQUARE_HEIGHT // 2)

    def update_ghost(self):
        self.target = self.game.Pacman.grid_coordinate
        if self.target != self.grid_coordinate:   
            self.pixel_coordinate += self.direction
            if self.is_time_to_move():
                self.move()
        self.grid_coords_to_pixel_coords()

    def grid_coords_to_pixel_coords(self):
        self.grid_coordinate[0] = (self.pixel_coordinate[0] - INDENT + SQUARE_WIDTH // 2) // SQUARE_WIDTH + 1
        self.grid_coordinate[1] = (self.pixel_coordinate[1] - INDENT + SQUARE_HEIGHT // 2) // SQUARE_HEIGHT + 1

    def display_ghost(self):
        self.player_image = pygame.image.load('images/ghost.png')
        self.player_image = pygame.transform.scale(self.player_image, (SQUARE_WIDTH, SQUARE_HEIGHT))
        self.game.screen.blit(self.player_image, (int(self.pixel_coordinate.x - INDENT // 5),int(self.pixel_coordinate.y - INDENT // 5)))    

    def is_time_to_move(self):
        if int(self.pixel_coordinate.x + INDENT // 2) % SQUARE_WIDTH == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pixel_coordinate.y + INDENT // 2) % SQUARE_HEIGHT == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True
        return False

    def move(self):
        self.direction = self.get_random_direction()

    def get_random_direction(self):
        while True:
            randomDigit = random.randint(0, 4) 
            if randomDigit == 0:
                x, y = 1, 0
            elif randomDigit == 1:
                x, y = 0, 1
            elif randomDigit == 2:
                x, y = -1, 0
            else:
                x, y = 0, -1

            nextCoordinate = vec(self.grid_coordinate.x + x, self.grid_coordinate.y + y)
            if nextCoordinate not in self.game.walls:
                break
        return vec(x, y)