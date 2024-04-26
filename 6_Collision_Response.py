import pygame, sys

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GRAVITATIONAL_CONSTANT = 0.0 # 1000.0

pygame.init()
pygame.display.set_caption("6. Collision Response")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Object:
    def __init__(self, pos : pygame.Vector2):
        self.position = pos
        self.velocity = pygame.Vector2(0, 0)
        self.force = pygame.Vector2(0, 0)
        self.mass = 1.0
        self.restitution = 1.0

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
        self.force = pygame.Vector2()
    def draw(self):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

circle1 = Circle(pygame.Vector2(1024/2, 600/2), 80)
circle2 = Circle(pygame.Vector2(0, 600/2), 50)

circle1.mass = 0.8
circle2.mass = 0.5

circle2.force = pygame.Vector2(5000, 0)

def CircleVsCircle(obj1, obj2):
    dist = obj1.radius + obj2.radius - (obj2.position - obj1.position).length()
    return [(obj2.position - obj1.position).length() <= obj1.radius + obj2.radius, (obj2.position - obj1.position).normalize() * dist * 0.5]

while True:
    deltaTime = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # UPDATING SECTION

    result, mtv = CircleVsCircle(circle1, circle2)
    if result:
        circle1.position -= mtv
        circle2.position += mtv
        relVel = circle2.velocity - circle1.velocity
        velAlongNormal = relVel.dot(mtv.normalize())
        if velAlongNormal <= 0:
            e = min(circle1.restitution, circle2.restitution)
            j = -(1 + e) * velAlongNormal
            j /= (1 / circle1.mass) + (1 / circle2.mass)
            impulse = mtv.normalize() * j
            circle1.velocity -= (1 / circle1.mass) * impulse
            circle2.velocity += (1 / circle2.mass) * impulse

        
    circle1.update(deltaTime)
    circle2.update(deltaTime)
        
    # DRAWING SECTION
    screen.fill(WHITE)

    circle1.draw()
    circle2.draw()
    
    pygame.display.update()

pygame.quit()
sys.exit()
