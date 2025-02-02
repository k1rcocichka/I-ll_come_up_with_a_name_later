import pygame
import sys

# Настройки
WIDTH, HEIGHT = 800, 600
FPS = 60
DAY_LENGTH = 60  # Длина дня в секундах

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARK_BLUE = (10, 10, 50)
DAY_COLOR = (135, 206, 250)

# Инициализация Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Загрузка карты
map_image = pygame.image.load("data/map1.png").convert()
map_rect = map_image.get_rect()

# Игрок
player_size = 20
player_pos = [WIDTH // 2, HEIGHT // 2]

class Flashlight:
    def __init__(self, radius):
        self.radius = radius
        self.light_color = (255, 255, 50)
        self.light_surface = pygame.Surface((self.radius * 2, self.radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.light_surface, self.light_color + (100,), (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.light_surface, BLACK, (self.radius, self.radius), self.radius, 0)

    def draw(self, screen, player_pos, camera_x, camera_y):
        light_pos = (player_pos[0] - self.radius - camera_x, player_pos[1] - self.radius - camera_y)
        screen.blit(self.light_surface, light_pos)

# Создание фонарика
flashlight = Flashlight(radius=100)

# Уровень освещения
current_time = 0

# Основной цикл игры
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_pos[0] -= 5
    if keys[pygame.K_RIGHT]:
        player_pos[0] += 5
    if keys[pygame.K_UP]:
        player_pos[1] -= 5
    if keys[pygame.K_DOWN]:
        player_pos[1] += 5
    
    # Камера
    camera_x = player_pos[0] - WIDTH // 2
    camera_y = player_pos[1] - HEIGHT // 2

    # Время суток
    current_time += 1 / FPS
    day_progress = (current_time % DAY_LENGTH) / DAY_LENGTH

    if day_progress < 0.25:  # Утро
        background_color = (DAY_COLOR[0], DAY_COLOR[1], DAY_COLOR[2])
    elif day_progress < 0.5:  # День
        background_color = WHITE
    elif day_progress < 0.75:  # Вечер
        background_color = (DAY_COLOR[0] * (1 - (day_progress - 0.5) * 2), 
                            DAY_COLOR[1] * (1 - (day_progress - 0.5) * 2), 
                            DAY_COLOR[2] * (1 - (day_progress - 0.5) * 2))
    else:  # Ночь
        background_color = DARK_BLUE

    screen.fill(background_color)

    # Отображение карты
    screen.blit(map_image, (-camera_x, -camera_y))

    # Отображение игрока
    pygame.draw.rect(screen, WHITE, (player_pos[0] - camera_x, player_pos[1] - camera_y, player_size, player_size))

    # Фонарик
    if day_progress >= 0.75:  # Ночь
        flashlight.draw(screen, player_pos, camera_x, camera_y)

    pygame.display.flip()
    clock.tick(FPS)
