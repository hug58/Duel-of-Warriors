import pymunk
import pygame
import pymunk.pygame_util

# Inicializar Pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# Crear un espacio de Pymunk
espacio = pymunk.Space()

# Crear el cuerpo de la flecha
masa_cuerpo = 1.0
longitud_cuerpo = 100
cuerpo_flecha = pymunk.Body(masa_cuerpo, pymunk.moment_for_segment(masa_cuerpo, (0, 0), (0, longitud_cuerpo),1))
cuerpo_flecha.position = (400, 300)

# Crear la forma del cuerpo de la flecha
forma_flecha = pymunk.Segment(cuerpo_flecha, (0, 0), (0, longitud_cuerpo), 5)
forma_flecha.elasticity = 0.5
espacio.add(cuerpo_flecha, forma_flecha)

# Crear la punta de la flecha
masa_punta = 5.0  # Peso mayor para la punta
radio_punta = 10
cuerpo_punta = pymunk.Body(masa_punta, pymunk.moment_for_circle(masa_punta, 0, radio_punta))
cuerpo_punta.position = (400, 300 + longitud_cuerpo)  # Colocar la punta en la parte superior del cuerpo

# Crear la forma de la punta
forma_punta = pymunk.Circle(cuerpo_punta, radio_punta)
forma_punta.elasticity = 0.5
espacio.add(cuerpo_punta, forma_punta)

# Conectar la punta al cuerpo de la flecha
junta = pymunk.PinJoint(cuerpo_flecha, cuerpo_punta, (0, longitud_cuerpo), (0, 0))
espacio.add(junta)
draw_options = pymunk.pygame_util.DrawOptions(screen)
# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualizar el espacio
    espacio.step(1/60.0)

    # Dibujar
    screen.fill((255, 255, 255))
    # pymunk.pygame_util.draw(espacio, screen)
    espacio.debug_draw(draw_options)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
