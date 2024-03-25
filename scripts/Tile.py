import pygame
from scripts.Entity import Entity


class Tile(Entity):
    def __init__(self, app, x, y):
        super().__init__(app)
