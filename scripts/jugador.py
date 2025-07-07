# jugador.py
# Nombre: [Francisiveliz Nuñez Matos]
# Matrícula: [22-eisn-2-019]
import pygame

class Jugador(pygame.sprite.Sprite):
    def __init__(self, x, y, ancho, alto, imagen, vidas=3):
        super().__init__()
        self.image = pygame.transform.scale(imagen, (ancho, alto))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos_pixel = pygame.Vector2(x, y)
        self.vida = vidas
        self.velocidad = 5

    def recibir_dano(self, cantidad):
        self.vida -= cantidad
        print(f"Jugador recibe {cantidad} de daño, vida restante: {self.vida}")
        if self.vida <= 0:
            print("Jugador murió")

    def disparar(self, direccion):
        print(f"Disparo hacia {direccion}")        
