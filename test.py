import pygame
import sys

# Инициализация Pygame
pygame.init()

# Настройки окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Game with Smooth Day-Night Cycle")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Загрузка карты
map_image = pygame.image.load("data/map.png").convert_alpha()
map_rect = map_image.get_rect()

# Игрок (белый квадрат)
player_size = 40
player_rect = pygame.Rect(0, 0, player_size, player_size)
player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Скорость игрока
player_speed = 5

# Камера
camera_x = 0
camera_y = 0

# Настройки времени суток
time_of_day = {
    "morning": {"length": 5000, "start_alpha": 0, "end_alpha": 0},  # Утро (5 секунд)
    "day": {"length": 10000, "start_alpha": 0, "end_alpha": 0},  # День (10 секунд)
    "evening": {"length": 5000, "start_alpha": 0, "end_alpha": 128},  # Вечер (5 секунд)
    "night": {"length": 10000, "start_alpha": 128, "end_alpha": 255},  # Ночь (10 секунд)
}
current_time = 0  # Текущее время в текущей фазе
current_phase = "morning"  # Текущая фаза времени суток

# Основной игровой цикл
clock = pygame.time.Clock()
running = True

while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Обработка движения игрока
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_rect.y -= player_speed
    if keys[pygame.K_s]:
        player_rect.y += player_speed
    if keys[pygame.K_a]:
        player_rect.x -= player_speed
    if keys[pygame.K_d]:
        player_rect.x += player_speed

    # Движение камеры
    camera_x = player_rect.centerx - SCREEN_WIDTH // 2
    camera_y = player_rect.centery - SCREEN_HEIGHT // 2

    # Ограничение камеры в пределах карты
    camera_x = max(0, min(camera_x, map_rect.width - SCREEN_WIDTH))
    camera_y = max(0, min(camera_y, map_rect.height - SCREEN_HEIGHT))

    # Обновление времени суток
    current_time += clock.get_time()
    if current_time >= time_of_day[current_phase]["length"]:
        # Переход к следующей фазе
        if current_phase == "morning":
            current_phase = "day"
        elif current_phase == "day":
            current_phase = "evening"
        elif current_phase == "evening":
            current_phase = "night"
        elif current_phase == "night":
            current_phase = "morning"
        current_time = 0

    # Отрисовка
    screen.fill(BLACK)
    screen.blit(map_image, (-camera_x, -camera_y))  # Отрисовка карты
    pygame.draw.rect(screen, WHITE, (player_rect.x - camera_x, player_rect.y - camera_y, player_size, player_size))  # Отрисовка игрока

    # Плавный расчет прозрачности для текущей фазы
    phase_data = time_of_day[current_phase]
    progress = current_time / phase_data["length"]  # Прогресс текущей фазы (от 0 до 1)
    alpha = phase_data["start_alpha"] + (phase_data["end_alpha"] - phase_data["start_alpha"]) * progress

    # Создание затемняющего слоя
    dark_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    dark_surface.fill(BLACK)
    dark_surface.set_alpha(int(alpha))  # Установка прозрачности
    screen.blit(dark_surface, (0, 0))  # Наложение слоя

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()