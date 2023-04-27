import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self):
        super().__init__()
        self.healthy_image = pygame.image.load("assets/ship.png")
        self.light_damage_image = pygame.image.load("assets/ship_light_damage.png")
        self.heavy_damage_image = pygame.image.load("assets/ship_heavy_damage.png")

        # start healthy
        self.image = self.healthy_image
        self.rect = self.image.get_rect()
        self.health = 100

    def move(self, coordinate):
        self.rect.center = coordinate

    def update(self):
        if self.health < 60:
            self.image = self.light_damage_image
        if self.health < 30:
            self.image = self.heavy_damage_image
