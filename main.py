import pygame
import math
import os
import sys
import random
from settings import *

#создание игры
pygame.init() 
clock = pygame.time.Clock()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption(TITLE)
font = pygame.font.SysFont('serif', 50)

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

#для рисование групп
def custom_draw(group):
    for sprite in group:
        sprite.draw()

#класс объктов
class Object(pygame.sprite.Sprite):
    image_e = load_image("e.png")
    image_e = pygame.transform.scale(image_e, (40, 40))
    def __init__(self, position, image, name, *groups):
        super().__init__(*groups)
        image = load_image(image)
        image = pygame.transform.scale(image, (50, 50))
        self.sprite = image
        self.rect = self.sprite.get_rect()
        self.rect.center = position
        self.sprite_e = Object.image_e
        self.rect_e = self.sprite_e.get_rect()
        self.rect_e.center = position

        self.use_me = False
        self.name = name

    def draw(self):
        screen.blit(self.sprite, (self.rect.x - camera_x, self.rect.y - camera_y))

    def use(self):
        if (player.rect.x > self.rect.x - 50 and player.rect.y > self.rect.y - 50) and (player.rect.x < self.rect.x + 50 and player.rect.y < self.rect.y + 50):
            screen.blit(self.sprite_e, (self.rect_e.x - camera_x, self.rect_e.y - camera_y - 40))
            self.use_me = True
        else:
            self.use_me = False

    def update(self):
        self.use()


class Wearon(Object):
    def __init__(self, position, image, name, full_clip, clip, *groups):
        super().__init__(position, image, name, *groups)
        self.full_clip = full_clip
        self.clip = clip


class Medkit(Object):
    def __init__(self, position, image, use_medkit, name, *groups):
        super().__init__(position, image, name,*groups)
        self.use_medkit = use_medkit


class ClipsWearon(Object):
    def __init__(self, position, image, clips_many, use_clips, name, *groups):
        super().__init__(position, image, name, *groups)
        self.clips_many = clips_many
        self.use_clips = use_clips


class Bullet(pygame.sprite.Sprite):
    """конструктор пуль"""
    image = load_image("bullet.png")
    image = pygame.transform.scale(image, (20, 20))
    def __init__(self, position, angle, *group):
        super().__init__(*group)
        self.sprite = Bullet.image
        self.rect = self.sprite.get_rect()
        self.rect.inflate_ip(-50, -50)
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
        
        for box in boxs_group:
            if self.rect.colliderect(box.rect):
                box.hp = box.hp - 10
                print(box.hp)
                self.kill()
        
    def draw(self):
        """рисууем пулю"""
        rotate_image = pygame.transform.rotate(self.sprite, self.angle)
        rotate_rect = rotate_image.get_rect(center=self.rect.center)
        screen.blit(rotate_image, (rotate_rect.x - camera_x, rotate_rect.y - camera_y))

