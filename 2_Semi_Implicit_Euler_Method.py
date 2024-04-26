import pygame, sys

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()
pygame.display.set_caption("2. Semi-Implicit Euler Method")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Object:
    def __init__(self, pos : pygame.Vector2):
        self.position = pos
        self.velocity = pygame.Vector2(0, 0)
        self.acceleration = pygame.Vector2(0, 0)

class Circle(Object):
    def __init__(self, pos : pygame.Vector2, radius : float):
        super(Circle, self).__init__(pos)
        self.radius = radius;
    def update(self, dt):
        # USING SEMI-IMPLICIT EULER METHOD (INSTEAD OF EULER METHOD)
        self.velocity += self.acceleration * dt
        self.position += self.velocity * dt
    def draw(self):
        pygame.draw.circle(screen, BLACK, self.position, self.radius)

circle = Circle(pygame.Vector2(1024/2, 0), 50)
circle.acceleration = pygame.Vector2(0, 100)


while True:
    deltaTime = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # UPDATING SECTION
    circle.update(deltaTime)
    
    if (circle.position.y - circle.radius > SCREEN_HEIGHT):
        circle.position.y = 0
        print("Velocity =", circle.velocity)
    # DRAWING SECTION
    screen.fill(WHITE)

    circle.draw()
    
    pygame.display.update()
pygame.quit()
sys.exit()
