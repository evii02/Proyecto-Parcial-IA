# scripts/enemigo.py
# Nombre: [Francisiveliz Nuñez Matos]
# Matrícula: [22-eisn-2-019]

import pygame
from scripts.algoritmo_astar import astar  
from scripts.arbol_de_comportamiento import (
    Selector, Secuencia, CondicionJugadorCerca,
    AccionPerseguirJugador, AccionPatrullar,
    AccionFlanquearJugador, AccionIdle, AccionAtacarJugador
)

TAM_CELDA = 50

class Enemigo(pygame.sprite.Sprite):
    def __init__(self, x, y, imagen):
        super().__init__()
        self.image = pygame.transform.scale(imagen, (40, 40))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.pos_pixel = pygame.Vector2(x, y)
        self.velocidad = 2
        self.ruta = []
        self.objetivo = None
        
        self.frame_idx = 0
        self.frames = []
        self.anim_timer = 0
        self.direccion = pygame.Vector2(0, 0)

        self.arbol = None
        self.jugador = None
        self.mapa = None
        
        self.cooldown_ataque = 0

    def pixel_a_celda(self, pixel_pos):
        return (int(pixel_pos.y // TAM_CELDA), int(pixel_pos.x // TAM_CELDA))

    def celda_a_pixel(self, celda):
        fila, col = celda
        return pygame.Vector2(col * TAM_CELDA, fila * TAM_CELDA)

    def dentro_de_limites(self, celda, mapa):
        fila, col = celda
        return 0 <= fila < len(mapa) and 0 <= col < len(mapa[0])

    def actualizar_ruta(self, mapa, objetivo_pos):
        inicio = self.pixel_a_celda(self.pos_pixel)
        objetivo = self.pixel_a_celda(objetivo_pos)
        if self.dentro_de_limites(inicio, mapa) and self.dentro_de_limites(objetivo, mapa):
            nueva_ruta = astar(mapa, inicio, objetivo)
            if nueva_ruta and len(nueva_ruta) > 1:
                self.ruta = nueva_ruta[1:]
                self.objetivo = self.celda_a_pixel(self.ruta[0])
            else:
                self.ruta = []
                self.objetivo = None
        else:
            self.ruta = []
            self.objetivo = None

    def mover(self):
        if self.objetivo:
            direccion = self.objetivo - self.pos_pixel
            print(f"Enemigo en {self.pos_pixel}, moviéndose hacia {self.objetivo}, distancia {direccion.length():.2f}")
            if direccion.length() > 1:
                self.direccion = direccion.normalize()
                self.pos_pixel += self.direccion * self.velocidad
                self.rect.topleft = (round(self.pos_pixel.x), round(self.pos_pixel.y))
            else:
                self.pos_pixel = self.objetivo
                self.rect.topleft = (round(self.pos_pixel.x), round(self.pos_pixel.y))
                if self.ruta:
                    self.ruta.pop(0)
                if self.ruta:
                    self.objetivo = self.celda_a_pixel(self.ruta[0])
                else:
                    self.objetivo = None
                self.direccion = pygame.Vector2(0, 0)

    def dibujar(self, screen):
        screen.blit(self.image, self.rect)

    def configurar_arbol(self, jugador, mapa):
        self.jugador = jugador
        self.mapa = mapa

        self.arbol = Selector([
            Secuencia([
                CondicionJugadorCerca(jugador, rango=30),
                AccionAtacarJugador(jugador)
            ]),
            Secuencia([
                CondicionJugadorCerca(jugador, rango=150),
                AccionPerseguirJugador(jugador, mapa)
            ]),
            AccionPatrullar(mapa),
            AccionIdle()
        ])

    def update(self):
        if self.arbol:
            self.arbol.ejecutar(self)
        self.mover()

    def obtener_celda_actual(self):
        return (int(self.pos_pixel.x // TAM_CELDA), int(self.pos_pixel.y // TAM_CELDA))

    def obtener_celda_objetivo(self, pos_objetivo):
        return (int(pos_objetivo.x // TAM_CELDA), int(pos_objetivo.y // TAM_CELDA))
