import pygame
import random
from settings import MIN_PLATFORM_DISTANCE


class Player:
    def __init__(self, x, y):
        self.image = pygame.Surface((50, 50))
        self.image.fill((0, 128, 255))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity_y = 0
        self.is_jumping = True
        self.jump_sound = pygame.mixer.Sound("media/jump.wav")

    def update(self, keys):
        # Горизонтальное движение
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Вертикальное движение (гравитация)
        self.velocity_y += 0.5
        self.rect.y += self.velocity_y

        # Выход за границы экрана
        if self.rect.right > 800:
            self.rect.left = 0
        elif self.rect.left < 0:
            self.rect.right = 800

    def jump(self):
        if self.is_jumping:
            self.velocity_y = -20
            self.is_jumping = False
            self.jump_sound.play()

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)


class Platform:
    def __init__(self, x, y):
        self.image = pygame.Surface((100, 10))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

    @staticmethod
    def create_platforms(platforms, num_platforms):
        while len(platforms) < num_platforms:
            while True:
                x = random.randint(0, 800 - 100)
                y = random.randint(-100, 0)
                # Проверяем расстояние до существующих платформ
                too_close = False
                for platform in platforms:
                    if abs(platform.rect.x - x) < MIN_PLATFORM_DISTANCE and abs(
                            platform.rect.y - y) < MIN_PLATFORM_DISTANCE:
                        too_close = True
                        break
                if not too_close:
                    platforms.append(Platform(x, y))
                    break
        return platforms
