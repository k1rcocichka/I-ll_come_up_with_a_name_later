import pygame
import sys

# Инициализация Pygame
pygame.init()

# Параметры экрана
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)

# Параметры игрока
player_pos = [400, 300]
player_size = 50
player_speed = 5

# Загрузка карты из PNG изображения
map_image = pygame.image.load('map.jpg')  # Убедитесь, что файл "map.png" находится в той же папке, что и этот скрипт
map_rect = map_image.get_rect()

# Основной цикл игры
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT]:
        player_pos[0] += player_speed
    if keys[pygame.K_UP]:
        player_pos[1] -= player_speed
    if keys[pygame.K_DOWN]:
        player_pos[1] += player_speed

    # Убедимся, что игрок не выходит за пределы карты
    player_pos[0] = max(0, min(player_pos[0], map_rect.width - player_size))
    player_pos[1] = max(0, min(player_pos[1], map_rect.height - player_size))

    # Рассчитываем позицию камеры
    camera_x = player_pos[0] - screen_width // 2 + player_size // 2
    camera_y = player_pos[1] - screen_height // 2 + player_size // 2

    # Заливка фона
    screen.fill(white)

    # Отрисовка карты с учетом камеры
    screen.blit(map_image, (-camera_x, -camera_y))

    # Отрисовка игрока
    pygame.draw.rect(screen, black, (player_pos[0] - camera_x, player_pos[1] - camera_y, player_size, player_size))

    # Обновление экрана
    pygame.display.flip()
    clock.tick(30)