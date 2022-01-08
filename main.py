from pygame.math import Vector2 as vector 
import sys, pygame
from helper import *
from pacman import *
from ghost import *


class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()
        self.is_game_launched = True
        self.state = 'menu'
        self.walls = []
        self.points = []
        self.ghosts = []
        self.ghost_coordinates = []
        self.pacman_coordinate = None
        self.read_txt()
        self.Pacman = Pacman(self, vector(self.pacman_coordinate))
        self.create_ghosts()
        

    def run_game(self):
        while self.is_game_launched:
            if self.state == 'menu':
                self.menu_events()
                self.menu_display()
            elif self.state == 'game':
                self.game_events()
                self.game_update()
                self.game_display()
            elif self.state == 'result':
                self.result_events()
                self.result_display()
            elif self.state == 'next':
                self.next_events()
                self.next_draw()
            else:
                self.is_game_launched = False
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()


    def read_txt(self):
        self.background = pygame.image.load('images/background.jpg')
        self.background = pygame.transform.scale(self.background, (MAP_WIDTH, MAP_HEIGHT))
        with open("maze.txt", 'r') as file:
            for yIndex, line in enumerate(file):
                for xIndex, sign in enumerate(line):
                    if sign == "w":
                        self.walls.append(vector(xIndex, yIndex))
                    elif sign == "p":
                        self.points.append(vector(xIndex, yIndex))
                    elif sign == "X":
                        self.pacman_coordinate = [xIndex, yIndex]
                    elif sign in ["1", "2", "3", "4"]:
                        self.ghost_coordinates.append([xIndex, yIndex])

    def display_lines(self):
        for x in range(WINDOW_WIDTH // SQUARE_WIDTH):
            pygame.draw.line(self.background, LINES_COLOR, (x * SQUARE_WIDTH, 0), (x * SQUARE_WIDTH, WINDOW_HEIGHT))
        for y in range(WINDOW_HEIGHT // SQUARE_HEIGHT):
            pygame.draw.line(self.background, LINES_COLOR, (0, y * SQUARE_HEIGHT), (WINDOW_WIDTH, y * SQUARE_HEIGHT))

    def display_walls(self):
        for wall in self.walls:
            pygame.draw.rect(self.background, GAME_WALLS_COLOR, (wall.x * SQUARE_WIDTH, wall.y * SQUARE_HEIGHT, SQUARE_WIDTH, SQUARE_HEIGHT))

    def display_text(self, words, screen, position, size, COLOR, fontName, centered = False):
        font = pygame.font.SysFont(fontName, size)
        text = font.render(words, False, COLOR)
        textSize = text.get_size()
        if centered:
            position[0] = position[0] - textSize[0] // 2
            position[1] = position[1] - textSize[1] // 2
        screen.blit(text, position)

    def create_ghosts(self):
        for index, position in enumerate(self.ghost_coordinates):
            self.ghosts.append(Ghost(self, vector(position)))

    def reboot(self):
        self.background = pygame.image.load('images/background.jpg')
        self.background = pygame.transform.scale(self.background, (MAP_WIDTH, MAP_HEIGHT))
        self.Pacman.lives = 3
        self.Pacman.grid_coordinate = vector(self.Pacman.starting_coordinate)
        self.Pacman.pixel_coordinate = self.Pacman.get_pixel_coordinate()
        self.Pacman.direction *= 0
        for ghost in self.ghosts:
            ghost.grid_coordinate = vector(ghost.starting_coordinate)
            ghost.pixel_coordinate = ghost.get_pixel_coordinate()
            ghost.direction *= 0

        self.walls = []
        self.points = []
        self.ghost_coordinates = []
        self.pacman_coordinate = None
        with open("maze.txt", 'r') as file:
            for yIndex, line in enumerate(file):
                for xIndex, sign in enumerate(line):
                    if sign == "w":
                        self.walls.append(vector(xIndex, yIndex))
                    elif sign == "p":
                        self.points.append(vector(xIndex, yIndex))
                    elif sign == "U":
                        self.pacman_coordinate = [xIndex, yIndex]
                    elif sign in ["2", "3", "4", "5"]:
                        self.ghost_coordinates.append([xIndex, yIndex])
        self.state = "game"


    ########## MENU STATE ##########


    def menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.is_game_launched = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.state = 'game'

    def menu_display(self):
        self.screen.fill(MENU_BACKGROUND_COLOR)
        self.display_text(PLAY_AGAIN_TEXT, self.screen, [
                       WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - INDENT], menu_TEXT_SIZE, MENU_TEXT_COLOR, menu_FONT, centered = True)
        self.display_text(EXIT_TEXT, self.screen, [
                       WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + INDENT], menu_TEXT_SIZE, MENU_TEXT_COLOR, menu_FONT, centered = True)
        pygame.display.update()


    ########## GAME STATE ##########


    def game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_game_launched = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.Pacman.move(vector(-1, 0))
                if event.key == pygame.K_RIGHT:
                    self.Pacman.move(vector(1, 0))
                if event.key == pygame.K_UP:
                    self.Pacman.move(vector(0, -1))
                if event.key == pygame.K_DOWN:
                    self.Pacman.move(vector(0, 1))
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.is_game_launched = False

    def game_update(self):
        self.Pacman.updatePacman()
        for ghost in self.ghosts:
            ghost.update_ghost()
        for ghost in self.ghosts:
            if ghost.grid_coordinate == self.Pacman.grid_coordinate:
                self.delete_life()

    def game_display(self):
        self.screen.fill(GAME_BACKGROUND_COLOR)
        self.screen.blit(self.background, (INDENT // 2, INDENT // 2))
        self.display_lines()
        self.display_walls()
        self.draw_points()
        self.display_text(f'SCORE: {self.Pacman.score}', self.screen, [280, 0], 18, GAME_SCORE_COLOR, menu_FONT)
        self.Pacman.display_pacman()
        self.Pacman.display_lives()
        for ghost in self.ghosts:
            ghost.display_ghost()
        pygame.display.update()

    def delete_life(self):
        self.Pacman.lives -= 1
        if self.Pacman.lives == 0:
            self.Pacman.score = 0
            self.state = "result"          
        else:
            self.Pacman.grid_coordinate = vector(self.Pacman.starting_coordinate)
            self.Pacman.pixel_coordinate = self.Pacman.get_pixel_coordinate()
            self.Pacman.direction *= 0

            for ghost in self.ghosts:
                ghost.grid_coordinate = vector(ghost.starting_coordinate)
                ghost.pixel_coordinate = ghost.get_pixel_coordinate()
                ghost.direction *= 0

    def draw_points(self):
        for point in self.points:
            pygame.draw.circle(self.screen, GAME_POINT_COLOR, (int(point.x * SQUARE_WIDTH) + SQUARE_WIDTH // 2 + HALF_INDENT, int(point.y * SQUARE_HEIGHT) + SQUARE_HEIGHT // 2 + HALF_INDENT), 5)


    ########## RESULT STATE ##########


    def result_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.is_game_launched = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                self.reboot()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.is_game_launched = False

    def result_display(self):
        self.screen.fill(RESULT_BACKGROUND_COLOR)
        self.display_text("You lose", self.screen, [WINDOW_WIDTH//2, 100],  52, RESULT_TEXT_COLOR, "arial", centered = True)
        self.display_text(PLAY_AGAIN_TEXT, self.screen, [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2],  36, (190, 190, 190), "arial", centered = True)
        self.display_text(EXIT_TEXT, self.screen, [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 1.5],  36, (190, 190, 190), "arial", centered = True)
        pygame.display.update()


    ########## NEXT STATE ##########


    def next_events(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.is_game_launched = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    self.reboot()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    self.is_game_launched = False

    def next_draw(self):
        self.screen.fill(RESULT_BACKGROUND_COLOR)
        self.display_text("Level passed", self.screen, [WINDOW_WIDTH//2, 100],  52, RESULT_TEXT_COLOR, "arial", centered = True)
        self.display_text(PLAY_NEXT_LEVEL_TEXT, self.screen, [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2],  36, (190, 190, 190), "arial", centered = True)
        self.display_text(EXIT_TEXT, self.screen, [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 1.5],  36, (190, 190, 190), "arial", centered = True)
        pygame.display.update()


pygame.init()
game = Game()
game.run_game()