import pygame
import sys
import random

# Colores
negro = (0, 0, 0)
rojo_intenso = (200, 0, 0)
blanco = (255, 255, 255)
verde = (0, 255, 0)

pygame.init()
pygame.mixer.init()

ventana = pygame.display.set_mode((1365, 780))
pygame.display.set_caption("cinco noches con los brainrots")
clock = pygame.time.Clock()

# Música de fondo
pygame.mixer.music.load("sounds/menu-o-creditos.ogg")
pygame.mixer.music.play(-1, 0.0)

# Sonido de jumpscare
sonido_jumpscare = pygame.mixer.Sound("sounds/jumpscare.ogg")

# Imágenes
oficina = pygame.image.load("img/Oficina_normal.png").convert_alpha()
oficina = pygame.transform.scale(oficina, (1365, 780))

# Cargar frames del personaje
personaje_frames = [
    pygame.transform.scale(pygame.image.load("img/Oficina_Tralalelo_1_V2.png").convert_alpha(), (1365, 780)),
    pygame.transform.scale(pygame.image.load("img/Oficina_Tralalelo_2_v2.png").convert_alpha(), (1365, 780)),
    pygame.transform.scale(pygame.image.load("img/Oficina_Tralalelo_3_V2.png").convert_alpha(), (1365, 780)),
    pygame.transform.scale(pygame.image.load("img/Oficina_Tralalelo_4_V2.png").convert_alpha(), (1365, 780)),
]

# Frames de jumpscare
jumpscare_frames = [
    pygame.transform.scale(pygame.image.load("img/Tralalelo_jumpscare.png").convert_alpha(), (1365, 780)),
    pygame.transform.scale(pygame.image.load("img/tralalero_jumpscare2.png").convert_alpha(), (1365, 780)),
    pygame.transform.scale(pygame.image.load("img/tralalerojumpscare3}.png").convert_alpha(), (1365, 780))
]

# Puerta
puerta_fotogramas = [
    pygame.transform.scale(pygame.image.load(f"img/Puerta_izquierda_{i+1}.png").convert_alpha(), (1365, 780))
    for i in range(4)
]

boton = pygame.Rect(260, 250, 60, 60)

fuente_titulo = pygame.font.SysFont("OCR A Extended", 60, bold=True)
fuente_texto = pygame.font.SysFont("Courier New", 24, bold=True)
fuente_noche = pygame.font.SysFont("OCR A Extended", 50, bold=True)

texto_titulo = fuente_titulo.render("⚠ ¡ADVERTENCIA! ⚠", True, rojo_intenso)
texto_advertencia = fuente_texto.render(
    "Este juego contiene luces parpadeantes, ruidos fuertes y muchos sustos repentinos",
    True, blanco
)

