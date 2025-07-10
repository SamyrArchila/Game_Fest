import sys
import random
import pygame

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

# Música
pygame.mixer.music.load("sounds/menu-o-creditos.ogg")
pygame.mixer.music.play(-1)

# Sonido jumpscare
sonido_jumpscare = pygame.mixer.Sound("sounds/jumpscare.ogg")

# Oficina
oficina = pygame.transform.scale(pygame.image.load("img/Oficina_normal.png").convert_alpha(), (1365, 780))

# Puertas
puerta_fotogramas = [
    pygame.transform.scale(pygame.image.load(f"img/Puerta_izquierda_{i+1}.png").convert_alpha(), (1365, 780))
    for i in range(4)
]

puerta_derecha_fotogramas = [
    pygame.transform.scale(pygame.image.load(f"img/Puerta_derecha_{i+1}.png").convert_alpha(), (1365, 780))
    for i in range(4)
]

# Oficina cerrada
puerta_derecha_cerrada = pygame.transform.scale(pygame.image.load("img/Oficina_cerrada.png").convert_alpha(), (1365, 780))

# Interferencias
interferencias = [
    pygame.transform.scale(pygame.image.load("img/interferencia_1.png").convert_alpha(), (1365, 780)),
    pygame.transform.scale(pygame.image.load("img/interferencia_2.png").convert_alpha(), (1365, 780))
]

# Personaje
personaje_frames = [
    pygame.transform.scale(pygame.image.load("img/Oficina_Tralalelo_1_V2.png").convert_alpha(), (1365, 780)),
    pygame.transform.scale(pygame.image.load("img/Oficina_Tralalelo_2_v2.png").convert_alpha(), (1365, 780)),
    pygame.transform.scale(pygame.image.load("img/Oficina_Tralalelo_3_V2.png").convert_alpha(), (1365, 780)),
    pygame.transform.scale(pygame.image.load("img/Oficina_Tralalelo_4_V2.png").convert_alpha(), (1365, 780)),
]

# Jumpscare
jumpscare_frames = [
    pygame.transform.scale(pygame.image.load("img/Tralalelo_jumpscare.png").convert_alpha(), (1365, 780)),
    pygame.transform.scale(pygame.image.load("img/tralalero_jumpscare2.png").convert_alpha(), (1365, 780)),
    pygame.transform.scale(pygame.image.load("img/tralalerojumpscare3}.png").convert_alpha(), (1365, 780)),
]

# Fuente
fuente_titulo = pygame.font.SysFont("OCR A Extended", 60, bold=True)
fuente_texto = pygame.font.SysFont("Courier New", 24, bold=True)
fuente_noche = pygame.font.SysFont("OCR A Extended", 50, bold=True)

