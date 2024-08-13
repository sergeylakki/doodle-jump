from data.base import MenuGame, Game, EnterNickname, ShowHighscore, ShowRules
from settings import *
from data.database import delete_scores


class MainGame:
    screen_list = {"Играть": Game, "Меню": MenuGame, "Рейтинг": ShowHighscore, "Правила": ShowRules}

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = None
        self.nickname = ''

        self.input_nickname()
        self.open_screen(MenuGame)
        self.loop()

    def input_nickname(self):
        self.open_screen(EnterNickname)
        while True:
            self.nickname = self.screen.loop()
            if self.nickname:
                break

    def open_screen(self, class_screen):
        self.screen = class_screen(self.width, self.height, nickname=self.nickname,
                                   screen_list=list(MainGame.screen_list.keys()) + ["Очистить рейтинг"])

    def loop(self):
        while True:
            response = self.screen.loop()
            for name, screen in MainGame.screen_list.items():
                if response == name:
                    self.open_screen(screen)
            if response == "Очистить рейтинг":
                delete_scores()


if __name__ == "__main__":
    game = MainGame(SCREEN_WIDTH, SCREEN_HEIGHT)