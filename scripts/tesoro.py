# tesoro.py
# Nombre: [Francisiveliz Nuñez Matos]
# Matrícula: [22-eisn-2-019]

import pygame

class Tesoro(pygame.sprite.Sprite):
    def __init__(self, x, y, frames):
        super().__init__()
        self.frames = frames
        self.image = self.frames[0]  # ✅ Usa la primera imagen al inicio
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frame_idx = 0
        self.anim_timer = 0
        self.anim_vel = 10  # Velocidad de animación (puedes ajustarla)

    def update(self):
        self.anim_timer += 1
        if self.anim_timer >= self.anim_vel:
            self.anim_timer = 0
            self.frame_idx = (self.frame_idx + 1) % len(self.frames)
            self.image = self.frames[self.frame_idx]