#анимация
class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns, 
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Player():
    """класс игрока"""
    def __init__(self, image, position):
        self.sprite = load_image(image)
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))
        self.rect = self.sprite.get_rect()
        self.rect.inflate_ip(-50, -50)
        self.mask = pygame.mask.from_surface(self.sprite)

        self.inventory_cell = 0
        self.rect.center = position
        self.speed_x = 2
        self.speed_y = 2
        self.angle = 0
        self.hp = 190
        self.inventory = [None, None, None]

        self.inventory_sprite = load_image("inventory.png")
        self.inventory_sprite = pygame.transform.scale(self.inventory_sprite, (600, 600))
        
        self.hp_bar = load_image("hp_bar.png")
        self.hp_bar = pygame.transform.scale(self.hp_bar, (250, 250))
        self.start_ticks = pygame.time.get_ticks()

    """отрисовка поворота"""
    def draw(self):
        rotate_image = pygame.transform.rotate(self.sprite, self.angle)
        rotate_rect = rotate_image.get_rect(center=self.rect.center)
        screen.blit(rotate_image, (rotate_rect.x - camera_x, rotate_rect.y - camera_y))
        screen.blit(self.hp_bar, (0, 350))
        
        if self.have_wearon():
            text = f"{self.inventory[self.inventory_cell].clip}/{self.inventory[self.inventory_cell].full_clip}"
            text = font.render(text, True, (0, 0, 0))
            screen.blit(text, (450, 520))

        if type(self.inventory[self.inventory_cell]) == Medkit:
            text = f"{self.inventory[self.inventory_cell].use_medkit}"
            text = font.render(text, True, (0, 0, 0))
            screen.blit(text, (450, 520))

        if type(self.inventory[self.inventory_cell]) == ClipsWearon:
            text = f"{self.inventory[self.inventory_cell].use_clips}"
            text = font.render(text, True, (0, 0, 0))
            screen.blit(text, (450, 520))

        if DISPLAY_iNVENTORY:
            screen.blit(self.inventory_sprite, (0, 0))

        lost_hp = pygame.draw.rect(screen, 'grey', (40, 388, 10, 190 - self.hp))
        lost_stamina = pygame.draw.rect(screen, 'grey', (53, 388, 10, 190))
    
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

        if player.rect.colliderect(enemy) and enemy.hp >= 0:
            self.rect.center = original_position
            self.hp -= self.hp - 10
            print(self.hp)
        
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

    def have_wearon(self):
        if type(self.inventory[self.inventory_cell]) == Wearon:
            return True
        return False
        

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
        self.hp = 20

    def update(self):   
        if self.hp <= 0:
            self.kill()

    def draw(self):
        screen.blit(self.sprite, (self.rect.x - camera_x, self.rect.y - camera_y))


class Enemy(pygame.sprite.Sprite):
    """конструктор класса"""
    image = load_image("enemy.png")
    image = pygame.transform.scale(image, (100, 100))
    def __init__(self, position, *group):
        super().__init__(*group)
        self.sprite = Enemy.image
        self.rect = self.sprite.get_rect()
        self.rect.inflate_ip(-50, -50)
        self.mask = pygame.mask.from_surface(self.sprite)

        self.rect.center = position
        self.speed_x_ = 3
        self.speed_y_ = 3
        self.angle = 0
        self.hp = 100

    def update(self, target, target_pos):
        """рисуем врага"""
        self.target(target_pos)
        rotate_image = pygame.transform.rotate(self.sprite, self.angle)
        rotate_rect = rotate_image.get_rect(center=self.rect.center)
        if self.hp >= 0:
            screen.blit(rotate_image, (rotate_rect.x - camera_x, rotate_rect.y - camera_y))

    def move(self):
        """логику позже"""
        original_position = self.rect.center
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        for box in boxs_group:
            if self.rect.colliderect(box.rect):
                self.rect.center = original_position

        if self.rect.colliderect(player) and self.hp >= 0:
            self.rect.center = original_position

        for bullets in bullet_group:
            if self.rect.colliderect(bullet) and self.hp >= 0:
                self.hp = self.hp - 10
                bullet.kill()

    def border(self):
        """ограничитель"""
        self.rect.x = max(0, min(self.rect.x, map_rect.width - self.sprite.get_height()))
        self.rect.y = max(0, min(self.rect.y, map_rect.height - self.sprite.get_width()))

    def angle_finder(self, target_pos):
        """поиск врага"""
        d_x = target_pos[0] - self.rect.centerx + camera_x
        d_y = target_pos[1] - self.rect.centery + camera_y
        self.angle =- math.degrees(math.atan2(d_y, d_x))

    def target(self, target_pos):
        if (player.rect.x > self.rect.x - 200 and player.rect.y > self.rect.y - 200) and (player.rect.x < self.rect.x + 200 and player.rect.y < self.rect.y + 200):
            self.angle_finder(target_pos)
            self.speed_x = int(self.speed_x_ * math.cos(math.radians(self.angle)))
            self.speed_y = -int(self.speed_y_ * math.sin(math.radians(self.angle)))
        else:
            self.speed_x = 0
            self.speed_y = 0
        self.move()

