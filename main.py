# main.py
# Nombre: [Francisiveliz Nuñez Matos]
# Matrícula: [22-eisn-2-019]

import pygame
import sys
import os
import random
from scripts.enemigo import Enemigo
from scripts.jugador import Jugador
from scripts.disparo import Disparo
from scripts.explosion import Explosion
from scripts.tesoro import Tesoro
from scripts.nave import Nave

def obtener_direccion_disparo(teclas):
    direccion = pygame.Vector2(0, 0)
    if teclas[pygame.K_UP] or teclas[pygame.K_w]:
        direccion.y = -1
    elif teclas[pygame.K_DOWN] or teclas[pygame.K_s]:
        direccion.y = 1
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        direccion.x = -1
    elif teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        direccion.x = 1
    if direccion.length_squared() > 0:
        return direccion.normalize()
    else:
        
        
        return None

pygame.init()

# Inicializar joystick
pygame.joystick.init()
joystick = None
if pygame.joystick.get_count () > 0:
    joystick = pygame.joystick.Joystick(0)
    joystick.init ()
    print(f"Joystick conectado: {joystick.get_name()}")
else:
    print("No hay joystick conectado.")

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Batalla Galáctica")
clock = pygame.time.Clock()
fuente = pygame.font.SysFont("arial", 24)
pygame.mixer.init()

tiempo_spawn = 0
TIEMPO_SPAWN_ENEMIGO = 5000

TAM_CELDA = 20
nivel_actual = 1
max_niveles = 3

# Definimos los mapas para los niveles 
mapas = [
    # Nivel 1
    [
         [0]*30,
        [0,1,1,1,0,1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,0],
        [0,1,0,1,0,1,0,1,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,1,0,1,0,1,0,0],
        [0,1,0,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,0,1,0,1,0,1,0,0],
        [0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,1,0,0,1,0],
        [0,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,0],
        [0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,1,0],
        [0,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,1,0],
        [0,1,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,1,0],
        [0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,0],
        [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1,0],
        [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,0],
        [0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0],
        [0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0],
        [0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0]*30
    ],
    # Nivel 2 (más difícil)
    [
         [0]*30,
        [0,1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0],
        [0,1,0,0,0,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0],
        [0,1,0,1,1,1,0,1,0,1,0,1,1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,0,0],
        [0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,0],
        [0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,1,0],
        [0,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,1,0],
        [0,1,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,1,0],
        [0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,0],
        [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1,0],
        [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,0],
        [0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0],
        [0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0],
        [0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0]*30
    ],
    # Nivel 3 (último nivel con nave)
    [
         [0]*30,
        [0,1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,0],
        [0,1,0,0,0,0,0,1,0,1,0,0,1,0,1,0,0,1,0,1,0,0,0,0,0,1,0,1,0,0],
        [0,1,0,1,1,1,0,1,0,1,0,1,1,0,1,1,0,1,0,1,1,1,1,1,0,1,0,1,0,0],
        [0,1,0,0,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0],
        [0,1,1,1,1,1,1,1,0,1,1,1,1,0,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,0],
        [0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,1,0,0,0,0,0,1,0,0,1,0],
        [0,1,0,1,1,1,0,1,1,1,1,1,0,1,0,1,0,1,1,1,1,1,0,1,1,1,0,1,1,0],
        [0,1,0,1,0,1,0,0,0,0,0,1,0,0,0,1,0,1,0,0,0,1,0,0,0,1,0,0,1,0],
        [0,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,0,1,1,0],
        [0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,1,0,0,1,0],
        [0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,0,1,1,1,1,1,1,0],
        [0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,1,0],
        [0,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,1,0,1,1,1,1,1,1,0],
        [0,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0],
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
        [0]*30
    ]
]

# Coordenadas de enemigos y tesoros por nivel
enemigos_por_nivel = {
    1: [(28, 1), (25, 16), (5, 10)],
    2: [(27, 2), (22, 18), (7, 12), (10, 25)],
    3: [(5, 5), (15, 15), (25, 10), (20, 22), (10, 28)],
}

tesoros_por_nivel = {
    1: [(5, 5), (10, 15), (16, 8)],
    2: [(5, 5), (10, 15), (14, 10)],  # Tres tesoros en lugares accesibles del mapa nivel 2 
    3: [(8, 8), (14, 14), (22, 20), (25, 25)],
} 

estado_juego = "jugando"
pausado = False
jugador_vel = 3
disparos = pygame.sprite.Group()
enemigos = pygame.sprite.Group()
explosiones = pygame.sprite.Group()
tesoros = pygame.sprite.Group()
nave_group = pygame.sprite.Group()

