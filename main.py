import pygame
import math
import os
import sys
import random
from settings import *
from PIL import Image


#создание игры
HIT_CLOCK = 400

pygame.init() 
clock = pygame.time.Clock()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption(TITLE)
font = pygame.font.SysFont('serif', 50)

# Настройки времени суток
time_of_day = {
    "morning": {"length": 10000, "start_alpha": 210, "end_alpha": 128},  # Утро (10 секунд)
    "day": {"length": 100000, "start_alpha": 128, "end_alpha": 0},  # День (10 секунд)
    "evening": {"length": 10000, "start_alpha": 0, "end_alpha": 128},  # Вечер (10 секунд)
    "night": {"length": 10000, "start_alpha": 128, "end_alpha": 210},  # Ночь (10 секунд)
}
current_time = 0  # Текущее время в текущей фазе
current_phase = "morning"  # Текущая фаза времени суток

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

#ф-ция для анимации гифок
def split_animated_gif(gif_file_path):
    ret = []
    gif = Image.open(gif_file_path)
    for frame_index in range(gif.n_frames):
        gif.seek(frame_index)
        frame_rgba = gif.convert("RGBA")
        pygame_image = pygame.image.fromstring(
            frame_rgba.tobytes(), frame_rgba.size, frame_rgba.mode
        )
        ret.append(pygame_image)
    return ret

#для рисование групп
def custom_draw(group):
    for sprite in group:
        sprite.draw()


class Object(pygame.sprite.Sprite):
    """класс объктов"""
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
    """класс оружия"""
    def __init__(self, position, image, name, full_clip, damage, clip, *groups):
        super().__init__(position, image, name, *groups)
        self.full_clip = full_clip
        self.clip = clip
        self.damage = damage


class Medkit(Object):
    """класс аптечки"""
    def __init__(self, position, image, use_medkit, name, *groups):
        super().__init__(position, image, name,*groups)
        self.use_medkit = use_medkit


class ClipsWearon(Object):
    """класс магазин с патронами"""
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
            if self.rect.colliderect(box.rect) and box.hp > 0:
                box.hp = box.hp - 10
                print(box.hp)
                self.kill()

        for barrier in barrier_group:
            if self.rect.colliderect(barrier.rect):
                self.kill()
        
    def draw(self):
        """рисууем пулю"""
        rotate_image = pygame.transform.rotate(self.sprite, self.angle)
        rotate_rect = rotate_image.get_rect(center=self.rect.center)
        screen.blit(rotate_image, (rotate_rect.x - camera_x, rotate_rect.y - camera_y))


class AnimatedSprite(pygame.sprite.Sprite):
    """класс анимация"""
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__()
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


class BloodParticle(pygame.sprite.Sprite):
    """констурктор препятствий"""
    def __init__(self, position, image, *group):
        super().__init__(*group)
        image = load_image(image)
        image = pygame.transform.scale(image, (20, 20))
        self.sprite = image
        self.rect = self.sprite.get_rect()
        self.rect.inflate_ip(-20, -20)
        self.rect.center = position

        self.lifetime = random.randint(10, 20)  # Время жизни в кадрах
        self.angle = random.uniform(0, 2 * math.pi)  # Направление движения
        self.speed = random.uniform(1, 3)  # Скорость движения

    def update(self):
        # Движение частицы
        self.rect.x += math.cos(self.angle) * self.speed
        self.rect.y += math.sin(self.angle) * self.speed
        self.lifetime -= 1
        if self.lifetime == 0:
            self.kill()
        
    def draw(self):
        screen.blit(self.sprite, (self.rect.x - camera_x, self.rect.y - camera_y))


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
        self.player_hit_clock = 0
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
            if self.rect.colliderect(box.rect) and box.hp > 0:
                self.rect.center = original_position

        for barrier in barrier_group:
            if self.rect.colliderect(barrier.rect):
                self.rect.center = original_position

        for enemy in enemy_group:
            if player.rect.colliderect(enemy) and enemy.hp > 0:
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

    def have_wearon(self):
        if type(self.inventory[self.inventory_cell]) == Wearon:
            return True
        return False
        

