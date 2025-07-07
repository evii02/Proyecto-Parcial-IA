# scripts/algoritmo_astar.py
# Nombre: [Francisiveliz Nuñez Matos]
# Matrícula: [22-eisn-2-019]

import heapq

def astar(mapa, inicio, objetivo):
    """
    Realiza la búsqueda A* en un mapa 2D desde una celda de inicio hasta una celda objetivo.
    :param mapa: lista de listas con 0 (camino) y 1 (obstáculo).
    :param inicio: tupla (fila, columna) de inicio.
    :param objetivo: tupla (fila, columna) de destino.
    :return: lista de celdas [(fila1, col1), (fila2, col2), ...] desde inicio hasta objetivo.
    """

    def heuristica(a, b):
        # Distancia Manhattan
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def vecinos(nodo):
        fila, col = nodo
        direcciones = [(-1,0), (1,0), (0,-1), (0,1)]  # arriba, abajo, izquierda, derecha
        resultado = []
        for d in direcciones:
            nf, nc = fila + d[0], col + d[1]
            if 0 <= nf < len(mapa) and 0 <= nc < len(mapa[0]):
                if mapa[nf][nc] == 0:  # 0 es camino libre
                    resultado.append((nf, nc))
        return resultado

    abiertos = []
    heapq.heappush(abiertos, (0 + heuristica(inicio, objetivo), 0, inicio))
    came_from = {}
    costo_g = {inicio: 0}

    while abiertos:
        _, costo_actual, actual = heapq.heappop(abiertos)

        if actual == objetivo:
            # Reconstruir camino
            camino = [actual]
            while actual in came_from:
                actual = came_from[actual]
                camino.append(actual)
            camino.reverse()
            return camino

        for vecino in vecinos(actual):
            nuevo_costo = costo_actual + 1  # todos los pasos valen 1
            if vecino not in costo_g or nuevo_costo < costo_g[vecino]:
                costo_g[vecino] = nuevo_costo
                prioridad = nuevo_costo + heuristica(vecino, objetivo)
                heapq.heappush(abiertos, (prioridad, nuevo_costo, vecino))
                came_from[vecino] = actual

    return []  # sin ruta posible
