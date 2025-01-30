import pygame
import math

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)

# Загрузка карты
background = pygame.image.load('data/map1.png')

# Настройка окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D Game with Camera Follow")

# Игрок
player_img = pygame.Surface((50, 50))
player_img.fill((0, 128, 255))
player_rect = player_img.get_rect(center=(WIDTH // 2, HEIGHT // 2))

# Часы для контроля FPS
clock = pygame.time.Clock()

# Основной игровой цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Получение позиции мыши
    mouse_x, mouse_y = pygame.mouse.get_pos()

    # Поворот игрока в сторону курсора
    angle = math.atan2(mouse_y - player_rect.centery, mouse_x - player_rect.centerx)
    player_img_rotated = pygame.transform.rotate(player_img, -math.degrees(angle))

    # Обновление позиции игрока (простой пример, здесь можно добавить логику передвижения)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_rect.y -= 5
    if keys[pygame.K_s]:
        player_rect.y += 5
    if keys[pygame.K_a]:
        player_rect.x -= 5
    if keys[pygame.K_d]:
        player_rect.x += 5

    # Определение позиции камеры (центрировать камеру на игроке)
    camera_x = player_rect.centerx - WIDTH // 2
    camera_y = player_rect.centery - HEIGHT // 2

    # Отрисовка
    screen.fill(WHITE)
    screen.blit(background, (-camera_x, -camera_y))
    
    # Вычислить центр для вращения
    player_rotated_rect = player_img_rotated.get_rect(center=(player_rect.centerx - camera_x, player_rect.centery - camera_y))
    screen.blit(player_img_rotated, player_rotated_rect.topleft)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()