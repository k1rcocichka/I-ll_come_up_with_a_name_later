import pygame
import math
import os
import sys
import random
from settings import *
from PIL import Image


#загрузка лвлов
level_1_data = {
    "enemies": [
        {"position": (700, 450)},
        {"position": (700, 550)},
        {"position": (700, 650)}
    ],
    "barriers": [
        {"position": (300, 200), "image": "box.png"},
        {"position": (400, 200), "image": "box.png"},
        {"position": (500, 200), "image": "box.png"}
    ],
    "boxs": [
        {"position": (300, 600), "image": "box.png", "image_update": "wreckage.png"},
        {"position": (400, 600), "image": "box.png", "image_update": "wreckage.png"},
        {"position": (500, 600), "image": "box.png", "image_update": "wreckage.png"},
    ],
    "lights": [
        {
            "position": (600, 450),
            "image": "box.png",
            "radius": 200,
            "intensity": 250,
            "switch": True
        },
    ],
    "npcs": [
        {
            "position": (500, 400),
            "image": "stone.png",
            "name": "Лесник",
            "dialogues": [
                "Эй, путник! Ты не должен быть здесь...",
                "Этот дом проклят. Уходи, пока не поздно.",
                "Если ты настаиваешь, ищи ключ в доме.",
                "Но помни: то, что в подвале, лучше оставить в покое."
            ]
        }

    ],
    "objects": [
        {
            "type": "weapon",
            "position": (320, 420),
            "image": "assault.png",
            "name": "винтовка",
            "full_clip": 30,
            "clip": 30,
            "damage": 20,
            "weight": 80,
            "height": 150
        },
        {
            "type": "weapon",
            "position": (320, 340),
            "image": "gun.png",
            "name": "пистолет",
            "full_clip": 15,
            "clip": 15,
            "damage": 10,
            "weight": 60,
            "height": 60
        },
        {
            "type": "weapon",
            "position": (320, 300),
            "image": "shotgun.png",
            "name": "дробаш",
            "full_clip": 8,
            "clip": 8,
            "damage": 30,
            "weight": 50,
            "height": 100
        },
        {
            "type": "knife",
            "position": (320, 380),
            "image": "knife.png",
            "name": "нож",
        },
        {
            "type": "medkit",
            "position": (320, 460),
            "image": "medkit.png",
            "use_medkit": 3,
            "name": "аптечка"
        },
        {
            "type": "clips",
            "position": (320, 500),
            "image": "clips.png",
            "clips_many": 10,
            "use_clips": 3,
            "name": "патроны"
        },
        {
            "type": "fumo",
            "position": (200, 400),
            "image": "fumo.png",
            "name": "fumo",
            "sound": "data/baka.wav",
            "num": 1
        }
    ]
}

#создание игры
HIT_CLOCK = 400

pygame.init() 
clock = pygame.time.Clock()
screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption(TITLE)
font = pygame.font.SysFont('Bleeker Cyrillic', 60)


