import pygame, sys

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GRAVITATIONAL_CONSTANT = 9.8

pygame.init()
pygame.display.set_caption("4. Force")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Object:
    def __init__(self, pos : pygame.Vector2):
        self.position = pos
        self.velocity = pygame.Vector2(0, 0)
        self.force = pygame.Vector2(0, 0)
        self.mass = 1.0

class Circle(Object):
    def __init__(self, pos : pygame.Vector2, radius : float):
        super(Circle, self).__init__(pos)
        self.radius = radius
        self.color = BLACK
    def update(self, dt):
        # IMPLEMENTING GRAVITY
        self.force.y += GRAVITATIONAL_CONSTANT
        # USING SEMI-IMPLICIT EULER METHOD
        self.velocity += (self.force / self.mass) * dt # F = ma -> a = F / m
        self.position += self.velocity * dt
    def draw(self):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

circle = Circle(pygame.Vector2(0, 200), 20)
circle.force = pygame.Vector2(500, -150)

tracing_count = 0
traces = []

while True:
    deltaTime = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # UPDATING SECTION
    
    if (circle.position.y + circle.radius > SCREEN_HEIGHT):
        pass
    else:
        if (tracing_count % 10 == 0):
            c = Circle(pygame.Vector2(circle.position), 10)
            c.color = RED
            traces.append(c)
        circle.update(deltaTime)
        print("Velocity =", circle.velocity)
    
    # DRAWING SECTION
    screen.fill(WHITE)

    for i in range(len(traces)):
        traces[i].draw()
    circle.draw()
    
    pygame.display.update()

    tracing_count += 1

pygame.quit()
sys.exit()
