# arbol_de_comportamiento.py
# Nombre: [Francisiveliz Nuñez Matos]
# Matrícula: [22-eisn-2-019]

import pygame
import random
from scripts.algoritmo_astar import astar

# Nodo base del árbol
class NodoBT:
    def ejecutar(self, agente):
        pass

# Nodo de tipo Selector
class Selector(NodoBT):
    def __init__(self, hijos):
        self.hijos = hijos

    def ejecutar(self, agente):
        for hijo in self.hijos:
            if hijo.ejecutar(agente):
                return True
        return False

# Nodo de tipo Secuencia
class Secuencia(NodoBT):
    def __init__(self, hijos):
        self.hijos = hijos

    def ejecutar(self, agente):
        for hijo in self.hijos:
            if not hijo.ejecutar(agente):
                return False
        return True

# Condición: si el jugador está dentro de cierto rango
class CondicionJugadorCerca(NodoBT):
    def __init__(self, jugador, rango=150):
        self.jugador = jugador
        self.rango = rango

    def ejecutar(self, agente):
        distancia = agente.pos_pixel.distance_to(self.jugador.pos_pixel)
        return distancia < self.rango

# Acción: perseguir al jugador con A*
class AccionPerseguirJugador(NodoBT):
    def __init__(self, jugador, mapa):
        self.jugador = jugador
        self.mapa = mapa

    def ejecutar(self, agente):
        objetivo = self.jugador.pos_pixel
        agente.actualizar_ruta(self.mapa, objetivo)
        return True

# Acción: flanquear al jugador
class AccionFlanquearJugador(NodoBT):
    def __init__(self, jugador, mapa):
        self.jugador = jugador
        self.mapa = mapa

    def ejecutar(self, agente):
        jugador_celda = agente.pixel_a_celda(self.jugador.pos_pixel)
        opciones = [(0, 1), (0, -1), (1, 0), (-1, 0)]
        random.shuffle(opciones)

        for dx, dy in opciones:
            flanco = (jugador_celda[0] + dy, jugador_celda[1] + dx)
            if agente.dentro_de_limites(flanco, self.mapa) and self.mapa[flanco[0]][flanco[1]] == 0:
                destino = agente.celda_a_pixel(flanco)
                agente.actualizar_ruta(self.mapa, destino)
                return True
        return False

# Acción: patrullar aleatoriamente
class AccionPatrullar(NodoBT):
    def __init__(self, mapa):
        self.mapa = mapa

    def ejecutar(self, agente):
        for _ in range(10):
            fila = random.randint(1, len(self.mapa) - 2)
            col = random.randint(1, len(self.mapa[0]) - 2)
            if self.mapa[fila][col] == 0:
                destino = agente.celda_a_pixel((fila, col))
                agente.actualizar_ruta(self.mapa, destino)
                return True
        return False

# Acción: quedarse quieto
class AccionIdle(NodoBT):
    def ejecutar(self, agente):
        agente.ruta = []
        agente.objetivo = None
        return True

# Acción: atacar al jugador si está muy cerca
class AccionAtacarJugador(NodoBT):
    def __init__(self, jugador):
        self.jugador = jugador
        self.cooldown = 60  # Enemigo solo ataca cada 60 frames
        self.contador = 0

    def ejecutar(self, agente):
        if self.contador > 0:
            self.contador -= 1
            return False

        distancia = agente.pos_pixel.distance_to(self.jugador.pos_pixel)
        if distancia < 30:
            self.jugador.recibir_dano(1)
            print("⚔️ ¡Enemigo ataca al jugador!")
            self.contador = self.cooldown
            return True
        return False