def indicator():
    screen.blit(player.hp_bar, (0, 350))
    lost_hp = pygame.draw.rect(screen, 'grey', (40, 388, 10, 190 - player.hp))
    lost_stamina = pygame.draw.rect(screen, 'grey', (53, 388, 10, 190 - player.stamina))

    if cells[player.inventory_cell].item is not None:
        if type(cells[player.inventory_cell].item.item_type) == Wearon:
                text = f"{cells[player.inventory_cell].item.item_type.clip}/{cells[player.inventory_cell].item.item_type.full_clip}"
                text = font.render(text, True, (0, 0, 0))
                screen.blit(text, (450, 520))

        if type(cells[player.inventory_cell].item.item_type) == Medkit:
            text = f"{cells[player.inventory_cell].item.item_type.use_medkit}"
            text = font.render(text, True, (0, 0, 0))
            screen.blit(text, (450, 520))

        if type(cells[player.inventory_cell].item.item_type) == ClipsWearon:
            text = f"{cells[player.inventory_cell].item.item_type.use_clips}"
            text = font.render(text, True, (0, 0, 0))
            screen.blit(text, (450, 520))

        if type(cells[player.inventory_cell].item.item_type) == Knife:
            text = f"1/1"
            text = font.render(text, True, (0, 0, 0))
            screen.blit(text, (450, 520))

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
        image = pygame.transform.scale(image, (60, 60))
        self.sprite = image
        self.rect = self.sprite.get_rect()
        self.rect.center = position
        self.sprite_e = Object.image_e
        self.rect_e = self.sprite_e.get_rect()
        self.rect_e.center = position

        self.use_me = False
        self.name = name

    def draw(self):
        screen.blit(self.sprite, (self.rect.x - camera.camera_x, self.rect.y - camera.camera_y))

    def use(self):
        if (player.rect.x > self.rect.x - 50 and player.rect.y > self.rect.y - 50) and (player.rect.x < self.rect.x + 50 and player.rect.y < self.rect.y + 50):
            screen.blit(self.sprite_e, (self.rect_e.x - camera.camera_x, self.rect_e.y - camera.camera_y - 40))
            self.use_me = True
        else:
            self.use_me = False

    def update(self):
        self.use()


class Wearon(Object):
    """класс оружия"""
    def __init__(self, position, image, name, full_clip, damage, clip, height, weight, *groups):
        super().__init__(position, image, name, *groups)
        image = load_image(image)
        image = pygame.transform.scale(image, (height, weight))
        self.sprite = image
        self.rect = self.sprite.get_rect()
        self.rect.center = position
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
        if self.rect.right < 0 or self.rect.left > WIDTH + camera.camera_x or self.rect.top > HEIGHT + camera.camera_y or self.rect.bottom < 0:
            self.kill()
        
        for box in level.boxes:
            if self.rect.colliderect(box.rect) and box.hp > 0:
                box.hp = box.hp - 10
                self.kill()

        for barrier in level.barriers:
            if self.rect.colliderect(barrier.rect):
                self.kill()

        for light in level.lights:
            if self.rect.colliderect(light.rect):
                self.kill()
        
    def draw(self):
        """рисууем пулю"""
        rotate_image = pygame.transform.rotate(self.sprite, self.angle)
        rotate_rect = rotate_image.get_rect(center=self.rect.center)
        screen.blit(rotate_image, (rotate_rect.x - camera.camera_x, rotate_rect.y - camera.camera_y))


class Knife(Object):
    def __init__(self, position, image, name, *groups):
        super().__init__(position, image, name, *groups)


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
        screen.blit(self.sprite, (self.rect.x - camera.camera_x, self.rect.y - camera.camera_y))


