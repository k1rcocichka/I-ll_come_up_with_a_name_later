import pygame
import sys
import socket
import pickle

# Устанавливаем размеры экрана
WIDTH, HEIGHT = 300, 300
GRID_SIZE = 3
CELL_SIZE = WIDTH // GRID_SIZE

# Инициализируем Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Крестики-нолики")
font = pygame.font.SysFont(None, 60)


# Функция отрисовки сетки
def draw_grid():
    for i in range(1, GRID_SIZE):
        pygame.draw.line(screen, (0, 0, 0), (CELL_SIZE * i, 0), (CELL_SIZE * i, HEIGHT), 2)
        pygame.draw.line(screen, (0, 0, 0), (0, CELL_SIZE * i), (WIDTH, CELL_SIZE * i), 2)


# Основные переменные
board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
turn = 'X'  # 'X' или 'O'


# Основной игровой цикл
def game_loop(conn):
    global turn
    while True:
        screen.fill((255, 255, 255))
        draw_grid()

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and turn:
                x, y = event.pos
                column = x // CELL_SIZE
                row = y // CELL_SIZE

                if board[row][column] == '':
                    board[row][column] = turn
                    turn = 'O' if turn == 'X' else 'X'
                    conn.send(pickle.dumps(board))  # Отправить изменения по сети

        # Изменить состояние доски если данные получены
        data = conn.recv(1024)
        if data:
            board = pickle.loads(data)
            turn = 'O' if turn == 'X' else 'X'

        # Отрисовка символов
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                if board[row][col] == 'X':
                    text = font.render('X', True, (0, 0, 0))
                    screen.blit(text, (col * CELL_SIZE + 50, row * CELL_SIZE + 10))
                elif board[row][col] == 'O':
                    text = font.render('O', True, (0, 0, 0))
                    screen.blit(text, (col * CELL_SIZE + 50, row * CELL_SIZE + 10))

        pygame.display.flip()


# Запуск сервера или клиента в зависимости от запуска
def start_game():
    host = socket.gethostname()  # Доменное имя текущего хоста
    port = 12345
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    choice = input("Запустить как (1) сервер или (2) клиент? ")
    if choice == '1':
        conn.bind((host, port))
        conn.listen(1)
        print("Ожидание подключения...")
        conn, addr = conn.accept()
        print("Подключено к:", addr)
    elif choice == '2':
        conn.connect((host, port))

    game_loop(conn)


if __name__ == "__main__":
    start_game()