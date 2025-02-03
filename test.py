import pygame
import sys
import random

# Инициализация Pygame
pygame.init()

# Настройки окна
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("2D Game with Enemy")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Загрузка карты
map_image = pygame.image.load("data/map.png").convert_alpha()
map_rect = map_image.get_rect()

# Игрок (белый квадрат)
player_size = 40
player_rect = pygame.Rect(0, 0, player_size, player_size)
player_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Скорость игрока
player_speed = 5

# Здоровье игрока
player_health = 100

# Камера
camera_x = 0
camera_y = 0

# Враг
class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 2
        self.direction = random.choice(["up", "down", "left", "right"])
        self.move_timer = 0  # Таймер для перемещения каждые 5 секунд

    def update(self):
        # Перемещение врага каждые 5 секунд
        self.move_timer += 1
        if self.move_timer >= 300:  # 300 кадров = 5 секунд (при 60 FPS)
            self.move_timer = 0
            self.direction = random.choice(["up", "down", "left", "right"])

        # Движение врага
        if self.direction == "up":
            self.rect.y -= self.speed
        elif self.direction == "down":
            self.rect.y += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed
        elif self.direction == "right":
            self.rect.x += self.speed

        # Ограничение движения врага в пределах карты
        self.rect.x = max(0, min(self.rect.x, map_rect.width - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, map_rect.height - self.rect.height))

    def draw(self, surface, camera_x, camera_y):
        # Отрисовка врага с учетом камеры
        pygame.draw.rect(surface, RED, (self.rect.x - camera_x, self.rect.y - camera_y, self.rect.width, self.rect.height))

# Создание врага
enemy = Enemy(random.randint(0, map_rect.width), random.randint(0, map_rect.height))

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

    # Обновление врага
    enemy.update()

    # Проверка столкновения игрока с врагом
    if player_rect.colliderect(enemy.rect):
        player_health -= 1
        if player_health <= 0:
            player_health = 0
            print("Игрок умер!")

    # Отрисовка
    screen.fill(BLACK)
    screen.blit(map_image, (-camera_x, -camera_y))  # Отрисовка карты
    pygame.draw.rect(screen, WHITE, (player_rect.x - camera_x, player_rect.y - camera_y, player_size, player_size))  # Отрисовка игрока
    enemy.draw(screen, camera_x, camera_y)  # Отрисовка врага

    # Обновление экрана
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()