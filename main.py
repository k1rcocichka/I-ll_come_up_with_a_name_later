import pygame
import math
import os


#конфиг
FPS = 60
BULLET_SPEED = 90
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
        if self.rect.right < 0 or self.rect.left > SCREEN_WIDTH or self.rect.top > SCREEN_HEIGHT or self.rect.bottom < 0:
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
        self.speed_x = 1
        self.speed_y = 1
        self.angle = 0
        self.hp = 100
        self.inventory = []

    """отрисовка поворота"""
    def draw(self):
        rotate_image = pygame.transform.rotate(self.sprite, self.angle)
        rotate_rect = rotate_image.get_rect(center=self.rect.center)
        screen.blit(rotate_image, rotate_rect)

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
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

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

#экземпляры класса
player = Player(image="player.png", position=(70, 70))
zombey = Enemy(image="enemy.png", position=(250, 250))
bullet_group = pygame.sprite.Group()

#делаю иконку, она поч на верху не хочет работать
programIcon = load_image('icon.png')
pygame.display.set_icon(programIcon)

while running: #цикл
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONUP:
            bullet = Bullet(player.rect.center, player.angle)
            bullet.speed_x = int(BULLET_SPEED * math.cos(math.radians(player.angle)))
            bullet.speed_y = -int(BULLET_SPEED * math.sin(math.radians(player.angle)))
            bullet_group.add(bullet)

    screen.fill(BG_COLOR)

    zombey.draw()
    player.move()
    player.angle_finder(pygame.mouse.get_pos())

    bullet_group.update()
    custom_draw(bullet_group)
    
    player.draw()
    
    pygame.display.flip()

    clock.tick(FPS)

#ИГРА САМА НЕ ЗАКРЫВАТЕСЯ ХЕЛП
pygame.quit()