titulo_surf = texto_titulo.convert_alpha()
advertencia_surf = texto_advertencia.convert_alpha()
titulo_rect = titulo_surf.get_rect(center=(1365 // 2 - 30, 300))
advertencia_rect = advertencia_surf.get_rect(center=(1365 // 2, 370))

alpha = 0
velocidad_fade = 2
tiempo_espera = 3
tiempo_transcurrido = 0

pantalla = "advertencia"
mostrar_hora = False
tiempo_hora_inicio = 0
inicio_noche = 0
hora_actual = 0
tiempo_por_hora = 60000
energia = 100

# Animación puerta
puerta_abierta = True
puerta_animando = False
puerta_fotograma_actual = -1
animacion_inversa = False
tiempo_ultimo_fotograma = 0
intervalo_fotograma = 500

# Aparición del personaje enemigo
tiempo_entre_apariciones = 10000
duracion_aparicion = 3000
tiempo_ultima_aparicion = 0
mostrar_personaje = False
frame_personaje_actual = 0
tiempo_ultimo_frame_personaje = 0
intervalo_frame_personaje = 500
tiempo_inicio_aparicion = 0

# Control jumpscare
jumpscare_activado_por_aparicion = False
jumpscare_activo = False
jumpscare_tiempo_inicio = 0
duracion_jumpscare = 3000
jumpscare_temblor_intensidad = 15
frame_jumpscare_actual = 0
tiempo_ultimo_frame_jumpscare = 0
intervalo_frame_jumpscare = 500

botones = {
    "Nuevo Juego": pygame.Rect(100, ventana.get_height() // 2 - 100, 200, 50),
    "Continuar": pygame.Rect(100, ventana.get_height() // 2, 200, 50),
    "Extras": pygame.Rect(100, ventana.get_height() // 2 + 100, 200, 50)
}

def dibujar_botones():
    for texto, rect in botones.items():
        texto_boton = fuente_texto.render(texto, True, blanco)
        ventana.blit(texto_boton, (
            rect.x + (rect.width - texto_boton.get_width()) // 2,
            rect.y + (rect.height - texto_boton.get_height()) // 2
        ))

def aplicar_temblor(surface, intensidad):
    offset_x = random.randint(-intensidad, intensidad)
    offset_y = random.randint(-intensidad, intensidad)
    ventana.blit(surface, (offset_x, offset_y))

while True:
    tiempo_actual = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if pantalla == "menu" and event.type == pygame.MOUSEBUTTONDOWN:
            if botones["Nuevo Juego"].collidepoint(event.pos):
                pantalla = "noche_1"
                mostrar_hora = True
                tiempo_hora_inicio = tiempo_actual
                inicio_noche = tiempo_actual
                tiempo_ultima_aparicion = tiempo_actual
                mostrar_personaje = False
                jumpscare_activo = False
                jumpscare_activado_por_aparicion = False
                tiempo_inicio_aparicion = 0
                pygame.mixer.music.stop()

        if pantalla == "noche_1" and event.type == pygame.MOUSEBUTTONDOWN:
            if not puerta_animando and boton.collidepoint(event.pos):
                puerta_abierta = not puerta_abierta
                puerta_animando = True
                tiempo_ultimo_fotograma = tiempo_actual
                if puerta_abierta:
                    puerta_fotograma_actual = len(puerta_fotogramas) - 1
                    animacion_inversa = True
                else:
                    puerta_fotograma_actual = 0
                    animacion_inversa = False

    ventana.fill(negro)

    if pantalla == "advertencia":
        if alpha < 255:
            alpha += velocidad_fade
            alpha = min(alpha, 255)
            titulo_surf.set_alpha(alpha)
            advertencia_surf.set_alpha(alpha)

        ventana.blit(titulo_surf, titulo_rect)
        ventana.blit(advertencia_surf, advertencia_rect)

        if alpha == 255:
            tiempo_transcurrido += 1 / 60
            if tiempo_transcurrido >= tiempo_espera:
                pantalla = "menu"

    elif pantalla == "menu":
        titulo_menu = fuente_titulo.render("cinco noches con los brainrots", True, rojo_intenso)
        ventana.blit(titulo_menu, (20, 20))
        dibujar_botones()

    elif pantalla == "noche_1":
        if mostrar_hora:
            ventana.fill(negro)
            texto_noche = fuente_noche.render("12 AM - 1 Noche", True, blanco)
            rect_noche = texto_noche.get_rect(center=(1365 // 2, 780 // 2))
            ventana.blit(texto_noche, rect_noche)

            if tiempo_actual - tiempo_hora_inicio > 3000:
                mostrar_hora = False
        else:
            if jumpscare_activo:
                tiempo_jumpscare = tiempo_actual - jumpscare_tiempo_inicio

                if tiempo_actual - tiempo_ultimo_frame_jumpscare >= intervalo_frame_jumpscare:
                    tiempo_ultimo_frame_jumpscare = tiempo_actual
                    frame_jumpscare_actual += 1
                    if frame_jumpscare_actual >= len(jumpscare_frames):
                        frame_jumpscare_actual = len(jumpscare_frames) - 1

                if tiempo_jumpscare <= duracion_jumpscare:
                    aplicar_temblor(jumpscare_frames[frame_jumpscare_actual], jumpscare_temblor_intensidad)
                else:
                    pantalla = "menu"
                    jumpscare_activo = False
                    jumpscare_activado_por_aparicion = False
                    pygame.mixer.music.play(-1, 0.0)

                pygame.display.flip()
                clock.tick(60)
                continue

            ventana.blit(oficina, (0, 0))

            if puerta_animando:
                if animacion_inversa:
                    if tiempo_actual - tiempo_ultimo_fotograma >= intervalo_fotograma:
                        tiempo_ultimo_fotograma = tiempo_actual
                        puerta_fotograma_actual -= 1
                        if puerta_fotograma_actual < 0:
                            puerta_animando = False
                else:
                    if tiempo_actual - tiempo_ultimo_fotograma >= intervalo_fotograma:
                        tiempo_ultimo_fotograma = tiempo_actual
                        puerta_fotograma_actual += 1
                        if puerta_fotograma_actual >= len(puerta_fotogramas):
                            puerta_animando = False

            if 0 <= puerta_fotograma_actual < len(puerta_fotogramas):
                ventana.blit(puerta_fotogramas[puerta_fotograma_actual], (0, 0))
            elif not puerta_abierta:
                ventana.blit(puerta_fotogramas[-1], (0, 0))

            if not mostrar_personaje and tiempo_actual - tiempo_ultima_aparicion >= tiempo_entre_apariciones:
                mostrar_personaje = True
                tiempo_ultima_aparicion = tiempo_actual
                frame_personaje_actual = 0
                tiempo_ultimo_frame_personaje = tiempo_actual
                jumpscare_activado_por_aparicion = False
                tiempo_inicio_aparicion = tiempo_actual

            if mostrar_personaje and puerta_abierta:
                if tiempo_actual - tiempo_ultimo_frame_personaje >= intervalo_frame_personaje:
                    tiempo_ultimo_frame_personaje = tiempo_actual
                    frame_personaje_actual += 1
                    if frame_personaje_actual >= len(personaje_frames):
                        frame_personaje_actual = len(personaje_frames) - 1

                ventana.blit(personaje_frames[frame_personaje_actual], (0, 0))

                if tiempo_actual - tiempo_ultima_aparicion >= duracion_aparicion:
                    mostrar_personaje = False
                    jumpscare_activado_por_aparicion = False
                    tiempo_inicio_aparicion = 0

                tiempo_visible = tiempo_actual - tiempo_inicio_aparicion
                if puerta_abierta and mostrar_personaje and tiempo_visible > 500 and not jumpscare_activo and not jumpscare_activado_por_aparicion:
                    jumpscare_activo = True
                    jumpscare_tiempo_inicio = tiempo_actual
                    frame_jumpscare_actual = 0
                    tiempo_ultimo_frame_jumpscare = tiempo_actual
                    mostrar_personaje = False
                    jumpscare_activado_por_aparicion = True
                    sonido_jumpscare.play()

            if tiempo_actual - inicio_noche >= tiempo_por_hora:
                hora_actual += 1
                inicio_noche = tiempo_actual
                if hora_actual >= 6:
                    jumpscare_activo = True
                    jumpscare_tiempo_inicio = tiempo_actual
                    frame_jumpscare_actual = 0
                    tiempo_ultimo_frame_jumpscare = tiempo_actual

    pygame.display.flip()
    clock.tick(60)



































































    pygame.display.flip()



