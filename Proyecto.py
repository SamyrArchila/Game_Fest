import sys
import random
import pygame
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

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
pygame.mixer.music.load(os.path.join("sounds", "menu-o-creditos.ogg"))
pygame.mixer.music.play(-1)

# Sonido jumpscare
sonido_jumpscare = pygame.mixer.Sound("sounds/jumpscare.ogg")

# Imagen y música para cuando se acaba la energía
imagen_sin_energia = pygame.transform.scale(
    pygame.image.load("img/tralalero tralala.png").convert_alpha(), (1365, 780)
)
musica_sin_energia = pygame.mixer.Sound(os.path.join("sounds", "FNAF-1-Freddy-Jumpscare.ogg"))


# Oficina
oficina = pygame.transform.scale(pygame.image.load("img/Oficina_normal.png").convert_alpha(), (1365, 780))

# Puertas (invertimos el orden para que se animen de abajo hacia arriba)
puerta_fotogramas = [
    pygame.transform.scale(pygame.image.load(f"img/Puerta_izquierda_{i+1}.png").convert_alpha(), (1365, 780))
    for i in reversed(range(4))
]
puerta_derecha_fotogramas = [
    pygame.transform.scale(pygame.image.load(f"img/Puerta_derecha_{i+1}.png").convert_alpha(), (1365, 780))
    for i in reversed(range(4))
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
    pygame.transform.scale(pygame.image.load(f"img/Oficina_Tralalelo_{i+1}_V2.png").convert_alpha(), (1365, 780))
    for i in range(4)
]

# Jumpscares

sahur_jumpscare_frames = [
    pygame.transform.scale(pygame.image.load("img/sahur jumpscare1.png").convert_alpha(), (1365, 780)),
    pygame.transform.scale(pygame.image.load("img/sahur jumpscare2.png").convert_alpha(), (1365, 780)),
    pygame.transform.scale(pygame.image.load("img/sahur jumpscare3.png").convert_alpha(), (1365, 780)),
]

jumpscare_frames = [
    pygame.transform.scale(pygame.image.load("img/Tralalelo_jumpscare.png").convert_alpha(), (1365, 780)),
    pygame.transform.scale(pygame.image.load("img/tralalero_jumpscare2.png").convert_alpha(), (1365, 780)),
    pygame.transform.scale(pygame.image.load("img/tralalerojumpscare3.png").convert_alpha(), (1365, 780))
]

# Fuente
fuente_titulo = pygame.font.SysFont("OCR A Extended", 60, bold=True)
fuente_texto = pygame.font.SysFont("Courier New", 24, bold=True)
fuente_noche = pygame.font.SysFont("OCR A Extended", 50, bold=True)

