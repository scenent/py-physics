import pygame, sys

SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 600

RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

GRAVITATIONAL_CONSTANT = 1000.0

pygame.init()
pygame.display.set_caption("7. Sandbox")
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

class Object:
    def __init__(self, pos : pygame.Vector2):
        self.position = pos
        self.velocity = pygame.Vector2(0, 0)
        self.force = pygame.Vector2(0, 0)
        self.mass = 1.0
        self.restitution = 1.0
        self.type = "Unknown"
        assert(self.mass != 0.0)
        
class Circle(Object):
    def __init__(self, pos : pygame.Vector2, radius : float):
        super(Circle, self).__init__(pos)
        self.radius = radius
        self.color = BLACK
        self.type = "Circle"
    def update(self, dt):
        # IMPLEMENTING GRAVITY
        self.force.y += GRAVITATIONAL_CONSTANT
        # USING SEMI-IMPLICIT EULER METHOD
        self.velocity += (self.force / self.mass) * dt # F = ma -> a = F / m           
        self.position += self.velocity * dt
        self.force = pygame.Vector2(0, 0)
    def draw(self):
        pygame.draw.circle(screen, self.color, self.position, self.radius)

def CircleVsCircle(obj1, obj2):
    dist = obj1.radius + obj2.radius - (obj2.position - obj1.position).length()
    return [(obj2.position - obj1.position).length() <= obj1.radius + obj2.radius, (obj2.position - obj1.position).normalize() * dist * 0.5]


objectList = []

myCircle = Circle(pygame.Vector2(512, 300), 50.0)
objectList.append(myCircle)
objectList.append(Circle(pygame.Vector2(312, 300), 50.0))
objectList.append(Circle(pygame.Vector2(712, 300), 50.0))

print("Press A / D to force middle circle.")

while True:
    deltaTime = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    # UPDATING SECTION

    if (pygame.key.get_pressed()[pygame.K_d]):
        myCircle.force.x += 1000
    if (pygame.key.get_pressed()[pygame.K_a]):
        myCircle.force.x -= 1000

    for o in objectList:
        if (o.position.x - o.radius < 0 and o.velocity.x < 0):
            o.position.x = o.radius
            o.velocity.x *= -1
        if (o.position.x + o.radius > 1024 and o.velocity.x > 0):
            o.position.x = 1024 - o.radius
            o.velocity.x *= -1
        if (o.position.y - o.radius < 0 and o.velocity.y < 0):
            o.position.y = o.radius
            o.velocity.y *= -1
        if (o.position.y + o.radius > 600 and o.velocity.y > 0):
            o.position.y = 600 - o.radius
            o.velocity.y *= -1

    for i in range(0, len(objectList)):
        circle1 = objectList[i]
        for j in range(i + 1, len(objectList)):
            circle2 = objectList[j]
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

    for o in objectList:
        o.update(deltaTime)
    
    # DRAWING SECTION
    screen.fill(WHITE)

    for o in objectList:
        o.draw()
    
    pygame.display.update()

pygame.quit()
sys.exit()
