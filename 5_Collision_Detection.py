import pygame, sys

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GRAVITATIONAL_CONSTANT = 9.8

pygame.init()
pygame.display.set_caption("5. Collision Detection")
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

circle1 = Circle(pygame.Vector2(1024/2, 600/2), 80)
circle2 = Circle(pygame.Vector2(0, 0), 50)

def CircleVsCircle(c1, c2):
    return (c2.position - c1.position).length() <= (c1.radius + c2.radius)


while True:
    deltaTime = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # UPDATING SECTION

    circle2.position = pygame.mouse.get_pos()

    if (CircleVsCircle(circle1, circle2)):
        circle1.color = RED
        circle2.color = RED
    else:
        circle1.color = BLACK
        circle2.color = BLACK
    
    # DRAWING SECTION
    screen.fill(WHITE)

    circle1.draw()
    circle2.draw()
    
    pygame.display.update()

pygame.quit()
sys.exit()
