import pygame
import math


class Player():
    """класс игрока"""
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

    def angle_finder(self, target_pos):
        d_x = target_pos[0] - self.rect.centerx
        d_y = target_pos[1] - self.rect.centery
        self.angle =- math.degrees(math.atan2(d_y, d_x))


#конфиг
if __name__ == '__main__':
    FPS = 60
    running = True
    SIZE = SCREEN_WIDTH, SCREEN_HEIGHT = 600, 600
    BG_COLOR = (20), (120), (0)
    
    player = Player(image="player.png", position=(50, 50))
    
    #запуск
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(SIZE)
    pygame.display.set_caption("cursed_wood")
    
    #цикл
    while running:
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