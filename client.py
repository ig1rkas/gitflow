import pygame
import socket
import pickle

from config import *
from math import *
from pprint import pprint


class Menu():
    def __init__(self) -> None:
        pygame.init()
        # main config
        # main options
        self.name = "login"
        self.FPS = 60
        self.running = True
        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()

        self.x_start = 400
        self.y_start = 200
        self.degree = 0

        self.writing = 0
        self.select_button = 0

    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.running = False
                    if self.select_button == 0:
                        try:
                            self.game.run()
                        except:
                            self.game = Game(self.name)
                            self.game.run()
                            
                    elif self.select_button == 1:
                        quit()
                        
                if event.key == pygame.K_DOWN:
                    self.select_button = self.select_button + 1 if self.select_button < 1 else 0
                    
                if event.key == pygame.K_UP:
                    self.select_button = self.select_button - 1 if self.select_button > 0 else 1
                    
                if self.writing:
                    if event.key == pygame.K_BACKSPACE:
                        self.name = self.name[:-1]
                    else:
                        self.name += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    if self.x_start + 50 <= x <= self.x_start + 400:
                        if self.y_start + 70 <= y <= self.y_start + 120:
                            self.writing = 0 if self.writing else 1
                            continue
                    self.writing = 0

    def update(self):
        self.degree = (self.degree + 1) % 360
        self.clock.tick(FPS)
        if not self.writing:
            if not self.name:
                self.name = "login"

    def render(self):
        self.screen.fill(background_color)

        for i in range(62):
            self.print_text("ONCE AT THE CASINO", 
                            self.x_start + i/6 * -cos(radians(self.degree)), 
                            self.y_start + i/6 * sin(radians(self.degree)), 
                            (133 - i * 2, i * 2, 170), 
                            font_size=60,
                            degree=sin(radians(self.degree)) * 2)
            if self.writing:
                pygame.draw.line(self.screen, 
                                 (126 - i * 2, 124 + i * 2, 170), 
                                 (self.x_start + 50 + i / 6 * -cos(radians(self.degree)), self.y_start + 120 + i / 6 * sin(radians(self.degree))), 
                                 (self.x_start + 400 + i / 6 * -cos(radians(self.degree)), self.y_start + 120 + i / 6 * -sin(radians(self.degree))), 
                                 3)
                self.print_text(self.name, 
                                    self.x_start + 70 + i/15 * -cos(radians(self.degree)), 
                                    self.y_start + 80 + i/15 * sin(radians(self.degree)), 
                                    (126 - i * 2, 124 + i * 2, 170),  
                                    font_size=50,
                                    degree=sin(radians(self.degree)) * 2)
            else:
                pygame.draw.line(self.screen, 
                                 (133 - i * 2, i * 2, 170), 
                                 (self.x_start + 50 + i / 6 * -cos(radians(self.degree)), self.y_start + 120 + i / 6 * sin(radians(self.degree))), 
                                 (self.x_start + 400 + i / 6 * -cos(radians(self.degree)), self.y_start + 120 + i / 6 * -sin(radians(self.degree))), 
                                 3)
                self.print_text(self.name, 
                                    self.x_start + 70 + i/6 * -cos(radians(self.degree)), 
                                    self.y_start + 80 + i/6 * sin(radians(self.degree)), 
                                    (133 - i * 2, i * 2, 170), 
                                    font_size=50,
                                    degree=sin(radians(self.degree)) * 2)
            
            selected_color = (126 - i * 2, 124 + i * 2, 170)
            self.print_text("PLAY!", 
                            self.x_start + i/6 * -cos(radians(self.degree)) + 150, 
                            self.y_start + i/6 * sin(radians(self.degree)) + 150, 
                            (133 - i * 2, i * 2, 170) if self.select_button != 0 else selected_color, 
                            font_size=60,
                            degree=sin(radians(self.degree)) * 2)
            
            self.print_text("QUIT", 
                            self.x_start + i/6 * -cos(radians(self.degree)) + 155, 
                            self.y_start + i/6 * sin(radians(self.degree)) + 220, 
                            (133 - i * 2, i * 2, 170) if self.select_button != 1 else selected_color, 
                            font_size=60,
                            degree=sin(radians(self.degree)) * 2)
        
        pygame.display.flip()

    def print_text(self, message, x, y, font_color=(0, 0, 0), font_size=60, font_type=None, degree=0):
        self.font_type = pygame.font.Font(font_type, font_size)
        self.text = self.font_type.render(message, True, font_color)
        self.text = pygame.transform.rotate(self.text, degree)
        self.screen.blit(self.text, (x, y))

    def run(self):
        while self.running:
            self.update()
            self.render()
            self.events()


