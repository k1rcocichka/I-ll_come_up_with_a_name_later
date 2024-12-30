import pygame
import math
import os


#конфиг
FPS = 60
running = True
SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
BG_COLOR = (20), (120), (0)

pygame.init() 
clock = pygame.time.Clock()
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("cursed_wood")


def load_image(name, colorkey=None): #тут загрузка картинок
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


class Player():
    """класс игрока"""
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

    """штука для отслежки курсора"""
    def angle_finder(self, target_pos):
        d_x = target_pos[0] - self.rect.centerx
        d_y = target_pos[1] - self.rect.centery
        self.angle =- math.degrees(math.atan2(d_y, d_x))




class Npc():
    pass


class Enemy():
    """класс врагов"""
    def __init__(self, image, position):
        self.image = pygame.image.load(image)
        self.image = pygame.transform.scale(self.image, (105, 90))
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.speed_x = 3
        self.speed_y = 3
        self.angle = 0

    def draw(self):
        rotate_image = pygame.transform.rotate(self.image, self.angle)
        rotate_rect = rotate_image.get_rect(center=self.rect.center)
        screen.blit(rotate_image, rotate_rect)




player = Player(image="pngwing.com.png", position=(50, 50))

#запуск



while running: #цикл
    for event in pygame.event.get():
        if event == pygame.QUIT:
            running = False

    screen.fill(BG_COLOR)
    
    player.angle_finder(pygame.mouse.get_pos())
    player.draw()
    player.move()
    pygame.display.flip()
    clock.tick(FPS)
    
pygame.quit()
