import pygame
import sys


# Инициализация Pygame
def init_pygame():
    pygame.init()
    pygame.mixer.init()


# Настройки экрана
def create_screen(width, height):
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Первая катсцена")
    return screen


# Загрузка изображений
def load_images(image_paths, width, height):
    images = [pygame.image.load(path) for path in image_paths]
    return [pygame.transform.scale(img, (width, height)) for img in images]


# Загрузка звуков
def load_sounds(sound_paths):
    return [pygame.mixer.Sound(path) for path in sound_paths]


# Функция для отображения катсцены
def cutscene(screen, images, click_sounds, background_music, texts):
    current_image_index = 0  # Индекс текущего изображения
    background_music.play(0)  # Воспроизведение фоновой музыки в цикле

    font = pygame.font.Font(None, 32)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:  # Проверка нажатия мыши
                music = click_sounds[current_image_index]
                music.play()  # Воспроизведение соответствующего звука
                current_image_index += 1
                if current_image_index >= len(images):
                    music.stop()
                    background_music.stop()
                    return  # Выход из цикла, если все изображения показаны

        screen.blit(images[current_image_index], (0, 0))

        text = font.render(texts[current_image_index], True, (0, 0, 0))
        text_rect = text.get_rect(center=(screen.get_width() // 2, screen.get_height() - 50))
        screen.blit(text, text_rect)

        pygame.display.flip()

        pygame.time.Clock().tick(60)


# Основной игровой цикл
def main_game_loop(screen):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill((0, 0, 0))
        pygame.display.flip()


# Главная программа
def main():
    init_pygame()

    screen_width = 600
    screen_height = 600
    screen = create_screen(screen_width, screen_height)

    image_paths = ['data/город.jpg', "data/коридор.jpg", "data/1.jpg", "data/2.jpg", "data/3.jpg", "data/открытое письмо.png", "data/завещание.png",
                   "data/завещание.png", "data/завещание.png"]
    images = load_images(image_paths, screen_width, screen_height)

    sound_paths = ["data/звуки шагов.mp3", "data/door-bell.mp3", "data/open door.mp3", "data/шелест бумаги.mp3", "data/фоновая 1 кат сцена.mp3",
                   "data/фоновая 1 кат сцена.mp3", "data/фоновая 1 кат сцена.mp3", "data/фоновая 1 кат сцена.mp3", "data/фоновая 1 кат сцена.mp3"]
    click_sounds = load_sounds(sound_paths)

    background_music = pygame.mixer.Sound("data/фоновая 1 кат сцена.mp3")  # Фоновая музыка
    texts = [
        "",
        "",
        "Кто там?", "Письмо? От кого?", "Странно. Давно я не получал писем", 'Завещание отца?',
        "выражая свою последнюю волю", "Я завещаю сыну свой дом.", f"Долгое время мы не общались, \n"
                                                                   "но  я верю, что ты сумеешь сохранить дом\n"
                                                                   " и будешь относиться к нему с любовью и заботой.\n"
    ]

    cutscene(screen, images, click_sounds, background_music, texts)  # Запуск катсцены
    main_game_loop(screen)  


if __name__ == "__main__":
    main()
