import pygame
import socket
import threading
import pickle

# Настройки
WIDTH, HEIGHT = 500, 500
BLUE = (0, 0, 255)
RED = (255, 0, 0)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Онлайн игра с квадратами")

# Игрок
player_pos = [0, 0]

# Сокет
server_address = ('localhost', 12345)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(server_address)

def receive_data():
    global player_pos
    while True:
        data = client_socket.recv(1024)
        if data:
            player_pos = pickle.loads(data)

# Запуск потока для получения данных
threading.Thread(target=receive_data, daemon=True).start()

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player_pos[1] -= 5
    if keys[pygame.K_DOWN]:
        player_pos[1] += 5
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5

    # Отправка позиции игрока на сервер
    client_socket.send(pickle.dumps(player_pos))

    # Отрисовка
    screen.fill((200, 200, 200))
    pygame.draw.rect(screen, RED, (player_pos[0], player_pos[1], 50, 50))  # Красный квадрат
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
client_socket.close()
