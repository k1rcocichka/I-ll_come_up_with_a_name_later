import pygame
import math
import os
import sys
from settings import *
from inventory import *


pygame.init() 
clock = pygame.time.Clock()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption(TITLE)


#тут загрузка картинок
def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Bullet(pygame.sprite.Sprite):
    image = load_image("bullet.png")
    def __init__(self, position, angle, *group):
        super().__init__(*group)
        self.sprite = Bullet.image
        self.rect = self.sprite.get_rect()
        self.sprite = pygame.transform.scale(self.sprite, (20, 20))
        self.rect.center = position
        self.speed_x = 0
        self.speed_y = 0
        self.angle = angle

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right < 0 or self.rect.left > WIDTH or self.rect.top > HEIGHT or self.rect.bottom < 0:
            self.kill()
    
    def draw(self):
        rotate_image = pygame.transform.rotate(self.sprite, self.angle)
        rotate_rect = rotate_image.get_rect(center=self.rect.center)
        screen.blit(rotate_image, rotate_rect)
    
    
def custom_draw(group):
    for sprite in group:
        sprite.draw()


class Player():
    """класс игрока"""
    def __init__(self, image, position):
        self.sprite = load_image(image)
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))
        self.rect = self.sprite.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite)
        self.rect.center = position
        self.speed_x = 2
        self.speed_y = 2
        self.angle = 0
        self.hp = 100
        self.inventory = []
        self.inventory_sprite = load_image("inventory.png")
        self.inventory_sprite = pygame.transform.scale(self.inventory_sprite, (600, 600))
        
        self.hp_bar = load_image("hp_bar.png")
        self.hp_bar = pygame.transform.scale(self.hp_bar, (250, 250))

    """отрисовка поворота"""
    def draw(self):
        rotate_image = pygame.transform.rotate(self.sprite, self.angle)
        rotate_rect = rotate_image.get_rect(center=self.rect.center)
        screen.blit(rotate_image, (rotate_rect.x - camera_x, rotate_rect.y - camera_y))
        screen.blit(self.hp_bar, (0, 350))
        if DISPLAY_iNVENTORY:
            screen.blit(self.inventory_sprite, (0, 0))
        pygame.draw.rect(screen, 'grey', (39, 388, 10, 1))
        pygame.draw.rect(screen, 'grey', (53, 388, 10, 1))
    

    """движения"""
    def move(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_w]:
            self.rect.y -= self.speed_y
        if key[pygame.K_s]:
            self.rect.y += self.speed_y
        if key[pygame.K_a]:
            self.rect.x -= self.speed_x
        if key[pygame.K_d]:
            self.rect.x += self.speed_x
        self.border()

    """штука для отслежки курсора"""
    def angle_finder(self, target_pos):
        d_x = target_pos[0] - self.rect.centerx
        d_y = target_pos[1] - self.rect.centery
        self.angle =- math.degrees(math.atan2(d_y, d_x))

    def border(self):
        self.rect.x = max(0, min(self.rect.x, map_rect.width - self.sprite.get_height()))
        self.rect.y = max(0, min(self.rect.y, map_rect.height - self.sprite.get_width()))

    def update(self):
        pass
        

class Npc():
    pass


class Enemy():
    """класс врагов"""
    def __init__(self, image, position):
        self.sprite = load_image(image)
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))
        self.rect = self.sprite.get_rect()
        self.rect.center = position
        self.speed_x = 3
        self.speed_y = 3
        self.angle = 0
        self.hp = 100

    def draw(self):
        rotate_image = pygame.transform.rotate(self.sprite, self.angle)
        rotate_rect = rotate_image.get_rect(center=self.rect.center)
        screen.blit(rotate_image, rotate_rect)


class Camera():
    def __init__(self, cam_x, cam_y):
        self.cam_x = cam_x
        self.cam_y = cam_y
        

#экземпляры класса
player = Player(image="player.png", position=(300, 400))
map = load_image("map.jpg")
map = pygame.transform.scale(map, (1000, 1000))
map_rect = map.get_rect()

bullet_group = pygame.sprite.Group()

#делаю иконку, она поч на верху не хочет работать
programIcon = load_image('icon.png')
pygame.display.set_icon(programIcon)
inventory_open = False

while running:  # цикл
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                inventory_open = not inventory_open

        if event.type == pygame.MOUSEBUTTONUP:
            bullet = Bullet(player.rect.center, player.angle)
            bullet.speed_x = int(BULLET_SPEED * math.cos(math.radians(player.angle)))
            bullet.speed_y = -int(BULLET_SPEED * math.sin(math.radians(player.angle)))
            bullet_group.add(bullet)

    camera_x = player.rect.x - WIDTH // 2 + 100 // 2
    camera_y = player.rect.y - HEIGHT // 2 + 100 // 2

    screen.fill(WHITE)
    
    screen.blit(map, (-camera_x, -camera_y))

    player.move()
    player.angle_finder(pygame.mouse.get_pos())

    bullet_group.update()
    custom_draw(bullet_group)

    player.draw()

    if inventory_open:
        # Отображаем инвентарь
        screen.blit(inventor_image, (center_x, center_y ))

    pygame.display.flip()

    clock.tick(FPS)

#ИГРА САМА НЕ ЗАКРЫВАТЕСЯ ХЕЛП
pygame.quit()
