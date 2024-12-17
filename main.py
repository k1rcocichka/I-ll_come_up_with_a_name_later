import pygame

screen = pygame.display.set_mode((600, 300))
speed = 7
player_x = 100
player_y = 200
is_jumping = False
jump_height = 7
p = pygame.image.load("i.png")
p = pygame.transform.scale(p, (100, 200))

running = True
while running:
    screen.fill((255, 255, 255))
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP] and (150 < player_x < 250) and player_y >= 100:
        player_y = 50
    if keys[pygame.K_DOWN] and (100 < player_x < 250) and player_y < 90:
        player_y = 200
    if keys[pygame.K_SPACE] and not is_jumping:
        is_jumping = True
    if is_jumping:
        if jump_height >= -7:
            if jump_height > 0:
                player_y -= (jump_height ** 2) / 2
            else:
                player_y += (jump_height ** 2) / 2
            jump_height -= 1
        else:
            is_jumping = False
            jump_height = 7

    if keys[pygame.K_LEFT] and player_x >= 0:
        player_x -= speed
    if keys[pygame.K_RIGHT] and player_x <= 550:
        player_x += speed
    if keys[pygame.K_UP] and player_y >= 0:
        pass
    if keys[pygame.K_DOWN] and player_y <= 250:
        pass
    screen.fill((0, 0, 0))
    screen.blit(p, (200, 100))
    pygame.draw.rect(screen, (255, 0, 0), (player_x, player_y, 50, 50))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.time.Clock().tick(100)

    pygame.display.flip()