class Game():
    def __init__(self, name) -> None:
        pygame.init()
        pygame.display.set_caption("Online Game")
        self.win = pygame.display.set_mode(SIZE)
        self.running = True
        self.name = name

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        self.clock = pygame.time.Clock()

        hero = pygame.image.load(hero_img)
        self.hero = pygame.transform.scale(hero, HERO_SIZE)
        self.x, self.y = 0, 0
        self.right, self.left, self.up, self.down = 0, 0, 0, 0

        self.bg = pygame.image.load(bg_img)
        self.bg_x, self.bg_y = 570, 290
        self.hitboxes = []

        self.players = {}

    def send_packeges(self, packege: tuple):
        self.client.sendall(pickle.dumps(packege))

    def check_move(self, hitboxes: list, x: int, y: int, move_x: int, move_y: int, size: tuple) -> bool:
        hitboxes += self.hitboxes
        x += move_x
        y += move_y
        for x1, y1, x2, y2 in hitboxes:
            if y1 <= y <= y2 or y1 <= y + size[1] <= y2:
                if x1 <= x <= x2 or x1 <= x + size[0] <= x2:
                    return False
        return True

    def event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    self.right = 1
                if event.key == pygame.K_a:
                    self.left = 1
                if event.key == pygame.K_w:
                    self.up = 1
                if event.key == pygame.K_s:
                    self.down = 1
                if event.key == pygame.K_ESCAPE:
                    Menu().run()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.right = 0
                if event.key == pygame.K_a:
                    self.left = 0
                if event.key == pygame.K_w:
                    self.up = 0
                if event.key == pygame.K_s:
                    self.down = 0

    def update(self):
        hitboxes = [[i[0], i[1], i[0] + HERO_SIZE[0], i[1] + HERO_SIZE[1]]
                    for i in self.players.values() if i[2] != self.name]
        if self.right and self.x < 3970:
            if self.check_move(hitboxes, self.x, self.y, 10, 0, HERO_SIZE):
                self.x += 10
                self.bg_x -= 10
        if self.left and self.x > 0:
            if self.check_move(hitboxes, self.x, self.y, -10, 0, HERO_SIZE):
                self.x -= 10
                self.bg_x += 10
        if self.up and self.y > 0:
            if self.check_move(hitboxes, self.x, self.y, 0, -10, HERO_SIZE):
                self.y -= 10
                self.bg_y += 10
        if self.down and self.y < 4200:
            if self.check_move(hitboxes, self.x, self.y, 0, 10, HERO_SIZE):
                self.y += 10
                self.bg_y -= 10

        self.send_packeges((self.x, self.y, self.name))

        # Читаем позиции всех игроков из сервера
        try:
            self.players = pickle.loads(self.client.recv(4096))
        except Exception as e:
            print(f"[ERROR] {e}")
            self.players = {}

    def render(self):
        # Обновляем экран
        self.win.fill((0, 0, 0))

        # Рисуем всех игроков
        self.win.blit(self.bg, (self.bg_x, self.bg_y))
        self.win.blit(
            self.hero, (SIZE[0] // 2 - HERO_SIZE[0] // 2, SIZE[1] // 2 - HERO_SIZE[1] // 2))
        for x, y, name in self.players.values():
            if name == self.name:
                continue
            self.win.blit(self.hero, (self.bg_x + x + 20, self.bg_y + y + 20))

        pygame.display.update()
        self.clock.tick(60)

    def run(self):
        while self.running:
            self.update()
            self.event()
            self.render()


if __name__ == "__main__":
    Menu().run()
