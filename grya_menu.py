import pygame
import sys
import random
import fist_scene


class GameMenu:
    def __init__(self, width, height, title):
        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.RED = (255, 0, 0)

        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)

        self.font = pygame.font.Font(None, 36)
        self.background_image = pygame.image.load("data/меню игры.jpg").convert()
        self.background_image = pygame.transform.scale(self.background_image, (width, height))

        self.menu_items = ["Начать", "Продолжить", "Титры", "Достижение", "Трофеи", "Загрузить", "Настройки", "Выход"]
        self.button_rects = []
        self.button_image = pygame.image.load("data/кнопки.jpg")
        self.button_image = pygame.transform.scale(self.button_image, (self.width // 3, 50))
        self.button_height = 50
        self.button_spacing = 10
        self.start_y = self.height // 2 - (len(self.menu_items) * (self.button_height + self.button_spacing)) // 2

        self.music = pygame.mixer.Sound("data/музыка меню.mp3")
        self.music.play(-1)  # бесконечное воспроизведение музыки

        self._create_buttons()
        self.particles = []  # Список для хранения частиц
        self.leaf_images = self._load_leaf_images()

    def _load_leaf_images(self):
        # Загрузка изображений листьев
        leaf_filenames = ["data/листок1.png", "data/листок2.png", "data/листок3.png"]
        leaf_images = []
        for filename in leaf_filenames:
            try:
                image = pygame.image.load(filename).convert_alpha()
                leaf_images.append(image)
            except pygame.error as e:
                print(f"Ошибка загрузки изображения {filename}: {e}")
                return []

        return leaf_images

    def _create_buttons(self):
        for i, item in enumerate(self.menu_items):
            text_rect = self.button_image.get_rect(center=(self.width // 2, self.start_y + i *
                                                           (self.button_height + self.button_spacing)
                                                           + self.button_height // 2))
            self.button_rects.append(text_rect)

    def create_leaf_particle(self, x, y):
        leaf_image = random.choice(self.leaf_images)  # Выбор случайного изображения листика
        scale = random.uniform(0.01, 0.05)  # Случайное масштабирование
        leaf_image = pygame.transform.scale(leaf_image,
                                            (int(leaf_image.get_width() * scale),
                                             int(leaf_image.get_height() * scale)))
        angle = random.uniform(-10, 360)  # Случайный угол поворота
        leaf_image = pygame.transform.rotate(leaf_image, angle)
        vx = random.uniform(-0.5, 0.5)  # Скорость по горизонтали
        vy = random.uniform(0.5, 1)  # Скорость по вертикали
        rotation_speed = random.uniform(-0.5, 0.5)  # скорость вращения
        life = random.randint(100, 2000)  # время жизни частицы
        self.particles.append(
            {"x": x, "y": y, "vx": vx, "vy": vy, "image": leaf_image, "angle": angle, "rotation_speed": rotation_speed,
             "life": life})

    def update_particles(self):
        for particle in self.particles[:]:  # итерируемся по копии списка для удаления
            particle["x"] += particle["vx"]
            particle["y"] += particle["vy"]
            particle["angle"] += particle["rotation_speed"]  # вращение листика
            particle["life"] -= 1
            if particle["y"] > self.height + 50 or particle["life"] <= 0:
                self.particles.remove(particle)  # удаление частиц которые вышли за границы

    def draw_particles(self):
        for particle in self.particles:
            rotated_image = pygame.transform.rotate(particle["image"], particle["angle"])  # поворот изображения
            rect = rotated_image.get_rect(
                center=(int(particle["x"]), int(particle["y"])))  # меняем центр  для отрисовки
            self.screen.blit(rotated_image, rect)  # отрисовываем

    def draw_menu(self):
        self.screen.blit(self.background_image, (0, 0))
        for i, rect in enumerate(self.button_rects):
            self.screen.blit(self.button_image, rect.topleft)  # Отрисовка одного изображения для кнопки
            text_surface = self.font.render(self.menu_items[i], True, self.BLACK)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)  # Отрисовка текста на кнопке
        self.draw_particles()  # отрисовываем частицы
        pygame.display.flip()

    def run(self):
        # основной игровой цикл
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(self.button_rects):
                        if rect.collidepoint(mouse_pos):
                            # Действия при нажатии на кнопку
                            if self.menu_items[i] == "Начать":
                                self.music.stop()
                                    # ЗАПУСК ПЕРВОЙ КАТ СЦЕНЫ
                                fist_scene.main()
                            elif self.menu_items[i] == "Настройки":
                                print("настройки")
                                    # ОТКРЫТИЕ ОКОШКА С НАСТРОЙКАМИ
                            elif self.menu_items[i] == "Выход":
                                running = False  # Выход из игры
                            elif self.menu_items[i] == "Продолжить":
                                print("продолжить")
                                    # КОД ПРОДОЛЖАЮЩИЙ ИГРУ
                            elif self.menu_items[i] == "Титры":
                                show_titles(800, 600, text_sequence)
                                    # вопрос, что вы хотите сделать в титрах?
                            elif self.menu_items[i] == "Достижение":
                                print("Достижение")
                                    # pygame.mixer.Sound("звук монет.mp3").play()
                                    # Код с достижением, думаю добавить может звук рассыпавшихся монет?
                            elif self.menu_items[i] == "Трофеи":
                                print("Трофеи")
                                    # код для трофеев
                            elif self.menu_items[i] == "Загрузить":
                                print("Загрузить")
                                    # вопрос, что сюда будут загружать?
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                    self.create_leaf_particle(event.pos[0], event.pos[1])
            self.update_particles()  # обновляем частицы
            self.draw_menu()
        pygame.quit()
        sys.exit()


def show_titles(screen_width, screen_height, text_list, font_size=36, font_color=(255, 255, 255)):
    pygame.init()
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Титры")
    font = pygame.font.Font(None, font_size)
    current_text_index = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                current_text_index += 1  # Переключение на следующий текст
                if current_text_index >= len(text_list):
                    running = False  # Завершение программы после последнего текста
        screen.fill((0, 0, 0))
        # Проверяем, есть ли еще текст для отображения
        if current_text_index < len(text_list):
            current_text = text_list[current_text_index]
            text_surface = font.render(current_text, True, font_color)
            text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(text_surface, text_rect)
        pygame.display.flip()
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    text_sequence = ["Над проектом работали:, \n Коноплева Анжелика \n Кечуткин Игорь \n Кривоногов Андрей",
                     "Кечуткин Игорь сделал код, \n отвечающий препятствия, появление врагов. \n"
                     " Собрал игру в единое целое", "Кривоногов Андрей ответственный за инвентарь, \n"
                                                    " передвижение героя", "Коноплева Анжелика сделала меню игры \n "
                                                                           "и начало игры"]
    menu = GameMenu(600, 600, "Игровое Меню")
    menu.run()