# Advertencia
titulo_surf = fuente_titulo.render("\u26a0 \u00a1ADVERTENCIA! \u26a0", True, rojo_intenso).convert_alpha()
advertencia_surf = fuente_texto.render(
    "Este juego contiene luces parpadeantes, ruidos fuertes y muchos sustos repentinos",
    True, blanco
).convert_alpha()
titulo_rect = titulo_surf.get_rect(center=(1365 // 2 - 30, 300))
advertencia_rect = advertencia_surf.get_rect(center=(1365 // 2, 370))

# Botones
botones = {
    "Nuevo Juego": pygame.Rect(100, ventana.get_height() // 2 - 100, 200, 50),
    "Continuar": pygame.Rect(100, ventana.get_height() // 2, 200, 50),
    "Extras": pygame.Rect(100, ventana.get_height() // 2 + 100, 200, 50)
}

botones_extras = {
    "Volver": pygame.Rect(50, 700, 150, 40)
}

# Logo Tralalero Entertainment
logo_tralalero = pygame.transform.scale(
    pygame.image.load("img/tralalero entertaiment.jpg").convert_alpha(), (300, 150)
)


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
energia_agotada = False
inicio_musica_sin_energia = 0


tipo_jumpscare = "tralalelo"  # Valor por defecto

# Datos puertas
datos_puerta = {"abierta": True, "animando": False, "fotograma": 0, "inversa": False, "ultimo": 0, "intervalo": 200, "boton": pygame.Rect(260, 250, 60, 60), "apertura": 0}
datos_derecha = {"abierta": True, "animando": False, "fotograma": 0, "inversa": False, "ultimo": 0, "intervalo": 200, "boton": pygame.Rect(1045, 250, 60, 60)}

# Jumpscare especial tungtungsahur
sonido_tungtungsahur = pygame.mixer.Sound("sounds/tungtungsahur_zapatazo.ogg")
tungtungsahur_sono = False
tungtungsahur_activado = False
tungtungsahur_tiempo = pygame.time.get_ticks() + random.randint(15000, 40000)
tungtungsahur_inicio = 0
tungtungsahur_defendido = False



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

def aplicar_temblor(surf, intensidad):
    x = random.randint(-intensidad, intensidad)
    y = random.randint(-intensidad, intensidad)
    ventana.blit(surf, (x, y))

def dibujar_barra_bateria():
    barra_ancho = 200
    barra_alto = 20
    borde = pygame.Rect(ventana.get_width() - barra_ancho - 30, 30, barra_ancho, barra_alto)
    relleno = pygame.Rect(ventana.get_width() - barra_ancho - 30, 30, barra_ancho * (energia / 100), barra_alto)

    # Cambiar color dinámico de la barra
    if energia > 30:
        color = verde
    elif energia > 10:
        color = rojo_intenso
    else:
        # Parpadeo entre rojo y negro cuando la batería es crítica
        if pygame.time.get_ticks() // 300 % 2 == 0:
            color = rojo_intenso
        else:
            color = negro

    pygame.draw.rect(ventana, blanco, borde, 2)
    pygame.draw.rect(ventana, color, relleno)

    # Mostrar porcentaje
    texto_bateria = fuente_texto.render(f"{int(energia)}%", True, blanco)
    ventana.blit(texto_bateria, (ventana.get_width() - 80, 55))

    # Alerta visual cuando está muy baja
    if energia <= 10:
        alerta_texto = fuente_texto.render("¡BATERÍA CRÍTICA!", True, rojo_intenso)
        ventana.blit(alerta_texto, (ventana.get_width() - 250, 5))


def dibujar_manual():
    ventana.fill(negro)
    ventana.blit(fuente_titulo.render("MANUAL DE JUEGO", True, rojo_intenso), (400, 50))

    instrucciones = [
        "- Usa los botones a los lados de la oficina para cerrar las puertas.",
        "- Evita que los personajes entren o te harán jumpscare.",
        "- Si oyes un zapatazo (tungtungsahur), ¡reacciona rápido!",
        "- La batería es limitada. No mantengas las puertas cerradas sin motivo.",
        "- Sobrevive desde las 12 AM hasta las 6 AM.",
        "- Si se acaba la energía, aparecerá Tralalero...",
        "- Puedes volver al menú con el botón 'Volver'."
    ]

    for i, texto in enumerate(instrucciones):
        superficie = fuente_texto.render(texto, True, blanco)
        ventana.blit(superficie, (100, 150 + i * 40))

    pygame.draw.rect(ventana, rojo_intenso, botones_extras["Volver"], 2)
    ventana.blit(fuente_texto.render("Volver", True, blanco), botones_extras["Volver"].topleft)

def dibujar_botones():
    for texto, rect in botones.items():
        pygame.draw.rect(ventana, rojo_intenso, rect, 2)  # Dibujar borde rojo
        superficie_texto = fuente_texto.render(texto, True, blanco)
        ventana.blit(superficie_texto, rect.topleft)


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

            if botones["Continuar"].collidepoint(e.pos):
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

            if botones["Extras"].collidepoint(e.pos):
                pantalla = "Extras"

        if pantalla == "Extras" and e.type == pygame.MOUSEBUTTONDOWN:
            if botones_extras["Volver"].collidepoint(e.pos):
                pantalla = "menu"
        
        
        if pantalla == "noche_1" and e.type == pygame.MOUSEBUTTONDOWN:
            for datos, frames in zip((datos_puerta, datos_derecha), (puerta_fotogramas, puerta_derecha_fotogramas)):
                if not datos["animando"] and datos["boton"].collidepoint(e.pos):
                    datos["inversa"] = datos["abierta"]
                    datos["abierta"] = not datos["abierta"]
                    datos["animando"] = True
                    datos["ultimo"] = t_a
                    datos["fotograma"] = len(frames) - 1 if datos["inversa"] else 0
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
        ventana.blit(fuente_titulo.render("SOBREVIVE LA NOCHE", True, rojo_intenso), (20, 20))
        dibujar_botones()

# Mostrar logo a la derecha
        # Parpadeo suave del logo (alpha)
        alpha_logo = abs(int(255 * (pygame.time.get_ticks() % 2000) / 1000 - 255)) if (pygame.time.get_ticks() // 1000) % 2 == 0 else 255

        # Crear una copia del logo con alpha aplicado
        logo_temp = logo_tralalero.copy()
        logo_temp.set_alpha(alpha_logo)

        # Mostrar el logo en parte inferior derecha sin tapar
        pos_x = ventana.get_width() - logo_tralalero.get_width() - 20
        pos_y = ventana.get_height() - logo_tralalero.get_height() - 30
        ventana.blit(logo_temp, (pos_x, pos_y))

    elif pantalla == "Extras":
        dibujar_manual()


    elif pantalla == "noche_1":
        if mostrar_hora:
            ventana.fill(negro)
            ventana.blit(fuente_noche.render("12 AM - 1 Noche", True, blanco), (500, 350))
            if t_a - tiempo_hora_inicio > 3000:
                mostrar_hora = False
        else:
            if jumpscare_activo:
                frames_jumpscare_actual = sahur_jumpscare_frames if tipo_jumpscare == "sahur" else jumpscare_frames

                if t_a - t_u_f_j >= i_f_j:
                    t_u_f_j = t_a
                    f_j_c = min(f_j_c + 1, len(frames_jumpscare_actual) - 1)
                if t_a - j_t_i <= d_j:
                    aplicar_temblor(frames_jumpscare_actual[f_j_c], j_temblor)

                elif t_a - j_t_i <= d_j + 2000:
                    ventana.blit(interferencias[(t_a // 100) % 2], (0, 0))
                else:
                    
                    pantalla = "menu"
                    jumpscare_activo = False
                    tipo_jumpscare = "tralalelo"  # Reinicia al valor por defecto
                    pygame.mixer.music.play(-1, 0.0)

                pygame.display.flip()
                clock.tick(60)
                continue

            ventana.blit(oficina, (0, 0))

            if not tungtungsahur_sono and t_a >= tungtungsahur_tiempo:
                sonido_tungtungsahur.play()
                tungtungsahur_sono = True
                tungtungsahur_inicio = t_a

                if tungtungsahur_sono and not jumpscare_activo:
                    if not tungtungsahur_defendido:
                        if not datos_puerta["abierta"] and not datos_derecha["abierta"]:
                            tungtungsahur_defendido = True


            if tungtungsahur_sono:
                 if t_a - tungtungsahur_inicio >= sonido_tungtungsahur.get_length() * 1000:
                    tungtungsahur_sono = False
                    if not tungtungsahur_defendido:
                        if (
                            (datos_puerta["abierta"] and not datos_puerta["animando"]) or
                            (datos_derecha["abierta"] and not datos_derecha["animando"])
                        ):
                            tipo_jumpscare = "sahur"
                            jumpscare_activo = True
                            j_t_i = t_a
                            f_j_c = 0
                            t_u_f_j = t_a
                            sonido_jumpscare.play()
                    tungtungsahur_tiempo = t_a + random.randint(15000, 40000)
                    tungtungsahur_defendido = False

            for datos, frames in zip((datos_puerta, datos_derecha), (puerta_fotogramas, puerta_derecha_fotogramas)):
                if datos["animando"] and t_a - datos["ultimo"] >= datos["intervalo"]:
                    datos["ultimo"] = t_a
                    if datos["inversa"]:
                        datos["fotograma"] -= 1
                        if datos["fotograma"] < 0:
                            datos["animando"] = False
                            datos["fotograma"] = 0
                    else:
                        datos["fotograma"] += 1
                        if datos["fotograma"] >= len(frames):
                            datos["animando"] = False
                            datos["fotograma"] = len(frames) - 1

            for datos, frames in zip((datos_puerta, datos_derecha), (puerta_fotogramas, puerta_derecha_fotogramas)):
                if datos["animando"]:
                    if 0 <= datos["fotograma"] < len(frames):
                        ventana.blit(frames[datos["fotograma"]], (0, 0))
                elif not datos["abierta"]:
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

            if energia <= 0 and not jumpscare_activo and not energia_agotada:
                energia_agotada = True
                inicio_musica_sin_energia = t_a
                musica_sin_energia.play()
            
            if energia_agotada and not jumpscare_activo:
                ventana.blit(imagen_sin_energia, (0, 0))

                # Esperar a que termine el audio antes de iniciar el jumpscare visual
                if t_a - inicio_musica_sin_energia >= musica_sin_energia.get_length() * 1000:
                    tipo_jumpscare = "tralalelo"  # Asegurar que sea el jumpscare correcto
                    jumpscare_activo = True
                    j_t_i = t_a
                    f_j_c = 0
                    t_u_f_j = t_a
                    # NO reproducimos otro sonido aquí porque ya se oyó el largo



            if t_a - inicio_noche >= tiempo_por_hora:
                hora_actual += 1
                inicio_noche = t_a
                if hora_actual >= 6:
                    pantalla = "menu"
                    pygame.mixer.music.play(-1, 0.0)

    pygame.display.flip()
    clock.tick(60)









































































    pygame.display.flip()