ASSETS = os.path.join("assets", "images")
SONIDOS = os.path.join("assets", "sounds")
jugador_img = pygame.image.load(os.path.join(ASSETS, "player", "player_walk.png"))
disparo_img = pygame.image.load(os.path.join(ASSETS, "player", "laser.png"))
nave_img = pygame.image.load(os.path.join(ASSETS, "nave", "nave.png"))

enemigo_frames = [
    pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, "enemy", "enemy_1.png")), (TAM_CELDA, TAM_CELDA))
    for _ in range(2)
]

explosion_frames = [
    pygame.transform.scale(pygame.image.load(os.path.join(ASSETS, "explosion", "explosion02.png")), (TAM_CELDA, TAM_CELDA))
    for _ in range(5)
]

tesoro_frames = [
    pygame.transform.scale(
        pygame.image.load(os.path.join(ASSETS, "tesoros", f"coin_1.png")),
        (TAM_CELDA, TAM_CELDA)
    )
    for _ in range(4)
]

disparo_sfx = pygame.mixer.Sound(os.path.join(SONIDOS, "disparo.wav"))
gameover_sfx = pygame.mixer.Sound(os.path.join(SONIDOS, "gameover.wav"))
menu_sfx = pygame.mixer.Sound(os.path.join(SONIDOS, "menu.wav"))

jugador = Jugador(TAM_CELDA, TAM_CELDA, TAM_CELDA, TAM_CELDA, jugador_img, vidas=3)
jugador.pos_pixel.update(jugador.rect.topleft)

def cargar_nivel(nivel):
    enemigos.empty()
    tesoros.empty()
    nave_group.empty()
    mapa_actual = mapas[nivel - 1]

    for fila, col in enemigos_por_nivel[nivel]:
        e = Enemigo(col * TAM_CELDA, fila * TAM_CELDA, enemigo_frames[0])
        e.frames = enemigo_frames
        e.configurar_arbol(jugador, mapa_actual)
        enemigos.add(e)

    for fila, col in tesoros_por_nivel[nivel]:
        x = col * TAM_CELDA
        y = fila * TAM_CELDA
        tesoros.add(Tesoro(x, y, tesoro_frames))

    if nivel == max_niveles:
        nave_x, nave_y = 28 * TAM_CELDA, 16 * TAM_CELDA
        nave = Nave(nave_x, nave_y, nave_img)
        nave_group.add(nave)

    jugador.rect.topleft = (TAM_CELDA, TAM_CELDA)
    jugador.pos_pixel.update(jugador.rect.topleft)
    return mapa_actual

mapa = cargar_nivel(nivel_actual)
nivel_cargado = nivel_actual