# Advertencia
texto_titulo = fuente_titulo.render("⚠ ¡ADVERTENCIA! ⚠", True, rojo_intenso)
texto_advertencia = fuente_texto.render("Este juego contiene luces parpadeantes, ruidos fuertes y muchos sustos repentinos", True, blanco)
titulo_surf = texto_titulo.convert_alpha()
advertencia_surf = texto_advertencia.convert_alpha()
titulo_rect = titulo_surf.get_rect(center=(1365 // 2 - 30, 300))
advertencia_rect = advertencia_surf.get_rect(center=(1365 // 2, 370))

# Botones
botones = {
    "Nuevo Juego": pygame.Rect(100, ventana.get_height() // 2 - 100, 200, 50),
    "Continuar": pygame.Rect(100, ventana.get_height() // 2, 200, 50),
    "Extras": pygame.Rect(100, ventana.get_height() // 2 + 100, 200, 50)
}

# Estado del juego
pantalla = "advertencia"
alpha = 0
velocidad_fade = 2
tiempo_espera = 3
tiempo_transcurrido = 0
mostrar_hora = False
tiempo_hora_inicio = 0
inicio_noche = 0
hora_actual = 0
tiempo_por_hora = 60000
energia = 100

# Datos puertas
datos_puerta = {
    "abierta": True,
    "animando": False,
    "fotograma": 0,
    "inversa": False,
    "ultimo": 0,
    "intervalo": 200,
    "boton": pygame.Rect(260, 250, 60, 60),
    "apertura": 0
}

datos_derecha = {
    "abierta": True,
    "animando": False,
    "fotograma": 0,
    "inversa": False,
    "ultimo": 0,
    "intervalo": 200,
    "boton": pygame.Rect(1045, 250, 60, 60)
}

# Enemigo y jumpscare
TIEMPO_MINIMO_PUERTA_ABIERTA = 1000
t_i_a = 10000
d_a = 3000
t_u_a = 0
mostrar_personaje = False
frame_personaje_actual = 0
t_u_f_p = 0
i_f_p = 500
t_i_aparicion = 0

jumpscare_activo = False
j_t_i = 0
d_j = 3000
j_temblor = 15
f_j_c = 0
t_u_f_j = 0
i_f_j = 500

# Funciones auxiliares
def aplicar_temblor(surf, intensidad):
    x = random.randint(-intensidad, intensidad)
    y = random.randint(-intensidad, intensidad)
    ventana.blit(surf, (x, y))

def dibujar_barra_bateria():
    barra_ancho = 200
    barra_alto = 20
    borde = pygame.Rect(ventana.get_width() - barra_ancho - 30, 30, barra_ancho, barra_alto)
    relleno = pygame.Rect(ventana.get_width() - barra_ancho - 30, 30, barra_ancho * (energia / 100), barra_alto)
    pygame.draw.rect(ventana, blanco, borde, 2)
    pygame.draw.rect(ventana, verde if energia > 30 else rojo_intenso, relleno)

def dibujar_botones():
    for texto, rect in botones.items():
        ventana.blit(fuente_texto.render(texto, True, blanco), rect.topleft)

# Loop principal
while True:
    t_a = pygame.time.get_ticks()

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if pantalla == "menu" and e.type == pygame.MOUSEBUTTONDOWN:
            if botones["Nuevo Juego"].collidepoint(e.pos):
                pantalla = "noche_1"
                mostrar_hora = True
                tiempo_hora_inicio = t_a
                inicio_noche = t_a
                t_u_a = t_a
                mostrar_personaje = False
                jumpscare_activo = False
                hora_actual = 0
                energia = 100
                pygame.mixer.music.stop()

        if pantalla == "noche_1" and e.type == pygame.MOUSEBUTTONDOWN:
            for datos, frames in zip((datos_puerta, datos_derecha), (puerta_fotogramas, puerta_derecha_fotogramas)):
                if not datos["animando"] and datos["boton"].collidepoint(e.pos):
                    datos["abierta"] = not datos["abierta"]
                    datos["animando"] = True
                    datos["ultimo"] = t_a
                    datos["fotograma"] = 0
                    datos["inversa"] = not datos["abierta"]
                    if datos is datos_puerta:
                        datos["apertura"] = t_a

    ventana.fill(negro)

    if pantalla == "advertencia":
        if alpha < 255:
            alpha = min(255, alpha + velocidad_fade)
            titulo_surf.set_alpha(alpha)
            advertencia_surf.set_alpha(alpha)
        ventana.blit(titulo_surf, titulo_rect)
        ventana.blit(advertencia_surf, advertencia_rect)
        if alpha == 255:
            tiempo_transcurrido += 1 / 60
            if tiempo_transcurrido >= tiempo_espera:
                pantalla = "menu"

    elif pantalla == "menu":
        ventana.blit(fuente_titulo.render("cinco noches con los brainrots", True, rojo_intenso), (20, 20))
        dibujar_botones()

    elif pantalla == "noche_1":
        if mostrar_hora:
            ventana.fill(negro)
            ventana.blit(fuente_noche.render("12 AM - 1 Noche", True, blanco), (500, 350))
            if t_a - tiempo_hora_inicio > 3000:
                mostrar_hora = False
        else:
            if jumpscare_activo:
                if t_a - t_u_f_j >= i_f_j:
                    t_u_f_j = t_a
                    f_j_c = min(f_j_c + 1, len(jumpscare_frames) - 1)
                if t_a - j_t_i <= d_j:
                    aplicar_temblor(jumpscare_frames[f_j_c], j_temblor)
                elif t_a - j_t_i <= d_j + 2000:
                    ventana.blit(interferencias[(t_a // 100) % 2], (0, 0))
                else:
                    pantalla = "menu"
                    jumpscare_activo = False
                    pygame.mixer.music.play(-1, 0.0)
                pygame.display.flip()
                clock.tick(60)
                continue

            ventana.blit(oficina, (0, 0))

            # Animación de puertas
            for datos, frames in zip((datos_puerta, datos_derecha), (puerta_fotogramas, puerta_derecha_fotogramas)):
                if datos["animando"] and t_a - datos["ultimo"] >= datos["intervalo"]:
                    datos["ultimo"] = t_a
                    if datos["inversa"]:  # Animar apertura (del 4 al 1)
                        datos["fotograma"] -= 1
                        if datos["fotograma"] < 0:
                            datos["animando"] = False
                            datos["fotograma"] = -1
                    else:  # Animar cierre (del 1 al 4)
                     datos["fotograma"] += 1
                    if datos["fotograma"] >= len(frames):
                        datos["animando"] = False
                        datos["fotograma"] = len(frames) - 1
            # Dibujar puertas
            for datos, frames in zip((datos_puerta, datos_derecha), (puerta_fotogramas, puerta_derecha_fotogramas)):
                if datos["animando"]:
                    if 0 <= datos["fotograma"] < len(frames):
                        ventana.blit(frames[datos["fotograma"]], (0, 0))
                elif not datos["abierta"]:  # Puerta cerrada (mostrar último frame)
                    ventana.blit(frames[-1], (0, 0))

            pygame.draw.rect(ventana, rojo_intenso if not datos_puerta["abierta"] else verde, datos_puerta["boton"])
            pygame.draw.rect(ventana, rojo_intenso if not datos_derecha["abierta"] else verde, datos_derecha["boton"])

            texto_hora = fuente_noche.render(f"{hora_actual + 12 if hora_actual == 0 else hora_actual}:00 AM", True, blanco)
            ventana.blit(texto_hora, (ventana.get_width() - 250, 720))

            if not mostrar_personaje and t_a - t_u_a >= t_i_a:
                mostrar_personaje = True
                t_u_a = t_a
                frame_personaje_actual = 0
                t_u_f_p = t_a
                t_i_aparicion = t_a

            if mostrar_personaje:
                if t_a - t_u_f_p >= i_f_p:
                    t_u_f_p = t_a
                    frame_personaje_actual = min(frame_personaje_actual + 1, len(personaje_frames) - 1)
                if datos_puerta["abierta"] and not datos_puerta["animando"]:
                    ventana.blit(personaje_frames[frame_personaje_actual], (0, 0))
                if t_a - t_i_aparicion >= d_a:
                    mostrar_personaje = False
                if datos_puerta["abierta"] and not datos_puerta["animando"] and (t_a - datos_puerta["apertura"] > TIEMPO_MINIMO_PUERTA_ABIERTA) and (t_a - t_i_aparicion > 500):
                    jumpscare_activo = True
                    j_t_i = t_a
                    f_j_c = 0
                    t_u_f_j = t_a
                    mostrar_personaje = False
                    sonido_jumpscare.play()

            puerta_izq_abierta = datos_puerta["abierta"] or datos_puerta["animando"]
            puerta_der_abierta = datos_derecha["abierta"] or datos_derecha["animando"]

            consumo = 0 if puerta_izq_abierta and puerta_der_abierta else 0.02 if puerta_izq_abierta or puerta_der_abierta else 0.04
            energia = max(0, energia - consumo)
            dibujar_barra_bateria()

            if energia <= 0 and not jumpscare_activo:
                jumpscare_activo = True
                j_t_i = t_a
                f_j_c = 0
                t_u_f_j = t_a
                sonido_jumpscare.play()

            if t_a - inicio_noche >= tiempo_por_hora:
                hora_actual += 1
                inicio_noche = t_a
                if hora_actual >= 6:
                    pantalla = "menu"
                    pygame.mixer.music.play(-1, 0.0)

    pygame.display.flip()
    clock.tick(60)








































































    pygame.display.flip()



