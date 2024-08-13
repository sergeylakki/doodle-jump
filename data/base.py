import sys
import pygame
from data.resources import Player, Platform
from data.database import save_score, get_top_players
import time
from settings import WIN_CONDITION


class BaseGame:
    def __init__(self, width, height, *args, **kwargs):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.font = pygame.font.SysFont('Arial', 36)
        self.width = width
        self.height = height
        self.clock = pygame.time.Clock()
        self.FPS = 60

    def set_font_size(self, size):
        self.font = pygame.font.SysFont('Arial', size)

    def event_run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return "Меню"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    return "Меню"

    def logic(self):
        pass

    def draw_text(self, text, color, x, y):
        textobj = self.font.render(text, True, color)
        textrect = textobj.get_rect(center=(x, y))
        self.screen.blit(textobj, textrect)
        return textrect

    def loop(self):
        self.screen.fill((255, 255, 255))
        event = self.logic()
        if event:
            return event
        event = self.event_run()
        if event:
            return event
        pygame.display.flip()
        self.clock.tick(self.FPS)


class MenuGame(BaseGame):
    def __init__(self, width, height, *args, screen_list, **kwargs):
        super().__init__(width, height)
        self.menu_list = {i: None for i in screen_list}
        pygame.display.set_caption("Menu")

    def event_run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    for name, button in self.menu_list.items():
                        if button.collidepoint(event.pos):
                            return name

    def logic(self):
        self.draw_text("Главное меню", (0, 255, 0), self.width // 2, self.height // 10)
        for i, title in enumerate(self.menu_list.keys()):
            self.menu_list[title] = self.draw_text(title, (0, 0, 0), self.width // 2, self.height // 10*(i+2))


class EnterNickname(BaseGame):
    def __init__(self, *args, num_platforms=10, **kwargs, ):
        super().__init__(*args, **kwargs)
        pygame.display.set_caption("Game")
        self.nickname = ''

    def event_run(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return self.nickname
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return self.nickname
                elif event.key == pygame.K_BACKSPACE:
                    self.nickname = self.nickname[:-1]
                else:
                    self.nickname += event.unicode

    def logic(self):
        self.draw_text("Введите ваш никнейм:", (0, 0, 0), self.width // 2, self.height // 2 - 50)
        self.draw_text(self.nickname, (0, 0, 0), self.width // 2, self.height // 2)
        self.draw_text("Нажмите ENTER для продолжения", (0, 0, 0), self.width // 2, self.height // 2 + 50)


class Game(BaseGame):
    def __init__(self, *args, nickname, num_platforms=10, **kwargs, ):
        super().__init__(*args, **kwargs)
        pygame.display.set_caption("Game")
        self.player = Player(375, 500)
        self.num_platforms = num_platforms
        self.platforms = [Platform(375, 550), Platform(200, 400), Platform(600, 300), Platform(100, 200)]
        self.score = 0
        self.nickname = nickname

    def logic(self):
        keys = pygame.key.get_pressed()
        self.player.update(keys)
        Platform.create_platforms(self.platforms, self.num_platforms)
        self.platforms = [platform for platform in self.platforms if platform.rect.top < 600]

        if self.player.rect.top <= 300:  # если игрок достигает верхней половины экрана
            self.player.rect.y += abs(self.player.velocity_y)  # компенсируем движение игрока
            for platform in self.platforms:
                platform.rect.y += abs(self.player.velocity_y)  # движем платформы вниз
                if platform.rect.top > 600:  # если платформа уходит за нижний край экрана
                    self.platforms.remove(platform)  # удаляем ее

        # Логика для прыжков и взаимодействия с платформами
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect) and self.player.velocity_y > 0:
                self.player.is_jumping = True
                self.player.jump()
                self.score += 10  # Увеличение очков при прыжке
                if self.score % 100 == 0:
                    self.num_platforms -= 1

        # Проверка проигрыша (если игрок падает ниже экрана)
        if self.player.rect.top > 600:
            save_score(self.nickname, self.score)
            pygame.quit()
            return "Меню"

        # Выйгрышь
        if self.score >= WIN_CONDITION:
            self.draw_text(f"Вы победили: {self.score}", (255, 0, 0), self.width//2, self.height//2)
            save_score(self.nickname, self.score)
            pygame.display.flip()
            time.sleep(5)
            pygame.quit()
            return "Меню"

        # Рендеринг
        self.player.draw(self.screen)
        for platform in self.platforms:
            platform.draw(self.screen)
        self.draw_text(f"Score: {self.score}", (255, 0, 0), 100, 50)


class ShowHighscore(BaseGame):
    def __init__(self, *args, **kwargs, ):
        super().__init__(*args, **kwargs)
        pygame.display.set_caption("Рейтинг")

    def logic(self):
        self.draw_text(f"Рейтинг:", (0, 0, 0), self.width // 2, self.height // 10)
        for i, (name, score) in enumerate(get_top_players()):
            self.draw_text(f"{name}: {score}", (0, 0, 0), self.width // 2, self.height // 10 * (i+2))

        self.draw_text("Нажмите ESC для возврата в меню.", (0, 0, 0), self.width // 2, self.height // 2 + 600)


class ShowRules(BaseGame):

    def logic(self):
        self.set_font_size(20)
        self.draw_text("Правила игры: Используйте стрелки для передвижения.",
                       (0, 0, 0), self.width // 2, self.height // 2 - 50)
        self.draw_text("Задача прыгать по платформам набирая все больше очков",
                       (0, 0, 0), self.width // 2, self.height // 2)
        self.draw_text("Нажмите ESC для возврата в меню.", (0, 0, 0), self.width // 2+50, self.height // 2 + 50)