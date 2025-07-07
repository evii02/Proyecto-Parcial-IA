# disparo.py
# Nombre: [Francisiveliz Nuñez Matos]
# Matrícula: [22-eisn-2-019]

import pygame

class Disparo(pygame.sprite.Sprite):
    def __init__(self, x, y, direccion, velocidad, imagen=None):
        super().__init__()
        if imagen:
            self.image = pygame.transform.scale(imagen, (5, 15))
        else:
            self.image = pygame.Surface((5, 15))
            self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.velocidad = velocidad
        self.direccion = direccion

    def update(self):
        self.rect.x += self.direccion.x * self.velocidad
        self.rect.y += self.direccion.y * self.velocidad

        if (
            self.rect.bottom < 0 or self.rect.top > 600 or
            self.rect.right < 0 or self.rect.left > 800
        ):
            self.kill()