class Player():
    """класс игрока"""
    def __init__(self, image, position):
        self.sprite = load_image(image)
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))
        self.rect = self.sprite.get_rect()
        self.rect.inflate_ip(-50, -50)
        self.mask = pygame.mask.from_surface(self.sprite)

        self.run = False
        self.inventory_cell = 0
        self.rect.center = position
        self.speed_x = 2
        self.speed_y = 2
        self.angle = 0
        self.hp = 190
        self.stamina = 190
        self.player_hit_clock = 0
        self.player_sprint_clock = 0
        self.death = False

        self.attack_range = 50  # Расстояние атаки
        self.attack_damage = 30
        self.detection_radius = 100
        self.player_melle_tick = 0

        self.timer = 0 # обнуляем начальное значение для отсчета
        pygame.time.set_timer(pygame.USEREVENT, 1000) # запускаем таймер (в милисекундах) на срабатывание каждую секунд

        self.inventory_sprite = load_image("inventory.png")
        self.inventory_sprite = pygame.transform.scale(self.inventory_sprite, (600, 600))
        
        self.hp_bar = load_image("hp_bar.png")
        self.hp_bar = pygame.transform.scale(self.hp_bar, (250, 250))
        self.start_ticks = pygame.time.get_ticks()

    """отрисовка поворота"""
    def draw(self):
        rotate_image = pygame.transform.rotate(self.sprite, self.angle)
        rotate_rect = rotate_image.get_rect(center=self.rect.center)
        screen.blit(rotate_image, (rotate_rect.x - camera.camera_x, rotate_rect.y - camera.camera_y))

        if DISPLAY_iNVENTORY:
            screen.blit(self.inventory_sprite, (0, 0))

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
        if key[pygame.K_LSHIFT] and self.stamina > 0:
            time_now = pygame.time.get_ticks()
            if time_now > self.player_sprint_clock:
                self.player_sprint_clock = time_now + 1
                self.stamina -= 1
            if self.stamina > 20:
                self.speed_x = 4
                self.speed_y = 4
        else:
            time_now = pygame.time.get_ticks()
            if time_now > self.player_sprint_clock and self.stamina < 190:
                self.player_sprint_clock = time_now + 20
                self.stamina += 1
            self.speed_x = 2
            self.speed_y = 2
        self.border()

        for box in level.boxes:
            if self.rect.colliderect(box.rect) and box.hp > 0:
                self.rect.center = original_position

        for barrier in level.barriers:
            if self.rect.colliderect(barrier.rect):
                self.rect.center = original_position

        for enemy in level.enemies:
            if player.rect.colliderect(enemy) and enemy.hp > 0:
                self.rect.center = original_position

        for light in level.lights:
            if self.rect.colliderect(light.rect):
                self.rect.center = original_position

        for npc in level.npcs:
            if self.rect.colliderect(npc.rect):
                self.rect.center = original_position

        if self.hp <= 0:
            self.death = True

    def melee_attack(self):
        # Анимация рукопашной атаки
        if type(self.inventory[self.inventory_cell]) == Knife:
            time_now = pygame.time.get_ticks()
            if time_now > self.player_melle_tick:
                self.player_melle_tick = time_now + 700
                self.is_attacking = True
                self.check_melee_hit()

    def check_melee_hit(self):
        radius_surface = pygame.Surface((self.detection_radius * 2, self.detection_radius * 2), pygame.SRCALPHA)
        radius = pygame.draw.circle(radius_surface, (255, 0, 0, 50), (self.detection_radius, self.detection_radius), self.detection_radius)
        screen.blit(radius_surface, (self.rect.centerx - self.detection_radius - camera.camera_x, self.rect.centery - self.detection_radius - camera.camera_y))
        # Проверка попадания по врагамr
        for enemy in level.enemies:
            distance_to_player = math.hypot(
                enemy.rect.centerx - self.rect.centerx,
                enemy.rect.centery - self.rect.centery
            )      
            if distance_to_player <= self.detection_radius:
                enemy.hp -= self.attack_damage
    
    """штука для отслежки курсора"""
    def angle_finder(self, target_pos):
        d_x = target_pos[0] - self.rect.centerx + camera.camera_x
        d_y = target_pos[1] - self.rect.centery + camera.camera_y
        self.angle =- math.degrees(math.atan2(d_y, d_x))

    """ограничитель"""
    def border(self):
        self.rect.x = max(0, min(self.rect.x, level.map_rect.width - self.sprite.get_height()))
        self.rect.y = max(0, min(self.rect.y, level.map_rect.height - self.sprite.get_width()))

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
        screen.blit(self.sprite, (self.rect.x - camera.camera_x, self.rect.y - camera.camera_y))


