import pygame
import socket
import pickle

# Настройки клиента
HOST = '81.31.247.7'  # Адрес сервера
PORT = 5555          # Порт сервера

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Online Game")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def send_position(pos):
    client.sendall(pickle.dumps(pos))

def main():
    x, y = 50, 50
    clock = pygame.time.Clock()
    right, left, up, down = 0, 0, 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    right = 1
                if event.key == pygame.K_a:
                    left = 1
                if event.key == pygame.K_w:
                    up = 1
                if event.key == pygame.K_s:
                    down = 1
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    right = 0
                if event.key == pygame.K_a:
                    left = 0
                if event.key == pygame.K_w:
                    up = 0
                if event.key == pygame.K_s:
                    down = 0
        
        if right:
            x += 10
        if left:
            x -= 10
        if up:
            y -= 10
        if down:
            y += 10

        # Отправляем текущую позицию игрока на сервер
        send_position((x, y))

        # Читаем позиции всех игроков из сервера
        try:
            players = pickle.loads(client.recv(4096))
        except Exception as e:
            print(f"[ERROR] {e}")
            players = {}

        # Обновляем экран
        win.fill((0, 0, 0))
        
        # Рисуем всех игроков
        for player_pos in players.values():
            pygame.draw.rect(win, (255, 0, 0), (player_pos[0], player_pos[1], 20, 20))

        # Рисуем текущего игрока
        pygame.draw.rect(win, (0, 255, 0), (x, y, 20, 20))  # Зелёный цвет для текущего игрока

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
import pygame
import socket
import pickle

# Настройки клиента
HOST = '81.31.247.7'  # Адрес сервера
PORT = 5555          # Порт сервера

pygame.init()
win = pygame.display.set_mode((500, 500))
pygame.display.set_caption("Online Game")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

def send_position(pos):
    client.sendall(pickle.dumps(pos))

def main():
    x, y = 50, 50
    clock = pygame.time.Clock()
    right, left, up, down = 0, 0, 0, 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_d:
                    right = 1
                if event.key == pygame.K_a:
                    left = 1
                if event.key == pygame.K_w:
                    up = 1
                if event.key == pygame.K_s:
                    down = 1
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    right = 0
                if event.key == pygame.K_a:
                    left = 0
                if event.key == pygame.K_w:
                    up = 0
                if event.key == pygame.K_s:
                    down = 0
        
        if right:
            x += 10
        if left:
            x -= 10
        if up:
            y -= 10
        if down:
            y += 10

        # Отправляем текущую позицию игрока на сервер
        send_position((x, y))

        # Читаем позиции всех игроков из сервера
        try:
            players = pickle.loads(client.recv(4096))
        except Exception as e:
            print(f"[ERROR] {e}")
            players = {}

        # Обновляем экран
        win.fill((0, 0, 0))
        
        # Рисуем всех игроков
        for player_pos in players.values():
            pygame.draw.rect(win, (255, 0, 0), (player_pos[0], player_pos[1], 20, 20))

        # Рисуем текущего игрока
        pygame.draw.rect(win, (0, 255, 0), (x, y, 20, 20))  # Зелёный цвет для текущего игрока

        pygame.display.update()
        clock.tick(60)

if __name__ == "__main__":
    main()
