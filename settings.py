import pygame


#разные цвета
WHITE = (255, 255, 255)
BLACK =(0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
DARKGREEN = (0, 102, 0)
BLUE = (0, 0, 255)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
YELLOW = (255, 255, 0)
GOLD = (255,215,0)
GRAY = (128, 128, 128)
LIGHTRED = (180, 76, 67)
LIGHTGREEN = (71, 167, 106)

#конфиг
TITLE = "Cursed wood"
WIDTH = 600
HEIGHT = 600
inventory_width = 500
inventory_height = 500
FPS = 60
BGCOLOR = DARKGREY

#настройки игрока
DEFUALT_HP = 100
DEFUALT_PROT = 100
DEFUALT_ATK = 10

STATPOSX = 50
TILESIZE = 32
UIHEIGTH = 300
INVTILESIZE = 48
COINOFFSET = 4
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

BULLET_SPEED = 30
DISPLAY_iNVENTORY = False
inventory_open = False
center_x = (WIDTH - inventory_width) // 2
center_y = (HEIGHT - inventory_height) // 2

# Константы
CELL_SIZE = 36
GRID_ORIGIN = (50, 50)


# Создание ячеек инвентаря
inventory_positions = [
    (137, 345), (179, 345), (221, 345), (262, 345), (304, 345), (345, 345), (387, 345), (429, 345),
    (137, 387), (179, 387), (221, 387), (262, 387), (304, 387), (345, 387), (387, 387), (429, 387),
    (137, 429), (179, 429), (221, 429), (262, 429), (304, 429), (345, 429), (387, 429), (429, 429),
    (137, 471), (179, 471), (221, 471), (262, 471), (304, 471), (345, 471), (387, 471), (429, 471),
]

armor_positions = [
    (387, 261), (429, 261),
    (387, 137),  # большая ячейка для брони
]

weapon_positions = [
    (137, 137), (179, 137), (221, 137),
    (137, 179), (179, 179), (221, 179),
    (137, 220), (179, 220), (179, 261),
]

dragging_item = None
original_cell = None