class Light(Barrier):
    def __init__(self, position, image, radius, intensity, switch, *group):
        super().__init__(position, image, *group)
        self.switch = switch
        self.position = position
        self.radius = radius
        self.intensity = intensity
        self.light_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        self.create_light()

    def create_light(self):
        """Создает поверхность с градиентным освещением."""
        for i in range(self.radius, 0, -1):
            alpha = int(self.intensity * (1 - i / self.radius))
            if alpha < 0:
                alpha = 0
            pygame.draw.circle(self.light_surface, (255, 255, 255, alpha), (self.radius, self.radius), i)

    def draw(self):
        """Отрисовывает источник света на экране."""
        screen.blit(self.sprite, (self.rect.x - camera.camera_x, self.rect.y - camera.camera_y))
        if alpha_.current_phase != "day" and self.switch:
            screen.blit(self.light_surface, (self.position[0] - self.radius - camera.camera_x + 5, self.position[1] - self.radius - camera.camera_y + 5))


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
            screen.blit(self.sprite_update, (self.rect_update.x - camera.camera_x, self.rect_update.y - camera.camera_y))
        else:
            screen.blit(self.sprite, (self.rect.x - camera.camera_x, self.rect.y - camera.camera_y))


class Enemy(pygame.sprite.Sprite):
    """конструктор класса"""
    image = load_image("enemy.png")
    image = pygame.transform.scale(image, (100, 100))
    zombey_sprite = AnimatedSprite(
                    load_image("zombey_move.png"),
                    columns=17,
                    rows=1,
                    x=50,
                    y=50
                )
    def __init__(self, position, *group):
        super().__init__(*group)
        self.sprite = Enemy.image
        self.rect = self.sprite.get_rect()
        self.rect.inflate_ip(-50, -50)
        self.mask = pygame.mask.from_surface(self.sprite)

        self.sprite_zombie = Enemy.zombey_sprite
        self.image_zombie = self.zombey_sprite.image
        self.rect_zombie = self.image_zombie.get_rect()
        self.rect_zombie.center = position

        self.can_move = True
        self.enemy_tick = 0
        self.rect.center = position
        self.speed_x_ = 3
        self.speed_y_ = 3
        self.angle = 0
        self.hp = 100
        self.detection_radius = 200
        self.damage = 1
        self.move_to_player = False
        self.position = position
        self.random_move_time = random.randint(200, 400)

    def update(self, target, target_pos):
        """рисуем врага"""
        self.target(target_pos)
        rotate_image = pygame.transform.rotate(self.sprite, self.angle)
        rotate_rect = rotate_image.get_rect(center=self.rect.center)
        if self.move_to_player:
            self.sprite_zombie.update()
            self.image_zombie = self.sprite_zombie.image
            self.image_zombie = pygame.transform.scale(self.image_zombie, (100, 100))
            self.rect_zombie = self.image_zombie.get_rect()
            self.rect_zombie.center = self.rect.center
            rotate_image = pygame.transform.rotate(self.image_zombie, self.angle)
            rotate_rect = rotate_image.get_rect(center=self.rect.center)
            screen.blit(rotate_image, (rotate_rect.x - camera.camera_x, rotate_rect.y - camera.camera_y))
        else:
            screen.blit(rotate_image, (rotate_rect.x - camera.camera_x, rotate_rect.y - camera.camera_y))

        fill = (self.hp / 100) * 60
        
        bar_hp = pygame.draw.rect(screen, LIGHTRED, (rotate_rect.x - camera.camera_x + 30, rotate_rect.y - camera.camera_y, 60, 10))
        lost_hp = pygame.draw.rect(screen, LIGHTGREEN, (rotate_rect.x - camera.camera_x + 30, rotate_rect.y - camera.camera_y, fill, 10))
        outline = pygame.draw.rect(screen, LIGHTGREY, (rotate_rect.x - camera.camera_x + 30, rotate_rect.y - camera.camera_y, 60, 10), 2)
        
        if self.hp <= 0:
            self.kill()

    def move(self):
        """логику позже"""
        original_position = self.rect.center
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.rect_zombie.x += self.speed_x
        self.rect_zombie.y += self.speed_y

        for box in level.boxes:
            if self.rect.colliderect(box.rect) and box.hp > 0:
                self.rect.center = original_position

        for barrier in level.barriers:
            if self.rect.colliderect(barrier.rect):
                self.rect.center = original_position
        
        for light in level.lights:
            if self.rect.colliderect(light.rect):
                self.rect.center = original_position

        for enemy_ in level.enemies:
            if self.rect.colliderect(enemy_.rect) and enemy_.rect_zombie.center != self.rect_zombie.center:
                self.rect.center = original_position

        if self.rect.colliderect(player) and self.hp > 0 and player.hp > 0:
            time_now = pygame.time.get_ticks()
            self.rect.center = original_position
            if time_now > player.player_hit_clock:
                player.hp = player.hp - self.damage
                player.player_hit_clock = time_now + HIT_CLOCK
                # Создание частиц крови
                for _ in range(20):  # Создаем 20 частиц
                    blood_particles.add(BloodParticle(image="blood.png", position=player.rect.center))

        for bullet in bullet_group:
            if self.rect.colliderect(bullet) and self.hp >= 0:
                self.hp = self.hp - cells[player.inventory_cell].item.item_type.damage
                # Создание частиц крови
                for _ in range(20):  # Создаем 20 частиц
                    blood_particles.add(BloodParticle(image="blood.png", position=self.rect.center))
                bullet.kill()

    def border(self):
        """ограничитель"""
        self.rect.x = max(0, min(self.rect.x, level.map_rect.width - self.sprite.get_height()))
        self.rect.y = max(0, min(self.rect.y, level.map_rect.height - self.sprite.get_width()))

    def angle_finder(self, target_pos):
        """поиск врага"""
        d_x = target_pos[0] - self.rect.centerx + camera.camera_x
        d_y = target_pos[1] - self.rect.centery + camera.camera_y
        self.angle =- math.degrees(math.atan2(d_y, d_x))

    def target(self, target_pos):
        radius_surface = pygame.Surface((self.detection_radius * 2, self.detection_radius * 2), pygame.SRCALPHA)
        radius = pygame.draw.circle(radius_surface, (255, 0, 0, 50), (self.detection_radius, self.detection_radius), self.detection_radius)
        screen.blit(radius_surface, (self.rect.centerx - self.detection_radius - camera.camera_x, self.rect.centery - self.detection_radius - camera.camera_y))
        distance_to_player = math.hypot(
            player.rect.centerx - self.rect.centerx,
            player.rect.centery - self.rect.centery
        )
        if distance_to_player <= self.detection_radius and not player.death:
            self.angle_finder(target_pos)
            self.speed_x = int(self.speed_x_ * math.cos(math.radians(self.angle)))
            self.speed_y = -int(self.speed_y_ * math.sin(math.radians(self.angle)))
            self.move_to_player = True
        else:
            self.random_move_time += 1
            if self.random_move_time >= 300:
                self.speed_x = int(self.speed_x_ * math.cos(math.radians(self.angle)))
                self.speed_y = -int(self.speed_y_ * math.sin(math.radians(self.angle)))
                self.move_to_player = True
                if self.can_move:
                    self.angle = random.randint(-180, 180)
                    self.can_move = False
                if self.random_move_time >= 330:
                    self.random_move_time = 0
                    self.can_move = True
            else:
                self.speed_x = 0
                self.speed_y = 0
                self.move_to_player = False
        self.move()

    def draw(self):
        pass


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
    def __init__(self, position, image, name, sound, num, *groups):
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
        self.num = num

    def draw(self):
        self.sprite_fumo.update()
        self.sprite = self.sprite_fumo.image
        self.sprite = pygame.transform.scale(self.sprite, (100, 100))
        self.rect = self.sprite.get_rect()
        self.rect.center = self.position
        screen.blit(self.sprite, (self.rect.x - camera.camera_x, self.rect.y - camera.camera_y))

    def use(self):
        if (player.rect.x > self.rect.x - 50 and player.rect.y > self.rect.y - 50) and (player.rect.x < self.rect.x + 50 and player.rect.y < self.rect.y + 50):
            screen.blit(self.sprite_e, (self.rect_e.x - camera.camera_x, self.rect_e.y - camera.camera_y - 40))
            self.use_me = True
        else:
            self.use_me = False

    def update(self):
        self.use()

    def sound(self):
        self.sound.play()

    def save(self):
        with open("save.txt") as file:
            lines = file.readlines()
        # Split the lines by '$'
        lines_split = [line for line in lines]

        lines_split[1] = lines_split[1].split()
        lines_split[1][self.num - 1] = '1'
        lines_split[1] = ' '.join(lines_split[1])

        print(lines_split)

        # Write the file
        with open('save.txt', 'w') as file:
            file.writelines(lines_split)


