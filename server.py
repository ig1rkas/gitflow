import socket
import threading
import pickle
from config import *


# Игроки
players = {}

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    players[addr] = (50, 50, None)  # Начальные координаты игрока

    while True:
        try:
            data = conn.recv(4096)
            if not data:
                break
            players[addr] = pickle.loads(data)
            broadcast(players, conn)

        except Exception as e:
            print(f"[ERROR] {e}")
            break

    del players[addr]
    conn.close()

def broadcast(players, conn):
    for player in players:
        conn.sendall(pickle.dumps(players))

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen()
    print("[SERVER STARTED]")

    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
