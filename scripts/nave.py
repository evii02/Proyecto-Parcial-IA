# nave.py
# Nombre: [Francisiveliz Nuñez Matos]
# Matrícula: [22-eisn-2-019]

import pygame

class Nave(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen):
        super().__init__()
        self.image = pygame.transform.scale(imagen, (40, 40))  # Ajusta tamaño según convenga
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