#группы
bullet_group = pygame.sprite.Group()
boxs_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()

#экземпляры класса
player = Player(image="player.png", position=(300, 400))
enemy = Enemy(position=(500, 500))
mka = Wearon(position=(320, 420), image="мка.png", name="пушка-мяушка", full_clip=30, clip=30)
gun = Wearon(position=(320, 500), image="gun.png", name="пистолет",full_clip=15, clip=15)
medkit = Medkit(position=(320, 460), image="medkit.png", name="аптечка", use_medkit=3)
clips = ClipsWearon(position=(320, 550), image="clips.png", clips_many=10, use_clips=3 ,name="патроны")
x, y = 200, 200
for box in range(5):
    x += 100
    cords = x, y
    box = Barrier(position=cords)
    boxs_group.add(box)

objects_group.add(medkit)
objects_group.add(mka)
objects_group.add(gun)
objects_group.add(clips)
enemy_group.add(enemy)

inventory_image = pygame.image.load('./data/inventory.png', )
inventor_image = pygame.transform.scale(inventory_image, (inventory_width, inventory_height))

#карта
map = load_image("map.png")
map = pygame.transform.scale(map, (1000, 1000))
map_rect = map.get_rect()

#иконка
programIcon = load_image('icon.png')
pygame.display.set_icon(programIcon)
inventory_open = False

#запуск игры
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                inventory_open = not inventory_open

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                player.inventory_cell = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_2:
                player.inventory_cell = 1

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                player.inventory_cell = 2
        
        if event.type == pygame.MOUSEBUTTONUP:
            if player.have_wearon() and type(player.inventory[player.inventory_cell]) == Wearon: #проверка оружия
                if player.inventory[player.inventory_cell].full_clip > 0:
                    player.inventory[player.inventory_cell].full_clip -= 1
                    bullet = Bullet(player.rect.center, player.angle)
                    bullet.speed_x = int(BULLET_SPEED * math.cos(math.radians(player.angle)))
                    bullet.speed_y = -int(BULLET_SPEED * math.sin(math.radians(player.angle)))
                    bullet_group.add(bullet)

            if type(player.inventory[player.inventory_cell]) == Medkit and player.inventory[player.inventory_cell].use_medkit > 0: #проверка на аптечку
                player.inventory[player.inventory_cell].use_medkit -= 1
                player.hp += 50

            if type(player.inventory[player.inventory_cell]) == ClipsWearon and player.inventory[player.inventory_cell].use_clips > 0:
                for obj in player.inventory:
                    if type(obj) == Wearon:
                        obj.full_clip += player.inventory[player.inventory_cell].clips_many
                player.inventory[player.inventory_cell].use_clips -= 1

        if event.type == pygame.KEYDOWN: #как мне гидры поюзать
            if event.key == pygame.K_e:
                for obj in objects_group:
                    if obj.use_me:
                        obj.kill()
                        for j in player.inventory:
                           if j == None:
                               player.inventory[player.inventory.index(None)] = obj
                               break

    camera_x = player.rect.x - WIDTH // 2 + 100 // 2
    camera_y = player.rect.y - HEIGHT // 2 + 100 // 2

    screen.fill(WHITE)

    screen.blit(map, (-camera_x, -camera_y))
    
    #заргузка ассетов
    player.move()
    player.angle_finder(pygame.mouse.get_pos())

    enemy_group.update(player, (player.rect.x - camera_x + 30, player.rect.y - camera_y + 30))
    
    custom_draw(bullet_group)
    bullet_group.update()

    custom_draw(boxs_group)
    boxs_group.update()

    custom_draw(objects_group)
    objects_group.update()

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

pygame.quit()