class Camera():
    def __init__(self):
        self.camera_x = 0
        self.camera_y = 0

    def update(self):
        self.camera_x = player.rect.x - WIDTH // 2 + 100 // 2
        self.camera_y = player.rect.y - HEIGHT // 2 + 100 // 2


class TimeOfDay:
    def __init__(self):
        self.phases = {
            "morning": {"length": 10000, "start_alpha": 210, "end_alpha": 128},
            "day": {"length": 10000, "start_alpha": 128, "end_alpha": 0},
            "evening": {"length": 10000, "start_alpha": 0, "end_alpha": 128},
            "night": {"length": 10000, "start_alpha": 128, "end_alpha": 210},
        }
        self.current_phase = "morning"
        self.current_time = 0

    def update(self, dt):
        self.current_time += dt
        phase_data = self.phases[self.current_phase]
        if self.current_time >= phase_data["length"]:
            self.next_phase()

    def next_phase(self):
        phases = list(self.phases.keys())
        current_index = phases.index(self.current_phase)
        next_index = (current_index + 1) % len(phases)
        self.current_phase = phases[next_index]
        self.current_time = 0

    def get_alpha(self):
        phase_data = self.phases[self.current_phase]
        progress = self.current_time / phase_data["length"]
        return phase_data["start_alpha"] + (phase_data["end_alpha"] - phase_data["start_alpha"]) * progress


