import pygame
import socket
import pickle

from config.config import *

        
class Game():
    def __init__(self) -> None:
        pygame.init()
        pygame.display.set_caption("Online Game")
        self.win = pygame.display.set_mode(SIZE)

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((HOST, PORT))
        self.x, self.y = 50, 50
        self.clock = pygame.time.Clock()
        self.right, self.left, self.up, self.down = 0, 0, 0, 0

    def send_position(self, pos):
        self.client.sendall(pickle.dumps(pos))
        
    def event(self):
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:
                        self.right = 1
                    if event.key == pygame.K_a:
                        self.left = 1
                    if event.key == pygame.K_w:
                        self.up = 1
                    if event.key == pygame.K_s:
                        self.down = 1
                
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
        if self.right:
            if self.x < SIZE[0] - 20:
                self.x += 10
        if self.left and self.x > 0:
            self.x -= 10
        if self.up and self.y > 0:
            self.y -= 10
        if self.down and self.y < SIZE[1] - 20:
            self.y += 10
            
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
            for player_pos in self.players.values():
                pygame.draw.rect(self.win, (255, 0, 0), (player_pos[0], player_pos[1], 20, 20))

            # Рисуем текущего игрока
            pygame.draw.rect(self.win, (0, 255, 0), (self.x, self.y, 20, 20))  # Зелёный цвет для текущего игрока

            pygame.display.update()
            self.clock.tick(60)
            
    def run(self):
        while True:
            self.update()
            self.event()
            self.render()

if __name__ == "__main__":
    Game().run()
