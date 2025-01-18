import pygame
import pymunk
import sys

from pymunk.examples.arrows import width

# Inicializar Pygame
pygame.init()

# Cargar la imagen de la flecha
arrow_image = pygame.image.load("assets/arrow.png")
# Crear el espacio de Pymunk
space = pymunk.Space()
space.gravity = (0, 900)  # Gravedad hacia abajo
# Crear la clase de la flecha
# Función para crear el piso
def crear_piso():
    width = 600

    body = pymunk.Body(body_type=pymunk.Body.STATIC)  # Cuerpo estático
    body.position = (0, 500)  # Posición del piso
    shape = pymunk.Segment(body, (-400, 0), (600, 0), 20)  # Crear un segmento
    shape.friction = 0.5  # Fricción del piso
    space.add(body, shape)

class Arrow(object):
    def __init__(self, x, y, angle):
        self.body = pymunk.Body(1, 100, body_type=pymunk.Body.DYNAMIC)
        self.body.position = x, y
        self.body.angle = angle
        self.shape = pymunk.Poly.create_box(self.body, (50, 10))
        self.shape.friction = 0.5
        self.shape.elasticity = 0.3
        space.add(self.body, self.shape)  # Añadir la flecha al espacio

    def update(self):
        # Actualizar la posición y rotación de la flecha
        self.x, self.y = self.body.position
        self.angle = self.body.angle

    def draw(self, screen):
        # Dibujar la flecha en la pantalla
        rotated_image = pygame.transform.rotate(arrow_image, -self.angle * 180 / 3.14159)
        rect = rotated_image.get_rect()
        rect.center = (self.x, self.y)
        screen.blit(rotated_image, rect)

    def launch(self):
        # Aplicar fuerza al lanzar la flecha
        force = (20, -1000)  # Fuerza hacia la derecha
        self.body.apply_impulse_at_local_point(force, (0, 0))
        print(self.body)

# Crear una flecha y aplicar fuerzas
arrow = Arrow(100, 100, 62)
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
crear_piso()

# Bucle principal del juego
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit(1)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Al presionar la barra espaciadora
                arrow.launch()  # Lanza la flecha
    # Actualizar la flecha
    arrow.update()
    space.step(1/60.0)  # Avanzar el espacio en el tiempo


    # Dibujar el piso
    screen.fill((255, 255, 255))

    pygame.draw.line(screen, (0, 0, 0), (0, 500), (width, 500), 5)

    # Dibujar la flecha
    arrow.draw(screen)
    pygame.display.flip()
    clock.tick(60)  # Limitar a 60 FPS