class Level:
    def __init__(self, level_data, width, height, map_im):
        """
        Инициализация уровня.
        :param level_data: Данные уровня (враги, барьеры, объекты и т.д.)
        """
        self.map = load_image(map_im)
        self.map = pygame.transform.scale(self.map, (width, height))
        self.map_rect = self.map.get_rect()

        self.level_data = level_data
        self.enemies = pygame.sprite.Group()
        self.barriers = pygame.sprite.Group()
        self.objects = pygame.sprite.Group()
        self.boxes = pygame.sprite.Group()
        self.lights = pygame.sprite.Group()
        self.npcs = pygame.sprite.Group()
        self.load_level()

    def load_level(self):
        """
        Загрузка уровня на основе данных.
        """
        # Загрузка врагов
        for enemy_data in self.level_data.get("enemies", []):
            enemy = Enemy(position=enemy_data["position"])
            self.enemies.add(enemy)

        # Загрузка барьеров
        for barrier_data in self.level_data.get("barriers", []):
            barrier = Barrier(
                position=barrier_data["position"],
                image=barrier_data["image"]
            )
            self.barriers.add(barrier)

        # Загрузка света
        for light_data in self.level_data.get("lights", []):
            light = Light(
                position=light_data["position"],
                image=light_data["image"],
                radius=light_data["radius"],
                intensity=light_data["intensity"],
                switch=light_data["switch"]
            )
            self.lights.add(light)

        # Загрузка боксов
        for boxs_data in self.level_data.get("boxs", []):
            box = Box(
                position=boxs_data["position"],
                image=boxs_data["image"],
                image_update=boxs_data["image_update"]
            )
            self.boxes.add(box)

        for npc_data in self.level_data.get("npcs", []):
            npc = NPC(
                position=npc_data["position"],
                image=npc_data["image"],
                name=npc_data["name"],
                dialogues=npc_data["dialogues"]
            )
            self.npcs.add(npc)

        # Загрузка объектов
        for object_data in self.level_data.get("objects", []):
            if object_data["type"] == "weapon":
                obj = Wearon(
                    position=object_data["position"],
                    image=object_data["image"],
                    name=object_data["name"],
                    full_clip=object_data["full_clip"],
                    clip=object_data["clip"],
                    damage=object_data["damage"],
                    height=object_data["height"],
                    weight=object_data["weight"]
                )
            elif object_data["type"] == "medkit":
                obj = Medkit(
                    position=object_data["position"],
                    image=object_data["image"],
                    use_medkit=object_data["use_medkit"],
                    name=object_data["name"]
                )
            elif object_data["type"] == "clips":
                obj = ClipsWearon(
                    position=object_data["position"],
                    image=object_data["image"],
                    clips_many=object_data["clips_many"],
                    use_clips=object_data["use_clips"],
                    name=object_data["name"]
                )
            elif object_data["type"] == "knife":
                obj = Knife(
                    position=object_data["position"],
                    image=object_data["image"],
                    name=object_data["name"]
                )
            elif object_data["type"] == "fumo":
                fumo_sprite = AnimatedSprite(
                    load_image(object_data["image"]),
                    columns=11,
                    rows=1,
                    x=50,
                    y=50
                )
                obj = Fumo(
                    position=object_data["position"],
                    image=fumo_sprite,
                    name=object_data["name"],
                    sound=object_data["sound"],
                    num=object_data["num"]
                )
            self.objects.add(obj)

    def update(self):
        """
        Обновление всех объектов уровня.
        """
        self.enemies.update(player, (player.rect.x - camera.camera_x + 30, player.rect.y - camera.camera_y + 30))
        self.barriers.update()
        self.objects.update()
        self.boxes.update()
        self.lights.update()
        self.npcs.update()

    def draw(self, screen):
        """
        Отрисовка всех объектов уровня.
        """
        custom_draw(self.enemies)
        custom_draw(self.barriers)
        custom_draw(self.objects)
        custom_draw(self.boxes)
        custom_draw(self.npcs)
        player.draw()
        custom_draw(self.lights)


