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

#конфиг
TITLE = "Cursed wood"
WIDTH = 650
HEIGHT = 650
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
running = True
inventory_open = False

          #броня с лево сверху
#pygame.draw.rect(screen, 'yellow', (137, 137, 36, 36))
#pygame.draw.rect(screen, 'yellow', (179, 137, 36, 36))
#pygame.draw.rect(screen, 'yellow', (221, 137, 36, 36))
#pygame.draw.rect(screen, 'yellow', (137, 179, 36, 36))
#pygame.draw.rect(screen, 'yellow', (179, 179, 36, 36))
#pygame.draw.rect(screen, 'yellow', (221, 179, 36, 36))
#pygame.draw.rect(screen, 'yellow', (137, 220, 36, 36))
#pygame.draw.rect(screen, 'yellow', (179, 220, 36, 36))
#pygame.draw.rect(screen, 'yellow', (179, 261, 36, 36))
#         #картинка игрока с права сверху
#pygame.draw.rect(screen, 'yellow', (387, 137, 78, 119))
#pygame.draw.rect(screen, 'yellow', (387, 261, 36, 36))
#pygame.draw.rect(screen, 'yellow', (429, 261, 36, 36))
#         #инвентарь 1 ряд
#pygame.draw.rect(screen, 'yellow', (137, 345, 36, 36))
#pygame.draw.rect(screen, 'yellow', (179, 345, 36, 36))
#pygame.draw.rect(screen, 'yellow', (221, 345, 36, 36))
#pygame.draw.rect(screen, 'yellow', (262, 345, 36, 36))
#pygame.draw.rect(screen, 'yellow', (304, 345, 36, 36))
#pygame.draw.rect(screen, 'yellow', (345, 345, 36, 36))
#pygame.draw.rect(screen, 'yellow', (387, 345, 36, 36))
#pygame.draw.rect(screen, 'yellow', (429, 345, 36, 36))
#        # инвентарь 2 ряд
#pygame.draw.rect(screen, 'yellow', (137, 387, 36, 36))
#pygame.draw.rect(screen, 'yellow', (179, 387, 36, 36))
#pygame.draw.rect(screen, 'yellow', (221, 387, 36, 36))
#pygame.draw.rect(screen, 'yellow', (262, 387, 36, 36))
#pygame.draw.rect(screen, 'yellow', (304, 387, 36, 36))
#pygame.draw.rect(screen, 'yellow', (345, 387, 36, 36))
#pygame.draw.rect(screen, 'yellow', (387, 387, 36, 36))
#pygame.draw.rect(screen, 'yellow', (429, 387, 36, 36))
#        # инвентарь 3 ряд
#pygame.draw.rect(screen, 'yellow', (137, 429, 36, 36))
#pygame.draw.rect(screen, 'yellow', (179, 429, 36, 36))
#pygame.draw.rect(screen, 'yellow', (221, 429, 36, 36))
#pygame.draw.rect(screen, 'yellow', (262, 429, 36, 36))
#pygame.draw.rect(screen, 'yellow', (304, 429, 36, 36))
#pygame.draw.rect(screen, 'yellow', (345, 429, 36, 36))
#pygame.draw.rect(screen, 'yellow', (387, 429, 36, 36))
#pygame.draw.rect(screen, 'yellow', (429, 429, 36, 36))
#      # инвентарь 4 ряд
#pygame.draw.rect(screen, 'yellow', (137, 471, 36, 36))
#pygame.draw.rect(screen, 'yellow', (179, 471, 36, 36))
#pygame.draw.rect(screen, 'yellow', (221, 471, 36, 36))
#pygame.draw.rect(screen, 'yellow', (262, 471, 36, 36))
#pygame.draw.rect(screen, 'yellow', (304, 471, 36, 36))
#pygame.draw.rect(screen, 'yellow', (345, 471, 36, 36))
#pygame.draw.rect(screen, 'yellow', (387, 471, 36, 36))
#pygame.draw.rect(screen, 'yellow', (429, 471, 36, 36))