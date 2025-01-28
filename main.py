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

#commit шедевр


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
        
class Cell:
    def __init__(self, x, y, cell_type):
        self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        self.cell_type = cell_type
        self.item = None

    def draw(self, screen):
        # Создаем полностью прозрачный цвет
        color = (GRAY[0], GRAY[1], GRAY[2], 0)  # Полностью прозрачный
        surface = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        surface.fill(color)
        screen.blit(surface, self.rect.topleft)

        if self.item:
            self.item.draw(screen)

# Классы для предметов
class Item:
    def __init__(self, x, y, item_type, image):
        self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        self.item_type = item_type
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, self.rect)


cells = [Cell(x, y, 'inventory') for x, y in inventory_positions] + \
        [Cell(x, y, 'armor') for x, y in armor_positions] + \
        [Cell(x, y, 'weapon') for x, y in weapon_positions]

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

inventory_image = pygame.image.load('./data/inventory.png', )
inventor_image = pygame.transform.scale(inventory_image, (inventory_width, inventory_height))
player = Player(image="player.png", position=(300, 400))
enemy = Enemy(image="enemy.png", position=(500, 500))
map = load_image("map.png")
map = pygame.transform.scale(map, (1000, 1000))


armor_image = load_image("shotgun.png")
weapon_image = load_image("M4A1-S.png")

armor_image = pygame.transform.scale(armor_image, (36, 36))
weapon_image = pygame.transform.scale(weapon_image, (36, 36))

# Создание предметов
armor_item = Item(cells[0].rect.x, cells[0].rect.y,'armor', armor_image)
weapon_item = Item(cells[1].rect.x, cells[1].rect.y,'weapon', weapon_image)

# Помещение предметов в ячейки
cells[0].item = armor_item
cells[1].item = weapon_item
map_rect = map.get_rect()

programIcon = load_image('icon.png')
inventory_open = False
running = True
dragging_item = None
original_cell = None


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

    enemy.update(pygame.mouse.get_pos(), player)
    
    bullet_group.update()
    custom_draw(bullet_group)

    boxs_group.draw(map)

    player.draw()

    if inventory_open:
        # Отображаем инвентарь
        screen.blit(inventor_image, (center_x, center_y))
        if event.type == pygame.MOUSEBUTTONDOWN:
            for cell in cells:
                if cell.item and cell.item.rect.collidepoint(event.pos):
                    dragging_item = cell.item
                    original_cell = cell
                    cell.item = None
                    break

            if event.type == pygame.MOUSEBUTTONDOWN:
                for cell in cells:
                    if cell.item and cell.item.rect.collidepoint(event.pos):
                        dragging_item = cell.item
                        original_cell = cell
                        cell.item = None
                        break

            if event.type == pygame.MOUSEBUTTONUP:
                if dragging_item:
                    placed = False
                    for cell in cells:
                        if cell.rect.collidepoint(event.pos):
                            if cell.cell_type != 'inventory' and cell.cell_type == dragging_item.item_type:
                                dragging_item.rect.topleft = cell.rect.topleft
                                cell.item = dragging_item
                                placed = True
                                break
                            elif cell.cell_type == 'inventory':
                                if cell.item is None:  # Если ячейка пустая
                                    dragging_item.rect.topleft = cell.rect.topleft
                                    cell.item = dragging_item
                                    placed = True
                                    break
                                else:  # Если ячейка занята, возвращаем предмет обратно
                                    original_cell.item = dragging_item
                                    dragging_item.rect.topleft = (original_cell.rect.x, original_cell.rect.y)
                                    placed = True
                                    break

                    if not placed and original_cell:
                        dragging_item.rect.topleft = (original_cell.rect.x, original_cell.rect.y)
                        original_cell.item = dragging_item

                    dragging_item = None
                    original_cell = None

            if event.type == pygame.MOUSEMOTION:
                if dragging_item:
                    dragging_item.rect.topleft = event.pos


        # Отрисовка ячеек
        for cell in cells:
            cell.draw(screen)

        # Отрисовка перетаскиваемого предмета, если он есть
        if dragging_item:
            screen.blit(dragging_item.image, dragging_item.rect)

        pygame.display.flip()

        if event.type == pygame.MOUSEBUTTONUP:
            if dragging_item:
                placed = False
                for cell in cells:
                    if cell.rect.collidepoint(event.pos):
                        if cell.item is None:  # Если ячейка пустая
                            dragging_item.rect.topleft = cell.rect.topleft
                            cell.item = dragging_item
                            placed = True
                            break
                        else:  # Если ячейка занята, возвращаем предмет обратно
                            original_cell.item = dragging_item
                            dragging_item.rect.topleft = (original_cell.rect.x, original_cell.rect.y)
                            placed = True
                            break

                if not placed and original_cell:
                    dragging_item.rect.topleft = (original_cell.rect.x, original_cell.rect.y)
                    original_cell.item = dragging_item

                dragging_item = None
                original_cell = None

        if event.type == pygame.MOUSEMOTION:
            if dragging_item:
                dragging_item.rect.topleft = event.pos



    pygame.display.flip()

    clock.tick(FPS)

# ИГРА САМА НЕ ЗАКРЫВАТЕСЯ ХЕЛП
pygame.quit()