class NPC(pygame.sprite.Sprite):
    def __init__(self, position, image, name, dialogues, *groups):
        super().__init__(*groups)
        self.image = load_image(image)
        self.image = pygame.transform.scale(self.image, (50, 50))  # Размер NPC
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.name = name
        self.dialogues = dialogues  # Список строк с диалогами
        self.current_dialogue = 0
        self.is_talking = False

    def draw(self):
        screen.blit(self.image, (self.rect.x - camera.camera_x, self.rect.y - camera.camera_y))

    def interact(self):
        """Начать диалог с NPC."""
        self.is_talking = True
        self.current_dialogue = 0

    def next_dialogue(self):
        """Перейти к следующему диалогу."""
        if self.current_dialogue < len(self.dialogues) - 1:
            self.current_dialogue += 1
        else:
            self.is_talking = False  # Завершить диалог

    def draw_dialogue(self):
        """Отрисовка диалога на экране."""
        if self.is_talking:
            dialogue_box = pygame.Surface((WIDTH - 100, 100))
            dialogue_box.fill((0, 0, 0))
            dialogue_box.set_alpha(200)
            screen.blit(dialogue_box, (50, HEIGHT - 150))

            font = pygame.font.SysFont('Arial', 24)
            text = font.render(self.dialogues[self.current_dialogue], True, (255, 255, 255))
            screen.blit(text, (70, HEIGHT - 130))

            # Подсказка для продолжения диалога
            hint = font.render("Нажмите E для продолжения...", True, (255, 255, 255))
            screen.blit(hint, (70, HEIGHT - 100))


cells = [Cell(x, y, 'inventory') for x, y in inventory_positions] + \
        [Cell(x, y, 'armor') for x, y in armor_positions] + \
        [Cell(x, y, 'weapon') for x, y in weapon_positions]


level = Level(level_1_data, 1000, 1000, "map.png")

#группы
bullet_group = pygame.sprite.Group()
blood_particles = pygame.sprite.Group()