class Barrier(pygame.sprite.Sprite):
    """констурктор препятствий"""
    def __init__(self, position, image, *group):
        super().__init__(*group)
        image = load_image(image)
        image = pygame.transform.scale(image, (80, 80))
        self.sprite = image
        self.rect = self.sprite.get_rect()
        self.rect.inflate_ip(-20, -20)
        self.rect.center = position

    def draw(self):
        screen.blit(self.sprite, (self.rect.x - camera_x, self.rect.y - camera_y))


class Box(Barrier):
    """класс лут боксов"""
    def __init__(self, position, image, image_update, *group):
        super().__init__(position, image, *group)
        image_update = load_image(image_update)
        image_update = pygame.transform.scale(image_update, (80, 80))
        self.sprite_update = image_update
        self.rect_update = self.sprite_update.get_rect()
        self.rect_update.center = position

        self.hp = 20
        self.destroy = False

    def update(self):   
        if self.hp <= 0:
            self.destroy = True

    def draw(self):
        if self.destroy:
            screen.blit(self.sprite_update, (self.rect_update.x - camera_x, self.rect_update.y - camera_y))
        else:
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
        if self.hp > 0:
            screen.blit(rotate_image, (rotate_rect.x - camera_x, rotate_rect.y - camera_y))

    def move(self):
        """логику позже"""
        original_position = self.rect.center
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        for box in boxs_group:
            if self.rect.colliderect(box.rect) and box.hp > 0:
                self.rect.center = original_position

        for barrier in barrier_group:
            if self.rect.colliderect(barrier.rect):
                self.rect.center = original_position

        if self.rect.colliderect(player) and self.hp > 0:
            time_now = pygame.time.get_ticks()
            self.rect.center = original_position
            if time_now > player.player_hit_clock:
                player.hp = player.hp - 10
                player.player_hit_clock = time_now + HIT_CLOCK
                # Создание частиц крови
                for _ in range(20):  # Создаем 20 частиц
                    blood_particles.add(BloodParticle(image="blood.png", position=player.rect.center))


        for bullets in bullet_group:
            if self.rect.colliderect(bullet) and self.hp >= 0:
                self.hp = self.hp - player.inventory[player.inventory_cell].damage
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
        if (player.rect.x > self.rect.x - 250 and player.rect.y > self.rect.y - 250) and (player.rect.x < self.rect.x + 250 and player.rect.y < self.rect.y + 250):
            self.angle_finder(target_pos)
            self.speed_x = int(self.speed_x_ * math.cos(math.radians(self.angle)))
            self.speed_y = -int(self.speed_y_ * math.sin(math.radians(self.angle)))
        else:
            self.speed_x = 0
            self.speed_y = 0
        self.move()


class Cell:
    """клас хз чего"""
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


class Item:
    """классы для предметов наверно"""
    def __init__(self, x, y, item_type, image):
        self.rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)
        self.item_type = item_type
        self.image = image

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Fumo(pygame.sprite.Sprite):
    """фумо фумо (коллекционки)"""
    image_e = load_image("e.png")
    image_e = pygame.transform.scale(image_e, (40, 40))
    def __init__(self, position, image, name, sound, *groups):
        super().__init__(*groups)
        self.sound = pygame.mixer.Sound(sound)
        self.position = position
        self.sprite_fumo = image
        self.sprite = self.sprite_fumo.image
        self.rect = self.sprite.get_rect()
        self.rect.center = self.position
        self.sprite_e = Fumo.image_e
        self.rect_e = self.sprite_e.get_rect()
        self.rect_e.center = self.position

        self.use_me = False
        self.name = name

    def draw(self):
        self.sprite_fumo.update()
        self.sprite = self.sprite_fumo.image
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))
        self.rect = self.sprite.get_rect()
        self.rect.center = self.position
        screen.blit(self.sprite, (self.rect.x - camera_x, self.rect.y - camera_y))

    def use(self):
        if (player.rect.x > self.rect.x - 50 and player.rect.y > self.rect.y - 50) and (player.rect.x < self.rect.x + 50 and player.rect.y < self.rect.y + 50):
            screen.blit(self.sprite_e, (self.rect_e.x - camera_x, self.rect_e.y - camera_y - 40))
            self.use_me = True
        else:
            self.use_me = False

    def update(self):
        self.use()

    def sound(self):
        self.sound.play()


