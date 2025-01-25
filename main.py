import pygame
import math
import os
import sys
from settings import *
from inventory import *

#создание игры
pygame.init() 
clock = pygame.time.Clock()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption(TITLE)

#commit


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
    """конструктор пуль"""
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
        """передвижение и смерть"""
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.right < 0 or self.rect.left > WIDTH + camera_x or self.rect.top > HEIGHT + camera_y or self.rect.bottom < 0:
            self.kill()
    
    def draw(self):
        """рисууем пулю"""
        rotate_image = pygame.transform.rotate(self.sprite, self.angle)
        rotate_rect = rotate_image.get_rect(center=self.rect.center)
        screen.blit(rotate_image, (rotate_rect.x - camera_x, rotate_rect.y - camera_y))
    
#для рисование групп
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
        original_position = self.rect.center

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

        for box in boxs_group:
            if self.rect.colliderect(box.rect):
                self.rect.center = original_position

    """штука для отслежки курсора"""
    def angle_finder(self, target_pos):
        d_x = target_pos[0] - self.rect.centerx + camera_x
        d_y = target_pos[1] - self.rect.centery + camera_y
        self.angle =- math.degrees(math.atan2(d_y, d_x))

    """ограничитель"""
    def border(self):
        self.rect.x = max(0, min(self.rect.x, map_rect.width - self.sprite.get_height()))
        self.rect.y = max(0, min(self.rect.y, map_rect.height - self.sprite.get_width()))

    def update(self):
        pass
        

class Barrier(pygame.sprite.Sprite):
    """констурктор препятствий"""
    image = load_image("box.png")
    image = pygame.transform.scale(image, (80, 80))
    def __init__(self, position, *group):
        super().__init__(*group)
        self.sprite = Barrier.image
        self.rect = self.sprite.get_rect()
        self.rect.inflate_ip(-20, -20)
        self.rect.center = position

    def update(self):
        pass



class Enemy():
    """конструктор класса"""
    def __init__(self, image, position):
        self.sprite = load_image(image)
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))
        self.rect = self.sprite.get_rect()
        self.mask = pygame.mask.from_surface(self.sprite)
        self.rect.center = position
        self.speed_x = 1
        self.speed_y = 1
        self.angle = 0

    def draw(self):
        """рисуем врага"""
        rotate_image = pygame.transform.rotate(self.sprite, self.angle)
        rotate_rect = rotate_image.get_rect(center=self.rect.center)
        screen.blit(rotate_image, (rotate_rect.x - camera_x, rotate_rect.y - camera_y))

    def move(self):
        """логику позже"""
        pass

    def border(self):
        """ограничитель"""
        self.rect.x = max(0, min(self.rect.x, map_rect.width - self.sprite.get_height()))
        self.rect.y = max(0, min(self.rect.y, map_rect.height - self.sprite.get_width()))

    def angle_finder(self, target_pos):
        """поиск врага"""
        d_x = target_pos[0] - self.rect.centerx + camera_x
        d_y = target_pos[1] - self.rect.centery + camera_y
        self.angle =- math.degrees(math.atan2(d_y, d_x))
        

#группы
bullet_group = pygame.sprite.Group()
boxs_group = pygame.sprite.Group()

#экземпляры класса
x, y = 200, 200
for box in range(5):
    x += 100
    cords = x, y
    box = Barrier(position=cords)
    boxs_group.add(box)

player = Player(image="player.png", position=(300, 400))
enemy = Enemy(image="enemy.png", position=(500, 500))
inventory_image = pygame.image.load('./data/inventory.png', )
inventor_image = pygame.transform.scale(inventory_image, (inventory_width, inventory_height))
map = load_image("map.png")
map = pygame.transform.scale(map, (1000, 1000))
map_rect = map.get_rect()

#иконка
programIcon = load_image('icon.png')
pygame.display.set_icon(programIcon)
inwentory = Inventory(Player, 10, 5, 2)
inventory_open = False