#экземпляры класса
player = Player(image="player.png", position=(400, 400))

camera = Camera()
alpha_ = TimeOfDay()

inventory_image = pygame.image.load('./data/inventory.png', )
inventor_image = pygame.transform.scale(inventory_image, (inventory_width, inventory_height))

programIcon = load_image('icon.png')
pygame.display.set_icon(programIcon)

#запуск игры
def main_loop(running):
    inventory_open = False
    dragging_item = None
    original_cell = None
    current_npc = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_i:
                    inventory_open = not inventory_open
                elif event.key == pygame.K_1:
                    player.inventory_cell = 0
                elif event.key == pygame.K_2:
                    player.inventory_cell = 1
                elif event.key == pygame.K_3:
                    player.inventory_cell = 2
                elif event.key == pygame.K_r:
                    player.melee_attack()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    # Взаимодействие с NPC
                    if current_npc:
                        current_npc.next_dialogue()
                    else:
                        for npc in level.npcs:
                            if npc.rect.colliderect(player.rect):
                                current_npc = npc
                                current_npc.interact()
                                break    
                        

            if event.type == pygame.MOUSEBUTTONUP:
                handle_mouse_button_up(event)

            if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
                handle_interaction()

            if player.death:
                player.timer += 1
                if player.timer > 5:
                    pygame.time.set_timer(pygame.USEREVENT, 0)
                    return True

        alpha_.update(5)

        camera.update()
        screen.fill(WHITE)
        screen.blit(level.map, (-camera.camera_x, -camera.camera_y))

        player.move()
        player.angle_finder(pygame.mouse.get_pos())

        bullet_group.update()
        blood_particles.update()

        custom_draw(bullet_group)

        level.draw(screen)
        level.update()
        
        custom_draw(blood_particles)
        indicator()

        dark_surface = pygame.Surface((WIDTH, HEIGHT))
        dark_surface.fill(BLACK)
        dark_surface.set_alpha(alpha_.get_alpha())
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

        if current_npc:
            current_npc.draw_dialogue()

        pygame.display.flip()

        clock.tick(FPS)

    pygame.quit()


def handle_mouse_button_up(event):
    if cells[player.inventory_cell].item == None:
        pass
    elif type(cells[player.inventory_cell].item.item_type) == Wearon:
        if cells[player.inventory_cell].item.item_type.full_clip > 0:
            cells[player.inventory_cell].item.item_type.full_clip -= 1
            bullet = Bullet(player.rect.center, player.angle)
            bullet.speed_x = int(BULLET_SPEED * math.cos(math.radians(player.angle)))
            bullet.speed_y = -int(BULLET_SPEED * math.sin(math.radians(player.angle)))
            bullet_group.add(bullet)

    elif type(cells[player.inventory_cell].item.item_type) == Medkit and cells[player.inventory_cell].item.item_type.use_medkit > 0:
        cells[player.inventory_cell].item.item_type.use_medkit -= 1
        player.hp += 50

    elif type(cells[player.inventory_cell].item.item_type) == ClipsWearon and cells[player.inventory_cell].item.item_type.use_clips > 0:
        for obj in cells:
            if obj.item is not None:
                if type(obj.item.item_type) == Wearon:
                    obj.item.item_type.full_clip += cells[player.inventory_cell].item.item_type.clips_many
        cells[player.inventory_cell].item.item_type.use_clips -= 1


def handle_interaction():
    for obj in level.objects:
        if obj.use_me and type(obj) != Fumo:
            obj.kill()
            for n, cell in enumerate(cells):
                if cell.item is None:
                    item_sprite = pygame.transform.scale(obj.sprite, (36, 36))
                    item_ = Item(cells[n].rect.x, cells[n].rect.y, obj, item_sprite)
                    cells[n].item = item_
                    break
        if obj.use_me and type(obj) == Fumo:
            obj.save()
            obj.kill()
            obj.sound.play()


main_loop(True)