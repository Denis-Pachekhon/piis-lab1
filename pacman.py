import pygame
from helper import *
from pygame.math import Vector2 as vec 

class Pacman:
    def __init__(self, game, position):
        self.game = game
        self.grid_coordinate = position
        self.starting_coordinate = [position.x, position.y]
        self.pixel_coordinate = self.get_pixel_coordinate() #vec
        self.direction = vec(0, 0) # vec
        self.is_able_to_move = True
        self.lives = 3
        self.score = 0
        self.saved_direction = None
        self.speed = 2

    def updatePacman(self):
        if self.is_able_to_move:
            self.pixel_coordinate += self.direction * self.speed
        if self.is_time_to_move():
            if self.saved_direction != None:
                self.direction = self.saved_direction
            self.is_able_to_move = self.can_move()
        self.grid_coords_to_pixel_coords()
        if self.on_point():
            self.take_point()
    
    def grid_coords_to_pixel_coords(self):
        self.grid_coordinate[0] = (self.pixel_coordinate[0] + SQUARE_WIDTH // 2 - INDENT) // SQUARE_WIDTH + 1
        self.grid_coordinate[1] = (self.pixel_coordinate[1] + SQUARE_HEIGHT // 2 - INDENT) // SQUARE_HEIGHT + 1

    def display_pacman(self):
        self.player_image = pygame.image.load('images/pacman.png')
        if self.direction == vec(0, -1):
            self.player_image = pygame.transform.rotate(self.player_image, 90)
        if self.direction == vec(0, 1):
            self.player_image = pygame.transform.rotate(self.player_image, -90)
        if self.direction == vec(-1, 0):
            self.player_image = pygame.transform.flip(self.player_image, 1, 0)
        
        self.player_image = pygame.transform.scale(self.player_image, (SQUARE_WIDTH, SQUARE_HEIGHT))
        self.game.screen.blit(self.player_image, (int(self.pixel_coordinate.x - INDENT // 5), int(self.pixel_coordinate.y - INDENT // 5)))


    def display_lives(self):
        for x in range(self.lives):
            self.game.screen.blit(self.player_image, (30 + 20 * x, WINDOW_HEIGHT - 23))

    def on_point(self): 
        if self.grid_coordinate in self.game.points:
            if int(self.pixel_coordinate.x + INDENT // 2) % SQUARE_WIDTH == 0:
                if self.direction == vec(1, 0) or self.direction == vec(-1, 0):
                    return True
            if int(self.pixel_coordinate.y + INDENT // 2) % SQUARE_HEIGHT == 0:
                if self.direction == vec(0, 1) or self.direction == vec(0, -1):
                    return True
        return False

    def take_point(self):
        self.game.points.remove(self.grid_coordinate)
        self.score += 1
        if len(self.game.points) == 0:
            self.game.state = 'next'

    def move(self, direction):
        self.saved_direction = direction

    def get_pixel_coordinate(self):
        return vec((self.grid_coordinate[0] * SQUARE_WIDTH) + HALF_INDENT + SQUARE_WIDTH // 2, (self.grid_coordinate[1] * SQUARE_HEIGHT) + HALF_INDENT + SQUARE_HEIGHT // 2)

    def is_time_to_move(self):
        if int(self.pixel_coordinate.x + HALF_INDENT) % SQUARE_WIDTH == 0:
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0) or self.direction == vec(0, 0):
                return True
        if int(self.pixel_coordinate.y + HALF_INDENT) % SQUARE_HEIGHT == 0:
            if self.direction == vec(0, 1) or self.direction == vec(0, -1) or self.direction == vec(0, 0):
                return True

    def can_move(self):
        for wall in self.game.walls:
            if vec(self.grid_coordinate + self.direction) == wall:
                return False
        return True