while True:
    for evento in pygame.event.get():
       if evento.type == pygame.QUIT:
        pygame.quit()
        sys.exit()
       elif evento.type == pygame.KEYDOWN:
        if estado_juego == "jugando":
            if evento.key == pygame.K_SPACE:
                dir_disp = obtener_direccion_disparo(pygame.key.get_pressed()) or pygame.Vector2(0, -1)
                disparo = Disparo(jugador.rect.centerx, jugador.rect.centery, dir_disp, 10, disparo_img)
                disparos.add(disparo)
                disparo_sfx.play()
        elif evento.key == pygame.K_ESCAPE:
          pausado = not pausado                       
                
    if estado_juego == "jugando" and not pausado:
        screen.fill((0, 0, 20))  # FONDO CORRECTO
        keys = pygame.key.get_pressed()

         # Disparo con botones del control
        if joystick:
                if joystick.get_button(3): # Triangulo
                    dir_disp = pygame.Vector2(0, -1)
                elif joystick.get_button(0): # Cuadrado
                    dir_disp = pygame.Vector2(-1, 0)
                elif joystick.get_button(2): # Circulo
                    dir_disp = pygame.Vector2(1, 0)
                elif joystick.get_button(1): # X
                    dir_disp = pygame.Vector2(0, 1)
                else:
                    dir_disp = None

        if dir_disp:
                disparo = Disparo(jugador.rect.centerx, jugador.rect.centery, dir_disp, 10, disparo_img)
                disparos.add(disparo) 
                disparo_sfx.play()

        if keys[pygame.K_w] or keys[pygame.K_UP]: jugador.rect.y -= jugador_vel
        if keys[pygame.K_s] or keys[pygame.K_DOWN]: jugador.rect.y += jugador_vel
        if keys[pygame.K_a] or keys[pygame.K_LEFT]: jugador.rect.x -= jugador_vel
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]: jugador.rect.x += jugador_vel
        jugador.pos_pixel.update(jugador.rect.topleft)

        for enemigo in enemigos:
            enemigo.update()
            if jugador.rect.colliderect(enemigo.rect):
                jugador.recibir_dano(1)
                enemigo.kill()
                if jugador.vida <= 0:
                    estado_juego = "game_over"
                    gameover_sfx.play()

        recolectados = pygame.sprite.spritecollide(jugador, tesoros, True)
        for t in recolectados:
            print("💰 ¡Tesoro recolectado!")

        if len(tesoros) == 0 and nivel_cargado == nivel_actual and nivel_actual < max_niveles:
            nivel_actual += 1
            mapa = cargar_nivel(nivel_actual)
            nivel_cargado = nivel_actual
            print(f"🚀 Nivel {nivel_actual} cargado")

        if nivel_actual == max_niveles and len(tesoros) == 0:
            texto_nave = fuente.render("¡Dirígete a la nave!", True, (255, 255, 0))
            screen.blit(texto_nave, (WIDTH // 2 - texto_nave.get_width() // 2, 50))

        disparos.update()
        explosiones.update()
        tesoros.update()

        colisiones = pygame.sprite.groupcollide(disparos, enemigos, True, True)
        for impactos in colisiones.values():
            for enemigo in impactos:
                explosion = Explosion(enemigo.rect.centerx, enemigo.rect.centery, explosion_frames)
                explosiones.add(explosion)

        # DIBUJO DEL MAPA
        for fila in range(len(mapa)):
            for col in range(len(mapa[0])):
                if mapa[fila][col] == 1:
                    pygame.draw.rect(screen, (70, 70, 70), (col * TAM_CELDA, fila * TAM_CELDA, TAM_CELDA, TAM_CELDA))

        screen.blit(jugador.image, jugador.rect)
        enemigos.draw(screen)
        disparos.draw(screen)
        explosiones.draw(screen)
        tesoros.draw(screen)
        if nivel_actual == max_niveles:
            nave_group.draw(screen)

        texto_vida = fuente.render(f"Vidas: {jugador.vida}", True, (255, 0, 0))
        screen.blit(texto_vida, (10, 10))

        # VERIFICACIÓN DE NAVE
        if pygame.sprite.spritecollideany(jugador, nave_group):
            print("✅ El jugador tocó la nave")
            estado_juego = "ganaste"
            print("🚀 ¡Has llegado a la nave y ganaste el juego!")

    elif estado_juego == "game_over":
        texto = fuente.render("GAME OVER", True, (255, 0, 0))
        screen.fill((0, 0, 0))
        screen.blit(texto, (WIDTH // 2 - texto.get_width() // 2, HEIGHT // 2))

    elif estado_juego == "ganaste":
        texto = fuente.render("🎉 ¡Felicidades! Ganaste el juego", True, (0, 255, 0))
        screen.fill((0, 0, 0))
        screen.blit(texto, (WIDTH // 2 - texto.get_width() // 2, HEIGHT // 2))

    tiempo_spawn += clock.get_time()
    if tiempo_spawn >= TIEMPO_SPAWN_ENEMIGO and estado_juego == "jugando" and not pausado:
        while True:
            fila = random.randint(1, len(mapa) - 2)
            col = random.randint(1, len(mapa[0]) - 2)
            if mapa[fila][col] == 0:
                nuevo_enemigo = Enemigo(col * TAM_CELDA, fila * TAM_CELDA, enemigo_frames[0])
                nuevo_enemigo.frames = enemigo_frames
                nuevo_enemigo.configurar_arbol(jugador, mapa)
                enemigos.add(nuevo_enemigo)
                tiempo_spawn = 0
                print("🧬 Nuevo enemigo creado")
                break

    # Movimiento con joystick
    if joystick:
        eje_x = joystick.get_axis (0) # -1 izquierda, 1 derecha
        eje_y = joystick.get_axis (1) # -1 arriba, 1 abajo

        if abs (eje_x) > 0.1:
            jugador.rect.x += int (eje_x * jugador.velocidad)
        if abs (eje_y) > 0.1:
            jugador.rect.y += int (eje_y * jugador.velocidad)

    # Disparar con botones del control
    if joystick:
        if joystick.get_button (3) : # Triangulo
            jugador.disparar("arriba")
        if joystick.get_button (0) : # Cuadrado
            jugador.disparar("izquierda")
        if joystick.get_button (2) : # Circulo
            jugador.disparar("derecha")
        if joystick.get_button (1) : # X
            jugador.disparar("abajo")                               
      
    pygame.display.flip()
    clock.tick(60)
    # prueba de commit