while running:  # цикл
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pg.MOUSEBUTTONDOWN and event.button == 3:
            if inwentory.display_inventory:
                mouse_pos = pg.mouse.get_pos()
                inwentory.checkSlot(screen, mouse_pos)
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
            if inwentory.display_inventory:
                inwentory.moveItem(screen)
        if event.type == pg.MOUSEBUTTONUP and event.button == 1:
            if inwentory.display_inventory:
                inwentory.placeItem(screen)

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
        screen.blit(inventor_image, (center_x, center_y))
        #броня с лево сверху
        pygame.draw.rect(screen, 'yellow', (137, 137, 36, 36))
        pygame.draw.rect(screen, 'yellow', (179, 137, 36, 36))
        pygame.draw.rect(screen, 'yellow', (221, 137, 36, 36))
        pygame.draw.rect(screen, 'yellow', (137, 179, 36, 36))
        pygame.draw.rect(screen, 'yellow', (179, 179, 36, 36))
        pygame.draw.rect(screen, 'yellow', (221, 179, 36, 36))
        pygame.draw.rect(screen, 'yellow', (137, 220, 36, 36))
        pygame.draw.rect(screen, 'yellow', (179, 220, 36, 36))
        pygame.draw.rect(screen, 'yellow', (179, 261, 36, 36))
        #картинка игрока с права сверху
        pygame.draw.rect(screen, 'yellow', (387, 137, 78, 119))
        pygame.draw.rect(screen, 'yellow', (387, 261, 36, 36))
        pygame.draw.rect(screen, 'yellow', (429, 261, 36, 36))
        #инвентарь 1 ряд
        pygame.draw.rect(screen, 'yellow', (137, 345, 36, 36))
        pygame.draw.rect(screen, 'yellow', (179, 345, 36, 36))
        pygame.draw.rect(screen, 'yellow', (221, 345, 36, 36))
        pygame.draw.rect(screen, 'yellow', (262, 345, 36, 36))
        pygame.draw.rect(screen, 'yellow', (304, 345, 36, 36))
        pygame.draw.rect(screen, 'yellow', (345, 345, 36, 36))
        pygame.draw.rect(screen, 'yellow', (387, 345, 36, 36))
        pygame.draw.rect(screen, 'yellow', (429, 345, 36, 36))
        # инвентарь 2 ряд
        pygame.draw.rect(screen, 'yellow', (137, 387, 36, 36))
        pygame.draw.rect(screen, 'yellow', (179, 387, 36, 36))
        pygame.draw.rect(screen, 'yellow', (221, 387, 36, 36))
        pygame.draw.rect(screen, 'yellow', (262, 387, 36, 36))
        pygame.draw.rect(screen, 'yellow', (304, 387, 36, 36))
        pygame.draw.rect(screen, 'yellow', (345, 387, 36, 36))
        pygame.draw.rect(screen, 'yellow', (387, 387, 36, 36))
        pygame.draw.rect(screen, 'yellow', (429, 387, 36, 36))
        # инвентарь 3 ряд
        pygame.draw.rect(screen, 'yellow', (137, 429, 36, 36))
        pygame.draw.rect(screen, 'yellow', (179, 429, 36, 36))
        pygame.draw.rect(screen, 'yellow', (221, 429, 36, 36))
        pygame.draw.rect(screen, 'yellow', (262, 429, 36, 36))
        pygame.draw.rect(screen, 'yellow', (304, 429, 36, 36))
        pygame.draw.rect(screen, 'yellow', (345, 429, 36, 36))
        pygame.draw.rect(screen, 'yellow', (387, 429, 36, 36))
        pygame.draw.rect(screen, 'yellow', (429, 429, 36, 36))
        # инвентарь 4 ряд
        pygame.draw.rect(screen, 'yellow', (137, 471, 36, 36))
        pygame.draw.rect(screen, 'yellow', (179, 471, 36, 36))
        pygame.draw.rect(screen, 'yellow', (221, 471, 36, 36))
        pygame.draw.rect(screen, 'yellow', (262, 471, 36, 36))
        pygame.draw.rect(screen, 'yellow', (304, 471, 36, 36))
        pygame.draw.rect(screen, 'yellow', (345, 471, 36, 36))
        pygame.draw.rect(screen, 'yellow', (387, 471, 36, 36))
        pygame.draw.rect(screen, 'yellow', (429, 471, 36, 36))


    pygame.display.flip()

    clock.tick(FPS)

# ИГРА САМА НЕ ЗАКРЫВАТЕСЯ ХЕЛП
pygame.quit()
