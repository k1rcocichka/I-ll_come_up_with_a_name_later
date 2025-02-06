import pygame
import sys
import fist_scene


class GameMenu:
    def __init__(self, width, height, title):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(title)

        # Цвета
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (200, 200, 200)
        self.RED = (255, 0, 0)

        self.font = pygame.font.Font(None, 36)
        self.background_image = pygame.image.load("data/меню игры.jpg")
        self.background_image = pygame.transform.scale(self.background_image, (width, height))

        # Кнопки меню
        self.menu_items = ["Начать", "Продолжить", "Титры", "Достижение", "Трофеи", "Загрузить", "Настройки", "Выход"]
        self.button_rects = []
        self.button_colors = []
        self.button_height = 50
        self.button_spacing = 10
        self.start_y = self.height // 2 - (len(self.menu_items) * (self.button_height + self.button_spacing)) // 2

        self._create_buttons()
        self.music = pygame.mixer.Sound("data/музыка меню.mp3")
        self.music.play()

    def _create_buttons(self):
        for i, item in enumerate(self.menu_items):
            text_surface = self.font.render(item, True, self.BLACK)
            text_rect = text_surface.get_rect(center=(self.width // 2, self.start_y + i * (self.button_height + self.button_spacing) + self.button_height // 2))
            button_rect = text_rect.inflate(20, 20)
            self.button_rects.append(button_rect)
            self.button_colors.append(self.GRAY)

    def draw_menu(self): #отрисовывание меню на экране
        self.screen.blit(self.background_image, (0, 0))
        for i, rect in enumerate(self.button_rects):
            pygame.draw.rect(self.screen, self.button_colors[i], rect)
            text_surface = self.font.render(self.menu_items[i], True, self.BLACK)
            text_rect = text_surface.get_rect(center=rect.center)
            self.screen.blit(text_surface, text_rect)
        pygame.display.flip()

    def run(self):
        #основной игровой цикл
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
                                running = False # Выход из игры
                            elif self.menu_items[i] == "Продолжить":
                                print("продолжить")
                                # КОД ПРОДОЛЖАЮЩИЙ ИГРУ
                            elif self.menu_items[i] == "Титры":
                                show_titles(800, 600, text_sequence) #после окончания титров, игра завершает работу
                                # вопрос, что вы хотите сделать в титрах?
                                # расписать кто что делал кратко
                            elif self.menu_items[i] == "Достижение":
                                print("Достижение")
                                #pygame.mixer.Sound("звук монет.mp3").play()
                                # Код с достижением, думаю добавить может звук рассыпавшихся монет?
                                # По уровням будут раскиданы разные коллекционки (как выглядеть будут ещё не придумал)
                                # Тут должны будут отобраться все которые мы собрали при прохождении игры
                                # в файле с сейвом будут прописаны
                            elif self.menu_items[i] == "Трофеи":
                                print("Трофеи")
                                #код для трофеев
                            elif self.menu_items[i] == "Загрузить":
                                print("Загрузить")
                                #вопрос, что сюда будут загружать?
                                #Андерей заргузит уровни и тут нужна будт заргузка уровней по выбору
                if event.type == pygame.MOUSEMOTION:
                    mouse_pos = pygame.mouse.get_pos()
                    for i, rect in enumerate(self.button_rects):
                        if rect.collidepoint(mouse_pos):
                            self.button_colors[i] = self.RED
                        else:
                            self.button_colors[i] = self.GRAY
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
