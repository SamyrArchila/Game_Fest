import pygame
import sys

# Colores
negro = (0, 0, 0)
rojo_intenso = (200, 0, 0)
blanco = (255, 255, 255)

pygame.init()
pygame.mixer.init()

ventana = pygame.display.set_mode((1365, 780))
pygame.display.set_caption("MIEDDDOOO")
clock = pygame.time.Clock()

# Música
pygame.mixer.music.load("sounds/menu-o-creditos.ogg")
pygame.mixer.music.play(-1, 0.0)

# Imagen del personaje
selfie = pygame.image.load("img/tralalero.png").convert_alpha()

# Posicionar selfie a la derecha centrado
selfie_rect = selfie.get_rect()
selfie_rect.right = 1365 - 50  # Margen derecho
selfie_rect.centery = 780 // 2

# Fuentes
fuente_titulo = pygame.font.SysFont("OCR A Extended", 60, bold=True)
fuente_texto = pygame.font.SysFont("Courier New", 24, bold=True)
fuente_noche = pygame.font.SysFont("OCR A Extended", 50, bold=True)

# Textos de advertencia
texto_titulo = fuente_titulo.render("⚠ ¡ADVERTENCIA! ⚠", True, rojo_intenso)
texto_advertencia = fuente_texto.render(
    "Este juego contiene luces parpadeantes, ruidos fuertes y muchos sustos repentinos",
    True, blanco
)

# Crear superficies con canal alfa
titulo_surf = texto_titulo.convert_alpha()
advertencia_surf = texto_advertencia.convert_alpha()

# Posiciones
titulo_rect = titulo_surf.get_rect(center=(1365 // 2 - 30, 300))
advertencia_rect = advertencia_surf.get_rect(center=(1365 // 2, 370))

# Transparencia y temporizador
alpha = 0
velocidad_fade = 2
tiempo_espera = 3
tiempo_transcurrido = 0

pantalla = "advertencia"
mostrar_hora = False
tiempo_hora_inicio = 0

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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

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
        titulo_menu = fuente_titulo.render("Cinco noches con Tralalero Tralala", True, rojo_intenso)
        ventana.blit(titulo_menu, (20, 20))
        dibujar_botones()

        # Dibujar selfie del personaje
        ventana.blit(selfie, selfie_rect)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if botones["Nuevo Juego"].collidepoint(event.pos):
                pantalla = "noche_1"
                mostrar_hora = True
                tiempo_hora_inicio = pygame.time.get_ticks()

    elif pantalla == "noche_1":
        if mostrar_hora:
            texto_noche = fuente_noche.render("12 AM - 1 Noche", True, blanco)
            rect_noche = texto_noche.get_rect(center=(1365 // 2, 780 // 2))
            ventana.blit(texto_noche, rect_noche)

            if pygame.time.get_ticks() - tiempo_hora_inicio > 3000:
                mostrar_hora = False

    pygame.display.flip()
    clock.tick(60)




























































    pygame.display.flip()