cells = [Cell(x, y, 'inventory') for x, y in inventory_positions] + \
        [Cell(x, y, 'armor') for x, y in armor_positions] + \
        [Cell(x, y, 'weapon') for x, y in weapon_positions]

#группы
bullet_group = pygame.sprite.Group()
boxs_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()
objects_group = pygame.sprite.Group()
barrier_group = pygame.sprite.Group()
blood_particles = pygame.sprite.Group()

#экземпляры класса
player = Player(image="player.png", position=(400, 400))
enemy = Enemy(position=(700, 450))
mka = Wearon(position=(320, 420), image="мка.jpg", name="пушка-мяушка", full_clip=30, clip=30, damage=50)
gun = Wearon(position=(320, 500), image="gun.png", name="пистолет",full_clip=15, clip=15, damage=50)
medkit = Medkit(position=(320, 460), image="medkit.png", name="аптечка", use_medkit=3)
clips = ClipsWearon(position=(320, 550), image="clips.png", clips_many=10, use_clips=3 ,name="патроны")
fumo = AnimatedSprite(load_image("fumo.png"), 11, 1, 50, 50)
fumo = Fumo(position=(200, 400), image=fumo, name="fumo", sound="data/baka.wav")

x, y = 200, 200
for _ in range(5):
    x += 100
    cords = x, y
    barrier = Barrier(position=cords, image="box.png")
    barrier_group.add(barrier)

x, y = 200, 700
for _ in range(5):
    x += 100
    cords = x, y
    box = Box(position=cords, image="box.png", image_update="wreckage.png")
    boxs_group.add(box)

objects_group.add(medkit)
objects_group.add(mka)
objects_group.add(gun)
objects_group.add(clips)
enemy_group.add(enemy)
objects_group.add(fumo)

inventory_image = pygame.image.load('./data/inventory.png', )
inventor_image = pygame.transform.scale(inventory_image, (inventory_width, inventory_height))

#карта
map = load_image("map.png")
map = pygame.transform.scale(map, (2000, 2000))

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
pygame.display.set_icon(programIcon)
inventory_open = False
running = True
dragging_item = None
original_cell = None

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

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                player.inventory_cell = 3
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                player.inventory_cell = 4

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                player.inventory_cell = 5

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                player.inventory_cell = 6

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_3:
                player.inventory_cell = 7

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
                    if obj.use_me and type(obj) != Fumo:
                        obj.kill()
                        for j in player.inventory:
                           if j == None:
                               player.inventory[player.inventory.index(None)] = obj
                               break
                    if obj.use_me and type(obj) == Fumo:
                        obj.kill()
                        obj.sound.play()

    camera_x = player.rect.x - WIDTH // 2 + 100 // 2
    camera_y = player.rect.y - HEIGHT // 2 + 100 // 2

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

    phase_data = time_of_day[current_phase]
    progress = current_time / phase_data["length"]  # Прогресс текущей фазы (от 0 до 1)
    alpha = phase_data["start_alpha"] + (phase_data["end_alpha"] - phase_data["start_alpha"]) * progress

    # Создание затемняющего слоя
    dark_surface = pygame.Surface((WIDTH, HEIGHT))
    dark_surface.fill(BLACK)
    dark_surface.set_alpha(alpha)  # Установка прозрачности  # Наложение слоя

    screen.fill(WHITE)
    screen.blit(map, (-camera_x, -camera_y))
    
    #заргузка ассетов
    player.move()
    player.angle_finder(pygame.mouse.get_pos())
    
    custom_draw(bullet_group)
    bullet_group.update()

    custom_draw(objects_group)
    objects_group.update()

    custom_draw(boxs_group)
    boxs_group.update()

    custom_draw(barrier_group)
    barrier_group.update()

    custom_draw(blood_particles)
    blood_particles.update()

    enemy_group.update(player, (player.rect.x - camera_x + 30, player.rect.y - camera_y + 30))

    player.draw()

    screen.blit(dark_surface, (0, 0))
    
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

pygame.quit()