import pygame
import socket
import pickle

from config import *
from math import *



class Menu():
    def __init__(self) -> None:
        pygame.init()
        # main config
        # main options
        self.FPS = 60
        self.running = True
        self.screen = pygame.display.set_mode(SIZE)
        self.clock = pygame.time.Clock()
        
        self.x_start = 400
        self.y_start = 200  
        self.degree = 0
        
        
    


    def events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                self.running = False
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.running = False
                    try:
                        self.game.run()
                    except:
                        self.game = Game()
                        self.game.run()
                    
                
           
    def update(self):
        self.degree = (self.degree + 1) % 360
        self.clock.tick(FPS)


    def render(self):
        self.screen.fill(background_color)
       
        for i in range(62):
            self.print_text("ONCE AT THE CASINO", self.x_start + i/6 * -cos(radians(self.degree)), self.y_start + i/6 * sin(radians(self.degree)), (133 - i * 2, i * 2, 170), font_size=60, degree=sin(radians(self.degree)) * 2)
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
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Online Game")
        self.win = pygame.display.set_mode(SIZE)
        self.running = True

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        self.clock = pygame.time.Clock()
        
        hero = pygame.image.load(hero_img)
        self.hero = pygame.transform.scale(hero, HERO_SIZE)
        self.x, self.y = 0, 0
        self.right, self.left, self.up, self.down = 0, 0, 0, 0
        
        self.bg = pygame.image.load(bg_img)
        self.bg_x, self.bg_y = 570, 290

    def send_position(self, pos):
        self.client.sendall(pickle.dumps(pos))
        
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
        if self.right and self.x < 3970:
            self.x += 10
            self.bg_x -= 10
        if self.left and self.x > 0:
            self.x -= 10
            self.bg_x += 10
        if self.up and self.y > 0:
            self.y -= 10
            self.bg_y += 10
        if self.down and self.y < 4200:
            self.y += 10
            self.bg_y -= 10
            
        self.send_position((self.x, self.y))

            # Читаем позиции всех игроков из сервера
        try:
            self.players = pickle.loads(self.client.recv(4096))
        except Exception as e:
            print(f"[ERROR] {e}")
            self.players = {}
        
    def render(self):
            # Отправляем текущую позицию игрока на сервер
            

            # Обновляем экран
            self.win.fill((0, 0, 0))
            
            # Рисуем всех игроков
            self.win.blit(self.bg, (self.bg_x, self.bg_y))
            for x, y in self.players.values():
                if (x, y) == (self.x, self.y): #если текущий
                    self.win.blit(self.hero, (SIZE[0] // 2 - HERO_SIZE[0] // 2, SIZE[1] // 2 - HERO_SIZE[1] // 2))
                    continue
                else:
                    self.win.blit(self.hero, (self.bg_x + x, self.bg_y + y))
                    

            pygame.display.update()
            self.clock.tick(60)
            
    def run(self):
        while self.running:
            self.update()
            self.event()
            self.render()

if __name__ == "__main__":
    Menu().run()
